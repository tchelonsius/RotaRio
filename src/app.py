from src.secure_route_finder import BusRouteFinder
from src.get_data_bus import get_data_bus
from src.pipeline import run_pipeline

import streamlit as st
import folium
from streamlit_folium import st_folium

#get bus data before starts
bus_data = get_data_bus()
gdf_shapes = bus_data["gdf_shapes"]
df_matching_rt = bus_data["df_matching_rt"]


mapa = folium.Map(
    location=[-22.90, -43.20],
    zoom_start=11
)

map_data = st_folium(
    mapa,
    width=700,
    height=500
)

st.write(map_data)

if map_data["last_clicked"]:

    lat = map_data["last_clicked"]["lat"]
    lng = map_data["last_clicked"]["lng"]

    st.write(lat, lng)