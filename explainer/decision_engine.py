import hashlib

def incident_id(incident):
    base = f"{incident['category']}:{incident['source']['ip']}:{incident['target']['port']}"
    return hashlib.sha1(base.encode()).hexdigest()[:12]

def propose_decision(incident):
    category = incident["category"]
    severity = incident["severity"]
    alerts = incident["alerts"]

    decision = "observe"
    reason = "no action required"
    confidence = 0.2
    expires = "5m"

    if category == "scan" and alerts >= 20:
        decision = "rate_limit"
        reason = "scan activity within time window"
        confidence = 0.6
        expires = "10m"

    elif category == "web_exploit" and severity == "high" and alerts >= 5:
        decision = "block"
        reason = "repeated high severity web exploit attempts"
        confidence = 0.9
        expires = "30m"

    elif category == "policy_violation":
        decision = "observe"
        reason = "policy violation detected"
        confidence = 0.4
        expires = "5m"

    return {
        "incident_id": incident_id(incident),
        "decision": decision,
        "scope": {
            "src_ip": incident["source"]["ip"],
            "dest_port": incident["target"]["port"]
        },
        "reason": reason,
        "confidence": confidence,
        "expires_in": expires
    }
