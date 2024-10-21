import tkinter as tk
from tkinter import filedialog, messagebox
import socket
import threading
import os
import nmap  # For network scanning

class FileTransferApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("File Transfer App with Network Scanner")
        self.geometry("500x400")
        
        # Variables
        self.role = tk.StringVar(value="Server")
        self.file_path = tk.StringVar(value="No file selected")
        self.server_ip = tk.StringVar(value="127.0.0.1")
        self.port = 5001
        self.is_running = False

        # UI Components
        self.create_widgets()

    def create_widgets(self):
        # Role Selection
        tk.Label(self, text="Choose Role:").grid(row=0, column=0, padx=10, pady=10)
        tk.Radiobutton(self, text="Server", variable=self.role, value="Server", command=self.toggle_role).grid(row=0, column=1)
        tk.Radiobutton(self, text="Client", variable=self.role, value="Client", command=self.toggle_role).grid(row=0, column=2)

        # File Selection (for Client)
        tk.Button(self, text="Select File", command=self.select_file).grid(row=1, column=0, padx=10, pady=10)
        tk.Label(self, textvariable=self.file_path).grid(row=1, column=1, columnspan=2)

        # Server IP Entry (for Client)
        tk.Label(self, text="Server IP:").grid(row=2, column=0, padx=10, pady=10)
        self.ip_entry = tk.Entry(self, textvariable=self.server_ip, state='disabled')
        self.ip_entry.grid(row=2, column=1, columnspan=2)

        # Network Scan Button
        tk.Button(self, text="Scan Network", command=self.scan_network).grid(row=3, column=0, columnspan=3, pady=10)

        # Listbox for displaying active IPs
        self.ip_listbox = tk.Listbox(self, height=6)
        self.ip_listbox.grid(row=4, column=0, columnspan=3, padx=10, pady=10)
        self.ip_listbox.bind('<<ListboxSelect>>', self.select_ip)

        # Start/Stop Button
        self.start_button = tk.Button(self, text="Start", command=self.start_transfer)
        self.start_button.grid(row=5, column=0, columnspan=3, pady=20)

        # Status Display
        self.status_label = tk.Label(self, text="Status: Idle", fg="blue")
        self.status_label.grid(row=6, column=0, columnspan=3, pady=10)

    def toggle_role(self):
        """Toggle entry state based on the selected role."""
        if self.role.get() == "Client":
            self.ip_entry.config(state='normal')
        else:
            self.ip_entry.config(state='disabled')

    def select_file(self):
        """Open file dialog to select a file (client-side)."""
        file_path = filedialog.askopenfilename()
        if file_path:
            self.file_path.set(file_path)

    def scan_network(self):
        """Scan the local network for active devices."""
        self.status_label.config(text="Status: Scanning network...", fg="orange")
        self.ip_listbox.delete(0, tk.END)  # Clear the listbox

        try:
            scanner = nmap.PortScanner()
            network_range = "192.168.1.0/24"  # Modify this according to your network range
            scanner.scan(hosts=network_range, arguments='-sn')

            active_hosts = [host for host in scanner.all_hosts() if scanner[host].state() == 'up']
            for host in active_hosts:
                self.ip_listbox.insert(tk.END, host)

            if active_hosts:
                self.status_label.config(text="Status: Scan complete", fg="green")
            else:
                self.status_label.config(text="Status: No devices found", fg="red")
        except Exception as e:
            messagebox.showerror("Error", f"Network scan error: {e}")
            self.status_label.config(text="Status: Idle", fg="blue")

    def select_ip(self, event):
        """Select IP from the listbox and set it as server IP."""
        selection = event.widget.curselection()
        if selection:
            ip = event.widget.get(selection[0])
            self.server_ip.set(ip)

    def start_transfer(self):
        """Start the file transfer process (server or client)."""
        if self.is_running:
            self.is_running = False
            self.status_label.config(text="Status: Stopped", fg="red")
            return

        self.is_running = True
        role = self.role.get()

        if role == "Server":
            self.status_label.config(text="Status: Starting server...", fg="green")
            threading.Thread(target=self.run_server, daemon=True).start()
        elif role == "Client":
            self.status_label.config(text="Status: Sending file...", fg="green")
            threading.Thread(target=self.send_file, daemon=True).start()

    def run_server(self):
        """Run the server to receive a file."""
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
            server_socket.bind(('0.0.0.0', self.port))
            server_socket.listen(1)
            self.status_label.config(text="Status: Waiting for connection...", fg="blue")
            
            try:
                client_socket, client_address = server_socket.accept()
                self.status_label.config(text=f"Connected to {client_address}", fg="green")
                
                with open('received_file', 'wb') as f:
                    while True:
                        data = client_socket.recv(1024)
                        if not data:
                            break
                        f.write(data)

                self.status_label.config(text="File received successfully!", fg="green")
            except Exception as e:
                messagebox.showerror("Error", f"Server error: {e}")
                self.status_label.config(text="Status: Idle", fg="blue")
                self.is_running = False

    def send_file(self):
        """Send a file to the server (client-side)."""
        file_path = self.file_path.get()
        server_ip = self.server_ip.get()

        if not os.path.isfile(file_path):
            messagebox.showerror("Error", "Please select a valid file!")
            self.status_label.config(text="Status: Idle", fg="blue")
            self.is_running = False
            return

        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
                client_socket.connect((server_ip, self.port))
                
                with open(file_path, 'rb') as f:
                    for data in iter(lambda: f.read(1024), b''):
                        client_socket.sendall(data)

            self.status_label.config(text="File sent successfully!", fg="green")
        except Exception as e:
            messagebox.showerror("Error", f"Client error: {e}")
        finally:
            self.is_running = False

if __name__ == "__main__":
    app = FileTransferApp()
    app.mainloop()
