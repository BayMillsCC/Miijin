from MiijinPython.MiijinDatabase import miijin_mssql, mssql_config
import xlsxwriter
import time
import os


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

        for employee in employee_rows:
            employee_sum_cost = int(employee[1] * self.lunch_cost)
            temp_emp_list = [employee[0], employee[1], employee_sum_cost]
            self.output_employee_list.append(temp_emp_list)

        for student in student_rows:
            temp_stud_list = [student[0], student[1]]
            self.output_student_list.append(temp_stud_list)

    def generate_excel_file(self, filename):
        # Create a workbook and add a worksheet.
        current_date = time.strftime("%Y%m%d")
        user_download_folder = os.path.join(os.path.expanduser('~'), 'Downloads')
        excel_file_name = str(filename) + "-" + str(current_date) + '.xlsx'
        excel_path = os.path.join(user_download_folder, excel_file_name)

        workbook = xlsxwriter.Workbook(excel_path)
        employee_worksheet = workbook.add_worksheet("Employees")
        student_worksheet = workbook.add_worksheet("Students")
        currency_format = workbook.add_format({'bold': True, 'font_color': 'red', 'num_format': '$#,##0.00'})

        employee_worksheet.set_header('&L' + str(self.header_name) + " - Pay Period: "
                                      + str(self.period_number) + "&CPage &P of &N")

        employee_worksheet.set_footer('&CUpdated at &T')

        student_worksheet.set_header('&L' + str(self.header_name) + " - Pay Period: "
                                     + str(self.period_number) + "&CPage &P of &N")

        student_worksheet.set_footer('&CUpdated at &T')

        # Start from the first cell. Rows and columns are zero indexed.
        row = 0
        col = 0

        employee_worksheet.write(row, col, "Employee ID: ")
        employee_worksheet.write(row, col + 1, "Number of Lunches: ")
        employee_worksheet.write(row, col + 2, "Cost for Lunch: ")
        employee_worksheet.write(row + 1, col + 3, "Total Employee Lunches: ")
        employee_worksheet.write(row + 1, col + 4, self.employee_sum_lunches)
        employee_worksheet.write(row + 2, col + 3, "Total Unique Employees Served: ")
        employee_worksheet.write(row + 2, col + 4, self.total_employees_served)
        employee_worksheet.write(row + 3, col + 3, "Total Employee Cost: ")
        employee_worksheet.write(row + 3, col + 4, (self.employee_sum_lunches * self.lunch_cost), currency_format)
        row += 1

        # Iterate over the data and write it out row by row.
        for employee in self.output_employee_list:

            employee_worksheet.write(row, col, employee[0])
            employee_worksheet.write(row, col + 1, employee[1])
            employee_worksheet.write(row, col + 2, employee[2], currency_format)
            row += 1

        # Start from the first cell. Rows and columns are zero indexed.
        row = 0
        col = 0

        student_worksheet.write(row, col, "Student ID: ")
        student_worksheet.write(row, col + 1, "Number of Lunches: ")
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
