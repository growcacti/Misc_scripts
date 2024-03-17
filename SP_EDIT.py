import tkinter as tk

def delete_text():
    start_line = int(start_line_spinbox.get())
    start_char = int(start_char_spinbox.get())
    end_line = int(end_line_spinbox.get())
    end_char = int(end_char_spinbox.get())

    start = f"{start_line}.{start_char}"
    end = f"{end_line}.{end_char}"
    text_widget.delete(start, end)

# Create the main window
root = tk.Tk()
root.geometry("400x300")  # Adjusted size to fit SpinBoxes

# Create a Text widget
text_widget = tk.Text(root, height=10)
text_widget.pack(expand=True, fill='both', padx=10, pady=10)

# SpinBox for start line
start_line_spinbox = tk.Spinbox(root, from_=1, to=100, width=5)
start_line_spinbox.pack(side='left', padx=5, pady=5)

# SpinBox for start char
start_char_spinbox = tk.Spinbox(root, from_=0, to=100, width=5)
start_char_spinbox.pack(side='left', padx=5, pady=5)

# SpinBox for end line
end_line_spinbox = tk.Spinbox(root, from_=1, to=100, width=5)
end_line_spinbox.pack(side='left', padx=5, pady=5)

# SpinBox for end char
end_char_spinbox = tk.Spinbox(root, from_=0, to=100, width=5)
end_char_spinbox.pack(side='left', padx=5, pady=5)

# Button to trigger text deletion
delete_button = tk.Button(root, text="Delete Text", command=delete_text)
delete_button.pack(pady=10)

# Initialize the GUI loop
root.mainloop()
