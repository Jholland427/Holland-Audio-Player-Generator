import tkinter as tk
import re
import os
from tkinter import messagebox
from login_window import LoginWindow

class RegisterWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.title("Account Creation")
        self.geometry("800x200")
        self.iconphoto(False, tk.PhotoImage(file="audio.png"))
        self.create_widgets()
        self.center_window()
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

    def create_widgets(self):
        tk.Label(self, text="Create a username:").pack()
        self.username_entry = tk.Entry(self, justify='right')
        self.username_entry.pack()
        tk.Label(self, text="Create a password of at least nine (9) characters that contain at least one digit, one uppercase, and one lowercase letter. Then press <enter>").pack()
        self.password_entry = tk.Entry(self, show='*', justify='right')
        self.password_entry.pack()
        tk.Label(self, text="").pack()

        self.username_entry.bind('<Return>', self.create_account)
        self.password_entry.bind('<Return>', self.create_account)

    def create_account(self, event=None):
        username = self.username_entry.get()
        password = self.password_entry.get()
        if self.validate_password(password) and self.unique_username(username):
            with open("accounts.txt", "a") as file:
                file.write(f"{username},{password}\n")
            messagebox.showinfo("Registration Success", "Account created!")
            self.quit_program()
            LoginWindow(self.parent)
        else:
            messagebox.showerror("Registration Failed", "Invalid username or password")
            self.username_entry.delete(0, tk.END)
            self.password_entry.delete(0, tk.END)

    def validate_password(self, password):
        if len(password) >= 9 and re.search(r"\d", password) and re.search(r"[A-Z]", password) and re.search(r"[a-z]", password):
            return True
        return False

    def unique_username(self, username):
        if os.path.exists("accounts.txt"):
            with open("accounts.txt", "r") as file:
                for line in file:
                    stored_username, _ = line.strip().split(",")
                    if username == stored_username:
                        return False
        return True

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
