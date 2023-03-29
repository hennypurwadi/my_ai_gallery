
import openai
import requests
import streamlit as st
from io import BytesIO

import streamlit as st
import base64
from dish2image import Dish2Image

def main():
    # Set page title and favicon
    st.set_page_config(page_title="DALL-E Image Generator", page_icon=":camera:")

    # Prompt user to enter API key
    api_key = st.text_input("Enter your OpenAI API key", type="password")

    # Set API key
    openai.api_key = api_key

    # Prompt user to enter a DALL-E prompt
    prompt = st.text_input("Enter a DALL-E prompt")

    # Generate image based on prompt
    if prompt:
        dalle = Dish2Image(prompt)
        image = dalle.generate_image()

        # Display generated image
        st.image(image, use_column_width=True)

        # Allow user to download generated image
        b64 = base64.b64encode(image.read()).decode()
        href = f'<a href="data:application/octet-stream;base64,{b64}" download="{dalle.title}.jpg">Download generated image</a>'
        st.markdown(href, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
