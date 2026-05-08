import pandas as pd
import geopandas as gpd 
from shapely import wkt
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

def get_data_bus():
    print('getting routes data')
    df_routes = pd.read_csv(BASE_DIR / "routes.csv")
    df_routes_info = df_routes[['route_long_name', 'route_short_name','route_desc','route_id', 'route_color']]

    print('getting trips data')
    df_trips = pd.read_csv(BASE_DIR / "trips.csv")
    df_trips_info = df_trips[['route_id', 'shape_id',  'trip_id', 'trip_headsign', 'trip_short_name', 'direction_id', 'service_id' ]]

    df_matching = df_routes_info.merge(df_trips_info, on="route_id")

    print("getting shapes data")
    df_shapes = pd.read_csv(BASE_DIR / "shapes_geom.csv")
    df_shapes["shape_id"] = df_shapes['shape_id'].astype("category")
    df_shapes_info = df_shapes[['shape_id','shape','shape_distance','start_pt','end_pt']]


    df_shapes_info["shape"] = (
    df_shapes_info["shape"].astype(str).apply(wkt.loads)
    )

    df_shapes_info["start_pt"] = (
        df_shapes_info["start_pt"].astype(str).apply(wkt.loads)
    )

    df_shapes_info["end_pt"] = (
        df_shapes_info["end_pt"].astype(str).apply(wkt.loads)
    )


    type(df_shapes_info["shape"].iloc[0])


    gdf_shapes = gpd.GeoDataFrame(df_shapes_info,geometry="shape")
    gdf_start_points = gpd.GeoDataFrame(df_shapes_info,geometry="start_pt")
    gdf_end_points = gpd.GeoDataFrame(df_shapes_info,geometry="end_pt")

    gdf_shapes = gdf_shapes.set_crs(epsg=4326)
    gdf_start_points = gdf_start_points.set_crs(epsg=4326)
    gdf_end_points = gdf_end_points.set_crs(epsg=4326)

    return {"gdf_shapes": gdf_shapes,
            "df_matching_rt": df_matching}


