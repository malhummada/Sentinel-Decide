import json
import sys
from datetime import datetime, timedelta
from pathlib import Path

from explainer.incident_builder import build_incidents_time_window
from explainer.decision_engine import propose_decision
from explainer.decision_aggregator import aggregate_decisions
from explainer.nftables_file_exporter import export_nftables_file
from explainer.nftables_installer import install_nftables_file

EVE_PATH = Path("/var/log/suricata/eve.json")
OUT_DIR = Path("output")

# ---------- Time parsing ----------

def parse_flexible_time(value):
    for fmt in (
        "%Y-%m-%dT%H:%M:%S",
        "%Y-%m-%dT%H:%M",
        "%Y-%m-%d",
    ):
        try:
            return datetime.strptime(value, fmt)
        except ValueError:
            pass
    raise ValueError(f"Invalid time format: {value}")

def parse_human_time(args):
    now = datetime.now()

    # auto → last 5 minutes
    if args == ["auto"]:
        return now - timedelta(minutes=5), now

    # last <Nm|Nh|Nd>
    if len(args) == 2 and args[0] == "last":
        value = args[1]

        if len(value) < 2 or not value[:-1].isdigit():
            raise ValueError(
                f"Invalid duration format: {value} (use 5m, 2h, 1d)"
            )

        num = int(value[:-1])
        unit = value[-1]

        if unit not in ("m", "h", "d"):
            raise ValueError(
                f"Invalid duration unit: {unit} (use m, h, d)"
            )

        if unit == "m":
            return now - timedelta(minutes=num), now
        if unit == "h":
            return now - timedelta(hours=num), now
        if unit == "d":
            return now - timedelta(days=num), now

    # since <DATE>
    if len(args) == 2 and args[0] == "since":
        start = parse_flexible_time(args[1])
        return start, now

    # between <DATE> <DATE>
    if len(args) == 3 and args[0] == "between":
        start = parse_flexible_time(args[1])
        end = parse_flexible_time(args[2])
        return start, end

    return None, None

# ---------- Main ----------

def print_usage():
    print("Usage examples:")
    print("  python3 -m tools.run_pipeline auto")
    print("  python3 -m tools.run_pipeline last 5m")
    print("  python3 -m tools.run_pipeline last 2h")
    print("  python3 -m tools.run_pipeline last 1d")
    print("  python3 -m tools.run_pipeline since 2025-12-20")
    print("  python3 -m tools.run_pipeline between 2025-12-20 2025-12-27")
    print("  python3 -m tools.run_pipeline 2025-12-27T02:40:00 2025-12-28T02:45:00")

def main():
    args = sys.argv[1:]

    try:
        start, end = parse_human_time(args)
    except ValueError as e:
        print(f"Error: {e}")
        print_usage()
        sys.exit(1)

    # Fallback: ISO <start> <end>
    if not start or not end:
        if len(args) == 2:
            try:
                start = parse_flexible_time(args[0])
                end = parse_flexible_time(args[1])
            except ValueError as e:
                print(f"Error: {e}")
                print_usage()
                sys.exit(1)
        else:
            print_usage()
            sys.exit(1)

    if start >= end:
        print("Error: Invalid time window (start >= end)")
        sys.exit(1)


    WINDOW_DAYS = (end - start).days
    TAIL_MAX_DAYS = 2

    if WINDOW_DAYS > TAIL_MAX_DAYS:
        scan_mode = "full"
        print("[INFO] Large time window detected")
        print("[INFO] Switching to full log scan mode")
    else:
        scan_mode = "tail"



    # ---------- Incident analysis ----------
    try:
        incidents = build_incidents_time_window(
            str(EVE_PATH),
            start,
            end,
            mode=scan_mode
        )
    except KeyboardInterrupt:
        print("\n[INFO] Analysis interrupted by user.")
        print("[INFO] No changes were applied.")
        sys.exit(130)
    

    OUT_DIR.mkdir(exist_ok=True)

    incidents_file = OUT_DIR / "incidents.json"
    with open(incidents_file, "w") as f:
        json.dump(incidents, f, indent=2)

    print(f"[OK] Time window : {start} -> {end}")
    print(f"[OK] Incidents   : {len(incidents)}")
    print(f"[OK] Output      : {incidents_file}")

    # ---------- Decisions ----------
    decisions = [propose_decision(i) for i in incidents]

    decisions_file = OUT_DIR / "decisions.json"
    with open(decisions_file, "w") as f:
        json.dump(decisions, f, indent=2)

    print(f"[OK] Decisions   : {len(decisions)}")
    print(f"[OK] Output      : {decisions_file}")

    summary = aggregate_decisions(decisions)

    summary_file = OUT_DIR / "decision_summary.json"
    with open(summary_file, "w") as f:
        json.dump(summary, f, indent=2)

    print(f"[OK] Decision summary : {len(summary)}")
    print(f"[OK] Output           : {summary_file}")

    # ---------- nftables ----------
    if not summary:
        print("[OK] No actionable decisions found")
        print("[OK] nftables step skipped")
        return

    nft_output = export_nftables_file(summary)

    nft_file = OUT_DIR / "sentinel-decide.nft"
    with open(nft_file, "w") as f:
        f.write(nft_output)

    print(f"[OK] nftables file generated : {nft_file}")

    install_nftables_file(nft_file)

if __name__ == "__main__":
    main()
