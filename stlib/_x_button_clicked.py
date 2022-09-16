import streamlit as st
from utils import sb


def _button_clicked(make, model, trim, year):
    if "available_video_ids" not in st.session_state:
        st.session_state["available_video_ids"] = []

    if (make == "" or make == "Make"):
        st.markdown("ℹ️ Please select a *Make* first")
        button = False

    elif (make != "" and make != "Make") and (model != "" and model != "Model") and (trim != "" and trim != "Trim") and (year != "" and year != "Year"):
        # Everythung entered
        st.session_state["car_selected"] = {
            "make": make,
            "model": model,
            "trim": trim,
            "year": year
        }
        car_id = sb.get_car_id(make, model, trim, year)
        available_video_ids = sb.get_video_ids_for_car_id(car_id)
        st.session_state["available_video_ids"] = available_video_ids
        st.session_state["home"] = False
        st.session_state["catalogue"] = True
        st.experimental_rerun()

    elif (make != "" and make != "Make") and (model != "" and model != "Model") and (trim != "" and trim != "Trim"):
        # YEAR not entered
        st.session_state["car_selected"] = {
            "make": make,
            "model": model,
            "trim": trim,
            "year": "Year"
        }
        available_car_ids = sb.get_cars_ids_for_make_model_trim(
            make, model, trim)
        available_video_ids = []
        for car_id in available_car_ids:
            for video_id in sb.get_video_ids_for_car_id(car_id):
                available_video_ids.append(video_id)
        st.session_state["available_video_ids"] = available_video_ids
        st.session_state["home"] = False
        st.session_state["catalogue"] = True
        st.experimental_rerun()

    elif (make != "" and make != "Make") and (model != "" and model != "Model"):
        # TRIM and YEAR not entered
        st.session_state["car_selected"] = {
            "make": make,
            "model": model,
            "trim": "Trim",
            "year": "Year"
        }

        available_car_ids = sb.get_cars_ids_for_make_model(make, model)
        available_video_ids = []
        for car_id in available_car_ids:
            for video_id in sb.get_video_ids_for_car_id(car_id):
                available_video_ids.append(video_id)
        st.session_state["available_video_ids"] = available_video_ids
        st.session_state["home"] = False
        st.session_state["catalogue"] = True
        st.experimental_rerun()

    elif (make != "" and make != "Make"):
        # MODEL, TRIM and YEAR not entered
        st.session_state["car_selected"] = {
            "make": make,
            "model": "Model",
            "trim": "Trim",
            "year": "Year"
        }

        available_car_ids = sb.get_cars_ids_for_make(make)
        available_video_ids = []
        for car_id in available_car_ids:
            for video_id in sb.get_video_ids_for_car_id(car_id):
                available_video_ids.append(video_id)
        st.session_state["available_video_ids"] = available_video_ids
        st.session_state["home"] = False
        st.session_state["catalogue"] = True
        st.experimental_rerun()


# -----------------------------------------------------------------------

# Run

def run(make, model, trim, year):
    _button_clicked(make, model, trim, year)


if __name__ == "__main__":
    run()
