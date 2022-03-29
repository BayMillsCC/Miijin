from MiijinPython.MiijinDatabase import miijin_mssql, mssql_config
import xlsxwriter
import time
import os

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

        self.lunch_cost = 5
        self.employee_sum_lunches = 0
        self.student_sum_lunches = 0
        self.total_employees_served = ''
        self.total_students_served = ''
        self.output_employee_list = []
        self.output_student_list = []

    def get_lunch_counts(self):
        employee_rows = self.miijin_db.get_lunches(self.date_start, self.date_end, 'emp')
        student_rows = self.miijin_db.get_lunches(self.date_start, self.date_end, 'stud')
        self.total_employees_served = self.miijin_db.get_unique_users(self.date_start, self.date_end, 'emp')
        self.total_students_served = self.miijin_db.get_unique_users(self.date_start, self.date_end, 'stud')
        self.employee_sum_lunches = self.miijin_db.get_duplicate_users(self.date_start, self.date_end, 'emp')
        self.student_sum_lunches = self.miijin_db.get_duplicate_users(self.date_start, self.date_end, 'stud')

        # print("ID - Lunches - Cost")
        for employee in employee_rows:
            employee_sum_cost = int(employee[1] * self.lunch_cost)
            temp_emp_list = [employee[0], employee[1], employee_sum_cost]
            self.output_employee_list.append(temp_emp_list)
            # print(str(employee[0]) + " - " + str(employee[1]) + " - $" + str(employee_sum_cost))

        for student in student_rows:
            temp_stud_list = [student[0], student[1]]
            self.output_student_list.append(temp_stud_list)
            # print(str(student[0]) + " - " + str(student[1]) + " - $0")

        # print(self.output_employee_list)
        # print(self.output_student_list)
        # print("Total Employee Lunches: " + str(self.employee_sum_lunches))
        # print("Total Student Lunches: " + str(self.student_sum_lunches))
        # print("Total Combined Lunches: " + str(self.employee_sum_lunches + self.student_sum_lunches))
        # print("Total Unique Employees Served: " + str(self.total_employees_served))
        # print("Total Unique Students Served: " + str(self.total_students_served))
        # print("Total Employee Cost: $" + str(self.employee_sum_lunches * self.lunch_cost))

    def generate_excel_file(self, filename):
        # Create a workbook and add a worksheet.
        current_date = time.strftime("%Y%m%d")
        user_download_folder = os.path.join(os.path.expanduser('~'), 'Downloads')
        excel_file_name = str(filename) + "-" + str(current_date) + '.xlsx'
        excel_path = os.path.join(user_download_folder, excel_file_name)

        workbook = xlsxwriter.Workbook(excel_path)
        employee_worksheet = workbook.add_worksheet("Employees")
        student_worksheet = workbook.add_worksheet("Students")

        # Start from the first cell. Rows and columns are zero indexed.
        row = 0
        col = 0

        employee_worksheet.write(row, col, "Employee ID: ")
        employee_worksheet.write(row, col + 1, "Number of Lunches: ")
        employee_worksheet.write(row, col + 2, "Cost for Lunch: ")
        employee_worksheet.write(row, col + 3, "Header: " + str(self.header_name))
        employee_worksheet.write(row, col + 4, "Pay Period: " + str(self.period_number))
        employee_worksheet.write(row + 1, col + 3, "Total Employee Lunches: ")
        employee_worksheet.write(row + 1, col + 4, self.employee_sum_lunches)
        employee_worksheet.write(row + 2, col + 3, "Total Unique Employees Served: ")
        employee_worksheet.write(row + 2, col + 4, self.total_employees_served)
        employee_worksheet.write(row + 3, col + 3, "Total Employee Cost: $ ")
        employee_worksheet.write(row + 3, col + 4, (self.employee_sum_lunches * self.lunch_cost))
        row += 1
        # Iterate over the data and write it out row by row.
        for employee in self.output_employee_list:

            employee_worksheet.write(row, col, employee[0])
            employee_worksheet.write(row, col + 1, employee[1])
            employee_worksheet.write(row, col + 2, employee[2])
            row += 1

        # Start from the first cell. Rows and columns are zero indexed.
        row = 0
        col = 0

        student_worksheet.write(row, col, "Student ID: ")
        student_worksheet.write(row, col + 1, "Number of Lunches: ")
        student_worksheet.write(row, col + 3, "Header: " + str(self.header_name))
        student_worksheet.write(row, col + 4, "Pay Period: " + str(self.period_number))
        student_worksheet.write(row + 1, col + 3, "Total Student Lunches: ")
        student_worksheet.write(row + 1, col + 4, self.student_sum_lunches)
        student_worksheet.write(row + 2, col + 3, "Total Unique Students Served: ")
        student_worksheet.write(row + 2, col + 4, self.total_students_served)
        row += 1
        # Iterate over the data and write it out row by row.
        for student in self.output_student_list:
            student_worksheet.write(row, col, student[0])
            student_worksheet.write(row, col + 1, student[1])
            row += 1

        workbook.close()


def main():
    report = MiijinReportGUI()
    report.get_lunch_counts()
    report.generate_excel_file("lunches")


main()
