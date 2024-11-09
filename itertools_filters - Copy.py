import tkinter as tk
from tkinter import filedialog, messagebox
import itertools

# Function to open a file dialog and read the content of the selected file
def open_file():
    file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
    if not file_path:
        return
    with open(file_path, 'r') as file:
        content = file.read().splitlines()
    file_content.set(content)

# Function to apply the selected iterator to the file content
def apply_iterator():
    iterator_name = iterator_var.get()
    content = file_content.get()
    if not content:
        messagebox.showerror("Error", "No file content loaded")
        return

    # Convert content to a list of strings
    content_list = [line for line in content]

    try:
        if iterator_name == "accumulate":
            result = list(itertools.accumulate(map(int, content_list)))
        elif iterator_name == "chain":
            result = list(itertools.chain.from_iterable(content_list))
        elif iterator_name == "compress":
            selectors = [1 if i % 2 == 0 else 0 for i in range(len(content_list))]
            result = list(itertools.compress(content_list, selectors))
        elif iterator_name == "dropwhile":
            result = list(itertools.dropwhile(lambda x: len(x) < 5, content_list))
        elif iterator_name == "filterfalse":
            result = list(itertools.filterfalse(lambda x: len(x) < 5, content_list))
        elif iterator_name == "islice":
            result = list(itertools.islice(content_list, 2, None))
        elif iterator_name == "pairwise":
            result = list(itertools.pairwise(content_list))
        elif iterator_name == "takewhile":
            result = list(itertools.takewhile(lambda x: len(x) < 5, content_list))
        else:
            result = "Unknown iterator selected"
    except Exception as e:
        result = f"Error: {e}"

    result_var.set(result)

# Main GUI setup
root = tk.Tk()
root.title("Iterator Tool")

file_content = tk.Variable()
iterator_var = tk.StringVar(value="accumulate")
result_var = tk.Variable()

# GUI layout
tk.Label(root, text="Choose Iterator:").grid(row=0, column=0, padx=5, pady=5)
tk.OptionMenu(root, iterator_var, "accumulate", "chain", "compress", "dropwhile", "filterfalse", "islice", "pairwise", "takewhile").grid(row=0, column=1, padx=5, pady=5)

tk.Button(root, text="Open File", command=open_file).grid(row=1, column=0, padx=5, pady=5)
tk.Button(root, text="Apply Iterator", command=apply_iterator).grid(row=1, column=1, padx=5, pady=5)

tk.Label(root, text="File Content:").grid(row=2, column=0, padx=5, pady=5)
tk.Listbox(root, listvariable=file_content, height=10, width=50).grid(row=3, column=0, columnspan=2, padx=5, pady=5)

tk.Label(root, text="Result:").grid(row=4, column=0, padx=5, pady=5)
tk.Listbox(root, listvariable=result_var, height=10, width=50).grid(row=5, column=0, columnspan=2, padx=5, pady=5)

root.mainloop()
