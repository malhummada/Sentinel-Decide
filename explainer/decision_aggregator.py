from collections import defaultdict

def aggregate_decisions(decisions, window_minutes=5):
    per_source = defaultdict(lambda: {
        "incidents": 0,
        "ports": set()
    })

    for d in decisions:
        src_ip = d["scope"]["src_ip"]
        port = d["scope"]["dest_port"]

        per_source[src_ip]["incidents"] += 1
        per_source[src_ip]["ports"].add(port)

    summaries = []

    for src_ip, data in per_source.items():
        incident_count = data["incidents"]
        port_count = len(data["ports"])

        decision = "observe"
        reason = "low activity"
        confidence = 0.2
        expires = "5m"

        if incident_count >= 10 and port_count >= 10:
            decision = "rate_limit"
            reason = "multiple incidents across many ports in short time"
            confidence = 0.65
            expires = "10m"

        summaries.append({
            "src_ip": src_ip,
            "window": f"{window_minutes}m",
            "incidents": incident_count,
            "ports": port_count,
            "decision": decision,
            "reason": reason,
            "confidence": confidence,
            "expires_in": expires
        })

    return summaries
