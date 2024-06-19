import tkinter as tk
from tkinter import ttk
import tkinter.filedialog as filedialog
import tkinter.messagebox as messagebox
import os

class FilemainrApp:
    def __init__(self, root):
        self.root = root
        self.root.title('File Tool')
        self.root.geometry('800x600')  # Adjust size as needed

        self.path = os.getcwd()
        self.output_folder = ''

        self.create_widgets()
        self.create_menu()

    def create_widgets(self):
        # Directory Tree Frame
        self.tree_frame = ttk.Frame(self.root)
        self.tree_frame.grid(row=0, column=0, padx=10, pady=5, sticky='nsew')
        self.pathdir = tk.Entry(self.tree_frame,width=50,bd=10,bg ='alice blue')
        self.pathdir.grid(row=0,column=0,padx=5, pady=5, sticky='ew')


        self.tree = ttk.Treeview(self.tree_frame, columns=('Directory Structure',), show='tree')
        self.tree.grid(row=1, column=0, sticky='nsew')

        self.tree_scroll = ttk.Scrollbar(self.tree_frame, orient='vertical', command=self.tree.yview)
        self.tree.config(yscrollcommand=self.tree_scroll.set)
        self.tree_scroll.grid(row=0, column=1, sticky='ns')

        # Original and Changed File List Frame
        self.list_frame = ttk.Frame(self.root)
        self.list_frame.grid(row=0, column=1, padx=10, pady=5, sticky='nsew')
        self.root.grid_columnconfigure(1, weight=1)

        # Original File List
        self.file_list_label = ttk.Label(self.list_frame, text='Filenames')
        self.file_list_label.grid(row=0, column=0, padx=5, pady=5)

        self.file_list = tk.Listbox(self.list_frame, width=50, height=20)
        self.file_list.grid(row=1, column=0, padx=5, pady=5, sticky='nsew')

        # Changed File List
        self.file_size_list_label = ttk.Label(self.list_frame, text='  ')
        self.file_size_list_label.grid(row=0, column=3, padx=5, pady=5)

        self.file_size = tk.Listbox(self.list_frame, width=50, height=20)
        self.file_size_list.grid(row=1, column=3, padx=5, pady=5, sticky='nsew')
        self.file_date = tk.Listbox(self.list_frame, width=50, height=20)
        self.file_date_list.grid(row=1, column=5, padx=5, pady=5, sticky='nsew')


        self.file_type = tk.Listbox(self.list_frame, width=50, height=20)
        self.file_type.grid(row=1, column=7, padx=5, pady=5, sticky='nsew')



        self.list_frame.grid_rowconfigure(1, weight=1)
        self.list_frame.grid_columnconfigure(0, weight=1)
        self.list_frame.grid_columnconfigure(1, weight=1)

        # main Options Frame
        self.main_frame = ttk.Frame(self.root)
        self.main_frame.grid(row=1, column=0, columnspan=2, padx=10, pady=5, sticky='ew')

      
        tk.Label(self.main_frame, text='  ').grid(row=1, column=0, padx=5, pady=5)
        tk.Button(self.main_frame, text='  ').grid(row=2, column=0, columnspan=2, padx=5, pady=5, sticky='ew')

        self.main_frame.grid_columnconfigure(1, weight=1)

    def create_menu(self):
        self.menu_bar = tk.Menu(self.root)
        self.root.config(menu=self.menu_bar)

        self.file_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.file_menu.add_command(label='Select Directory', command=self.select_directory)
        self.menu_bar.add_cascade(label='File', menu=self.file_menu)

    def select_directory(self):
        self.pathdir.delete(0, tk.END)
        self.path = filedialog.askdirectory()
        if self.path:
            self.pathdir.insert(self.path)
            self.populate_treeview(self.path)
            for file in os.scandir(self.path):
                if file.is_file:
                    self.file_list.insert(tk.END, file)

    def populate_treeview(self, root_path):
        self.tree.delete(*self.tree.get_children())  # Clear existing items in the Treeview
        for entry in os.scandir(root_path):
            if entry.is_dir():
                self.tree.insert('', 'end', entry.path, text=entry.name)

    def weview_main(self):
        selected_item = self.tree.selection()
        if selected_item:
            selected_dir = self.tree.item(selected_item, 'text')
            self.path = os.path.join(self.path, selected_dir)
            self.file_list.delete(0, tk.END)
           
            try:
                for file in os.listdir(self.path):
                    self.file_list.insert(tk.END, file)
                    base_name, ext = os.path.splitext(file)
                    
            except Exception as e:
                messagebox.showerror('Error', f'Failed to read directory contents: {e}')

if __name__ == '__main__':
    root = tk.Tk()
    app = FilemainrApp(root)
    root.mainloop()
