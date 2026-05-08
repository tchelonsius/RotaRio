import pandas as pd
import geopandas as gpd 
from shapely.geometry import Point
from shapely import wkt




class BusRouteFinder():
    def __init__(self) -> None:
        pass
    def find_close_routes(self,arr: list, gdf_shapes):
        """get user cords on the map"""

        lgn = arr[0]
        lat = arr[1]
        destiny = Point(lgn, lat)
        """-------------------------"""

        gdf_destiny = gpd.GeoSeries([destiny], crs='EPSG:4326')

        gdf_shapes_meters = gdf_shapes.to_crs("EPSG:31983")
        destiny_meters = gdf_destiny.to_crs("EPSG:31983").iloc[0]

        """create 300m buffer from destiny point to find close routes"""

        buffer = destiny_meters.buffer(300)

        close_routes = gdf_shapes_meters[gdf_shapes_meters.intersects(buffer)]

        return close_routes
    
    def find_bus(self, df_matching_rt, close_routes):
        shape_ids = close_routes["shape_id"]
        # look for matchs in shape id from close routes to shape id from mathing_rt(routes and trips)
        buses = df_matching_rt[df_matching_rt["shape_id"].isin(shape_ids)]
        
        return buses

    def find_secure_route(self, gdf_relevant, close_routes):
        # change the crs to be equal
        gdf_relevant = gdf_relevant.to_crs(
        close_routes.crs
    )
        gdf_peso = gdf_relevant[["peso_log", "geometry"]]

        #get the intersections and sums the pesos_log 

        intersections = gpd.sjoin(close_routes, gdf_relevant, predicate="intersects")
        risk_scores = (intersections.groupby("shape_id")["peso_log"].sum().reset_index())
        
        #return the routes with theyr respective score
        secure_routes = close_routes.merge(risk_scores, on="shape_id")

        #sort for the safest order
        secure_routes = secure_routes.sort_values("peso_log")

        return secure_routes



    