import pandas as pd
import geopandas as gpd 
from shapely.geometry import Point
from shapely import wkt




class BusRouteFinder():
    def __init__(self, gdf_relevant) -> None:
        self.gdf_relevant = gdf_relevant
    def find_close_routes(self,arr: list, gdf_shapes, df_matching_rt):
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

    def find_secure_route(self, gdf_relevant):
        gdf_peso = gdf_relevant[gdf_relevant["peso_log", "geometry"]]
        return gdf_peso


    