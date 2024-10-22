import librosa
import numpy as np

# Load the audio file
audio_path = 'audios/harvard.wav'  # Replace with your file path
audio_data, sample_rate = librosa.load(audio_path, sr=16000)

# Split the audio into 1-second chunks
frame_size = sample_rate * 1  # 1 second per frame

audio_frames = [audio_data[i:i+frame_size] for i in range(0, len(audio_data), frame_size)]

# Print the total number of frames
print(f"Total frames: {len(audio_frames)}")
