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

Update the password variable, and run that code on your Postgres server. Please note you may need to also allow remote connections and configure SSL for your database connections.




Additionally, you will need to edit the following file:

```
src/Miijin/MiijinDatabase/postgres_config.py
```

And update the following variables:

```python
host = "localhost"
database = "miijinprod"
username = "miijin_app"
password = "YOUR_PASSWORD"
port = 5432
sslmode = "require"
```

---

## Requirements

### Python Version
- **Python 3.14 or newer**

### Python Dependencies

All runtime dependencies are listed in `requirements.txt`.

Install them with:

```bash
pip install -r requirements.txt
```

Contents of `requirements.txt`:

```txt
Babel
XlsxWriter
psycopg
psycopg-binary
pytz
tkcalendar
cx_Freeze
cx_Logging
wheel
```

### Notes
- `tk` is included with Python on macOS and Windows
- `pip`, `setuptools`, and Python itself are **not** listed in `requirements.txt`
- `MiijinDatabase` is part of this repository, not a pip package but is still required

---

## Setup Instructions

### Clone the repository

```bash
git clone https://github.com/BayMillsCC/Miijin.git
cd Miijin
```

---

###  Create and activate a virtual environment

#### macOS / Linux

```bash
python3.14 -m venv .venv
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

### Run the application (for testing, go to Build Instructions for an Executable)

#### MiijinLunch

```bash
python src/Miijin/MiijinLunch/MiijinLunch.py
```

#### MiijinReport

```bash
python src/Miijin/MiijinReport/MiijinReport.py
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

Windows requires **Visual C++ Build Tools v14 or newer** and the **Windows SDK**

Download here:  
https://visualstudio.microsoft.com/visual-cpp-build-tools/

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

## Signing the Windows MSI

If Windows Defender or SmartScreen blocks the MSI, you can sign it using a self-signed certificate.

### Notes
- Two PowerShell scripts are provided:
  - `miijin_cert_generator.ps1`
  - `miijin_msi_signer.ps1`
- MSI files must be moved to `C:\Temp`
- File names **must not contain spaces**

### Steps

1. Install OpenSSL  
   https://slproweb.com/products/Win32OpenSSL.html

2. Run the certificate generator:
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

### Trusting the Certificate (Optional)

1. Open the MSI Properties → Digital Signatures
2. Click **View Certificate**
3. Click **Install Certificate**
4. Choose **Local Machine**
5. Place it in **Trusted Root Certification Authorities**
6. Complete the wizard

---

## Notes

- PostgreSQL stores timestamps in UTC internally
- Reports are converted to **America/Detroit** time when exported to Excel
- Advanced Analytics can be generated with PowerBI or another BI tool
- Excel does not support timezone-aware timestamps; conversion is handled explicitly in code
