import openai
import streamlit as st
import pandas as pd
import io
import openpyxl
import base64

COMPLETIONS_MODEL = "text-davinci-003"

def load_csv(file):
    df = pd.read_csv(file)
    return df

def load_xlsx(file):
    df = pd.read_excel(file)
    return df

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

# Download button function
def download_button(df):
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()
    button = f'<a href="data:file/csv;base64,{b64}" download="classification_results.csv"><input type="button" value="Download CSV"></a>'
    return button

# Streamlit app
def main():
    st.title("Auto Classifier")
    st.title("App to classify unlabeld texts in CSV or XLSX file based on user's input for up to 6 categories for classification..")

    # user input API key
    api_key = st.text_input("Enter your OpenAI API key got from https://platform.openai.com/account/api-keys", type="password")
    
    openai.api_key = api_key

    # user to upload a file
    file = st.file_uploader("Upload less than 100 rows of unlabeled texts in .csv, or .xlsx file", type=["csv", "xlsx"])

    # user to input up to 6 categories
    categories = st.text_input("Enter up to 6 categories separated by commas", "")

    # Processing
    if file and categories:
        if file.type == "text/csv":
            df = load_csv(file)
        elif file.type == "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet":
            df = load_xlsx(file)

        # Clean the text
        df['cleaned_text'] = df['text'].apply(clean_text)

        # Define the classification prompt
        classify_prompt = (
            f"Classify the following text as one of the user input: {categories} "
            "If it's not clear, choose the emotion that is closest to the user's input.\n"
            "Text: cleaned_text\nEmotion:"
        )

        # Get the classification label
        df['label'] = df['cleaned_text'].apply(lambda x: classify_label(x, classify_prompt))

        # Display results
        st.write("Classification Results:")
        st.write(df[['text', 'label']])

        # Download the results as CSV file
        st.markdown(download_button(df), unsafe_allow_html=True)

# Run the app
if __name__ == "__main__":
    main()
