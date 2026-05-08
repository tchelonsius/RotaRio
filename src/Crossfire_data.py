# Tratamento dos dados do Fogo Cruzado
import pandas as pd

crossfire_data_path = r"data\raw\fogo_cruzado\fc_api_occurrences_with_victims_2026-04-30T13_07_37.000Z.csv"
crossfire_df = pd.read_csv(crossfire_data_path)

crossfire_df.drop(["address","region","state","city",'locality',"sub_neighborhood",'complementary_reason', "police_unit", "clippings",'agents_dead', 'agents_wounded',
       'men_dead', 'men_wounded', 'women_dead', 'women_wounded', 'kids_dead',
       'kids_wounded', 'teenagers_dead', 'teenagers_wounded', 'elderly_dead',
       'elderly_wounded'], axis=1, inplace=True)

dt = pd.to_datetime(crossfire_df["data"], dayfirst=True, errors="coerce")
crossfire_df["data_timestamp"] = dt.dt.normalize()
crossfire_df["hora_timestamp"] = dt.dt.time
crossfire_df["hora"] = pd.to_datetime(
    crossfire_df["hora_timestamp"].astype(str),
    errors="coerce"
).dt.hour

def periodo_dia(hora):
    if 0 <= hora < 6:
        return 'Madrugada'
    elif 6 <= hora < 12:
        return 'Manhã'
    elif 12 <= hora < 18:
        return 'Tarde'
    else:
        return 'Noite'

crossfire_df['turno'] = crossfire_df['hora'].apply(periodo_dia)
