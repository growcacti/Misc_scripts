import tkinter as tk

class DraggableRuler(tk.Toplevel):
    def __init__(self, root, orientation='horizontal'):
        super().__init__(root)
        self.orientation = orientation
        self.is_dragging = False
        
        # Set window properties
        self.overrideredirect(True)
        self.attributes('-topmost', True)
        
        # Create a canvas
        self.canvas = tk.Canvas(self, bg='white')
        self.canvas.pack(fill=tk.BOTH, expand=True)
        
        # Draw the ruler
        self.draw_ruler()
        
        # Bind mouse events
        self.canvas.bind('<Button-1>', self.start_drag)
        self.canvas.bind('<B1-Motion>', self.do_drag)
        self.canvas.bind('<ButtonRelease-1>', self.stop_drag)
        
    def draw_ruler(self):
        if self.orientation == 'horizontal':
            self.geometry('1800x40')  # Initial size
            for i in range(0, 1800, 10):
                if i % 100 == 0:
                    self.canvas.create_line(i, 0, i, 20, fill="black")
                    self.canvas.create_text(i, 30, text=str(i), fill="black")
                else:
                    self.canvas.create_line(i, 0, i, 10, fill="black")
        else:
            self.geometry('40x1000')  # Initial size
            for i in range(0, 1000, 10):
                if i % 100 == 0:
                    self.canvas.create_line(0, i, 20, i, fill="black")
                    self.canvas.create_text(30, i, text=str(i), fill="black")
                else:
                    self.canvas.create_line(0, i, 10, i, fill="black")
        
    def start_drag(self, event):
        self.is_dragging = True
        self._drag_start_x = event.x
        self._drag_start_y = event.y
        
    def do_drag(self, event):
        if self.is_dragging:
            x = self.winfo_x() + event.x - self._drag_start_x
            y = self.winfo_y() + event.y - self._drag_start_y
            self.geometry(f'+{x}+{y}')
        
    def stop_drag(self, event):
        self.is_dragging = False

if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()  # Hide the root window

    # Create horizontal and vertical rulers
    horizontal_ruler = DraggableRuler(root, 'horizontal')
    vertical_ruler = DraggableRuler(root, 'vertical')
    
    root.mainloop()
