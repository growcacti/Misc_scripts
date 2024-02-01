import os
import shutil
import tkinter as tk
from tkinter import filedialog

def select_directory(title):
    root = tk.Tk()
    root.withdraw()  # Hide the main window
    directory = filedialog.askdirectory(title=title)
    root.destroy()
    return directory

def gather_mp3_files(src_dir):
    mp3_files = []
    for root, dirs, files in os.walk(src_dir):
        for file in files:
            if file.endswith(".mp3"):
                full_path = os.path.join(root, file)
                mp3_files.append(full_path)
    return mp3_files

def copy_mp3_files(mp3_files, dest_dir):
    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)

    for file in mp3_files:
        shutil.copy(file, dest_dir)

if __name__ == "__main__":
    src_dir = select_directory("Select Source Directory for Searching MP3 Files")
    if src_dir:
        mp3_files = gather_mp3_files(src_dir)
        if mp3_files:
            dest_dir = select_directory("Select Destination Directory for MP3 Files")
            if dest_dir:
                copy_mp3_files(mp3_files, dest_dir)
                print(f"MP3 files have been copied successfully to {dest_dir}")
            else:
                print("No destination directory selected.")
        else:
            print("No MP3 files found in the selected source directory.")
    else:
        print("No source directory selected.")

pytesseract.pytesseract.tesseract_cmd = r'/usr/bin/tesseract'  # Adjust the path as per your Tesseract installation
