import streamlit as st
from components import header
from utils.video import Video
from utils import app
from utils.add_data import get_content, get_meta, get_sentiment, post_content, post_meta, post_sentiment


def request():
    """
    Request car/video to be added to app

    TODO: Cancel if video_id already in meta
    """
    with st.form(key='my_form'):
        st.write("Request to add a new Car/Video")
        make = st.text_input("Make")
        model = st.text_input("Model")
        trim = st.text_input("Trim")
        year = st.text_input("Year")
        url = st.text_input("YouTube URL")
        app.space(1)
        submit_button = st.form_submit_button(label='Submit request')
        if submit_button:
            if make != "" and model != "" and trim != "" and year != "" and url != "":
                print(make, model, trim, year, url)
                video = Video(str(make),
                              str(model),
                              str(trim),
                              str(year),
                              str(url))

                st.success(
                    "Processing {} {}. Requests usually take no more than 5 minutes.".format(make, model))

                st.markdown(
                    "\n1) Get *meta data*")
                meta = get_meta(video)
                st.markdown(
                    "\n2) Scrape *content*")
                content = get_content(video)
                st.markdown(
                    "\n3) Calcualte *sentiment*")
                sentiment = get_sentiment(video, content)

                st.markdown(
                    "\n4) Push *meta data* for {} {} to database".format(make, model))
                post_meta(video, meta)
                st.markdown(
                    "\n5) Push *content* for {} {} to database".format(make, model))
                post_content(video, content)
                st.markdown(
                    "\n6) Push *sentiment* for {} {} to database".format(make, model))
                post_sentiment(video, sentiment)

                st.success("Successfully added {} {}.".format(make, model))
            else:
                st.warning(
                    "Form is not ready to be submitted. All fields need to be filled out.")


def run():
    header.display()

    with open("style/main.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

    request()


if __name__ == "__main__":
    run()
