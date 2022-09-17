import streamlit as st
from utils import sb


# -----------------------------------------------------------------------

# Get defined feature list

def get_defined_feature_list():
    feature_list = ["rim", "steering wheel", "engine", "color", "colour", "carbon", "light", "design", "sound", "interior", "exterior", "mirror", "body", "brake", "chassis", "suspension",
                    "gearbox", "navigation", "infotainment", "power", "acceleration", "handling", "range", "battery", "screen", "styling", "safety", "speed", "sustainability", "connectivity"]
    return feature_list


# -----------------------------------------------------------------------

# Get car info from video_id

def get_car_info(video_id):
    car_info = sb.get_car_from_video_id(video_id)
    car_info_string = car_info["make"] + " " + \
        car_info["model"] + " (" + \
        video_id + ")"
    # car_info_string = car_info["make"] + " " + \
    #     car_info["model"] + " " + \
    #     car_info["trim"] + " " + \
    #     str(car_info["year"]) + " (" + \
    #     video_id + ")"
    return car_info_string


# -----------------------------------------------------------------------

# Add single line space to streamlit frontend

def space(num_lines=1):
    for _ in range(num_lines):
        st.write("")


# -----------------------------------------------------------------------

# Turn numbers into human readable format e.g., 2.9M

def human_format(num):
    num = float('{:.3g}'.format(num))
    magnitude = 0
    while abs(num) >= 1000:
        magnitude += 1
        num /= 1000.0
    return '{}{}'.format('{:f}'.format(num).rstrip('0').rstrip('.'), ['', 'K', 'M', 'B', 'T'][magnitude])
