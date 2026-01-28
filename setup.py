#!/usr/bin/env python3
import subprocess
import sys
import argparse
import os
import re

# ANSI color codes
COLOR_GREEN = "\033[92m"
COLOR_RED = "\033[91m"
COLOR_RESET = "\033[0m"

def run_command(command, description, check_output=False, expected_output_pattern=None):
    """Runs a command and prints its output. Optionally checks output against a pattern."""
    print(f"--- {description} ---")
    try:
        process = subprocess.run(
            command,
            shell=True,
            check=True,
            capture_output=True,
            text=True,
        )
        print(process.stdout)
        if process.stderr:
            print("Stderr:")
            print(process.stderr)

        if check_output and expected_output_pattern:
            if re.search(expected_output_pattern, process.stdout):
                print(f"{COLOR_GREEN}Verification: SUCCESS{COLOR_RESET}")
                return True
            else:
                print(f"{COLOR_RED}Verification: FAILED - Pattern '{expected_output_pattern}' not found.{COLOR_RESET}")
                return False
        return True # Command ran successfully, no output check or check passed
    except subprocess.CalledProcessError as e:
        print(f"Error running command: {command}")
        print(e.stderr)
        return False # Command failed

def create_service_file():
    """Creates the scx_lavd systemd service file."""
    print("--- Creating scx_lavd.service file ---")
    service_content = """[Unit]
Description=SCX LAVD Scheduler
After=network.target

[Service]
Type=simple
ExecStart=/usr/bin/scx_lavd
Restart=on-failure

[Install]
WantedBy=multi-user.target
"""
    command = f"echo '{service_content}' | sudo tee /etc/systemd/system/scx_lavd.service"
    run_command(command, "Creating scx_lavd.service file")

def setup():
    """Runs the initial setup for the Fafnir Build."""
    print("Starting Fafnir Build setup...")

    # 2. Software Installation
    run_command("sudo pacman -Syu --noconfirm", "Updating system")
    run_command(
        "sudo pacman -S --noconfirm scx-scheds gamescope mangoapp btop dmidecode lact",
        "Installing core gaming & monitoring utilities"
    )

    # 3. System Services Configuration
    create_service_file()
    run_command("sudo systemctl daemon-reload", "Reloading systemd daemon")
    run_command("sudo systemctl enable --now scx_lavd", "Enabling scx_lavd service")
    run_command("sudo systemctl enable --now lactd", "Enabling lactd service")

    print("\n--- Manual Configuration Required ---")
    print("Open LACT to configure GPU settings:")
    print("  - Power Cap: Max")
    print("  - Performance Level: P0")
    print("  - GPU Core Offset: +300 MHz")
    print("  - VRAM Offset: +2000 MHz")
    print("  - Apply on Startup: Checked")

    print("\nFafnir Build setup script finished.")
    print("Please review the output and reboot your system.")

def verify():
    """Runs the verification steps for the Fafnir Build."""
    print("\n--- Verification ---")
    print("Running the following commands to verify the setup:")

    results = []

    # Verify Scheduler
    scheduler_cmd = 'ps aux | grep scx_lavd | grep -v grep'
    scheduler_desc = "Verify Scheduler (Must see scx_lavd)"
    results.append(run_command(scheduler_cmd, scheduler_desc, check_output=True, expected_output_pattern='scx_lavd'))

    # Verify RAM Speed & 1:1 Sync
    ram_cmd = 'sudo dmidecode -t memory | grep "Configured"'
    ram_desc = "Verify RAM Speed & 1:1 Sync (Should show Configured Memory Speed: 6200 MT/s)"
    results.append(run_command(ram_cmd, ram_desc, check_output=True, expected_output_pattern='Configured Memory Speed: 6200 MT/s'))

        # Verify Resizable BAR
            bar_cmd = 'nvidia-smi -q -d MEMORY | grep -A 3 "BAR1"'
            bar_desc = "Verify Resizable BAR (Should show Total ~32GB, not 256MB)"
            results.append(run_command(bar_cmd, bar_desc, check_output=True, expected_output_pattern=r'Total\s*:\s*32768 MiB'))        
        # Verify GPU Limits
        gpu_cmd = 'nvidia-smi -q -d POWER'
        gpu_desc = "Verify GPU Limits (Should show Power Limit: 600.00 W)"
        results.append(run_command(gpu_cmd, gpu_desc, check_output=True, expected_output_pattern=r'Power Limit\s*:\s*600\.00 W'))
    if all(results):
        print(f"\n{COLOR_GREEN}All verification checks passed!{COLOR_RESET}")
    else:
        print(f"\n{COLOR_RED}Some verification checks failed. Please review the output.{COLOR_RESET}")

import os

def monitor():
    """Launches the btop system monitor."""
    print("--- Launching btop ---")
    os.system("btop")

def edit_mangohud():
    """Opens the MangoHud config file in nano."""
    print("--- Opening MangoHud config in nano ---")
    config_path = os.path.expanduser("~/.config/MangoHud/MangoHud.conf")
    os.system(f"nano {config_path}")

def main():
    """Main function to display a menu and run the appropriate function."""
    while True:
        print("\nFafnir Build Setup")
        print("1. Setup")
        print("2. Verify")
        print("3. Monitor")
        print("4. Edit MangoHud Config")
        print("5. Quit")

        choice = input("Enter your choice: ")

        if choice == "1":
            setup()
        elif choice == "2":
            verify()
        elif choice == "3":
            monitor()
        elif choice == "4":
            edit_mangohud()
        elif choice == "5":
            break
        else:
            print("Invalid choice. Please try again.")

    # parser = argparse.ArgumentParser(description="Fafnir Build setup script.")
    # parser.add_argument("action", choices=["setup", "verify", "monitor", "edit_mangohud"], help="The action to perform.")
    #
    # args = parser.parse_args()
    #
    # if args.action == "setup":
    #     setup()
    # elif args.action == "verify":
    #     verify()
    # elif args.action == "monitor":
    #     monitor()
    # elif args.action == "edit_mangohud":
    #     edit_mangohud()

if __name__ == "__main__":
    main()

