# Miijin

Miijin was designed to replace an Excel spreadsheet macro with a proper database-backed application.

**MiijinLunch** reads QR or barcode input from a basic Honeywell optical scanner and inserts records into a PostgreSQL database. Users can optionally type an ID number manually if the scanner is unavailable.

**MiijinReport** generates Excel audit reports based on user input and retrieves data between two selected dates.

---

## Database Configuration

Before running or building either application, you must configure the PostgreSQL connection.

Edit the following file:

```
src/Miijin/MiijinDatabase/MiijinDBInitialization.sql
```

Update the password variable, and run that code on your PostgreSQL server. You may also need to allow remote connections and configure SSL for database access on your Postgres server.

---

## Setup Instructions (Manual / Developer Builds)

### Clone the repository

```bash
git clone https://github.com/BayMillsCC/Miijin.git
cd Miijin
```

---

### Create and activate a virtual environment

#### macOS / Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
```

#### Windows (PowerShell)

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

---

### Install dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

---

## Build Instructions

### Windows

1. Configure `postgres_config.py` with your database settings
2. Build MiijinLunch:
   ```bash
   python setup_lunch.py bdist_msi
   ```
3. Build MiijinReport:
   ```bash
   python setup_report.py bdist_msi
   ```
4. Navigate to the `dist` directory and install the generated MSI files

**Requirements**
- Visual C++ Build Tools v14 or newer
- Windows SDK

Download:  
https://visualstudio.microsoft.com/visual-cpp-build-tools/

---

### Linux (Manual Build)

To keep builds portable across distributions, Miijin is deployed as an **AppImage**.

You may need to install a `fuse` package depending on your distribution.

1. Configure `postgres_config.py` with your database settings
2. Install dependencies (python3, python3-tkinter, and `requirements.txt`)
3. Build MiijinLunch:
   ```bash
   python setup_lunch.py bdist_appimage
   ```
4. Build MiijinReport:
   ```bash
   python setup_report.py bdist_appimage
   ```

---

### macOS

1. Configure `postgres_config.py` with your database settings
2. Build MiijinLunch:
   ```bash
   python setup_lunch.py bdist_mac
   ```
3. Build MiijinReport:
   ```bash
   python setup_report.py bdist_mac
   ```
4. Open the generated DMG and copy the app into `/Applications`

---

## Automated Deployment (AlmaLinux + Ansible)

This deployment method is intended for **headless systems**, kiosks, and managed environments. It builds MiijinLunch as an AppImage and configures the system for automatic login and application startup.

---

### Prerequisites

- AlmaLinux ISO (matching target architecture)
- SSH key pair on the host (control) machine (ssh-keygen)
- Ansible installed on the host machine (on Windows setup WSL and install Ansible in there)
- Network connectivity to the target system
- PostgreSQL credentials

---

### Deployment Steps

1. Burn an AlmaLinux ISO.

2. Boot and install AlmaLinux.
   - Do **not** install a GUI
   - Select a **Minimal / Server** environment
   - Ensure networking is enabled

3. Copy your SSH key to the system after installation.
   - You may need to log in locally to determine the IP address:
     ```bash
     ip addr
     ```
   - From the host machine:
     ```bash
     ssh-copy-id user@<IP_ADDRESS>
     ```

4. Enable passwordless sudo for the wheel group:
   ```bash
   sudo visudo
   ```
   Comment out:
   ```
   %wheel ALL=(ALL) ALL
   ```
   Uncomment:
   ```
   %wheel ALL=(ALL) NOPASSWD: ALL
   ```

5. On the **host machine**, edit the PostgreSQL configuration file:
   ```
   Ansible/files/postgres_config.py
   ```
   Populate it with the correct credentials.  
   A template is available in the `MiijinDatabase` directory.

6. Build the Miijin Lunch AppImage:
   ```bash
   ansible-playbook -i inventory build_miijin_lunch_appimage.yml
   ```

7. Configure automatic login and application autorun:
   ```bash
   ansible-playbook -i inventory deploy_user_autorun.yml
   ```

8. Reboot the target system:
   ```bash
   sudo reboot
   ```

After reboot, the system should automatically log in and launch **MiijinLunch**.

---

## Signing the Windows MSI

If Windows Defender or SmartScreen blocks the MSI, you can sign it using a self-signed certificate.

### Notes

- PowerShell scripts provided:
  - `miijin_cert_generator.ps1`
  - `miijin_msi_signer.ps1`
- MSI files must be moved to `C:\Temp`
- File names must **not contain spaces**

### Steps

1. Install OpenSSL  
   https://slproweb.com/products/Win32OpenSSL.html

2. Generate the certificate:
   ```powershell
   .\miijin_cert_generator.ps1
   ```

3. Sign the MSI:
   ```powershell
   .\miijin_msi_signer.ps1
   ```

4. Verify:
   - Right-click the MSI → Properties
   - Confirm a **Digital Signatures** tab exists

---

## Notes

- PostgreSQL stores timestamps internally in UTC
- Reports are converted to **America/Detroit** time when exported to Excel
- Advanced analytics can be generated with PowerBI or another BI tool
