import tkinter as tk

# Function to update the color canvas and save the color to the listbox
def update_color():
    red = int(red_slider.get())
    green = int(green_slider.get())
    blue = int(blue_slider.get())
    
    color_canvas.config(bg=f'#{red:02X}{green:02X}{blue:02X}')
    
    # Display the color tuple
    color_output.config(text=f'Color: ({red}, {green}, {blue})')

def add_to_listbox():
    red = int(red_slider.get())
    green = int(green_slider.get())
    blue = int(blue_slider.get())
    
    color_listbox.insert(tk.END, f'({red}, {green}, {blue})')

# Create the main window
root = tk.Tk()
root.title("Color Picker")

# Create vertical sliders for red, green, and blue values
red_slider = tk.Scale(root, from_=0, to=255, orient=tk.VERTICAL)
green_slider = tk.Scale(root, from_=0, to=255, orient=tk.VERTICAL)
blue_slider = tk.Scale(root, from_=0, to=255, orient=tk.VERTICAL)

# Create a canvas to display the selected color
color_canvas = tk.Canvas(root, width=100, height=100, bg="white")

# Create a button to update the color and add it to the listbox
update_button = tk.Button(root, text="Update Color", command=update_color)
add_to_list_button = tk.Button(root, text="Send to Listbox", command=add_to_listbox)

# Create a label to display the color tuple
color_output = tk.Label(root, text="Color: (0, 0, 0)")

# Create a listbox to store selected colors
color_listbox = tk.Listbox(root)

# Arrange the widgets using grid layout
red_slider.grid(row=0, column=0, padx=10, pady=10)
green_slider.grid(row=0, column=1, padx=10, pady=10)
blue_slider.grid(row=0, column=2, padx=10, pady=10)
update_button.grid(row=1, column=0, padx=10, pady=10)
add_to_list_button.grid(row=1, column=1, padx=10, pady=10)
color_canvas.grid(row=2, column=0, rowspan=3, columnspan=3, padx=10, pady=10)
color_output.grid(row=5, column=0, columnspan=3, padx=10, pady=10)
color_listbox.grid(row=0, column=3, rowspan=6, padx=10, pady=10)

# Start the tkinter main loop
root.mainloop()
