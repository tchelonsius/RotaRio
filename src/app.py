from src.secure_route_finder import BusRouteFinder
from src.get_data_bus import get_data_bus
from src.pipeline import run_pipeline
# from flask import Flask, request, jsonify

# app = Flask('__name__')

# @app.route('/')
# def home():
#     return 'hello'





# if __name__ == "__main__":
#     app.run(debug=True)



import folium
print('RUNNING............')

#get bus data before starts
bus_data = get_data_bus()

gdf_shapes = bus_data["gdf_shapes"]
print(f'GDF SHAPES ="{gdf_shapes}"')

df_matching_rt = bus_data["df_matching_rt"]
print(f'MATCHING_DF = "{df_matching_rt}"')



finder = BusRouteFinder()
close_routes = finder.find_close_routes(gdf_shapes=gdf_shapes,arr=[-43.1729,-22.9068])
print(f'CLOSE ROUTES:"{close_routes}"')
busses = finder.find_bus(close_routes=close_routes,df_matching_rt=df_matching_rt)
print(f'BUSSES:"{busses}"')