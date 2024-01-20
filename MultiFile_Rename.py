import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os

class FileRenamerApp(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.create_widgets()

    def create_widgets(self):
        # Folder Selection
        self.folder_label = tk.Label(self, text="Select Folder:")
        self.folder_label.grid(row=0, column=0, sticky="w")
        self.folder_path = tk.StringVar(self)
        self.folder_entry = tk.Entry(self, textvariable=self.folder_path, width=50)
        self.folder_entry.grid(row=0, column=1)
        self.folder_button = tk.Button(self, text="Browse", command=self.select_folder)
        self.folder_button.grid(row=0, column=2)

        # Base Name Entry
        self.base_name_label = tk.Label(self, text="Enter Base Name:")
        self.base_name_label.grid(row=1, column=0, sticky="w")
        self.base_name = tk.StringVar(self, value="bg")
        self.base_name_entry = tk.Entry(self, textvariable=self.base_name, width=50)
        self.base_name_entry.grid(row=1, column=1)

        # File Extension Entry
        self.ext_label = tk.Label(self, text="Enter File Extension (e.g., png, txt):")
        self.ext_label.grid(row=2, column=0, sticky="w")
        self.file_ext = tk.StringVar(self, value="png")
        self.ext_entry = tk.Entry(self, textvariable=self.file_ext, width=50)
        self.ext_entry.grid(row=2, column=1)

        # Number Format Selection
        self.num_format_label = tk.Label(self, text="Number Format:")
        self.num_format_label.grid(row=3, column=0, sticky="w")
        self.num_format_options = ['Decimal', 'Hexadecimal']
        self.num_format = tk.StringVar(self, value=self.num_format_options[0])
        self.num_format_combobox = ttk.Combobox(self, textvariable=self.num_format, values=self.num_format_options, state='readonly')
        self.num_format_combobox.grid(row=3, column=1)

        # Preview Button
        self.preview_button = tk.Button(self, text="Preview Rename", command=self.generate_preview)
        self.preview_button.grid(row=4, column=0, columnspan=3)

        # ListBox for Preview
        self.preview_label = tk.Label(self, text="Preview of Renamed Files:")
        self.preview_label.grid(row=5, column=0, sticky="w")
        self.preview_listbox = tk.Listbox(self, width=50, height=10)
        self.preview_listbox.grid(row=5, column=1, columnspan=2)
        # Original File Names Label and ListBox
        self.original_files_label = tk.Label(self, text="Original File Names:")
        self.original_files_label.grid(row=7, column=0, sticky="w")
        self.original_files_listbox = tk.Listbox(self, width=50, height=10)
        self.original_files_listbox.grid(row=7, column=1, columnspan=2)

        # Rename Button
        self.rename_button = tk.Button(self, text="Rename Files", command=self.rename_files)
        self.rename_button.grid(row=6, column=0, columnspan=3)

 
    def select_folder(self):
        selected_folder = filedialog.askdirectory()
        if selected_folder:  # Check if a folder was selected
            self.folder_path.set(selected_folder)
            for filename in os.listdir(selected_folder):
                self.original_files_listbox.insert(tk.END, filename)



    def generate_preview(self):
        self.folder = self.folder_path.get()
        self.base = self.base_name.get()
        self.ext = self.file_ext.get().strip()
        if not self.ext.startswith('.'):
            self.ext = '.' + self.ext

        if not self.folder:
            messagebox.showinfo("Info", "Please select a folder first.")
            return

        self.preview_listbox.delete(0, tk.END)  # Clear existing items in preview
        self.original_files_listbox.delete(0, tk.END)  # Clear existing items in original files listbox
        i = 1
        for filename in os.listdir(self.folder):
            if filename.endswith(self.ext):
                number = f"{i:x}" if self.num_format.get() == 'Hexadecimal' else str(i)
                new_name = f"{self.base}{number}{self.ext}"
                self.preview_listbox.insert(tk.END, new_name)
                self.original_files_listbox.insert(tk.END, filename)
                i += 1



    def rename_files(self):
        self.folder = self.folder_path.get()
        base = self.base_name.get()
        self.ext = self.file_ext.get().strip()
        if not self.ext.startswith('.'):
            self.ext = '.' + self.ext

        if not self.folder:
            messagebox.showinfo("Info", "Please select a folder first.")
            return

        output_folder = os.path.join(self.folder, 'output')
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)

        # We need to get both the original and new names
        original_files = os.listdir(self.folder)
        i = 1
        renamed_files = 0
        for original_file in original_files:
            if original_file.endswith(self.ext):
                new_name = f"{base}{i}{self.ext}"
                src = os.path.join(self.folder, original_file)
                dst = os.path.join(output_folder, new_name)
                os.rename(src, dst)
                i += 1
                renamed_files += 1

        messagebox.showinfo("Success", f"Renamed {renamed_files} files to {output_folder}.")


if __name__ == "__main__":
    root = tk.Tk()
    notebook = ttk.Notebook(root)
    file_renamer_tab = FileRenamerApp(notebook)
    notebook.add(file_renamer_tab, text='File Renamer')
    notebook.pack(expand=True, fill='both')
    root.mainloop()
