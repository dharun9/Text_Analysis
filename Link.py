import streamlit as st
import pandas as pd
import re
import base64
import io
from urllib.parse import urlparse

# Function to extract URLs and their associated text from text
def extract_urls_with_text(text):
    # Use regular expression to find all URLs
    urls = re.findall(r'(https?://[^\s]+)', text)
    
    # Extract the associated text for each URL
    url_data = []
    for url in urls:
        parsed_url = urlparse(url)
        start = text.find(url)
        end = start + len(url)
        url_text = text[:start] + text[end:]
        url_data.append({'URL': url, 'Text': url_text.strip()})
    
    return url_data

# Function to clean text data
def clean_text(text):
    if isinstance(text, str):
        # Remove unwanted characters or patterns
        cleaned_text = re.sub(r'\n', ' ', text)  # Remove newlines
        return cleaned_text
    return text

def app():
    st.subheader("Links associated with Data")
    df = st.session_state.df

    # Extract URLs and their associated text from the "Message" column
    df['URLs with Text'] = df['Message'].apply(extract_urls_with_text)

    # Clean text in the "URLs with Text" column
    df['URLs with Text'] = df['URLs with Text'].apply(lambda x: [clean_text(item) for item in x])

    # Filter rows where "URLs with Text" is not empty (remove rows with empty lists)
    df = df[df['URLs with Text'].apply(lambda x: bool(x))]

    # Create a new Excel file with the extracted URLs and associated text
    new_excel_file = "extracted_urls_with_text.xlsx"
    df[['Date', 'Time', 'Sender', 'URLs with Text']].to_excel(new_excel_file, index=False)

    st.success(f"URLs with associated text extracted and saved to {new_excel_file}.")

    # Display all the contents of the Excel file in Streamlit
    st.subheader("Contents of the Excel File")
    st.dataframe(df)

    # Display a link to download the extracted Excel file
    st.subheader("Download Extracted URLs with Text as Excel")
    st.write(f"You can download the extracted URLs with associated text as an Excel file from the following link:")
    st.markdown(get_download_link(new_excel_file), unsafe_allow_html=True)

def get_download_link(file_path):
# Create a download link for the given file path
    with open(file_path, "rb") as file:
        file_contents = file.read()
        b64 = base64.b64encode(file_contents).decode()
        href = f'<a href="data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{b64}" download="{file_path}">Download {file_path}</a>'
        return href

if __name__ == "__main__":
    app()
