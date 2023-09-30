import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import regex as re
from collections import Counter
from matplotlib.ticker import MaxNLocator

# Create a function to load data with caching
@st.cache(allow_output_mutation=True)
def load_data(file):
    return pd.read_excel(file)

def app():
    # Upload an Excel file
    uploaded_file = st.file_uploader("Upload an Excel file", type=["xlsx"])
    if uploaded_file is not None:
        # Load the data
        df = load_data(uploaded_file)

        # Show the DataFrame
        st.subheader("Data")

        # Add a button to toggle data visibility
        if st.button("Toggle Data Display"):
            st.write(df)

        # Visualize the top 10 active members with a unique color
        st.subheader("Top 10 Active Members")
        top_active_members = df['Sender'].value_counts().head(10)
        color_active = st.color_picker("Choose a color for Active Members", "#0074D9")

        # Create a professional-looking bar chart
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.bar(top_active_members.index, top_active_members, color=color_active)
        ax.set_xlabel("Members", fontsize=14)
        ax.set_ylabel("Message Count", fontsize=14)
        ax.set_title("Top 10 Active Members", fontsize=16)
        ax.tick_params(axis='x', labelrotation=45)  # Rotate x-axis labels for better readability
        plt.tight_layout()  # Ensure proper spacing
        st.pyplot(fig)
# Extract the day of the week from the date
        def extract_day_of_week(date):
        # Convert the date to a day of the week (Monday, Tuesday, etc.)
            return date.strftime("%A")
        # Extract the day of the week from the date
        df['Day of Week'] = df['Date'].apply(extract_day_of_week)

        # Visualize the most active days of the week with a unique color
        st.subheader("Most Active Days of the Week")
        active_day = df['Day of Week'].value_counts()
        top_active_days = active_day.head(10)

        # Create a professional-looking bar chart
        fig, ax = plt.subplots(figsize=(10, 6))
        tx = top_active_days.plot(kind='bar', color='dodgerblue', edgecolor='black', ax=ax)

        ax.set_xlabel('Day of Week', fontsize=14, fontweight='bold')
        ax.set_ylabel('Number of Messages', fontsize=14, fontweight='bold')
        ax.set_title('Most Active Days in the Group', fontsize=18, fontweight='bold')

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

       

if __name__ == "__main__":
    app()
