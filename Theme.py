import streamlit as st
import pandas as pd
import re
import base64
import nltk
import io
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import TruncatedSVD
import plotly.express as px

# Function to generate a download link for a DataFrame
def get_table_download_link(df):
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()  # Bypass pandas DataFrame.to_csv() conversion
    href = f'<a href="data:file/csv;base64,{b64}" download="filtered_data.csv">Download CSV File</a>'
    return href

def create_bar_chart(data, x_col, y_col, title, filename):
    fig = px.bar(data, x=x_col, y=y_col, labels={"x": "Sender", "y": "Count"}, title=title)
    st.plotly_chart(fig)

    # Create a link to download the chart
    buffer = io.StringIO()
    fig.write_html(buffer)
    chart_html = buffer.getvalue()
    st.markdown(get_download_link(chart_html, filename), unsafe_allow_html=True)

def get_download_link(html, filename):
    """Generate a link to download the given HTML content."""
    b64 = base64.b64encode(html.encode()).decode()
    href = f'<a href="data:text/html;base64,{b64}" download="{filename}.html">Download {filename}</a>'
    return href

def app():
    # Download NLTK data and corpora (you need to do this only once)
    nltk.download('punkt')
    nltk.download('stopwords')

    # Streamlit UI
    st.title("Agricultural related Classification")
    
    # Initialize df if it's not already in session_state
    uploaded_file = st.file_uploader("Upload an XLSX file", type=["xlsx"])
    if uploaded_file is not None:
        df = pd.read_excel(uploaded_file)
    
 

    # Function to preprocess text
    def preprocess_text(text):
        # Tokenization
        tokens = word_tokenize(text)

        # Remove punctuation and convert to lowercase
        tokens = [re.sub(r'[^\w\s]', '', token.lower()) for token in tokens]

        # Remove stopwords
        stop_words = set(stopwords.words('english'))
        tokens = [token for token in tokens if token not in stop_words]

        # Stemming
        stemmer = PorterStemmer()
        tokens = [stemmer.stem(token) for token in tokens]

        return ' '.join(tokens)  # Join tokens back into a text string

    # Apply preprocessing to the 'Message' column
    df['Preprocessed Message'] = df['Message'].apply(preprocess_text)

    # Create a TF-IDF matrix
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(df['Preprocessed Message'])

    # Apply TruncatedSVD to perform LSA
    lsa_model = TruncatedSVD(n_components=5)  # You can adjust the number of components as needed
    lsa_topic_matrix = lsa_model.fit_transform(tfidf_matrix)

    # Define keywords related to themes
    themes_keywords = {
        'food': ['food', 'eat', 'meal', 'dish'],
        'agricultural': ['agricultur', 'farm', 'crop', 'harvest'],
        'fertilizer': ['fertil', 'nutrient', 'soil', 'plant'],
        'seeds': ['seed', 'plant', 'grow', 'crop'],
        'fruits': ['fruit', 'apple', 'banana', 'citrus'],
        'pesticide': ['pesticid', 'insect', 'chemical', 'spray'],
        'plants': ['plant', 'grow', 'veget', 'leaf'],
        'animals': ['anim', 'livestock', 'cattl', 'poultri']
    }

    # Create a function to check if a message contains keywords related to a theme
    def has_theme_keywords(message, theme_keywords):
        for theme_keyword in theme_keywords:
            if re.search(rf'\b{re.escape(theme_keyword)}\b', message, re.IGNORECASE):
                return True
        return False

    # Filter LSA topics based on themes and create theme-related columns
    for theme in themes_keywords:
        theme_keywords_list = themes_keywords[theme]
        theme_column = f'{theme}_related'
        df[theme_column] = df['Preprocessed Message'].apply(lambda x: 1 if has_theme_keywords(x, theme_keywords_list) else 0)

    # Slicer to categorize data based on themes
    st.sidebar.header("Categorize Data")
    selected_themes = st.sidebar.multiselect("Select Themes", list(themes_keywords.keys()))

    if not selected_themes:
        st.sidebar.warning("Select one or more themes to categorize the data.")
    else:
        # Filter DataFrame to keep rows related to selected themes
        selected_theme_columns = [f'{theme}_related' for theme in selected_themes]
        filtered_df = df[df[selected_theme_columns].sum(axis=1) > 0]

        # Remove the specified columns
        columns_to_remove = ['Preprocessed Message'] + [f'{theme}_related' for theme in themes_keywords if theme not in selected_themes]
        filtered_df.drop(columns=columns_to_remove, inplace=True)

        # Show the filtered DataFrame
        st.subheader("Filtered Data")
        st.dataframe(filtered_df)

        # Generate and display the download link
        download_link = get_table_download_link(filtered_df)
        st.markdown(download_link, unsafe_allow_html=True)

        # Create bar charts for active senders
        for theme in selected_themes:
            active_senders = filtered_df.groupby("Sender").size().sort_values(ascending=False).head(10)
            st.subheader(f"Top 10 Active Senders for '{theme}' Theme")
            create_bar_chart(active_senders, x_col=active_senders.index, y_col=active_senders.values, title=f"Top 10 Active Senders for '{theme}' Theme", filename=f"active_senders_{theme}")

if __name__ == "__main__":
    app()
