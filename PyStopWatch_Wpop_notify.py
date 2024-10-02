import tkinter as tk
from tkinter import messagebox
import time

class StopwatchApp:
    def __init__(self, master):
        self.master = master
        master.title("Stopwatch")

        self.timer_running = False
        self.start_time = None
        self.last_time = 0  # Initialize last_time with 0

        self.time_entry = tk.Entry(master, font=('Arial', 30))
        self.time_entry.grid(row=0, columnspan=3)

        self.duration_label = tk.Label(master, text="Duration (seconds):")
        self.duration_label.grid(row=1, column=0)

        self.duration_spinbox = tk.Spinbox(master, from_=1, to=3600, font=('Arial', 20))
        self.duration_spinbox.grid(row=1, column=1)

        self.popup_var = tk.IntVar()
        self.popup_checkbutton = tk.Checkbutton(master, text="Enable Pop-up", variable=self.popup_var)
        self.popup_checkbutton.grid(row=1, column=2)

        self.start_button = tk.Button(master, text='Start', command=self.start_timer)
        self.start_button.grid(row=2, column=0)

        self.stop_button = tk.Button(master, text='Stop', command=self.stop_timer)
        self.stop_button.grid(row=2, column=1)

        self.reset_button = tk.Button(master, text='Reset', command=self.reset_timer)
        self.reset_button.grid(row=2, column=2)

        self.continue_button = tk.Button(master, text='Continue', command=self.continue_timer)
        self.continue_button.grid(row=2, column=3)

        # Listbox to display stopped times
        self.stopped_times_listbox = tk.Listbox(master, width=20, height=10)
        self.stopped_times_listbox.grid(row=3, columnspan=3)

    def start_timer(self):
        if not self.timer_running:
            try:
                self.user_duration = int(self.duration_spinbox.get())
            except ValueError:
                self.user_duration = 0  # Default to 0 if no valid duration is entered

            self.start_time = time.time() - self.last_time
            self.update_timer()
            if self.popup_var.get() == 1:  # Check if the pop-up feature is enabled
                self.master.after(self.user_duration * 1000, self.show_popup)  # Schedule the pop-up message
            self.timer_running = True

    def stop_timer(self):
        if self.timer_running:
            elapsed_time = time.time() - self.start_time
            self.last_time = elapsed_time  # Save the elapsed time
            time_string = time.strftime('%H:%M:%S', time.gmtime(elapsed_time))
            self.stopped_times_listbox.insert(tk.END, time_string)
            self.timer_running = False

    def reset_timer(self):
        self.start_time = None
        self.timer_running = False
        self.last_time = 0  # Reset last_time to 0
        self.time_entry.delete(0, tk.END)
        self.stopped_times_listbox.delete(0, tk.END)

    def continue_timer(self):
        if not self.timer_running:
            self.start_time = time.time() - self.last_time
            self.update_timer()
            self.timer_running = True

    def update_timer(self):
        if self.timer_running:
            elapsed_time = time.time() - self.start_time
            minutes, seconds = divmod(int(elapsed_time), 60)
            hours, minutes = divmod(minutes, 60)
            milliseconds = int((elapsed_time - int(elapsed_time)) * 1000)
            time_string = f'{hours:02d}:{minutes:02d}:{seconds:02d}.{milliseconds:03d}'
            self.time_entry.delete(0, tk.END)
            self.time_entry.insert(0, time_string)
        self.master.after(10, self.update_timer)

    def show_popup(self):
        if self.timer_running and self.popup_var.get() == 1:
            result = messagebox.askyesno("Time's up!", "Do you want to repeat the timer?")
            if result:
                self.master.after(self.user_duration * 1000, self.show_popup)  # Schedule the next pop-up
            else:
                self.stop_timer()

def main():
    root = tk.Tk()
    app = StopwatchApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
