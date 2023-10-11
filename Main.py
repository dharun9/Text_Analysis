import streamlit as st
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

        # Create a sidebar with the option menu and apply custom styling
        with st.sidebar:
            st.write("### Options")  # Add a title
            app = st.selectbox("Select an option:", ['Index', 'Home', 'Analysis', 'Link', 'Theme'],
                           index=self.apps.index(next(app for app in self.apps if app["title"] == selected_app)))

            # Add custom CSS styling for the sidebar
            st.markdown(
                """
                <style>
                .sidebar .stSelectbox {
                    background-color: #F5F5F5;
                    padding: 10px;
                    border-radius: 8px;
                }
                </style>
                """,
                unsafe_allow_html=True,
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
