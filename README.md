# Fafnir Build: High-Performance Linux Gaming Config

**System Target:** Ryzen 7 9800X3D | RTX 5090 | CachyOS (Arch)
**Goal:** Maximize frame consistency (1% lows) and unleash hardware limits safely.

---

## 1. BIOS Configuration (The Foundation)
**⚠️ Critical:** Apply these settings before installing OS or booting.
*Access BIOS with `Del` or `F2`.*

### **CPU (Ryzen 7 9800X3D)**
* **Precision Boost Overdrive (PBO):** Advanced
* **Curve Optimizer:** All Cores -> **Negative 20** (`-20`)
    * *Note: If unstable, revert to -15.*

### **Memory (DDR5-6000+ Optimization)**
* **Frequency:** **DDR5-6200**
    * *Warning:* This requires a high-quality memory controller. If boot fails, drop to 6000.
* **Memory Controller (UCLK):** **UCLK=MEMCLK**
    * *Critical:* Forces 1:1 Sync Mode (3100 MHz). Do NOT leave on Auto (1:2).
* **FCLK:** Auto (Defaults to ~2000-2133 MHz)
* **Voltage Check:** Ensure `VSOC` / `VDDIO_MEM` is **≤ 1.25V**. If Auto sets it to >1.30V, manually lower it.

### **PCIe / System**
* **Above 4G Decoding:** Enabled
* **Re-Size BAR Support:** Enabled
* **CSM Support:** Disabled (UEFI Only)

---

## 2. Software Installation
Install the necessary gaming, monitoring, and tuning utilities.

```bash
# Update System
sudo pacman -Syu

# Install Core Gaming & Monitoring Utilities
# scx-scheds: Scheduler extensions
# gamescope: Micro-compositor for frame pacing
# lact: GPU tuning/overclocking for Linux
# btop: System monitoring
# dmidecode: Hardware verification
sudo pacman -S scx-scheds gamescope mangoapp btop dmidecode lact

## 3. System Services Configuration
### A. CPU Scheduler (SCX_LAVD)

We bypass the default scx_loader to force the lavd (Latency-critical) scheduler directly.

    Create the Service File:
    Bash

    sudo nano /etc/systemd/system/scx_lavd.service

    Paste Content:
    Ini, TOML

    [Unit]
    Description=SCX LAVD Scheduler
    After=network.target

    [Service]
    Type=simple
    ExecStart=/usr/bin/scx_lavd
    Restart=on-failure

    [Install]
    WantedBy=multi-user.target

    Enable the Service:
    Bash

    sudo systemctl daemon-reload
    sudo systemctl enable --now scx_lavd

### B. GPU Tuning (LACT)

We use lact to handle Power Limits and Overclocking (replacing manual nvidia-smi scripts).

    Enable the Daemon:
    Bash

    sudo systemctl enable --now lactd

    Configure Settings (GUI):

        Open LACT.

        Power Cap: Set to Max (600W).

        Performance Level: Force P0 (Highest).

        Clocks:

            GPU Core Offset: +300 MHz

            VRAM Offset: +2000 MHz (Monitor for artifacts; drop to +1500 if unstable).

        Apply: Ensure "Apply on Startup" is checked.

## 4. Steam Launch Options

Use these flags for Cyberpunk 2077 and other heavy titles to enforce the compositor and power profiles.

Standard Command:
Bash

gamescope --mangoapp -- game-performance %command%

    gamescope: Handles windowing and frame pacing.

    --mangoapp: Injects the performance overlay.

    game-performance: CachyOS optimized "GameMode" (governor tweaks).

If using DLSS Frame Gen (DLSS 3.5):
Bash

PROTON_ENABLE_NVAPI=1 gamescope --mangoapp -- game-performance %command%

## 5. Verification Checklist

Run these commands after a reboot to confirm the stack is active.

    Verify Scheduler (Must see scx_lavd):
    Bash

    ps aux | grep scx_lavd

    Verify RAM Speed & 1:1 Sync:
    Bash

    # Should show "Configured Memory Speed: 6200 MT/s"
    sudo dmidecode -t memory | grep "Configured"

    Verify Resizable BAR:
    Bash

    # Should show Total ~32GB (not 256MB)
    nvidia-smi -q -d MEMORY | grep -A 3 "BAR1"

    Verify GPU Limits:
    Bash

    # Should show Power Limit: 600.00 W
    nvidia-smi -q -d POWER
