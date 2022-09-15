import streamlit as st
from utils import app
from utils import sb
import time


# -----------------------------------------------------------------------

# Sidebar

def sidebar():
    print(st.session_state["car_selected"])
    with st.sidebar:
        makes = sb.get_makes()
        if st.session_state["car_selected"] and st.session_state["catalogue_first_run"]:
            index = makes.index(st.session_state["car_selected"]["make"])
            st.session_state.makes = makes[index]
        makes.insert(0, "Make")
        make = st.selectbox("Select Make", makes, key='makes')

        models = sb.get_models(make)
        if st.session_state["car_selected"] and st.session_state["catalogue_first_run"]:
            index = models.index(st.session_state["car_selected"]["model"])
            st.session_state.models = models[index]
        models.insert(0, "Model")
        model = st.selectbox("Select Model", models, key='models')

        trims = sb.get_trim(make, model)
        if st.session_state["car_selected"] and st.session_state["catalogue_first_run"]:
            index = trims.index(st.session_state["car_selected"]["trim"])
            st.session_state.trims = trims[index]
        trims.insert(0, "Trim")
        trim = st.selectbox("Select Trim", trims, key='trims')

        years = sb.get_year(make, model, trim)
        if st.session_state["car_selected"] and st.session_state["catalogue_first_run"]:
            index = years.index(st.session_state["car_selected"]["year"])
            st.session_state.years = years[index]
        years.insert(0, "Year")
        year = st.selectbox("Select Year", years, key='years')
        app.space(1)

        button = st.button("See all {} videos".format(
            st.session_state["video_count"]))
        app.space(1)

        if button:
            if (make == "" or make == "Make"):
                st.markdown("ℹ️ Please select a *Make* first")
                button = False
            elif (make != "" and make != "Make") and (model != "" and model != "Model") and (trim != "" and trim != "Trim") and (year != "" and year != "Year"):
                st.session_state["car_selected"] = {
                    "make": make,
                    "model": model,
                    "trim": trim,
                    "year": year
                }
                car_id = sb.get_car_id(make, model, trim, year)
                available_video_ids = sb.get_video_ids_for_car_id(car_id)
                st.session_state["video_ids_selected"] = available_video_ids
                st.session_state["home"] = False
                st.session_state["catalogue"] = True
                st.experimental_rerun()

            st.session_state["catalogue_first_run"] = False


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
    selected_add = col5.button('Add to Analysis', key=video_id + "_add")
    if selected_add and video_id not in st.session_state['video_ids_selected']:
        st.session_state['video_ids_selected'].append(video_id)

# -----------------------------------------------------------------------

# Catalogue


def catalogue():
    for video_id in st.session_state["video_ids_selected"]:
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


if __name__ == "__main__":
    run()
