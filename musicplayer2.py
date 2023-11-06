import tkinter as tk
from tkinter import filedialog
import pygame

class MusicPlayer:
    def __init__(self, root):
        self.root = root
        self.root.title("Simple Music Player with Playlist")
        
        pygame.init()
        pygame.mixer.init()

        self.playlist = []
        self.track_index = 0

        self.status = tk.StringVar()
        self.current_track = tk.StringVar()

        # Create GUI components
        tk.Label(root, text="Playlist").grid(row=0, column=0)
        self.playlist_box = tk.Listbox(root)
        self.playlist_box.grid(row=1, column=0, rowspan=4, padx=5, pady=5)
        
        tk.Button(root, text="Load Tracks", command=self.load_tracks).grid(row=0, column=1, pady=5, padx=5)
        tk.Button(root, text="Play", command=self.play_song).grid(row=1, column=1, pady=5, padx=5)
        tk.Button(root, text="Pause", command=self.pause_song).grid(row=2, column=1, pady=5, padx=5)
        tk.Button(root, text="Stop", command=self.stop_song).grid(row=3, column=1, pady=5, padx=5)
        tk.Button(root, text="Next", command=self.next_song).grid(row=4, column=1, pady=5, padx=5)

        tk.Label(root, textvariable=self.current_track).grid(row=5, column=0, pady=5)
        tk.Label(root, textvariable=self.status).grid(row=5, column=1, pady=5)

    def load_tracks(self):
        files = filedialog.askopenfilenames(filetypes=[("Audio Files", "*.mp3 *.wav")])
        self.playlist.extend(files)
        for f in files:
            self.playlist_box.insert(tk.END, f.split("/")[-1])

    def play_song(self, event=None):
        track = self.playlist[self.track_index]
        pygame.mixer.music.load(track)
        pygame.mixer.music.play()
        self.status.set("Playing...")
        self.current_track.set(f"Current Track: {track.split('/')[-1]}")

    def pause_song(self):
        pygame.mixer.music.pause()
        self.status.set("Paused...")

    def stop_song(self):
        pygame.mixer.music.stop()
        self.status.set("Stopped.")

    def next_song(self):
        if self.track_index + 1 < len(self.playlist):
            self.track_index += 1
            self.play_song()
        else:
            self.stop_song()

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("500x200")
    MusicPlayer(root)
    root.mainloop()
