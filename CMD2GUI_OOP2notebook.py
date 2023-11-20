import tkinter as tk
from tkinter import ttk, Toplevel, END,INSERT
import subprocess
import shlex
import sys
import os
from tkinter import filedialog
from tkinter import scrolledtext


from cmdlist import *



class CommandExecutorApp:
    def __init__(self, root,cmdlist1):
        self.root = root
        self.cmdlist1 =cmdlist1
        root.title("CL Commander")
        self.notebook = ttk.Notebook(self.root)
        self.notebook.grid(row=0, column=0)

        self.frm1 = ttk.Frame(self.notebook, width=200, height=45)
        self.notebook.add(self.frm1, text="CMD1")
        self.sidefrm = tk.Frame(self.frm1, width=60, height=40)
        self.sidefrm.grid(row=0, column=0)
        tk.Label(self.sidefrm,text="    ").grid(row=0,column=0)
        tk.Label(self.sidefrm,text="    ").grid(row=2,column=0)
        tk.Label(self.sidefrm,text="    ").grid(row=4,column=0)
        tk.Label(self.sidefrm,text="    ").grid(row=5,column=0)
        tk.Label(self.sidefrm,text="    ").grid(row=6,column=0)
        tk.Label(self.sidefrm,text="    ").grid(row=7,column=0)
        self.frm2 = ttk.Frame(self.notebook, width=200, height=600)
        self.notebook.add(self.frm2, text="")
        tk.Label(self.frm2,text="              ").grid(row=0,column=0)
        tk.Label(self.frm2,text="               ").grid(row=2,column=0)
        tk.Label(self.frm2,text="              ").grid(row=4,column=0)
        tk.Label(self.frm2,text="             ").grid(row=5,column=0)
       
        self.cb1 =ttk.Combobox(self.frm2, values=self.cmdlist1)
        self.cb1.grid(row=2,column=2)
        self.lbox = tk.Listbox(self.frm2,bd=7,bg="lavender")
        self.lbox.grid(row=2,column=4)
        self.send = tk.Button(self.frm2, text="send to CMD Entry",bg="orange", bd=5, command=self.send)
        self.send.grid(row=6, column=2)
        self.lbadd = tk.Button(self.frm2,text="populate listbox",bg="violet", bd=5, command=self.populate_lbox)
        self.lbadd.grid(row=8, column=4)
        self.frm3 = ttk.Frame(self.notebook, width=200, height=200)
        self.notebook.add(self.frm3, text="")
        self.textwidget = scrolledtext.ScrolledText(self.frm3, height=45, width=100, bg="white", bd=10)
        self.textwidget.grid(row=0, column=0, sticky="nsew")
        self.textwidget.insert("1.0", "end-1c")

        
        self.frm4 = ttk.Frame(self.notebook, width=200, height=200)
        self.notebook.add(self.frm4, text="4")
        self.frm5 = ttk.Frame(self.notebook, width=200, height=200)
        self.notebook.add(self.frm5, text="5")

        self.frm6 = ttk.Frame(self.notebook, width=200, height=200)
        self.notebook.add(self.frm6, text="6")
        self.frm7 = ttk.Frame(self.notebook, width=200, height=200)
        self.notebook.add(self.frm5, text="7")

        self.frm8 = ttk.Frame(self.notebook, width=200, height=200)
        self.notebook.add(self.frm8, text="8")
        self.frm9 = ttk.Frame(self.notebook, width=200, height=200)
        self.notebook.add(self.frm9, text="9")


        self.path = os.getcwd()
        tk.Label(self.frm1, text="Directory Path").grid(row=1, column=6)
        self.dirpath= tk.Entry(self.frm1, bd=7, width=50)
        self.dirpath.grid(row=3,column=6)
        self.dirpath.insert(END, self.path)
        tk.Label(self.frm1, text="Command Line Entry").grid(row=5, column=6)
        self.entry = tk.Entry(self.frm1,bd=4, width=50)
        self.entry.grid(row=6, column=6, columnspan=2, padx=10, pady=10)

        run_button = tk.Button(self.frm1, text="Run Command", command=self.run_command)
        run_button.grid(row=9, column=6, padx=10, pady=10)

       # Inside your CommandExecutorApp class

        self.output_text = scrolledtext.ScrolledText(self.frm1, height=10, width=50)
        self.output_text.grid(row=12, column=6, columnspan=2, padx=10, pady=10)

        save_button = tk.Button(self.frm1, text="Save Output", command=self.save_output)
        save_button.grid(row=13, column=6, padx=10, pady=10)

        clear_button = tk.Button(self.frm1, text="Clear Output", command=self.clear)
        clear_button.grid(row=13, column=6, padx=10, pady=10)

        listdrv_button = tk.Button(self.frm1, text="List Drives", command=self.list_drives)
        listdrv_button.grid(row=14, column=5, padx=10, pady=10)
        mount_button = tk.Button(self.frm1, text="Mount Drive", command=self.mount_drive)
        mount_button.grid(row=14, column=6, padx=10, pady=10)
        change_perm_button = tk.Button(self.frm1, text="Change Permissions", command=self.change_permissions)
        change_perm_button.grid(row=15, column=6, padx=10, pady=10)
        select_dir_button = tk.Button(self.frm1, text="Select Directory", command=self.select_directory)
        select_dir_button.grid(row=17, column=6, padx=10, pady=10)
    def run_command(self):
        command = self.entry.get()
        try:
            if sys.platform == "linux" or sys.platform == "linux2":
                # For Linux, execute the command using the shell
                process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            elif sys.platform == "win32":
                # For Windows, execute the command in PowerShell
                process = subprocess.Popen(["powershell", "-Command", command], stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
            
            output, error = process.communicate()
            self.output_text.delete('1.0', tk.END)
            self.output_text.insert(tk.END, output.decode())
            self.output_text.insert(tk.END, error.decode())
        except Exception as e:
            self.output_text.insert(tk.END, str(e))
    def clear(self):
        self.output_text.delete('1.0', tk.END)
    def save_output(self):
        output = self.output_text.get("1.0", tk.END)
        file_path = filedialog.asksaveasfilename(defaultextension=".txt")
        if file_path:
            with open(file_path, "w") as file:
                file.write(output)
    def list_drives(self):
        try:
            # Using 'lsblk' to list block devices
            result = subprocess.run(['lsblk'], stdout=subprocess.PIPE, text=True)
            self.output_text.insert(tk.END, result.stdout)
            return result.stdout
        except Exception as e:
            self.output_text.insert(tk.END. str(e))
            return str(e)


        # Inside your CommandExecutorApp class

    def mount_drive(self):
       

        def mount(drv_entry):
              device_path = drv_entry # Replace with the actual device path
              mount_point = "/mnt/usb"   # Replace with your mount point
              command = f"sudo mount {device_path} {mount_point}"
              try:
                  
                  subprocess.run(shlex.split(command), check=True)
                  self.output_text.insert(tk.END, f"Mounted {device_path} to {mount_point}\n")
              except subprocess.CalledProcessError as e:
                  self.output_text.insert(tk.END, f"Failed to mount: {e}\n")

        top =Toplevel()
        self.drv_entry = tk.Entry(top, width=50)
        self.drv_entry.grid(row=0, column=0, columnspan=2, padx=10, pady=10)
        mbutton = tk.Button(top, text="M", command=lambda: mount(self.drv_entry.get()))
        mbutton.grid(row=3, column=0, padx=10, pady=10)


    def change_permissions(self):
        top = Toplevel()
        self.path = self.dirpath.get()  # Get the path from the entry widget
        permissions =[ "u+rw","775","777"]  # Example permission, you can make this dynamic
        self.cb = ttk.Combobox(top,values =permissions)
        self.cb.grid(row=5,column=5)
        btn = tk.Button(top,text="send permission" ,bd=2, command=lambda :self.perm_set(self.cb.get()))
        btn.grid(row=7,column=5)
       
    def populate_lbox(self):
         self.lbox.delete(0, END)
         for item in cmditem:
             self.lbox.insert(END, item)
         
    def send(self):
        self.entry.delete(0, END)
        self.entry.insert(END, self.cb1.get())
        
    def perm_set(self,permissions):
         if not self.path:
            
            self.output_text.insert(tk.END, "Please select a directory first.\n")
            return

         command = f"chmod {permissions} '{self.path}'"
         try:
            subprocess.run(shlex.split(command), check=True)
            self.output_text.insert(tk.END, f"Changed permissions of {self.path} to {permissions}\n")
         except subprocess.CalledProcessError as e:
            self.output_text.insert(tk.END, f"Failed to change permissions: {e}\n")

    def create_directory(self):
        self.path = self.dir_path_entry.get()  # Get the directory path from the entry widget
        if not self.dirpath:
            self.output_text.insert(tk.END, "Please enter a directory path.\n")
            return

        try:
            os.makedirs(self.path, exist_ok=True)  # Create the directory, ignore if it already exists
            self.output_text.insert(tk.END, f"Directory created at {self.path}\n")
        except Exception as e:
            self.output_text.insert(tk.END, f"Failed to create directory: {e}\n")
    def select_directory(self):
        self.path = filedialog.askdirectory()  # Open the dialog and store the selected path
        if self.path:
            self.dirpath.delete(0, END)  # Clear the current entry
            self.dirpath.insert(0, self.path)  # Insert the selected path into the entry widget
                         
# Running the application
root = tk.Tk()
app = CommandExecutorApp(root,cmdlist1)
root.mainloop()
