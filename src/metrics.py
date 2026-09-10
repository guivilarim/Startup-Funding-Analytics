def calculate_metrics(df_filtrado):
    total_startups = len(df_filtrado)

    total_investimento = (
        df_filtrado["Total_Funding_USD"].sum() / 1e12
    )

    media_valuation = (
        df_filtrado["Valuation_USD"].mean() / 1e9
        if not df_filtrado.empty
        else 0
    )

    percentual_unicornios = (
        df_filtrado["Unicorn_Flag"].sum()
        / len(df_filtrado)
        * 100
        if not df_filtrado.empty
        else 0
    )

    return (
        total_startups,
        total_investimento,
        media_valuation,
        percentual_unicornios,
    )