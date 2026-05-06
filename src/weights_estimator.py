import h3
import pandas as pd
from collections import defaultdict
import numpy as np

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

def atribuir_pesos_hexagonos(gdf_hex, df_crimes, col_peso: str = "peso_bruto", resolucao_h3: int = 8, decaimento: float = 0.5, niveis_suavizacao: int = 2,):
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

    # normalizamos o peso para um valor entre 0 e 10 com a função log
    gdf_resultado["peso_log"] = np.log1p(gdf_resultado["peso_suavizado"])

    print(gdf_resultado.tail().to_string())
    print("PESOS ATRIBUÍDOS AOS HEXÁGONOS!\n")
    return gdf_resultado
