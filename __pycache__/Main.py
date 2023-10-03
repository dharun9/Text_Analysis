import streamlit as st 
from streamlit_option_menu import option_menu 

import Index, Home, Analysis, Link;
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

    def run(self):  # Added 'self' as a parameter
        # app = st.sidebar(
        with st.sidebar:        
            app = option_menu(
                menu_title='Options',
                options=['Index','Home','Analysis','Link'],
                icons=['house-fill','chat-fill','trophy-fill','chat-fill','info-circle-fill'],
                menu_icon='chat-text-fill',
                default_index=1,
                styles={
                    "container": {"padding": "5!important","background-color":'black'},
                    "icon": {"color": "white", "font-size": "23px"}, 
                    "nav-link": {"color":"white","font-size": "20px", "text-align": "left", "margin":"0px", "--hover-color": "blue"},
                    "nav-link-selected": {"background-color": "#02ab21"},
                }
            )
        if app == "Index":
            Index.app()
        if app == "Home":
            Home.app()
        if app == "Analysis":
            Analysis.app()
        if app == "Link":
            Link.app()

# Create an instance of MultiApp
multi_app = MultiApp()
# Add your apps to the MultiApp instance
multi_app.add_app("Index", Index.app)
multi_app.add_app("Home", Home.app)
multi_app.add_app("Analysis", Analysis.app)
multi_app.add_app("Link", Link.app)
# Run the selected app
multi_app.run()
