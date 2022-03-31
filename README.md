# Miijin

A program that collects user IDs and stores it in a database. 

This program is quite simple, but suits the needs to simply log who is eating lunch and when. 

It reads in QR code or barcode input from a basic honeywell optical scanner and inserts it into a MS-SQL database.

Prior to building it you will need to modify mssql_config.py to match the config settings for your DB server. 


##Build Instructions

###MacOS:

1. Configure mssql_config.py with respective options
2. Run ```python setup_lunch.py bdist_mac``` to generate the MiijinLunch Program (to collect IDs)
3. Run ```python setup_report.py bdist_mac```  to generate the MiijinReport Program (to Export Data to Excel)
