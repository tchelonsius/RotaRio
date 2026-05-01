

# Documentação de Dados — Transporte e Dados Urbanos (Rio de Janeiro)

Este documento descreve as fontes de dados utilizadas e o dicionário das bases relacionadas ao sistema de transportes (SMTR), além de fontes públicas complementares recomendadas para o desenvolvimento de soluções no contexto do hackathon.

![banner](banner.jpeg)

---

## Fontes de Dados

As bases de dados deste projeto estão organizadas em duas categorias:

### Dataset Principal (Projeto)

O dataset principal utilizado no projeto é o conjunto de dados da Secretaria Municipal de Transportes.

**SMTR — Sistema Municipal de Transportes**
Download consolidado:
[https://drive.google.com/drive/folders/1HOImipCoQWywaJq-mhKt1ufxJDNq0bip?usp=sharing](https://drive.google.com/drive/folders/1HOImipCoQWywaJq-mhKt1ufxJDNq0bip?usp=sharing)

Este dataset contém dados operacionais, financeiros e estruturais do sistema de transporte público do Rio de Janeiro, sendo a base central para análise e desenvolvimento da solução.

---

---

### Fontes Complementares (Hackathon)

As fontes abaixo não fazem parte diretamente do dataset principal, mas são recomendadas para enriquecer análises, gerar insights e construir soluções mais robustas durante o hackathon:

* Data.Rio
  [https://www.data.rio/](https://www.data.rio/)
  Dados urbanos diversos, incluindo mobilidade, clima, demografia e infraestrutura.

* Portal de Dados Abertos do RJ
  [https://dadosabertos.rj.gov.br/](https://dadosabertos.rj.gov.br/)
  Base ampla de dados governamentais estaduais.

* Instituto de Segurança Pública do RJ
  [https://www.ispdados.rj.gov.br/](https://www.ispdados.rj.gov.br/)
  Dados relacionados à criminalidade e segurança pública.

* Fogo Cruzado
  [https://api.fogocruzado.org.br/search](https://api.fogocruzado.org.br/search)
  API com registros de eventos de violência armada.

* Ministério da Saúde do Brasil
  [https://dadosabertos.saude.gov.br/](https://dadosabertos.saude.gov.br/)
  Dados de saúde pública, incluindo informações epidemiológicas e de infraestrutura hospitalar.

---


**Observação:**
O desafio do hackathon possui caráter aberto, incentivando o uso combinado dessas fontes para cruzamento de dados, geração de valor e desenvolvimento de soluções inovadoras para a cidade do Rio de Janeiro.

---

## Materiais de Apoio e Diretrizes do Hackathon

Para auxiliar no desenvolvimento técnico e organizacional do projeto, recomenda-se o uso dos seguintes recursos:

### Materiais de Apoio

* **Git e controle de versão**
  Boas práticas de versionamento, uso de branches, commits descritivos e pull requests:
  [https://github.com/UFRJ-Analytica/PS-2025.1/blob/main/Materiais/git.md](https://github.com/UFRJ-Analytica/PS-2025.1/blob/main/Materiais/git.md)

* **Análise Exploratória de Dados (EDA)**
  Compreensão inicial dos dados, identificação de padrões, outliers e correlações:
  [https://github.com/UFRJ-Analytica/PS-2025.1/blob/main/Materiais/EDA.md](https://github.com/UFRJ-Analytica/PS-2025.1/blob/main/Materiais/EDA.md)


Adicionalmente, recomenda-se a utilização de documentação técnica, mecanismos de busca, fóruns especializados (como Stack Overflow) e ferramentas baseadas em modelos de linguagem para apoio ao desenvolvimento.

---

### Organização em Equipe

Os participantes foram organizados em grupos para desenvolvimento colaborativo. É fundamental manter comunicação contínua entre os membros da equipe ao longo do projeto.

---

### Boas Práticas de Desenvolvimento

Cada grupo deve:

* Clonar o repositório do projeto
* Trabalhar com branches organizadas
* Criar commits claros e bem descritos
* Utilizar pull requests para integração de código
* Manter o código limpo, estruturado e documentado

Essas práticas são fundamentais para garantir qualidade, rastreabilidade e escalabilidade no desenvolvimento do projeto.

---

## Dataset Principal — SMTR

O conjunto de dados da SMTR contempla informações sobre operação, planejamento, subsídios e monitoramento da frota de transporte público.

---

## Dicionário de Dados (SMTR)

Abaixo está a descrição das pastas presentes no dataset:

---

### 1. `br_rj_riodejaneiro_recursos`

**Tema:** Recursos e Apelações
**Descrição:**
Dados administrativos referentes a recursos interpostos por operadores do sistema de transporte, incluindo:

* Bloqueios de via
* Reprocessamento de viagens
* Validação de serviços

---

### 2. `br_rj_riodejaneiro_viagem_zirix`

**Tema:** Registros de Viagem
**Descrição:**
Contém dados de viagens provenientes de sistemas de bilhetagem, incluindo:

* Execução de viagens
* Eventos operacionais

---

### 3. `cadastro`

**Tema:** Cadastros do Sistema
**Descrição:**
Informações cadastrais gerais, como:

* Consórcios operadores
* Estrutura organizacional do sistema

---

### 4. `dashboard_bilhetagem_implantacao_jae`

**Tema:** Monitoramento GPS
**Descrição:**
Dados agregados de localização de veículos por modal:

* BRT
* Ônibus (SPPO)
* Vans (STPL)
* VLT

---

### 5. `dashboard_subsidio_sppo`

**Tema:** Subsídios
**Descrição:**
Tabelas consolidadas utilizadas para acompanhamento financeiro:

* Pagamentos de subsídios
* Indicadores operacionais

---

### 6. `gtfs`

**Tema:** General Transit Feed Specification
**Descrição:**
Base padronizada de transporte contendo:

* routes: linhas
* stops: paradas
* trips: viagens
* shapes: geometria das rotas
* calendar: operação temporal

---

### 7. `monitoramento`

**Tema:** Fiscalização
**Descrição:**
Registros relacionados ao controle operacional:

* Multas
* Autuações
* Penalidades

---

### 8. `planejamento`

**Tema:** Planejamento Operacional
**Descrição:**
Define regras e parâmetros do sistema:

* Tarifas
* Integrações tarifárias
* Calendário operacional
* Ordens de serviço

---

### 9. `projeto_subsidio_sppo`

**Tema:** Dados de Subsídio (Base Bruta)
**Descrição:**
Dados granulares utilizados no cálculo de subsídios:

* Quilometragem percorrida
* Status de trajetos
* Processamento de viagens

---

### 10. `projeto_subsidio_sppo_encontro_contas`

**Tema:** Auditoria Financeira (V1)
**Descrição:**
Relatórios financeiros contendo:

* Subsídio devido
* Receita tarifária

---

### 11. `projeto_subsidio_sppo_encontro_contas_v2`

**Tema:** Auditoria Financeira (V2)
**Descrição:**
Versão atualizada com:

* Serviços atípicos
* Correções operacionais
* Receitas não tarifárias

---

### 12. `subsidio`

**Tema:** Parâmetros Financeiros
**Descrição:**
Define métricas utilizadas no cálculo de remuneração:

* Valor por quilômetro
* Penalidades
* Metas operacionais

---

### 13. `veiculo`

**Tema:** Frota
**Descrição:**
Dados dos veículos do sistema:

* Licenciamento
* Operação diária
* Inspeções
* Condições operacionais


