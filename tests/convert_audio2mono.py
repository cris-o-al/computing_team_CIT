import librosa
import soundfile as sf

# Path to the stereo audio file
stereo_audio_path = "audios/harvard.wav"  # Update this to your file path

# Load the stereo audio
audio_data, sample_rate = librosa.load(stereo_audio_path, sr=None, mono=False)  # Set mono=False to retain both channels

# Check the shape of the audio data to verify it's stereo
print(f"Audio data shape: {audio_data.shape}")  # Should be (2, N) where N is the number of samples

# Extract one channel (e.g., the left channel)
mono_audio_data = audio_data[0]  # Extract the left channel (index 0); use [1] for the right channel

# Save the mono audio to a new file
mono_audio_path = "mono_audio_file.wav"
sf.write(mono_audio_path, mono_audio_data, sample_rate)

print(f"Mono audio saved to: {mono_audio_path}")
