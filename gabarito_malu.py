import pandas as pd

from leituras.leitura_INMET import junta_clima
from leituras.leitura_IBGE import municipios_rj_unicos
from leituras.leitura_SUS import junta_sus

from scripts.cruzamento import conectar_sus_inmet_via_ibge

pd.set_option('display.max_columns', None)

df_clima = junta_clima()
df_ibge = municipios_rj_unicos()
df_saude = junta_sus()

df_ibge["UF"] = "RJ"

df_completo = conectar_sus_inmet_via_ibge(df_saude, df_ibge, df_clima)

sexo_dic = {1:'Masculino', 2:'Feminino', 0:'Ignorado'}
raca_dic = {1:'Branca', 2:'Preta', 3:'Amarela', 4:'Parda', 5:'Indígena', 9:'Ignorado'}
local_dic = {1:'Hospital', 2:'Outro estab. saúde', 3:'Domicílio', 4:'Via pública', 5:'Outros', 9:'Ignorado'}

df_completo['SEXO'] = df_completo['SEXO'].astype(float).astype('Int64')
df_completo['RACACOR'] = df_completo['RACACOR'].astype(float).astype('Int64')
df_completo['LOCOCOR'] = df_completo['LOCOCOR'].astype(float).astype('Int64')

df_completo['SEXO_DESC'] = df_completo['SEXO'].map(sexo_dic)
df_completo['RACA_DESC'] = df_completo['RACACOR'].map(raca_dic)
df_completo['LOCAL_DESC'] = df_completo['LOCOCOR'].map(local_dic)

# 2- Quais são os grupos de causa de morte mais frequentes e como se distribuem entre homens e mulheres?
# Requisitos atendidos: Req 3,Req 5.3,Req 6b,Req 9a.1.
# Objetivo: Identificar as causas que lideram a mortalidade no RJ e verificar se há diferença na frequência entre homens e mulheres.

def classifica_causa(cid):
    c = cid[0]
    if c=='I':
        return 'Doenças circulatórias'
    elif c=='J':
        return 'Doenças respiratórias'
    elif c=='C' or c=='D':
        return 'Neoplasias'
    elif c=='V' or c=='W' or c=='X' or c=='Y':
        return 'Causas externas'
    elif c=='U':
        return 'COVID-19'
    else:
        return 'Outras causas'

df_completo_2 = df_completo.copy()

df_completo_2['GRUPO_CAUSA'] = df_completo_2['CAUSABAS'].apply(classifica_causa)

frequencias = df_completo_2['GRUPO_CAUSA'].value_counts()

df_2 = pd.crosstab(df_completo_2['GRUPO_CAUSA'], df_completo_2['SEXO_DESC'])

print("grupos de causa de morte mais frequentes:\n", frequencias)
print("\nDistribuição entre homens e mulheres:\n", df_2)

# 4- Como variam temperatura, precipitação acumulada e umidade relativa entre os municípios do INMET no RJ?
# Requisitos atendidos: Req 3,Req 5.1,Req 7.1,Req 8b.
# Objetivo: Caracterizar o perfil climático dos municípios fluminenses e verificar a existência de correlação entre temperatura e precipitação.

df_completo_3 = df_completo_2.copy()

df_completo_3['temp_media'] = df_completo_3['temp_media'].astype(float)
df_completo_3['precip_total'] = df_completo_3['precip_total'].astype(float)
df_completo_3['umidade_media'] = df_completo_3['umidade_media'].astype(float)

resumo_rj = df_completo_3.groupby('municipio_inmet').agg({
    'temp_media': 'mean',
    'precip_total': 'mean',
    'umidade_media': 'mean'
})

print("\nTemperatura, precipitação acumulada e umidade relativa entre os municípios do INMET no RJ:\n")
print(resumo_rj)

# 6- Qual é o perfil racial e de sexo dos óbitos domiciliares de pessoas com mais de 79 anos, excluindo causas externas?
# Requisitos atendidos: Req 5.3,Req 5.4,Req 7.2,Req 9b.1.
# Objetivo: Identificar vulnerabilidades específicas da população muito idosa que falece em domicílio, investigando quais grupos raciais e de sexo são mais afetados por cada tipo de causa.

df_completo_4 = df_completo_3.copy()

def decodifica_idade(valor):
    valor = str(valor).zfill(3)
    primeiro_dig = valor[0]
    demais_dig = valor[1:]

    if primeiro_dig=='4':
        return int(demais_dig)
    else:
        return None

df_completo_4['IDADE_ANOS'] = df_completo_4['IDADE'].apply(decodifica_idade)

demais_causa = df_completo_4[df_completo_4['GRUPO_CAUSA'] != 'Causas externas']

demais_causa_79 = demais_causa[demais_causa['IDADE_ANOS'] > 79]

demais_causa_79_local = demais_causa_79[demais_causa_79['LOCAL_DESC'] == 'Domicílio']

raca_sexo = demais_causa_79_local.groupby(['RACA_DESC', 'SEXO_DESC'])['CODMUNRES'].size()

print("\nPerfil racial e de sexo dos óbitos domiciliares de pessoas com mais de 79 anos, excluindo causas externas:\n")
print(raca_sexo)

# 8- Como a mortalidade por doenças respiratórias e circulatórias se distribui ao longo dos meses de 2024 e existe sazonalidade nesse padrão?
# Requisitos atendidos: Req 5.3,Req 8c,Req 9a.1,Req 7.
# Objetivo: Investigar se os óbitos por causas respiratórias e circulatórias aumentam em meses frios (inverno) ou chuvosos, conectando o padrão temporal de mortalidade com as condições climáticas analisadas nas perguntas anteriores

df_completo_5 = df_completo_4.copy()

df_completo_5['MES_INMET'] = pd.to_datetime(df_completo_5['Data Medicao']).dt.month

df_completo_5_circ = df_completo_5.copy()
df_completo_5_circ = df_completo_5_circ[df_completo_5_circ['GRUPO_CAUSA'].isin(['Doenças circulatórias'])]
freq_doencas_circ = df_completo_5_circ['MES_INMET'].value_counts()

df_completo_5_resp = df_completo_5.copy()
df_completo_5_resp = df_completo_5_resp[df_completo_5_resp['GRUPO_CAUSA'].isin(['Doenças respiratórias'])]
freq_doencas_resp = df_completo_5_resp['MES_INMET'].value_counts()

print("\nDistribuição ao longo dos meses de 2024 para doenças circulatórias:\n", freq_doencas_circ)
print("\nDistribuição ao longo dos meses de 2024 para doenças respiratórias:\n", freq_doencas_resp)
