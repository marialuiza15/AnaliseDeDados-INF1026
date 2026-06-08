from pathlib import Path
from constants import *
import pandas as pd
import os

def junta_sus():
    #Lê arquivos CSV de dados de saúde (SUS) da pasta dados/SUS/
    
    df_completo = None
    dfs_lista = []
    
    # Verificar se a pasta existe
    if not os.path.exists('dados/SUS/'):
        print(f'Pasta {'dados/SUS/'} não encontrada.')
        return None
    
    for arquivo in sorted(os.listdir('dados/SUS/')):
        if arquivo.endswith('.csv'):
            caminho_completo = os.path.join('dados/SUS/', arquivo)
            try:
                df = pd.read_csv(caminho_completo,sep=';',dtype=str,low_memory=False)
                # Remove colunas vazias (Unnamed)
                df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
                dfs_lista.append(df)
                print(f'Lido: {arquivo} ({len(df)} linhas)')
            except Exception as e:
                print(f'Erro ao ler {arquivo}: {e}')

    if dfs_lista:
        df_completo = pd.concat(dfs_lista, ignore_index=True)
        print(f'\nDataFrame SUS consolidado: {len(df_completo)} linhas e {len(df_completo.columns)} colunas')
        return df_completo
    else:
        print('Nenhum arquivo CSV encontrado na pasta SUS.')
        return None