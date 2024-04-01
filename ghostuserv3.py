import tkinter as tk
from tkinter import messagebox
import pyautogui as pag
import time
import sys

class Ghost:
    def __init__(self):
        self.counter=0
    def move_mouse_and_press_scroll_lock(self):
      
        """Moves the mouse slightly and presses Scroll Lock twice."""
        
        current_mouse_position = pag.position()
        pag.moveTo(current_mouse_position[0] + 5, current_mouse_position[1] + 5)
        pag.PAUSE = 10
        pag.moveTo(current_mouse_position[0], current_mouse_position[1])
        pag.PAUSE = 100
        pag.press('scrolllock')
        pag.PAUSE = 100
        pag.press('scrolllock')
        pag.PAUSE = 100
        pag.press('scrolllock')
        pag.PAUSE = 100
        # Schedule this function to be called again after 300 seconds without blocking the GUI
        root.after(30000, move_mouse_and_press_scroll_lock)  # 30000 milliseconds = 30 seconds
        self.counter =+ 1
        e2.insert(0, counter)
    # Adjust other parts of your code that rely on time.sleep() in a similar fashion.

    def runonce(self):
        
        self.move_mouse_and_press_scroll_lock()
        
        e2.insert(0, counter)
        
    def numoftimes(self):
        
         
        num = e1.get()
        
        
        if not num:
            messagebox.showinfo("Validation", "The input is empty. Please enter a number.")
            return
        
        
        try:
            numtimes = int(num)
        except ValueError:
            messagebox.showinfo("Validation", "Please enter a valid number.")
            return
        
        
        
        if numtimes <= 0:
            messagebox.showinfo("Validation", "Please enter a positive number.")
            return
        
        
        for i in range(numtimes):
           
            
            self.move_mouse_and_press_scroll_lock()
            self.counter += 1
            e2.insert(0, counter)
          

    def infinite_loops(self):
      

        while True:
             try:
                 pag.PAUSE =10
                 self.move_mouse_and_press_scroll_lock()
                 pag.PAUSE =10
                 self.counter += 1
                 e2.insert(0, counter)
              
               
             except KeyboardInterrupt:
                 messagebox.showinfo("Stopped By User")
                 print("\nProgram terminated by user.")
             except Exception as e:
                 print(f"Error: {e}")


    def on_keypress(self, event):
        if event.char == 'q':  # Pressing the 'q' key will quit the application
            sys.exit()

if __name__ == "__main__":

    root = tk.Tk()
    g=Ghost()
    root.bind('<KeyPress>', g.on_keypress)
    frame = tk.Frame(root, width=300, height=100)  # Adjusted size
    frame.grid(row=0, column=0)
    canvas = tk.Canvas(frame, bg="lavender", width=280, height=80)  # Adjusted size
    canvas.grid(row=0, column=0, columnspan=6)
    e1 = tk.Entry(canvas, bd=7, bg="seashell2")
    e1.grid(row=1, column=1)
    tk.Label(canvas,text="loops completed").grid(row=1,column=3)
    e2 = tk.Entry(canvas,bd=7,bg="mistyrose")
    e2.grid(row=1,column=4)
    
    b1 = tk.Button(canvas, bg="orange", bd=7, text="run once", command=g.move_mouse_and_press_scroll_lock)
    b1.grid(row=2, column=1)
    b2 = tk.Button(canvas, bg="alice blue", bd=7, text="run num of times", command=g.numoftimes)
    b2.grid(row=2, column=2)
    b3 = tk.Button(canvas, bg="sky blue", bd=7, text="exit", command=sys.exit)  # Fixed exit issue
    b3.grid(row=2, column=3)
    b4 = tk.Button(canvas, bg="thistle", bd=7, text="infinite", command=g.infinite_loops)
    b4.grid(row=2, column=4)
    root.mainloop()

