from . import miijin_mssql
from . import mssql_config
import tkinter
import tkinter.messagebox


class MiijinPyGUI:
    def __init__(self):
        self.driver = mssql_config.driver
        self.server = mssql_config.server
        self.database = mssql_config.database
        self.username = mssql_config.username
        self.password = mssql_config.password
        self.trusted = mssql_config.trust_server

        self.miijin_db = miijin_mssql.MiijinDatabase(self.driver, self.server, self.database,
                                                     self.username, self.password, self.trusted)

        # Make the main window
        self.main_window = tkinter.Tk()
        self.main_window.title("MiijinPy")

        # Create a frame for our label and entry widgets
        self.top_frame = tkinter.Frame(self.main_window)

        self.middle_frame = tkinter.Frame(self.main_window)
        # Create a frame for our button
        self.bottom_frame = tkinter.Frame(self.main_window)

        # Create a label widget and put it in the top frame
        self.userid_label = tkinter.Label(self.top_frame, text='Student/Employee ID: ')
        self.last_userid_label = tkinter.Label(self.middle_frame, text='Last User ID Scanned:')
        # Create an entry widget and put it in the top frame
        self.last_userid_entry = tkinter.Entry(self.middle_frame, state='disabled')

        self.userid_entry = tkinter.Entry(self.top_frame)
        self.userid_entry.bind('<Return>', self.insert_data)
        # Pack the top frame's widgets
        self.userid_label.pack(side='left')
        self.last_userid_label.pack(side='left')
        self.last_userid_entry.pack(side='left')

        self.userid_entry.pack(side='left')

        # Create a quit button so that we can destroy our GUI (put in the bottom frame)
        self.quit_button = tkinter.Button(self.bottom_frame, text='Quit', command=self.main_window.destroy)

        # Pack the bottom frame's widgets (the buttons)
        self.quit_button.pack(side='left')

        # Pack our frames
        self.top_frame.pack()
        self.middle_frame.pack()
        self.bottom_frame.pack()

        # Create the tkinter main loop, this is essential for the GUI to load
        self.userid_entry.focus_set()
        tkinter.mainloop()

    def insert_data(self, event=None):
        userid = self.userid_entry.get()

        self.last_userid_entry.configure(state='normal')
        self.last_userid_entry.delete(0, 'end')
        self.last_userid_entry.insert(0, str(userid))
        self.last_userid_entry.configure(state='disabled')

        self.miijin_db.perform_insert(int(userid))

        self.userid_entry.delete(0, 'end')
        self.userid_entry.insert(0, "")


def main():
    MiijinPyGUI()
