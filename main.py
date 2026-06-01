from scripts.preparaçãoDados import unir_e_separar_clima, unindo_clima_saude

clima_total, dfs_por_ano = unir_e_separar_clima('dados_clima_mg/')

dfs_gerais = {}
for ano in range(2010, 2024):
    df_clima_ano = dfs_por_ano[ano]
    dfs_gerais[ano] = unindo_clima_saude(df_clima_ano, 'dados_saude_mg/', ano)
    print(f'Ano {ano}: registros unidos = {len(dfs_gerais[ano])}')

print('Junções concluídas para todos os anos.')
