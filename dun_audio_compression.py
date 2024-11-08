import tkinter as tk
import subprocess

def toggle_drc():
    global drc_enabled
    if drc_enabled:
        subprocess.run(["pactl", "unload-module", "module-ladspa-sink"])
        status_label.config(text="DRC Disabled", fg="red")
    else:
        subprocess.run([
            "pactl", "load-module", "module-ladspa-sink",
            "sink_name=ladspa_compressor", "plugin=compressor",
            "label=compressor", "control=0,1,0.5,0.5,0.5,0.5,1,0.5"
        ])
        status_label.config(text="DRC Enabled", fg="green")
    drc_enabled = not drc_enabled

def check_drc_status():
    global drc_enabled
    result = subprocess.run(["pactl", "list", "modules", "short"], stdout=subprocess.PIPE)
    drc_enabled = "module-ladspa-sink" in result.stdout.decode()
    status_label.config(text="DRC Enabled" if drc_enabled else "DRC Disabled", fg="green" if drc_enabled else "red")

# Initialize the GUI
root = tk.Tk()
root.title("DRC Toggle")

# Layout
root.grid_columnconfigure(0, weight=1)
root.grid_rowconfigure(0, weight=1)
root.grid_rowconfigure(1, weight=1)

status_label = tk.Label(root, text="Checking DRC status...", font=("Arial", 14))
status_label.grid(row=0, column=0, pady=10, padx=10)

toggle_button = tk.Button(root, text="Toggle DRC", command=toggle_drc, font=("Arial", 12))
toggle_button.grid(row=1, column=0, pady=10, padx=10)

# Check initial status of DRC
check_drc_status()

root.mainloop()
