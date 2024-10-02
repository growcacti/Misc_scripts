import tkinter as tk
from tkinter import filedialog, messagebox
import difflib

class FileDifferenceViewer:
    def __init__(self, root):
        self.root = root
        self.root.title("Side-by-Side File Difference Viewer")

        # Create a menu bar with a Help menu
        self.menu = tk.Menu(self.root)
        self.root.config(menu=self.menu)
        
        # Add Help menu with Color Guide
        help_menu = tk.Menu(self.menu, tearoff=0)
        self.menu.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="Color Guide", command=self.show_color_guide)

        # Add a label showing "V" at the top
        self.label = tk.Label(self.root, text="V", font=("Helvetica", 16))
        self.label.grid(row=0, column=0, columnspan=3)

        # Frame to hold text widgets and scrollbars
        self.text_frame = tk.Frame(self.root)
        self.text_frame.grid(row=1, column=0, columnspan=3)

        # Create two text widgets with scrollbars side by side
        self.text1 = tk.Text(self.text_frame, width=60, height=25)
        self.text2 = tk.Text(self.text_frame, width=60, height=25)

        self.scrollbar1 = tk.Scrollbar(self.text_frame, command=self.text1.yview)
        self.scrollbar2 = tk.Scrollbar(self.text_frame, command=self.text2.yview)

        self.text1.config(yscrollcommand=self.scrollbar1.set)
        self.text2.config(yscrollcommand=self.scrollbar2.set)

        self.text1.grid(row=0, column=0)
        self.scrollbar1.grid(row=0, column=1, sticky="ns")
        self.text2.grid(row=0, column=2)
        self.scrollbar2.grid(row=0, column=3, sticky="ns")

        # Checkbox for synchronized scrolling
        self.sync_scroll_var = tk.BooleanVar(value=False)
        self.sync_scroll_checkbox = tk.Checkbutton(
            self.root, text="Synchronized Scrolling", variable=self.sync_scroll_var, command=self.toggle_sync_scroll
        )
        self.sync_scroll_checkbox.grid(row=2, column=0, columnspan=3, pady=5)

        # Info label to display text statistics and cursor position
        self.info_label = tk.Label(self.root, text="Lines: 0  | Words: 0  | Characters: 0  | Cursor Position: Line 1, Column 0")
        self.info_label.grid(row=3, column=0, columnspan=3, pady=5)

        # Bind to text change and cursor movement events
        self.text1.bind("<KeyRelease>", self.update_info)
        self.text1.bind("<ButtonRelease-1>", self.update_info)
        self.text1.bind("<<Modified>>", self.on_text_modified)
        self.text1.bind("<ButtonRelease-2>", self.update_info)
        self.text1.bind("<MouseWheel>", self.scroll_both)

        self.text2.bind("<KeyRelease>", self.update_info)
        self.text2.bind("<ButtonRelease-1>", self.update_info)
        self.text2.bind("<<Modified>>", self.on_text_modified)
        self.text2.bind("<ButtonRelease-2>", self.update_info)
        self.text2.bind("<MouseWheel>", self.scroll_both)

        # Button to load files and show the difference
        self.load_button = tk.Button(self.root, text="Load Files and Show Difference", command=self.show_diff)
        self.load_button.grid(row=4, column=0, columnspan=3, pady=10)

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

        self.update_info()

    def on_text_modified(self, event):
        """Event triggered when text is modified to update the statistics."""
        if event.widget.edit_modified():
            self.update_info(event)
            event.widget.edit_modified(False)

    def update_info(self, event=None):
        """Update the info label with the current statistics and cursor position."""
        if event:
            text_widget = event.widget
        else:
            text_widget = self.text1

        # Get the current text content
        content = text_widget.get("1.0", "end-1c")

        # Count the lines, words, and characters
        lines = text_widget.index("end-1c").split(".")[0]
        words = len(content.split())
        characters = len(content)

        # Get the current cursor position (line and column)
        cursor_position = text_widget.index("insert")
        cursor_line, cursor_column = cursor_position.split(".")

        # Update the label with the new information
        self.info_label.config(
            text=f"Lines: {lines} | Words: {words} | Characters: {characters} | Cursor Position: Line {cursor_line}, Column {cursor_column}"
        )

    def toggle_sync_scroll(self):
        """Toggle synchronized scrolling based on the checkbox state."""
        if self.sync_scroll_var.get():
            self.text1.yview = self.scroll_both
            self.text2.yview = self.scroll_both
        else:
            self.text1.config(yscrollcommand=self.scrollbar1.set)
            self.text2.config(yscrollcommand=self.scrollbar2.set)

    def scroll_both(self, *args):
        """Scroll both text widgets together when synchronized scrolling is enabled."""
        if self.sync_scroll_var.get():
            self.text1.yview(*args)
            self.text2.yview(*args)

    def show_color_guide(self):
        """Show a pop-up with color explanations."""
        messagebox.showinfo(
            "Color Guide", 
            "Color Guide:\n\n"
            "Red: Deletions (lines in the first file but not in the second)\n"
            "Green: Additions (lines in the second file but not in the first)\n"
            "Yellow: Changes (modified lines present in both files)"
        )


# Main application setup
if __name__ == "__main__":
    root = tk.Tk()
    app = FileDifferenceViewer(root)
    root.mainloop()
