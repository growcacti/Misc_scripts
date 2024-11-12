import os
import tkinter as tk
from tkinter import filedialog, messagebox
from collections import Counter
from pathlib import Path

# Function to analyze text file and count word occurrences
def analyze_text_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
            words = content.split()
            return Counter(words)
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
        return Counter()

# Function to scan directory for text files and analyze them
def analyze_directory(directory_path, recursive=False):
    all_words_counter = Counter()
    for root, _, files in os.walk(directory_path):
        for filename in files:
            if filename.endswith('.txt'):
                file_path = os.path.join(root, filename)
                all_words_counter += analyze_text_file(file_path)
        if not recursive:
            break
    return all_words_counter

# Function to display word counts in a tkinter Listbox
def display_word_counts(word_counts):
    listbox.delete(0, tk.END)
    for word, count in word_counts.items():
        listbox.insert(tk.END, f"{word}: {count}")

# Function triggered by "Analyze" button
def analyze():
    path = filedialog.askdirectory() if directory_var.get() else filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
    if not path:
        return

    recursive = recursive_var.get()
    if directory_var.get():
        word_counts = analyze_directory(path, recursive=recursive)
    else:
        word_counts = analyze_text_file(path)

    display_word_counts(word_counts)

# Setting up tkinter GUI
root = tk.Tk()
root.title("Text File Word Occurrence Analyzer")

directory_var = tk.BooleanVar()
recursive_var = tk.BooleanVar()

frame = tk.Frame(root)
frame.pack(padx=10, pady=10)

# Directory or File Selection
tk.Checkbutton(frame, text="Analyze Directory", variable=directory_var).grid(row=0, column=0, sticky="w")
tk.Checkbutton(frame, text="Recursive Search (if Directory)", variable=recursive_var).grid(row=1, column=0, sticky="w")

analyze_button = tk.Button(frame, text="Analyze", command=analyze)
analyze_button.grid(row=2, column=0, pady=5)

# Listbox to show word occurrences
listbox = tk.Listbox(root, width=50, height=20)
listbox.pack(padx=10, pady=10)

root.mainloop()
