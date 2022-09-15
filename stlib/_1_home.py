import streamlit as st
from utils import app
from utils import sb

#
# TODO: Add "Select all videos" button
# TODO: Add built-in video vierwer
# TODO: Animate comment numbers"
#


def _landing_page():
    col1, col2 = st.columns([1, 2.7])
    col1.markdown("")
    col1.subheader("Automotive Market Intelligence")
    col1.markdown("")
    col1.markdown(
        "✅ Learn what **Social Media** thinks about your Product Line")
    col1.markdown("✅ Extract **Sentiment Analysis** of Product Features")
    col1.markdown("✅ Benchmark against your **Competiton**")
    col1.markdown("")

    col2.image(
        "https://p-john.com/wp-content/uploads/2022/09/wallpaper.png")

    app.space(2)


def _form():
    if "video_count" not in st.session_state:
        st.session_state["video_count"] = ""

    if "car_selected" not in st.session_state:
        st.session_state["car_selected"] = []

    if "video_ids_selected" not in st.session_state:
        st.session_state["video_ids_selected"] = []

    with st.container():
        st.subheader("Select a car to get started 🚗")

        col1, col2 = st.columns(2)
        col3, col4 = st.columns(2)

        makes = sb.get_makes()
        makes.insert(0, "Make")
        make = col1.selectbox("Select Make", makes)

        models = sb.get_models(make)
        models.insert(0, "Model")
        model = col2.selectbox("Select Model", models)

        trims = sb.get_trim(make, model)
        trims.insert(0, "Trim")
        trim = col3.selectbox("Select Trim", trims)

        years = sb.get_year(make, model, trim)
        years.insert(0, "Year")
        year = col4.selectbox("Select Year", years)
        app.space(1)

    if ((make != "" and make != "Make") and (model == "" or model == "Model")):
        available_car_ids = sb.get_cars_ids_for_make(make)
        print(available_car_ids)
        available_video_ids = []
        for car_id in available_car_ids:
            for video_id in sb.get_video_ids_for_car_id(car_id):
                available_video_ids.append(video_id)
        st.session_state["video_count"] = str(len(available_video_ids))
        print("Len 1: " + st.session_state["video_count"])

    if ((make != "" and make != "Make") and (model != "" and model != "Model")):
        available_car_ids = sb.get_cars_ids_for_make_and_model(make, model)
        print(available_car_ids)
        available_video_ids = []
        for car_id in available_car_ids:
            for video_id in sb.get_video_ids_for_car_id(car_id):
                available_video_ids.append(video_id)
        st.session_state["video_count"] = str(len(available_video_ids))
        print("Len 2: " + st.session_state["video_count"])

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


# -----------------------------------------------------------------------

# Run

def run():
    _landing_page()
    _form()


if __name__ == "__main__":
    run()
