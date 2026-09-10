import streamlit as st
from pathlib import Path
from src.data import load_data
from src.filters import render_filters, apply_filters
from src.metrics import calculate_metrics
from src.charts import (
    create_funding_map,
    create_industry_evolution_chart,
    create_valuation_boxplot,
    create_ranking_chart,
    create_country_investment_chart,
    create_average_investment_chart,
    create_country_scatter_chart,
    create_country_industry_heatmap,
    create_investment_evolution_chart,
    create_average_ticket_by_round_chart,
    create_rounds_evolution_chart,
    create_funding_by_round_evolution_chart,
    create_capital_evolution_chart,
    create_growth_evolution_chart,
    create_average_valuation_by_industry_chart,
    create_valuation_vs_investment_chart,
    create_valuation_evolution_chart,
    create_unicorns_by_industry_chart,
    create_unicorn_valuation_boxplot,
    create_unicorn_funding_valuation_scatter,
    create_unicorn_evolution_chart,
    create_unicorns_by_country_chart,
)
from src.ui import apply_chart_theme, metric_card

BASE_DIR = Path(__file__).resolve().parent

DATA_FILE = BASE_DIR / "data" / "Startup_Funding_Analytics_150k.csv"
IMAGE_FILE = BASE_DIR / "assets" / "Logo.png"


st.set_page_config(
    page_title="Dashboard - Startup Funding",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ==========================================================
# DESIGN SYSTEM
# ==========================================================
BG = "#0B1220"
BG_ALT = "#0E1728"
SIDEBAR_BG = "#0A101C"
PANEL = "#111C2E"
PANEL_HOVER = "#152238"
BORDER = "rgba(148, 163, 184, 0.16)"
TEXT = "#F8FAFC"
TEXT_MUTED = "#A8B3C7"
TEXT_SOFT = "#7F8CA3"
GRID = "rgba(148, 163, 184, 0.10)"

BLUE = "#3B82F6"
CYAN = "#22D3EE"
VIOLET = "#8B5CF6"
AMBER = "#F59E0B"
EMERALD = "#10B981"
ROSE = "#F43F5E"


# ==========================================================
# PALETAS DOS GRÁFICOS
# ==========================================================
QUALITATIVE = [
    "#5B6E8C",
    "#7A6F9B",
    "#5F8F87",
    "#A48762",
    "#8C6570",
    "#627D9D",
    "#786C82",
    "#6F8779",
]

BAR_PALETTE = [
    "#1E3A5F",
    "#2563EB",
    "#3B82F6",
    "#4F46E5",
    "#6366F1",
    "#7C3AED",
    "#8B5CF6",
]

MAP_SCALE = [
    [0.00, "#172554"],
    [0.20, "#1E3A8A"],
    [0.45, "#1D4ED8"],
    [0.70, "#0284C7"],
    [1.00, "#22D3EE"],
]

AMBER_PALETTE = [
    "#3D2508",
    "#563508",
    "#704509",
    "#8A550A",
    "#A66A10",
    "#C1841B",
    "#D49A2A",
]

# ==========================================================
# CSS
# ==========================================================
CSS_FILE = BASE_DIR / "assets" / "style.css"

css = CSS_FILE.read_text(
    encoding="utf-8"
)

st.markdown(
    f"<style>{css}</style>",
    unsafe_allow_html=True,
)


# ==========================================================
# DATA
# ==========================================================
df = load_data(DATA_FILE)


# ==========================================================
# SIDEBAR
# ==========================================================
(
    pais_selecionado,
    industria_selecionada,
    ano_inicial,
    ano_final,
    metrica_ranking,
) = render_filters(df)

# ==========================================================
# APLICAÇÃO DOS FILTROS
# ==========================================================
df_filtrado = apply_filters(
    df,
    pais_selecionado,
    industria_selecionada,
    ano_inicial,
    ano_final,
)

(
    total_startups,
    total_investimento,
    media_valuation,
    percentual_unicornios,
) = calculate_metrics(df_filtrado)

# ==========================================================
# ABAS DO DASHBOARD
# ==========================================================
tab_visao_geral, tab_mercado, tab_evolucao, tab_valuation, tab_unicornios = st.tabs(
    [
        "Visão Geral",
        "Mercado & Geografia",
        "Evolução & Crescimento",
        "Valuation & Desempenho",
        "Unicórnios",
    ]
)


with tab_visao_geral:

    # ==========================================================
    # KPI CARDS
    # ==========================================================
    with st.container():

        col1, col2, col3, col4 = st.columns(4)

        # ------------------------------------------------------
        # KPI 1
        # ------------------------------------------------------
        with col1:

            metric_card(
                f"{total_startups:,}",
                "Total Startups",
                f"{ano_inicial}–{ano_final}",
                CYAN,
                "#102F4A",
            )

        # ------------------------------------------------------
        # KPI 2
        # ------------------------------------------------------
        with col2:

            metric_card(
                f"${total_investimento:.2f}T",
                "Total Investimento",
                "Capital acumulado no recorte",
                ROSE,
                "#3A202B",
            )

        # ------------------------------------------------------
        # KPI 3
        # ------------------------------------------------------
        with col3:

            metric_card(
                f"${media_valuation:.1f}B",
                "Média Valuation",
                "Média das empresas filtradas",
                AMBER,
                "#3B3018",
            )

        # ------------------------------------------------------
        # KPI 4
        # ------------------------------------------------------
        with col4:

            metric_card(
                f"{percentual_unicornios:.1f}%",
                "Unicórnios",
                "Participação no recorte",
                VIOLET,
                "#302044",
            )

    # ==========================================================
    # GRÁFICOS — LINHA 1
    # ==========================================================
    with st.container():

        st.markdown(
            '<h3 class="section-title">'
            'Panorama do Mercado de Startups'
            '</h3>',
            unsafe_allow_html=True,
        )

        col1, col2 = st.columns(2)

        # ======================================================
        # MAPA
        # ======================================================
        with col1:

            fig1 = create_funding_map(
                df_filtrado,
                MAP_SCALE,
            )

            apply_chart_theme(
                fig1,
                "Capital Captado por País (US$ Bilhões)",
                height=400,
                showlegend=False,
            )

            fig1.update_layout(

                geo=dict(
                    bgcolor="rgba(0,0,0,0)",
                    showframe=False,
                    showcoastlines=False,
                    showland=True,
                    landcolor="#172236",
                    showcountries=True,
                    countrycolor="#334155",
                    countrywidth=0.7,
                    showocean=True,
                    oceancolor="#0E1728",
                    showlakes=True,
                    lakecolor="#0E1728",
                    projection_scale=1.03,
                ),

                coloraxis_colorbar=dict(
                    title="US$ B",
                    thickness=9,
                    len=0.62,
                    x=0.98,
                    outlinewidth=0,

                    tickfont=dict(
                        color=TEXT_MUTED,
                        size=10,
                    ),

                    title_font=dict(
                        color=TEXT_MUTED,
                        size=10,
                    ),
                ),
            )

            fig1.update_traces(

                marker_line_color="#0B1220",
                marker_line_width=0.55,

                hovertemplate=(
                    "<b>%{hovertext}</b>"
                    "<br>US$ %{z:.2f} bi"
                    "<extra></extra>"
                ),
            )

            st.plotly_chart(
                fig1,
                use_container_width=True,
                config={
                    "displayModeBar": False
                },
            )

           # ======================================================
        # RANKING DINÂMICO
        # ======================================================
        with col2:

            if metrica_ranking == "Investimento":

                ranking = (
                    df_filtrado
                    .groupby("Industry")[
                        "Funding_Amount_USD"
                    ]
                    .sum()
                    .reset_index()
                )

                ranking["Metric"] = (
                    ranking[
                        "Funding_Amount_USD"
                    ]
                )

                titulo_ranking = (
                    "Investimento por Indústria"
                )

                eixo_x = "Investimento (USD)"

                hover_template = (
                    "<b>%{y}</b>"
                    "<br>US$ %{x:,.0f}"
                    "<extra></extra>"
                )

            elif metrica_ranking == "Número de Startups":

                ranking = (
                    df_filtrado
                    .groupby("Industry")
                    .size()
                    .reset_index(
                        name="Startup_Count"
                    )
                )

                ranking["Metric"] = (
                    ranking[
                        "Startup_Count"
                    ]
                )

                titulo_ranking = (
                    "Número de Startups por Indústria"
                )

                eixo_x = "Startups"

                hover_template = (
                    "<b>%{y}</b>"
                    "<br>%{x:,.0f} startups"
                    "<extra></extra>"
                )

            else:

                ranking = (
                    df_filtrado
                    .groupby("Industry")[
                        "Valuation_USD"
                    ]
                    .mean()
                    .reset_index()
                )

                ranking["Metric"] = (
                    ranking[
                        "Valuation_USD"
                    ]
                )

                titulo_ranking = (
                    "Valuation Médio por Indústria"
                )

                eixo_x = "Valuation Médio (USD)"

                hover_template = (
                    "<b>%{y}</b>"
                    "<br>US$ %{x:,.0f}"
                    "<extra></extra>"
                )

            ranking = ranking.sort_values(
                "Metric",
                ascending=True,
            )

            values = (
                ranking["Metric"]
                .tolist()
            )

            if (
                len(values) > 1
                and max(values) != min(values)
            ):

                normalized = [

                    (
                        v - min(values)
                    )
                    / (
                        max(values)
                        - min(values)
                    )

                    for v in values
                ]

            else:

                normalized = [
                    0.65
                ] * len(values)

            colors = [

                BAR_PALETTE[
                    min(
                        int(
                            n
                            * (
                                len(BAR_PALETTE)
                                - 1
                            )
                        ),
                        len(BAR_PALETTE)
                        - 1,
                    )
                ]

                for n in normalized
            ]

            fig2 = create_ranking_chart(
                ranking,
            )

            apply_chart_theme(
                fig2,
                titulo_ranking,
                height=400,
                showlegend=False,
            )

            fig2.update_traces(

                marker=dict(
                    color=colors,

                    line=dict(
                        color="rgba(255,255,255,.08)",
                        width=1,
                    ),
                ),

                opacity=0.96,

                hovertemplate=hover_template,
            )

            fig2.update_xaxes(
                title_text=eixo_x,
                tickformat="~s",
            )

            fig2.update_yaxes(

                showgrid=False,

                categoryorder="array",

                categoryarray=(
                    ranking[
                        "Industry"
                    ].tolist()
                ),
            )

            st.plotly_chart(
                fig2,
                use_container_width=True,
                config={
                    "displayModeBar": False
                },
            )
    # ==========================================================
    # GRÁFICOS — LINHA 2
    # ==========================================================
    with st.container():

        st.markdown(
            '<h3 class="section-title">'
            'Evolução e Distribuição'
            '</h3>',
            unsafe_allow_html=True,
        )

        col3, col4 = st.columns(2)

        # ======================================================
        # LINHAS
        # ======================================================
        with col3:

            fig3 = create_industry_evolution_chart(
                df_filtrado,
                QUALITATIVE,
            )

            apply_chart_theme(
                fig3,
                "Evolução Temporal por Indústria",
                height=400,
                showlegend=True,
            )

            fig3.update_traces(
                line=dict(
                    width=2
                ),

                marker=dict(
                    size=4
                ),

                opacity=0.82,
            )

            fig3.update_xaxes(
                showgrid=False,
                title_text="",
            )

            fig3.update_yaxes(

                showgrid=True,
                gridcolor=GRID,
                title_text="Quantidade",
            )

            st.plotly_chart(
                fig3,
                use_container_width=True,
                config={
                    "displayModeBar": False
                },
            )

        # ======================================================
        # BOX PLOT
        # ======================================================
        with col4:

            fig4 = create_valuation_boxplot(
                df_filtrado,
                QUALITATIVE,
            )

            apply_chart_theme(
                fig4,
                "Distribuição de Valuation por Setor",
                height=400,
                showlegend=False,
            )

            fig4.update_traces(

                line=dict(
                    width=1.1
                ),

                marker=dict(
                    size=2.5,
                    opacity=0.35,
                ),
            )

            fig4.update_xaxes(
                showgrid=False,
                tickangle=-25,
            )

            fig4.update_yaxes(

                showgrid=True,
                gridcolor=GRID,
                tickformat="~s",
            )

            st.plotly_chart(
                fig4,
                use_container_width=True,
                config={
                    "displayModeBar": False
                },
            )
# ==========================================================
# ABAS
# ==========================================================
with tab_mercado:

    maior_pais_valor = (
    df_filtrado
    .groupby("Country")["Funding_Amount_USD"]
    .sum()
    .max()
    / 1e12
    if not df_filtrado.empty
    else 0
)

    if maior_pais_valor != maior_pais_valor:
        maior_pais_valor = 0

    maior_pais = (
        df_filtrado
        .groupby("Country")["Funding_Amount_USD"]
        .sum()
        .idxmax()
        if not df_filtrado.empty
        else "—"
    )

    maior_industria_valor = (
    df_filtrado
    .groupby("Industry")["Funding_Amount_USD"]
    .sum()
    .max()
    / 1e12
    if not df_filtrado.empty
    else 0
    )

    maior_industria = (
        df_filtrado
        .groupby("Industry")["Funding_Amount_USD"]
        .sum()
        .idxmax()
        if not df_filtrado.empty
        else "—"
    )

    total_paises = df_filtrado["Country"].nunique()
    total_industrias = df_filtrado["Industry"].nunique()

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        metric_card(
            f"${maior_pais_valor:.2f}T",
            "Maior País",
            maior_pais,
            CYAN,
            "#102F4A",
        )

    with col2:
        metric_card(
            f"${maior_industria_valor:.2f}T",
            "Maior Indústria",
            maior_industria,
            ROSE,
            "#3A202B",
        )

    with col3:
        metric_card(
            total_paises,
            "Países",
            "No período filtrado",
            AMBER,
            "#3B3018",
        )

    with col4:
        metric_card(
            total_industrias,
            "Indústrias",
            "No período filtrado",
            VIOLET,
            "#302044",
        )

    st.markdown(
        '<h3 class="section-title">Mercado & Geografia</h3>',
        unsafe_allow_html=True,
    )

    col1, col2 = st.columns(2)

    with col1:
        fig = create_country_investment_chart(
            df_filtrado
        )

        fig = apply_chart_theme(
            fig,
            "Ranking de Investimento por País",
            height=400,
            showlegend=False,
        )

        st.plotly_chart(
            fig,
            use_container_width=True,
        )

    with col2:
        fig = create_average_investment_chart(
            df_filtrado
        )

        fig = apply_chart_theme(
            fig,
            "Investimento Médio por Startup",
            height=400,
            showlegend=False,
        )

        st.plotly_chart(
            fig,
            use_container_width=True,
        )

    col1, col2 = st.columns(2)

    with col1:
        fig = create_country_industry_heatmap(
            df_filtrado
        )

        fig = apply_chart_theme(
            fig,
            "Startups por País e Indústria",
            height=520,
            showlegend=False,
        )

        st.plotly_chart(
            fig,
            use_container_width=True,
        )

    with col2:
        fig = create_country_scatter_chart(
            df_filtrado
        )

        fig = apply_chart_theme(
            fig,
            "Startups × Investimento por País",
            height=520,
            showlegend=False,
        )

        st.plotly_chart(
            fig,
            use_container_width=True,
        )

with tab_evolucao:

    # ==========================================================
    # KPI CARDS
    # ==========================================================

    capital_por_ano = (
        df_filtrado
        .groupby("Year")["Funding_Amount_USD"]
        .sum()
        .sort_index()
    )

    crescimentos = (
        capital_por_ano
        .pct_change()
        .replace(
            [float("inf"), -float("inf")],
            float("nan"),
        )
        .dropna()
        * 100
    )

    crescimento_medio = (
        crescimentos.mean()
        if not crescimentos.empty
        else 0
    )

    total_rodadas = len(df_filtrado)

    ano_pico = (
        capital_por_ano.idxmax()
        if not capital_por_ano.empty
        else "—"
    )

    capital_pico = (
        capital_por_ano.max() / 1e12
        if not capital_por_ano.empty
        else 0
    )

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        metric_card(
            f"${capital_pico:.2f}T",
            "Pico de Capital",
            f"Ano {ano_pico}",
            CYAN,
            "#102F4A",
        )

    with col2:
        metric_card(
            f"{crescimento_medio:.1f}%",
            "Crescimento Médio",
            "Variação anual do capital",
            ROSE,
            "#3A202B",
        )

    with col3:
        metric_card(
            f"{total_rodadas:,}",
            "Rodadas",
            "No período filtrado",
            AMBER,
            "#3B3018",
        )

    with col4:
        metric_card(
            str(ano_final),
            "Último Ano",
            "No período filtrado",
            VIOLET,
            "#302044",
        )

    # ==========================================================
    # TÍTULO
    # ==========================================================

    st.markdown(
        '<h3 class="section-title">'
        'Evolução & Crescimento'
        '</h3>',
        unsafe_allow_html=True,
    )

    # ==========================================================
    # LINHA 1
    # ==========================================================

    col1, col2 = st.columns(2)

    with col1:
        fig = create_capital_evolution_chart(
            df_filtrado
        )

        fig = apply_chart_theme(
            fig,
            "Capital Captado ao Longo dos Anos",
            height=420,
            showlegend=False,
        )

        st.plotly_chart(
            fig,
            use_container_width=True,
        )

    with col2:
        fig = create_growth_evolution_chart(
            df_filtrado
        )

        fig = apply_chart_theme(
            fig,
            "Crescimento Anual do Capital",
            height=420,
            showlegend=False,
        )

        st.plotly_chart(
            fig,
            use_container_width=True,
        )

    # ==========================================================
    # LINHA 2
    # ==========================================================

    col1, col2 = st.columns(2)

    with col1:
        fig = create_rounds_evolution_chart(
            df_filtrado
        )

        fig = apply_chart_theme(
            fig,
            "Rodadas de Investimento por Ano",
            height=420,
            showlegend=True,
        )

        st.plotly_chart(
            fig,
            use_container_width=True,
        )

    with col2:
        fig = create_average_ticket_by_round_chart(
            df_filtrado
        )

        fig = apply_chart_theme(
            fig,
            "Ticket Médio por Rodada",
            height=420,
            showlegend=False,
        )

        st.plotly_chart(
            fig,
            use_container_width=True,
        )

with tab_valuation:

    # =========================================================
    # KPIs — VALUATION & DESEMPENHO
    # =========================================================

    valuation = df_filtrado["Valuation_USD"].dropna()

    if not valuation.empty:
        valuation_media = valuation.mean() / 1e9
        valuation_mediana = valuation.median() / 1e9
        valuation_max = valuation.max() / 1e9
        valuation_acima_bilhao = int((valuation > 1e9).sum())
    else:
        valuation_media = 0
        valuation_mediana = 0
        valuation_max = 0
        valuation_acima_bilhao = 0

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        metric_card(
            f"${valuation_media:.2f}B",
            "Valuation Médio",
            "Média no período filtrado",
            CYAN,
            "#102F4A",
        )

    with col2:
        metric_card(
            f"${valuation_mediana:.2f}B",
            "Valuation Mediano",
            "Mediana no período filtrado",
            ROSE,
            "#3A202B",
        )

    with col3:
        metric_card(
            f"${valuation_max:.2f}B",
            "Maior Valuation",
            "Maior valor observado",
            AMBER,
            "#3B3018",
        )

    with col4:
        metric_card(
            f"{valuation_acima_bilhao:,}",
            "Valuation > US$ 1B",
            "Startups acima de US$ 1 bi",
            VIOLET,
            "#302044",
        )

    # =========================================================
    # TÍTULO DA SEÇÃO
    # =========================================================

    st.markdown(
        '<h3 class="section-title">Valuation & Desempenho</h3>',
        unsafe_allow_html=True,
    )

    # =========================================================
    # LINHA 1 — DISTRIBUIÇÃO + MÉDIA POR INDÚSTRIA
    # =========================================================

    col1, col2 = st.columns(2)

    with col1:
        fig = create_valuation_boxplot(
            df_filtrado,
            AMBER_PALETTE,
        )

        fig = apply_chart_theme(
            fig,
            "Distribuição de Valuation por Indústria",
            height=400,
            showlegend=False,
        )

        st.plotly_chart(
            fig,
            use_container_width=True,
            config={"displayModeBar": False},
        )

    with col2:
        fig = create_average_valuation_by_industry_chart(
            df_filtrado
        )

        fig = apply_chart_theme(
            fig,
            "Valuation Médio por Indústria",
            height=400,
            showlegend=False,
        )

        st.plotly_chart(
            fig,
            use_container_width=True,
            config={"displayModeBar": False},
        )

    # =========================================================
    # LINHA 2 — RELAÇÃO + EVOLUÇÃO
    # =========================================================

    col1, col2 = st.columns(2)

    with col1:
        fig = create_valuation_vs_investment_chart(
            df_filtrado
        )

        fig = apply_chart_theme(
            fig,
            "Valuation × Investimento",
            height=400,
            showlegend=True,
        )

        st.plotly_chart(
            fig,
            use_container_width=True,
            config={"displayModeBar": False},
        )

    with col2:
        fig = create_valuation_evolution_chart(
            df_filtrado
        )

        fig = apply_chart_theme(
            fig,
            "Evolução do Valuation Médio",
            height=400,
            showlegend=False,
        )

        st.plotly_chart(
            fig,
            use_container_width=True,
            config={"displayModeBar": False},
        )

with tab_unicornios:

    # =========================================================
    # KPIs — UNICÓRNIOS
    # =========================================================

    total_unicornios = int(
        df_filtrado["Unicorn_Flag"]
        .fillna(0)
        .sum()
    )

    total_registros = len(df_filtrado)

    percentual_unicornios = (
        (total_unicornios / total_registros) * 100
        if total_registros > 0
        else 0
    )

    dados_unicornio = df_filtrado[
        df_filtrado["Unicorn_Flag"] == 1
    ]

    if not dados_unicornio.empty:

        valuation_unicornio = (
            dados_unicornio["Valuation_USD"]
            .dropna()
            .mean()
            / 1e9
        )

        funding_unicornio = (
            dados_unicornio["Funding_Amount_USD"]
            .dropna()
            .mean()
            / 1e6
        )

    else:

        valuation_unicornio = 0
        funding_unicornio = 0

    # =========================================================
    # CARDS
    # =========================================================

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        metric_card(
            f"{total_unicornios:,}",
            "Total de Unicórnios",
            "Empresas com Unicorn Flag",
            CYAN,
            "#102F4A",
        )

    with col2:
        metric_card(
            f"{percentual_unicornios:.1f}%",
            "% de Unicórnios",
            "Participação no recorte",
            ROSE,
            "#3A202B",
        )

    with col3:
        metric_card(
            f"${valuation_unicornio:.2f}B",
            "Valuation Médio",
            "Entre os unicórnios",
            AMBER,
            "#3B3018",
        )

    with col4:
        metric_card(
            f"${funding_unicornio:.1f}M",
            "Funding Médio",
            "Entre os unicórnios",
            VIOLET,
            "#302044",
        )

    # =========================================================
    # TÍTULO
    # =========================================================

    st.markdown(
        '<h3 class="section-title">Unicórnios</h3>',
        unsafe_allow_html=True,
    )

    # =========================================================
    # LINHA 1
    # =========================================================

    col1, col2 = st.columns(2)

    with col1:

        fig = create_unicorns_by_industry_chart(
            df_filtrado
        )

        fig = apply_chart_theme(
            fig,
            "Unicórnios por Indústria",
            height=400,
            showlegend=False,
        )

        st.plotly_chart(
            fig,
            use_container_width=True,
            config={"displayModeBar": False},
        )

    with col2:

        fig = create_unicorn_valuation_boxplot(
            df_filtrado
        )

        fig = apply_chart_theme(
            fig,
            "Valuation: Unicórnios × Não Unicórnios",
            height=400,
            showlegend=False,
        )

        fig.update_xaxes(
            showgrid=False,
        )

        fig.update_yaxes(
            showgrid=True,
            gridcolor=GRID,
            tickformat="~s",
        )

        st.plotly_chart(
            fig,
            use_container_width=True,
            config={"displayModeBar": False},
        )

   # =========================================================
# LINHA 2
# =========================================================

    col1, col2 = st.columns(2)

    with col1:

        fig = create_unicorns_by_country_chart(
            df_filtrado
        )

        fig = apply_chart_theme(
            fig,
            "Unicórnios por País",
            height=400,
            showlegend=False,
        )

        fig.update_xaxes(
            showgrid=True,
            gridcolor=GRID,
        )

        fig.update_yaxes(
            showgrid=False,
        )

        st.plotly_chart(
            fig,
            use_container_width=True,
            config={"displayModeBar": False},
        )

    with col2:

        fig = create_unicorn_evolution_chart(
            df_filtrado
        )

        fig = apply_chart_theme(
            fig,
            "Evolução dos Unicórnios",
            height=400,
            showlegend=False,
        )

        fig.update_xaxes(
            showgrid=False,
        )

        fig.update_yaxes(
            showgrid=True,
            gridcolor=GRID,
        )

        st.plotly_chart(
            fig,
            use_container_width=True,
            config={"displayModeBar": False},
        )

# ==========================================================
# RODAPÉ
# ==========================================================
with st.container():

    st.markdown("---")

    st.markdown(
        f"""
        <p
            style='
                text-align:center;
                color:{TEXT_MUTED};
                font-size:13px;
            '
        >
            Dashboard desenvolvido para Atividade 2 -
            Pós em Engenharia de Dados
        </p>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        f"""
        <p
            style='
                text-align:center;
                color:{TEXT_SOFT};
                font-size:11px;
            '
        >
            Fonte: Startup Funding Analytics Dataset (Kaggle)
        </p>
        """,
        unsafe_allow_html=True,
    )