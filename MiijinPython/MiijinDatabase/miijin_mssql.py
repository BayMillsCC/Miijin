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

    def get_lunches(self, date_start, date_end, dbtype):
        date_start = date_start + ' 00:00:00'
        date_end = date_end + ' 23:59:59'

        if dbtype == 'stud':
            self.cursor.execute('''SELECT students.[studentLunchID], students.[studentID],
                                    students.[timeIDScanned] FROM [MiijinDB].MiijinProd.studentLunchRecords students
                                    WHERE students.timeIDScanned BETWEEN
                                    ? AND
                                    ?''', date_start, date_end)
        else:
            self.cursor.execute('''SELECT employees.[employeeLunchID], employees.[employeeID],
                                    employees.[timeIDScanned] FROM [MiijinDB].MiijinProd.employeeLunchRecords employees
                                    WHERE employees.timeIDScanned BETWEEN
                                    ? AND
                                    ?''', date_start, date_end)

        return self.cursor.fetchall()

    def perform_insert(self, userid):
        if len(str(userid)) == 7:
            self.cursor.execute('''insert into MiijinDB.MiijinProd.studentLunchRecords(studentID, timeIDScanned)
                                    values (?, ?)''', int(userid), datetime.datetime.now())
        else:
            self.cursor.execute('''insert into MiijinDB.MiijinProd.employeeLunchRecords(employeeID, timeIDScanned)
                                                values (?, ?)''', int(userid), datetime.datetime.now())
        self.cursor.commit()
