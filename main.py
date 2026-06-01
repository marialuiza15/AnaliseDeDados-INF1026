from scripts.limpeza import unir_e_separar_clima, unindo_clima_saude

CAMINHO_CLIMA = 'dados_clima_mg/'
CAMINHO_SAUDE = 'dados_saude_mg/'

clima_total, dfs_por_ano = unir_e_separar_clima(CAMINHO_CLIMA)

dfs_gerais = {}
for ano in range(2010, 2024):
    df_clima_ano = dfs_por_ano[ano]
    dfs_gerais[ano] = unindo_clima_saude(df_clima_ano, CAMINHO_SAUDE, ano)
    print(f'Ano {ano}: registros unidos = {len(dfs_gerais[ano])}')

print('Junções concluídas para todos os anos.')
