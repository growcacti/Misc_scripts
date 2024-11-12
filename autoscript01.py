import tkinter as tk
from tkinter import messagebox
import pyautogui
import time
import webbrowser

# Function to start the automation
def automate_login():
    web_address = url_entry.get()
    username = username_entry.get()
    password = password_entry.get()
    delay = float(delay_entry.get())
    
    if not web_address or not username or not password:
        messagebox.showerror("Error", "Please fill in all fields.")
        return

    # Open the web browser
    webbrowser.open(web_address)
    time.sleep(delay)

    # Automate login with PyAutoGUI
    pyautogui.write(username)
    pyautogui.press('tab')
    time.sleep(0.5)
    pyautogui.write(password)
    pyautogui.press('enter')

# Create the Tkinter interface
root = tk.Tk()
root.title("Login Automation")
root.geometry("400x200")

# URL Entry
tk.Label(root, text="Website URL:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
url_entry = tk.Entry(root, width=30)
url_entry.grid(row=0, column=1, padx=5, pady=5)

# Username Entry
tk.Label(root, text="Username:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
username_entry = tk.Entry(root, width=30)
username_entry.grid(row=1, column=1, padx=5, pady=5)

# Password Entry
tk.Label(root, text="Password:").grid(row=2, column=0, padx=5, pady=5, sticky="w")
password_entry = tk.Entry(root, width=30, show="*")
password_entry.grid(row=2, column=1, padx=5, pady=5)

# Delay Entry
tk.Label(root, text="Delay (seconds):").grid(row=3, column=0, padx=5, pady=5, sticky="w")
delay_entry = tk.Entry(root, width=10)
delay_entry.grid(row=3, column=1, padx=5, pady=5, sticky="w")
delay_entry.insert(0, "5")  # Default delay

# Automate Button
start_button = tk.Button(root, text="Start Automation", command=automate_login)
start_button.grid(row=4, column=0, columnspan=2, pady=10)

root.mainloop()
