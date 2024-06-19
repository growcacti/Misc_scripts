import socket
import tkinter as tk
from tkinter import scrolledtext

# Function to start the socket server
def start_server():
    s = socket.socket()
    text_widget.insert(tk.END, "Socket successfully created\n")
    
    port = 40674
    s.bind(('', port))
    text_widget.insert(tk.END, f"Socket binded to {port}\n")
    
    s.listen(5)
    text_widget.insert(tk.END, "Socket is listening\n")
    
    while True:
        c, addr = s.accept()
        text_widget.insert(tk.END, f"Got connection from {addr}\n")
        c.send(b'Thank you for connecting')
        c.close()

# Function to run the server in a separate thread
def run_server():
    import threading
    server_thread = threading.Thread(target=start_server)
    server_thread.daemon = True
    server_thread.start()

# Create the main window
root = tk.Tk()
root.title("Socket Server")

# Create a scrolled text widget
text_widget = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=40, height=10)
text_widget.pack(padx=10, pady=10)

# Create a start button
start_button = tk.Button(root, text="Start Server", command=run_server)
start_button.pack(pady=10)

# Start the Tkinter event loop
root.mainloop()
