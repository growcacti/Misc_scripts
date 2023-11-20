import tkinter as tk
from tkinter.filedialog import askopenfilename, asksaveasfilename
import tkinter.scrolledtext as st
import importlib
import contextlib
import io
import pydoc

##def show_help():
##    textwidget.delete('1.0', tk.END)  # Clear the text widget
##    name = entry.get()
##
##    # Attempt to resolve the name to a Python object
##    try:
##        # If the name is something like 'tk.Frame', this line will resolve it
##        obj = eval(name)
##    except Exception as e:
##        # If resolving fails, display the error message in the text widget
##        textwidget.insert(tk.END, f"Error: {e}\n")
##        return
##
##    # Fetch and display the documentation for the resolved object
##    doc = pydoc.render_doc(obj)
##    textwidget.insert(tk.END, doc)
##
def clear():
    textwidget.delete('1.0', tk.END)  # Clear the text widget

def show_help():
    textwidget.delete('1.0', tk.END)  # Clear the text widget
    name = entry.get()

    # Attempt to dynamically import the module or get the object
    try:
        if '.' in name:
            module_name, attr_name = name.rsplit('.', 1)
            module = importlib.import_module(module_name)
            obj = getattr(module, attr_name)
        else:
            obj = importlib.import_module(name)
    except Exception as e:
        textwidget.insert(tk.END, f"Error: {e}\n")
        return

    # Capture the output of help()
    with contextlib.redirect_stdout(io.StringIO()) as f:
        help(obj)

    # Fetch and display the help information
    doc = f.getvalue()
    textwidget.insert(tk.END, doc)

    # Optionally display the dir() output
    textwidget.insert(tk.END, f"\nDirectory of {name}:\n{dir(obj)}\n")







def save_file():

    filepath = (
        asksaveasfilename(
            defaultextension="txt",
            filetypes=[("Text Files", "*.txt"), ("Python", "py"), ("All Files", "*.*")],
        ),
    )

    if not filepath:

        return

    with open(filepath, "w") as output_file:

        text = textwidget.get(1.0, tk.END)

        output_file.write(text)


# Main window
root = tk.Tk()
root.title("Python Documentation and Directory Viewer")

# Input for module/class name
entry = tk.Entry(root)
entry.grid(row=0,column=2)
textwidget = st.ScrolledText(root, wrap="word", bg="snow", height=40, width=80)
textwidget.grid(row=3, column=1, columnspan=7, rowspan=4)


# Button to fetch documentation
button = tk.Button(root, text="Show Help", command=show_help)
button.grid(row=1, column=1)
clr = tk.Button(root, text="clear", command=clear)
clr.grid(row=15, column=1)

# Text widget to display the documentation

save_btn = tk.Button(root, text="Save to File", command=save_file)
save_btn.grid(row=14, column=1)
# Start the application
root.mainloop()
