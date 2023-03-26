
import streamlit as st
import openai
from pytube import YouTube
from io import BytesIO
import tempfile
import os

# Set API key as a secret
with open('api_key.txt', 'r') as f:
    api_key = f.read().strip()
openai.api_key = api_key

# Transcribe the audio file using Whisper
def transcribe_audio(audio_file):
    audio_file.seek(0)
    transcript = openai.Audio.transcribe("whisper-1", audio_file)
    return transcript['text']

st.title("YouTube Video Transcription")

# Get YouTube video URL from user input
video_url = st.text_input("Enter YouTube video URL:")

# Check if the input is a valid YouTube URL
if video_url.startswith("https://www.youtube.com/") or video_url.startswith("https://youtu.be/"):
    try:
        yt = YouTube(video_url)
        video_title = yt.title
        st.subheader(f"Video title: {video_title}")

        stream = yt.streams.filter(only_audio=True).first()

        # Save the file with the video title
        st.write("Converting video to audio... Please wait.")
        temp_file_1 = tempfile.NamedTemporaryFile(delete=False, suffix=".mp4")
        stream.download(output_path=temp_file_1.name, filename=f"{video_title}.mp4")
        temp_file_1.close()

        # Download audio file
        st.download_button(
            label="Download Audio",
            data=open(temp_file_1.name, "rb"),
            file_name=f"{video_title}_audio.mp4",
            mime="audio/mp4",
        )

        # Clean up the temporary files
        os.unlink(temp_file_1.name)

    except Exception as e:
        st.error(f"Error: {e}")
        
else:
    st.warning("Please enter a valid YouTube URL.")
    st.subheader("Upload Audio and Transcribe")
    uploaded_audio = st.file_uploader("Upload the audio file:")

if uploaded_audio:
    try:
        # Transcribe the audio
        st.write("Transcribing audio... Please wait.")
        transcript = transcribe_audio(uploaded_audio)

        # Display the transcript
        st.subheader("Transcript:")
        st.write(transcript)

        # Download transcript as a text file
        st.download_button(
            label="Download Transcript",
            data=BytesIO(transcript.encode("utf-8")),
            file_name="transcript.txt",
            mime="text/plain",
        )

    except Exception as e:
        st.error(f"Error: {e}")
