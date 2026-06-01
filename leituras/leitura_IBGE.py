from constants import *
import pandas as pd
import os
from pathlib import Path

dfs_lista = []

def junta_ibge():
    for arquivo in sorted(os.listdir(ibge_path)):
        if arquivo.endswith('.csv'):
            caminho_completo = os.path.join(ibge_path, arquivo)
            try:
                df = pd.read_csv(caminho_completo, sep=';')
                dfs_lista.append(df)
                print(f'Lido: {arquivo} ({len(df)} linhas)')
            except Exception as e:
                print(f'Erro ao ler {arquivo}: {e}')

    if dfs_lista:
        df_completo = pd.concat(dfs_lista, ignore_index=True)
        print(f'\nDataFrame consolidado: {len(df_completo)} linhas e {len(df_completo.columns)} colunas')
    else:
        print('Nenhum arquivo CSV encontrado na pasta IBGE.')

    return df_completo