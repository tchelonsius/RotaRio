from src.secure_route_finder import BusRouteFinder
from src.get_data_bus import get_data_bus
from src.pipeline import run_pipeline
from flask import Flask, request, jsonify
import pandas as pd
import geopandas as gpd

app = Flask('__name__')

# run map pipeline
print('LOADING PIPELINE DATA. . .')
map_data = run_pipeline()
#get pipeline map usefull data
gdf_relevant = map_data["gdf_relevant"]


#get bus data before server starts
print("API RotaRio: LOADING BUS DATA. . .")
bus_data = get_data_bus()
#get route shapes
gdf_shapes = bus_data["gdf_shapes"]
#get bus route+trip data
df_matching_rt = bus_data["df_matching_rt"]

#initialize bus finder
router = BusRouteFinder()

# return a geoDataFrame with the secure routes + their respective busses, in order from the safest to the least safe
@app.route('/secure_bus_routes')
def secure_bus_routes():
    arr = request.args.get('arr') # get the cords from the destiny with the user
    arr = [float(x) for x in arr.split(',')] # converts str into float

    if not arr:
        return jsonify({"error": "arr param must be set,arr=[lon,lat]"}), 400
    else:
        close_routes = router.find_close_routes(arr=arr, gdf_shapes=gdf_shapes)
        secure_routes = router.find_secure_route(gdf_relevant=gdf_relevant,close_routes=close_routes)
        secure_busses = router.find_bus(df_matching_rt=df_matching_rt, routes=secure_routes)
        print("converting to json . . .")
        #retorna as rotas seguras e seus respectivos onibus em formato de dict
        return jsonify(secure_busses.to_dict(orient='records')), 200 





if __name__ == "__main__":
    app.run(debug=True, use_reloader=False)








"""bus router """
# import folium
# print('RUNNING............')





# finder = BusRouteFinder()
# close_routes = finder.find_close_routes(gdf_shapes=gdf_shapes,arr=[-43.1729,-22.9068])
# print(f'CLOSE ROUTES:"{close_routes}"')
# busses = finder.find_bus(close_routes=close_routes,df_matching_rt=df_matching_rt)
# print(f'BUSSES:"{busses}"')