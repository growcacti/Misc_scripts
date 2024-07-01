#!/bin/python3
import tkinter as tk
from tkinter import messagebox
from datetime import datetime

DOOMSDAY_LEAP = [4, 1, 7, 4, 2, 6, 4, 1, 5, 3, 7, 5]
DOOMSDAY_NOT_LEAP = [3, 7, 7, 4, 2, 6, 4, 1, 5, 3, 7, 5]
WEEK_DAY_NAMES = {
    0: "Sunday",
    1: "Monday",
    2: "Tuesday",
    3: "Wednesday",
    4: "Thursday",
    5: "Friday",
    6: "Saturday",
}

def get_week_day(year: int, month: int, day: int) -> str:
    """Returns the week-day name out of a given date."""
    assert len(str(year)) > 2, "year should be in YYYY format"
    assert 1 <= month <= 12, "month should be between 1 to 12"
    assert 1 <= day <= 31, "day should be between 1 to 31"
    
    # Validate the date
    try:
        datetime(year, month, day)
    except ValueError:
        raise AssertionError("Invalid date")
    
    century = year // 100
    century_anchor = (5 * (century % 4) + 2) % 7
    centurian = year % 100
    centurian_m = centurian % 12
    dooms_day = (
        (centurian // 12) + centurian_m + (centurian_m // 4) + century_anchor
    ) % 7
    day_anchor = (
        DOOMSDAY_NOT_LEAP[month - 1]
        if (year % 4 != 0) or (centurian == 0 and (year % 400) == 0)
        else DOOMSDAY_LEAP[month - 1]
    )
    week_day = (dooms_day + day - day_anchor) % 7
    return WEEK_DAY_NAMES[week_day]

def show_week_day():
    try:
        year = int(entry_year.get())
        month = int(entry_month.get())
        day = int(entry_day.get())
        week_day = get_week_day(year, month, day)
        messagebox.showinfo("Day of the Week", f"The day of the week is: {week_day}")
    except AssertionError as e:
        messagebox.showerror("Input Error", str(e))
    except Exception as e:
        messagebox.showerror("Error", str(e))

# Create the main window
root = tk.Tk()
root.title("Doomsday Algorithm - Day of the Week Calculator")

# Create and place the labels and entry widgets
tk.Label(root, text="Year (YYYY):").grid(row=0, column=0)
entry_year = tk.Entry(root)
entry_year.grid(row=0, column=1)

tk.Label(root, text="Month (MM):").grid(row=1, column=0)
entry_month = tk.Entry(root)
entry_month.grid(row=1, column=1)

tk.Label(root, text="Day (DD):").grid(row=2, column=0)
entry_day = tk.Entry(root)
entry_day.grid(row=2, column=1)

# Create and place the button
button_calculate = tk.Button(root, text="Calculate Day", command=show_week_day)
button_calculate.grid(row=3, columnspan=2)

# Run the application
root.mainloop()
