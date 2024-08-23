import tkinter as tk

class DataHandler:
    def __init__(self):
        self.list_data = []
        self.load_data()

    def load_data(self):
        '''Retrieve data from file and populate list_data'''
        try:
            with open("save.txt", "r", encoding="utf-8") as file:
                for f in file:
                    self.list_data.append(f.strip())
        except FileNotFoundError:
            pass

    def save_data(self):
        '''Save list_data to file'''
        with open("save.txt", "w", encoding="utf-8") as file:
            for d in self.list_data:
                file.write(d + "\n")


class Application(tk.Tk):
    def __init__(self, data_handler):
        super().__init__()
        self.title("List App")
        self.data_handler = data_handler

        # Create frames
        self.frame1 = ControlFrame(self, self.data_handler)
        self.frame1.pack(side="left")

        self.frame2 = DisplayFrame(self, self.data_handler)
        self.frame2.pack(side="left", fill="both", expand=1)

        self.frame2.populate_listbox()


class ControlFrame(tk.Frame):
    def __init__(self, parent, data_handler):
        super().__init__(parent)
        self.data_handler = data_handler

        # Add item button
        self.add_button = tk.Button(self, text="Add Item", command=self.add_item)
        self.add_button.pack()

        # Insert item button
        self.insert_button = tk.Button(self, text="Insert Item after", command=self.insert_item)
        self.insert_button.pack()

        # Delete button
        self.delete_button = tk.Button(self, text="Delete", command=self.delete_all)
        self.delete_button.pack()

        # Delete selected button
        self.delete_selected_button = tk.Button(self, text="Delete Selected", command=self.delete_selected)
        self.delete_selected_button.pack()

        # Save button
        self.save_button = tk.Button(self, text="Save", command=self.save_data)
        self.save_button.pack()

        # Quit button
        self.quit_button = tk.Button(self, text="Quit", command=self.quit_app)
        self.quit_button.pack()

    def add_item(self):
        content = self.master.frame2.content.get()
        if content:
            self.master.frame2.listbox.insert(tk.END, content)
            self.data_handler.list_data.append(content)
            self.master.frame2.content.set("")

    def insert_item(self):
        content = self.master.frame2.content.get()
        if content:
            try:
                pos = self.master.frame2.listbox.curselection()[0] + 1
                self.master.frame2.listbox.insert(pos, content)
                self.data_handler.list_data.insert(pos, content)
            except IndexError:
                self.master.frame2.listbox.insert(tk.END, content)
                self.data_handler.list_data.append(content)
            self.master.frame2.content.set("")

    def delete_all(self):
        self.master.frame2.listbox.delete(0, tk.END)
        self.data_handler.list_data.clear()

    def delete_selected(self):
        try:
            selected = self.master.frame2.listbox.get(self.master.frame2.listbox.curselection())
            self.master.frame2.listbox.delete(self.master.frame2.listbox.curselection())
            self.data_handler.list_data.remove(selected)
        except tk.TclError:
            pass

    def save_data(self):
        self.data_handler.save_data()

    def quit_app(self):
        self.save_data()
        self.master.destroy()


class DisplayFrame(tk.Frame):
    def __init__(self, parent, data_handler):
        super().__init__(parent)
        self.data_handler = data_handler

        # Entry field
        self.content = tk.StringVar()
        self.entry = tk.Entry(self, textvariable=self.content, bg="yellow")
        self.entry.pack(fill="both", expand=1)
        self.entry.focus()
        self.entry.bind("<Return>", self.add_item)

        # Listbox
        self.listbox = tk.Listbox(self)
        self.listbox.pack(fill="both", expand=1)

    def populate_listbox(self):
        for item in self.data_handler.list_data:
            self.listbox.insert(tk.END, item)

    def add_item(self, event):
        self.master.frame1.add_item()


if __name__ == "__main__":
    data_handler = DataHandler()
    app = Application(data_handler)
    app.mainloop()
