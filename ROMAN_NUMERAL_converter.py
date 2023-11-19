import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import showinfo
import re

# Custom exceptions
class OutOfRangeError(ValueError):
    pass

class NotIntegerError(ValueError):
    pass

class InvalidRomanNumeralError(ValueError):
    pass

root = tk.Tk()
root.geometry("500x500")
root.resizable(True, True)
root.title("Convert Integer to Roman Numeral")

# Result display listbox
lb = tk.Listbox(root)
lb.grid(row=3, column=0)

# Roman numeral mapping
romanNumeralMap = (
    ("M", 1000), ("CM", 900), ("D", 500), ("CD", 400),
    ("C", 100), ("XC", 90), ("L", 50), ("XL", 40),
    ("X", 10), ("IX", 9), ("V", 5), ("IV", 4), ("I", 1),
)

# Convert integer to Roman numeral
def toRoman(n):
    
    if n <= 0:
        raise OutOfRangeError("number must be greater than 0")
    if int(n) != n:
        raise NotIntegerError("decimals can not be converted")

    result = ""
    for numeral, integer in romanNumeralMap:
        while n >= integer:
            result += numeral
            n -= integer

    lb.insert(tk.END, result)

   

# Roman numeral validation pattern
romanNumeralPattern = re.compile(
    "^M{0,4}(CM|CD|D?C{0,3})(XC|XL|L?X{0,3})(IX|IV|V?I{0,3})$",
    re.VERBOSE,
)

# Convert Roman numeral to integer
def fromRoman(s):
    if not s:
        raise InvalidRomanNumeralError("Input can not be blank")
    if not romanNumeralPattern.search(s):
        raise InvalidRomanNumeralError("Invalid Roman numeral: %s" % s)

    result = 0
    index = 0
    for numeral, integer in romanNumeralMap:
        while s[index : index + len(numeral)] == numeral:
            result += integer
            index += len(numeral)
    return result

# Clear listbox content
def clearlist():
    lb.delete(0, tk.END)

# Entry for number input
number_entry = tk.Entry(root)
number_entry.grid(row=0, column=0)

# Button to convert number to Roman numeral
convert_button = tk.Button(
    root,
    text="Convert to Roman Numeral",
    bg="light green",
    command=lambda: toRoman(int(number_entry.get()))
)
convert_button.grid(row=1, column=0)

# Button to clear results
clear_button = tk.Button(root, text="Clear", bg="light blue", command=clearlist)
clear_button.grid(row=4, column=0)

root.mainloop()
