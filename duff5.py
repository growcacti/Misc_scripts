import tkinter as tk
from tkinter import filedialog
import difflib

class FileDifferenceViewer:
    def __init__(self, root):
        self.root = root
        self.root.title("Side-by-Side File Difference Viewer")

        # Add a label showing "V" at the top
        self.label = tk.Label(self.root, text="V", font=("Helvetica", 16))
        self.label.grid(row=0, column=0, columnspan=2)

        # Create two text widgets side by side
        self.text1 = tk.Text(self.root, width=60, height=25)
        self.text1.grid(row=1, column=0, padx=5, pady=5)

        self.text2 = tk.Text(self.root, width=60, height=25)
        self.text2.grid(row=1, column=1, padx=5, pady=5)

        # Create tags for different types of changes
        self.text1.tag_config("delete", background="red")  # Deletions in red
        self.text2.tag_config("add", background="green")   # Additions in green
        self.text1.tag_config("change", background="yellow")  # Changes in yellow (file1)
        self.text2.tag_config("change", background="yellow")  # Changes in yellow (file2)

        # Button to load files and show the difference
        self.load_button = tk.Button(self.root, text="Load Files and Show Difference", command=self.show_diff)
        self.load_button.grid(row=2, column=0, columnspan=2, pady=10)

    def load_file(self):
        """Open file dialog to select a file and return its content as a list of lines."""
        filepath = filedialog.askopenfilename()
        with open(filepath, 'r') as file:
            return file.readlines()

    def show_diff(self):
        """Clear the text widgets, load files, and show the differences with highlighted changes."""
        # Clear previous content
        self.text1.delete(1.0, tk.END)
        self.text2.delete(1.0, tk.END)

        # Load two files
        file1_lines = self.load_file()
        file2_lines = self.load_file()

        # Insert the lines into the text widgets
        self.text1.insert(tk.END, ''.join(file1_lines))
        self.text2.insert(tk.END, ''.join(file2_lines))

        # Calculate the differences using difflib
        diff = list(difflib.ndiff(file1_lines, file2_lines))

        # Variables to keep track of line numbers for text widgets
        line_num1, line_num2 = 1, 1

        for line in diff:
            if line.startswith('-'):
                # Line is present in the first file but not in the second (deletion)
                self.text1.tag_add("delete", f"{line_num1}.0", f"{line_num1}.end")
                line_num1 += 1
            elif line.startswith('+'):
                # Line is present in the second file but not in the first (addition)
                self.text2.tag_add("add", f"{line_num2}.0", f"{line_num2}.end")
                line_num2 += 1
            elif line.startswith(' '):
                # Line is the same in both files (no change)
                line_num1 += 1
                line_num2 += 1
            elif line.startswith('?'):
                # Line has been modified (change)
                self.text1.tag_add("change", f"{line_num1 - 1}.0", f"{line_num1 - 1}.end")
                self.text2.tag_add("change", f"{line_num2 - 1}.0", f"{line_num2 - 1}.end")


# Main application setup
if __name__ == "__main__":
    root = tk.Tk()
    app = FileDifferenceViewer(root)
    root.mainloop()
