import tkinter as tk
from tkinter import filedialog, messagebox
import winsound
import numpy as np
import wave
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class MainGUI(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.title("Audio Frequency Program")
        self.geometry("600x600")
        self.configure(bg="black")
        self.iconphoto(False, tk.PhotoImage(file="audio.png"))
        self.create_widgets()
        self.center_window()
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.wave_file = None
        self.frequency = None  

    def create_widgets(self):
        waveform_frame = tk.Frame(self, bg="black")
        waveform_frame.pack(fill="both", expand=True, padx=10, pady=10)
        self.image = tk.PhotoImage(file="th.png")
        tk.Label(waveform_frame, image=self.image, bg="black").place(relx=0.5, rely=0.5, anchor="center")
        tk.Label(self, text="Enter a Frequency or Select a .WAV", fg="white", bg="black", font=("Helvetica", 14)).pack(pady=10)
        btn_frame = tk.Frame(self, bg="black")
        btn_frame.pack(pady=10)
        tk.Button(btn_frame, text="Enter Frequency", height="2", width="15", fg="white", bg="black", command=self.enter_frequency).grid(row=0, column=0, padx=5, pady=5)
        tk.Button(btn_frame, text="Plot Frequency", height="2", width="15", fg="white", bg="black", command=self.plot_frequency).grid(row=1, column=0, padx=5, pady=5)
        tk.Button(btn_frame, text="Plot Audio File", height="2", width="15", fg="white", bg="black", command=self.plot_amplitude).grid(row=2, column=0, padx=5, pady=5)
        tk.Button(btn_frame, text="Select .WAV", height="2", width="15", fg="white", bg="black", command=self.select_wave_file).grid(row=0, column=1, padx=5, pady=5)
        tk.Button(btn_frame, text="Play Chosen .WAV", height="2", width="15", fg="white", bg="black", command=self.play_audio_tone).grid(row=1, column=1, padx=5, pady=5)
        tk.Button(btn_frame, text="Return Home", height="2", width="15", fg="white", bg="red", command=self.quit_program).grid(row=2, column=1, padx=5, pady=5)

    def enter_frequency(self):
        def play_frequency():
            try:
                frequency = int(entry.get())
                if 90 <= frequency <= 6000:
                    self.frequency = frequency  
                    winsound.Beep(frequency, 1000)
                    dialog.destroy()
                else:
                    messagebox.showerror("Invalid Frequency", "Please enter a frequency between 90 and 6,000 Hz.")
                    entry.delete(0, tk.END)
            except ValueError:
                messagebox.showerror("Invalid Input", "Please enter a valid integer.")
                entry.delete(0, tk.END)

        dialog = tk.Toplevel(self)
        dialog.title("Frequency")
        dialog.configure(bg="black")
        dialog.geometry(f"+{self.winfo_rootx() + self.winfo_width() // 2 - dialog.winfo_reqwidth() // 2}+{self.winfo_rooty() + self.winfo_height() // 2 - dialog.winfo_reqheight() // 2}")
        tk.Label(dialog, text="Enter a frequency in Hz between 90 and 6,000", fg="white", bg="black").pack(pady=10)
        entry = tk.Entry(dialog)
        entry.pack(pady=5)
        tk.Button(dialog, text="OK", command=play_frequency, fg="white", bg="black").pack(side="left", padx=10, pady=10)
        tk.Button(dialog, text="Cancel", command=dialog.destroy, fg="white", bg="black").pack(side="right", padx=10, pady=10)

    def select_wave_file(self):
        try:
            self.wave_file = filedialog.askopenfilename(filetypes=[("Wave files", "*.wav")])
            if self.wave_file:
                messagebox.showinfo("File Selected", f"Selected file: {self.wave_file}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to select file: {e}")

    def play_audio_tone(self):
        if not self.wave_file:
            messagebox.showwarning("No File", "No wave file selected. Please select a wave file first.")
            return
        try:
            winsound.PlaySound(self.wave_file, winsound.SND_FILENAME)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to play audio: {e}")

    def plot_amplitude(self):
        if not self.wave_file:
            messagebox.showwarning("No File", "No wave file selected. Please select a wave file first.")
            return
        try:
            with wave.open(self.wave_file, 'r') as wav_file:
                n_frames = wav_file.getnframes()
                frame_rate = wav_file.getframerate()
                duration = n_frames / float(frame_rate)
                signal_wave = wav_file.readframes(n_frames)
                signal_array = np.frombuffer(signal_wave, dtype=np.int16)
                times = np.linspace(0, duration, num=n_frames)

                zoom_duration = 0.01  
                zoom_samples = int(frame_rate * zoom_duration)
                zoom_times = times[:zoom_samples]
                zoom_signal_array = signal_array[:zoom_samples]

                fig, ax = plt.subplots()
                ax.plot(zoom_times, zoom_signal_array)
                ax.set_xlabel('Time (s)')
                ax.set_ylabel('Amplitude')
                ax.set_title(f'{self.wave_file}')

                self.show_plot(fig)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to plot amplitude: {e}")

    def plot_frequency(self):
        if self.frequency is None:
            messagebox.showwarning("No Frequency", "No frequency entered. Please enter a frequency first.")
            return
        try:
            duration = 1.0  
            sample_rate = 44100  
            t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
            signal = 0.5 * np.sin(2 * np.pi * self.frequency * t)

            zoom_duration = 0.01  
            zoom_samples = int(sample_rate * zoom_duration)
            zoom_t = t[:zoom_samples]
            zoom_signal = signal[:zoom_samples]

            fig, ax = plt.subplots()
            ax.plot(zoom_t, zoom_signal)
            ax.set_xlabel('Time (s)')
            ax.set_ylabel('Amplitude')
            ax.set_title(f'{self.frequency} Hz')

            self.show_plot(fig)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to plot frequency: {e}")

    def show_plot(self, fig):
        plot_window = tk.Toplevel(self)
        plot_window.title("Frequency/Amplitude Display")
        plot_window.geometry("800x600")
        self.center_window(plot_window)

        canvas = FigureCanvasTkAgg(fig, master=plot_window)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def quit_program(self):
        self.destroy()
        self.parent.deiconify()

    def on_closing(self):
        self.quit_program()

    def center_window(self, window=None):
        if window is None:
            window = self
        window.update_idletasks()
        width = window.winfo_width()
        height = window.winfo_height()
        x = (window.winfo_screenwidth() // 2) - (width // 2)
        y = (window.winfo_screenheight() // 2) - (height // 2)
        window.geometry('{}x{}+{}+{}'.format(width, height, x, y))

if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()
    app = MainGUI(root)
    root.mainloop()
