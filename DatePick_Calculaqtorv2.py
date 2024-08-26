import tkinter as tk
from tkinter import ttk, END
from datetime import datetime
from time import time, strftime, localtime
import calendar
# Date and Time Picker/Calculator that only uses the standard library
#  by JH

class DatePicker_Calculator:
    def __init__(self, parent):
        self.parent = parent
        self.now = datetime.now().strftime("%m %d %Y %H %M %S")
        month, day, year, hour, minute, second = self.now.split()
        self.current_time = strftime('%H:%M:%S', localtime())

        # Entry frame using grid
        self.efrm = tk.Frame(self.parent, width=180, height=15)
        self.efrm.grid(row=0, column=0)
         

        # Spinboxes for hour, minute, second
        self.hour_var = tk.StringVar(value=hour)
        self.hour_spin = ttk.Spinbox(self.efrm, from_=0, to=23, width=2, textvariable=self.hour_var)
        self.hour_spin.grid(row=0, column=5)

        self.minute_var = tk.StringVar(value=minute)
        self.minute_spin = ttk.Spinbox(self.efrm, from_=0, to=59, width=2, textvariable=self.minute_var)
        self.minute_spin.grid(row=0, column=6)

        self.second_var = tk.StringVar(value=second)
        self.second_spin = ttk.Spinbox(self.efrm, from_=0, to=59, width=2, textvariable=self.second_var)
        self.second_spin.grid(row=0, column=7)

        tk.Label(self.efrm, text="T1 Entry").grid(row=0,column=0)
        self.et1 = tk.Entry(self.efrm, bd=7)
        self.et1.grid(row=0, column=1)
        tk.Label(self.efrm, text="T2 Entry").grid(row=1,column=0)
        self.et2 = tk.Entry(self.efrm, bd=7)
        self.et2.grid(row=1, column=1)
        tk.Label(self.efrm, text="").grid(row=1,column=2)
        tk.Label(self.efrm, text="Date Selection").grid(row=0,column=4)
        self.et11 = tk.Entry(self.efrm, bd=7,width=60)
        self.et11.grid(row=1, column=4, columnspan=2)
        tk.Label(self.efrm, text="Time Difference").grid(row=3,column=4)
        self.et22 = tk.Entry(self.efrm, bd=7,width=60)
        self.et22.grid(row=2, column=4, columnspan=2)
        self.et3 = tk.Entry(self.efrm, bd=7)
        
        tk.Label(self.efrm, text="Date1").grid(row=0,column=7)
        self.et3.grid(row=1, column=7)
        tk.Label(self.efrm, text="Date2").grid(row=3,column=7)
        self.et4 = tk.Entry(self.efrm, bd=7)
        self.et4.grid(row=4, column=7)
        tk.Label(self.efrm, text="Date Diff").grid(row=0,column=10)
        self.output=tk.Text(self.efrm,width=40,height=8)
        self.output.grid(row=0,column=12)
        tk.Label(self.efrm, text="Current Epoch Time").grid(row=0,column=16)
        self.et7 = tk.Entry(self.efrm, bd=7,font=("Helvetica", 14))
        self.et7.grid(row=0, column=17)
        tk.Label(self.efrm, text="Current Time").grid(row=1,column=16)
        self.et8 = tk.Entry(self.efrm, bd=7,font=("Helvetica", 14))
        self.et8.grid(row=1, column=17)
        #tk.Label(self.efrm, text="").grid(row=1,column=0)
        self.current_month = datetime.now().month  # Corrected to datetime.now().month
        self.current_year = datetime.now().year    # Corrected to datetime.now().year
        self.current_time = strftime('%H:%M:%S', localtime())
        self.epoch_time = int(time())  # Removed the typo 'aself'
        nav_frame = tk.Frame(self.parent, width=40, height=40)
        nav_frame.grid(row=1, column=0, pady=10)

        b1=tk.Button(self.efrm, text="Time1",bd=4, command=self.insert1)
        b1.grid(row=10, column=0)
        b2=tk.Button(self.efrm, text="Time2",bd=4, command=self.insert2)
        b2.grid(row=11, column=0)
        b3=tk.Button(self.efrm, text="Calculate Diff",bd=6,command=self.hour_diff)
        b3.grid(row=10, column=1)
        b4=tk.Button(self.efrm, text="Date1", bd=4,command=self.date1)
        b4.grid(row=10, column=12)    
        b5=tk.Button(self.efrm, text="Date2", bd=4,command=self.date2)
        b5.grid(row=11, column=12)
        b6=tk.Button(self.efrm, text="Calculate Date Diff",bd=7, command=self.date_diff)
        b6.grid(row=10, column=15)
        bt12=tk.Button(self.efrm, text="Clear Entries",bd=5, command=self.clear)
        bt12.grid(row=10, column=20)
        self.month_pick = tk.Entry(self.efrm, bd=9,width=20)
        self.month_pick.grid(row=20, column=4)
        self.day_pick = tk.Entry(self.efrm, bd=9,width=20)
        self.day_pick.grid(row=20, column=5)


        # Previous month button
        self.day_buttons = []
        prev_month_btn = tk.Button(nav_frame, text="< Prev",bd=6, command=self.prev_month)
        prev_month_btn.grid(row=0, column=0)

        # Month/Year label
        self.month_year_label = tk.Label(nav_frame, text="", font=("Helvetica", 16))
        self.month_year_label.grid(row=20, column=1)

        # Next month button
        next_month_btn = tk.Button(nav_frame, text="Next >",bd=6, command=self.next_month)
        next_month_btn.grid(row=0, column=2)

        # Calendar frame using grid
        self.calendar_frame = tk.Frame(self.parent)
        self.calendar_frame.grid(row=2, column=0, rowspan=2,columnspan=2)
        
        # Display the current month calendar
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

        # Fill in the days of the month
        month_days = calendar.monthcalendar(year, month)
        month_days = calendar.monthcalendar(year, month)

        self.day_buttons.clear()  # Make sure to clear the list before adding new buttons
        for row_index, week in enumerate(month_days):
            for col_index, day in enumerate(week):
                if day == 0:
                    # Create a blank label for alignment if the day is 0 (empty cell)
                    lbl = tk.Label(self.calendar_frame, text="")
                    lbl.grid(row=row_index + 1, column=col_index)
                    continue
                btn = tk.Button(self.calendar_frame, text=str(day), bd=16, width=3, height=2,bg="alice blue",font=("Helvetica", 14),
                                command=lambda m=month, d=day, y=year: self.update(m, d, y))
                btn.grid(row=row_index + 1, column=col_index)
                self.day_buttons.append(btn)  # Add the button to the list

    def display_prev(self, year, month):
        self.clear_calendar()
        self.display_calendar(year, month)

    def display_next(self, year, month):
        self.clear_calendar()
        self.display_calendar(year, month)

    
    def update_clock(self):
        self.time = f"{self.hour_var.get()}:{self.minute_var.get()}:{self.second_var.get()}"
        
        self.current_time = strftime('%H:%M:%S', localtime())
        self.epoch_time = int(time())
        self.et7.delete(0, END)
        self.et8.delete(0, END)
        self.et7.insert(END, self.epoch_time)  # Corrected the typo 'eself.poch_time'
        self.et8.insert(END, self.current_time)  # Corrected the typo 'cuurent_time'
        self.parent.after(1000, self.update_clock)
    def update(self, month, day, year):
        weekday_dict = {0: "Monday", 1: "Tuesday", 2: "Wednesday", 3: "Thursday", 
                     4: "Friday", 5: "Saturday", 6: "Sunday"}

          # Create a date object from the year, month, and day
        months_dict = {'January': 1, 'February': 2,'March': 3, 'April': 4,'May': 5,
                  'June': 6,'July': 7, 'August': 8, 'September': 9,'October': 10,
                  'November': 11,'December': 12}

        # Create a date object from the year, month, and day
        self.date_obj = datetime(year, month, day)
        formatted_date = self.date_obj.strftime("%m-%d-%Y")  # Format the date as "month-day-year"

        # Get the day of the week as an integer (Monday is 0, Sunday is 6)
        day_of_week_int = self.date_obj.weekday()

        # Use the day_of_week_int to get the day name from weekday_dict
        day_of_week_name = weekday_dict[day_of_week_int]

        # Get the month name from the month number
        month_name = calendar.month_name[month]

        # Update the daypick entry with the day of the week name
        self.day_pick.delete(0, tk.END)
        self.day_pick.insert(tk.END, day_of_week_name)

        # Update the month_pick entry with the month name
        self.month_pick.delete(0, tk.END)
        self.month_pick.insert(tk.END, month_name)

        # Update the date Entry with the formatted date
        self.et11.delete(0, tk.END)
        self.et11.insert(tk.END, formatted_date)

    def insert1(self):
        self.time = f"{self.hour_var.get()}:{self.minute_var.get()}:{self.second_var.get()}"
        self.et1.delete(0, END)
        self.et1.insert(END, self.time)
        
    def insert2(self):
        self.time = f"{self.hour_var.get()}:{self.minute_var.get()}:{self.second_var.get()}"
        self.et2.delete(0, END)
        self.et2.insert(END, self.time)
    def date1(self):
        dateone = self.et11.get()
        self.et3.delete(0, END)
        self.et3.insert(END, dateone)


    def date2(self):
        datetwo = self.et11.get()
        self.et4.delete(0, END)
        self.et4.insert(END, datetwo)
    def hour_diff(self):
        hhmmss = "%H:%M:%S"
        try:
            self.et11.delete(0, END)
            print(self.et1.get())
            print(self.et2.get())
            start_time = datetime.strptime(self.et1.get(), hhmmss).time()
            end_time = datetime.strptime(self.et2.get(), hhmmss).time()
            # Calculate the difference in seconds
            difference_in_seconds = (datetime.combine(datetime.today(), end_time) - datetime.combine(datetime.today(), start_time)).total_seconds()
            # Convert seconds to hours and minutes
            hours, remainder = divmod(difference_in_seconds, 3600)
            minutes, seconds = divmod(remainder, 60)
            
            result = f"Time difference: {int(hours)} hours  {int(minutes)} minutes and {int(seconds)} Seconds"
       
            self.et22.delete(0, END)
            
            self.et22.insert(END, result)
        except ValueError:
            self.et22.delete(0, END)
  
    def date_diff(self):
        date_format = "%m-%d-%Y"  # Date format without time
        try:
            start_date_str = self.et3.get()
            end_date_str = self.et4.get()
            start_date = datetime.strptime(start_date_str, date_format)
            end_date = datetime.strptime(end_date_str, date_format)

            # Calculate the difference in seconds between the two dates
            difference_in_seconds = (end_date - start_date).total_seconds()

            # Define the number of seconds in each time unit
            minute = 60
            hour = minute * 60
            day = hour * 24
            week = day * 7
            # Approximate the average month length
            month = day * 30.436875
            # Approximate the average year length (including leap years)
            year = day * 365.2425

            # Calculate the time difference in each unit
            years, rem = divmod(difference_in_seconds, year)
            months, rem = divmod(rem, month)
            weeks, rem = divmod(rem, week)
            days, rem = divmod(rem, day)
            hours, rem = divmod(rem, hour)
            minutes, seconds = divmod(rem, minute)

            # Format the result
            result = f"Date difference: {int(years)} years, {int(months)} months, {int(weeks)} weeks, {int(days)} days, {int(hours)} hours, {int(minutes)} minutes, {int(seconds)} seconds"
            self.output.delete("1.0", END)
            self.output.insert(END, result)
        except ValueError:
            self.output.delete("1.0", END)
            self.output.insert(END, "Invalid date format. Please use MM-DD-YYYY")
    def clear(self):
        self.et1.delete(0, END)
        self.et2.delete(0, END)
        self.et3.delete(0, END)
        self.et4.delete(0, END)
        self.et11.delete(0, END)
        self.et22.delete(0, END)     
        self.output.delete("1.0", END)
    def find_day(self, month,day,year):
        daynum = calendar.weekday(year, month, day)
        # Modify days list to start with Sunday as 0
        days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday","Sunday"]
        return days[daynum]   
    def clear_calendar(self):
        for button in self.day_buttons:
            button.grid_forget()  # This will remove the button from the grid
            button.destroy()      # This will destroy the button widget
        self.day_buttons.clear()
if __name__ == '__main__':
    parent = tk.Tk()
    dp = DatePicker_Calculator(parent)
    parent.after(1000, dp.update_clock)
    parent.mainloop()
