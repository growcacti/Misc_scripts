import tkinter as tk

# Function to update the color canvas and output the color tuple
def update_color():
    red = int(red_spinbox.get())
    green = int(green_spinbox.get())
    blue = int(blue_spinbox.get())
    
    color_canvas.config(bg=f'#{red:02X}{green:02X}{blue:02X}')
    
    # Display the color tuple
    color_output.config(text=f'Color: ({red}, {green}, {blue})')

# Create the main window
root = tk.Tk()
root.title("Color Picker")

# Create Spinbox widgets for red, green, and blue values
red_spinbox = tk.Spinbox(root, from_=0, to=255)
green_spinbox = tk.Spinbox(root, from_=0, to=255)
blue_spinbox = tk.Spinbox(root, from_=0, to=255)

# Create a canvas to display the selected color
color_canvas = tk.Canvas(root, width=100, height=100, bg="white")

# Create a button to trigger color display
display_button = tk.Button(root, text="Display Color", command=update_color)

# Create a label to display the color tuple
color_output = tk.Label(root, text="Color: (0, 0, 0)")

# Arrange the widgets using grid layout
red_spinbox.grid(row=0, column=0, padx=10, pady=10)
green_spinbox.grid(row=0, column=1, padx=10, pady=10)
blue_spinbox.grid(row=0, column=2, padx=10, pady=10)
display_button.grid(row=1, column=0, columnspan=3, padx=10, pady=10)
color_canvas.grid(row=2, column=0, columnspan=3, padx=10, pady=10)
color_output.grid(row=3, column=0, columnspan=3)

# Start the tkinter main loop
root.mainloop()
