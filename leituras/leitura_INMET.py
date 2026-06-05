from pathlib import Path
from constants import *
import pandas as pd
import os


def limpar_municipio_inmet(regiao):
    """
    Limpa o nome da região/estação do INMET para tentar obter
    o nome do município compatível com a tabela do IBGE.

    Exemplo:
    RIO DE JANEIRO-MARAMBAIA -> RIO DE JANEIRO
    CAMPOS DOS GOYTACAZES-SAO TOME -> CAMPOS DOS GOYTACAZES
    SEROPEDICA -> SEROPEDICA
    """
    if pd.isna(regiao):
        return None

    regiao = str(regiao).strip()

    # Pega o texto antes do primeiro hífen
    municipio = regiao.split("-")[0].strip()

    return municipio


def junta_clima():
    dfs_lista = []

    for arquivo in sorted(os.listdir(inmet_path)):
        if arquivo.endswith('.csv'):
            nome_sem_extensao = arquivo[:-4]
            partes = nome_sem_extensao.split('_', 1)

            if len(partes) == 2:
                codigo_estacao = partes[0]
                regiao = partes[1]
            else:
                codigo_estacao = None
                regiao = nome_sem_extensao

            municipio_inmet = limpar_municipio_inmet(regiao)

            caminho_completo = os.path.join(inmet_path, arquivo)

            try:
                df = pd.read_csv(
                    caminho_completo,
                    sep=';',
                    dtype=str,
                    low_memory=False
                )

                df = df.loc[:, ~df.columns.str.contains('^Unnamed')]

                df['codigo_estacao_inmet'] = codigo_estacao
                df['Regiao'] = regiao
                df['municipio_inmet'] = municipio_inmet
                df['UF'] = 'RJ'
                df['arquivo_origem'] = arquivo

                dfs_lista.append(df)

                print(
                    f'Lido: {arquivo} ({len(df)} linhas) '
                    f'- Estação: {codigo_estacao} '
                    f'- Região: {regiao} '
                    f'- Município: {municipio_inmet}'
                )

            except Exception as e:
                print(f'Erro ao ler {arquivo}: {e}')

    if dfs_lista:
        df_completo = pd.concat(dfs_lista, ignore_index=True)
        print(
            f'\nDataFrame INMET consolidado: '
            f'{len(df_completo)} linhas e {len(df_completo.columns)} colunas'
        )
        return df_completo

    else:
        print('Nenhum arquivo CSV encontrado na pasta INMET.')
        return None