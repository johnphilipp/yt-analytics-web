from utils import app
from components import home
from components import request
import streamlit as st
import pandas as pd
from streamlit_option_menu import option_menu


# -----------------------------------------------------------------------

# Header

st.set_page_config(layout="centered", page_icon="🚗",
                   page_title="YouTube Comment Analyzer")

menu = option_menu(None, ["Home", "Request", 'Settings'],
                   icons=['house', 'cloud-plus', 'gear'],
                   menu_icon="cast", default_index=0, orientation="horizontal")

st.header("📊 Senty")
app.space(2)

if menu == "Home":
    home.home()
elif menu == "Request":
    request.request()
app.space(2)
