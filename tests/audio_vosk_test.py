import os
import queue
import sounddevice as sd
import vosk
import json

# Path to the Vosk model
model_path = "models/vosk-model-small-fr-0.22"

# Load Vosk model
if not os.path.exists(model_path):
    print("Model not found!")
    exit(1)

model = vosk.Model(model_path)

# Initialize a queue to store audio chunks
q = queue.Queue()

# Callback function to capture audio and store it in the queue
def callback(indata, frames, time, status):
    if status:
        print(status)
    q.put(bytes(indata))

# Function to transcribe audio in real time
def recognize():
    # Create Vosk recognizer with a sample rate of 16000 Hz
    recognizer = vosk.KaldiRecognizer(model, 16000)
    
    while True:
        # Get audio data from the queue
        data = q.get()
        
        # If the queue is empty, continue capturing audio
        if recognizer.AcceptWaveform(data):
            # Get the transcription result as JSON
            result = json.loads(recognizer.Result())
            print("Transcription:", result.get("text", ""))
        else:
            partial_result = json.loads(recognizer.PartialResult())
            print("Partial result:", partial_result.get("partial", ""))

# Set up the audio stream with a sample rate of 16000 Hz and 1 channel (mono)
stream = sd.RawInputStream(samplerate=16000, blocksize=8000, dtype='int16',
                           channels=1, callback=callback)

# Start the transcription in a separate thread
with stream:
    print("Listening... Press Ctrl+C to stop.")
    recognize()
