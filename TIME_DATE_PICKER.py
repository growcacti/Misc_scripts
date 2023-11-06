import tkinter as tk
from tkinter import ttk
from datetime import datetime

class DateTimePicker(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Date and Time Picker")

        # Format current date and time
        self.now = datetime.now().strftime("%m %d %Y %H %M %S")
        month, day, year, hour, minute, second = self.now.split()

        # Date Picker
        self.date_frame = ttk.LabelFrame(self, text="Date")
        self.date_frame.grid(row=0, column=0, padx=10, pady=5, sticky='w')

        # Spinboxes for day, month, year
        self.day_var = tk.StringVar(value=day)
        self.day_spin = ttk.Spinbox(self.date_frame, from_=1, to=31, width=2, textvariable=self.day_var)
        self.day_spin.grid(row=0, column=1)  # Changed column to match order

        self.month_var = tk.StringVar(value=month)
        self.month_spin = ttk.Spinbox(self.date_frame, from_=1, to=12, width=2, textvariable=self.month_var)
        self.month_spin.grid(row=0, column=0)  # Changed column to match order

        self.year_var = tk.StringVar(value=year)
        self.year_spin = ttk.Spinbox(self.date_frame, from_=1900, to=2100, width=4, textvariable=self.year_var)
        self.year_spin.grid(row=0, column=2)

        # Time Picker
        self.time_frame = ttk.LabelFrame(self, text="Time")
        self.time_frame.grid(row=1, column=0, padx=10, pady=5, sticky='w')

        # Spinboxes for hour, minute, second
        self.hour_var = tk.StringVar(value=hour)
        self.hour_spin = ttk.Spinbox(self.time_frame, from_=0, to=23, width=2, textvariable=self.hour_var)
        self.hour_spin.grid(row=0, column=0)

        self.minute_var = tk.StringVar(value=minute)
        self.minute_spin = ttk.Spinbox(self.time_frame, from_=0, to=59, width=2, textvariable=self.minute_var)
        self.minute_spin.grid(row=0, column=1)

        self.second_var = tk.StringVar(value=second)
        self.second_spin = ttk.Spinbox(self.time_frame, from_=0, to=59, width=2, textvariable=self.second_var)
        self.second_spin.grid(row=0, column=2)


        self.btn_frame = ttk.Frame(self)
        self.btn_frame.grid(row=2, column=0, padx=10, pady=10, sticky='e')

        self.ok_btn = ttk.Button(self.btn_frame, text="OK", command=self.on_ok)
        self.ok_btn.grid(row=0, column=0, padx=5)
        
        self.cancel_btn = ttk.Button(self.btn_frame, text="Cancel", command=self.destroy)
        self.cancel_btn.grid(row=0, column=1)

    def on_ok(self):
        # Retrieve the values and destroy the window
        self.date = f"{self.month_var.get()}/{self.day_var.get()}/{self.year_var.get()}"
        self.time = f"{self.hour_var.get()}:{self.minute_var.get()}:{self.second_var.get()}"
        self.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Date and Time Picker Test")

    def show_picker():
        picker = DateTimePicker(root)
        root.wait_window(picker)
        try:
            print(f"Selected Date: {picker.date}")
            print(f"Selected Time: {picker.time}")
        except AttributeError:
            print("Selection cancelled")

    btn = ttk.Button(root, text="Pick Date and Time", command=show_picker)
    btn.pack(pady=20)

    root.mainloop()
