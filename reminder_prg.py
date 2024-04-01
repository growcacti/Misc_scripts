import tkinter as tk
from tkinter import ttk, filedialog
from tkcalendar import Calendar
import datetime
import csv

def update_time():
    now = datetime.datetime.now()
    time_label.config(text=now.strftime('%Y-%m-%d %H:%M:%S'))
    root.after(1000, update_time)

def add_reminder():
    selected_date = calendar.get_date()
    reminder_text = entry.get()
    if reminder_text:  # Only add if there's text
        full_reminder = f"{selected_date}: {reminder_text}"
        text_widget.insert(tk.END, full_reminder + '\n')
        entry.delete(0, tk.END)

def save_reminders():
    file_path = filedialog.asksaveasfilename(defaultextension=".csv",
                                             filetypes=[("CSV files", "*.csv"), ("All files", "*.*")])
    if file_path:
        with open(file_path, 'w', newline='') as file:
            writer = csv.writer(file)
            reminders = text_widget.get("1.0", tk.END).strip().split('\n')
            for reminder in reminders:
                date, text = reminder.split(": ", 1)
                writer.writerow([date, text])

def load_reminders():
    file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv"), ("All files", "*.*")])
    if file_path:
        text_widget.delete("1.0", tk.END)
        try:
            with open(file_path, newline='') as file:
                reader = csv.reader(file)
                for date, text in reader:
                    text_widget.insert(tk.END, f"{date}: {text}\n")
        except FileNotFoundError:
            print("File not found.")

root = tk.Tk()
root.title("Reminder Application with Calendar and File Dialogs")
root.geometry("800x500")
root.resizable(True, True)
main_frame = tk.Frame(root)
main_frame.pack(fill=tk.BOTH, expand=True)
main_frame.columnconfigure(0, weight=1)
main_frame.rowconfigure(0, weight=1)

canvas = tk.Canvas(main_frame)
canvas.grid(row=0, column=0, sticky="nsew")

scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
scrollbar.grid(row=0, column=1, sticky="ns")

canvas.configure(yscrollcommand=scrollbar.set)

second_frame = tk.Frame(canvas)
canvas.create_window((0, 0), window=second_frame, anchor="nw")

time_label = tk.Label(second_frame, text="")
time_label.grid(row=0, column=0, columnspan=3, sticky="ew")
update_time()

calendar = Calendar(second_frame)
calendar.grid(row=1, column=0, sticky="ew", padx=10, pady=10)

entry = tk.Entry(second_frame)
entry.grid(row=2, column=0, sticky="ew", padx=10)

add_button = tk.Button(second_frame, text="Add Reminder", command=add_reminder)
add_button.grid(row=2, column=1, padx=10)

load_button = tk.Button(second_frame, text="Load Reminders", command=load_reminders)
load_button.grid(row=2, column=2, padx=10)

save_button = tk.Button(second_frame, text="Save Reminders", command=save_reminders)
save_button.grid(row=2, column=3, padx=10)

text_widget = tk.Text(second_frame, height=10)
text_widget.grid(row=3, column=0, columnspan=4, sticky="ew", padx=10, pady=10)

second_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

root.mainloop()
