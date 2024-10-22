import tensorflow as tf
import numpy as np
import librosa

# Load the TensorFlow Lite model
interpreter = tf.lite.Interpreter(model_path="1.tflite")
interpreter.allocate_tensors()

# Get input and output tensors
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

# Load the audio file
audio_path = 'audios/harvard.wav'  # Replace with your file path
audio_data, sample_rate = librosa.load(audio_path, sr=16000)

# Split the audio into 1-second chunks
frame_size = sample_rate * 1  # 1 second per frame
audio_frames = [audio_data[i:i+frame_size] for i in range(0, len(audio_data), frame_size)]

# Preprocess: Normalize the audio between -1 and 1
audio_frames = [frame / np.max(np.abs(frame)) for frame in audio_frames]

# Run inference on each frame
for frame in audio_frames:
    frame = np.expand_dims(frame, axis=0)  # Reshape to match model input shape

    # Set the input tensor
    interpreter.set_tensor(input_details[0]['index'], frame)

    # Run the model
    interpreter.invoke()

    # Get the output transcription
    transcription = interpreter.get_tensor(output_details[0]['index'])

    print("Transcription: ", transcription)
