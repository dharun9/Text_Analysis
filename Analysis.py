import matplotlib
matplotlib.use("Agg")  # Use the "Agg" backend for Matplotlib

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter
from matplotlib.ticker import MaxNLocator
from wordcloud import WordCloud
from textblob import TextBlob

# Create a function to load data with caching
@st.cache(allow_output_mutation=True)
def load_data(file):
    return pd.read_excel(file)

def app():
    df = st.session_state.df

    # Show the DataFrame
    st.subheader("Data")

    # Add a button to toggle data visibility
    if st.button("Toggle Data Display"):
        st.write(df)

    # Visualize the top N active members with a unique color
    st.subheader("Top Active Members")
    top_active_members_count = st.slider("Select the number of top active members", 1, 20, 10)
    top_active_members = df['Sender'].value_counts().head(top_active_members_count)
    color_active = st.color_picker("Choose a color for Active Members", "#0074D9")

    # Create a professional-looking bar chart
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.bar(top_active_members.index, top_active_members, color=color_active)
    ax.set_xlabel("Members", fontsize=14)
    ax.set_ylabel("Message Count", fontsize=14)
    ax.set_title(f"Top {top_active_members_count} Active Members", fontsize=16)
    ax.tick_params(axis='x', labelrotation=45, labelsize=12)  # Rotate x-axis labels and set label size
    ax.tick_params(axis='y', labelsize=12)  # Set y-axis label size
    plt.tight_layout()  # Ensure proper spacing
    st.pyplot(fig)

    # Extract and count the top 10 <Media Omitted> on Message by sender
    top_media_omitted = df[df['Message'] == '<Media omitted>']['Sender'].value_counts().head(10)

    # Create a professional-looking histogram
    st.subheader("Top 10 <Media Omitted> on Message by Sender")
    color_media = st.color_picker("Choose a color for Media Omitted", "#FF5733")

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.bar(top_media_omitted.index, top_media_omitted, color=color_media)
    ax.set_xlabel("Senders", fontsize=14)
    ax.set_ylabel("<Media Omitted> Count", fontsize=14)
    ax.set_title("Top 10 <Media Omitted> on Message by Sender", fontsize=16)
    ax.tick_params(axis='x', labelrotation=45, labelsize=12)  # Rotate x-axis labels and set label size
    ax.tick_params(axis='y', labelsize=12)  # Set y-axis label size
    plt.tight_layout()  # Ensure proper spacing
    st.pyplot(fig)

    # Convert the 'Date' column to datetime objects
    df['Date'] = pd.to_datetime(df['Date'])

    # Extract the day of the week from the date
    df['Day of Week'] = df['Date'].dt.strftime("%A")

    # Visualize the top N most active days of the week with a unique color
    st.subheader("Most Active Days of the Week")
    top_active_days_count = st.slider("Select the number of top active days", 1, 7, 5)
    active_day = df['Day of Week'].value_counts().head(top_active_days_count)

    # Create a professional-looking bar chart
    fig, ax = plt.subplots(figsize=(10, 6))
    tx = active_day.plot(kind='bar', color='dodgerblue', edgecolor='black', ax=ax)

    ax.set_xlabel('Day of Week', fontsize=14, fontweight='bold')
    ax.set_ylabel('Number of Messages', fontsize=14, fontweight='bold')
    ax.set_title(f"Top {top_active_days_count} Active Days in the Group", fontsize=16, fontweight='bold')

    # Converting y-axis data to integer
    ax.yaxis.set_major_locator(MaxNLocator(integer=True))

    # Add value labels above each bar
    for bar in tx.patches:
        height = bar.get_height()
        ax.annotate(f'{height}', xy=(bar.get_x() + bar.get_width() / 2, height),
                    xytext=(0, 3), textcoords='offset points',
                    ha='center', va='bottom', fontsize=12, fontweight='bold')

    plt.xticks(rotation=0, ha='center', fontsize=12)
    plt.yticks(fontsize=12)
    plt.tight_layout()
    st.pyplot(fig)

    # Create a word cloud
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate(' '.join(df['Message']))

    # Display the word cloud
    st.subheader("Word Cloud of Most Common Words")
    st.image(wordcloud.to_array(), use_column_width=True)

    # Message activity over time
    st.subheader("Message Activity Over Time")
    df['Date'] = pd.to_datetime(df['Date'])
    message_activity_days = st.slider("Select the number of days for message activity", 1, 365, 30)
    message_activity = df.resample(f'{message_activity_days}D', on='Date').size()  # Resample data by days

    # Create a professional-looking line chart
    fig, ax = plt.subplots(figsize=(10, 6))
    message_activity.plot(kind='line', color='green', marker='o', ax=ax)
    ax.set_xlabel("Date", fontsize=14)
    ax.set_ylabel("Message Count", fontsize=14)
    ax.set_title(f"Message Activity Over the Years", fontsize=16)
    ax.grid(True)
    plt.xticks(rotation=45, fontsize=12)  # Rotate x-axis labels and set label size
    plt.yticks(fontsize=12)  # Set y-axis label size
    plt.tight_layout()
    st.pyplot(fig)

    # Perform sentiment analysis on messages
    def get_sentiment(text):
        analysis = TextBlob(text)
        if analysis.sentiment.polarity > 0:
            return 'Positive'
        elif analysis.sentiment.polarity < 0:
            return 'Negative'
        else:
            return 'Neutral'

    df['Sentiment'] = df['Message'].apply(get_sentiment)

    st.subheader("Sentiment Analysis")
    sentiment_counts = df['Sentiment'].value_counts()

    # Create a professional-looking bar chart for sentiment analysis
    fig, ax = plt.subplots(figsize=(8, 6))
    sentiment_counts.plot(kind='bar', color='skyblue', edgecolor='black', ax=ax)
    ax.set_xlabel("Sentiment", fontsize=14)
    ax.set_ylabel("Count", fontsize=14)
    ax.set_title("Sentiment Analysis", fontsize=16)
    ax.tick_params(axis='x', rotation=0, labelsize=12)
    ax.tick_params(axis='y', labelsize=12)
    plt.tight_layout()
    st.pyplot(fig)



if __name__ == "__main__":
    app()
