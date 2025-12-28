import json
from collections import defaultdict
from datetime import datetime, timedelta
from pathlib import Path

WINDOW_MINUTES = 5
TAIL_BYTES = 20 * 1024 * 1024  # 20MB tail for fast mode


# ---------- Helpers ----------

def parse_ts(ts):
    base = ts[:19]  # YYYY-MM-DDTHH:MM:SS
    return datetime.strptime(base, "%Y-%m-%dT%H:%M:%S")

def normalize_severity(sev):
    if sev <= 2:
        return "low"
    if sev == 3:
        return "medium"
    return "high"

def normalize_category(signature, raw_category):
    sig = (signature or "").lower()
    raw = (raw_category or "").lower()

    if "not suspicious" in raw or "info" in sig:
        return "info"
    if "scan" in sig:
        return "scan"
    if "sql" in sig or "web" in sig:
        return "web_exploit"
    if "policy" in sig:
        return "policy_violation"

    return "unknown"

def time_bucket(dt):
    minute = (dt.minute // WINDOW_MINUTES) * WINDOW_MINUTES
    return dt.replace(minute=minute, second=0)

def tail_bytes(path):
    path = Path(path)
    size = path.stat().st_size

    with path.open("rb") as f:
        if size > TAIL_BYTES:
            f.seek(size - TAIL_BYTES)
        data = f.read()

    lines = data.splitlines()
    return (line.decode(errors="ignore") for line in lines)


# ---------- Main builder ----------

def build_incidents_time_window(eve_path, start, end, mode="tail"):
    buckets = defaultdict(lambda: {
        "count": 0,
        "ports": set(),
        "signatures": set(),
        "severities": set()
    })

    if mode == "tail":
        lines = tail_bytes(eve_path)
    else:
        lines = open(eve_path, "r")

    try:
        for line in lines:
            try:
                event = json.loads(line)
            except Exception:
                continue

            if event.get("event_type") != "alert":
                continue

            ts_raw = event.get("timestamp")
            if not ts_raw:
                continue

            try:
                ts = parse_ts(ts_raw)
            except Exception:
                continue

            if ts < start:
                continue

            if ts >= end:
                if mode == "full":
                    break
                continue

            alert = event.get("alert", {})
            category = normalize_category(
                alert.get("signature"),
                alert.get("category")
            )

            if category == "info":
                continue

            src_ip = event.get("src_ip")
            dest_port = event.get("dest_port")

            if not src_ip or not dest_port:
                continue

            bucket = time_bucket(ts)
            key = (category, src_ip, dest_port, bucket)

            b = buckets[key]
            b["count"] += 1
            b["ports"].add(dest_port)
            b["signatures"].add(alert.get("signature"))
            b["severities"].add(
                normalize_severity(alert.get("severity", 3))
            )
    finally:
        if mode == "full":
            lines.close()

    incidents = []

    for (category, src_ip, port, bucket), data in buckets.items():
        severity = (
            "high" if "high" in data["severities"] else
            "medium" if "medium" in data["severities"] else
            "low"
        )

        incidents.append({
            "category": category,
            "severity": severity,
            "time_window": {
                "start": bucket.isoformat() + "Z",
                "end": (bucket + timedelta(minutes=WINDOW_MINUTES)).isoformat() + "Z"
            },
            "source": {"ip": src_ip},
            "target": {"port": port},
            "alerts": data["count"],
            "evidence": {
                "signatures": list(data["signatures"])
            }
        })

    return incidents
