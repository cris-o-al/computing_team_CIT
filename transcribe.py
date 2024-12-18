import wave
import json
import os
from vosk import Model, KaldiRecognizer
import time
from pydub import AudioSegment
from pydub import AudioSegment
from deep_translator import GoogleTranslator
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from datetime import datetime

############################ Connect to MongoDB ##################

uri = "mongodb+srv://admin:CIT_admin0@citcluster0.mhrd1.mongodb.net/?retryWrites=true&w=majority&appName=CITcluster0"

# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))
database_name="CITcluster0"
collection_name="Collection_1"
db = client[database_name]
collection = db[collection_name]
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)
    
    
##TODO : Make it so every 1 second of transcription, the data is being sent
##to MongoDB with title and timestamp

############################ VARIABLES ############################

MODEL_PATH = "models/vosk-model-small-fr-0.22"
AUDIO_FILE = "data/liberte_audio.mp3"
OUTPUT_FILE="transcript/liberte_audio.txt"
output_directory = os.path.dirname(OUTPUT_FILE)
if not os.path.exists(output_directory):
    os.makedirs(output_directory)
# Load the audio file
audio = AudioSegment.from_file(AUDIO_FILE)

# Convert audio to mono and set the sample rate to 16 kHz
audio = audio.set_channels(1).set_frame_rate(16000)

# Export the audio to a WAV file
audio.export("converted_audio.wav", format="wav")

# Now use the "converted_audio.wav" file for processing
AUDIO_FILE = "converted_audio.wav"

############################ LOAD FILES ############################

model = Model(MODEL_PATH)

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
        data = wf.readframes(10000)  # Read 4000 frames (small chunk of audio)
        if len(data) == 0:
            break

        # If the recognizer accepts the waveform, append the result
        if recognizer.AcceptWaveform(data):
            result = json.loads(recognizer.Result())
            transcript.append(result['text'])
        else:
            # Get partial results (useful for live transcriptions)
            partial_result = json.loads(recognizer.PartialResult())
            if(partial_result):
                    data_to_send= {
                            "title": "test1",
                            "content": partial_result,
                            "timestamp": datetime.now()
                    }
                    collection.insert_one(data_to_send)
                    print("data sent")
            #print("Partial transcript:", partial_result['partial'])

    # Get the final result after the loop ends
    final_result = json.loads(recognizer.FinalResult())
    transcript.append(final_result['text'])

    # Print the full transcript
    full_transcription = ' '.join(transcript)
    print("\nFull Transcription:\n", full_transcription)
    translated = GoogleTranslator(source='auto', target='english').translate(full_transcription) 
    print("\nFull Translated Transcription:\n", translated)
    # Save the full transcript to a text file
    with open(OUTPUT_FILE, "w") as f:
        f.write(full_transcription)

    end =time.time()
    duration=end-start
    print(f"20 seconds of audio processed in {duration} seconds")
    print(f"Transcript saved to {f}")