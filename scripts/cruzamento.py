import pandas as pd


def normaliza_municipio(serie):
    #Remove acentos, espaços e padroniza para maiúsculo.
    return (
        serie.astype(str)
             .str.normalize("NFKD")
             .str.encode("ascii", errors="ignore")
             .str.decode("utf-8")
             .str.strip()
             .str.upper()
    )


def conectar_sus_inmet_via_ibge(df_sus, df_ibge, df_inmet,coluna_cod_sus="CODMUNRES"):
    """
    Conecta as três bases com o IBGE como ponte:

        SUS (código 6 dig) -> IBGE (nome + UF) -> INMET

    """

    sus   = df_sus.copy()
    ibge  = df_ibge.copy()
    inmet = df_inmet.copy()

    # 7 dígitos -> 6 dígitos (remove o dígito verificador)
    ibge["cod_6dig"] = (
        ibge["Código Município Completo"]
        .astype(str).str.replace(".0", "", regex=False)
        .str.zfill(7).str[:6]
        .astype(int)
    )
    ibge["municipio_norm"] = normaliza_municipio(ibge["Nome_Município"])

    if "UF" not in ibge.columns:
        ibge["UF"] = "RJ"
    else:
        ibge["UF"] = ibge["UF"].str.strip().str.upper()

    inmet["municipio_norm"] = normaliza_municipio(inmet["municipio_inmet"])
    inmet["UF"]             = inmet["UF"].str.strip().str.upper()

    inmet["Data Medicao"] = pd.to_datetime(inmet["Data Medicao"], errors="coerce")
    inmet["Data Medicao_date"] = inmet["Data Medicao"].dt.normalize()

    inmet["temp_float"] = (
        inmet["TEMPERATURA MEDIA, DIARIA (AUT)(°C)"]
        .astype(str).str.replace(",", ".")
        .pipe(pd.to_numeric, errors="coerce")
    )
    inmet["precip_float"] = pd.to_numeric(
        inmet["PRECIPITACAO TOTAL, DIARIO (AUT)(mm)"], errors="coerce"
    )
    inmet["umidade_float"] = pd.to_numeric(
        inmet["UMIDADE RELATIVA DO AR, MEDIA DIARIA (AUT)(%)"], errors="coerce"
    )

    inmet = inmet.merge(
        ibge[["cod_6dig", "municipio_norm", "UF", "Nome_Município"]],
        on=["municipio_norm", "UF"],
        how="left"
    )

    inmet_por_dia = (
        inmet
        .groupby(["cod_6dig", "Data Medicao_date", "municipio_inmet", "UF", "Nome_Município"], as_index=False)
        .agg(
            **{"Data Medicao": ("Data Medicao", "first")},
            temp_media         = ("temp_float", "mean"),
            precip_media       = ("precip_float", "mean"),
            umidade_media      = ("umidade_float", "mean"),
        )
    )

    sus["cod_municipio_6dig"] = (
        sus[coluna_cod_sus]
        .astype(str).str.replace(".0", "", regex=False)
        .str[:6]
        .pipe(pd.to_numeric, errors="coerce")
        .astype("Int64")
    )

    sus["DTOBITO"] = pd.to_datetime(sus["DTOBITO"], format="%d%m%Y", errors="coerce")
    sus["DTOBITO_date"] = sus["DTOBITO"].dt.normalize()

    #SUS x INMET por código de município e data
    df_completo = sus.merge(
        inmet_por_dia[[
            "cod_6dig", "Data Medicao", "Data Medicao_date",
            "municipio_inmet", "UF",
            "temp_media", "precip_media", "umidade_media"
        ]],
        left_on=["cod_municipio_6dig", "DTOBITO_date"],
        right_on=["cod_6dig", "Data Medicao_date"],
        how="left"
    )

    return df_completo