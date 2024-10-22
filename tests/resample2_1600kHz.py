import librosa
import soundfile as sf

# Path to the original audio file
original_audio_path = "audios/mono_audio_file.wav"  # Update this to your file path

# Load the audio file (it will resample to the target sample rate if specified)
target_sample_rate = 16000  # Desired sample rate (16 kHz)
audio_data, original_sample_rate = librosa.load(original_audio_path, sr=target_sample_rate)

# Print the original and new sample rate for verification
print(f"Original sample rate: {original_sample_rate}")
print(f"Resampled to: {target_sample_rate}")

# Save the resampled audio to a new file
resampled_audio_path = "audios/resampled_audio_file_16k.wav"
sf.write(resampled_audio_path, audio_data, target_sample_rate)

print(f"Resampled audio saved to: {resampled_audio_path}")
