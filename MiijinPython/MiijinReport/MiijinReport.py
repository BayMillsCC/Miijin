from MiijinPython.MiijinDatabase import miijin_mssql, mssql_config
import xlsxwriter

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
        student_rows = self.miijin_db.get_lunches(self.date_start, self.date_end, 'stud')

        employee_sum_lunches = 0
        student_sum_lunches = 0
        total_employees_served = 0
        lunch_cost = 5  # Currently, we pay $5 for lunch

        print("ID - Lunches - Cost")
        for employee in employee_rows:
            employee_sum_lunches += int(employee[1])
            total_employees_served += 1
            # TODO: Re-write this into a separate function to return duplicate count
            # TODO: Write a separate function to return non-duplicate employee count for period

            employee_sum_cost = int(employee[1] * lunch_cost)
            print(str(employee[0]) + " - " + str(employee[1]) + " - $" + str(employee_sum_cost))

        for student in student_rows:
            student_sum_lunches += int(student[1])
            print(str(student[0]) + " - " + str(student[1]) + " - $0")

        print("Total Employee Lunches: " + str(employee_sum_lunches))
        print("Total Student Lunches: " + str(student_sum_lunches))
        print("Total Combined Lunches: " + str(employee_sum_lunches + student_sum_lunches))
        print("Total Employee Cost: $" + str(employee_sum_lunches * lunch_cost))

    def generate_excel_file(self, output_list, filename):
        # TODO: Implement this function
        # Create a workbook and add a worksheet.
        workbook = xlsxwriter.Workbook(str(filename) + '.xlsx')
        worksheet = workbook.add_worksheet()

        # Some data we want to write to the worksheet.
        expenses = (
            ['Rent', 1000],
            ['Gas', 100],
            ['Food', 300],
            ['Gym', 50],
        )

        # Start from the first cell. Rows and columns are zero indexed.
        row = 0
        col = 0

        # Iterate over the data and write it out row by row.
        for item, cost in expenses:
            worksheet.write(row, col, item)
            worksheet.write(row, col + 1, cost)
            row += 1

        # Write a total using a formula.
        worksheet.write(row, 0, 'Total')
        worksheet.write(row, 1, '=SUM(B1:B4)')

        workbook.close()


def main():
    report = MiijinReportGUI()
    report.get_lunch_counts()


main()
