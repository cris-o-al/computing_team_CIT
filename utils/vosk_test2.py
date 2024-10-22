import wave
import json
from vosk import Model, KaldiRecognizer
import time
from pydub import AudioSegment

############################ VARIABLES ############################

MODEL_PATH = "vosk-model-fr-0.6-linto-2.2.0"
AUDIO_FILE = "Audio_Leo.wav"

############################ LOAD FILES ############################

model = Model(MODEL_PATH)
audio = AudioSegment.from_file(AUDIO_FILE)

############################ PRE-PROCESS AUDIOS IF NEEDED ############################

#first_five_seconds = audio[:5000]
#first_five_seconds.export("first_5_seconds.wav", format="wav")
#AUDIO_FILE = "first_5_seconds.wav"


############################ START PROCESSING AUDIO ############################

start = time.time()


with wave.open(AUDIO_FILE, "rb") as wf:
    # Vosk only works with 16kHz wav
    if wf.getnchannels() != 1 or wf.getsampwidth() != 2 or wf.getframerate() != 16000:
        print("Audio file must be WAV format with 16kHz mono")
        exit(1)
    
    # KaldiRecognizer is a class used to process the speech to text based on the imported model
    recognizer = KaldiRecognizer(model, wf.getframerate())
    
    # Chunk the audio and transcribe
    transcript = []
    while True:
        data = wf.readframes(4000)  # Read 4000 frames (small chunk of audio)
        if len(data) == 0:
            break

        # If the recognizer accepts the waveform, append the result
        if recognizer.AcceptWaveform(data):
            result = json.loads(recognizer.Result())
            transcript.append(result['text'])
        else:
            # Get partial results (useful for live transcriptions)
            partial_result = json.loads(recognizer.PartialResult())
            #print("Partial transcript:", partial_result['partial'])

    # Get the final result after the loop ends
    final_result = json.loads(recognizer.FinalResult())
    transcript.append(final_result['text'])

    # Print the full transcript
    full_transcription = ' '.join(transcript)
    print("\nFull Transcription:\n", full_transcription)


    end =time.time()
    duration=end-start
    print(f"20 seconds of audio processed in {duration} seconds") 