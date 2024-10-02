import tkinter as tk
from tkinter import ttk, filedialog, messagebox, Spinbox, Scrollbar, INSERT, END, font, Toplevel
import os
import calendar
from datetime import datetime
from time import time, strftime, localtime

class Calendar_Widget:
    def __init__(self, parent):
        self.parent = parent
        self.efrm = tk.Frame(self.parent)
        self.efrm.grid(row=1, column=1)
        self.now = datetime.now().strftime("%m %d %Y %H %M %S")
        month, day, year, hour, minute, second = self.now.split()

        self.current_month = datetime.now().month
        self.current_year = datetime.now().year
        self.current_time = strftime('%H:%M:%S', localtime())
        self.epoch_time = int(time())
        nav_frame = tk.Frame(self.parent, width=75, height=70)
        nav_frame.grid(row=1, column=0,columnspan=3, pady=10)
        self.day_buttons = []

        prev_month_btn = tk.Button(nav_frame, text="< Prev", bd=4, command=self.prev_month)
        prev_month_btn.grid(row=0, column=0)

        self.month_year_label = tk.Label(nav_frame, text="", font=("Helvetica", 10))
        self.month_year_label.grid(row=0, column=1,columnspan=2)

        next_month_btn = tk.Button(nav_frame, text="Next >", bd=4, command=self.next_month)
        next_month_btn.grid(row=0, column=4)

        self.efrm = tk.Frame(self.parent)
        self.calendar_frame = tk.Frame(self.parent)
        self.calendar_frame.grid(row=2, column=0, rowspan=2, columnspan=2)

        # Label to display the selected date
        self.selected_date_label = tk.Label(self.parent, text="", font=("Helvetica", 10))
        self.selected_date_label.grid(row=4, column=0, columnspan=3, pady=10)

        self.display_calendar(self.current_year, self.current_month)

    def prev_month(self):
        if self.current_month == 1:
            self.current_month = 12
            self.current_year -= 1
        else:
            self.current_month -= 1
        self.display_prev(self.current_year, self.current_month)

    def next_month(self):
        if self.current_month == 12:
            self.current_month = 1
            self.current_year += 1
        else:
            self.current_month += 1
        self.display_next(self.current_year, self.current_month)

    def display_calendar(self, year, month):
        self.month_year_label.config(text=f"{calendar.month_name[month]} {year}")
        weekdays = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
        for i, day in enumerate(weekdays):
            tk.Label(self.calendar_frame, text=day).grid(row=0, column=i)

        month_days = calendar.monthcalendar(year, month)
        self.day_buttons.clear()
        for row_index, week in enumerate(month_days):
            for col_index, day in enumerate(week):
                if day == 0:
                    lbl = tk.Label(self.calendar_frame, text="")
                    lbl.grid(row=row_index + 1, column=col_index)
                    continue
                btn = tk.Button(self.calendar_frame, text=str(day), bd=8, width=3, height=1, bg="alice blue", font=("Helvetica", 9),
                                command=lambda m=month, d=day, y=year: self.update(m, d, y))
                btn.grid(row=row_index + 1, column=col_index)
                self.day_buttons.append(btn)

    def display_prev(self, year, month):
        self.clear_calendar()
        self.display_calendar(year, month)

    def display_next(self, year, month):
        self.clear_calendar()
        self.display_calendar(year, month)

    def update(self, month, day, year):
        selected_date = datetime(year, month, day)
        formatted_date = selected_date.strftime("%B %d, %Y")
        weekday = selected_date.strftime("%A")
        self.selected_date_label.config(text=f"Selected Date: {formatted_date}, {weekday}")

    def clear_calendar(self):
        for button in self.day_buttons:
            button.grid_forget()
            button.destroy()
        self.day_buttons.clear()

if __name__ == '__main__':
    parent = tk.Tk()
    date = Calendar_Widget(parent)
    parent.mainloop()
