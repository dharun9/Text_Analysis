import streamlit as st
from streamlit_option_menu import option_menu
import Index, Home, Analysis, Link, Theme

# Set page configuration
st.set_page_config(
    page_title="String Analysis",
)

class CustomSessionState:
    def __init__(self):
        self._state = {}

    def get(self, key, default):
        return self._state.get(key, default)

    def set(self, key, value):
        self._state[key] = value

class MultiApp:
    def __init__(self):
        self.apps = []
        self.session_state = CustomSessionState()

    def add_app(self, title, func):
        self.apps.append({
            "title": title,
            "function": func
        })

    def run(self):
        # Get the selected app from the custom session state or default to "Home"
        selected_app = self.session_state.get("selected_app", "Home")

        # Create a sidebar with the option menu
        with st.sidebar:
            app = option_menu(
                menu_title='Options',
                options=['Index', 'Home', 'Analysis', 'Link', 'Theme'],
                icons=['house-fill', 'chat-fill', 'trophy-fill', 'chat-fill', 'info-circle-fill'],
                menu_icon='chat-text-fill',
                default_index=self.apps.index(next(app for app in self.apps if app["title"] == selected_app)),
                styles={
                    "container": {"padding": "5!important", "background-color": 'black'},
                    "icon": {"color": "white", "font-size": "23px"},
                    "nav-link": {"color": "white", "font-size": "20px", "text-align": "left", "margin": "0px", "---hover-color": "blue"},
                    "nav-link-selected": {"background-color": "#02ab21"},
                }
            )

        # Store the selected app in the custom session state
        self.session_state.set("selected_app", app)

        # Run the selected app
        for item in self.apps:
            if item["title"] == app:
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
