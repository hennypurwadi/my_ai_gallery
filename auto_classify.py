
import openai
import streamlit as st
import pandas as pd
import io
from PyPDF2 import PdfReader
import openpyxl
import base64

# Loading functions
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

# Text cleaning function
def clean_text(text):
    tokens = text.split()
    return ' '.join(tokens)

# Classification function
def classify_label(text, prompt):
    prompt = prompt.replace('cleaned_text', text)
    classification = request_completion(prompt)['choices'][0]['text'].replace('\n', '')
    return classification.lower()

# API request function
def request_completion(prompt):
    completion_response = openai.Completion.create(
        prompt=prompt,
        temperature=0,
        max_tokens=5,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
        model=COMPLETIONS_MODEL
    )
    return completion_response

# Download link function
def get_csv_download_link(df):
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()
    href = f'<a href="data:file/csv;base64,{b64}" download="classification_results.csv">Download CSV</a>'
    return href

# Streamlit app
def main():
    st.title("Document Classifier")

    # user to enter API key
    api_key = st.text_input("Enter your OpenAI API key got from https://platform.openai.com/account/api-keys", type="password")
    
    openai.api_key = api_key

    # user to upload a file
    file = st.file_uploader("Upload a readable .pdf(NOT an image scanned Pdf), .csv, or .xlsx file", type=["pdf", "csv", "xlsx"])

    # user to input up to 6 categories
    categories = st.text_input("Enter up to 6 categories separated by commas", "")

    # Processing
    if file and categories:
        if file.type == "application/pdf":
            text = load_pdf(file)
        elif file.type == "text/csv":
            text = load_csv(file)
        elif file.type == "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet":
            text = load_xlsx(file)

        # Clean the text
        cleaned_text = clean_text(text)

        # Define the classification prompt
        classify_prompt = (
            f"Classify the following text as one of the user input: {categories} "
            "If it's not clear, choose the emotion that is closest to the user's input.\n"
            "Text: cleaned_text\nEmotion:"
        )

        # Get the classification label
        label = classify_label(cleaned_text, classify_prompt)

        # Create dataframe
        df = pd.DataFrame({"text": [text], "cleaned_text": [cleaned_text], "label": [label]})
        
            # Display the results
        st.write("Classification Results:")
        st.write(df)

        # Download the results as a CSV file
        st.markdown(get_csv_download_link(df), unsafe_allow_html=True)
        
#Run the app
if name == "main":
    main()      
