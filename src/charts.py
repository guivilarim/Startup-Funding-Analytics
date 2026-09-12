import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.colors import sample_colorscale

# Paleta categórica do dashboard (mesmas cores dos KPIs).
INDUSTRY_COLORS = [
    "#22D3EE",  # CYAN
    "#F43F5E",  # ROSE
    "#F59E0B",  # AMBER
    "#8B5CF6",  # VIOLET
    "#10B981",  # EMERALD
    "#3B82F6",  # BLUE
    "#F472B6",  # ROSE claro
    "#A3E635",  # LIME
]

def empty_figure():
    fig = go.Figure()

    fig.update_xaxes(visible=False)
    fig.update_yaxes(visible=False)

    fig.add_annotation(
        text="Nenhum dado disponível para os filtros selecionados",
        x=0.5,
        y=0.5,
        xref="paper",
        yref="paper",
        showarrow=False,
        font=dict(
            size=14,
            color="#A8B3C7",
        ),
    )

    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
    )

    return fig

def create_funding_map(df_filtrado, map_scale):
    if df_filtrado.empty:
        return empty_figure()
    funding_by_country = (
        df_filtrado
        .groupby("Country")["Funding_Amount_USD"]
        .sum()
        .reset_index()
    )

    funding_by_country["Funding_Billions"] = (
        funding_by_country["Funding_Amount_USD"] / 1e9
    )

    country_to_iso = {
        "USA": "USA",
        "United States": "USA",
        "US": "USA",
        "UK": "GBR",
        "United Kingdom": "GBR",
        "Germany": "DEU",
        "Canada": "CAN",
        "Australia": "AUS",
        "India": "IND",
        "Singapore": "SGP",
        "Brazil": "BRA",
        "France": "FRA",
        "Italy": "ITA",
        "Spain": "ESP",
        "Japan": "JPN",
        "China": "CHN",
        "South Korea": "KOR",
        "Mexico": "MEX",
        "Argentina": "ARG",
        "Chile": "CHL",
        "Colombia": "COL",
        "Peru": "PER",
        "South Africa": "ZAF",
        "Nigeria": "NGA",
        "Egypt": "EGY",
        "Israel": "ISR",
        "Turkey": "TUR",
        "Russia": "RUS",
        "Switzerland": "CHE",
        "Sweden": "SWE",
        "Norway": "NOR",
        "Denmark": "DNK",
        "Finland": "FIN",
        "Netherlands": "NLD",
        "Belgium": "BEL",
        "Portugal": "PRT",
        "Greece": "GRC",
        "Poland": "POL",
        "Czech Republic": "CZE",
        "Hungary": "HUN",
        "Austria": "AUT",
        "Ireland": "IRL",
        "New Zealand": "NZL",
    }

    funding_by_country["ISO"] = (
        funding_by_country["Country"].map(country_to_iso)
    )

    funding_map = funding_by_country.dropna(subset=["ISO"])

    fig = px.choropleth(
        funding_map,
        locations="ISO",
        color="Funding_Billions",
        hover_name="Country",
        custom_data=["Country"],
        color_continuous_scale=map_scale,
        labels={"Funding_Billions": "US$ Bilhões"},
        projection="natural earth",
    )

    return fig


def create_industry_evolution_chart(
    df_filtrado,
    qualitative_palette,
):
    if df_filtrado.empty:
        return empty_figure()
    evolution = (
        df_filtrado
        .groupby(["Year", "Industry"])
        .size()
        .reset_index(name="Count")
    )

    fig = px.line(
        evolution,
        x="Year",
        y="Count",
        color="Industry",
        markers=True,
        color_discrete_sequence=qualitative_palette,
    )

    return fig


def create_valuation_boxplot(
    df_filtrado,
    qualitative_palette,
):
    if df_filtrado.empty:
        return empty_figure()
    fig = px.box(
        df_filtrado,
        x="Industry",
        y="Valuation_USD",
        labels={
            "Valuation_USD": "Valuation (USD)",
            "Industry": "",
        },
        color="Industry",
        color_discrete_sequence=qualitative_palette,
    )

    return fig


def create_ranking_chart(ranking):
    fig = px.bar(
        ranking,
        x="Metric",
        y="Industry",
        orientation="h",
    )

    return fig


def create_country_investment_chart(df_filtrado):
    if df_filtrado.empty:
        return empty_figure()
    ranking = (
        df_filtrado
        .groupby("Country")["Funding_Amount_USD"]
        .sum()
        .reset_index()
        .sort_values(
            "Funding_Amount_USD",
            ascending=False,
        )
        .head(10)
    )

    ranking["Funding_Billions"] = (
        ranking["Funding_Amount_USD"] / 1e9
    )

    ranking = ranking.sort_values(
        "Funding_Billions",
        ascending=True,
    )

    fig = px.bar(
        ranking,
        x="Funding_Billions",
        y="Country",
        orientation="h",
        labels={
            "Funding_Billions": "Investimento (US$ Bilhões)",
            "Country": "",
        },
        color="Funding_Billions",
        color_continuous_scale=[
            "#164E63",
            "#155E75",
            "#0E7490",
            "#0891B2",
        ],
    )

    fig.update_coloraxes(
        showscale=False
    )

    fig.update_traces(
        hovertemplate=(
            "<b>%{y}</b>"
            "<br>US$ %{x:.1f} bilhões"
            "<extra></extra>"
        )
    )

    fig.update_xaxes(
        tickformat=".1f"
    )

    return fig


def create_average_investment_chart(df_filtrado):
    if df_filtrado.empty:
        return empty_figure()
    country_analysis = (
        df_filtrado
        .groupby("Country")
        .agg(
            Startups=("Country", "size"),
            Investment_USD=("Funding_Amount_USD", "sum"),
        )
        .reset_index()
    )

    country_analysis["Average_Investment_USD"] = (
        country_analysis["Investment_USD"]
        / country_analysis["Startups"]
    )

    ranking = (
        country_analysis
        .sort_values(
            "Average_Investment_USD",
            ascending=False,
        )
        .head(10)
    )

    ranking["Average_Investment_Millions"] = (
        ranking["Average_Investment_USD"] / 1e6
    )

    ranking = ranking.sort_values(
        "Average_Investment_Millions",
        ascending=True,
    )

    fig = px.bar(
        ranking,
        x="Average_Investment_Millions",
        y="Country",
        orientation="h",
        labels={
            "Average_Investment_Millions":
                "Investimento Médio por Startup (US$ Milhões)",
            "Country": "",
        },
        color="Average_Investment_Millions",
        color_continuous_scale=[
            "#164E63",
            "#155E75",
            "#0E7490",
            "#0891B2",
            "#06B6D4",
            "#22D3EE",
        ],
    )

    fig.update_coloraxes(
        showscale=False
    )

    fig.update_traces(
        hovertemplate=(
            "<b>%{y}</b>"
            "<br>US$ %{x:.1f} milhões por startup"
            "<extra></extra>"
        )
    )

    return fig


def create_country_scatter_chart(df_filtrado):
    if df_filtrado.empty:
        return empty_figure()
    country_analysis = (
        df_filtrado
        .groupby("Country")
        .agg(
            Startups=("Country", "size"),
            Investment_USD=("Funding_Amount_USD", "sum"),
        )
        .reset_index()
    )

    country_analysis["Investment_Billions"] = (
        country_analysis["Investment_USD"] / 1e9
    )

    fig = px.scatter(
        country_analysis,
        x="Startups",
        y="Investment_Billions",
        size="Investment_Billions",
        hover_name="Country",
        custom_data=["Country"],
        labels={
            "Startups": "Número de Startups",
            "Investment_Billions":
                "Investimento (US$ Bilhões)",
        },
    )

    return fig


def create_country_industry_heatmap(df_filtrado):
    if df_filtrado.empty:
        return empty_figure()
    country_industry = pd.crosstab(
        df_filtrado["Country"],
        df_filtrado["Industry"],
    )

    paises = country_industry.index.tolist()
    industrias = country_industry.columns.tolist()

    color_scale = [
        "#172554",
        "#1E3A8A",
        "#1D4ED8",
        "#0284C7",
        "#22D3EE",
    ]

    valores = [
        int(country_industry.loc[pais, industria])
        for pais in paises
        for industria in industrias
    ]
    vmin, vmax = min(valores), max(valores)

    def normaliza(v):
        return (v - vmin) / (vmax - vmin) if vmax > vmin else 0.5

    cores = sample_colorscale(
        color_scale,
        [normaliza(v) for v in valores],
    )

    shapes = []
    annotations = []
    click_x, click_y, click_pais, click_industria = [], [], [], []

    k = 0
    for i, pais in enumerate(paises):
        for j, industria in enumerate(industrias):
            valor = valores[k]

            shapes.append(dict(
                type="rect",
                x0=j - 0.5,
                x1=j + 0.5,
                y0=i - 0.5,
                y1=i + 0.5,
                fillcolor=cores[k],
                line=dict(width=0),
                layer="below",
            ))

            annotations.append(dict(
                x=j,
                y=i,
                text=str(valor),
                showarrow=False,
                font=dict(color="#F8FAFC", size=11),
            ))

            click_x.append(j)
            click_y.append(i)
            click_pais.append(pais)
            click_industria.append(industria)
            k += 1

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=click_x,
        y=click_y,
        mode="markers",
        marker=dict(
            size=40,
            opacity=0.02,
            color=valores,
            colorscale=color_scale,
            cmin=vmin,
            cmax=vmax,
            showscale=True,
            colorbar=dict(title="Startups", thickness=12),
        ),
        customdata=list(zip(click_pais, click_industria)),
        text=[str(v) for v in valores],
        hovertemplate=(
            "<b>País:</b> %{customdata[0]}"
            "<br><b>Indústria:</b> %{customdata[1]}"
            "<br><b>Startups:</b> %{text}"
            "<extra></extra>"
        ),
        showlegend=False,
    ))

    fig.update_layout(
        shapes=shapes,
        annotations=annotations,
    )

    fig.update_xaxes(
        tickmode="array",
        tickvals=list(range(len(industrias))),
        ticktext=industrias,
        tickangle=-35,
        range=[-0.5, len(industrias) - 0.5],
        showgrid=False,
    )

    fig.update_yaxes(
        tickmode="array",
        tickvals=list(range(len(paises))),
        ticktext=paises,
        range=[len(paises) - 0.5, -0.5],
        showgrid=False,
    )

    return fig


def create_investment_evolution_chart(df_filtrado):
    if df_filtrado.empty:
        return empty_figure()
    evolution = (
        df_filtrado
        .groupby("Year")["Funding_Amount_USD"]
        .sum()
        .reset_index()
        .sort_values("Year")
    )

    evolution["Funding_Billions"] = (
        evolution["Funding_Amount_USD"] / 1e9
    )

    fig = px.line(
        evolution,
        x="Year",
        y="Funding_Billions",
        markers=True,
        labels={
            "Year": "Ano",
            "Funding_Billions":
                "Investimento (US$ Bilhões)",
        },
    )

    fig.update_traces(
        line=dict(
            color="#06B6D4",
            width=3,
        ),
        marker=dict(
            size=7,
            color="#22D3EE",
        ),
        hovertemplate=(
            "<b>%{x}</b>"
            "<br>US$ %{y:.1f} bilhões"
            "<extra></extra>"
        ),
    )

    return fig


def create_average_ticket_by_round_chart(df_filtrado):
    if df_filtrado.empty:
        return empty_figure()
    round_order = [
        "Pre-Seed",
        "Seed",
        "Series A",
        "Series B",
        "Series C",
        "Series D",
        "Series E",
        "Series F",
        "Series G",
    ]

    ticket = (
        df_filtrado
        .groupby("Funding_Round")["Funding_Amount_USD"]
        .mean()
        .reset_index()
    )

    ticket["Round_Order"] = (
        ticket["Funding_Round"]
        .map({
            round_name: i
            for i, round_name in enumerate(round_order)
        })
    )

    ticket = (
        ticket
        .dropna(subset=["Round_Order"])
        .sort_values("Round_Order")
    )

    ticket["Ticket_Millions"] = (
        ticket["Funding_Amount_USD"] / 1e6
    )

    fig = px.line(
        ticket,
        x="Funding_Round",
        y="Ticket_Millions",
        markers=True,
        labels={
            "Funding_Round": "Rodada",
            "Ticket_Millions":
                "Ticket médio (US$ Milhões)",
        },
    )

    fig.update_traces(
        line=dict(
            color="#3B82F6",
            width=3,
        ),
        marker=dict(
            size=8,
            color="#22D3EE",
        ),
        hovertemplate=(
            "<b>%{x}</b>"
            "<br>US$ %{y:.1f} milhões"
            "<extra></extra>"
        ),
    )

    return fig


def create_rounds_evolution_chart(df_filtrado):
    if df_filtrado.empty:
        return empty_figure()
    evolution = (
        df_filtrado
        .groupby("Year")
        .size()
        .reset_index(name="Rounds")
        .sort_values("Year")
    )

    fig = px.line(
        evolution,
        x="Year",
        y="Rounds",
        markers=True,
        labels={
            "Year": "Ano",
            "Rounds": "Número de rodadas",
        },
    )

    fig.update_traces(
        line=dict(
            color="#8B5CF6",
            width=3,
        ),
        marker=dict(
            size=7,
            color="#A78BFA",
        ),
        hovertemplate=(
            "<b>%{x}</b>"
            "<br>%{y:,} rodadas"
            "<extra></extra>"
        ),
    )

    return fig


def create_funding_by_round_evolution_chart(
    df_filtrado,
    qualitative_palette,
):
    if df_filtrado.empty:
        return empty_figure()
    evolution = (
        df_filtrado
        .groupby(
            ["Year", "Funding_Round"]
        )["Funding_Amount_USD"]
        .sum()
        .reset_index()
    )

    evolution["Funding_Billions"] = (
        evolution["Funding_Amount_USD"] / 1e9
    )

    round_order = [
        "Pre-Seed",
        "Seed",
        "Series A",
        "Series B",
        "Series C",
        "Series D",
        "Series E",
        "Series F",
        "Series G",
    ]

    evolution["Round_Order"] = (
        evolution["Funding_Round"]
        .map({
            round_name: i
            for i, round_name in enumerate(round_order)
        })
    )

    evolution = (
        evolution
        .dropna(subset=["Round_Order"])
        .sort_values(
            ["Year", "Round_Order"]
        )
    )

    fig = px.area(
        evolution,
        x="Year",
        y="Funding_Billions",
        color="Funding_Round",
        markers=False,
        color_discrete_sequence=qualitative_palette,
        labels={
            "Year": "Ano",
            "Funding_Billions":
                "Capital captado (US$ Bilhões)",
            "Funding_Round": "Rodada",
        },
    )

    fig.update_traces(
        hovertemplate=(
            "<b>%{x}</b>"
            "<br>%{fullData.name}"
            "<br>US$ %{y:.1f} bilhões"
            "<extra></extra>"
        )
    )

    return fig

###############
def create_capital_evolution_chart(df):
    """
    Evolução anual do capital captado.
    """
    if df.empty:
        return empty_figure()

    dados = (
        df.groupby("Year", as_index=False)["Funding_Amount_USD"]
        .sum()
        .sort_values("Year")
    )

    dados["Capital_B"] = (
        dados["Funding_Amount_USD"] / 1e9
    )

    fig = px.line(
        dados,
        x="Year",
        y="Capital_B",
        markers=True,
    )

    fig.update_traces(
        line=dict(
            color="#F43F5E",
            width=3,
        ),
        marker=dict(
            color="#F43F5E",
            size=7,
        ),
        fill="tozeroy",
        fillcolor="rgba(244,63,94,0.12)",
        hovertemplate=(
            "<b>%{x}</b>"
            "<br>Capital: US$ %{y:.2f} bi"
            "<extra></extra>"
        ),
    )

    fig.update_layout(
        showlegend=False,
        hovermode="x unified",
    )

    fig.update_xaxes(
        title_text="Ano",
        dtick=1,
    )

    fig.update_yaxes(
        title_text="Capital captado (US$ bi)",
    )

    return fig


def create_rounds_evolution_chart(df):
    """
    Evolução anual do volume de investimentos.
    Usa a quantidade de registros por ano,
    pois Funding_Round não está disponível no dataframe filtrado.
    """
    if df.empty:
        return empty_figure()
    dados = (
        df.groupby("Year")
        .size()
        .reset_index(name="Rounds")
        .sort_values("Year")
    )

    fig = px.bar(
        dados,
        x="Year",
        y="Rounds",
    )

    # Gradiente visual dentro da família ROSE
    valores = dados["Rounds"].tolist()

    if len(valores) > 1 and max(valores) != min(valores):
        normalizados = [
            (v - min(valores)) / (max(valores) - min(valores))
            for v in valores
        ]
    else:
        normalizados = [0.6] * len(valores)

    escala = [
        "#4C1025",
        "#6B1735",
        "#881C42",
        "#A51F49",
        "#BE123C",
        "#E11D48",
        "#F43F5E",
    ]

    cores = [
        escala[
            min(
                int(n * (len(escala) - 1)),
                len(escala) - 1,
            )
        ]
        for n in normalizados
    ]

    fig.update_traces(
        marker=dict(
            color=cores,
            line=dict(
                color="rgba(255,255,255,.08)",
                width=1,
            ),
        ),
        opacity=0.94,
        hovertemplate=(
            "<b>%{x}</b>"
            "<br>Rodadas: %{y:,.0f}"
            "<extra></extra>"
        ),
    )

    fig.update_layout(
        showlegend=False,
        hovermode="x",
    )

    fig.update_xaxes(
        title_text="Ano",
        dtick=1,
    )

    fig.update_yaxes(
        title_text="Número de rodadas",
    )

    return fig


def create_average_ticket_by_round_chart(df):
    """
    Ticket médio de investimento por ano.
    Usa Funding_Amount_USD, disponível no dataframe filtrado.
    """
    if df.empty:
        return empty_figure()
    dados = (
        df.groupby("Year", as_index=False)["Funding_Amount_USD"]
        .mean()
        .sort_values("Year")
    )

    fig = px.bar(
        dados,
        x="Year",
        y="Funding_Amount_USD",
    )

    valores = dados["Funding_Amount_USD"].tolist()

    if len(valores) > 1 and max(valores) != min(valores):
        normalizados = [
            (v - min(valores)) / (max(valores) - min(valores))
            for v in valores
        ]
    else:
        normalizados = [0.6] * len(valores)

    escala = [
        "#4C1025",
        "#6B1735",
        "#881C42",
        "#A51F49",
        "#BE123C",
        "#E11D48",
        "#F43F5E",
    ]

    cores = [
        escala[
            min(
                int(n * (len(escala) - 1)),
                len(escala) - 1,
            )
        ]
        for n in normalizados
    ]

    fig.update_traces(
        marker=dict(
            color=cores,
            line=dict(
                color="rgba(255,255,255,.08)",
                width=1,
            ),
        ),
        opacity=0.94,
        hovertemplate=(
            "<b>%{x}</b>"
            "<br>Ticket médio: $%{y:,.0f}"
            "<extra></extra>"
        ),
    )

    fig.update_layout(
        showlegend=False,
        hovermode="x",
    )

    fig.update_xaxes(
        title_text="Ano",
        dtick=1,
    )

    fig.update_yaxes(
        title_text="Ticket médio (USD)",
        tickformat="~s",
    )

    return fig


def create_growth_evolution_chart(df):
    """
    Evolução anual do crescimento do capital captado.

    O crescimento é calculado diretamente a partir
    do funding agregado por ano, evitando dependência
    da coluna Annual_Growth_Rate.
    """
    if df.empty:
        return empty_figure()
    dados = (
        df.groupby(
            "Year",
            as_index=False,
        )["Funding_Amount_USD"]
        .sum()
        .sort_values("Year")
    )

    dados["Growth_Pct"] = (
        dados["Funding_Amount_USD"]
        .pct_change()
        .replace(
            [float("inf"), -float("inf")],
            float("nan"),
        )
        * 100
    )

    dados = dados.dropna(
        subset=["Growth_Pct"]
    )

    fig = px.line(
        dados,
        x="Year",
        y="Growth_Pct",
        markers=True,
    )

    fig.update_traces(
        line=dict(
            color="#BE123C",
            width=3,
        ),
        marker=dict(
            color="#F43F5E",
            size=7,
        ),
        hovertemplate=(
            "<b>%{x}</b>"
            "<br>Crescimento: %{y:.1f}%"
            "<extra></extra>"
        ),
    )

    fig.add_hline(
        y=0,
        line_dash="dash",
        line_color="rgba(148,163,184,.35)",
        line_width=1,
    )

    fig.update_layout(
        showlegend=False,
        hovermode="x unified",
    )

    fig.update_xaxes(
        title_text="Ano",
        dtick=1,
    )

    fig.update_yaxes(
        title_text="Crescimento do capital (%)",
    )

    return fig

    def create_average_valuation_by_industry_chart(df):
        if df.empty:
            return empty_figure()

        dados = (
            df[["Industry", "Valuation_USD"]]
            .dropna()
            .groupby("Industry", as_index=False)["Valuation_USD"]
            .mean()
        )

        if dados.empty:
            return empty_figure()

        dados["Average_Valuation_B"] = dados["Valuation_USD"] / 1e9

        dados = (
            dados
            .sort_values("Average_Valuation_B", ascending=False)
            .head(10)
            .sort_values("Average_Valuation_B", ascending=True)
        )

        fig = px.bar(
            dados,
            x="Average_Valuation_B",
            y="Industry",
            orientation="h",
            color="Average_Valuation_B",
            color_continuous_scale=[
                "#5C2D05",
                "#7C3F08",
                "#92400E",
                "#B45309",
                "#D97706",
                "#F59E0B",
            ],
            labels={
                "Average_Valuation_B": "Valuation Médio (US$ bi)",
                "Industry": "Indústria",
            },
        )

        fig.update_traces(
            hovertemplate=(
                "<b>%{y}</b><br>"
                "Valuation médio: US$ %{x:.2f} bi"
                "<extra></extra>"
            )
        )

        fig.update_coloraxes(showscale=False)

        return fig


def create_valuation_vs_investment_chart(df):
    if df.empty:
        return empty_figure()

    dados = (
        df[
            [
                "Funding_Amount_USD",
                "Valuation_USD",
                "Industry",
                "Country",
            ]
        ]
        .dropna()
        .copy()
    )

    if dados.empty:
        return empty_figure()

    dados["Funding_T"] = dados["Funding_Amount_USD"] / 1e12
    dados["Valuation_T"] = dados["Valuation_USD"] / 1e12

    # Amostra menor deixa as cores por indústria distinguíveis.
    if len(dados) > 4000:
        dados = dados.sample(4000, random_state=42)

    # Ordem alfabetica, com EdTech deslocada para o fim da legenda.
    # A cor de cada industria continua vindo da posicao alfabetica,
    # entao reordenar a legenda nao troca as cores do grafico.
    industrias = sorted(dados["Industry"].unique())

    cores = {
        industria: INDUSTRY_COLORS[i % len(INDUSTRY_COLORS)]
        for i, industria in enumerate(industrias)
    }

    if "EdTech" in industrias:
        industrias.remove("EdTech")
        industrias.append("EdTech")

    dados["Industry"] = pd.Categorical(
        dados["Industry"],
        categories=industrias,
        ordered=True,
    )

    dados = dados.sort_values("Industry")

    fig = px.scatter(
        dados,
        x="Funding_T",
        y="Valuation_T",
        color="Industry",
        color_discrete_map=cores,
        category_orders={"Industry": industrias},
        hover_data=["Country", "Industry"],
        render_mode="webgl",
        labels={
            "Funding_T": "Investimento Captado (US$ tri)",
            "Valuation_T": "Valuation (US$ tri)",
            "Industry": "Indústria",
            "Country": "País",
        },
    )

    fig.update_traces(
        marker=dict(
            size=5,
            opacity=0.45,
            line=dict(width=0),
        ),
        hovertemplate=(
            "<b>%{fullData.name}</b><br>"
            "País: %{customdata[0]}<br>"
            "Investimento: US$ %{x:.6f} tri<br>"
            "Valuation: US$ %{y:.5f} tri"
            "<extra></extra>"
        ),
    )

    # A nuvem e densa e uniforme: abrir ja aproximado num recorte
    # espalha os pontos e deixa as cores por industria legiveis.
    # Duplo clique ou scroll volta para a visao completa.
    x_zoom = dados["Funding_T"].quantile(0.30)
    y_zoom = dados["Valuation_T"].quantile(0.30)

    fig.update_xaxes(
        range=[0, x_zoom],
        tickformat=".5f",
        nticks=6,
    )
    fig.update_yaxes(
        range=[0, y_zoom],
        tickformat=".4f",
        nticks=6,
    )

    fig.update_layout(
        legend=dict(
            orientation="h",
            yanchor="top",
            y=-0.22,
            xanchor="center",
            x=0.5,
            title_text="",
            font=dict(size=10),
            itemsizing="constant",
            # Reserva uma fatia fixa da largura por item: sem isso o
            # Plotly dimensiona pelo texto original e a traducao
            # automatica do navegador faz os rotulos se sobreporem.
            entrywidth=0.25,
            entrywidthmode="fraction",
            tracegroupgap=4,
        ),
    )

    return fig


def create_valuation_evolution_chart(df):
    if df.empty:
        return empty_figure()

    dados = (
        df[["Year", "Valuation_USD"]]
        .dropna()
        .groupby("Year", as_index=False)["Valuation_USD"]
        .mean()
    )

    if dados.empty:
        return empty_figure()

    dados["Average_Valuation_B"] = dados["Valuation_USD"] / 1e9

    fig = px.line(
        dados,
        x="Year",
        y="Average_Valuation_B",
        markers=True,
        labels={
            "Year": "Ano",
            "Average_Valuation_B": "Valuation Médio (US$ bi)",
        },
    )

    fig.update_traces(
        line=dict(
            color="#F59E0B",
            width=3,
        ),
        marker=dict(
            color="#FBBF24",
            size=7,
        ),
        hovertemplate=(
            "Ano: %{x}<br>"
            "Valuation médio: US$ %{y:.2f} bi"
            "<extra></extra>"
        ),
    )

    return fig

def create_average_valuation_by_industry_chart(df):
    if df.empty:
        return empty_figure()

    dados = (
        df[["Industry", "Valuation_USD"]]
        .dropna()
        .groupby("Industry", as_index=False)["Valuation_USD"]
        .mean()
    )

    if dados.empty:
        return empty_figure()

    dados["Average_Valuation_B"] = dados["Valuation_USD"] / 1e9

    dados = (
        dados
        .sort_values("Average_Valuation_B", ascending=False)
        .head(10)
        .sort_values("Average_Valuation_B", ascending=True)
    )

    fig = px.bar(
        dados,
        x="Average_Valuation_B",
        y="Industry",
        orientation="h",
        color="Average_Valuation_B",
        color_continuous_scale=[
            "#261705",
            "#3D2508",
            "#563508",
            "#704509",
            "#8A550A",
            "#A66A10",
            "#C1841B",
        ],
        labels={
            "Average_Valuation_B": "Valuation Médio (US$ bi)",
            "Industry": "Indústria",
        },
    )

    fig.update_traces(
        marker_line_width=0,
        hovertemplate=(
            "<b>%{y}</b><br>"
            "Valuation médio: US$ %{x:.2f} bi"
            "<extra></extra>"
        ),
    )

    fig.update_coloraxes(showscale=False)

    return fig


def create_valuation_vs_investment_chart(df):
    if df.empty:
        return empty_figure()

    dados = (
        df[
            [
                "Funding_Amount_USD",
                "Valuation_USD",
                "Industry",
                "Country",
            ]
        ]
        .dropna()
        .copy()
    )

    if dados.empty:
        return empty_figure()

    dados["Funding_T"] = dados["Funding_Amount_USD"] / 1e12
    dados["Valuation_T"] = dados["Valuation_USD"] / 1e12

    # Amostra menor deixa as cores por indústria distinguíveis.
    if len(dados) > 4000:
        dados = dados.sample(4000, random_state=42)

    # Ordem alfabetica, com EdTech deslocada para o fim da legenda.
    # A cor de cada industria continua vindo da posicao alfabetica,
    # entao reordenar a legenda nao troca as cores do grafico.
    industrias = sorted(dados["Industry"].unique())

    cores = {
        industria: INDUSTRY_COLORS[i % len(INDUSTRY_COLORS)]
        for i, industria in enumerate(industrias)
    }

    if "EdTech" in industrias:
        industrias.remove("EdTech")
        industrias.append("EdTech")

    dados["Industry"] = pd.Categorical(
        dados["Industry"],
        categories=industrias,
        ordered=True,
    )

    dados = dados.sort_values("Industry")

    fig = px.scatter(
        dados,
        x="Funding_T",
        y="Valuation_T",
        color="Industry",
        color_discrete_map=cores,
        category_orders={"Industry": industrias},
        hover_data=["Country", "Industry"],
        render_mode="webgl",
        labels={
            "Funding_T": "Investimento Captado (US$ tri)",
            "Valuation_T": "Valuation (US$ tri)",
            "Industry": "Indústria",
            "Country": "País",
        },
    )

    fig.update_traces(
        marker=dict(
            size=5,
            opacity=0.45,
            line=dict(width=0),
        ),
        hovertemplate=(
            "<b>%{fullData.name}</b><br>"
            "País: %{customdata[0]}<br>"
            "Investimento: US$ %{x:.6f} tri<br>"
            "Valuation: US$ %{y:.5f} tri"
            "<extra></extra>"
        ),
    )

    # A nuvem e densa e uniforme: abrir ja aproximado num recorte
    # espalha os pontos e deixa as cores por industria legiveis.
    # Duplo clique ou scroll volta para a visao completa.
    x_zoom = dados["Funding_T"].quantile(0.30)
    y_zoom = dados["Valuation_T"].quantile(0.30)

    fig.update_xaxes(
        range=[0, x_zoom],
        tickformat=".5f",
        nticks=6,
    )
    fig.update_yaxes(
        range=[0, y_zoom],
        tickformat=".4f",
        nticks=6,
    )

    fig.update_layout(
        legend=dict(
            orientation="h",
            yanchor="top",
            y=-0.22,
            xanchor="center",
            x=0.5,
            title_text="",
            font=dict(size=10),
            itemsizing="constant",
            # Reserva uma fatia fixa da largura por item: sem isso o
            # Plotly dimensiona pelo texto original e a traducao
            # automatica do navegador faz os rotulos se sobreporem.
            entrywidth=0.25,
            entrywidthmode="fraction",
            tracegroupgap=4,
        ),
    )

    return fig


def create_valuation_evolution_chart(df):
    if df.empty:
        return empty_figure()

    dados = (
        df[["Year", "Valuation_USD"]]
        .dropna()
        .groupby("Year", as_index=False)["Valuation_USD"]
        .mean()
    )

    if dados.empty:
        return empty_figure()

    dados["Average_Valuation_B"] = dados["Valuation_USD"] / 1e9

    fig = px.line(
        dados,
        x="Year",
        y="Average_Valuation_B",
        markers=True,
        labels={
            "Year": "Ano",
            "Average_Valuation_B": "Valuation Médio (US$ bi)",
        },
    )

    fig.update_traces(
        line=dict(
            color="#B77912",
            width=2.5,
        ),
        marker=dict(
            color="#C1841B",
            size=6,
        ),
        hovertemplate=(
            "Ano: %{x}<br>"
            "Valuation médio: US$ %{y:.2f} bi"
            "<extra></extra>"
        ),
    )

    return fig

def create_unicorns_by_industry_chart(df):
    if df.empty:
        return empty_figure()

    dados = (
        df[["Industry", "Unicorn_Flag"]]
        .dropna()
        .groupby("Industry", as_index=False)["Unicorn_Flag"]
        .sum()
    )

    if dados.empty:
        return empty_figure()

    dados = (
        dados
        .rename(columns={"Unicorn_Flag": "Unicorns"})
        .sort_values("Unicorns", ascending=True)
        .tail(10)
    )

    fig = px.bar(
        dados,
        x="Unicorns",
        y="Industry",
        orientation="h",
        color="Unicorns",
        color_continuous_scale=[
            "#211334",
            "#35204F",
            "#4C2870",
            "#62359A",
            "#7046B8",
            "#7C3AED",
        ],
        labels={
            "Unicorns": "Quantidade de Unicórnios",
            "Industry": "Indústria",
        },
    )

    fig.update_traces(
        marker_line_width=0,
        hovertemplate=(
            "<b>%{y}</b><br>"
            "Unicórnios: %{x:,}"
            "<extra></extra>"
        ),
    )

    fig.update_coloraxes(showscale=False)

    return fig


def create_unicorn_valuation_boxplot(df):
    if df.empty:
        return empty_figure()

    dados = (
        df[
            [
                "Valuation_USD",
                "Unicorn_Flag",
            ]
        ]
        .dropna()
        .copy()
    )

    if dados.empty:
        return empty_figure()

    dados["Tipo"] = dados["Unicorn_Flag"].map(
        {
            0: "Não Unicórnio",
            1: "Unicórnio",
        }
    )

    dados = dados.dropna(subset=["Tipo"])

    dados["Valuation_B"] = dados["Valuation_USD"] / 1e9

    fig = px.box(
        dados,
        x="Tipo",
        y="Valuation_B",
        color="Tipo",
        color_discrete_map={
            "Não Unicórnio": "#4A3A5E",
            "Unicórnio": "#8B5CF6",
        },
        labels={
            "Tipo": "",
            "Valuation_B": "Valuation (US$ bi)",
        },
        points=False,
    )

    fig.update_traces(
        line=dict(width=1.4),
        fillcolor="rgba(139,92,246,0.16)",
        hovertemplate=(
            "<b>%{x}</b><br>"
            "Valuation: US$ %{y:.2f} bi"
            "<extra></extra>"
        ),
    )

    return fig


def create_unicorn_funding_valuation_scatter(df):
    if df.empty:
        return empty_figure()

    dados = (
        df[
            [
                "Funding_Amount_USD",
                "Valuation_USD",
                "Unicorn_Flag",
                "Industry",
                "Country",
            ]
        ]
        .dropna()
        .copy()
    )

    if dados.empty:
        return empty_figure()

    dados["Tipo"] = dados["Unicorn_Flag"].map(
        {
            0: "Não Unicórnio",
            1: "Unicórnio",
        }
    )

    dados = dados.dropna(subset=["Tipo"])

    dados["Funding_B"] = dados["Funding_Amount_USD"] / 1e9
    dados["Valuation_B"] = dados["Valuation_USD"] / 1e9

    if len(dados) > 10000:
        dados = dados.sample(10000, random_state=42)

    fig = px.scatter(
        dados,
        x="Funding_B",
        y="Valuation_B",
        color="Tipo",
        hover_data=["Industry", "Country"],
        render_mode="webgl",
        color_discrete_map={
            "Não Unicórnio": "#4A3A5E",
            "Unicórnio": "#8B5CF6",
        },
        labels={
            "Funding_B": "Investimento Captado (US$ bi)",
            "Valuation_B": "Valuation (US$ bi)",
            "Tipo": "",
        },
    )

    fig.update_traces(
        marker=dict(
            size=5,
            opacity=0.42,
        ),
        hovertemplate=(
            "<b>%{customdata[0]}</b><br>"
            "País: %{customdata[1]}<br>"
            "Investimento: US$ %{x:.2f} bi<br>"
            "Valuation: US$ %{y:.2f} bi"
            "<extra></extra>"
        ),
    )

    return fig


def create_unicorn_evolution_chart(df):
    if df.empty:
        return empty_figure()

    dados = (
        df[["Year", "Unicorn_Flag"]]
        .dropna()
        .groupby("Year", as_index=False)["Unicorn_Flag"]
        .sum()
    )

    if dados.empty:
        return empty_figure()

    dados = dados.rename(
        columns={
            "Unicorn_Flag": "Unicorns",
        }
    )

    fig = px.line(
        dados,
        x="Year",
        y="Unicorns",
        markers=True,
        labels={
            "Year": "Ano",
            "Unicorns": "Quantidade de Unicórnios",
        },
    )

    fig.update_traces(
        line=dict(
            color="#7651B8",
            width=2.5,
        ),
        marker=dict(
            color="#8B5CF6",
            size=6,
        ),
        hovertemplate=(
            "Ano: %{x}<br>"
            "Unicórnios: %{y:,}"
            "<extra></extra>"
        ),
    )

    return fig

def create_unicorns_by_country_chart(df):
    if df.empty:
        return empty_figure()

    dados = (
        df[["Country", "Unicorn_Flag"]]
        .dropna()
        .groupby("Country", as_index=False)["Unicorn_Flag"]
        .sum()
    )

    if dados.empty:
        return empty_figure()

    dados = (
        dados
        .rename(columns={"Unicorn_Flag": "Unicorns"})
        .sort_values("Unicorns", ascending=True)
        .tail(10)
    )

    fig = px.bar(
        dados,
        x="Unicorns",
        y="Country",
        orientation="h",
        color="Unicorns",
        color_continuous_scale=[
            "#211334",
            "#35204F",
            "#4C2870",
            "#5B3288",
            "#6940A0",
            "#7651B8",
            "#8B5CF6",
        ],
        labels={
            "Unicorns": "Quantidade de Unicórnios",
            "Country": "País",
        },
    )

    fig.update_traces(
        marker_line_width=0,
        hovertemplate=(
            "<b>%{y}</b><br>"
            "Unicórnios: %{x:,}"
            "<extra></extra>"
        ),
    )

    fig.update_coloraxes(showscale=False)

    return fig