import shutil
import subprocess
from pathlib import Path

TARGET_PATH = Path("/etc/nftables.d/50-cyphorn-guard.nft")

def install_nftables_file(source_file):
    print("\nGenerated nftables rules file:")
    print(f"  {source_file}")

    print("\nChoose action:")
    print("  [1] Do nothing (recommended)")
    print("  [2] Copy file to /etc/nftables.d/")
    print("  [3] Copy and apply rules now (ADVANCED)")

    choice = input("\nSelection [1]: ").strip() or "1"

    if choice == "1":
        print("No action taken.")
        return

    if choice not in ("2", "3"):
        print("Invalid selection.")
        return

    # ---- Copy step ----
    try:
        shutil.copy(source_file, TARGET_PATH)
        print(f"[OK] File copied to {TARGET_PATH}")
    except PermissionError:
        print("[ERROR] Permission denied. Run as root to copy.")
        return

    if choice != "3":
        print("File copied. Review it before applying.")
        return

    # ---- Warning before apply ----
    print("\nWARNING:")
    print("You are about to APPLY nftables rules to the live system.")
    print("This may affect network connectivity.")
    print("Make sure you have console access.")

    confirm = input("\nType 'apply' to continue: ").strip()
    if confirm != "apply":
        print("Apply cancelled.")
        return

    # ---- Validate rules ----
    print("\nValidating nftables rules...")
    try:
        subprocess.run(
            ["nft", "-c", "-f", str(TARGET_PATH)],
            check=True,
            capture_output=True,
            text=True,
            timeout=10
        )
        print("[OK] Validation successful.")
    except subprocess.CalledProcessError as e:
        print("[ERROR] Validation failed:")
        print(e.stderr)
        return

    # ---- Apply rules ----
    print("\nApplying nftables rules...")
    try:
        subprocess.run(
            ["nft", "-f", str(TARGET_PATH)],
            check=True,
            capture_output=True,
            text=True,
            timeout=10
        )
        print("[OK] nftables rules applied successfully.")
    except subprocess.CalledProcessError as e:
        print("[ERROR] Failed to apply nftables rules:")
        print(e.stderr)
