# Miijin

This project was designed to replace an Excel spreadsheet macro with a proper database.
MiijinLunch reads in QR or barcode input from a basic honeywell optical scanner and inserts it into an MS-SQL database.
The user can optionally type in an ID number if the reader is offline.

MiijinReport generates an Excel spreadsheet based off user input to create an audit file and gather data between two dates. 

Prior to building either application you will need to modify mssql_config.py to match the config settings for your DB server. 


## Build Instructions

### Pre-requisite Packages:

The following packages are needed to build these project files:

* Babel
* XlsxWriter
* cx_freeze
* cx_logging
* MiijinDatabase
* pip
* python >= 3.8 
* pyodbc
* pytz
* setuptools
* tk
* tkcalendar
* wheel

You will also need the ODBC database driver to talk with the SQL server. You can download that
[here](https://docs.microsoft.com/en-us/sql/connect/odbc/download-odbc-driver-for-sql-server?view=sql-server-ver15) (I used 64 bit drivers). 

Additionally, if you are on Windows you will need to install the Visual C++ build tools version 14 or greater, and the Windows SDK. 
You can download those tools [here](https://visualstudio.microsoft.com/visual-cpp-build-tools/).

### Windows:
1. Configure mssql_config.py with respective options
2. Run ```python setup_lunch.py bdist_msi``` to generate the MiijinLunch Program (to collect IDs)
3. Run ```python setup_report.py bdist_msi```  to generate the MiijinReport Program (to Export Data to Excel)
4. Navigate to ```dist``` and install the respective MSI. 

### MacOS:

1. Configure mssql_config.py with respective options
2. Run ```python setup_lunch.py bdist_mac``` to generate the MiijinLunch Program (to collect IDs)
3. Run ```python setup_report.py bdist_mac```  to generate the MiijinReport Program (to Export Data to Excel)
4. Open the newly generated DMG file and copy it to your Applications directory


## Adding Certificate for MSI
If Windows Defender is proving problematic you can sign the MSI with either a self-signed certificate, or a proper EV 
certificate. I didn't have an EV cert at the time of this writing (and I doubt you'd have a CA infra available), so I will provide instructions for a self-signed cert.

* Note: I wrote two PowerShell scripts to aid with this. Run cert_generator first then msi_signer
* You will need to move the MSI files to C:\Temp beforehand and rename them to not include spaces

1. Install OpenSSL from [here](https://slproweb.com/products/Win32OpenSSL.html)
2. Run ```miijin_cert_generator.ps1``` and supply it with relevant information.
3. Run ```miijin_msi_signer.ps1``` and supply it with relevant information.
4. If you go to the properties window on either MSI file you should now have a "Digital Signatures" tab. 
5. If you want your computer to trust the cert you used you can directly install it by going to "Details" on the "Digital Signatures" tab.
6. Click "View Certificate".
7. Click "Install".
8. In the new window that pops up choose to add it to the "Local Machine".
9. Choose to "Place all certificates in the following store" and click "Browse".
10. Choose "Trusted Root Certification Authorities" and click "OK".
11. Follow through the rest of the prompts and the certificate should now be installed.

You can also hand out the .crt file you generated and have a user install it by clicking on that and following steps 8-11 above.

Windows Smartscreen may still complain about the files, but at this time you can just run the file anyway, and it should allow it depending on your organizational policies.