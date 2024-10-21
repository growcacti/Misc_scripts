import os
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog, messagebox

class SymlinkCreator(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Symlink Creator")
        self.geometry("600x400")
        self.configure_gui()

    def configure_gui(self):
        # Frame for file selection
        frame = ttk.Frame(self)
        frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        # Source and target entries
        ttk.Label(frame, text="Source Path:").grid(row=0, column=0, sticky="w")
        self.source_entry = ttk.Entry(frame, width=50)
        self.source_entry.grid(row=0, column=1, padx=5, pady=5)
        ttk.Button(frame, text="Browse", command=self.browse_source).grid(row=0, column=2, padx=5)

        ttk.Label(frame, text="Target Path:").grid(row=1, column=0, sticky="w")
        self.target_entry = ttk.Entry(frame, width=50)
        self.target_entry.grid(row=1, column=1, padx=5, pady=5)
        ttk.Button(frame, text="Browse", command=self.browse_target).grid(row=1, column=2, padx=5)

        # Create symlink button
        create_button = ttk.Button(frame, text="Create Symlink", command=self.create_symlink)
        create_button.grid(row=2, column=1, pady=20)

        # Treeview for drive navigation
        self.tree = ttk.Treeview(self)
        self.tree.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")
        self.populate_drives()

    def populate_drives(self):
        # Detect external drives and list them in the treeview
        for drive in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
            if os.path.exists(f"{drive}:/"):
                self.tree.insert('', 'end', text=f"{drive}:/", open=True)

    def browse_source(self):
        path = filedialog.askopenfilename(title="Select Source File")
        if path:
            self.source_entry.delete(0, tk.END)
            self.source_entry.insert(0, path)

    def browse_target(self):
        path = filedialog.askdirectory(title="Select Target Directory")
        if path:
            self.target_entry.delete(0, tk.END)
            self.target_entry.insert(0, path)

    def create_symlink(self):
        source = self.source_entry.get()
        target = os.path.join(self.target_entry.get(), os.path.basename(source))

        try:
            os.symlink(source, target)
            messagebox.showinfo("Success", f"Symlink created:\n{target}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to create symlink:\n{e}")

if __name__ == "__main__":
    app = SymlinkCreator()
    app.mainloop()
