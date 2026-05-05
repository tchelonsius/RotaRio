import h3
import pandas as pd
import geopandas as gpd
from collections import defaultdict
import numpy as np
from subareas_divider import gera_subareas_rj

# limites_path = r"C:\Users\marce\Documents\UFRJ\Analytica - Processo Seletivo\Limite_do_MunicADpio_do_Rio_de_Janeiro.geojson"
# path_crossfire_data = r"C:\Users\marce\Documents\UFRJ\Analytica - Processo Seletivo\fc_api_occurrences_with_victims_detailed_2026-04-30T12_36_30.000Z.csv"
# df = pd.read_csv(path_crossfire_data)

# Exemplo de pesos por tipo de crime (ajuste conforme sua realidade)
PESO_TIPO = {
    "Homicidio/Tentativa": 7.0,
    "Tentativa/Roubo": 5.0,
    "Operação policial":  9.0,
    "Ação policial": 8.0,
    "tiros a esmo": 7.0,
    "Tentativa/Roubo de cargas": 6.0,
    "Não identificado": 7.0,
}

def calcula_peso_tipo(df, mapa_peso_tipo):
    # Mapear peso por tipo
    df["peso_tipo"] = df["main_reason"].map(mapa_peso_tipo).fillna(1.0)
    return df

def calcula_peso_recencia(df, t_atual, meia_vida):
    # Mapear peso por recencia da ocorrência com decaimento exponencial
    ## 1° separar data em data_timestamp, hora_timestamp e hora
    dt = pd.to_datetime(df["data"], dayfirst=True, errors="coerce")
    df["data_timestamp"] = dt.dt.normalize()
    df["hora_timestamp"] = dt.dt.time
    # df["hora"] = pd.to_datetime(df["hora_timestamp"].astype(str),errors="coerce").dt.hour
    df["hora"] = pd.to_datetime(
        df["hora_timestamp"],
        format="%d/%m/%Y, %H:%M:%S",
        errors="coerce"
    ).dt.hour
    lambda_ = np.log(2) / meia_vida
    df["peso_recencia"] = np.exp(-lambda_ * (t_atual - df["data_timestamp"]).dt.days / 365.25)
    return df

def calcula_peso_bruto(df, mapa_peso_tipo, t_atual, meia_vida):
    print("\n--- CALCULANDO PESO BRUTO (PESO_RECENCIA * PESO_TIPO)...\n")
    # Calcular Peso final
    df = calcula_peso_tipo(df, mapa_peso_tipo)
    df = calcula_peso_recencia(df, t_atual, meia_vida)
    df["peso_bruto"] = df["peso_recencia"] * df["peso_tipo"]
    print("PESOS BRUTOS CALCULADOS!\n")
    return df

def atribuir_pesos_hexagonos(gdf_hex, df_crimes, col_peso: str = "peso_bruto", resolucao_h3: int = 9, decaimento: float = 0.5, niveis_suavizacao: int = 2,):
    """
    Atribui a cada hexágono H3 um peso suavizado com base em ocorrências criminais.
    Retorna GeoDataFrame igual ao gdf_hex, com a coluna 'peso_suavizado' adicionada.
    """
    print("\n--- ATRIBUINDO PESOS PARA CADA HEXÁGONO...\n")
    # 1. Mapear cada ocorrência ao seu hexágono H3
    hex_ids_validos = set(gdf_hex["hex_id"])

    pesos_brutos: dict[str, float] = defaultdict(float)

    for _, row in df_crimes.iterrows():
        hex_id = h3.latlng_to_cell(row["latitude"], row["longitude"], resolucao_h3)
        # Só acumula se o hexágono pertence ao município
        if hex_id in hex_ids_validos:
            pesos_brutos[hex_id] += row[col_peso]

    # ------------------------------------------------------------------
    # 2. Suavização por anéis de vizinhança com decaimento
    #
    #    peso_suavizado[h] = peso_bruto[h]
    #                        + decaimento^1 * soma(peso_bruto[vizinhos anel 1])
    #                        + decaimento^2 * soma(peso_bruto[vizinhos anel 2])
    # ------------------------------------------------------------------
    pesos_suavizados: dict[str, float] = defaultdict(float)

    for hex_id in hex_ids_validos:
        # Peso próprio do hexágono
        peso_acumulado = pesos_brutos.get(hex_id, 0.0)

        # Contribuição de cada anel de vizinhança
        for nivel in range(1, niveis_suavizacao + 1):
            fator = decaimento ** nivel
            # grid_disk retorna todos os hexágonos até o raio k;
            # grid_ring retorna apenas o anel exato de distância k
            vizinhos_anel = h3.grid_ring(hex_id, nivel)

            for viz in vizinhos_anel:
                peso_acumulado += fator * pesos_brutos.get(viz, 0.0)

        pesos_suavizados[hex_id] = peso_acumulado

    # ------------------------------------------------------------------
    # 3. Incorporar os pesos ao GeoDataFrame
    # ------------------------------------------------------------------
    gdf_resultado = gdf_hex.copy()
    gdf_resultado["peso_bruto"] = gdf_resultado["hex_id"].map(
        lambda h: pesos_brutos.get(h, 0.0)
    )
    gdf_resultado["peso_suavizado"] = gdf_resultado["hex_id"].map(
        lambda h: pesos_suavizados.get(h, 0.0)
    )
    print("PESOS ATRIBUÍDOS AOS HEXÁGONOS!\n")
    return gdf_resultado

# tatual = pd.Timestamp.today()
# lambda_ = np.log(2) / 4
# calcula_peso_bruto(df,PESO_TIPO, tatual, lambda_)
# gdf_hex = gera_subareas_rj(limites_path)
# gdf_resultado = atribuir_pesos_hexagonos(gdf_hex, df)

# print(gdf_resultado.to_string())
# gdf_resultado["peso_log"] = np.log1p(gdf_resultado["peso_suavizado"])
# print(gdf_resultado[gdf_resultado["peso_bruto"] > 0.0].count())
# print(df.head().to_string())
# print(gdf_resultado.head().to_string())
# print(gdf_resultado[gdf_resultado["peso_log"] == 0].count())

""" VISUALIZAÇÃO """
# m = folium.Map(location=[-22.9, -43.2], zoom_start=10)
#
# peso_max = gdf_resultado["peso_log"].max()
# colormap = cm.linear.YlOrRd_09.scale(0, peso_max)
#
# def estilo(feature):
#     peso = feature["properties"]["peso_log"]
#     return {
#         "color": "#333333",
#         "weight": 0.3,
#         "fillColor": colormap(peso),
#         "fillOpacity": 0.7,
#     }
#
# folium.GeoJson(
#     gdf_resultado.__geo_interface__,
#     name="Peso Log",
#     style_function=estilo,
#     tooltip=folium.GeoJsonTooltip(fields=["hex_id", "peso_bruto", "peso_suavizado", "peso_log"]),
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
# colormap.caption = "Peso Suavizado de Crimes"
# colormap.add_to(m)
# folium.LayerControl().add_to(m)
# m.save("mapa_crimes_suavizado.html")