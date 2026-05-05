import pandas as pd
import numpy as np
from subareas_divider import gera_subareas_rj
from weights_estimator import calcula_peso_bruto, atribuir_pesos_hexagonos, PESO_TIPO
from custom_model_builder import build_save_cmodel, generate_areas
import os

# data paths
# limites_path = os.environ.get("LIMITES_PATH")
# crossfire_path = os.environ.get("CROSSFIRE_PATH")
# custom_model_path = os.environ.get("CMODEL_PATH")
limites_path = r"C:\Users\marce\Documents\UFRJ\Analytica - Processo Seletivo\Limite_do_MunicADpio_do_Rio_de_Janeiro.geojson"
crossfire_path = r"C:\Users\marce\Documents\UFRJ\Analytica - Processo Seletivo\fc_api_occurrences_with_victims_detailed_2026-04-30T12_36_30.000Z.csv"
custom_model_path = r"C:\Users\marce\Documents\UFRJ\Analytica - Processo Seletivo\graphhopper\my_car.json"

# CONSTANTES:
t_atual = pd.Timestamp.today()
meia_vida = 4

# lê arquivos necessários e gera subáreas no município
df = pd.read_csv(crossfire_path)
gdf_hex = gera_subareas_rj(limites_path)

# calcula peso de cada ocorrência
df = calcula_peso_bruto(df,PESO_TIPO, t_atual, meia_vida)

# calcula peso de cada hexágono, considerando cada ocorrência de dentro dele
gdf_resultado = atribuir_pesos_hexagonos(gdf_hex, df)

# normalizamos o peso para um valor entre 0 e 10 com a função log
gdf_resultado["peso_log"] = np.log1p(gdf_resultado["peso_suavizado"])

# queremos alterar a prioridade apenas das áreas que tiverem risco maior que 1
gdf_relevant = gdf_resultado[gdf_resultado["peso_log"] > 1].reset_index(drop=True)
areas = generate_areas(gdf_relevant)
build_save_cmodel(custom_model_path, areas)


