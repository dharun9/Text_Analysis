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
    st.title("URLs with Associated Text")

    # Upload a dataset
    uploaded_file = st.file_uploader("Upload an XLSX file", type=["xlsx"])
    if uploaded_file is not None:
        df = pd.read_excel(uploaded_file)

        # Extract URLs and their associated text from the "Message" column
        df['URLs with Text'] = df['Message'].apply(extract_urls_with_text)

        # Clean text in the "URLs with Text" column
        df['URLs with Text'] = df['URLs with Text'].apply(lambda x: [clean_text(item) for item in x])

        # Create a new Excel file with the extracted URLs and associated text
        new_excel_file = "extracted_urls_with_text.xlsx"
        df[['Date', 'Time', 'Sender', 'URLs with Text']].to_excel(new_excel_file, index=False)

        st.success(f"URLs with associated text extracted and saved to {new_excel_file}.")

        # Create separate Excel files for each sender's URLs
        unique_senders = df['Sender'].unique()
        for sender in unique_senders:
            sender_df = df[df['Sender'] == sender].reset_index(drop=True)
            sender_excel_file = f"{sender}_urls_with_text.xlsx"
            sender_df[['Date', 'Time', 'Sender', 'URLs with Text']].to_excel(sender_excel_file, index=False)
        
            # Add a button to download each sender's URLs as an Excel file
            if st.button(f"Download {sender}'s URLs with Text as Excel"):
                # Create a BytesIO object to store the Excel data
                excel_buffer = io.BytesIO()

                # Use pandas to write the sender's URLs DataFrame to the BytesIO object as an Excel file
                with pd.ExcelWriter(excel_buffer, engine="xlsxwriter") as writer:
                    sender_df[['Date', 'Time', 'Sender', 'URLs with Text']].to_excel(writer, sheet_name=f"{sender}'s URLs with Text", index=False)

                # Set up the BytesIO object for download
                excel_buffer.seek(0)
                b64 = base64.b64encode(excel_buffer.read()).decode()
                href = f'<a href="data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{b64}" download="{sender}_URLs_with_Text.xlsx">Download {sender}\'s URLs with Text</a>'
                st.markdown(href, unsafe_allow_html=True)

if __name__ == "__main__":
    app()
