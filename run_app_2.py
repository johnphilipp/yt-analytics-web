# from components.select import select
# from components.analysis import analysis

# header.header()
# select.select_cars()
# analysis.view_analysis()

from components.header import header
from utils import sb
from utils import app
from components.request import request
import streamlit as st


def switch_page(page_name: str):
    from streamlit import _RerunData, _RerunException
    from streamlit.source_util import get_pages

    def standardize_name(name: str) -> str:
        return name.lower().replace("_", " ")

    page_name = standardize_name(page_name)

    # OR whatever your main page is called
    pages = get_pages("run_app.py")

    for page_hash, config in pages.items():
        if standardize_name(config["page_name"]) == page_name:
            raise _RerunException(
                _RerunData(
                    page_script_hash=page_hash,
                    page_name=page_name,
                )
            )

    page_names = [standardize_name(config["page_name"])
                  for config in pages.values()]

    raise ValueError(
        f"Could not find page {page_name}. Must be one of {page_names}")


if st.button("Switch"):
    switch_page("home")


# # -----------------------------------------------------------------------

# # 1st page -- Landingpage

# header.header()


# # -----------------------------------------------------------------------

# # 1st page -- Select cars


# select_cars()

# # # -----------------------------------------------------------------------

# # # 2nd page --


# # def _display_select(video_id, meta):
# #     col1, col2, col3, col4, col5 = st.columns([2, 2.2, 1.1, 1.1, 1.1])
# #     col1.image(meta["thumbnail_url"], width=180)
# #     col2.metric(label="Channel", value=meta["channel_title"])
# #     col3.metric(label="Views", value=app.human_format(int(meta["view_count"])))
# #     col4.metric(label="Comments", value=app.human_format(
# #         int(meta["comment_count"])))
# #     col5.text("")
# #     selected_add = col5.button('Add to Analysis', key=video_id + "_add")
# #     if selected_add and video_id not in st.session_state['video_ids_selected']:
# #         st.session_state['video_ids_selected'].append(video_id)
