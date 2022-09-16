import streamlit as st
from utils import sb


def _button_set_text(make, model, trim, year):
    # TODO: Merge with button clicked // Using same logic

    if (make != "" and make != "Make") and (model != "" and model != "Model") and (trim != "" and trim != "Trim") and (year != "" and year != "Year"):
        # Everythung entered
        car_id = sb.get_car_id(make, model, trim, year)
        available_video_ids = []
        for video_id in sb.get_video_ids_for_car_id(car_id):
            available_video_ids.append(video_id)
        st.session_state["video_count"] = str(len(available_video_ids))

    elif (make != "" and make != "Make") and (model != "" and model != "Model") and (trim != "" and trim != "Trim"):
        # YEAR not entered
        available_car_ids = sb.get_cars_ids_for_make_model_trim(
            make, model, trim)
        available_video_ids = []
        for car_id in available_car_ids:
            for video_id in sb.get_video_ids_for_car_id(car_id):
                available_video_ids.append(video_id)
        st.session_state["video_count"] = str(len(available_video_ids))

    elif (make != "" and make != "Make") and (model != "" and model != "Model"):
        available_car_ids = sb.get_cars_ids_for_make_model(make, model)
        available_video_ids = []
        for car_id in available_car_ids:
            for video_id in sb.get_video_ids_for_car_id(car_id):
                available_video_ids.append(video_id)
        st.session_state["video_count"] = str(len(available_video_ids))

    elif (make != "" and make != "Make"):
        # MODEL, TRIM and YEAR not entered
        available_car_ids = sb.get_cars_ids_for_make(make)
        available_video_ids = []
        for car_id in available_car_ids:
            for video_id in sb.get_video_ids_for_car_id(car_id):
                available_video_ids.append(video_id)
        st.session_state["video_count"] = str(len(available_video_ids))


# -----------------------------------------------------------------------

# Run

def run(make, model, trim, year):
    _button_set_text(make, model, trim, year)


if __name__ == "__main__":
    run()
