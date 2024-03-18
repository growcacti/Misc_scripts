import tkinter as tk
import pickle

class TextEditor:
    def __init__(self, root):
        self.root = root
        self.text_widget = tk.Text(root,width =400, height=45)
        self.text_widget.pack(expand=True, fill='both')

        # Load stacks if they exist
        self.undo_stack, self.redo_stack = self.load_stacks()

        # Bind keypress event to capture text changes
        self.text_widget.bind('<Key>', self.capture_edit)
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

    def capture_edit(self, event):
        # Simplified edit capture logic
        key = event.char
        if key and event.keysym != "BackSpace":
            insert_point = self.text_widget.index("insert")
            self.undo_stack.append(('insert', insert_point, key))
        elif event.keysym == "BackSpace":
            insert_point = self.text_widget.index("insert")
            char_before_cursor = self.text_widget.get(insert_point + "-1c", insert_point)
            if char_before_cursor:
                self.undo_stack.append(('delete', insert_point, char_before_cursor))
    
    def undo(self):
        if self.undo_stack:
            action, position, char = self.undo_stack.pop()
            self.redo_stack.append((action, position, char))
            
            if action == 'insert':
                self.text_widget.delete(f"{position} -1c")
            elif action == 'delete':
                self.text_widget.insert(position, char)

    def redo(self):
        if self.redo_stack:
            action, position, char = self.redo_stack.pop()
            self.undo_stack.append((action, position, char))
            
            if action == 'delete':
                self.text_widget.delete(f"{position} -1c")
            elif action == 'insert':
                self.text_widget.insert(position, char)

    def on_close(self):
        # Save stacks to a file upon closing
        self.save_stacks(self.undo_stack, self.redo_stack)
        self.root.destroy()

    def save_stacks(self, undo_stack, redo_stack):
        with open('text_editor_stacks.pkl', 'wb') as file:
            pickle.dump((undo_stack, redo_stack), file)

    def load_stacks(self):
        try:
            with open('text_editor_stacks.pkl', 'rb') as file:
                return pickle.load(file)
        except (FileNotFoundError, EOFError):
            return [], []

if __name__ == "__main__":
    root = tk.Tk()
    editor = TextEditor(root)
    root.mainloop()
