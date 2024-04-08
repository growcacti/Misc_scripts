import functools
import tkinter as tk
from tkinter import messagebox

def handle_errors(func):
    @functools.wraps(func)
    def wrapper_handle_errors(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            messagebox.showerror("Error", str(e))
            # Log the error, or handle it as needed
    return wrapper_handle_errors

# Example usage:
class MyApplication:
    def __init__(self, root):
        self.root = root
        self.initialize_ui()

    @handle_errors
    def some_function_that_might_fail(self):
        # Your code that might raise an exception
        raise ValueError("An example error")

# In your GUI setup:
root = tk.Tk()
app = MyApplication(root)
root.mainloop()
