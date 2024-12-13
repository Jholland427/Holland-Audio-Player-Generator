import tkinter as tk
import os
from tkinter import messagebox
from main_gui import MainGUI

class LoginWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.title("Account Login")
        self.geometry("300x200")
        self.iconphoto(False, tk.PhotoImage(file="audio.png"))
        self.create_widgets()
        self.center_window()
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

    def create_widgets(self):
        frame = tk.Frame(self)
        frame.pack(pady=10)

        tk.Label(frame, text="Username:").grid(row=0, column=0, padx=5, pady=5, sticky='e')
        self.username_entry = tk.Entry(frame, justify='right')
        self.username_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(frame, text="Password:").grid(row=1, column=0, padx=5, pady=5, sticky='e')
        self.password_entry = tk.Entry(frame, show='*', justify='right')
        self.password_entry.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(frame, text="Enter a username and password and press <enter>").grid(row=2, columnspan=2, padx=5, pady=10)

        self.username_entry.bind('<Return>', self.verify_login)
        self.password_entry.bind('<Return>', self.verify_login)

    def verify_login(self, event=None):
        username = self.username_entry.get()
        password = self.password_entry.get()
        if self.validate_login(username, password):
            self.quit_program()
            self.parent.open_main_gui()
        else:
            messagebox.showerror("Login Failed", "Invalid username or password")
            self.username_entry.delete(0, tk.END)
            self.password_entry.delete(0, tk.END)

    def validate_login(self, username, password):
        if os.path.exists("accounts.txt"):
            with open("accounts.txt", "r") as file:
                for line in file:
                    stored_username, stored_password = line.strip().split(",")
                    if username == stored_username and password == stored_password:
                        return True
        return False

    def quit_program(self):
        self.destroy()

    def on_closing(self):
        self.destroy()
        self.parent.deiconify()

    def center_window(self):
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry('{}x{}+{}+{}'.format(width, height, x, y))
