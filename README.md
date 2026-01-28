# Fafnir Build: High-Performance Linux Gaming Config

**System Target:** Ryzen 7 9800X3D | RTX 5090 | CachyOS (Arch)
**Goal:** Maximize frame consistency (1% lows) and unleash hardware limits safely.

---

This guide provides the steps to configure a high-performance Linux gaming environment. The process is streamlined using a setup script.

## 1. BIOS Configuration (The Foundation)
**⚠️ Critical:** Apply these settings before installing the OS or booting for the first time.
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

## 2. Automated Setup Script

After completing the BIOS configuration and installing your OS, use the provided Python script to automate the software installation and system configuration.

### How to Use the Script

1.  **Open a terminal** in this directory.
2.  **Make the script executable** (if you haven't already):
    ```bash
    chmod +x setup.py
    ```
3.  **Run the script with `sudo`:**
    ```bash
    sudo ./setup.py
    ```
4.  **Follow the on-screen menu:**

    *   **1. Setup:** Choose this option first. It will:
        *   Update your system packages.
        *   Install necessary gaming and monitoring utilities (`scx-scheds`, `gamescope`, `mangoapp`, `btop`, `dmidecode`, `lact`).
        *   Create and enable systemd services for `scx_lavd` (CPU scheduler) and `lactd` (GPU tuning).
    *   **2. Verify:** After running the setup and rebooting, choose this option to automatically check that everything is configured correctly. It will verify:
        *   The `scx_lavd` scheduler is active.
        *   RAM speed and sync mode.
        *   Resizable BAR is enabled and correctly sized.
        *   GPU power limits are set.
    *   **3. Monitor:** Launches `btop` for real-time system monitoring.
    *   **4. Edit MangoHud Config:** Opens the MangoHud configuration file (`~/.config/MangoHud/MangoHud.conf`) in `nano` for easy editing.
    *   **5. Quit:** Exits the script.

---

## 3. Manual GPU Tuning (LACT)

The setup script enables the `lactd` daemon, but you must configure the GPU settings manually via the LACT GUI.

1.  **Open LACT.**
2.  **Configure Settings:**
    *   **Power Cap:** Set to Max (e.g., 600W).
    *   **Performance Level:** Force P0 (Highest).
    *   **Clocks:**
        *   **GPU Core Offset:** +300 MHz
        *   **VRAM Offset:** +2000 MHz (Monitor for artifacts; drop to +1500 if unstable).
3.  **Apply and Save:** Ensure **"Apply on Startup"** is checked.

---

## 4. Steam Launch Options

Use these flags for Cyberpunk 2077 and other heavy titles to enforce the compositor and power profiles.

*   **Standard Command:**
    ```bash
    gamescope --mangoapp -- game-performance %command%
    ```
    *   `gamescope`: Handles windowing and frame pacing.
    *   `--mangoapp`: Injects the performance overlay.
    *   `game-performance`: CachyOS optimized "GameMode" (governor tweaks).

*   **If using DLSS Frame Gen (DLSS 3.5):**
    ```bash
    PROTON_ENABLE_NVAPI=1 gamescope --mangoapp -- game-performance %command%
    ```

---
Your system should now be fully optimized for a high-performance gaming experience. Enjoy!