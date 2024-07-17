import tkinter as tk
import time

def update_time():
    # Get the current local time
    now = time.localtime()
    
    # Format the time in different formats
    time_standard = time.strftime("%Y-%m-%d %H:%M:%S", now)  # Standard format
    time_epoch = int(time.mktime(now))  # Epoch format
    
    # Update the entry with the desired format
    entry_var.set(f"Standard: {time_standard} | Epoch: {time_epoch}")

# Create the main window
root = tk.Tk()
root.title("Time Display")

# Create a StringVar to hold the text for the Entry widget
entry_var = tk.StringVar(root)

# Create an Entry widget and pack it into the window
entry = tk.Entry(root, textvariable=entry_var, width=50)
entry.pack(padx=10, pady=10)

# Create a Button widget that will update the Entry with the current time when clicked
button = tk.Button(root, text="Show Current Time", command=update_time)
button.pack(padx=10, pady=10)

# Start the main event loop
root.mainloop()
