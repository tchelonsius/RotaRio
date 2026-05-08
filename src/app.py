from src.secure_route_finder import BusRouteFinder
from src.get_data_bus import get_data_bus
from src.pipeline import run_pipeline
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask('__name__')
CORS(app)

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

    #destination cords
    destination = request.args.get('destination') # get destiny cords
    origin = request.args.get('origin') # get user cords (origin)
    if not destination or not origin:
        return jsonify({"error": "destination param must be set, -> destination=[lon,lat]"}), 400
    else:
        destination = [float(x) for x in destination.split(',')] # converts str into float
        origin = [float(x) for x in origin.split(',')] # converts str into float

        #secure_route_finder pipeline
        close_routes = router.find_close_routes(destination=destination, gdf_shapes=gdf_shapes, origin=origin)
        if isinstance(close_routes, str) or close_routes.empty:
            return jsonify({"error": "nenhuma rota encontrada entre os dois pontos"}), 404

        secure_routes = router.find_secure_route(gdf_relevant=gdf_relevant,close_routes=close_routes)
        secure_busses = router.find_bus(df_matching_rt=df_matching_rt, routes=secure_routes)

        secure_busses = secure_busses.drop_duplicates(subset=["shape_id"])#drop duplicates

        # adiciona a geometria das rotas
        secure_busses = secure_busses.merge(
        gdf_shapes[["shape_id", "shape"]],
        on="shape_id",
        how="left"
        )

        # converte LineString para WKT string
        secure_busses["shape"] = secure_busses["shape"].apply(lambda x: x.wkt if x != "" else "")


        print("converting to json . . .")
        #retorna as rotas seguras e seus respectivos onibus em formato de dict
        secure_busses = secure_busses.fillna(value="")
        return jsonify(secure_busses.to_dict(orient='records')), 200




if __name__ == "__main__":
    app.run(debug=True, use_reloader=False)
