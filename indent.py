import tkinter as tk


def indent():
    selected_text = text_widget.get("sel.first", "sel.last")
    if selected_text:
        # Add four spaces to the beginning of each line
        indented_text = "\n".join(f"    {line}" for line in selected_text.split("\n"))
        text_widget.replace("sel.first", "sel.last", indented_text)


def dedent():
    selected_text = text_widget.get("sel.first", "sel.last")
    if selected_text:
        # Remove four spaces from the beginning of each line if present
        dedented_text = "\n".join(
            line[4:] if line.startswith("    ") else line
            for line in selected_text.split("\n")
        )
        text_widget.replace("sel.first", "sel.last", dedented_text)


def highlight():
    selected_text = text_widget.get("sel.first", "sel.last")
    if selected_text:
        text_widget.tag_add("highlight", "sel.first", "sel.last")


root = tk.Tk()

text_widget = tk.Text(root)
text_widget.pack()

indent_button = tk.Button(root, text="Indent", command=indent)
indent_button.pack()

dedent_button = tk.Button(root, text="Dedent", command=dedent)
dedent_button.pack()

highlight_button = tk.Button(root, text="Highlight", command=highlight)
highlight_button.pack()

# Create a tag to apply the highlighting
text_widget.tag_configure("highlight", background="yellow")

root.mainloop()
