import tkinter as tk
from tkinter import filedialog
import pygame

class MusicPlayer:
    def __init__(self, root):
        self.root = root
        self.root.title("Simple Music Player")
        
        pygame.init()
        pygame.mixer.init()

        self.track = tk.StringVar()
        self.status = tk.StringVar()

        # Create GUI components
        tk.Label(root, text="Select your track:").grid(row=0, column=0)
        tk.Entry(root, textvariable=self.track, width=35).grid(row=0, column=1, pady=5)
        tk.Button(root, text="Browse", command=self.load).grid(row=0, column=2, pady=5)
        tk.Button(root, text="Play", command=self.play_song).grid(row=1, column=0, padx=10, pady=5)
        tk.Button(root, text="Pause", command=self.pause_song).grid(row=1, column=1, pady=5)
        tk.Button(root, text="Stop", command=self.stop_song).grid(row=1, column=2, padx=10, pady=5)
        tk.Label(root, textvariable=self.status).grid(row=2, column=1)

    def load(self):
        self.track.set(filedialog.askopenfilename(filetypes=[("Audio Files", "*.mp3 *.wav")]))

    def play_song(self):
        pygame.mixer.music.load(self.track.get())
        pygame.mixer.music.play()
        self.status.set("Playing...")

    def pause_song(self):
        pygame.mixer.music.pause()
        self.status.set("Paused...")

    def stop_song(self):
        pygame.mixer.music.stop()
        self.status.set("Stopped.")

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("400x150")
    MusicPlayer(root)
    root.mainloop()
