from datetime import datetime, timezone

def compute_status(date_str):
    if not date_str or date_str == "null":
        return "missing"
    try:
        target = datetime.strptime(date_str, "%Y-%m-%d").replace(tzinfo=timezone.utc)
        now = datetime.now(timezone.utc)
        days_left = (target - now).days
        if days_left < 0:
            return "expired"
        elif days_left <= 30:
            return "expiring_30"
        elif days_left <= 60:
            return "expiring_60"
        elif days_left <= 90:
            return "expiring_90"
        else:
            return "valid"
    except Exception:
        return "unknown"

def earliest_date(extracted):
    dates = []
    for field in ["notice_deadline", "auto_renewal_date", "contract_end_date"]:
        val = extracted.get(field)
        if val and val != "null":
            dates.append(val)
    return sorted(dates)[0] if dates else None
