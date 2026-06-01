from scripts.limpeza import *
from scripts.features import *
from scripts.modelagem import *
from scripts.visualizacao import plot_distribuicao_causas, mostrar_matriz_confusao, plot_casos_por_mes

CAMINHO_CLIMA = 'dados_clima_mg/'
CAMINHO_SAUDE = 'dados_saude_mg/'

clima_total, dfs_por_ano = unir_e_separar_clima(CAMINHO_CLIMA)

df_clima_2010 = dfs_por_ano[2010]
df_clima_2011 = dfs_por_ano[2011]
df_clima_2012 = dfs_por_ano[2012]
df_clima_2013 = dfs_por_ano[2013]
df_clima_2014 = dfs_por_ano[2014]
df_clima_2015 = dfs_por_ano[2015]
df_clima_2016 = dfs_por_ano[2016]
df_clima_2017 = dfs_por_ano[2017]
df_clima_2018 = dfs_por_ano[2018]
df_clima_2019 = dfs_por_ano[2019]
df_clima_2020 = dfs_por_ano[2020]
df_clima_2021 = dfs_por_ano[2021]
df_clima_2022 = dfs_por_ano[2022]
df_clima_2023 = dfs_por_ano[2023]

df_geral_2010 = unindo_clima_saude(df_clima_2010, CAMINHO_SAUDE, 2010)
df_geral_2011 = unindo_clima_saude(df_clima_2011, CAMINHO_SAUDE, 2011)
df_geral_2012 = unindo_clima_saude(df_clima_2012, CAMINHO_SAUDE, 2012)
df_geral_2013 = unindo_clima_saude(df_clima_2013, CAMINHO_SAUDE, 2013)
df_geral_2014 = unindo_clima_saude(df_clima_2014, CAMINHO_SAUDE, 2014)
df_geral_2015 = unindo_clima_saude(df_clima_2015, CAMINHO_SAUDE, 2015)
df_geral_2016 = unindo_clima_saude(df_clima_2016, CAMINHO_SAUDE, 2016)
df_geral_2017 = unindo_clima_saude(df_clima_2017, CAMINHO_SAUDE, 2017)
df_geral_2018 = unindo_clima_saude(df_clima_2018, CAMINHO_SAUDE, 2018)
df_geral_2019 = unindo_clima_saude(df_clima_2019, CAMINHO_SAUDE, 2019)
df_geral_2020 = unindo_clima_saude(df_clima_2020, CAMINHO_SAUDE, 2020)
df_geral_2021 = unindo_clima_saude(df_clima_2021, CAMINHO_SAUDE, 2021)
df_geral_2022 = unindo_clima_saude(df_clima_2022, CAMINHO_SAUDE, 2022)
df_geral_2023 = unindo_clima_saude(df_clima_2023, CAMINHO_SAUDE, 2023)


dfs_gerais = {}
for ano in range(2010, 2024):
    df_clima_ano = dfs_por_ano[ano]
    dfs_gerais[ano] = unindo_clima_saude(df_clima_ano, CAMINHO_SAUDE, ano)


df_treino = pd.concat([
    engenharia_de_features(dfs_gerais[ano])
    for ano in range(2010, 2021)
], ignore_index=True)

df_teste = pd.concat([
    engenharia_de_features(dfs_gerais[ano])
    for ano in range(2021, 2024)
], ignore_index=True)


print("Tamanho treino:", df_treino.shape)
print("Tamanho teste:", df_teste.shape)
print("Colunas disponíveis:", df_treino.columns.tolist())
print("Exemplo de dados:\n", df_treino.head())

modelo, relatorio, X_test, y_test_enc, le_y = treinar_modelo_por_doenca(df_treino, df_teste, top_n=3)

print("\nRelatório de classificação:\n", relatorio)
mostrar_matriz_confusao(modelo, X_test, y_test_enc, le_y)