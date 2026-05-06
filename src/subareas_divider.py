import h3
import geopandas as gpd
from shapely.geometry import Polygon, mapping

def gera_subareas_rj(gdf):
    print("\n--- DEFININDO SUBÁREAS PARA OS LIMITES DO RIO DE JANEIRO...\n")

    # 1. Unir todas as features em um único polígono (caso haja múltiplas)
    municipio = gdf.union_all()  # ou gdf.unary_union em versões antigas

    # 2. Converter o polígono para o formato GeoJSON que o H3 entende
    geojson_municipio = mapping(municipio)

    # 3. Preencher o município com hexágonos H3 na resolução 8 (~0,7km²)
    hexagonos = h3.geo_to_cells(geojson_municipio, res=8)
    # print(f"Total de hexágonos: {len(hexagonos)}")

    # 4. Converter cada hexágono em um polígono Shapely
    def hex_to_polygon(hex_id):
        coords = h3.cell_to_boundary(hex_id)  # retorna [(lat, lon), ...]
        # Shapely usa (lon, lat), então invertemos
        return Polygon([(lon, lat) for lat, lon in coords])

    poligonos = [hex_to_polygon(h) for h in hexagonos]

    # 5. Criar um GeoDataFrame com os hexágonos
    gdf_hex = gpd.GeoDataFrame(
        {"hex_id": list(hexagonos)},
        geometry=poligonos,
        crs="EPSG:4326"
    )

    print(f"\ndataframe com os hexágonos:\n{gdf_hex.head().to_string}\n")
    print(f"{gdf_hex.shape[0]} ÁREAS DEFINIDAS!\n")

    return gdf_hex
