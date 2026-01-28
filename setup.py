#!/usr/bin/env python3
import subprocess
import sys

def run_command(command, description):
    """Runs a command and prints its output."""
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
    except subprocess.CalledProcessError as e:
        print(f"Error running command: {command}")
        print(e.stderr)
        sys.exit(1)

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

def main():
    """Main function to run the setup script."""
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
    print("\n--- Verification ---")
    print("After rebooting, run the following commands to verify the setup:")
    print('ps aux | grep scx_lavd')
    print('sudo dmidecode -t memory | grep "Configured"')
    print('nvidia-smi -q -d MEMORY | grep -A 3 "BAR1"')
    print('nvidia-smi -q -d POWER')

if __name__ == "__main__":
    main()

