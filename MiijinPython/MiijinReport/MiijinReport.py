from MiijinPython.MiijinDatabase import miijin_mssql, mssql_config

# Goals
# Generate two separate files, 1 for employees one for students
# Prompt the user to generate the data for the files based on a start date and end date
# Prompt user to enter header name and accounting period
# Count number of meals served and group it by the respective ID (per-student/per-employee)
# Order/Sort by ID Number
# Include a total/sum count for number of meals
# Add a footer for page number?

# For employees only:
# Show total $ amount in the grouping for how much the payroll deduct should be
# I will try to bold the numbers
# Run a sum total and also display a # of employees served * 5 for a comparison


class MiijinReportGUI:
    def __init__(self):
        self.date_start = input("Please enter start date in YYYY-MM-DD format: ")
        self.date_end = input("Please enter end date in YYYY-MM-DD format: ")
        self.header_name = input("Please enter a name for the header: ")
        self.period_number = input("Please enter a number for the pay period: ")

        self.driver = mssql_config.driver
        self.server = mssql_config.server
        self.database = mssql_config.database
        self.username = mssql_config.username
        self.password = mssql_config.password
        self.trusted = mssql_config.trust_server

        self.miijin_db = miijin_mssql.MiijinDatabase(self.driver, self.server, self.database,
                                                     self.username, self.password, self.trusted)

    def get_lunch_counts(self):
        employee_rows = self.miijin_db.get_lunches(self.date_start, self.date_end, 'emp')

        for employee in employee_rows:
            print(employee)


def main():
    report = MiijinReportGUI()
    report.get_lunch_counts()


main()
