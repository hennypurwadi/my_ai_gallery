
import openai
import streamlit as st
from PyPDF2 import PdfReader
import openpyxl

def load_pdf(file):
    pdf_reader = PdfReader(file)
    num_pages = len(pdf_reader.pages)
    text = ""
    for page in range(num_pages):
        page_obj = pdf_reader.pages[page]
        text += page_obj.extract_text()
    return text

def load_xlsx(file):
    workbook = openpyxl.load_workbook(file, read_only=True)
    sheet = workbook.active
    data = []

    for row in sheet.iter_rows(values_only=True):
        data.append(row)

    text = ""
    for row in data:
        text += " ".join([str(cell) for cell in row]) + "\n"
    
    return text

def main():    
    # Set API key as a secret
    with open('api_key.txt', 'r') as f:
        api_key = f.read().strip()
    openai.api_key = api_key 

    # Prompt user to upload a file
    file = st.file_uploader("Upload a PDF or XLSX file", type=["pdf", "xlsx"])

    # Generate summary and example QnAs if file is uploaded
    if file is not None:
        # Read file content
        with st.spinner('Extracting text from file...'):
            if file.type == "application/pdf":
                text = load_pdf(file)
            elif file.type == "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet":
                text = load_xlsx(file)

        # Set up Streamlit app 
        st.title("Ask a Question about Your Document")

        # Prompt user to enter a question
        question = st.text_input("What do you want to know about it?")

        # Generate answer if user inputs a question
        if question:
            prompt = f"Answer the question as truthfully as possible using the provided text. +\
            If the answer is not contained within the text below, say 'I don't know'.\n\n{prompt}"
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
                timeout=600  # wait for 600 seconds before timing out
            )

            # Extract answer from OpenAI API response
            answer = response.choices[0].text.strip()

            # Output answer or "I don't know" if answer is empty
            answer_output = answer.strip() if answer.strip() != '' else "I don't know"
            st.write(f"Q: {question}")
            st.write(f"A: {answer_output}\n")
                    
if __name__ == "__main__":
    st.set_page_config(page_title='PDF Question and Answer', page_icon=':books:')
    st.title('PDF Question and Answer')
    st.write('App to answer your questions about PDF or XLSX documents.')
    main()
