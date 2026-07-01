import json
import os
from compute_status import compute_status, earliest_date

# Simulate extracted contract data (no real PDF needed)
sample_contracts = [
    {
        "vendor_name": "Acme Software Ltd",
        "contract_end_date": "2026-08-15",
        "auto_renewal_date": "2026-07-15",
        "notice_deadline": "2026-07-01",
        "contract_value": "$12,000/year",
        "key_terms": "Auto-renews annually with 30-day notice required to cancel."
    },
    {
        "vendor_name": "CloudHost Inc",
        "contract_end_date": "2025-12-31",
        "auto_renewal_date": "2025-12-01",
        "notice_deadline": "2025-11-01",
        "contract_value": "$4,800/year",
        "key_terms": "Hosting agreement with SLA review at renewal."
    },
    {
        "vendor_name": "Office Supplies Co",
        "contract_end_date": "2027-03-01",
        "auto_renewal_date": None,
        "notice_deadline": None,
        "contract_value": "$600/year",
        "key_terms": "Fixed term supply agreement, no auto-renewal."
    },
]

print("Contract Renewal Monitor — Demo Run")
print("=" * 40)

results = []
for contract in sample_contracts:
    due_date = earliest_date(contract)
    status = compute_status(due_date)
    results.append({
        "vendor": contract["vendor_name"],
        "status": status,
        "due_date": due_date,
        "value": contract["contract_value"],
    })
    print(f"{contract['vendor_name']}: {status} (due: {due_date})")

print("=" * 40)
print(f"Total: {len(results)} contracts")
critical = [r for r in results if r["status"] in ("expired", "expiring_30")]
print(f"Needs attention: {len(critical)}")
print("Demo complete.")
