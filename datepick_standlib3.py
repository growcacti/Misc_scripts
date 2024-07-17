import tkinter as tk
from tkinter import ttk
import calendar
from datetime import datetime

class DatePicker(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Date Picker")
        
        self.current_month = datetime.now().month
        self.current_year = datetime.now().year
        
        # Navigation frame
        nav_frame = tk.Frame(self,width=40,height=40)
        nav_frame.pack(pady=10)

        # Previous month button
        prev_month_btn = tk.Button(nav_frame, text="< Prev", command=self.prev_month)
        prev_month_btn.grid(row=0, column=0)

        # Month/Year label
        self.month_year_label = tk.Label(nav_frame, text="", font=("Helvetica", 16))
        self.month_year_label.grid(row=0, column=1)

        # Next month button
        next_month_btn = tk.Button(nav_frame, text="Next >", command=self.next_month)
        next_month_btn.grid(row=0, column=2)

        # Calendar frame
        self.calendar_frame = tk.Frame(self)
        self.calendar_frame.pack()

        # Display the current month calendar
        self.display_calendar(self.current_year, self.current_month)

    def prev_month(self):
        if self.current_month == 1:
            self.current_month = 12
            self.current_year -= 1
        else:
            self.current_month -= 1
        self.display_calendar(self.current_year, self.current_month)

    def next_month(self):
        if self.current_month == 12:
            self.current_month = 1
            self.current_year += 1
        else:
            self.current_month += 1
        self.display_calendar(self.current_year, self.current_month)

    def display_calendar(self, year, month):
        # Clear the current calendar frame
        for widget in self.calendar_frame.winfo_children():
            widget.destroy()

        # Update the month/year label
        self.month_year_label.config(text=f"{calendar.month_name[month]} {year}")

        # Create weekday labels
        weekdays = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
        for i, day in enumerate(weekdays):
            tk.Label(self.calendar_frame, text=day).grid(row=0, column=i)

        # Fill in the days of the month
        month_days = calendar.monthcalendar(year, month)
        
        for row_index, week in enumerate(month_days):
            for col_index, day in enumerate(week):
                if day == 0:
                    continue  # Skip empty days
                
                btn = tk.Button(self.calendar_frame, text=str(day),bd=7, bg="alice blue", width=5,
                                command=lambda d=day: print(f"Selected Date: {year}-{month:02d}-{d}"))
                btn.grid(row=row_index + 1, column=col_index)

if __name__ == "__main__":
    app = DatePicker()
    app.mainloop()
