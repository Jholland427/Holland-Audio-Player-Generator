import tkinter as tk
import sys
from login_window import LoginWindow
from register_window import RegisterWindow
from main_gui import MainGUI
import numpy as np
import matplotlib.pyplot as plt

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Holland Audio Player & Generator")
        self.geometry("500x250")
        self.center_window()

        self.iconphoto(False, tk.PhotoImage(file="audio.png"))
        self.create_widgets()

    def create_widgets(self):
        self.sunburst_frame = tk.Frame(self)
        self.sunburst_frame.pack()

        self.typewriter_label = tk.Label(self.sunburst_frame, text="", font=("Helvetica", 17))
        self.typewriter_label.pack(pady=10)

        self.typewriter_text = "Welcome to Holland Audio Player & Generator"
        self.typewriter_index = 0

        self.typewriter_effect()

        btn_frame = tk.Frame(self)
        btn_frame.pack(pady=5)

        login_column = tk.Frame(btn_frame)
        login_column.pack(side=tk.LEFT, padx=5)
        create_account_column = tk.Frame(btn_frame)
        create_account_column.pack(side=tk.LEFT, padx=5)
        exit_column = tk.Frame(btn_frame)
        exit_column.pack(side=tk.LEFT, padx=5)

        tk.Label(login_column, text="(*^.^*)", font=("Helvetica", 16)).pack()
        tk.Label(create_account_column, text="||", font=("Helvetica", 16)).pack()
        tk.Label(exit_column, text="X", font=("Helvetica", 16)).pack()

        tk.Button(login_column, text="Login", height="2", width="20", bg="lightgreen", command=self.login).pack()
        tk.Button(create_account_column, text="Create Account", height="2", width="20", bg="lightblue", command=self.register).pack()
        tk.Button(exit_column, text="Exit Program", height="2", width="20", bg="lightcoral", command=self.quit_program).pack()

    def typewriter_effect(self):
        if self.typewriter_index < len(self.typewriter_text):
            current_text = self.typewriter_label.cget("text")
            next_character = self.typewriter_text[self.typewriter_index]
            self.typewriter_label.config(text=current_text + next_character)
            self.typewriter_index += 1
            self.after(70, self.typewriter_effect)
        else:
            self.create_sunburst_effect() 

    def create_sunburst_effect(self):
        colors = ["#90EE90", "#ADD8E6", "#FF6347"] 
        for offset, color in zip(range(0, 3), colors):
            tk.Label(self.sunburst_frame, text="Welcome to Holland Audio Player & Generator", font=("Helvetica", 17), fg=color).pack(padx=offset, pady=offset)

    def center_window(self):
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry('{}x{}+{}+{}'.format(width, height, x, y))

    def login(self):
        self.withdraw()
        login_window = LoginWindow(self)
        login_window.center_window()

    def register(self):
        self.withdraw()
        register_window = RegisterWindow(self)
        register_window.center_window()

    def open_main_gui(self):
        main_gui = MainGUI(self)
        main_gui.center_window()

    def quit_program(self):
        self.destroy()
        sys.exit()

if __name__ == "__main__":
    app = App()
    app.mainloop()
