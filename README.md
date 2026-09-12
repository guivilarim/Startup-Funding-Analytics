# Startup Funding Analytics

Dashboard interativo desenvolvido para análise de investimentos, valuation e distribuição de startups a partir de dados de funding.

## Equipe

**Grupo 9**

- André Cezar de Oliveira
- Caliel José Farias da Silva
- Guilherme Cavalcanti Vilarim

## Objetivo

O projeto tem como objetivo analisar dados de financiamento de startups, permitindo explorar padrões de investimento, distribuição geográfica, setores de atuação, valuation, desempenho e evolução temporal.

O dashboard foi desenvolvido com foco em análise exploratória e visualização interativa dos dados, permitindo que o usuário aplique filtros e observe os impactos diretamente nos indicadores e gráficos.

## Dataset

O projeto utiliza o dataset **Startup Funding Analytics**, disponibilizado em formato CSV.

O conjunto de dados contém informações relacionadas a startups, incluindo:

- Indústria
- País
- Ano
- Valor de investimento
- Investimento total
- Valuation
- Indicador de unicórnio

Arquivo utilizado:

    data/Startup_Funding_Analytics_150k.csv

## Funcionalidades

O dashboard está organizado em cinco áreas de análise:

- **Visão Geral:** panorama do mercado, distribuição e evolução dos investimentos
- **Mercado & Geografia:** análise dos investimentos por país e indústria
- **Evolução & Crescimento:** análise temporal dos investimentos e crescimento do mercado
- **Valuation & Desempenho:** análise de valuation e sua relação com investimentos
- **Unicórnios:** análise da distribuição, valuation e evolução das startups unicórnio

Além disso, o dashboard permite:

- Filtrar os dados por país
- Filtrar por indústria
- Selecionar um período de análise
- Alterar a métrica utilizada no ranking
- Visualizar indicadores atualizados conforme os filtros
- Explorar os dados por meio de gráficos interativos
- Interagir com os filtros de país, indústria e período diretamente pelos gráficos e aplica o filtro correspondente em todo o dashboard
- Redefinir todos os filtros para o estado padrão com um botão

Todos os indicadores e gráficos são atualizados de acordo com os filtros selecionados.

## Tecnologias

O projeto foi desenvolvido utilizando:

- Python
- Streamlit
- Pandas
- Plotly

## Estrutura do projeto

    Startup-Funding-Analytics/
    │
    ├── .streamlit/
    │
    ├── assets/
    │   ├── Logo.png
    │   └── style.css
    │
    ├── data/
    │   └── Startup_Funding_Analytics_150k.csv
    │
    ├── src/
    │   ├── data.py
    │   ├── filters.py
    │   ├── metrics.py
    │   ├── charts.py
    │   └── ui.py
    │
    ├── app.py
    ├── requirements.txt
    └── README.md

## Organização do código

A aplicação foi organizada de forma modular para separar responsabilidades:

**`app.py`**

Responsável pela execução principal da aplicação e integração entre os módulos.

**`src/data.py`**

Responsável pelo carregamento e preparação dos dados.

**`src/filters.py`**

Responsável pela criação e aplicação dos filtros.

**`src/metrics.py`**

Responsável pelo cálculo dos indicadores apresentados no dashboard.

**`src/charts.py`**

Responsável pela criação dos gráficos.

**`src/ui.py`**

Responsável por componentes reutilizáveis da interface e tema visual dos gráficos.

**`assets/style.css`**

Responsável pela estilização e identidade visual do dashboard.

## Como executar

### 1. Criar o ambiente virtual

No terminal, dentro da pasta do projeto:

    python -m venv st-venv

### 2. Ativar o ambiente virtual

No Windows:

    st-venv\Scripts\activate

### 3. Instalar as dependências

    pip install -r requirements.txt

### 4. Executar o dashboard

    streamlit run app.py

Após a execução, o Streamlit disponibilizará o endereço local para acessar o dashboard pelo navegador.

## Observações técnicas

O carregamento dos dados utiliza cache do Streamlit para evitar leituras desnecessárias do arquivo CSV durante as interações com o dashboard.

Os filtros são aplicados antes do cálculo dos indicadores e da geração dos gráficos, garantindo que as visualizações representem o mesmo recorte selecionado pelo usuário.

O filtro ao clicar nos gráficos atualiza os mesmos filtros da barra lateral, então um clique em qualquer gráfico reflete automaticamente em todos os outros. Cliques em país, indústria e período não se sobrepõem entre si e podem ser combinados livremente e redefinidos quando necessário também.

O projeto utiliza uma organização modular para facilitar a manutenção e evolução da aplicação.

## Fonte dos dados

**Dataset:** Startup Funding Analytics

**Fonte:** Kaggle
