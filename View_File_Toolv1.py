import os
import pwd
import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog, ttk
from datetime import datetime
import stat
import json

BOOKMARK_FILE = "bookmarks.json"

class FileToolApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("File Tool Suite")
        self.geometry("1000x600")

        # Initialize attributes
        self.current_file_path = None
        self.bookmarks = self.load_bookmarks()

        # Path entry widget with variable and dynamic width update
        self.path_frame = tk.Frame(self)
        self.path_frame.grid(row=0, column=0, columnspan=3, sticky="ew", padx=5, pady=5)
        self.path_var = tk.StringVar()
        self.path_var.trace("w", self.update_path_entry_width)  # Trace to update width on path change
        self.path_entry = tk.Entry(self.path_frame, bd=8, bg="alice blue", textvariable=self.path_var, width=50)
        self.path_entry.grid(row=0, column=0, sticky="we")

        # Top frame for options
        self.frame_top = tk.Frame(self)
        self.frame_top.grid(row=1, column=0, columnspan=3, sticky="ew", padx=10, pady=10)

        self.btn_browse = tk.Button(self.frame_top, text="Select Directory", command=self.browse_directory)
        self.btn_browse.grid(row=0, column=0, padx=5)

        self.var_recursive = tk.BooleanVar()
        self.check_recursive = tk.Checkbutton(
            self.frame_top, text="Recursive View", variable=self.var_recursive, command=self.refresh_view
        )
        self.check_recursive.grid(row=0, column=1, padx=5)

        # Bookmark controls
        self.btn_add_bookmark = tk.Button(self.frame_top, text="Add Bookmark", command=self.add_bookmark)
        self.btn_add_bookmark.grid(row=0, column=2, padx=5)
        self.btn_save_bookmark = tk.Button(self.frame_top, text="Save Bookmark", command=self.save_bookmarks)
        self.btn_save_bookmark.grid(row=0, column=3, padx=5)
        self.btn_delete_bookmark = tk.Button(self.frame_top, text="Delete Bookmark", command=self.delete_bookmark)
        self.btn_delete_bookmark.grid(row=0, column=4, padx=5)

        self.bookmark_var = tk.StringVar(self)
        self.bookmark_menu = ttk.Combobox(self.frame_top, textvariable=self.bookmark_var, values=list(self.bookmarks.keys()))
        self.bookmark_menu.grid(row=0, column=5, padx=5)
        self.bookmark_menu.bind("<<ComboboxSelected>>", self.goto_bookmark)

        # Directory Treeview (Left Side)
        self.dir_tree = ttk.Treeview(self, columns=("size",), selectmode="browse")
        self.dir_tree.heading("#0", text="Directory Browser", anchor="w")
        self.dir_tree.heading("size", text="Size")
        self.dir_tree.column("size", width=100, anchor="e")
        self.dir_tree.grid(row=2, column=0, rowspan=2, sticky="nswe", padx=5, pady=5)

        # Scrollbar for Directory Treeview
        scroll_y_dir = ttk.Scrollbar(self, orient="vertical", command=self.dir_tree.yview)
        self.dir_tree.configure(yscroll=scroll_y_dir.set)
        scroll_y_dir.grid(row=2, column=1, sticky="ns")

        # File details Treeview (Right Side)
        columns = ("Name", "Size (KB)", "Permissions", "Date Created", "Date Modified", "Owner", "Type")
        self.file_tree = ttk.Treeview(self, columns=columns, show="headings")
        for col in columns:
            self.file_tree.heading(col, text=col, command=lambda _col=col: self.sort_column(_col, False))
            self.file_tree.column(col, width=120, anchor="w")
        self.file_tree.grid(row=2, column=2, sticky="nsew")

        # Scrollbar for File Treeview
        scroll_y_file = ttk.Scrollbar(self, orient="vertical", command=self.file_tree.yview)
        self.file_tree.configure(yscroll=scroll_y_file.set)
        scroll_y_file.grid(row=2, column=3, sticky="ns")

        # Right-click menu for toggling columns
        self.menu = tk.Menu(self, tearoff=0)
        for col in columns:
            self.menu.add_command(label=f"Toggle {col}", command=lambda _col=col: self.toggle_column(_col))
        self.file_tree.bind("<Button-3>", self.show_menu)

        # Configure grid to expand with window resizing
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)

        # Bind events
        self.dir_tree.bind("<<TreeviewOpen>>", self.on_dirview_open)
        self.dir_tree.bind("<<TreeviewSelect>>", self.on_dir_select)

    def update_path_entry_width(self, *args):
        """Update path entry widget width based on the length of the path."""
        text = self.path_entry.get()
        new_width = len(text) + 1  # Adding 1 for some padding
        self.path_entry.config(width=new_width)        
    def refresh_view(self):
        """Refreshes the view by calling browse_directory."""
        self.browse_directory()

    def load_bookmarks(self):
        """Load bookmarks from a JSON file."""
        try:
            with open(BOOKMARK_FILE, 'r') as file:
                return json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            return {}

    def save_bookmarks(self):
        """Save bookmarks to a JSON file."""
        with open(BOOKMARK_FILE, 'w') as file:
            json.dump(self.bookmarks, file, indent=4)

    def add_bookmark(self):
        """Add the current directory to bookmarks."""
        if not self.current_file_path:
            messagebox.showwarning("No Directory", "Select a directory first.")
            return

        dir_name = os.path.basename(self.current_file_path)
        bookmark_name = simpledialog.askstring("Bookmark Name", f"Enter a name for this bookmark ({dir_name}):")
        if bookmark_name:
            self.bookmarks[bookmark_name] = self.current_file_path
            self.bookmark_menu['values'] = list(self.bookmarks.keys())
            self.save_bookmarks()
            messagebox.showinfo("Bookmark Added", f"Bookmark '{bookmark_name}' added successfully.")

    def delete_bookmark(self):
        """Delete the selected bookmark."""
        selected_bookmark = self.bookmark_var.get()
        if not selected_bookmark:
            messagebox.showwarning("No Bookmark Selected", "Select a bookmark to delete.")
            return

        del self.bookmarks[selected_bookmark]
        self.bookmark_menu['values'] = list(self.bookmarks.keys())
        self.bookmark_var.set('')
        self.save_bookmarks()
        messagebox.showinfo("Bookmark Deleted", f"Bookmark '{selected_bookmark}' deleted successfully.")

    def goto_bookmark(self, event):
        selected_bookmark = self.bookmark_var.get()
        if selected_bookmark and selected_bookmark in self.bookmarks:
            self.load_directory_tree(self.bookmarks[selected_bookmark])
            self.path_var.set(self.bookmarks[selected_bookmark])
            self.update_path_entry_width()
    def browse_directory(self):
        directory = filedialog.askdirectory()
        if directory:
            self.current_file_path = directory
            self.load_directory_tree(directory)
            self.path_var.set(directory)
            self.update_path_entry_width()
    def load_directory_tree(self, directory):
        """Loads the directory tree into the Directory Treeview."""
        self.dir_tree.delete(*self.dir_tree.get_children())
        self.insert_node("", directory, directory)

    def insert_node(self, parent, path, text):
        node = self.dir_tree.insert(parent, "end", text=text, open=False, values=(self.get_folder_size(path),))
        if os.path.isdir(path):
            self.dir_tree.insert(node, "end", text="placeholder")  # Placeholder for expandable node

    def on_dirview_open(self, event):
        """Expands a directory node in the Directory Treeview."""
        node_id = self.dir_tree.focus()
        path = self.get_node_path(node_id)
        self.dir_tree.delete(*self.dir_tree.get_children(node_id))
        if os.path.isdir(path):
            try:
                for entry in os.scandir(path):
                    if entry.is_dir():
                        self.insert_node(node_id, entry.path, entry.name)
            except PermissionError:
                messagebox.showwarning("Permission Denied", f"Cannot access {path}")

    def on_dir_select(self, event):
        """Displays files in the File Treeview when a directory is selected in the Directory Treeview."""
        node_id = self.dir_tree.focus()
        path = self.get_node_path(node_id)
        if os.path.isdir(path):
            self.load_files(path)
            self.path_var.set(path)
            self.update_path_entry_width()

    def get_node_path(self, node_id):
        """Retrieves the full path for a given node ID."""
        node_path = self.dir_tree.item(node_id, "text")
        while self.dir_tree.parent(node_id):
            node_id = self.dir_tree.parent(node_id)
            node_path = os.path.join(self.dir_tree.item(node_id, "text"), node_path)
        return node_path

    def get_folder_size(self, path):
        """Calculates the total size of a folder."""
        total_size = 0
        for dirpath, _, filenames in os.walk(path):
            for f in filenames:
                try:
                    fp = os.path.join(dirpath, f)
                    total_size += os.path.getsize(fp)
                except (FileNotFoundError, PermissionError):
                    continue
        return f"{total_size / (1024 ** 2):.2f} MB" if total_size else ""

    def load_files(self, directory):
        """Lists files in the File Treeview with detailed information."""
        for item in self.file_tree.get_children():
            self.file_tree.delete(item)
        
        for file_name in os.listdir(directory):
            file_path = os.path.join(directory, file_name)
            if os.path.isfile(file_path):
                file_stat = os.stat(file_path)
                file_size = file_stat.st_size // 1024
                permissions = stat.filemode(file_stat.st_mode)
                date_created = datetime.fromtimestamp(file_stat.st_ctime).strftime('%Y-%m-%d %H:%M:%S')
                date_modified = datetime.fromtimestamp(file_stat.st_mtime).strftime('%Y-%m-%d %H:%M:%S')
                owner = pwd.getpwuid(file_stat.st_uid).pw_name
                file_type = os.path.splitext(file_name)[1] if os.path.splitext(file_name)[1] else "Unknown"

                self.file_tree.insert("", "end", values=(file_name, file_size, permissions, date_created, date_modified, owner, file_type))

    def sort_column(self, col, reverse):
        """Sorts the File Treeview column."""
        data_list = [(self.file_tree.set(k, col), k) for k in self.file_tree.get_children('')]
        data_list.sort(reverse=reverse)
        for index, (val, k) in enumerate(data_list):
            self.file_tree.move(k, '', index)
        self.file_tree.heading(col, command=lambda: self.sort_column(col, not reverse))

    def toggle_column(self, col):
        """Toggles the visibility of a File Treeview column."""
        if self.file_tree.heading(col, "text") == "":
            self.file_tree.heading(col, text=col)
            self.file_tree.column(col, width=120)
        else:
            self.file_tree.heading(col, text="")
            self.file_tree.column(col, width=0)

    def show_menu(self, event):
        """Shows the right-click menu for toggling columns."""
        self.menu.post(event.x_root, event.y_root)

if __name__ == "__main__":
    app = FileToolApp()
    app.mainloop()
