from datetime import datetime, timedelta
from collections import defaultdict

# Track scan events
qr_scan_log = defaultdict(list)

FRAUD_WINDOW = timedelta(seconds=30)

def log_qr_scan(merchant_id: str) -> bool:
    now = datetime.utcnow()
    recent_scans = qr_scan_log[merchant_id]

    # Keep only recent entries
    qr_scan_log[merchant_id] = [t for t in recent_scans if now -t < FRAUD_WINDOW]
    qr_scan_log[merchant_id].append(now)

    # Detec duplicate/multiple use
    return len(qr_scan_log[merchant_id]) > 3