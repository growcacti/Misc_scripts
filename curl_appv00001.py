import tkinter as tk
from tkinter import filedialog
import subprocess

def browse_folder():
    """ Open a dialog to select a folder """
    folder_selected = filedialog.askdirectory()
    folder_entry.delete(0, tk.END)
    folder_entry.insert(tk.END, folder_selected)

def download_file():
    """ Download the file using curl """
    url = url_entry.get()
    destination = folder_entry.get()
    command = f"curl -L {url} -o {destination}/{url.split('/')[-1]}"
    
    try:
        subprocess.run(command, check=True, shell=True)
        status_label.config(text="Download successful!")
    except subprocess.CalledProcessError:
        status_label.config(text="Error during download.")

# Create the main window
root = tk.Tk()
root.title("File Downloader")

# URL entry
url_label = tk.Label(root, text="URL:")
url_label.pack()
url_entry = tk.Entry(root, width=50)
url_entry.pack()

# Folder entry and browse button
folder_label = tk.Label(root, text="Save to Folder:")
folder_label.pack()
folder_entry = tk.Entry(root, width=50)
folder_entry.pack()
browse_button = tk.Button(root, text="Browse", command=browse_folder)
browse_button.pack()

# Download button
download_button = tk.Button(root, text="Download", command=download_file)
download_button.pack()

# Status label
status_label = tk.Label(root, text="")
status_label.pack()

# Run the application
root.mainloop()
