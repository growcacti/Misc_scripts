import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox

def select_source_file():
    file_path = filedialog.askopenfilename()
    source_file_entry.delete(0, tk.END)
    source_file_entry.insert(0, file_path)

def select_target_file():
    file_path = filedialog.asksaveasfilename(defaultextension=".txt")
    target_file_entry.delete(0, tk.END)
    target_file_entry.insert(0, file_path)

def indentation():
    indent_depth = 0
    src_file_name = source_file_entry.get()
    tar_file_name = target_file_entry.get()

    with open(src_file_name, 'r') as src_file, open(tar_file_name, 'w') as tar_file:
        data = src_file.readlines()

        for items in data:
            items = items.strip()

            if len(items) > 0:
                if items[0] == '#' and len(items) > 1:
                    if items[1] == '{':
                        spaces = ' '*4*indent_depth
                        items = spaces + items
                        tar_file.writelines(items + '\n')
                        indent_depth += 1
                        continue

                    if items[1] == '}':
                        indent_depth -= 1
                        spaces = ' '*4*indent_depth
                        items = spaces + items
                        tar_file.writelines(items + '\n')
                        continue

            spaces = ' '*4*indent_depth
            items = spaces + items
            tar_file.writelines(items + '\n')

    messagebox.showinfo("Success", "Indentation process completed.")

app = tk.Tk()
app.title("Indentation GUI")

tk.Label(app, text="Source file:").pack()
source_file_entry = tk.Entry(app)
source_file_entry.pack()
tk.Button(app, text="Browse...", command=select_source_file).pack()

tk.Label(app, text="Target file:").pack()
target_file_entry = tk.Entry(app)
target_file_entry.pack()
tk.Button(app, text="Browse...", command=select_target_file).pack()

tk.Button(app, text="Indent", command=indentation).pack()

app.mainloop()
