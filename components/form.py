import streamlit as st
from utils import app
from database import db
from utils import switch_page


def _get_previews():
    """
    Return dict with previews for form preview values
    """
    return {"make": "Any make", "model": "Any model", "trim": "Any trim", "year": "Any year"}


def get_car_ids(make, model, form_previews, trim="", year=""):
    return db.get_car_id(make, model, trim, year, form_previews)


def get_available_video_ids(make, model, trim, year, form_previews):
    car_ids = db.get_car_id(make, model, trim, year, form_previews)
    available_video_ids = []
    if (isinstance(car_ids, int)):
        for video_id in db.get_video_ids_for_car_id(car_ids):
            available_video_ids.append(video_id)
    else:
        for car_id in car_ids:
            for video_id in db.get_video_ids_for_car_id(car_id):
                available_video_ids.append(video_id)
    return available_video_ids


def get_num_comments_for_car_id(make, model, trim, year, form_previews):
    """
    Get `available_video_ids` from current user selection in form

    If `count=True`, function returns # of `available_video_ids`
    This is called to update the form-button text which previews the #

    If `count=False`, function returns `array` with `available_video_ids`
    This is called to update the state `available_video_ids`, which is used
    to the display catalogue in `_1_Select.py`
    """
    car_ids = db.get_car_id(make, model, trim, year, form_previews)
    num_comments = 0
    if isinstance(car_ids, int):
        car_id = car_ids
        num_comments += db.get_num_comments_for_car_id(car_id)
    else:
        for car_id in car_ids:
            num_comments += db.get_num_comments_for_car_id(car_id)
    return app.human_format(num_comments)


def get_button_num_comments(make, model, preview, trim="", year="", previews=_get_previews()):
    """
    Return number of comments based on current selection
    """
    if (make != "" and make != previews["make"]):
        num_comments = get_num_comments_for_car_id(
            make, model, trim, year, preview)
    else:
        num_comments = ""
    return num_comments


def setup(select_page=True):
    """
    Display form
    """
    preview = _get_previews

    if "car_selected" not in st.session_state:
        st.session_state["car_selected"] = {
            "make": preview["make"],
            "model": preview["model"],
            "trim": preview["trim"],
            "year": preview["year"]
        }

    with st.container():
        col1, col2 = st.columns(2)
        col3, col4 = st.columns(2)

        previews = {"make": "Any make", "model": "Any model",
                    "trim": "Any trim", "year": "Any year"}

        makes = db.get_makes()
        makes.insert(0, previews["make"])
        make = col1.selectbox("Make", makes, key="make_selected")

        models = db.get_models(make)
        models.insert(0, previews["model"])
        model = col2.selectbox("Model", models)

        trims = db.get_trim(make, model)
        trims.insert(0, previews["trim"])
        trim = col3.selectbox("Trim", trims)

        years = db.get_year(make, model, trim)
        years.insert(0, previews["year"])
        year = col4.selectbox("Year", years)
        app.space(1)

    app.space(1)

    button = st.button("See all {} videos".format(
        get_button_num_comments(make, model, trim, year, preview)))

    if button:
        if (make == "" or make == previews["make"]):
            st.warning("Please select a Make")
        else:
            st.session_state["available_video_ids"] = get_num_comments_for_car_id(
                make, model, trim, year, preview)
            if not select_page:
                switch_page.switch_page("select")
