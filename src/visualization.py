import folium
import branca.colormap as cm

def visualizacao_hexagonos(gdf):
    """ CRIAÇÃO DE MAPA PARA VISUALIZAÇÃO """
    # 7. Visualizar com Folium
    bounds = gdf.total_bounds
    m = folium.Map(location=[-22.9, -43.2], zoom_start=10)

    folium.GeoJson(
        gdf.__geo_interface__,
        name="Hexágonos H3 (res=8)",
        style_function=lambda f: {
            "color": "#e63946",
            "weight": 0.5,
            "fillColor": "#457b9d",
            "fillOpacity": 0.3,
        }
    ).add_to(m)

    # Contorno do município por cima
    folium.GeoJson(
        gdf.__geo_interface__,
        name="Limite do Município",
        style_function=lambda f: {
            "color": "#000000",
            "weight": 2,
            "fillOpacity": 0,
        }
    ).add_to(m)

    folium.LayerControl().add_to(m)
    m.fit_bounds([[bounds[1], bounds[0]], [bounds[3], bounds[2]]])
    m.save("../mapas/mapa_hex_rio.html")

def visualizacao_crimes(gdf, gdf_resultado, coluna="peso_log", nome_arquivo=""):
    """ VISUALIZAÇÃO """
    m = folium.Map(location=[-22.9, -43.2], zoom_start=10)

    peso_max = gdf_resultado[coluna].max()
    colormap = cm.linear.YlOrRd_09.scale(0, peso_max)

    def estilo(feature):
        peso = feature["properties"][coluna]
        return {
            "color": "#333333",
            "weight": 0.3,
            "fillColor": colormap(peso),
            "fillOpacity": 0.7,
        }

    folium.GeoJson(
        gdf_resultado.__geo_interface__,
        name=coluna,
        style_function=estilo,
        tooltip=folium.GeoJsonTooltip(fields=["hex_id", "peso_bruto", "peso_suavizado", "peso_log"]),
    ).add_to(m)

    # Contorno do município por cima
    folium.GeoJson(
        gdf.__geo_interface__,
        name="Limite do Município",
        style_function=lambda f: {
            "color": "#000000",
            "weight": 2,
            "fillOpacity": 0,
        }
    ).add_to(m)

    colormap.caption = f"Peso {coluna} de Crimes"
    colormap.add_to(m)
    folium.LayerControl().add_to(m)
    m.save(f"../mapas/{nome_arquivo}")