import streamlit as st
from utils import app
from utils import sb
from stlib import _x_button_clicked
from stlib import _x_button_set_text
import time


# -----------------------------------------------------------------------

# Sidebar

def sidebar():
    with st.sidebar:
        makes = sb.get_makes()
        makes.insert(0, "Make")
        if st.session_state["car_selected"] and st.session_state["catalogue_first_run"]:
            index = makes.index(st.session_state["car_selected"]["make"])
            st.session_state.makes = makes[index]
        make = st.selectbox("Select Make", makes, key='makes')

        models = sb.get_models(make)
        models.insert(0, "Model")
        if st.session_state["car_selected"] and st.session_state["catalogue_first_run"]:
            index = models.index(st.session_state["car_selected"]["model"])
            st.session_state.models = models[index]
        model = st.selectbox("Select Model", models, key='models')

        trims = sb.get_trim(make, model)
        trims.insert(0, "Trim")
        if st.session_state["car_selected"] and st.session_state["catalogue_first_run"]:
            index = trims.index(st.session_state["car_selected"]["trim"])
            st.session_state.trims = trims[index]
        trim = st.selectbox("Select Trim", trims, key='trims')

        years = sb.get_year(make, model, trim)
        years.insert(0, "Year")
        if st.session_state["car_selected"] and st.session_state["catalogue_first_run"]:
            index = years.index(st.session_state["car_selected"]["year"])
            st.session_state.years = years[index]
        year = st.selectbox("Select Year", years, key='years')
        app.space(1)

        _x_button_set_text.run(make, model, trim, year)

        button = st.button("See all {} videos".format(
            st.session_state["video_count"]))
        app.space(1)

        if button:
            _x_button_clicked.run(make, model, trim, year)


# -----------------------------------------------------------------------

# Tile (helper function)

def _catalogue_tile(video_id, meta):
    col1, col2, col3, col4, col5 = st.columns([2, 2.2, 1.1, 1.1, 1.1])
    col1.image(meta["thumbnail_url"], width=180)
    col2.metric(label="Channel", value=meta["channel_title"])
    col3.metric(label="Views", value=app.human_format(
        int(meta["view_count"])))
    col4.metric(label="Comments", value=app.human_format(
        int(meta["comment_count"])))
    col5.text("")
    selected_add = col5.button("View Analysis", key=video_id + "_add")

    if selected_add:
        if "video_ids_selected" not in st.session_state:
            st.session_state["video_ids_selected"] = []
        st.session_state["video_ids_selected"].append(video_id)
        st.session_state["catalogue"] = False
        st.session_state["analysis"] = True
        print(st.session_state["video_ids_selected"])
        print(st.session_state["catalogue"])
        print(st.session_state["analysis"])
        print("")
        st.experimental_rerun()

    # selected_add = col5.button('View Analysis', key=video_id + "_add")
    # if selected_add and video_id not in st.session_state['video_ids_selected']:
    #     st.session_state['video_ids_selected'].append(video_id)

    # TODO: Switch page if button clicked

# -----------------------------------------------------------------------

# Catalogue


def catalogue():
    for video_id in st.session_state["available_video_ids"]:
        _catalogue_tile(video_id, sb.get_meta(video_id))
        app.space(2)


# -----------------------------------------------------------------------

# Run

def run():
    if st.session_state["catalogue_first_run"]:
        with st.spinner("Loading..."):
            time.sleep(1)
    sidebar()
    catalogue()
    st.session_state["catalogue_first_run"] = False


if __name__ == "__main__":
    run()
