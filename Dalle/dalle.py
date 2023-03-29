
import openai
import requests
import streamlit as st
from io import BytesIO

import streamlit as st

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

        # Set parameters for DALL-E API call
        params = {
            "model": "image-alpha-001",
            "prompt": prompt,
            "num_images": 1,
            "size": "256x256",
        }

        # Make API call to generate image
        response = openai.Image.create(**params)

        # Get image data from response
        image_data = response.content
        # Display image using Streamlit
        st.image(BytesIO(image_data), caption=f"Generated image for prompt: {prompt}", use_column_width=True)

if __name__ == "__main__":
    main()
