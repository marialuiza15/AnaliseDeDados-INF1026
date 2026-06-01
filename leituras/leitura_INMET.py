import pandas as pd
import os
from pathlib import Path
from constants import *

dfs_lista = []

def junta_clima():
    for arquivo in sorted(os.listdir(inmet_path)):
        if arquivo.endswith('.csv'):
            nome_sem_extensao = arquivo[:-4]  
            partes = nome_sem_extensao.split('_', 1)  
            
            if len(partes) == 2:
                regiao = partes[1]  
            else:
                regiao = nome_sem_extensao  
            
            caminho_completo = os.path.join(inmet_path, arquivo)
            try:
                df = pd.read_csv(caminho_completo, sep=';')
                # Remove coluna vazia (Unnamed) se existir
                df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
                # Adicionar coluna Regiao
                df['Regiao'] = regiao
                dfs_lista.append(df)
                print(f'Lido: {arquivo} ({len(df)} linhas) - Região: {regiao}')
            except Exception as e:
                print(f'Erro ao ler {arquivo}: {e}')

    # Concatenar todos os dataframes em um único
    if dfs_lista:
        df_completo = pd.concat(dfs_lista, ignore_index=True)
        print(f'\nDataFrame consolidado: {len(df_completo)} linhas e {len(df_completo.columns)} colunas')
        print(f'Regiões: {df_completo["Regiao"].nunique()} diferentes')
    else:
        print('Nenhum arquivo CSV encontrado na pasta INMET.')

    '''
    DF df_completo possui as colunas:
    'Data Medicao', 
    'PRECIPITACAO TOTAL, DIARIO (AUT)(mm)',
    'TEMPERATURA MEDIA, DIARIA (AUT)(°C)',
    'UMIDADE RELATIVA DO AR, MEDIA DIARIA (AUT)(%)', 
    'Regiao'
    '''

    return df_completo