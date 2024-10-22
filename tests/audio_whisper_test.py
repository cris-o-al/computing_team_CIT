import whisper

# Load the Whisper model
model = whisper.load_model("tiny")  # You can choose "tiny", "base", "small", "medium", or "large"

# Load and transcribe audio
result = model.transcribe("audios/harvard.wav'")

# Print the transcription
print(result["text"])
