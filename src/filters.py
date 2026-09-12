import streamlit as st

CLICK_FILTER_SOURCES = [
    ("map_click", "flt_pais"),
    ("ranking_click", "flt_industrias"),
    ("country_investment_click", "flt_pais"),
    ("avg_investment_click", "flt_pais"),
    ("country_scatter_click", "flt_pais"),
    ("heatmap_click", "flt_pais"),
    ("heatmap_click", "flt_industrias"),
    ("capital_evolution_click", "flt_periodo"),
    ("growth_evolution_click", "flt_periodo"),
    ("rounds_evolution_click", "flt_periodo"),
    ("avg_ticket_click", "flt_periodo"),
    ("avg_valuation_click", "flt_industrias"),
    ("valuation_scatter_click", "flt_industrias"),
    ("valuation_evolution_click", "flt_periodo"),
    ("unicorns_industry_click", "flt_industrias"),
    ("unicorns_country_click", "flt_pais"),
    ("unicorn_evolution_click", "flt_periodo"),
]


def marker_key_for(event_key, filter_key):
    return f"_{event_key}__{filter_key}"


CROSS_FILTER_KEYS = list(
    {event_key for event_key, _ in CLICK_FILTER_SOURCES}
) + [
    marker_key_for(event_key, filter_key)
    for event_key, filter_key in CLICK_FILTER_SOURCES
]


def render_filters(df):
    with st.sidebar:
        st.image(
            "assets/Logo.png",
            use_container_width=True,
        )

        st.markdown("---")
        st.header("Filtros")

        ano_min = int(df["Year"].min())
        ano_max = int(df["Year"].max())

        industrias_disponiveis = sorted(
            df["Industry"].dropna().unique().tolist()
        )

        if st.button(
            "Redefinir filtros",
            width="stretch",
        ):
            for key in CROSS_FILTER_KEYS:
                st.session_state.pop(key, None)

            st.session_state["flt_pais"] = "Todos"
            st.session_state["flt_industrias"] = industrias_disponiveis
            st.session_state["flt_periodo"] = (ano_min, ano_max)
            st.rerun()

        paises_disponiveis = sorted(
            df["Country"].dropna().unique().tolist()
        )

        pais_selecionado = st.selectbox(
            "País",
            ["Todos"] + paises_disponiveis,
            key="flt_pais",
        )

        if "flt_industrias" not in st.session_state:
            st.session_state["flt_industrias"] = industrias_disponiveis

        industria_selecionada = st.multiselect(
            "Indústria",
            industrias_disponiveis,
            key="flt_industrias",
        )

        if ano_min < ano_max:
            if "flt_periodo" not in st.session_state:
                st.session_state["flt_periodo"] = (ano_min, ano_max)

            ano_inicial, ano_final = st.slider(
                "Período",
                min_value=ano_min,
                max_value=ano_max,
                step=1,
                key="flt_periodo",
            )
        else:
            ano_inicial = ano_min
            ano_final = ano_max

            st.caption(
                f"Período disponível: {ano_min}"
            )

        metrica_ranking = st.selectbox(
            "Métrica do ranking",
            [
                "Investimento",
                "Número de Startups",
                "Valuation Médio",
            ],
        )

    return (
        pais_selecionado,
        industria_selecionada,
        ano_inicial,
        ano_final,
        metrica_ranking,
    )


def apply_filters(
    df,
    pais_selecionado,
    industria_selecionada,
    ano_inicial,
    ano_final,
):
    df_filtrado = df.copy()

    if pais_selecionado != "Todos":
        df_filtrado = df_filtrado[
            df_filtrado["Country"] == pais_selecionado
        ]

    if industria_selecionada:
        df_filtrado = df_filtrado[
            df_filtrado["Industry"].isin(
                industria_selecionada
            )
        ]
    else:
        df_filtrado = df_filtrado.iloc[0:0]

    df_filtrado = df_filtrado[
        df_filtrado["Year"].between(
            ano_inicial,
            ano_final,
        )
    ].copy()

    return df_filtrado