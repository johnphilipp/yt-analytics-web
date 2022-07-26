import streamlit as st
from database import db


def get_defined_feature_list():
    """
    Get defined feature list
    """
    feature_list = ["rim", "steering wheel", "engine", "color", "colour", "carbon", "light", "design", "sound", "interior", "exterior", "mirror", "body", "brake", "chassis", "suspension",
                    "gearbox", "navigation", "infotainment", "power", "acceleration", "handling", "range", "battery", "screen", "styling", "safety", "speed", "sustainability", "connectivity"]
    return feature_list


def get_car_info_from_car_id(car_id):
    """
    Get car info from car_id
    """
    car_info = db.get_car_from_car_id(car_id)
    car_info_string = car_info["make"] + " " + car_info["model"]
    return car_info_string


def get_car_make(video_id):
    """
    Get car info from video_id
    """
    car_info = db.get_car_from_car_id(video_id)
    car_info_string = car_info["make"]
    return car_info_string


def get_car_make_and_model_from_car_id(car_id):
    """
    Get car info from car_id
    """
    car_info = db.get_car_from_car_id(car_id)
    car_info_string = car_info["make"] + " " + car_info["model"]
    return car_info_string


def space(num_lines=1):
    """
    Add single line space to streamlit frontend
    """
    for _ in range(num_lines):
        st.write("")


def human_format(num):
    """
    Turn numbers into human readable format e.g., 2.9M
    """
    num = float('{:.3g}'.format(num))
    magnitude = 0
    while abs(num) >= 1000:
        magnitude += 1
        num /= 1000.0
    return '{}{}'.format('{:f}'.format(num).rstrip('0').rstrip('.'), ['', 'K', 'M', 'B', 'T'][magnitude])
