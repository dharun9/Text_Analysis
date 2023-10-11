import streamlit as st
from streamlit_option_menu import option_menu
import Index, Home, Analysis, Link, Theme

# Set page configuration
st.set_page_config(
    page_title="String Analysis",
)

class MultiApp:
    def __init__(self):
        self.apps = []

    def add_app(self, title, func):
        self.apps.append({
            "title": title,
            "function": func
        })

    def run(self):
        # Create a sidebar with the option menu
        with st.sidebar:
            selected_app = option_menu(
                menu_title='Options',
                options=['Index', 'Home', 'Analysis', 'Link', 'Theme'],
                icons=['house-fill', 'chat-fill', 'trophy-fill', 'chat-fill', 'info-circle-fill'],
                menu_icon='chat-text-fill',
            )

        # Run the selected app
        for item in self.apps:
            if item["title"] == selected_app:
                item["function"]()

# Create an instance of MultiApp
multi_app = MultiApp()

# Add your apps to the MultiApp instance
multi_app.add_app("Index", Index.app)
multi_app.add_app("Home", Home.app)
multi_app.add_app("Analysis", Analysis.app)
multi_app.add_app("Link", Link.app)
multi_app.add_app("Theme", Theme.app)

# Run the selected app
multi_app.run()
