import pandas as pd
import geopandas as gpd 
from shapely.geometry import Point
from shapely import wkt




class BusRouteFinder():
    def __init__(self) -> None:
        pass

    #find close bus routes from the destination cords from the arr parameter
    def find_close_routes(self,destination: list, gdf_shapes, origin: list):
        gdf_shapes_meters = gdf_shapes.to_crs("EPSG:31983")
        
        #user cords and turns into a point and into a gpdseries
        lgn_origin = origin[0]
        lat_origin = origin[1]
        origin = Point(lgn_origin, lat_origin)
        print(f'ORIGIN POINTS: [lon:"{lgn_origin}", lat:"{lat_origin}"]')
        gdf_origin = gpd.GeoSeries([origin], crs='EPSG:4326')
        origin_meters = gdf_origin.to_crs("EPSG:31983").iloc[0]

        #destination cords and turns into a point and into a gpdseries
        lgn_dest = destination[0]
        lat_dest = destination[1]
        destination = Point(lgn_dest, lat_dest)
        print(f'DESTINATION  POINTS:[lon:"{lgn_dest}", lat:"{lat_dest}"]')
        gdf_destination = gpd.GeoSeries([destination], crs='EPSG:4326')
        destination_meters = gdf_destination.to_crs("EPSG:31983").iloc[0]

        # buffer for origin
        origin_routes = gpd.GeoDataFrame()
        for radius in [300, 500, 1000]:
            buf = origin_meters.buffer(radius)
            origin_routes = gdf_shapes_meters[gdf_shapes_meters.intersects(buf)]
            if not origin_routes.empty:
                print(f'origin found in {radius}m buffer')
                break
            else:
                print("nao foram achadas rotas em comum com a origem em um raio de 1km")
                return gdf_shapes_meters.iloc[0:0].to_crs(gdf_shapes.crs)


        # buffer for destination
        destination_routes = gpd.GeoDataFrame()
        for radius in [300, 500, 1000]:
            buf = destination_meters.buffer(radius)
            destination_routes = gdf_shapes_meters[gdf_shapes_meters.intersects(buf)]
            if not destination_routes.empty:
                print(f'destination found in {radius}m buffer')
                break
            else:
                print("nao foram achadas rotas em comum com o destino em um raio de 1km")
                return gdf_shapes_meters.iloc[0:0].to_crs(gdf_shapes.crs)
        
        # interception
        common_ids = set(origin_routes["shape_id"]) & set(destination_routes["shape_id"])
        close_routes = gdf_shapes_meters[gdf_shapes_meters["shape_id"].isin(common_ids)]
        print(f'ROTAS EM COMUM: {len(close_routes)}')
        
        close_routes = close_routes.to_crs(gdf_shapes.crs)

        return close_routes  # returns empty
    


    
    def find_bus(self, df_matching_rt, routes):
        #the parameter should receive the secure routes if you desire to find the busses of the secure routes

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



    