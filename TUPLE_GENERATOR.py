import tkinter as tk
from tkinter import ttk, filedialog
import random

def generate_random_tuples():
    n = int(num_tuples_entry.get())
    tuple_size = int(tuple_size_entry.get())
    start_range = int(start_range_entry.get())
    end_range = int(end_range_entry.get())

    result = [tuple(random.randint(start_range, end_range) for _ in range(tuple_size)) for _ in range(n)]
    result_text.set(str(result))
    return result

def save_to_file():
    tuples = generate_random_tuples()
    filename = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
    if filename:
        with open(filename, 'w') as f:
            for t in tuples:
                f.write(str(t) + "\n")

app = tk.Tk()
app.title("Random Tuple Generator")

frame = ttk.Frame(app, padding="10")
frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

# Number of tuples
ttk.Label(frame, text="Number of tuples:").grid(column=0, row=0, sticky=tk.W, pady=5)
num_tuples_entry = ttk.Entry(frame)
num_tuples_entry.grid(column=1, row=0, pady=5)
num_tuples_entry.insert(0, "5")

# Tuple size
ttk.Label(frame, text="Size of each tuple:").grid(column=0, row=1, sticky=tk.W, pady=5)
tuple_size_entry = ttk.Entry(frame)
tuple_size_entry.grid(column=1, row=1, pady=5)
tuple_size_entry.insert(0, "3")

# Range start
ttk.Label(frame, text="Start range:").grid(column=0, row=2, sticky=tk.W, pady=5)
start_range_entry = ttk.Entry(frame)
start_range_entry.grid(column=1, row=2, pady=5)
start_range_entry.insert(0, "1")

# Range end
ttk.Label(frame, text="End range:").grid(column=0, row=3, sticky=tk.W, pady=5)
end_range_entry = ttk.Entry(frame)
end_range_entry.grid(column=1, row=3, pady=5)
end_range_entry.insert(0, "10")

# Generate button
generate_btn = ttk.Button(frame, text="Generate", command=generate_random_tuples)
generate_btn.grid(column=0, row=4, columnspan=2, pady=10)

# Save to file button
save_btn = ttk.Button(frame, text="Save to File", command=save_to_file)
save_btn.grid(column=0, row=5, columnspan=2, pady=10)

# Result display
result_text = tk.StringVar()
result_label = ttk.Label(frame, textvariable=result_text)
result_label.grid(column=0, row=6, columnspan=2, pady=5)

app.mainloop()
