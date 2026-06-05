from leituras.leitura_INMET import junta_clima
from leituras.leitura_IBGE import municipios_rj_unicos
from leituras.leitura_SUS import junta_sus

from scripts.cruzamento import criar_depara_inmet_ibge_sus, cruzar_sus_com_inmet


df_clima = junta_clima()
df_ibge = municipios_rj_unicos()
df_saude = junta_sus()

# Como municipios_rj_unicos() já retorna só municípios do RJ,
# criamos a coluna UF manualmente.
df_ibge["UF"] = "RJ"

print("\nColunas INMET:")
print(df_clima.columns.tolist())

print("\nColunas IBGE:")
print(df_ibge.columns.tolist())

print("\nColunas SUS:")
print(df_saude.columns.tolist())


depara_inmet_ibge_sus = criar_depara_inmet_ibge_sus(
    df_inmet=df_clima,
    df_ibge=df_ibge,

    # Agora usamos o município limpo criado em leitura_INMET.py
    coluna_municipio_inmet="municipio_inmet",
    coluna_uf_inmet="UF",
    coluna_codigo_inmet="codigo_estacao_inmet",

    coluna_municipio_ibge="Nome_Município",
    coluna_uf_ibge="UF",
    coluna_codigo_ibge="Código Município Completo"
)

df_saude_com_inmet = cruzar_sus_com_inmet(
    df_sus=df_saude,
    depara=depara_inmet_ibge_sus,
    coluna_sus="CODMUNOCOR"
)

depara_inmet_ibge_sus.to_csv(
    "depara_inmet_ibge_sus.csv",
    sep=";",
    index=False,
    encoding="utf-8-sig"
)

df_saude_com_inmet.to_csv(
    "sus_com_inmet.csv",
    sep=";",
    index=False,
    encoding="utf-8-sig"
)

print("\nDe/para criado:", depara_inmet_ibge_sus.shape)
print("Base SUS com INMET:", df_saude_com_inmet.shape)

print("\nColunas do de/para:")
print(depara_inmet_ibge_sus.columns.tolist())

print("\nPrévia do de/para:")
print(depara_inmet_ibge_sus.head(20))

print("\nTotal de linhas SUS com INMET:")
print(len(df_saude_com_inmet))

print("\nLinhas com código INMET:")
print(df_saude_com_inmet["codigo_local_inmet"].notna().sum())

print("\nLinhas sem código INMET:")
print(df_saude_com_inmet["codigo_local_inmet"].isna().sum())

print("\nPercentual com código INMET:")
print(df_saude_com_inmet["codigo_local_inmet"].notna().mean() * 100)

print("\nMunicípios SUS sem correspondência INMET:")
print(
    df_saude_com_inmet.loc[
        df_saude_com_inmet["codigo_local_inmet"].isna(),
        "CODMUNOCOR"
    ].drop_duplicates().head(30)
)