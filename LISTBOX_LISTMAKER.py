import tkinter as tk

class ListApp:
    def __init__(self, master):
        self.master = master
        self.list_data = []
        self.setup_ui()
        self.retrievedata()

    def setup_ui(self):
        # Configure the grid layout
        self.master.grid_rowconfigure(1, weight=1)
        self.master.grid_columnconfigure(0, weight=1)
        
        # Buttons
        self.add_button = tk.Button(self.master, text="Add Item", command=self.add_item)
        self.add_button.grid(row=0, column=0, sticky="ew")

        self.insert_button = tk.Button(self.master, text="Insert Item after", command=self.insert_item)
        self.insert_button.grid(row=0, column=1, sticky="ew")

        self.delete_button = tk.Button(self.master, text="Delete", command=self.delete_all)
        self.delete_button.grid(row=0, column=2, sticky="ew")

        self.delete_selected_button = tk.Button(self.master, text="Delete Selected", command=self.delete_selected)
        self.delete_selected_button.grid(row=0, column=3, sticky="ew")

        self.save_button = tk.Button(self.master, text="Save", command=lambda: self.quit(False))
        self.save_button.grid(row=0, column=4, sticky="ew")

        self.quit_button = tk.Button(self.master, text="Quit", command=self.quit)
        self.quit_button.grid(row=0, column=5, sticky="ew")

        # Entry for adding items
        self.content = tk.StringVar()
        self.entry = tk.Entry(self.master, textvariable=self.content, bg="yellow")
        self.entry.grid(row=1, column=0, columnspan=6, sticky="ew")
        self.entry.focus()
        self.entry.bind("<Return>", self.add_item)

        # Listbox
        self.listbox = tk.Listbox(self.master)
        self.listbox.grid(row=2, column=0, columnspan=6, sticky="nsew")

        # Configure grid to expand the listbox
        self.master.grid_rowconfigure(2, weight=1)

    def retrievedata(self):
        try:
            with open("save.txt", "r", encoding="utf-8") as file:
                for f in file:
                    self.listbox.insert(tk.END, f.strip())
                    self.list_data.append(f.strip())
        except Exception as e:
            print(f"Error loading data: {e}")

    def add_item(self, event=None):
        if self.content.get() != "":
            self.listbox.insert(tk.END, self.content.get())
            self.list_data.append(self.content.get())
            self.content.set("")

    def insert_item(self, event=None):
        if self.content.get() != "":
            try:
                pos = self.listbox.curselection()[0] + 1
                self.listbox.insert(pos, self.content.get())
                self.list_data.insert(pos, self.content.get())
            except IndexError:
                self.add_item()
            self.content.set("")

    def delete_all(self):
        self.listbox.delete(0, tk.END)
        self.list_data.clear()

    def delete_selected(self):
        try:
            index = self.listbox.curselection()[0]
            self.listbox.delete(index)
            self.list_data.pop(index)
        except IndexError:
            pass

    def quit(self, destroy=True):
        if not destroy:
            with open("saveLIST.txt", "w", encoding="utf-8") as file:
                for d in self.list_data:
                    file.write(d + "\n")
        else:
            self.master.destroy()

def main():
    root = tk.Tk()
    root.title("List App")
    app = ListApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()

