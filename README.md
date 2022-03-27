# Miijin

A program that collects user IDs and stores it in a database. 

This program is quite simple, but suits the needs to simply log who is eating lunch and when. 

It reads in QR code or barcode input from a basic honeywell optical scanner and inserts it into a MS-SQL database.

Prior to building it with cx_freeze you will need to modify mssql_config.py to match the config settings for your DB server. 
