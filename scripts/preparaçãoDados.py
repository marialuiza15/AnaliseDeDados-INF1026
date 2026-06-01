# Preparação dos dados

#  1 concatenação (em qualquer eixo)
#  2 estratégias distintas de preenchimento de valores ausentes (pelo menos uma por grupo), ex:

# Substituir pelo valor mais frequente (coluna textual)
# Substituir pela média do grupo (coluna numérica)

#  1 estratégia de substituição/alteração de valores (df[col].apply(...))

import pandas as pd
import glob
import unidecode
import os

def limpar_clima(df):

    df['TEMPERATURA MEDIA, DIARIA (AUT)(Â°C)'] = (
        df['TEMPERATURA MEDIA, DIARIA (AUT)(Â°C)']
        .str.replace(',', '.', regex=False)
        .astype(float)
    )
    df['UMIDADE RELATIVA DO AR, MEDIA DIARIA (AUT)(%)'] = (
        df['UMIDADE RELATIVA DO AR, MEDIA DIARIA (AUT)(%)']
        .str.replace(',', '.', regex=False)
        .astype(float)
    )
    df = df.dropna(subset=[
        'TEMPERATURA MEDIA, DIARIA (AUT)(Â°C)', 
        'UMIDADE RELATIVA DO AR, MEDIA DIARIA (AUT)(%)'
    ])
    df = df[
        (df['UMIDADE RELATIVA DO AR, MEDIA DIARIA (AUT)(%)'] <= 100) & 
        (df['TEMPERATURA MEDIA, DIARIA (AUT)(Â°C)'] > -50)
    ]
    df['TEMPERATURA_MEDIA'] = df['TEMPERATURA MEDIA, DIARIA (AUT)(Â°C)']
    df['UMIDADE_MEDIA'] = df['UMIDADE RELATIVA DO AR, MEDIA DIARIA (AUT)(%)']

    return df

def limpar_saude(df):
    colunas_utilizadas = [
        'dt_obito', 'nu_idade', 'sg_sexo', 'tp_raca_cor',
        'co_municipio_ibge_residencia', 'co_cid_causa_basica',
        'categoria_cid_causa_basica'
    ]
    df = df[colunas_utilizadas].dropna()
    return df


def unir_e_separar_clima(caminho_clima):
    dfs = []
    for i in range(502, 572):  # A502 até A571
        arquivo = os.path.join(caminho_clima, f'dados_A{i}_D_2010-01-01_2023-12-31.csv')
        if not os.path.exists(arquivo):
            continue
        with open(arquivo, encoding='latin1') as f:
            nome_lugar = f.readline().strip().split(':')[1].strip().lower()
        

        nome_lugar = (
            unidecode.unidecode(nome_lugar.lower()
                .replace(' (mg)', '')
                .replace('-', ' ')
                .replace('_', ' ')
                .strip())
        )
        df = pd.read_csv(arquivo, sep=';', encoding='latin1', header=9)
        df['Região'] = nome_lugar

        if 'TEMPERATURA MEDIA, DIARIA (AUT)(Â°C)' in df.columns:
            df['TEMPERATURA MEDIA, DIARIA (AUT)(Â°C)'] = (
                df['TEMPERATURA MEDIA, DIARIA (AUT)(Â°C)'].str.replace(',', '.', regex=False).astype(float)
            )
        if 'UMIDADE RELATIVA DO AR, MEDIA DIARIA (AUT)(%)' in df.columns:
            df['UMIDADE RELATIVA DO AR, MEDIA DIARIA (AUT)(%)'] = (
                df['UMIDADE RELATIVA DO AR, MEDIA DIARIA (AUT)(%)'].str.replace(',', '.', regex=False).astype(float)
            )
        df['data'] = pd.to_datetime(df['Data Medicao'], errors='coerce')
        dfs.append(df)

    clima_total = pd.concat(dfs, ignore_index=True)

    # Separa por ano
    dfs_por_ano = {}
    for ano in range(2010, 2024):
        dfs_por_ano[ano] = clima_total[clima_total['data'].dt.year == ano].copy()

    
    return clima_total, dfs_por_ano

def unindo_clima_saude(df_clima_ano, caminho_saude, ano_especifico):

    arquivo_saude = f'dados_cronicas_ses_{ano_especifico}.csv'
    caminho_arquivo_saude = os.path.join(caminho_saude, arquivo_saude)
    
    if not os.path.exists(caminho_arquivo_saude):
        print(f"Arquivo de saúde não encontrado para {ano_especifico}")
        return pd.DataFrame()

    df_saude = pd.read_csv(caminho_arquivo_saude, sep=';', encoding='utf-8-sig')
    
    df_clima_ano = df_clima_ano.copy()
    df_clima_ano['data'] = pd.to_datetime(df_clima_ano['Data Medicao'], errors='coerce').dt.date
    df_clima_ano['Região'] = df_clima_ano['Região'].str.strip().str.lower()

    df_saude['data'] = pd.to_datetime(df_saude['dt_obito'], dayfirst=True, errors='coerce').dt.date
    df_saude['Região'] = (
        df_saude['co_municipio_ibge_residencia']
        .astype(str)
        .str.lower()
        .str.strip()
        .replace('nan', '', regex=False)
        .apply(lambda value: unidecode.unidecode(value) if isinstance(value, str) and value else value)
    )
    df_merged = pd.merge(df_clima_ano, df_saude, on=['data', 'Região'], how='inner', suffixes=('_clima', '_saude'))

    return df_merged
