import streamlit as st
from utils import app
from database import db


def display_edit_box():
    """
    Display edit box
    """
    def _edit_tile(make, model, comment_count):
        """
        Display edit tile for each car_id
        """
        # TODO: Cache this for all cars
        col1, col2, col3 = st.columns(
            [2, 1, 1])

        col1.write("")
        col1.write("{} {}".format(make, model))

        col2.write("")
        col2.write(comment_count + " comments")

        # delete
        remove = col3.button('Remove', key=str(make + " " + model) + "_remove")
        if remove:
            if make in st.session_state['cars'].keys():
                if model in st.session_state['cars'][make].keys():
                    print("TODO: REMOVE ", make, model)
                    st.session_state['cars'][make].pop(model)
                if len(st.session_state['cars'][make].keys()) == 0:
                    st.session_state['cars'].pop(make)
            st.experimental_rerun()
        # if (remove and car_id in st.session_state["car_ids"][make][model]):
        #     st.session_state['car_ids_selected'].remove(car_id)
        #     print(st.session_state['car_ids_selected'])
        #     st.experimental_rerun()

            # if car_id not in st.session_state["car_ids"][make][model]:
            # st.session_state["car_ids"][make][model][car_id] = sb.get_num_comments_for_car_id(
            #     car_id)

    if len(st.session_state["cars"]) > 0:
        with st.expander("Edit selection ⚙️ 🚗", expanded=True):
            for make in st.session_state['cars'].keys():
                for model in st.session_state['cars'][make].keys():
                    _edit_tile(
                        make,
                        model,
                        app.human_format(db.get_num_comments_for_make_and_model(make, model)))
