import pyodbc
import datetime


class MiijinDatabase:
    def __init__(self, driver, server, database, username, password, trusted):
        self.driver = driver
        self.server = server
        self.database = database
        self.username = username
        self.password = password
        self.trusted = trusted

        conn = pyodbc.connect('DRIVER=' + self.driver + ';' + 'SERVER=' + self.server + ';DATABASE=' + self.database +
                              ';UID=' + self.username + ';PWD=' + self.password +
                              ';TrustServerCertificate=' + self.trusted)

        self.cursor = conn.cursor()

    def select_query(self):
        self.cursor.execute('''SELECT employees.[employeeLunchID], employees.[employeeID], employees.[timeIDScanned] 
                    FROM MiijinDB.MiijinProd.employeeLunchRecords employees''')

        return self.cursor.fetchall()

    def perform_insert(self, userid):
        if len(str(userid)) == 7:
            self.cursor.execute('''insert into MiijinDB.MiijinProd.studentLunchRecords(studentID, timeIDScanned)
                                    values (?, ?)''', int(userid), datetime.datetime.now())
        else:
            self.cursor.execute('''insert into MiijinDB.MiijinProd.employeeLunchRecords(employeeID, timeIDScanned)
                                                values (?, ?)''', int(userid), datetime.datetime.now())
        self.cursor.commit()
