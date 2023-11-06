import tkinter as tk

# Sample boilerplate code snippets
BOILERPLATE_CODE = {
    "if statement": "if condition: \n "+"    " ,
    "for loop": "for item in items: \n" +"    ",
    "function": "def my_function(arg1, arg2): \n" + "    ",
    "imports": "import tkinter as tk \n" + "    ",
}


def insert_snippet():
    selected_snippet = combo_var.get()
    snippet_code = BOILERPLATE_CODE.get(selected_snippet, "")
    text_widget.insert("insert", snippet_code)


# Create the main application
app = tk.Tk()
app.title("Auto Coder")

# Create a combo box to select snippets
combo_var = tk.StringVar(app)
combo_box = tk.OptionMenu(app, combo_var, *BOILERPLATE_CODE.keys())
combo_box.pack(pady=10)

# Create the text widget for code editing
text_widget = tk.Text(app, wrap="word", width=50, height=20)
text_widget.pack()

# Create the insert button
insert_button = tk.Button(app, text="Insert Snippet", command=insert_snippet)
insert_button.pack(pady=10)

app.mainloop()
