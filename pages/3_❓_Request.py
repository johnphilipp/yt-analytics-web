import streamlit as st
from components import header
from utils import app


def request():
    """
    Request car/video to be added to app
    """
    st.warning("Not yet functional")
    with st.form(key='my_form'):
        st.write("Request to add a new Car/Video")
        make_r = st.text_input("Make")
        model_r = st.text_input("Model")
        trim_r = st.text_input("Trim")
        year_r = st.text_input("Year")
        url_r = st.text_input("YouTube URL")
        app.space(1)
        submit_button = st.form_submit_button(label='Submit request')
        if submit_button:
            if make_r != "" and model_r != "" and trim_r != "" and year_r != "" and url_r != "":
                print(make_r, model_r, trim_r, year_r, url_r)
                st.success(
                    "Thank you for your request. Request usually take no more than 5 minutes to appear on the *Select* page.")
            else:
                st.warning(
                    "Form is not ready to be submitted. All fields need to be filled out.")


def run():
    header.display()
    request()


if __name__ == "__main__":
    run()
