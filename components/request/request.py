from utils import app
import streamlit as st


# -----------------------------------------------------------------------

# Request car/video to be added to app

def request():
    app.space(1)
    with st.form(key='my_form'):
        st.write("Request to add a new car and/or video")
        make_r = st.text_input('Make')
        model_r = st.text_input('Model')
        trim_r = st.text_input('Trim')
        year_r = st.text_input('Year')
        url_r = st.text_input('YouTube URL')
        submit_button = st.form_submit_button(label='Submit request')
        if submit_button:
            if make_r != "" and model_r != "" and trim_r != "" and year_r != "" and url_r != "":
                st.write("Request successfully submitted.")
                print(make_r, model_r, trim_r, year_r, url_r)
            else:
                st.write("Form is not ready to submit. Please re-check your form.")