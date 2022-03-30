from MiijinPython.MiijinDatabase import miijin_mssql, mssql_config
import tkinter as tk
from tkcalendar import DateEntry
import xlsxwriter
import time
import os


class MiijinReportGUI:
    def __init__(self):
        # Initiate our TK Root Window and set a title
        self.root = tk.Tk()
        self.root.title("MiijinReport")

        # Initiate internal variables
        self.date_start = ''
        self.date_end = ''
        self.header_name = ''
        self.period_number = ''
        self.export_file_name = ''
        self.lunch_cost = 5  # Lunches currently cost $5 for employees
        self.employee_sum_lunches = 0
        self.student_sum_lunches = 0
        self.total_employees_served = ''
        self.total_students_served = ''
        self.output_employee_list = []  # Used by xlsxwriter
        self.output_student_list = []  # Used by xlsxwriter

        # Our database configuration being puled from mssql_config
        self.driver = mssql_config.driver
        self.server = mssql_config.server
        self.database = mssql_config.database
        self.username = mssql_config.username
        self.password = mssql_config.password
        self.trusted = mssql_config.trust_server

        # Initiate the connection to our database
        self.miijin_db = miijin_mssql.MiijinDatabase(self.driver, self.server, self.database,
                                                     self.username, self.password, self.trusted)

        # Specific variables and elements used by the GUI side of the program
        self.header_name_tk = tk.StringVar()
        self.period_number_tk = tk.StringVar()
        self.export_file_name_tk = tk.StringVar()
        self.output_message_tk = tk.StringVar()

        self.start_date_label = tk.Label(self.root, text='Start Date (YYYY-MM-DD):', font=('calibre', 16, 'bold'))
        self.start_date_entry = DateEntry(self.root, selectmode='day', textvariable=self.start_date_label,
                                          background="magenta3", foreground="white", date_pattern='y/m/d')

        self.end_date_label = tk.Label(self.root, text='End Date (YYYY-MM-DD): ', font=('calibre', 16, 'bold'))
        self.end_date_entry = DateEntry(self.root, selectmode='day', textvariable=self.end_date_label,
                                        background="magenta3", foreground="white", date_pattern='y/m/d')

        self.header_label = tk.Label(self.root, text='Header: ', font=('calibre', 16, 'bold'))
        self.header_entry = tk.Entry(self.root, textvariable=self.header_name_tk, font=('calibre', 12, 'normal'))

        self.pay_period_label = tk.Label(self.root, text='Pay Period: ', font=('calibre', 16, 'bold'))
        self.pay_period_entry = tk.Entry(self.root, textvariable=self.period_number_tk, font=('calibre', 12, 'normal'))

        self.export_file_name_label = tk.Label(self.root, text='Export File Name: ', font=('calibre', 16, 'bold'))
        self.export_file_name_entry = tk.Entry(self.root, textvariable=self.export_file_name_tk,
                                               font=('calibre', 12, 'normal'))

        self.output_message_label = tk.Label(self.root, text='Output Message: ', font=('calibre', 16, 'bold'))
        self.output_message_value = tk.Label(self.root, textvariable=self.output_message_tk,
                                             font=('calibre', 12, 'normal'))

        self.generate_file_button = tk.Button(self.root, text='Generate File', command=self.generate_excel_file_button)
        self.quit_button = tk.Button(self.root, text='Quit', command=self.root.destroy)

        # Place our various GUI elements in a grid configuration
        self.start_date_label.grid(row=0, column=0)
        self.start_date_entry.grid(row=0, column=1)
        self.end_date_label.grid(row=1, column=0)
        self.end_date_entry.grid(row=1, column=1)
        self.header_label.grid(row=2, column=0)
        self.header_entry.grid(row=2, column=1)
        self.pay_period_label.grid(row=3, column=0)
        self.pay_period_entry.grid(row=3, column=1)
        self.export_file_name_label.grid(row=4, column=0)
        self.export_file_name_entry.grid(row=4, column=1)
        self.output_message_label.grid(row=5, column=0)
        self.output_message_value.grid(row=5, column=1)
        self.generate_file_button.grid(row=6, column=0)
        self.quit_button.grid(row=6, column=1)

        # Start our main loop to keep the GUI running
        self.root.mainloop()

    def generate_excel_file_button(self):
        # This function sets variables and calls the functions necessary to populate other data
        self.output_message_tk.set("")
        self.date_start = str(self.start_date_entry.get_date())
        self.date_end = str(self.end_date_entry.get_date())
        self.header_name = str(self.header_name_tk.get())
        self.period_number = str(self.period_number_tk.get())
        self.export_file_name = str(self.export_file_name_tk.get())
        self.header_name_tk.set("")
        self.period_number_tk.set("")
        self.export_file_name_tk.set("")

        # Call our lunch counts function and our Excel generator function
        self.get_lunch_counts()
        result = self.generate_excel_file(self.export_file_name)

        # Report back any output messages
        self.output_message_tk.set(result)

    def get_lunch_counts(self):
        # This function is responsible for actually pulling data from the database for employees and students
        # The two functions below pull data for students and employees separately
        employee_rows = self.miijin_db.get_lunches(self.date_start, self.date_end, 'emp')
        student_rows = self.miijin_db.get_lunches(self.date_start, self.date_end, 'stud')

        # Now we want to grab some specific numbers which were just more convenient to grab with SQL
        self.total_employees_served = self.miijin_db.get_unique_users(self.date_start, self.date_end, 'emp')
        self.total_students_served = self.miijin_db.get_unique_users(self.date_start, self.date_end, 'stud')
        self.employee_sum_lunches = self.miijin_db.get_duplicate_users(self.date_start, self.date_end, 'emp')
        self.student_sum_lunches = self.miijin_db.get_duplicate_users(self.date_start, self.date_end, 'stud')

        # We will iterate through each employee and calculate their lunch cost and generate the Excel list
        for employee in employee_rows:
            employee_sum_cost = int(employee[1] * self.lunch_cost)
            temp_emp_list = [employee[0], employee[1], employee_sum_cost]
            self.output_employee_list.append(temp_emp_list)

        # We will iterate through each student and generate the Excel list
        for student in student_rows:
            temp_stud_list = [student[0], student[1]]
            self.output_student_list.append(temp_stud_list)

    def generate_excel_file(self, filename):
        # This function is what actually generates our Excel file and sets formatting options
        # We also append the current date to the end of the file to keep it easier to differentiate
        current_date = time.strftime("%Y%m%d")

        # No, you don't get a choice, it will go to your Downloads folder because that's where downloads go
        user_download_folder = os.path.join(os.path.expanduser('~'), 'Downloads')
        excel_file_name = str(filename) + "-" + str(current_date) + '.xlsx'
        excel_path = os.path.join(user_download_folder, excel_file_name)

        # This will actually create the workbook and set up two separate worksheets to separate our data
        workbook = xlsxwriter.Workbook(excel_path)
        employee_worksheet = workbook.add_worksheet("Employees")
        student_worksheet = workbook.add_worksheet("Students")

        # Set the currency format for some of our cells to make it appear easier on the eyes
        currency_format = workbook.add_format({'bold': True, 'font_color': 'red', 'num_format': '$#,##0.00'})

        # Set our header information
        employee_worksheet.set_header('&L' + str(self.header_name) + " - Pay Period: "
                                      + str(self.period_number) + "&CPage &P of &N")

        # Set our footer information
        employee_worksheet.set_footer('&CUpdated at &T')

        # Now we will start outputting data to our file starting with Employees
        # Rows and columns are 0-indexed meaning the first top left cell is 0,0 according to this module
        row = 0
        col = 0

        # Output top row (header) information and some basic calculations
        employee_worksheet.write(row, col, "Employee ID: ")
        employee_worksheet.write(row, col + 1, "Number of Lunches: ")
        employee_worksheet.write(row, col + 2, "Cost for Lunch: ")
        employee_worksheet.write(row + 1, col + 3, "Total Employee Lunches: ")
        employee_worksheet.write(row + 1, col + 4, self.employee_sum_lunches)
        employee_worksheet.write(row + 2, col + 3, "Total Unique Employees Served: ")
        employee_worksheet.write(row + 2, col + 4, self.total_employees_served)
        employee_worksheet.write(row + 3, col + 3, "Total Employee Cost: ")
        employee_worksheet.write(row + 3, col + 4, (self.employee_sum_lunches * self.lunch_cost), currency_format)

        # Increment our row so that we don't accidentally overwrite data in the loop below
        row += 1

        # Iterate over the data we generated in our get_lunch_counts function and write it out row by row.
        for employee in self.output_employee_list:
            employee_worksheet.write(row, col, employee[0])
            employee_worksheet.write(row, col + 1, employee[1])
            employee_worksheet.write(row, col + 2, employee[2], currency_format)
            row += 1

        # Now we will repeat the exact same steps above but for students
        # I could have written this as a function, but we do generate separate data between employees and students
        row = 0
        col = 0

        # Output top row (header) information and some basic calculations
        student_worksheet.write(row, col, "Student ID: ")
        student_worksheet.write(row, col + 1, "Number of Lunches: ")
        student_worksheet.write(row + 1, col + 3, "Total Student Lunches: ")
        student_worksheet.write(row + 1, col + 4, self.student_sum_lunches)
        student_worksheet.write(row + 2, col + 3, "Total Unique Students Served: ")
        student_worksheet.write(row + 2, col + 4, self.total_students_served)

        # Increment our row so that we don't accidentally overwrite data in the loop below
        row += 1

        # Iterate over the data we generated in our get_lunch_counts function and write it out row by row.
        for student in self.output_student_list:
            student_worksheet.write(row, col, student[0])
            student_worksheet.write(row, col + 1, student[1])
            row += 1

        # We're done writing data, close the workbook
        workbook.close()

        # I haven't added proper error checking, but ideally the below message is what is returned to the user's GUI
        output_message = "File generated successfully"
        return output_message


def main():
    # Call our class and initialize
    MiijinReportGUI()


# Invoke our Main function
main()
