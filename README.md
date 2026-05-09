# RotaRio 🚌

Sistema de recomendação de rotas de ônibus seguras para o Rio de Janeiro.

A aplicação cruza dados de mobilidade urbana com dados de criminalidade para sugerir as rotas de ônibus mais seguras entre dois pontos da cidade, exibindo-as em um mapa interativo.

![banner](Orientações_Analytica/banner.jpeg)

---

## Como funciona

1. O usuário informa sua **origem** (via GPS ou clique no mapa) e seu **destino**
2. O sistema busca rotas de ônibus que passam próximas aos dois pontos — com buffer crescente de **300m → 500m → 1km**
3. Apenas rotas que passam **nos dois pontos** são consideradas (interseção)
4. Cada rota recebe um **índice de risco** baseado em ocorrências do Fogo Cruzado nas áreas por onde passa
5. As **3 rotas mais seguras** são exibidas no mapa em verde, laranja e vermelho

---

## Estrutura do Projeto

```
RotaRio/
├── data/
│   ├── cross_fire.csv          # Ocorrências do Fogo Cruzado
│   ├── custom_model.json       # Modelo de risco gerado pela pipeline (auto-gerado)
│   └── limites.geojson         # Limites geográficos do município do Rio
├── frontend/
│   └── index.html              # Interface web com mapa Leaflet.js
├── mapas/
│   └── mapa_crimes.html        # Mapa de visualização de crimes
├── notebooks/
│   ├── 01_EDA_crossfire.ipynb  # Análise exploratória do Fogo Cruzado
│   └── 02_EDA_ISP.ipynb        # Análise exploratória dos dados do ISP
├── Orientações_Analytica/      # Materiais e orientações do projeto
├── src/
│   ├── app.py                  # Servidor Flask — API REST
│   ├── secure_route_finder.py  # Busca e ranking de rotas seguras
│   ├── get_data_bus.py         # Carregamento dos dados GTFS
│   ├── pipeline.py             # Pipeline de geração do modelo de risco
│   ├── custom_model_builder.py # Construção do modelo de áreas de risco
│   ├── subareas_divider.py     # Divisão do Rio em hexágonos (H3)
│   ├── weights_estimator.py    # Cálculo dos pesos de risco por área
│   ├── visualization.py        # Utilitários de visualização
│   └── __init__.py
├── .env                        # Variáveis de ambiente (não versionado)
├── requirements.txt
└── README.md

# Arquivos CSV (não versionados — ver instruções abaixo)
├── routes.csv
├── trips.csv
└── shapes_geom.csv
```

---

## Instalação — Passo a Passo

### 1. Clone o repositório

```bash
git clone https://github.com/tchelonsius/RotaRio.git
cd RotaRio
```

### 2. Crie e ative o ambiente virtual

```bash
python3 -m venv .venv
source .venv/bin/activate        # Mac/Linux
.venv\Scripts\activate           # Windows
```

### 3. Instale as dependências

```bash
pip install -r requirements.txt
```

### 4. Baixe os arquivos de dados (GTFS)

Os arquivos CSV não estão versionados por excederem o limite do GitHub. Baixe-os pelo link abaixo e coloque-os na **raiz do projeto** (`RotaRio/`):

📁 **[Download — Dados GTFS Rio](https://drive.google.com/drive/folders/1qjn5hDKVLu_-_EsfOzCnV4giPqwA4ZTN)**

| Arquivo | Descrição | Onde colocar |
|---|---|---|
| `routes.csv` | Linhas e rotas de ônibus | `RotaRio/routes.csv` |
| `trips.csv` | Viagens e trajetos | `RotaRio/trips.csv` |
| `shapes_geom.csv` | Geometria das rotas | `RotaRio/shapes_geom.csv` |

> Os dados são do dataset **SMTR — GTFS** disponibilizado pela Secretaria Municipal de Transportes do Rio de Janeiro.

### 5. Configure o `.env`

Crie um arquivo `.env` na raiz do projeto:

```env
LIMITES_PATH=/caminho/absoluto/RotaRio/data/limites.geojson
CROSSFIRE_DATA=/caminho/absoluto/RotaRio/data/cross_fire.csv
CMODEL_PATH=/caminho/absoluto/RotaRio/data/custom_model.json
```

> 💡 No Mac/Linux, rode `pwd` dentro da pasta do projeto para descobrir o caminho absoluto.

**Exemplo:**
```env
LIMITES_PATH=/Users/seunome/RotaRio/data/limites.geojson
CROSSFIRE_DATA=/Users/seunome/RotaRio/data/cross_fire.csv
CMODEL_PATH=/Users/seunome/RotaRio/data/custom_model.json
```

### 6. Inicie o servidor

```bash
python3 -m src.app
```

Na primeira execução o servidor irá:
1. Rodar a **pipeline de risco** — divide o Rio em hexágonos H3 e calcula o peso de criminalidade de cada área (pode levar alguns minutos)
2. Carregar os **dados GTFS** de ônibus
3. Subir a API em `http://127.0.0.1:5000`

Você verá no terminal:
```
LOADING PIPELINE DATA. . .
CUSTOM MODEL SALVO!
API RotaRio: LOADING BUS DATA. . .
* Running on http://127.0.0.1:5000
```

---

## Usando o Frontend

### Opção 1 — Live Server (VS Code)
1. Instale a extensão **Live Server**
2. Clique com o botão direito em `frontend/index.html`
3. Selecione **"Open with Live Server"**
4. Permita o acesso à localização quando solicitado pelo browser

### Opção 2 — Servidor local
```bash
python3 -m http.server 8080
```
Acesse `http://localhost:8080/frontend/index.html`

### Como usar o mapa

| Passo | Ação |
|---|---|
| 1 | Permita o acesso à localização — a origem é definida automaticamente pelo GPS |
| 2 | Clique em **"Destino"** e depois clique no mapa para definir o destino |
| 3 | Clique em **"Calcular Rota Mais Segura"** |
| 4 | As 3 rotas mais seguras aparecem no mapa |

As rotas são coloridas por nível de segurança:
- 🟢 **Verde** — mais segura
- 🟠 **Laranja** — segurança intermediária
- 🔴 **Vermelho** — menos segura

---

## API

### `GET /secure_bus_routes`

Retorna as rotas de ônibus mais seguras entre dois pontos.

**Parâmetros:**

| Parâmetro | Tipo | Descrição |
|---|---|---|
| `origin` | `lon,lat` | Coordenadas de origem |
| `destination` | `lon,lat` | Coordenadas de destino |

**Exemplo:**

```
GET http://127.0.0.1:5000/secure_bus_routes?origin=-43.2282,-22.9121&destination=-43.1729,-22.9068
```

**Resposta:**

```json
[
  {
    "route_short_name": "352",
    "route_long_name": "Riocentro - Candelária",
    "shape_id": "ndqy",
    "shape": "LINESTRING (...)",
    "start_pt": "POINT (...)",
    "end_pt": "POINT (...)",
    "peso_log": 2.4
  }
]
```

**Códigos de resposta:**

| Código | Descrição |
|---|---|
| `200` | Rotas encontradas com sucesso |
| `400` | Parâmetros `origin` ou `destination` ausentes |
| `404` | Nenhuma rota encontrada entre os dois pontos |

---

## Fontes de Dados

| Fonte | Uso |
|---|---|
| [SMTR — GTFS Rio](https://drive.google.com/drive/folders/1HOImipCoQWywaJq-mhKt1ufxJDNq0bip) | Rotas, viagens e geometria dos ônibus |
| [Fogo Cruzado](https://api.fogocruzado.org.br/search) | Ocorrências de violência armada |
| [Data.Rio](https://www.data.rio/) | Dados urbanos complementares |
| [ISP-RJ](https://www.ispdados.rj.gov.br/) | Dados de segurança pública |

---

## Tecnologias

- **Python** — Flask, GeoPandas, Shapely, Pandas, H3
- **JavaScript** — Leaflet.js
- **Dados** — GTFS Rio (SMTR), Fogo Cruzado
