import streamlit as st
from stlib import _0_header
from stlib import _1_home
from stlib import _2_catalogue
from stlib import _3_analysis


_0_header.run()

if "home" not in st.session_state:
    st.session_state["home"] = True

if "catalogue" not in st.session_state:
    st.session_state["catalogue"] = False

if st.session_state["home"]:
    _1_home.run()

if st.session_state["catalogue"]:
    if "catalogue_first_run" not in st.session_state:
        st.session_state["catalogue_first_run"] = True
    _2_catalogue.run()
