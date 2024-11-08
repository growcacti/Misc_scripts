import tkinter as tk
from tkinter import filedialog
from pydub import AudioSegment, effects
import simpleaudio as sa

class DRCApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Dynamic Range Compression")
        
        self.file_path = None
        self.audio = None
        self.play_obj = None

        tk.Button(root, text="Load Audio", command=self.load_audio).grid(row=0, column=0)
        tk.Button(root, text="Apply DRC", command=self.apply_drc).grid(row=0, column=1)
        tk.Button(root, text="Play Audio", command=self.play_audio).grid(row=0, column=2)
        
        tk.Label(root, text="Threshold (dBFS)").grid(row=1, column=0)
        self.threshold_var = tk.DoubleVar(value=-20.0)
        tk.Entry(root, textvariable=self.threshold_var).grid(row=1, column=1)

        tk.Label(root, text="Ratio").grid(row=2, column=0)
        self.ratio_var = tk.DoubleVar(value=4.0)
        tk.Entry(root, textvariable=self.ratio_var).grid(row=2, column=1)

    def load_audio(self):
        file_path = filedialog.askopenfilename(filetypes=[("Audio Files", "*.mp3;*.wav")])
        if file_path:
            self.audio = AudioSegment.from_file(file_path)
            self.file_path = file_path

    def apply_drc(self):
        if self.audio:
            threshold = self.threshold_var.get()
            ratio = self.ratio_var.get()
            self.audio = effects.compress_dynamic_range(self.audio, threshold=threshold, ratio=ratio)
            print("DRC applied")

    def play_audio(self):
        if self.audio:
            play_obj = sa.play_buffer(
                self.audio.raw_data,
                num_channels=self.audio.channels,
                bytes_per_sample=self.audio.sample_width,
                sample_rate=self.audio.frame_rate
            )
            play_obj.wait_done()

if __name__ == "__main__":
    root = tk.Tk()
    app = DRCApp(root)
    root.mainloop()
