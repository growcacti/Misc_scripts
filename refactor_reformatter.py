import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from tkinter.scrolledtext import ScrolledText
import os
import csv
from datetime import datetime

class FileReformatter:
    def __init__(self, root):
        self.root = root
        self.setup_gui()

    def setup_gui(self):
        frame = tk.Frame(self.root, padx=20, pady=20)
        frame.grid(row=0, column=0)

        # Entry for number of keys
        tk.Label(frame, text="Number of Keys:").grid(row=0, column=0)
        self.num_keys_entry = tk.Entry(frame)
        self.num_keys_entry.grid(row=0, column=1)
        
        generate_button = tk.Button(frame, text="Generate Entry Widgets", command=self.generate_entries)
        generate_button.grid(row=0, column=2)

        # Dropdown for selecting delimiter
        tk.Label(frame, text="Select Delimiter:").grid(row=1, column=0)
        self.delimiter_var = tk.StringVar(value=':')
        self.delimiter_combo = ttk.Combobox(frame, textvariable=self.delimiter_var)
        self.delimiter_combo['values'] = (':', ' ', ',', ';')
        self.delimiter_combo.grid(row=1, column=1)

        # Combobox for selecting datetime format
        tk.Label(frame, text="Select DateTime Format:").grid(row=2, column=0)
        self.datetime_format_var = tk.StringVar(value='%a %m/%d/%y %H:%M:%S')
        self.datetime_format_combo = ttk.Combobox(frame, textvariable=self.datetime_format_var)
        self.datetime_format_combo['values'] = (
            '%a %m/%d/%y %H:%M:%S',
            '%Y-%m-%d %H:%M:%S',
            '%d/%m/%Y %H:%M:%S'
        )
        self.datetime_format_combo.grid(row=2, column=1)

        # Checkbutton to enable/disable datetime sorting
        self.sort_datetime_var = tk.BooleanVar(value=True)
        sort_datetime_checkbutton = tk.Checkbutton(frame, text="Sort by DateTime", variable=self.sort_datetime_var)
        sort_datetime_checkbutton.grid(row=2, column=2)

        self.entries_frame = tk.Frame(frame)
        self.entries_frame.grid(row=3, column=0, columnspan=3)

        process_button = tk.Button(frame, text="Select Directory and Process Files", command=self.process_files)
        process_button.grid(row=4, column=0, pady=10)

        help_button = tk.Button(frame, text="Help", command=self.help)
        help_button.grid(row=4, column=2)

        # Add Text widget to display results
        self.result_text = ScrolledText(frame, wrap='word', height=35, width=180, state='disabled')
        self.result_text.grid(row=5, column=0, columnspan=3)

    def generate_entries(self):
        # Clear previous entries if any
        for widget in self.entries_frame.winfo_children():
            widget.destroy()

        num_keys = int(self.num_keys_entry.get())
        
        self.entries = []
        
        for i in range(num_keys):
            tk.Label(self.entries_frame, text=f"Key {i+1}:").grid(row=i, column=0)
            entry = tk.Entry(self.entries_frame)
            entry.grid(row=i, column=1)
            self.entries.append(entry)

    def reformat_file(self, file_path):
        with open(file_path, 'r') as file:
            lines = file.readlines()

        data = []
        
        keys = [entry.get() for entry in self.entries]
        delimiter = self.delimiter_var.get()
        
        for line in lines:
            if delimiter in line:
                key, value = line.split(delimiter, 1)
                value = value.strip()
                if key in keys:
                    data.append(value)

        return data

    def process_files(self):
        directory = filedialog.askdirectory()
        if not directory:
            return

        all_data = []
        
        for root_directory_name, _, files_in_current_directory in os.walk(directory):
            for file_name in files_in_current_directory:
                if file_name.endswith(".txt"):  # Assuming we are processing .txt files
                    file_path = os.path.join(root_directory_name, file_name)
                    data = self.reformat_file(file_path)
                    all_data.append(data)
        
        if self.sort_datetime_var.get():
            try:
                all_data.sort(key=lambda x: datetime.strptime(x[2] + ' ' + x[3], self.datetime_format_var.get()))
            except Exception as e:
                messagebox.showerror("Error", f"DateTime sorting failed: {e}")

        output_file = os.path.join(directory, "output.csv")
        with open(output_file, 'w', newline='') as csvfile:
            csvwriter = csv.writer(csvfile)
            # Define headers based on keys
            headers = [entry.get() for entry in self.entries]
            csvwriter.writerow(headers)
            
            # Write the data rows
            for row in all_data:
                csvwriter.writerow(row)

        self.update_text_widget(all_data)

    def update_text_widget(self, data):
        self.result_text.config(state='normal')  # Enable editing in the Text widget
        self.result_text.delete(1.0, tk.END)     # Clear previous text

        # Add headers to the Text widget
        headers = [entry.get() for entry in self.entries]
        self.result_text.insert(tk.END, ', '.join(headers) + '\n')
        self.result_text.insert(tk.END, '-' * 100 + '\n')
        
        # Add data rows to the Text widget
        for row in data:
            self.result_text.insert(tk.END, ', '.join(row) + '\n')

        self.result_text.config(state='disabled')  # Disable editing again

    def help(self):
        help_info_str = """First thing is to select the number of Entrys,
    then fill the entries with the Key value  so  that it can search for the value of the keys.
    Check or Uncheck Date/Time.
    The format for the Date/Time is selectable with the combobox.
    When the button Select Directory and Process Files is pressed,
    the user selects a directory that contains multiple files.
    After that a CSV file is generated typically in the same folder as 
    the files that were parsed. Selected test headers from those test reports 
    are reformatted into a CSV file which can be opened in Excel. You have to 
    save it as xlsx to use Excel features. The original files are untouched 
    during this process."""
        messagebox.showinfo("Help", help_info_str)
       
if __name__=='__main__':
    root=tk.Tk()
    app = FileReformatter(root)
    root.mainloop()
