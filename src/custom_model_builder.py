import json

def build_custom_model(areas):
    print("\n--- CONSTRUINDO O CUSTOM MODEL COM ÁREAS CUSTOMIZADAS...\n")
    aux = 0
    params = {
        "speed": [{ "if": "road_environment == FERRY", "limit_to": "ferry_speed" },
    { "else": "", "limit_to": "car_average_speed" },
    { "if": "true", "limit_to": "max_speed * 0.9" }],
        "distance_influence": 15,
        "priority": [],
        "areas":{
            "type": "FeatureCollection",
            "features": []
        }
    }
    for area in areas:
        feature = {
        "type": "Feature",
        "id": "custom"+str(aux),
        "properties": {},
        "geometry": {
          "type": "Polygon",
          "coordinates": [
            area[:7]
          ]
        }
      }
        factor = 1/area[-1]
        params["priority"].append({"if": "in_custom"+str(aux),"multiply_by":factor})
        params["areas"]["features"].append(feature)
        aux+=1
    print("CUSTOM MODEL PRONTO!\n")
    return params

def generate_areas(gdf_relevant):
    print("\n--- GERANDO ÁREAS DE RISCO PARA O CUSTOM MODEL...\n")
    areas = []
    linhas = gdf_relevant.shape[0]
    for f in range(1500):
        coords = list(gdf_relevant.iloc[f]["geometry"].exterior.coords)
        coords.append(gdf_relevant.iloc[f]["peso_log"])
        areas.append(coords)
    print(f"{linhas} ÁREAS DE RISCO GERADAS!\n")
    return areas

def build_save_cmodel(path, areas):
    print("\n--- CONSTRUINDO E SALVANDO O CUSTOM MODEL COMO JSON...\n")
    params = build_custom_model(areas)
    with open(path, "w", encoding="utf-8") as file:
        json.dump(params, file, ensure_ascii=False, indent=2)
    print("CUSTOM MODEL SALVO!\n")
