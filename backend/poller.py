import os
import sys
import time
import json
import tempfile
import requests
from datetime import datetime, timezone

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from extract_dates import extract_contract_dates
from compute_status import compute_status, earliest_date

SUPABASE_URL = os.environ["SUPABASE_URL"]
SUPABASE_KEY = os.environ["SUPABASE_SERVICE_KEY"]
PRODUCT_ID = os.environ.get("PRODUCT_ID", "contract-renewal-monitor")
JOB_TYPE = "contract_audit"
POLL_INTERVAL = 60

HEADERS = {
    "apikey": SUPABASE_KEY,
    "Authorization": f"Bearer {SUPABASE_KEY}",
    "Content-Type": "application/json",
}

def fetch_pending_jobs():
    url = f"{SUPABASE_URL}/rest/v1/jobs?status=eq.pending&job_type=eq.{JOB_TYPE}&product_id=eq.{PRODUCT_ID}&select=*"
    r = requests.get(url, headers=HEADERS, timeout=15)
    r.raise_for_status()
    return r.json()

def update_job(job_id, fields):
    url = f"{SUPABASE_URL}/rest/v1/jobs?id=eq.{job_id}"
    r = requests.patch(url, headers={**HEADERS, "Prefer": "return=minimal"}, json=fields, timeout=15)
    r.raise_for_status()

def download_file(path, dest):
    url = f"{SUPABASE_URL}/storage/v1/object/uploads/{path}"
    r = requests.get(url, headers=HEADERS, timeout=30)
    r.raise_for_status()
    with open(dest, "wb") as f:
        f.write(r.content)

def insert_records(rows):
    url = f"{SUPABASE_URL}/rest/v1/records"
    r = requests.post(url, headers={**HEADERS, "Prefer": "return=minimal"}, json=rows, timeout=30)
    r.raise_for_status()

def process_job(job):
    job_id = job["id"]
    customer_id = job["customer_id"]
    input_paths = job.get("input_file_paths") or []
    if not input_paths:
        single = job.get("input_file_path")
        if single:
            input_paths = [single]

    if not input_paths:
        update_job(job_id, {"status": "failed", "error_message": "No input files"})
        return

    update_job(job_id, {"status": "processing"})

    workdir = tempfile.mkdtemp()
    db_rows = []
    processed = 0
    errors = 0

    for storage_path in input_paths:
        fname = storage_path.split("/")[-1]
        vendor_name = fname.replace(".pdf", "").replace("_", " ").replace("-", " ")
        local_path = os.path.join(workdir, fname)
        try:
            download_file(storage_path, local_path)
            extracted = extract_contract_dates(local_path, vendor_name)
            due_date = earliest_date(extracted)
            status = compute_status(due_date)
            db_rows.append({
                "product_id": PRODUCT_ID,
                "customer_id": customer_id,
                "title": extracted.get("vendor_name") or vendor_name,
                "status": status,
                "details": extracted,
                "source_file_path": storage_path,
                "due_date": due_date,
                "label": extracted.get("contract_value"),
            })
            processed += 1
        except Exception as e:
            print(f"WARNING: failed {fname}: {e}", file=sys.stderr)
            errors += 1

    if db_rows:
        insert_records(db_rows)

    critical = sum(1 for r in db_rows if r["status"] in ("expired", "expiring_30", "missing"))
    update_job(job_id, {
        "status": "completed",
        "result_summary": {"total": processed, "critical": critical, "errors": errors},
        "completed_at": datetime.now(timezone.utc).isoformat(),
    })
    print(f"Job {job_id} complete: {processed} contracts, {critical} critical")

def main():
    print(f"Contract Renewal poller started. Polling every {POLL_INTERVAL}s.")
    while True:
        try:
            jobs = fetch_pending_jobs()
            for job in jobs:
                try:
                    process_job(job)
                except Exception as e:
                    print(f"ERROR job {job['id']}: {e}", file=sys.stderr)
                    try:
                        update_job(job["id"], {"status": "failed", "error_message": str(e)[:500]})
                    except Exception:
                        pass
        except Exception as e:
            print(f"ERROR fetching jobs: {e}", file=sys.stderr)
        time.sleep(POLL_INTERVAL)

if __name__ == "__main__":
    main()
