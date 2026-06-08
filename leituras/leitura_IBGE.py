from pathlib import Path
from constants import *
import pandas as pd
import os

def junta_ibge():
    #Lê arquivo IBGE (Excel .xls) com dados de estruturas territoriais brasileiras
    
    df_completo = None
    
    for arquivo in sorted(os.listdir('dados/IBGE/')):
        if arquivo.endswith('.xls') or arquivo.endswith('.xlsx'):
            caminho_completo = os.path.join('dados/IBGE/', arquivo)
            try:
                df = pd.read_excel(caminho_completo, sheet_name=0, skiprows=6)
        
                df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
                
                colunas_importantes = ['UF', 'Nome_UF', 'Região Geográfica Intermediária', 
                                      'Nome Região Geográfica Intermediária', 'Região Geográfica Imediata',
                                      'Nome Região Geográfica Imediata', 'Município', 'Código Município Completo',
                                      'Nome_Município', 'Distrito', 'Código de Distrito Completo', 'Nome_Distrito']
                
                df = df[[col for col in colunas_importantes if col in df.columns]]
                
                df_completo = df
            except Exception as e:
                print(f'Erro ao ler {arquivo}: {e}')

    if df_completo is not None:
        print(f'\nDataFrame IBGE carregado: {len(df_completo)} linhas e {len(df_completo.columns)} colunas')
        return df_completo
    else:
        print('Nenhum arquivo Excel encontrado na pasta IBGE.')
        return None


def municipios_rj_unicos():
    """Retorna municípios únicos do Rio de Janeiro com seu código IBGE."""
    df = junta_ibge()
    if df is None:
        return None

    if 'UF' in df.columns:
        df_rj = df[df['UF'].astype(str).str.zfill(2) == '33']
    else:
        df_rj = df[df['Nome_UF'].str.contains('Rio de Janeiro', case=False, na=False)]

    cols = []
    if 'Código Município Completo' in df_rj.columns:
        cols.append('Código Município Completo')
    if 'Nome_Município' in df_rj.columns:
        cols.append('Nome_Município')

    if not cols:
        print('Não foi possível encontrar as colunas de código ou nome do município.')
        return None

    df_rj_unicos = df_rj[cols].drop_duplicates().reset_index(drop=True)
    print(f'IBGE Rio de Janeiro: {len(df_rj_unicos)} municípios únicos carregados')
    return df_rj_unicos