from src.Miijin.MiijinDatabase import miijin_mssql, mssql_config
import tkinter as tk


class MiijinLunchGUI:
    def __init__(self):
        # Initiate our TK Root Window and set a title
        self.root = tk.Tk()
        self.root.title("Miijin Lunch")

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

        self.user_id_tk = tk.StringVar()
        self.last_user_id_tk = tk.StringVar()

        self.userid_label = tk.Label(self.root, text='Student/Employee ID: ', font=('calibre', 16, 'bold'))
        self.userid_entry = tk.Entry(self.root, textvariable=self.user_id_tk, font=('calibre', 12, 'normal'))
        self.userid_entry.bind('<Return>', self.insert_data)

        self.last_userid_label = tk.Label(self.root, text='Last User ID Scanned: ', font=('calibre', 16, 'bold'))
        self.last_userid_entry = tk.Entry(self.root, textvariable=self.last_user_id_tk, font=('calibre', 12, 'normal'),
                                          state='disabled')

        # Create a quit button so that we can destroy our GUI
        self.quit_button = tk.Button(self.root, text='Quit', command=self.root.destroy)

        self.userid_label.grid(row=0, column=0)
        self.userid_entry.grid(row=0, column=1)
        self.last_userid_label.grid(row=1, column=0)
        self.last_userid_entry.grid(row=1, column=1)
        self.quit_button.grid(row=2, column=1)

        # Create the tkinter main loop, this is essential for the GUI to load
        self.userid_entry.focus_set()

        # Start our main loop to keep the GUI running
        self.root.mainloop()

    def insert_data(self, event=None):
        userid = str(self.user_id_tk.get())

        self.last_userid_entry.configure(state='normal')
        self.last_userid_entry.delete(0, 'end')
        self.last_userid_entry.insert(0, str(userid))
        self.last_userid_entry.configure(state='disabled')

        self.miijin_db.perform_insert(int(userid))

        self.user_id_tk.set("")


def main():
    MiijinLunchGUI()


main()
