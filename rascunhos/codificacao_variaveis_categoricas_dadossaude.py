import pandas as pd
from sklearn.preprocessing import OneHotEncoder, OrdinalEncoder
import numpy as np

df = pd.read_csv('arquivos/dados_cronicas_ses_2015.csv', sep=';')

print("\nColunas disponíveis no DataFrame:")
print(df.columns.tolist())

colunas_categoricas = ['sg_sexo', 'tp_raca_cor', 'tp_escolaridade']  
colunas_existentes = [col for col in colunas_categoricas if col in df.columns]

df[colunas_existentes] = df[colunas_existentes].fillna('Desconhecido')

if colunas_existentes:  #
    encoder = OneHotEncoder(sparse_output=False, drop='first')
    encoded_cols = encoder.fit_transform(df[colunas_existentes])
    encoded_df = pd.DataFrame(encoded_cols, columns=encoder.get_feature_names_out(colunas_existentes))
    
    df = pd.concat([df.drop(colunas_existentes, axis=1), encoded_df], axis=1)
else:
    print("\nNenhuma coluna categórica encontrada para codificação.")

if 'tp_escolaridade' in df.columns:
    escolaridade_map = {
        'Desconhecido': 0,
        'de 1 a 3': 1,
        'de 4 a 7': 2,
        'Fundamental': 3,
        'Médio': 4,
        'Superior': 5,
        'Ignora': -1
    }
    df['tp_escolaridade'] = df['tp_escolaridade'].map(escolaridade_map)

print("\nDataFrame após codificação:")
print(df.head())

df.to_csv('arquivos/dados_processados.csv', sep=';', index=False)