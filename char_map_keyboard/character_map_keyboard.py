"""A small character map and text editor built with Python's standard library."""

import os
import unicodedata
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from tkinter.scrolledtext import ScrolledText


CHARACTERS = (
    ("Greek", "Alpha", "α"), ("Greek", "Beta", "β"),
    ("Greek", "Gamma", "γ"), ("Greek", "Delta", "δ"),
    ("Greek", "Theta", "θ"), ("Greek", "Lambda", "λ"),
    ("Greek", "Mu", "μ"), ("Greek", "Pi", "π"),
    ("Greek", "Sigma", "Σ"), ("Greek", "Omega", "ω"),
    ("Math", "Plus or minus", "±"), ("Math", "Minus or plus", "∓"),
    ("Math", "Multiplication", "×"), ("Math", "Division", "÷"),
    ("Math", "Square root", "√"), ("Math", "Infinity", "∞"),
    ("Math", "Summation", "∑"), ("Math", "Product", "∏"),
    ("Math", "Integral", "∫"), ("Math", "Partial derivative", "∂"),
    ("Math", "Not equal", "≠"), ("Math", "Approximately equal", "≈"),
    ("Math", "Less than or equal", "≤"), ("Math", "Greater than or equal", "≥"),
    ("Math", "Element of", "∈"), ("Math", "Subset", "⊂"),
    ("Math", "Superset", "⊃"), ("Math", "Intersection", "∩"),
    ("Math", "Union", "∪"), ("Math", "For all", "∀"),
    ("Math", "There exists", "∃"), ("Math", "Empty set", "∅"),
    ("Arrows", "Right arrow", "→"), ("Arrows", "Left arrow", "←"),
    ("Arrows", "Up arrow", "↑"), ("Arrows", "Down arrow", "↓"),
    ("Arrows", "Right double arrow", "⇒"), ("Arrows", "Left double arrow", "⇐"),
    ("Units and Currency", "Degree", "°"), ("Units and Currency", "Ohm", "Ω"),
    ("Units and Currency", "Micro sign", "µ"), ("Units and Currency", "Euro", "€"),
    ("Units and Currency", "Pound sterling", "£"), ("Units and Currency", "Yen", "¥"),
    ("Units and Currency", "Trademark", "™"), ("Units and Currency", "Copyright", "©"),
    ("Units and Currency", "Registered", "®"), ("Shapes", "Square", "□"),
    ("Shapes", "Circle", "○"), ("Shapes", "Triangle up", "△"),
    ("Shapes", "Triangle down", "▽"), ("Shapes", "Diamond", "◇"),
    ("Symbols", "Check mark", "✓"), ("Symbols", "Cross mark", "✗"),
    ("Symbols", "Heart", "♥"), ("Symbols", "Star", "★"),
    ("Symbols", "Smiley face", "☺"), ("Symbols", "Sun", "☀"),
    ("Symbols", "Umbrella", "☂"), ("Symbols", "Snowflake", "❄"),
    ("Symbols", "Music note", "♫"), ("Symbols", "Phone", "☎"),
    ("Symbols", "Peace", "☮"), ("Symbols", "Yin yang", "☯"),
    ("Symbols", "Female", "♀"), ("Symbols", "Male", "♂"),
)


class CharacterMapKeyboard(tk.Tk):
    """Display common Unicode characters and provide a simple writing area."""

    def __init__(self):
        super().__init__()
        self.current_file = None
        self.is_dirty = False
        self.selected_character = None
        self.recent = []
        self.search_var = tk.StringVar()
        self.category_var = tk.StringVar(value="All categories")
        self.status_var = tk.StringVar(value="Choose a character to insert it at the cursor.")

        self.title("Character Map Keyboard")
        self.geometry("1080x720")
        self.minsize(820, 560)
        self._build_menu()
        self._build_widgets()
        self._bind_shortcuts()
        self.protocol("WM_DELETE_WINDOW", self.exit_application)
        self.text.edit_modified(False)
        self.update_title()

    def _build_menu(self):
        menu = tk.Menu(self)
        file_menu = tk.Menu(menu, tearoff=False)
        file_menu.add_command(label="New", accelerator="Ctrl+N", command=self.new_file)
        file_menu.add_command(label="Open...", accelerator="Ctrl+O", command=self.open_file)
        file_menu.add_command(label="Save", accelerator="Ctrl+S", command=self.save_file)
        file_menu.add_command(label="Save As...", accelerator="Ctrl+Shift+S", command=self.save_file_as)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.exit_application)
        menu.add_cascade(label="File", menu=file_menu)

        edit_menu = tk.Menu(menu, tearoff=False)
        edit_menu.add_command(label="Undo", accelerator="Ctrl+Z", command=lambda: self.text.event_generate("<<Undo>>"))
        edit_menu.add_command(label="Redo", accelerator="Ctrl+Y", command=lambda: self.text.event_generate("<<Redo>>"))
        edit_menu.add_separator()
        edit_menu.add_command(label="Cut", accelerator="Ctrl+X", command=lambda: self.text.event_generate("<<Cut>>"))
        edit_menu.add_command(label="Copy", accelerator="Ctrl+C", command=lambda: self.text.event_generate("<<Copy>>"))
        edit_menu.add_command(label="Paste", accelerator="Ctrl+V", command=lambda: self.text.event_generate("<<Paste>>"))
        edit_menu.add_command(label="Select All", accelerator="Ctrl+A", command=self.select_all)
        menu.add_cascade(label="Edit", menu=edit_menu)
        self.configure(menu=menu)

    def _build_widgets(self):
        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)

        controls = ttk.Frame(self, padding=(10, 10, 10, 5))
        controls.grid(row=0, column=0, sticky="ew")
        controls.columnconfigure(1, weight=1)
        ttk.Label(controls, text="Search:").grid(row=0, column=0, sticky="w")
        search = ttk.Entry(controls, textvariable=self.search_var)
        search.grid(row=0, column=1, sticky="ew", padx=(5, 10))
        search.bind("<KeyRelease>", lambda event: self.refresh_character_grid())
        categories = ["All categories"] + sorted({category for category, _, _ in CHARACTERS})
        category_box = ttk.Combobox(controls, textvariable=self.category_var, values=categories, state="readonly", width=20)
        category_box.grid(row=0, column=2, padx=(0, 5))
        category_box.bind("<<ComboboxSelected>>", lambda event: self.refresh_character_grid())
        ttk.Button(controls, text="Clear search", command=self.clear_search).grid(row=0, column=3)

        main = ttk.PanedWindow(self, orient="horizontal")
        main.grid(row=1, column=0, sticky="nsew", padx=10, pady=5)

        map_frame = ttk.Labelframe(main, text="Character Map", padding=8)
        editor_frame = ttk.Labelframe(main, text="Document", padding=8)
        main.add(map_frame, weight=3)
        main.add(editor_frame, weight=4)

        map_frame.columnconfigure(0, weight=1)
        map_frame.rowconfigure(1, weight=1)
        ttk.Label(map_frame, text="Left-click inserts. Right-click copies to the clipboard.").grid(row=0, column=0, sticky="w", pady=(0, 5))
        self.map_canvas = tk.Canvas(map_frame, highlightthickness=0)
        scrollbar = ttk.Scrollbar(map_frame, orient="vertical", command=self.map_canvas.yview)
        self.map_canvas.configure(yscrollcommand=scrollbar.set)
        self.map_canvas.grid(row=1, column=0, sticky="nsew")
        scrollbar.grid(row=1, column=1, sticky="ns")
        self.character_grid = ttk.Frame(self.map_canvas)
        self.grid_window = self.map_canvas.create_window((0, 0), window=self.character_grid, anchor="nw")
        self.character_grid.bind("<Configure>", self._update_scroll_region)
        self.map_canvas.bind("<Configure>", self._resize_grid)

        recent_frame = ttk.Frame(map_frame)
        recent_frame.grid(row=2, column=0, columnspan=2, sticky="ew", pady=(8, 0))
        ttk.Label(recent_frame, text="Recent:").pack(side="left")
        self.recent_buttons = ttk.Frame(recent_frame)
        self.recent_buttons.pack(side="left", padx=(6, 0))

        editor_frame.columnconfigure(0, weight=1)
        editor_frame.rowconfigure(0, weight=1)
        self.text = ScrolledText(editor_frame, wrap="word", undo=True, font=("Segoe UI", 12))
        self.text.grid(row=0, column=0, sticky="nsew")
        self.text.bind("<<Modified>>", self.on_text_modified)
        actions = ttk.Frame(editor_frame)
        actions.grid(row=1, column=0, sticky="ew", pady=(8, 0))
        ttk.Button(actions, text="Copy Selected Character", command=self.copy_selected).pack(side="left")
        ttk.Button(actions, text="Clear Document", command=self.clear_document).pack(side="left", padx=5)
        ttk.Label(actions, text="Copied characters can be pasted into any application.").pack(side="right")

        ttk.Label(self, textvariable=self.status_var, anchor="w", relief="sunken", padding=(8, 3)).grid(
            row=2, column=0, sticky="ew")
        self.refresh_character_grid()

    def _bind_shortcuts(self):
        self.bind_all("<Control-n>", lambda event: self._run_shortcut(self.new_file))
        self.bind_all("<Control-o>", lambda event: self._run_shortcut(self.open_file))
        self.bind_all("<Control-s>", lambda event: self._run_shortcut(self.save_file))
        self.bind_all("<Control-Shift-S>", lambda event: self._run_shortcut(self.save_file_as))
        self.bind_all("<Control-a>", lambda event: self._run_shortcut(self.select_all))

    @staticmethod
    def _run_shortcut(command):
        command()
        return "break"

    def _update_scroll_region(self, event=None):
        self.map_canvas.configure(scrollregion=self.map_canvas.bbox("all"))

    def _resize_grid(self, event):
        self.map_canvas.itemconfigure(self.grid_window, width=event.width)

    def clear_search(self):
        self.search_var.set("")
        self.category_var.set("All categories")
        self.refresh_character_grid()

    def filtered_characters(self):
        query = self.search_var.get().strip().casefold()
        category = self.category_var.get()
        return [item for item in CHARACTERS if (category == "All categories" or item[0] == category)
                and (not query or query in item[1].casefold() or query in item[2])]

    def refresh_character_grid(self):
        for child in self.character_grid.winfo_children():
            child.destroy()
        characters = self.filtered_characters()
        if not characters:
            ttk.Label(self.character_grid, text="No matching characters.").grid(row=0, column=0, padx=8, pady=8)
            return
        for index, (_, name, character) in enumerate(characters):
            row, column = divmod(index, 5)
            button = tk.Button(self.character_grid, text=character, font=("Segoe UI Symbol", 19), width=4,
                               command=lambda char=character, label=name: self.insert_character(char, label))
            button.grid(row=row, column=column, padx=3, pady=3, sticky="nsew")
            button.bind("<Button-3>", lambda event, char=character, label=name: self.copy_character(char, label))
            button.bind("<Enter>", lambda event, char=character, label=name: self.show_character_info(char, label))
        for column in range(5):
            self.character_grid.columnconfigure(column, weight=1)
        self.after_idle(self._update_scroll_region)

    def show_character_info(self, character, label):
        self.status_var.set("{0}: U+{1:04X} ({2})".format(label, ord(character), unicodedata.name(character, "Unnamed character")))

    def insert_character(self, character, label):
        self.text.focus_set()
        self.text.insert("insert", character)
        self.selected_character = character
        self.add_recent(character, label)
        self.show_character_info(character, label)

    def copy_character(self, character, label):
        self.clipboard_clear()
        self.clipboard_append(character)
        self.selected_character = character
        self.add_recent(character, label)
        self.status_var.set("Copied {0} to the clipboard. Paste it into any application with Ctrl+V.".format(label))
        return "break"

    def copy_selected(self):
        if not self.selected_character:
            messagebox.showinfo("Copy Character", "Choose a character from the map first.")
            return
        label = unicodedata.name(self.selected_character, "character").title()
        self.copy_character(self.selected_character, label)

    def add_recent(self, character, label):
        self.recent = [(char, text) for char, text in self.recent if char != character]
        self.recent.insert(0, (character, label))
        self.recent = self.recent[:8]
        for child in self.recent_buttons.winfo_children():
            child.destroy()
        for character, label in self.recent:
            button = tk.Button(self.recent_buttons, text=character, font=("Segoe UI Symbol", 14), width=2,
                               command=lambda char=character, text=label: self.insert_character(char, text))
            button.pack(side="left", padx=2)
            button.bind("<Button-3>", lambda event, char=character, text=label: self.copy_character(char, text))

    def on_text_modified(self, event=None):
        if self.text.edit_modified():
            self.is_dirty = True
            self.update_title()
            self.text.edit_modified(False)

    def update_title(self):
        name = os.path.basename(self.current_file) if self.current_file else "Untitled"
        marker = "*" if self.is_dirty else ""
        self.title("{0}{1} - Character Map Keyboard".format(name, marker))

    def confirm_discard_changes(self):
        if not self.is_dirty:
            return True
        return messagebox.askyesno("Unsaved Changes", "Discard the unsaved changes?")

    def new_file(self):
        if not self.confirm_discard_changes():
            return
        self.text.delete("1.0", "end")
        self.text.edit_reset()
        self.text.edit_modified(False)
        self.is_dirty = False
        self.current_file = None
        self.update_title()
        self.text.focus_set()

    def open_file(self):
        if not self.confirm_discard_changes():
            return
        path = filedialog.askopenfilename(filetypes=[("Text documents", "*.txt"), ("All files", "*.*")])
        if not path:
            return
        try:
            with open(path, "r", encoding="utf-8") as source:
                content = source.read()
        except (OSError, UnicodeError) as error:
            messagebox.showerror("Open Failed", str(error))
            return
        self.text.delete("1.0", "end")
        self.text.insert("1.0", content)
        self.text.edit_reset()
        self.text.edit_modified(False)
        self.is_dirty = False
        self.current_file = path
        self.update_title()

    def save_file(self):
        if not self.current_file:
            return self.save_file_as()
        return self._write_file(self.current_file)

    def save_file_as(self):
        path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text documents", "*.txt"), ("All files", "*.*")])
        if path:
            return self._write_file(path)
        return False

    def _write_file(self, path):
        try:
            with open(path, "w", encoding="utf-8") as target:
                target.write(self.text.get("1.0", "end-1c"))
        except OSError as error:
            messagebox.showerror("Save Failed", str(error))
            return False
        self.current_file = path
        self.text.edit_modified(False)
        self.is_dirty = False
        self.update_title()
        self.status_var.set("Saved {0}".format(path))
        return True

    def clear_document(self):
        if self.text.get("1.0", "end-1c") and not messagebox.askyesno("Clear Document", "Clear all document text?"):
            return
        self.text.delete("1.0", "end")
        self.text.focus_set()

    def select_all(self):
        self.text.tag_add("sel", "1.0", "end-1c")
        self.text.mark_set("insert", "1.0")
        self.text.see("insert")

    def exit_application(self):
        if self.confirm_discard_changes():
            self.destroy()


if __name__ == "__main__":
    CharacterMapKeyboard().mainloop()
