import tkinter as tk
from tkinter import ttk, messagebox
import re
from collections import defaultdict, Counter

# Import all the string manipulation functions here
from string import ascii_lowercase, ascii_uppercase

# Example functions from the provided code
def get_word_pattern(word: str) -> str:
    word = word.upper()
    next_num = 0
    letter_nums = {}
    word_pattern = []
    for letter in word:
        if letter not in letter_nums:
            letter_nums[letter] = str(next_num)
            next_num += 1
        word_pattern.append(letter_nums[letter])
    return ".".join(word_pattern)

def reverse_words(input_str: str) -> str:
    return " ".join(input_str.split()[::-1])

def to_title_case(word: str) -> str:
    if "a" <= word[0] <= "z":
        word = chr(ord(word[0]) - 32) + word[1:]
    for i in range(1, len(word)):
        if "A" <= word[i] <= "Z":
            word = word[:i] + chr(ord(word[i]) + 32) + word[i + 1 :]
    return word

def remove_duplicates(sentence: str) -> str:
    return " ".join(sorted(set(sentence.split())))

def dna(dna_str: str) -> str:
    if len(re.findall("[ATCG]", dna_str)) != len(dna_str):
        raise ValueError("Invalid Strand")
    return dna_str.translate(dna_str.maketrans("ATCG", "TAGC"))

# Tkinter GUI application
class StringManipulationApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("String Manipulation App")
        self.geometry("600x400")
        
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(expand=True, fill="both")

        # Add tabs
        self.add_get_word_pattern_tab()
        self.add_reverse_words_tab()
        self.add_to_title_case_tab()
        self.add_remove_duplicates_tab()
        self.add_dna_tab()

    def add_get_word_pattern_tab(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Get Word Pattern")

        ttk.Label(tab, text="Enter word:").grid(row=0, column=0, padx=10, pady=10)
        self.gwp_entry = ttk.Entry(tab, width=30)
        self.gwp_entry.grid(row=0, column=1, padx=10, pady=10)

        self.gwp_result = ttk.Label(tab, text="")
        self.gwp_result.grid(row=1, column=0, columnspan=2, padx=10, pady=10)

        ttk.Button(tab, text="Get Pattern", command=self.get_word_pattern).grid(row=2, column=0, columnspan=2, pady=10)

    def get_word_pattern(self):
        word = self.gwp_entry.get()
        try:
            result = get_word_pattern(word)
            self.gwp_result.config(text=f"Pattern: {result}")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def add_reverse_words_tab(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Reverse Words")

        ttk.Label(tab, text="Enter sentence:").grid(row=0, column=0, padx=10, pady=10)
        self.rw_entry = ttk.Entry(tab, width=30)
        self.rw_entry.grid(row=0, column=1, padx=10, pady=10)

        self.rw_result = ttk.Label(tab, text="")
        self.rw_result.grid(row=1, column=0, columnspan=2, padx=10, pady=10)

        ttk.Button(tab, text="Reverse", command=self.reverse_words).grid(row=2, column=0, columnspan=2, pady=10)

    def reverse_words(self):
        sentence = self.rw_entry.get()
        try:
            result = reverse_words(sentence)
            self.rw_result.config(text=f"Reversed: {result}")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def add_to_title_case_tab(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="To Title Case")

        ttk.Label(tab, text="Enter word:").grid(row=0, column=0, padx=10, pady=10)
        self.ttc_entry = ttk.Entry(tab, width=30)
        self.ttc_entry.grid(row=0, column=1, padx=10, pady=10)

        self.ttc_result = ttk.Label(tab, text="")
        self.ttc_result.grid(row=1, column=0, columnspan=2, padx=10, pady=10)

        ttk.Button(tab, text="Convert", command=self.to_title_case).grid(row=2, column=0, columnspan=2, pady=10)

    def to_title_case(self):
        word = self.ttc_entry.get()
        try:
            result = to_title_case(word)
            self.ttc_result.config(text=f"Title Case: {result}")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def add_remove_duplicates_tab(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Remove Duplicates")

        ttk.Label(tab, text="Enter sentence:").grid(row=0, column=0, padx=10, pady=10)
        self.rd_entry = ttk.Entry(tab, width=30)
        self.rd_entry.grid(row=0, column=1, padx=10, pady=10)

        self.rd_result = ttk.Label(tab, text="")
        self.rd_result.grid(row=1, column=0, columnspan=2, padx=10, pady=10)

        ttk.Button(tab, text="Remove", command=self.remove_duplicates).grid(row=2, column=0, columnspan=2, pady=10)

    def remove_duplicates(self):
        sentence = self.rd_entry.get()
        try:
            result = remove_duplicates(sentence)
            self.rd_result.config(text=f"Without Duplicates: {result}")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def add_dna_tab(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="DNA")

        ttk.Label(tab, text="Enter DNA sequence:").grid(row=0, column=0, padx=10, pady=10)
        self.dna_entry = ttk.Entry(tab, width=30)
        self.dna_entry.grid(row=0, column=1, padx=10, pady=10)

        self.dna_result = ttk.Label(tab, text="")
        self.dna_result.grid(row=1, column=0, columnspan=2, padx=10, pady=10)

        ttk.Button(tab, text="Convert", command=self.dna).grid(row=2, column=0, columnspan=2, pady=10)

    def dna(self):
        dna_str = self.dna_entry.get()
        try:
            result = dna(dna_str)
            self.dna_result.config(text=f"Complementary DNA: {result}")
        except Exception as e:
            messagebox.showerror("Error", str(e))

if __name__ == "__main__":
    app = StringManipulationApp()
    app.mainloop()
