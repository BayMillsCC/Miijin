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

    def get_daily_lunches(self, start_date, end_date, dbtype):
        date_start = start_date + ' 00:00:00'
        date_end = end_date + ' 23:59:59'

        if dbtype == 'stud':
            self.cursor.execute('''SELECT students.[studentID], students.[timeIDScanned] AS "total_lunches"
                                                    FROM [MiijinDB].MiijinProd.studentLunchRecords students
                                                    WHERE students.timeIDScanned BETWEEN
                                                    ? AND
                                                    ?
                                                    ORDER BY students.[timeIDScanned] ASC
                                                    ''', date_start, date_end)
        else:
            self.cursor.execute('''SELECT employees.[employeeID], employees.[timeIDScanned] AS "total_lunches" 
                                                    FROM [MiijinDB].MiijinProd.employeeLunchRecords employees
                                                    WHERE employees.timeIDScanned BETWEEN
                                                    ? AND
                                                    ?
                                                    ORDER BY employees.[timeIDScanned] ASC
                                                    ''', date_start, date_end)

        return self.cursor.fetchall()

    def get_individual_lunches(self, id_number, start_date, end_date, dbtype):
        date_start = start_date + ' 00:00:00'
        date_end = end_date + ' 23:59:59'

        if dbtype == 'stud':
            self.cursor.execute('''SELECT students.[studentID], students.[timeIDScanned] AS "total_lunches"
                                            FROM [MiijinDB].MiijinProd.studentLunchRecords students
                                            WHERE students.[studentID] = ? AND students.timeIDScanned BETWEEN
                                            ? AND
                                            ?
                                            ORDER BY students.[timeIDScanned] ASC
                                            ''', id_number, date_start, date_end)
        else:
            self.cursor.execute('''SELECT employees.[employeeID], employees.[timeIDScanned] AS "total_lunches" 
                                            FROM [MiijinDB].MiijinProd.employeeLunchRecords employees
                                            WHERE employees.[employeeID] = ? AND employees.timeIDScanned BETWEEN
                                            ? AND
                                            ?
                                            ORDER BY employees.[timeIDScanned] ASC
                                            ''', id_number, date_start, date_end)

        return self.cursor.fetchall()

    def get_lunches(self, date_start, date_end, dbtype):
        date_start = date_start + ' 00:00:00'
        date_end = date_end + ' 23:59:59'

        if dbtype == 'stud':
            self.cursor.execute('''SELECT students.[studentID], COUNT(*) AS "total_lunches"
                                    FROM [MiijinDB].MiijinProd.studentLunchRecords students
                                    WHERE students.timeIDScanned BETWEEN
                                    ? AND
                                    ?
                                    GROUP BY students.[studentID]
                                    ORDER BY students.[studentID] ASC''', date_start, date_end)
        else:
            self.cursor.execute('''SELECT employees.[employeeID], COUNT(*) AS "total_lunches" 
                                    FROM [MiijinDB].MiijinProd.employeeLunchRecords employees
                                    WHERE employees.timeIDScanned BETWEEN
                                    ? AND
                                    ?
                                    GROUP BY employees.[employeeID]
                                    ORDER BY employees.[employeeID] ASC''', date_start, date_end)

        return self.cursor.fetchall()

    def get_unique_users(self, date_start, date_end, dbtype):
        date_start = date_start + ' 00:00:00'
        date_end = date_end + ' 23:59:59'

        if dbtype == 'stud':
            self.cursor.execute('''SELECT COUNT(DISTINCT students.[studentID]) 
                                    FROM [MiijinDB].MiijinProd.studentLunchRecords students
                                    WHERE students.timeIDScanned BETWEEN
                                    ? AND
                                    ?''', date_start, date_end)
        else:
            self.cursor.execute('''SELECT COUNT(DISTINCT employees.[employeeID]) 
                                    FROM [MiijinDB].MiijinProd.employeeLunchRecords employees
                                    WHERE employees.timeIDScanned BETWEEN
                                    ? AND
                                    ?''', date_start, date_end)

        result = self.cursor.fetchall()
        row = result[0]
        user_count, = row

        return user_count

    def get_duplicate_users(self, date_start, date_end, dbtype):
        date_start = date_start + ' 00:00:00'
        date_end = date_end + ' 23:59:59'

        if dbtype == 'stud':
            self.cursor.execute('''SELECT COUNT(students.[studentID]) 
                                    FROM [MiijinDB].MiijinProd.studentLunchRecords students
                                    WHERE students.timeIDScanned BETWEEN
                                    ? AND
                                    ?''', date_start, date_end)
        else:
            self.cursor.execute('''SELECT COUNT(employees.[employeeID]) 
                                    FROM [MiijinDB].MiijinProd.employeeLunchRecords employees
                                    WHERE employees.timeIDScanned BETWEEN
                                    ? AND
                                    ?''', date_start, date_end)

        result = self.cursor.fetchall()
        row = result[0]
        duplicate_user_count, = row

        return duplicate_user_count

    def perform_insert(self, userid):
        if len(str(userid)) == 7:
            self.cursor.execute('''insert into MiijinDB.MiijinProd.studentLunchRecords(studentID, timeIDScanned)
                                    values (?, ?)''', int(userid), datetime.datetime.now())
        else:
            self.cursor.execute('''insert into MiijinDB.MiijinProd.employeeLunchRecords(employeeID, timeIDScanned)
                                                values (?, ?)''', int(userid), datetime.datetime.now())
        self.cursor.commit()
