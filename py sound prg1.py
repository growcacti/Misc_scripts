from moviepy.editor import VideoFileClip
from pydub import AudioSegment
from pydub.effects import normalize, compress_dynamic_range

# Load video and extract audio
video = VideoFileClip('your_movie.mp4')
audio = video.audio
audio.write_audiofile('extracted_audio.wav')

# Process audio using pydub
sound = AudioSegment.from_file('extracted_audio.wav')
normalized_sound = normalize(sound)
compressed_sound = compress_dynamic_range(normalized_sound)

# Export processed audio
compressed_sound.export('processed_audio.wav', format='wav')

# Combine processed audio with video
processed_video = video.set_audio('processed_audio.wav')
processed_video.write_videofile('final_movie.mp4')
