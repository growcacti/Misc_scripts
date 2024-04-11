def create_new_directory():
    directory_path = filedialog.askdirectory()
    if directory_path:
        new_dir_name = simpledialog.askstring("New Folder", "Enter the name of the new folder:")
        if new_dir_name:
            new_path = os.path.join(directory_path, new_dir_name)
            try:
                os.makedirs(new_path)
                tk.messagebox.showinfo("Success", f"New directory created: {new_path}")
            except Exception as e:
                tk.messagebox.showerror("Error", str(e))

