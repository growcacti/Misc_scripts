from contextlib import contextmanager
from tkinter import messagebox

@contextmanager
def error_handler():
    try:
        yield
    except Exception as e:
        messagebox.showerror("Error", str(e))
        # Handle the exception as needed

# Example usage in your code:
with error_handler():
    # Some operations that might raise an exception
    raise ValueError("Something went wrong")
