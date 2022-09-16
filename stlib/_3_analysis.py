import streamlit as st
from utils import app
from utils import sb
from stlib import _x_button_clicked
from stlib import _x_button_set_text
from components.analysis import sentiment
from components.analysis import wcloud
from components.analysis import topflop
import streamlit as st
from streamlit_option_menu import option_menu


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

# Helper Func -- Edit tile


def _display_edit(video_id, meta):
    car_info = sb.get_car_from_video_id(video_id)
    col1, col2, col3, col4, col5 = st.columns([0.6, 3.2, 1.2, 1.2, 1.2])
    selected_remove = col1.button('-', key=video_id + "_remove")
    # Remove selected videos from list
    if selected_remove and video_id in st.session_state['video_ids_selected']:
        st.session_state['video_ids_selected'].remove(video_id)
        st.experimental_rerun()
    col2.text(car_info["make"] + " " +
              car_info["model"] + " (" +
              car_info["trim"] + ", " +
              str(car_info["year"]) + ")")
    col3.text(meta["channel_title"])
    col4.text(app.human_format(int(meta["view_count"])) + " views")
    col5.text(app.human_format(int(meta["comment_count"])) + " comments")

# -----------------------------------------------------------------------

# Main func -- View Analysis


def view_analysis():
    if len(st.session_state['video_ids_selected']) > 0:
        # st.markdown("---")
        # app.space(2)
        # st.subheader("View Analysis 📊")
        # app.space(2)

        if len(st.session_state['video_ids_selected']) > 0:
            with st.expander("Edit Selection"):
                app.space(1)
                for video_id in st.session_state['video_ids_selected']:
                    _display_edit(video_id, sb.get_meta(video_id))
        app.space(1)

        menu = option_menu(None, ["Sentiment", "Wordcloud", "Top/Flop"],
                           icons=['bar-chart', 'type', 'star-half'],
                           menu_icon="cast", default_index=0, orientation="horizontal")

        if menu == "Sentiment":
            sentiment.get_sentiment()

        elif menu == "Wordcloud":
            wcloud.get_wordcloud()

        elif menu == "Top/Flop":
            topflop.get_topflop()


def run():
    sidebar()
    view_analysis()
    st.session_state["analysis_first_run"] = False


if __name__ == "__main__":
    run()
