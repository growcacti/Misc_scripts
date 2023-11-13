import tkinter as tk
from subprocess import Popen, PIPE

def runcmd(cmd, verbose=False):
    process = Popen(
        cmd,
        stdout=PIPE,
        stderr=PIPE,
        text=True,
        shell=True
    )
    std_out, std_err = process.communicate()
    if verbose:
        print(std_out.strip(), std_err)

def download_file():
    cmd = "wget "
    if timestamping_var.get():
        cmd += "--timestamping "
    # Add other options based on user input
    cmd += url_entry.get()
    runcmd(cmd, verbose=True)
    # Display output to the user

root = tk.Tk()
# Add widgets here
url_entry = tk.Entry(root)
timestamping_var = tk.BooleanVar()
timestamping_cb = tk.Checkbutton(root, text="Timestamping", variable=timestamping_var)
download_btn = tk.Button(root, text="Download", command=download_file)

# Pack or grid widgets
url_entry.pack()
timestamping_cb.pack()
download_btn.pack()

root.mainloop()
