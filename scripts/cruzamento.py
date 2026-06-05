# Cruzamentos (mínimo 4)

import pandas as pd
import unicodedata


def normalizar_texto(valor):
    """
    Padroniza textos para facilitar cruzamentos:
    - remove acentos
    - tira espaços extras
    - deixa tudo em maiúsculo
    """
    if pd.isna(valor):
        return None

    valor = str(valor).strip().upper()
    valor = unicodedata.normalize("NFKD", valor)
    valor = "".join(c for c in valor if not unicodedata.combining(c))

    return valor


def verificar_colunas(df, colunas, nome_base):
    """
    Verifica se as colunas necessárias existem no DataFrame.
    Se alguma não existir, mostra as colunas disponíveis.
    """
    colunas_faltando = [coluna for coluna in colunas if coluna not in df.columns]

    if colunas_faltando:
        raise KeyError(
            f"\nColunas não encontradas na base {nome_base}: {colunas_faltando}\n"
            f"Colunas disponíveis em {nome_base}:\n{df.columns.tolist()}"
        )


def criar_depara_inmet_ibge_sus(
    df_inmet,
    df_ibge,
    coluna_municipio_inmet,
    coluna_uf_inmet,
    coluna_codigo_inmet,
    coluna_municipio_ibge="Nome_Município",
    coluna_uf_ibge="UF",
    coluna_codigo_ibge="Código Município Completo"
):
    """
    Cria uma tabela de/para entre:
    INMET -> município/estação
    IBGE  -> município/código oficial
    SUS   -> código municipal usado na base de óbitos
    """

    inmet = df_inmet.copy()
    ibge = df_ibge.copy()

    verificar_colunas(
        inmet,
        [coluna_municipio_inmet, coluna_uf_inmet, coluna_codigo_inmet],
        "INMET"
    )

    verificar_colunas(
        ibge,
        [coluna_municipio_ibge, coluna_uf_ibge, coluna_codigo_ibge],
        "IBGE"
    )

    inmet = inmet[
        [
            coluna_codigo_inmet,
            coluna_municipio_inmet,
            coluna_uf_inmet
        ]
    ].drop_duplicates()

    inmet["municipio_norm"] = inmet[coluna_municipio_inmet].apply(normalizar_texto)
    ibge["municipio_norm"] = ibge[coluna_municipio_ibge].apply(normalizar_texto)

    inmet[coluna_uf_inmet] = (
        inmet[coluna_uf_inmet]
        .astype(str)
        .str.strip()
        .str.upper()
    )

    ibge[coluna_uf_ibge] = (
        ibge[coluna_uf_ibge]
        .astype(str)
        .str.strip()
        .str.upper()
    )

    ibge[coluna_codigo_ibge] = (
        ibge[coluna_codigo_ibge]
        .astype(str)
        .str.strip()
        .str.replace(".0", "", regex=False)
        .str.zfill(7)
    )

    ibge["codigo_municipio_sus"] = ibge[coluna_codigo_ibge].str[:6]

    ibge_reduzido = ibge[
        [
            "municipio_norm",
            coluna_uf_ibge,
            coluna_municipio_ibge,
            coluna_codigo_ibge,
            "codigo_municipio_sus"
        ]
    ].drop_duplicates()

    depara = inmet.merge(
        ibge_reduzido,
        left_on=["municipio_norm", coluna_uf_inmet],
        right_on=["municipio_norm", coluna_uf_ibge],
        how="left",
        suffixes=("_inmet", "_ibge")
    )

    depara = depara.rename(columns={
        coluna_codigo_inmet: "codigo_local_inmet",
        coluna_municipio_inmet: "municipio_inmet",
        coluna_uf_inmet: "uf_inmet",
        coluna_municipio_ibge: "nome_municipio_ibge",
        coluna_uf_ibge: "uf_ibge",
        coluna_codigo_ibge: "codigo_municipio_ibge_7"
    })

    colunas_finais = [
        "codigo_local_inmet",
        "municipio_inmet",
        "uf_inmet",
        "nome_municipio_ibge",
        "uf_ibge",
        "codigo_municipio_ibge_7",
        "codigo_municipio_sus"
    ]

    colunas_finais = [
        coluna for coluna in colunas_finais
        if coluna in depara.columns
    ]

    depara = depara[colunas_finais].drop_duplicates()

    return depara


def cruzar_sus_com_inmet(
    df_sus,
    depara,
    coluna_sus="CODMUNOCOR"
):
    """
    Junta a base SUS com o código/local do INMET usando o código do município.

    coluna_sus pode ser:
    - CODMUNOCOR: município onde ocorreu o óbito
    - CODMUNRES: município de residência da pessoa

    Importante:
    Se um município tiver mais de uma estação INMET, esta função mantém
    apenas uma estação por município para não duplicar os registros do SUS.
    """

    sus = df_sus.copy()
    depara_aux = depara.copy()

    verificar_colunas(
        sus,
        [coluna_sus],
        "SUS"
    )

    verificar_colunas(
        depara_aux,
        ["codigo_municipio_sus", "codigo_local_inmet"],
        "DEPARA INMET-IBGE-SUS"
    )

    sus[coluna_sus] = (
        sus[coluna_sus]
        .astype(str)
        .str.strip()
        .str.replace(".0", "", regex=False)
        .str[:6]
    )

    depara_aux["codigo_municipio_sus"] = (
        depara_aux["codigo_municipio_sus"]
        .astype(str)
        .str.strip()
        .str.replace(".0", "", regex=False)
        .str[:6]
    )

    colunas_para_trazer = [
        "codigo_municipio_sus",
        "codigo_local_inmet",
        "municipio_inmet",
        "uf_inmet",
        "nome_municipio_ibge"
    ]

    colunas_para_trazer = [
        coluna for coluna in colunas_para_trazer
        if coluna in depara_aux.columns
    ]

    depara_aux = depara_aux[colunas_para_trazer].drop_duplicates()

    depara_aux = depara_aux[
        depara_aux["codigo_municipio_sus"].notna()
    ]

    depara_aux = depara_aux.sort_values("codigo_local_inmet")
    depara_aux = depara_aux.drop_duplicates(
        subset=["codigo_municipio_sus"],
        keep="first"
    )

    resultado = sus.merge(
        depara_aux,
        left_on=coluna_sus,
        right_on="codigo_municipio_sus",
        how="left"
    )

    return resultado