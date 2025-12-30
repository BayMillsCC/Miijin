import psycopg

class MiijinDatabase:
    def __init__(self, host, database, username, password, port=5432, sslmode="require"):
        self.host = host
        self.database = database
        self.username = username
        self.password = password
        self.port = port
        self.sslmode = sslmode

        self.conn = psycopg.connect(
            host=self.host,
            dbname=self.database,
            user=self.username,
            password=self.password,
            port=self.port,
            sslmode=self.sslmode,
        )
        self.cursor = self.conn.cursor()

    def close(self):
        try:
            self.cursor.close()
        finally:
            self.conn.close()

    def get_daily_lunches(self, start_date, end_date, dbtype):
        date_start = start_date + " 00:00:00"
        date_end = end_date + " 23:59:59"

        if dbtype == "stud":
            self.cursor.execute(
                """
                SELECT students.studentid, students.timeidscanned AS total_lunches
                FROM miijinprod.studentlunchrecords AS students
                WHERE students.timeidscanned BETWEEN %s AND %s
                ORDER BY students.timeidscanned ASC
                """,
                (date_start, date_end),
            )
        else:
            self.cursor.execute(
                """
                SELECT employees.employeeid, employees.timeidscanned AS total_lunches
                FROM miijinprod.employeelunchrecords AS employees
                WHERE employees.timeidscanned BETWEEN %s AND %s
                ORDER BY employees.timeidscanned ASC
                """,
                (date_start, date_end),
            )

        return self.cursor.fetchall()

    def get_individual_lunches(self, id_number, start_date, end_date, dbtype):
        date_start = start_date + " 00:00:00"
        date_end = end_date + " 23:59:59"

        if dbtype == "stud":
            self.cursor.execute(
                """
                SELECT students.studentid, students.timeidscanned AS total_lunches
                FROM miijinprod.studentlunchrecords AS students
                WHERE students.studentid = %s
                  AND students.timeidscanned BETWEEN %s AND %s
                ORDER BY students.timeidscanned ASC
                """,
                (id_number, date_start, date_end),
            )
        else:
            self.cursor.execute(
                """
                SELECT employees.employeeid, employees.timeidscanned AS total_lunches
                FROM miijinprod.employeelunchrecords AS employees
                WHERE employees.employeeid = %s
                  AND employees.timeidscanned BETWEEN %s AND %s
                ORDER BY employees.timeidscanned ASC
                """,
                (id_number, date_start, date_end),
            )

        return self.cursor.fetchall()

    def get_lunches(self, date_start, date_end, dbtype):
        date_start = date_start + " 00:00:00"
        date_end = date_end + " 23:59:59"

        if dbtype == "stud":
            self.cursor.execute(
                """
                SELECT students.studentid, COUNT(*) AS total_lunches
                FROM miijinprod.studentlunchrecords AS students
                WHERE students.timeidscanned BETWEEN %s AND %s
                GROUP BY students.studentid
                ORDER BY students.studentid ASC
                """,
                (date_start, date_end),
            )
        else:
            self.cursor.execute(
                """
                SELECT employees.employeeid, COUNT(*) AS total_lunches
                FROM miijinprod.employeelunchrecords AS employees
                WHERE employees.timeidscanned BETWEEN %s AND %s
                GROUP BY employees.employeeid
                ORDER BY employees.employeeid ASC
                """,
                (date_start, date_end),
            )

        return self.cursor.fetchall()

    def get_unique_users(self, date_start, date_end, dbtype):
        date_start = date_start + " 00:00:00"
        date_end = date_end + " 23:59:59"

        if dbtype == "stud":
            self.cursor.execute(
                """
                SELECT COUNT(DISTINCT students.studentid)
                FROM miijinprod.studentlunchrecords AS students
                WHERE students.timeidscanned BETWEEN %s AND %s
                """,
                (date_start, date_end),
            )
        else:
            self.cursor.execute(
                """
                SELECT COUNT(DISTINCT employees.employeeid)
                FROM miijinprod.employeelunchrecords AS employees
                WHERE employees.timeidscanned BETWEEN %s AND %s
                """,
                (date_start, date_end),
            )

        (user_count,) = self.cursor.fetchone()
        return user_count

    def get_duplicate_users(self, date_start, date_end, dbtype):
        date_start = date_start + " 00:00:00"
        date_end = date_end + " 23:59:59"

        if dbtype == "stud":
            self.cursor.execute(
                """
                SELECT COUNT(students.studentid)
                FROM miijinprod.studentlunchrecords AS students
                WHERE students.timeidscanned BETWEEN %s AND %s
                """,
                (date_start, date_end),
            )
        else:
            self.cursor.execute(
                """
                SELECT COUNT(employees.employeeid)
                FROM miijinprod.employeelunchrecords AS employees
                WHERE employees.timeidscanned BETWEEN %s AND %s
                """,
                (date_start, date_end),
            )

        (duplicate_user_count,) = self.cursor.fetchone()
        return duplicate_user_count

    def perform_insert(self, userid):
        # Since you set DEFAULT CURRENT_TIMESTAMP on timeidscanned,
        # you can omit the timestamp entirely.
        if len(str(userid)) == 7:
            self.cursor.execute(
                """
                INSERT INTO miijinprod.studentlunchrecords (studentid)
                VALUES (%s)
                """,
                (int(userid),),
            )
        else:
            self.cursor.execute(
                """
                INSERT INTO miijinprod.employeelunchrecords (employeeid)
                VALUES (%s)
                """,
                (int(userid),),
            )

        self.conn.commit()
