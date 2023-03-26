
import streamlit as st
import openai
from pytube import YouTube
from io import BytesIO
from pydub import AudioSegment
import tempfile
import os

# Set API key as a secret
with open('api_key.txt', 'r') as f:
    api_key = f.read().strip()
openai.api_key = api_key    

# Convert mp4 to wav
def convert_to_wav(audio_data):
    audio = AudioSegment.from_file(audio_data, format='mp4')
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

st.title("YouTube Video Transcription")

# Get YouTube video URL from user input
video_url = st.text_input("Enter YouTube video URL:")

# Check if the input is a valid YouTube URL
if video_url.startswith("https://www.youtube.com/") or video_url.startswith("https://youtu.be/"):
    
    try:
        # Load the YouTube video
        youtube_video = YouTube(video_url)
        st.write(f"Video title: {youtube_video.title}")

        # Filter to get only audio streams and select the first one
        streams = youtube_video.streams.filter(only_audio=True)
        stream = streams.first()

        # Download the audio stream to memory
        audio_data = BytesIO()
        stream.stream_to_buffer(audio_data)
        audio_data.seek(0)

        # Transcribe the audio data
        with st.spinner("Transcribing YouTube video..."):
            transcript = transcribe_audio(audio_data)

        st.subheader("Transcription")
        st.write(transcript)

        # Create a download button for the transcription
        if st.button("Download Transcription"):
            st.download_button(
                "Download Transcription", data=transcript, file_name="transcription.txt"
            )
    except Exception as e:
        st.error(f"Error: {e}")
else:
    if video_url:
        st.error("Invalid YouTube URL. Please enter a valid URL.")
