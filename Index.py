# Index.py (Updated)

import streamlit as st

def app():
    st.title("Index Page")
    
    # Add a note explaining the CSV file requirements
    st.info("Please upload a CSV file with the following columns: Date, Time, Sender, and Message. Ensure that the column names match exactly as specified for successful analysis.")
    
    # Add a description of the data cleaning process
    st.write("In the WhatsApp dataset, there were 8500 records. To prepare the data for analysis, we performed the following cleaning steps:")
    
    # Add any additional information or instructions here
    st.write("Feel free to explore the 'Home' and 'Analysis' sections for insights and visualizations based on the cleaned data.")
    
    
