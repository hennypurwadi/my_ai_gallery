
import openai
import requests
import streamlit as st
from io import BytesIO

def generate_dalle_image(api_key, image_bytes, prompt, size=512):
    # Set OpenAI API key
    openai.api_key = api_key

    # Resize image
    if image_bytes is not None:
        image_data = BytesIO(image_bytes)
        response = requests.post(
            "https://api.openai.com/v1/images/generations",
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {api_key}",
            },
            json={
                "model": "image-alpha-001",
                "prompt": prompt,
                "num_images": 1,
                "size": size,
                "response_format": "url",
            },
            params={"n": 1},
        )
        response.raise_for_status()
        response_data = response.json()["data"][0]
        image_url = response_data["url"]

        # Download image
        response = requests.get(image_url)
        image_bytes = BytesIO(response.content).read()

    else:
        response = openai.Completion.create(
            engine="image-alpha-001",
            prompt=prompt,
            max_tokens=0,
            n=1,
            size=size,
            response_format="url"
        )
        image_url = response.choices[0].text.strip()
        response = requests.get(image_url)
        image_bytes = BytesIO(response.content).read()

    return image_bytes

def main():
    # Set page title and favicon
    st.set_page_config(page_title="DALL-E Image Generator", page_icon=":camera:")

    # Prompt user to enter API key
    api_key = st.text_input("Enter your OpenAI API key", type="password")

    # Set API key
    openai.api_key = api_key

    # Prompt user to upload image
    image_file = st.file_uploader("Upload an image file", type=["jpg", "jpeg", "png"])

    # Prompt user to enter prompt
    prompt = st.text_area("Enter a prompt to generate an image")

    # Generate image if either input is provided
    if image_file is not None or prompt:
        # Read image bytes
        if image_file is not None:
            image_bytes = image_file.read()
        else:
            image_bytes = None

        # Generate DALL-E image
        with st.spinner("Generating image..."):
            dalle_image = generate_dalle_image(api_key, image_bytes, prompt)

        # Display DALL-E image
        st.image(dalle_image, caption="Generated Image")

        # Allow user to download DALL-E image
        st.download_button(
            label="Download Image",
            data=dalle_image,
            file_name="generated_image.png",
            mime="image/png",
        )

if __name__ == "__main__":
    main()
