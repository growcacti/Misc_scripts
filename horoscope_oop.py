import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import showinfo
from bs4 import BeautifulSoup
import requests


MONTH_NAME_TO_NUM = {
    'Jan': 1, 'Feb': 2, 'Mar': 3, 'Apr': 4, 'May': 5, 'Jun': 6,
    'Jul': 7, 'Aug': 8, 'Sep': 9, 'Oct': 10, 'Nov': 11, 'Dec': 12,
}

SIGN_TO_NUM = {
    'Aries': 1, 'Taurus': 2, 'Gemini': 3, 'Cancer': 4, 'Leo': 5, 'Virgo': 6,
    'Libra': 7, 'Scorpio': 8, 'Sagittarius': 9, 'Capricorn': 10, 'Aquarius': 11, 'Pisces': 12
}


class HoroscopeApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.geometry("1200x500")
        self.resizable(True, True)
        self.title("Horoscope")

        self.lb = tk.Listbox(self, selectmode=tk.SINGLE)
        self.lb.grid(row=0, column=2, rowspan=6, padx=10, pady=5)
        self.lb.bind("<<ListboxSelect>>", self.on_sign_selected)

        for sign in SIGN_TO_NUM:
            self.lb.insert(tk.END, sign)

        label = ttk.Label(self, text="Please select day then a month:")
        label.grid(row=0, column=0)

        self.sel_day = tk.StringVar()
        days = ["yesterday", "today", "tomorrow"]
        cb2 = ttk.Combobox(self, textvariable=self.sel_day)
        cb2.grid(row=3, column=1)
        cb2["values"] = days
        cb2["state"] = "readonly"

        self.text = tk.Text(self)
        self.text.grid(row=5, column=0, columnspan=2, padx=5, pady=5)

        btn1 = tk.Button(self, text="clear", bg="light green", bd=4, command=self.clear)
        btn1.grid(row=4, column=1)

        fetch_btn = tk.Button(self, text="Fetch Horoscope", command=self.on_fetch_click)
        fetch_btn.grid(row=11, column=2)

    def clear(self):
        self.text.delete("1.0", tk.END)  # Clear the Text widget

    def on_sign_selected(self, event):
        self.fetch_horoscope()

    def on_fetch_click(self):
        self.fetch_horoscope()

    def fetch_horoscope(self):
        try:
            index = self.lb.curselection()[0]
            selected_sign = self.lb.get(index)
        except IndexError:  # No sign selected from the list
            showinfo("Error", "Please select a zodiac sign from the list.")
            return

        # Set the selected day
        day = self.sel_day.get()
        if not day:
            day = "today"  # default to today if no day is selected

        zodiac_sign = SIGN_TO_NUM[selected_sign]
        horoscope_text = self.get_horoscope_text(zodiac_sign, day)
        self.text.delete(1.0, tk.END)  # Clear the Text widget
        self.text.insert(tk.END, horoscope_text)  # Insert the new horoscope text

    @staticmethod
    def get_horoscope_text(zodiac_sign: int, day: str) -> str:
          url = f"https://www.horoscope.com/us/horoscopes/general/horoscope-general-daily-{day}.aspx?sign={zodiac_sign}"
          soup = BeautifulSoup(requests.get(url).content, "html.parser")
          div = soup.find("div", class_="main-horoscope")
          if div and div.p:
              return div.p.text
          else:
              return "Horoscope not found."


if __name__ == "__main__":
    app = HoroscopeApp()
    app.mainloop()
