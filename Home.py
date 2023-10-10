import streamlit as st
import pandas as pd
import re
import nltk
import base64
import heapq
from nltk.corpus import stopwords
import io

# Download NLTK resources
nltk.download('stopwords')
nltk.download('punkt')

def app():
    st.title("String Analysis")

    # Function to identify questions and remove "Welcome @"
    def is_question(text):
        if isinstance(text, str):
            text = re.sub(r'^Welcome @', '', text)  # Remove "Welcome @" from the beginning
            text = text.strip()  # Remove leading and trailing spaces

            # Define a list of common question words and articles
            question_words = ["how", "what", "who", "where", "why"]
            articles = ["the", "a"]

            # Split the text into words
            words = text.split()

            # Check if the last word ends with a question mark
            if text.endswith('?'):
                return True

            # Check if the text starts with a common question word or article
            if words[0].lower() in question_words or words[0].lower() in articles:
                return True

        return False

    def clean_text(text):
        patterns_to_remove = [
            r'Saravanan Sir Kct added.*',
            r'Welcome to the group, Thanks for adding.*',
            r'Your security code with the.*',
            r'added to this group',
            r'Media omitted',
            r'thanks',
            r'thank you',
            r'Welcome',
            r'Welcome to the group',
            r'Thanks for adding to the group',
            r'Thanks for adding me to this group',
            r'Saravanan Sir Kct',
            r'<@\d+>',  # Remove integers in the format <@integer>
            r'Thanks for adding',
            r'Thanks for adding me to this group',
            r'Thank you',
            r'Thank you.',
            r'@',
            r'Saravanan Sir Kct added<@integer>',
            r'You deleted this message',
            r'Mrs to the Group',
            r'Mr to the Group',
            r'Dr. to the group',
            r'This message was deleted',
            r'Thank you sir.',
            r'Thank you sir',
            r'Thanks a lot',
            r'Thanks bro',
            r'This message was deleted Your security code with Shyamsunder FT BK  changed. Tap to learn more.',
            r'Your security code',
            r'Tap to learn more.',
            r'Please contact me sir'
        ]

        # Apply each pattern for removal
        for pattern in patterns_to_remove:
            text = re.sub(pattern, ' ', text)  # Replace removed patterns with a space

        # Replace multiple spaces with a single space
        text = re.sub(r'\s+', ' ', text)

        return text.strip()
    # Function to extract themes from questions using NLTK
    def extract_theme(question):
        # Tokenize the question
        words = nltk.word_tokenize(question.lower())

        # Remove stopwords and punctuation
        words = [word for word in words if word not in stopwords.words('english') and re.match(r'\w', word)]

        # Find potential theme keywords (e.g., "theme", "topic", "subject")
        theme_keywords = ['theme', 'topic', 'subject']

        # Search for the theme keyword and return the following word
        for i, word in enumerate(words):
            if word in theme_keywords and i < len(words) - 1:
                return words[i + 1]

        return None  # If no theme is found

    # Function to generate a summary from a question using heapq
    def generate_summary(question, num_sentences=2):
        # Tokenize the question into sentences
        sentences = nltk.sent_tokenize(question)

        # Create a list to store sentence scores
        sentence_scores = {}

        # Calculate the score for each sentence based on word frequency
        word_frequencies = {}
        for sentence in sentences:
            words = nltk.word_tokenize(sentence.lower())
            for word in words:
                if word not in stopwords.words('english'):
                    if word in word_frequencies:
                        word_frequencies[word] += 1
                    else:
                        word_frequencies[word] = 1

        # Calculate sentence scores
        for sentence in sentences:
            for word in nltk.word_tokenize(sentence.lower()):
                if word in word_frequencies:
                    if sentence in sentence_scores:
                        sentence_scores[sentence] += word_frequencies[word]
                    else:
                        sentence_scores[sentence] = word_frequencies[word]

        # Get the top 'num_sentences' sentences as the summary
        summary_sentences = heapq.nlargest(num_sentences, sentence_scores, key=sentence_scores.get)

        # Combine the summary sentences into a single summary
        summary = ' '.join(summary_sentences)

        return summary

    # Upload a dataset
    uploaded_file = st.file_uploader("Upload an XLSX file", type=["xlsx"])
    if uploaded_file is not None:
        df = pd.read_excel(uploaded_file)
        st.session_state.df = df 


        # Initialize variables to store data
        dates = []
        questions = []
        answers = []
        senders = []  # Initialize a list to store senders
        sent_times = []  # Initialize a list to store sent times
        replying_times = []  # Initialize a list to store replying times

        # Initialize variables for the current question
        current_question = ""
        current_answers = []
        current_senders = set()  # Use a set to store unique senders for each question
        current_date = ""
        current_time = ""

        # Iterate through the 'tweet_text', 'Date', and 'Time' columns
        for index, row in df.iterrows():
            text = row['Message']
            date = row['Date']  # Assuming you have a 'Date' column in your DataFrame
            time = row['Time']  # Assuming you have a 'Time' column in your DataFrame
            sender = row['Sender']  # Assuming you have a 'Sender' column in your DataFrame

            # Check if the text is a question
            if is_question(text):
                # Start a new question
                if current_question:
                    # Append the current question, date, answers, senders, sent time, and replying time to lists
                    dates.append(current_date)
                    questions.append(current_question)
                    # Remove integers (contact numbers) from the answers and keep only text
                    filtered_answers = [re.sub(r'\d+', '', str(ans)) for ans in current_answers]
                    answers.append("\n".join(map(str, filtered_answers)))  # Convert filtered answers to strings before joining
                    senders.append(", ".join(map(str, current_senders)))  # Convert senders set to a comma-separated string
                    sent_times.append(current_time)
                    replying_times.append(time)
                    current_answers = []  # Reset the answers list for the new question
                    current_senders = set()  # Reset the senders set for the new question

                current_question = text
                current_date = date
                current_time = time
            else:
                # Add the text as an answer to the current question
                if current_question:
                    current_answers.append(text)
                    current_senders.add(str(sender))  # Convert the sender to a string and add it to the set of senders

        # Add the last question and its answers
        # Add the last question and its answers
        if current_question:
            dates.append(current_date)
            questions.append(current_question)
            # Remove integers (contact numbers) from the answers and keep only text
            filtered_answers = [re.sub(r'\d+', '', str(ans)) for ans in current_answers]
            answers.append("\n".join(map(str, filtered_answers)))  # Convert filtered answers to strings before joining
            senders.append(", ".join(map(str, current_senders)))  # Convert senders set to a comma-separated string
            sent_times.append(current_time)
            replying_times.append(time)

            # Create a DataFrame
            qa_df = pd.DataFrame({'Date': dates, 'Sent time': sent_times, 'Replying time': replying_times, 'Questions': questions, 'Answers': answers, 'Sender': senders})
            # Rename the "solution" column to "answer"
            qa_df.rename(columns={'Answers': 'Answer'}, inplace=True)
            qa_df['Questions'] = qa_df['Questions'].apply(clean_text)
            qa_df['Answer'] = qa_df['Answer'].apply(clean_text)

            # Filter out rows with blank answers
            qa_df = qa_df[qa_df['Answer'] != '']
            # Check if 'qa_df' is defined and not empty
            if 'qa_df' in locals() and not qa_df.empty:
                st.write("Displaying Data:")
                st.write(qa_df)


        # Add a button to download the displayed and cleaned data as an Excel file
        if st.button("Download Cleaned Data as Excel"):
            # Create a BytesIO object to store the Excel data
            excel_buffer = io.BytesIO()

            # Use pandas to write the cleaned DataFrame to the BytesIO object as an Excel file
            with pd.ExcelWriter(excel_buffer, engine="xlsxwriter") as writer:
                qa_df.to_excel(writer, sheet_name="Data", index=False)

            # Set up the BytesIO object for download
            excel_buffer.seek(0)
            b64 = base64.b64encode(excel_buffer.read()).decode()
            href = f'<a href="data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{b64}" download="Cleaned_Question_Answer_Data.xlsx">Download Cleaned Excel File</a>'
            st.markdown(href, unsafe_allow_html=True)
    else:
        st.write("Please upload an XLSX file to analyze.")


if __name__ == "__main__":
    app()
