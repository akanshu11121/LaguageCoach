import streamlit as st
import requests
import time
import numpy as np
# import sounddevice as sd
from st_audiorec import st_audiorec
import io
from scipy.io.wavfile import write
import wave
import openai
from openai import OpenAI
client = OpenAI(api_key=st.secrets["API_KEY"])



def speech_to_text(file_path):
    audio_file= open(file_path, "rb")
    transcription = client.audio.transcriptions.create(
      model="whisper-1",
      file=audio_file
    )
    print("transcript:")
    print(transcription.text)
    return transcription.text



def describe_image(image_url):
    response = client.chat.completions.create(
      model="gpt-4o-mini", #"gpt-4o",
      messages=[
        {
          "role": "user",
          "content": [
            {"type": "text", "text": "describe this image like an IELTS exam"},
            {
              "type": "image_url",
              "image_url": {
                "url": image_url,
              },
            },
          ],
        }
      ],
      max_tokens=300,
    )
    print("Chat GPT:")
    print(response.choices[0].message.content)
    return response.choices[0].message.content



def compare_descriptions(model_desc, user_desc):
    st.write(f" Description: {model_desc}")
    st.write(f"Your Description: {user_desc}")
    completion = client.chat.completions.create(
      model="gpt-4o-mini", #"gpt-3.5-turbo",
      messages=[
      {"role": "system", "content": "You are a language teacher. you have a predefined description of an image, and also a user written dscription. you just have to judge the language, grammer and vocabolary of the user provided description. keep in mind that the user is a beginner so be supportive and helpful."},
      {"role": "user", "content": f"Description: {model_desc},user Description: {user_desc}. based on these two respond what all the user can improve in their description of the image "}
      ]
    )

    print(completion.choices[0].message.content)
    st.subheader('Feedback')
    st.write(f"Analysis: {completion.choices[0].message.content.strip()}")


def app():
    st.header('Image Comprehension')
    st.write('Learn to understand and describe images in your target language. This task focuses on improving your speaking skills and vocabulary.')

    if 'image_shown' not in st.session_state:
        st.session_state.image_shown = False
    if 'recording_started' not in st.session_state:
        st.session_state.recording_started = False

    # Start button to display the image
    if st.button('Start'):
        st.session_state.image_shown = True
        st.session_state.image_generated = False

    if st.session_state.image_shown:
        # Display the image
        print(st.session_state.image_generated)
        if st.session_state.image_generated == False:
            url = f"https://picsum.photos/1280/720"
            response = requests.get(url)
            image_url = response.url
            st.session_state.image_url=image_url
            st.session_state.image_generated = True
            print(st.session_state.image_generated)
        st.image(st.session_state.image_url, caption='Describe this image.')
        st.subheader('You have to describe and talk about what you see in the image. Take yur time look and analyse the image think about what you want to say and then start.\n You will have 30 seconds to speak about it. Focus on rich decription fluid speech.')

        st.session_state.recording = False
        st.session_state.audio_data = None
        
        if st.button('Start Talking'):
          
            st.session_state.recording = True
            st.session_state.audio_data = None
            st.write("Recording started. It will stop automatically after 30 seconds...")

            # Start the recording
            audio_data = st_audiorec()
      
            st.session_state.recording_started = True
            duration = 30  # seconds
            sample_rate = 44100  # Sample rate
            
            if st.button('Stop Recording'):
                st.session_state.recording = False
                
                
                # Wait for 30 seconds or until recording is finished
                # start_time = time.time()
                # while st.session_state.recording and (time.time() - start_time) < duration:
                #     time.sleep(0.1)  # Small sleep to prevent busy-waiting and allow Streamlit to update

                st.session_state.recording = False
                if audio_data:
                    st.session_state.audio_data = audio_data
                else:
                    st.write(f"Audio data: {audio_data}")
                    st.write("NO AUDIO DATA.")
                        
                # Handle recording completion
                if not st.session_state.recording and st.session_state.audio_data:
                    st.write("Recording complete!")
                    st.session_state.recording_started = False

                    # Save the audio data as a WAV file
                    output_file = "output2.wav"
                    with wave.open(output_file, 'wb') as wf:
                        wf.setnchannels(1)  # Mono
                        wf.setsampwidth(2)  # Sample width in bytes
                        wf.setframerate(sample_rate)  # Sample rate in Hz (default value)
                        wf.writeframes(st.session_state.audio_data)

                    st.audio(output_file)  # Display the audio player
                    st.success(f"Audio saved to {output_file}") 
                    
                    print(f"Audio saved to {output_file}")
                    user_description = speech_to_text("output2.wav")
                    model_description = describe_image(st.session_state.image_url)
                    compare_descriptions(model_description, user_description)
                else:
                    st.write("Audio not recorded.")