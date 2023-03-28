
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
    # Set API key as a secret
    with open('api_key.txt', 'r') as f:
        api_key = f.read().strip()
    openai.api_key = api_key    
    
    # Prompt user to upload a file
    file = st.file_uploader("Upload a PDF, CSV, or XLSX file", type=["pdf", "csv", "xlsx"])

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

        # Assign file content to prompt var
        prompt = text

        # Set up Streamlit app 
        st.title("Ask a Question about the Document")

        # Prompt user to enter a question
        question = st.text_input("What do you want to know about it?")

        # Generate answer if user inputs question
        if question:
            prompt = f"Answer the question as truthfully as possible using the provided text. If the answer is not contained within the text below, say 'I don't know'.\n\n{prompt}"
            prompt_with_question= f"{prompt}\n\nQuestion: {question}\nA"
            response = openai.Completion.create(
                prompt=prompt_with_question,
                temperature=0.0,
                max_tokens=512,
                top_p=1,
                frequency_penalty=0,
                presence_penalty=0,
                model="text-davinci-003",
                stop=["Q:", "\n"],
                timeout=100  # wait for 100 seconds before timing out
            )

            # Extract answer from OpenAI API response
            answer = response.choices[0].text.strip()

            # Output answer or "I don't know" if answer is empty
            answer_output = answer.strip() if answer.strip() != '' else "I don't know"
            st.write(f"Q: {question}")
            st.write(f"A: {answer_output}\n")
                    
if __name__ == "__main__":
    st.set_page_config(page_title='Document Question and Answer', page_icon=':books:')
    st.title('Document Question and Answer')
    st.write('App to answer your questions about PDF, CSV, or XLSX documents.')
    main()
