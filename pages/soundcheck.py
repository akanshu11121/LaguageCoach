import streamlit as st
from streamlit_audiorec import st_audiorec
import wave
import numpy as np
import io

# Streamlit app title
st.title("Audio Recorder")

# Audio recording widget
audio_data = st_audiorec()

if audio_data is not None:
    # Convert audio data to numpy array
    audio_array = np.frombuffer(audio_data, dtype=np.int16)
    
    # Save the audio data as a WAV file
    output_file = "output.wav"
    with wave.open(output_file, 'wb') as wf:
        wf.setnchannels(1)  # Mono
        wf.setsampwidth(2)  # Sample width in bytes
        wf.setframerate(44100)  # Sample rate in Hz
        wf.writeframes(audio_data)

    st.audio(output_file)  # Show the audio file in the Streamlit app
    st.success(f"Audio saved to {output_file}")


# # import sounddevice as sd
# import pyaudio
# import numpy as np
# import wave

# # # Parameters
# # duration = 10  # seconds
# # sample_rate = 44100  # Sample rate in Hz

# # # Record audio
# # print("Recording...")
# # audio_data = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=2, dtype='int16')
# # sd.wait()  # Wait until the recording is finished
# # print("Recording complete")

# # Parameters
# duration = 10  # seconds
# sample_rate = 44100  # Sample rate in Hz
# channels = 2  # Number of audio channels

# # Setup PyAudio
# p = pyaudio.PyAudio()

# # Open stream for recording
# stream = p.open(format=pyaudio.paInt16,
#                 channels=channels,
#                 rate=sample_rate,
#                 input=True,
#                 frames_per_buffer=1024)

# print("Recording...")

# frames = []
# for _ in range(0, int(sample_rate / 1024 * duration)):
#     data = stream.read(1024)
#     frames.append(data)

# print("Recording complete")

# # Stop and close the stream
# stream.stop_stream()
# stream.close()
# p.terminate()

# # Save as WAV file
# output_file = "output.wav"
# # with wave.open(output_file, 'w') as wf:
# #     wf.setnchannels(2)  # Stereo
# #     wf.setsampwidth(2)  # Sample width in bytes
# #     wf.setframerate(sample_rate)
# #     wf.writeframes(audio_data.tobytes())
# # Save the audio to a file
# with wave.open(output_file, 'wb') as wf:
#     wf.setnchannels(channels)
#     wf.setsampwidth(pyaudio.PyAudio().get_sample_size(pyaudio.paInt16))
#     wf.setframerate(sample_rate)
#     wf.writeframes(b''.join(frames))

# print(f"Audio saved to {output_file}")
