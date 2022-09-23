import streamlit as st
from utils import app
from utils import sb
from utils import switch_page


def _get_video_ids(make, model, trim, year, form_previews, count=False):
    """
    Get `available_video_ids` from current user selection in form

    If `count=True`, function returns # of `available_video_ids`
    This is called to update the form-button text which previews the #

    If `count=False`, function returns `array` with `available_video_ids`
    This is called to update the state `available_video_ids`, which is used
    to the display catalogue in `_1_Select.py`
    """
    car_ids = sb.get_car_id(make, model, trim, year, form_previews)
    available_video_ids = []
    if (isinstance(car_ids, int)):
        for video_id in sb.get_video_ids_for_car_id(car_ids):
            available_video_ids.append(video_id)
    else:
        for car_id in car_ids:
            for video_id in sb.get_video_ids_for_car_id(car_id):
                available_video_ids.append(video_id)
    if (count):
        return str(len(available_video_ids))
    return available_video_ids


def display(select_page=True):
    """
    Display form
    """
    preview = {"make": "Any make", "model": "Any model",
               "trim": "Any trim", "year": "Any year"}

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

        form_previews = {"make": "Any make", "model": "Any model",
                         "trim": "Any trim", "year": "Any year"}

        makes = sb.get_makes()
        makes.insert(0, form_previews["make"])
        make = col1.selectbox("Make", makes, key="make_selected")

        models = sb.get_models(make)
        models.insert(0, form_previews["model"])
        model = col2.selectbox("Model", models)

        trims = sb.get_trim(make, model)
        trims.insert(0, form_previews["trim"])
        trim = col3.selectbox("Trim", trims)

        years = sb.get_year(make, model, trim)
        years.insert(0, form_previews["year"])
        year = col4.selectbox("Year", years)
        app.space(1)

    if (make != "" and make != form_previews["make"]):
        num_videos = _get_video_ids(make, model, trim, year, preview, True)
    else:
        num_videos = ""
    button = st.button("See all {} videos".format(num_videos))

    app.space(1)

    if button:
        if (make == "" or make == form_previews["make"]):
            st.warning("Please select a Make")
        else:
            st.session_state["available_video_ids"] = _get_video_ids(
                make, model, trim, year, preview)
            if not select_page:
                switch_page.run("select")
