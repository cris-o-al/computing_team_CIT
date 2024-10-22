import os
import wave
import json
import vosk

# Path to Vosk model and audio file
model_path = "models/vosk-model-small-en-us-0.15"
audio_path = "audios/resampled_audio_file_16k.wav"  # Update this to the path of your .wav file

# Load Vosk model
if not os.path.exists(model_path):
    print("Model not found!")
    exit(1)
    

model = vosk.Model(model_path)

# Function to read and process audio frames
def transcribe_wav_file(wav_file):
    wf = wave.open(wav_file, "rb")
    
    # Ensure the audio has the correct format
    if wf.getnchannels() != 1:
        print("Error: Audio file must be mono.")
        exit(1)
    
    if wf.getframerate() != 16000:
        print("Error: Audio file must have a sample rate of 16000.")
        exit(1)
    
    # Initialize the Vosk recognizer
    recognizer = vosk.KaldiRecognizer(model, wf.getframerate())

    # Process the audio file in chunks (frames)
    results = []
    while True:
        data = wf.readframes(4000)  # Read 4000 frames (small chunks for processing)
        if len(data) == 0:
            break  # End of file

        if recognizer.AcceptWaveform(data):
            # Get full result and append it to the list
            result = json.loads(recognizer.Result())
            results.append(result.get("text", ""))
        else:
            # Handle partial result (not fully recognized yet)
            partial_result = json.loads(recognizer.PartialResult())
            print("Partial result:", partial_result.get("partial", ""))

    # Process final result (in case there's anything left)
    final_result = json.loads(recognizer.FinalResult())
    results.append(final_result.get("text", ""))

    # Join and print the complete transcription
    complete_transcription = " ".join(results)
    print("\nTranscription:", complete_transcription)

# Call the function to transcribe the audio file
transcribe_wav_file(audio_path)
