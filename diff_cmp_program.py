import tkinter as tk
from tkinter import filedialog
import difflib

def choose_file(entry):
    file_path = filedialog.askopenfilename()
    entry.delete(0, tk.END)
    entry.insert(0, file_path)

def cmp_files(path1, path2):
    try:
        with open(path1, 'rb') as f1, open(path2, 'rb') as f2:
            f1_content = f1.read()
            f2_content = f2.read()
            return f1_content == f2_content
    except Exception as e:
        return f"Error: {e}"

def diff_files(path1, path2):
    try:
        with open(path1, 'r') as f1, open(path2, 'r') as f2:
            f1_lines = f1.readlines()
            f2_lines = f2.readlines()
            diff = difflib.unified_diff(f1_lines, f2_lines, fromfile='File1', tofile='File2', lineterm='')
            return ''.join(diff)
    except Exception as e:
        return f"Error: {e}"

def perform_cmp():
    result = cmp_files(entry1.get(), entry2.get())
    result_text.delete(1.0, tk.END)
    result_text.insert(tk.END, "Files are identical." if result is True else "Files are different." if result is False else result)

def perform_diff():
    result = diff_files(entry1.get(), entry2.get())
    result_text.delete(1.0, tk.END)
    result_text.insert(tk.END, result if result else "No differences found.")

root = tk.Tk()
root.title("File Compare Tool")

frame = tk.Frame(root)
frame.pack(padx=10, pady=10)

entry1 = tk.Entry(frame, width=50)
entry1.pack(side=tk.TOP, padx=10, pady=5)
button1 = tk.Button(frame, text="Browse...", command=lambda: choose_file(entry1))
button1.pack(side=tk.TOP, pady=5)

entry2 = tk.Entry(frame, width=50)
entry2.pack(side=tk.TOP, padx=10, pady=5)
button2 = tk.Button(frame, text="Browse...", command=lambda: choose_file(entry2))
button2.pack(side=tk.TOP, pady=5)

cmp_button = tk.Button(frame, text="Compare Byte-by-Byte", command=perform_cmp)
cmp_button.pack(side=tk.LEFT, padx=10, pady=10)

diff_button = tk.Button(frame, text="Compare Line-by-Line", command=perform_diff)
diff_button.pack(side=tk.LEFT, padx=10, pady=10)

result_text = tk.Text(root, height=15, width=80)
result_text.pack(padx=10, pady=10)

root.mainloop()
