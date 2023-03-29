
import openai
import streamlit as st
import pandas as pd
from PyPDF2 import PdfReader
import io

def load_pdf(file):
    pdf_reader = PdfReader(io.BytesIO(file.read()))
    num_pages = len(pdf_reader.pages)
    text = ""
    for page in range(num_pages):
        page_obj = pdf_reader.pages[page]
        text += page_obj.extract_text()
    return text

def load_csv(file):
    df = pd.read_csv(file)
    text = df.to_string()
    return text

def load_xlsx(file):
    df = pd.read_excel(file)
    text = df.to_string()
    return text

def main():
    # Prompt user to enter API key
    api_key = st.text_input("Enter your OpenAI API key got from https://platform.openai.com/account/api-keys", type="password")

    # Set API key
    openai.api_key = api_key
    
    # Prompt user to upload a file
    file = st.file_uploader("Upload a readable .pdf(NOT an image scanned Pdf), .csv, or .xlsx file", type=["pdf", "csv", "xlsx"])

    # Extract text if file is uploaded
    if file is not None:
        file_ext = file.name.split('.')[-1]
        
        if file_ext == "pdf":
            with st.spinner('Extracting text from PDF...'):
                text = load_pdf(file)
        elif file_ext == "csv":
            with st.spinner('Extracting text from CSV...'):
                text = load_csv(file)
        elif file_ext == "xlsx":
            with st.spinner('Extracting text from XLSX...'):
                text = load_xlsx(file)

        # Generate summary using OpenAI API
        prompt = f"Summarize this in 300 words {text}"        
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            temperature=0.0,
            max_tokens=1024,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )
        answer = response.choices[0].text.strip()

        # Display summary to user
        st.title("Summarizing Document")
        st.write("Here is a summary of the file content:")
        st.write(answer)

if __name__ == '__main__':
    main()
