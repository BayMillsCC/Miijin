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