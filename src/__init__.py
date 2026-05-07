# import pandas as pd
from .subareas_divider import gera_subareas_rj
from .weights_estimator import calcula_peso_bruto, atribuir_pesos_hexagonos
from .custom_model_builder import build_save_cmodel, generate_areas
from .pipeline import run_pipeline

# import os
# import visualization
# import geopandas as gpd

# """ Data Paths """
# limites_path = os.getenv("LIMITES_PATH").strip('"')
# crossfire_path = os.getenv("CROSSFIRE_DATA").strip('"')
# custom_model_path = os.getenv("CMODEL_PATH").strip('"')

# """ CONSTANTES """
# # pesos por tipo de crime (ajuste conforme sua realidade)
# PESO_TIPO = {
#     "Homicidio/Tentativa": 7.0,
#     "Tentativa/Roubo": 5.0,
#     "Operação policial":  9.0,
#     "Ação policial": 8.0,
#     "tiros a esmo": 7.0,
#     "Tentativa/Roubo de cargas": 6.0,
#     "Não identificado": 7.0,
# }
# T_ATUAL = pd.Timestamp.today()
# MEIA_VIDA = 4

# """ lê arquivos necessários e gera subáreas no município """
# # GeoJSON do município
# gdf = gpd.read_file(limites_path)
# df = pd.read_csv(crossfire_path)

# """ divide o Município em subáreas e retorna um gdf com um id e os pontos de cada hexágono """
# gdf_hex = gera_subareas_rj(gdf)

# """ calcula peso de cada ocorrência """
# df = calcula_peso_bruto(df, PESO_TIPO, T_ATUAL, MEIA_VIDA)

# """ calcula peso (bruto, suavizado e normalizado) de cada hexágono, considerando cada ocorrência de dentro dele """
# gdf_resultado = atribuir_pesos_hexagonos(gdf_hex, df)

# """ queremos alterar a prioridade apenas das áreas que tiverem risco maior que 1 """
# gdf_relevant = gdf_resultado[gdf_resultado["peso_log"] > 1].reset_index(drop=True)

# """ gerando áreas de risco com base nos pontos e nos pesos normalizados """
# areas = generate_areas(gdf_relevant)

# """ constrói e salva o modelo customizado para ser utilizado no Graphhopper """
# build_save_cmodel(custom_model_path, areas)

# """ funções para gerar visualizações gráficas com a biblioteca folium """
# visualization.visualizacao_hexagonos(gdf_hex)
# visualization.visualizacao_crimes(gdf_hex, gdf_resultado,coluna="peso_bruto", nome_arquivo="mapa_crimes_bruto.html")