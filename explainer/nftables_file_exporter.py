from datetime import datetime

def export_nftables_file(decision_summary):
    lines = []
    
    if not decision_summary:
        return (
            "# Cyphorn Guard\n"
            "# No actionable decisions generated\n"
            "# This file intentionally installs no rules\n"
        )

    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    lines.append("# =============================================")
    lines.append("# Cyphorn Guard - nftables rules")
    lines.append(f"# Generated at: {now}")
    lines.append("# Mode: manual review required")
    lines.append("# This file is NOT applied automatically")
    lines.append("# =============================================")
    lines.append("")

    lines.append("table inet cyphorn {")
    lines.append("    chain guard {")
    lines.append("        type filter hook input priority 0;")
    lines.append("        policy accept;")
    lines.append("")

    for entry in decision_summary:
        src_ip = entry["src_ip"]
        decision = entry["decision"]
        expires = entry["expires_in"]

        if decision == "observe":
            lines.append(
                f"        # observe only: {src_ip} (window {expires})"
            )
            continue

        if decision == "rate_limit":
            lines.append(
                f"        # rate limit {src_ip} for {expires}"
            )
            lines.append(
                f"        ip saddr {src_ip} limit rate 25/second accept"
            )
            lines.append("")
            continue

        if decision == "block":
            lines.append(
                f"        # temporary block {src_ip} for {expires}"
            )
            lines.append(
                f"        ip saddr {src_ip} drop"
            )
            lines.append("")
            continue

    lines.append("    }")
    lines.append("}")

    return "\n".join(lines)
