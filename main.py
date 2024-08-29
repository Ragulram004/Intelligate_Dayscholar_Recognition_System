import streamlit as st

from streamlit_option_menu import option_menu


import Home, User_logs,Images_Captured,About,login
st.set_page_config(
        page_title="Intelligate",
)



class MultiApp:

    def __init__(self):
        self.apps = []

    def add_app(self, title, func):

        self.apps.append({
            "title": title,
            "function": func
        })

    def run():
        # app = st.sidebar(     
            app = option_menu(
                menu_title=None,
                options=['Home','User logs','Captured','About'],
                icons=['house-fill','person-circle','trophy-fill','info-circle-fill'],
                default_index=0,
                orientation = "horizontal"
        #         styles={
        #             "container": {"padding": "5!important","background-color":'black'},
        # "icon": {"color": "white", "font-size": "18px"}, 
        # "nav-link": {"color":"white","font-size": "16px", "text-align": "left", "margin":"0px", "--hover-color": "#FF5D51"},
        # "nav-link.active":{"font-weight":"100"},
        # "nav-link-selected": {"background-color": "#262730"},}
                
                )

        
            if app == "Home":
                Home.app()
            if app == "User logs":
                User_logs.app()    
            if app == "Captured":
                Images_Captured.app()        
            if app == 'About':
                About.app()    
             
    run()            
         