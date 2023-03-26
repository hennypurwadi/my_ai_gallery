
import streamlit as st
import openai
from pydub import AudioSegment
import tempfile
import os

# Set up the OpenAI API key
openai.api_key = 'your-openai-api-key'

# Convert mp4 to wav
def convert_to_wav(audio_file):
    audio = AudioSegment.from_file(audio_file, format='mp4')
    temp_file = tempfile.NamedTemporaryFile(delete=False)
    audio.export(temp_file.name, format="wav")
    return temp_file.name

# Transcribe the audio file using Whisper
def transcribe_audio(audio_file):
    wav_file = convert_to_wav(audio_file)
    with open(wav_file, "rb") as file:
        transcript = openai.Audio.transcribe("whisper-1", file)
    os.unlink(wav_file)
    return transcript['text']

# Streamlit app
st.title("Audio Transcription App")

uploaded_file = st.file_uploader("Upload your .mp4 audio file", type=['mp4'])

if uploaded_file:
    with st.spinner("Transcribing your audio file..."):
        transcript = transcribe_audio(uploaded_file)

    st.subheader("Transcription")
    st.write(transcript)

    # Download the transcription
    if st.button("Download Transcription"):
        st.download_button(
            "Download Transcription", data=transcript, file_name="transcription.txt"
        )
