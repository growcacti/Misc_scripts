import tkinter as tk
from tkinter import filedialog, scrolledtext
import difflib



class FileComparerApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("File Comparer")
        self.geometry("500x800")

        # Buttons for selecting files
        self.btn_select_file1 = tk.Button(self, text="Select File 1", command=self.select_file1)
        self.btn_select_file1.grid(row=0, column=0, padx=10, pady=10)

        self.btn_select_file2 = tk.Button(self, text="Select File 2", command=self.select_file2)
        self.btn_select_file2.grid(row=1, column=0, padx=10, pady=10)
        self.btn_compare_files = tk.Button(self, text="Compare Files", command=self.compare_files)
        self.btn_compare_files.grid(row=10, column=0, columnspan=2, padx=10, pady=10)
        # Labels to display selected file paths
        self.lbl_file1_path = tk.Label(self, text="No File Selected")
        self.lbl_file1_path.grid(row=0, column=1, padx=10, pady=10)

        self.lbl_file2_path = tk.Label(self, text="No File Selected")
        self.lbl_file2_path.grid(row=1, column=1, padx=10, pady=10)

        # Text widget to display differences
        self.txt_differences = scrolledtext.ScrolledText(self, wrap=tk.WORD, height=10, width=60)
        self.txt_differences.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

        # Button to save differences
        self.btn_save_differences = tk.Button(self, text="Save Differences", command=self.save_differences)
        self.btn_save_differences.grid(row=3, column=0, columnspan=2, padx=10, pady=10)

    def select_file1(self):
        file_path = filedialog.askopenfilename()
        self.lbl_file1_path.config(text=file_path)


    def select_file2(self):
        file_path = filedialog.askopenfilename()
        self.lbl_file2_path.config(text=file_path)

    def save_differences(self):
        # Open save file dialog
        file_path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
        if file_path:
            # Write the contents of the Text widget to the file
            with open(file_path, "w") as file:
                file.write(self.txt_differences.get("1.0", tk.END))
    def compare_files(self):
        file1_path = self.lbl_file1_path.cget("text")
        file2_path = self.lbl_file2_path.cget("text")

        if file1_path != "No File Selected" and file2_path != "No File Selected":
            with open(file1_path, 'r') as file1, open(file2_path, 'r') as file2:
                file1_lines = file1.readlines()
                file2_lines = file2.readlines()

            # Implement the comparison logic
            self.compare_and_display(file1_lines, file2_lines)

    def compare_and_display(self, file1_lines, file2_lines):
        # Increase the number of context lines for better visibility
        context_lines = 3  # You can adjust this number as needed
        diff = list(difflib.unified_diff(file1_lines, file2_lines, lineterm='', n=context_lines))
        
        # Clear the Text widget before displaying new content
        self.txt_differences.delete('1.0', tk.END)

        if diff:
            # Enhanced formatting for readability
            for line in diff:
                # You can add more formatting here if needed
                self.txt_differences.insert(tk.END, line + '\n')
        else:
            # Display message if no differences are found
            self.txt_differences.insert(tk.END, "No differences found.")


if __name__ == "__main__":
    app = FileComparerApp()
    app.mainloop()
