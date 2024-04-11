import tkinter as tk
from tkinter import scrolledtext
from tkinter import messagebox
from tkinter import filedialog
import threading

# Assuming your PortScanner class is already defined

class PortScannerGUI:
    def __init__(self, master):
        self.master = master
        master.title("Port Scanner")

        # Target IP/Hostname
        self.label_target = tk.Label(master, text="Target IP/Hostname:")
        self.label_target.pack()
        self.entry_target = tk.Entry(master)
        self.entry_target.pack()

        # Ports
        self.label_ports = tk.Label(master, text="Port(s):")
        self.label_ports.pack()
        self.entry_ports = tk.Entry(master)
        self.entry_ports.pack()

        # Threads
        self.label_threads = tk.Label(master, text="Number of Threads:")
        self.label_threads.pack()
        self.entry_threads = tk.Entry(master)
        self.entry_threads.pack()

        # Timeout
        self.label_timeout = tk.Label(master, text="Timeout (seconds):")
        self.label_timeout.pack()
        self.entry_timeout = tk.Entry(master)
        self.entry_timeout.pack()

        # Output File
        self.label_output = tk.Label(master, text="Output File (optional):")
        self.label_output.pack()
        self.entry_output = tk.Entry(master)
        self.entry_output.pack()
        self.button_output = tk.Button(master, text="Browse", command=self.browse_file)
        self.button_output.pack()

        # Start Scan Button
        self.scan_button = tk.Button(master, text="Start Scan", command=self.start_scan)
        self.scan_button.pack()

        # Results Area
        self.results_area = scrolledtext.ScrolledText(master, height=10)
        self.results_area.pack()

    def browse_file(self):
        filename = filedialog.asksaveasfilename(defaultextension=".txt")
        self.entry_output.delete(0, tk.END)
        self.entry_output.insert(0, filename)

    def start_scan(self):
        target = self.entry_target.get()
        ports = self.entry_ports.get()  # This needs to be formatted into a list
        threads = self.entry_threads.get()
        timeout = self.entry_timeout.get()
        output = self.entry_output.get()
        
        # Validation or conversion of ports input to a list can be done here
        # Starting the scan in a non-blocking way
        threading.Thread(target=self.run_scan, args=(target, ports, threads, timeout, output), daemon=True).start()

    def run_scan(self, target, ports, threads, timeout, output):
        # Your scanning logic goes here
        # Update the GUI with the scan results
        # This is a placeholder for the logic to run the scan and handle results
        print("Scanning... (this is where you'd integrate your scanner)")

        # To update the GUI from another thread, use the following pattern:
        # self.results_area.insert(tk.END, "Results go here\n")

if __name__ == "__main__":
    root = tk.Tk()
    my_gui = PortScannerGUI(root)
    root.mainloop()
