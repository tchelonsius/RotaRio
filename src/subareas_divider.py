"""
ESSE ARQUIVO É RESPONSÁVEL POR LER OS DADOS COM OS LIMITES DO RIO DE JANEIRO
E DIVIDÍ-LO EM SUBÁREAS HEXÁGONAIS COM ~0.1Km², QUE VÃO SER ARMAZENADAS EM
no geodataframe gdf_hex.
"""

import json
import h3
import folium
import geopandas as gpd
from shapely.geometry import Polygon, mapping

limites_path = r"C:\Users\marce\Documents\UFRJ\Analytica - Processo Seletivo\Limite_do_MunicADpio_do_Rio_de_Janeiro.geojson"


def gera_subareas_rj(path):
    print("\n--- DEFININDO SUBÁREAS PARA OS LIMITES DO RIO DE JANEIRO...\n")
    # 1. Carregar o GeoJSON do município
    gdf = gpd.read_file(path)

    # 2. Unir todas as features em um único polígono (caso haja múltiplas)
    municipio = gdf.union_all()  # ou gdf.unary_union em versões antigas

    # 3. Converter o polígono para o formato GeoJSON que o H3 entende
    geojson_municipio = mapping(municipio)

    # 4. Preencher o município com hexágonos H3 na resolução 9 (~174m)
    hexagonos = h3.geo_to_cells(geojson_municipio, res=9)
    # print(f"Total de hexágonos: {len(hexagonos)}")

    # 5. Converter cada hexágono em um polígono Shapely
    def hex_to_polygon(hex_id):
        coords = h3.cell_to_boundary(hex_id)  # retorna [(lat, lon), ...]
        # Shapely usa (lon, lat), então invertemos
        return Polygon([(lon, lat) for lat, lon in coords])

    poligonos = [hex_to_polygon(h) for h in hexagonos]

    # 6. Criar um GeoDataFrame com os hexágonos
    gdf_hex = gpd.GeoDataFrame(
        {"hex_id": list(hexagonos)},
        geometry=poligonos,
        crs="EPSG:4326"
    )

    print("ÁREAS DEFINIDAS!\n")

    return gdf_hex


""" CRIAÇÃO DE MAPA PARA VISUALIZAÇÃO """
# # 7. Visualizar com Folium
# bounds = gdf.total_bounds
# m = folium.Map(location=[-22.9, -43.2], zoom_start=10)
#
# folium.GeoJson(
#     gdf_hex.__geo_interface__,
#     name="Hexágonos H3 (res=9)",
#     style_function=lambda f: {
#         "color": "#e63946",
#         "weight": 0.5,
#         "fillColor": "#457b9d",
#         "fillOpacity": 0.3,
#     }
# ).add_to(m)
#
# # Contorno do município por cima
# folium.GeoJson(
#     gdf.__geo_interface__,
#     name="Limite do Município",
#     style_function=lambda f: {
#         "color": "#000000",
#         "weight": 2,
#         "fillOpacity": 0,
#     }
# ).add_to(m)
#
# folium.LayerControl().add_to(m)
# m.fit_bounds([[bounds[1], bounds[0]], [bounds[3], bounds[2]]])
# m.save("mapa_hex_rio.html")