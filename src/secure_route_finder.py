import pandas as pd
import geopandas as gpd 
from shapely.geometry import Point
from shapely import wkt




class SecureRouteFinder():
    def __init__(self, gdf_shapes, df_trips, df_routes) -> None:
        self.gdf_shapes = gdf_shapes
        self.df_trips = df_trips
        self.df_routes = df_routes
    def find_close_routes(self,arr: list):
        """get user cords on the map"""

        lgn = arr[0]
        lat = arr[1]
        destiny = Point(lgn, lat)
        """-------------------------"""

        gdf_destiny = gpd.GeoSeries([destiny], crs='EPSG:4326')

        gdf_shapes_meters = self.gdf_shapes.to_crs("EPSG:31983")
        destiny_meters = gdf_destiny.to_crs("EPSG:31983").iloc[0]

        """create 300m buffer from destiny point to find close routes"""

        buffer = destiny_meters.buffer(300)

        close_routes = gdf_shapes_meters[gdf_shapes_meters.intersects(buffer)]

        return close_routes
    
    def find_bus(self,close_routes):


