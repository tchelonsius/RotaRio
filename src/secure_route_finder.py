import pandas as pd
import geopandas as gpd 
from shapely.geometry import Point
from shapely import wkt




class BusRouteFinder():
    def __init__(self) -> None:
        pass

    #find close bus routes from the destiny cords from the arr parameter
    def find_close_routes(self,arr: list, gdf_shapes):

        #get user cords on the map

        lgn = arr[0]
        lat = arr[1]
        destiny = Point(lgn, lat)
        print(f'DESTINY POINTS:[lon:"{lgn}", lat:"{lat}"]')

        #match the crs

        gdf_destiny = gpd.GeoSeries([destiny], crs='EPSG:4326')

        gdf_shapes_meters = gdf_shapes.to_crs("EPSG:31983")
        destiny_meters = gdf_destiny.to_crs("EPSG:31983").iloc[0]

        #create 300m buffer wich grows until find routes

        buffer300 = destiny_meters.buffer(300)
        close_routes = gdf_shapes_meters[gdf_shapes_meters.intersects(buffer300)]
        if not close_routes.empty:
            print("found in 300m buffer")
            return close_routes

        # 500m
        buffer500 = destiny_meters.buffer(500)
        close_routes = gdf_shapes_meters[gdf_shapes_meters.intersects(buffer500)]
        if not close_routes.empty:
            print("found in 500m buffer")
            return close_routes

        # 1000m
        buffer1000 = destiny_meters.buffer(1000)
        close_routes = gdf_shapes_meters[gdf_shapes_meters.intersects(buffer1000)]
        if not close_routes.empty:
            print("found in 1000m buffer")
            return close_routes

        print("nao foram achadas rotas em um raio de 1km de proximidade")
        return close_routes  # returns empty
    
    #the parameter should receive the secure routes if you desire to find the busses of the secure routes
    def find_bus(self, df_matching_rt, routes):
        shape_ids = routes["shape_id"]
        # look for matchs in shape id from close routes to shape id from mathing_rt(routes and trips)
        buses = df_matching_rt[df_matching_rt["shape_id"].isin(shape_ids)]

        #dropping duplicates
        buses = buses.drop_duplicates(subset=["route_id", "shape_id"])
        
        return buses

    
    def find_secure_route(self, gdf_relevant, close_routes):
        # change the crs to be equal   
        gdf_relevant = gdf_relevant.to_crs(close_routes.crs)

        #get the intersections and sums the pesos_log 

        intersections = gpd.sjoin(close_routes, gdf_relevant, predicate="intersects")
        risk_scores = (intersections.groupby("shape_id")["peso_log"].sum().reset_index())
        print("created the risk scores")
        
        #return the routes with theyr respective score
        secure_routes = close_routes.merge(risk_scores, on="shape_id")

        #sort for the safest order
        secure_routes = secure_routes.sort_values("peso_log")

        return secure_routes



    