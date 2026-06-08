# Grupo 06
# Nome completo 1: Maria Luiza Lima Bastos - 2320468
# Nome completo 2: Danilo de Castro Alves Nascimento - 2320401

"""
TRABALHO — PANDAS
Tema: Análise da associação entre variáveis meteorológicas e a mortalidade no estado do Rio de Janeiro em 2024
SIM - INMET - IBGE
-------------------------------------------------------------------------------
ATENÇÃO:
    ENTREGAR este template preenchido e executando, sem erros.
    CUIDADO: o template é corrigido somente até o primeiro erro de execução.

IMPORTANTE:
    As conclusões são baseadas nos dados da amostra e não afirmam causalidade.
    Use expressões como:
        "na amostra";
        "os dados sugerem";
        "aparece associado";
        "merece atenção";
        "não permite afirmar relação de causa e efeito".
"""

import pandas as pd
import matplotlib.pyplot as plt

from leituras.leitura_INMET import junta_clima
from leituras.leitura_IBGE import municipios_rj_unicos
from leituras.leitura_SUS import junta_sus
from scripts.cruzamento import conectar_sus_inmet_via_ibge

pd.set_option('display.max_columns', None)

# =============================================================================
# CARREGANDO E INTEGRANDO OS DADOS
# =============================================================================

df_clima = junta_clima()
df_ibge  = municipios_rj_unicos()
df_saude = junta_sus()

df_ibge["UF"] = "RJ"

df_completo = conectar_sus_inmet_via_ibge(df_saude, df_ibge, df_clima)

sexo_dic  = {1: 'Masculino', 2: 'Feminino',  0: 'Ignorado'}
raca_dic  = {1: 'Branca', 2: 'Preta', 3: 'Amarela', 4: 'Parda', 5: 'Indígena', 9: 'Ignorado'}
local_dic = {1: 'Hospital', 2: 'Outro estab. saúde', 3: 'Domicílio',
             4: 'Via pública', 5: 'Outros', 9: 'Ignorado'}

df_completo['SEXO']   = df_completo['SEXO'].astype(float).astype('Int64')
df_completo['RACACOR']= df_completo['RACACOR'].astype(float).astype('Int64')
df_completo['LOCOCOR']= df_completo['LOCOCOR'].astype(float).astype('Int64')

df_completo['SEXO_DESC']  = df_completo['SEXO'].map(sexo_dic)
df_completo['RACA_DESC']  = df_completo['RACACOR'].map(raca_dic)
df_completo['LOCAL_DESC'] = df_completo['LOCOCOR'].map(local_dic)

# =============================================================================
# QUESTÃO 1
# =============================================================================

print("\n-----------------------------------------------------")
print("\n 1 - Qual é o perfil (faixa etária, sexo, raça/cor) dos óbitos não fetais no RJ em 2024? \n")
print("\n-----------------------------------------------------")

df_completo_1 = df_completo[df_completo["TIPOBITO"] == '2'].copy()

def decodifica_idade(valor):
    valor = str(valor).zfill(3)
    primeiro_dig = valor[0]
    demais_dig   = valor[1:]
    if primeiro_dig == '4':
        return int(demais_dig)
    else:
        return None

df_completo_1['IDADE_ANOS'] = df_completo_1['IDADE'].apply(decodifica_idade)

bins   = [0, 14, 29, 59, 79, 120]
labels = ['Criança/Adolescente', 'Jovem', 'Adulto', 'Idoso', 'Muito idoso']

df_completo_1["FAIXA_ETARIA"] = pd.cut(
    df_completo_1["IDADE_ANOS"],
    bins=bins,
    labels=labels,
    include_lowest=True
)

df_completo_1["FAIXA_ETARIA"].value_counts().plot(kind='bar')
plt.title("Distribuição de óbitos não fetais por faixa etária — RJ 2024")
plt.tight_layout()
plt.show()

df_exibe = df_completo_1.groupby(['FAIXA_ETARIA', 'SEXO_DESC', 'RACA_DESC']).agg({
    'SEXO_DESC':   'count',
    'IDADE_ANOS':  ['mean', 'min', 'max'],
    'RACA_DESC':   'count',
    'FAIXA_ETARIA':'value_counts'
})

print("Perfil dos óbitos não fetais no RJ em 2024:\n", df_exibe)
print("Total de óbitos não fetais:", df_completo_1.shape[0])

print("\n-----------------------------------------------------")

# =============================================================================
# QUESTÃO 2
# =============================================================================

print("\n-----------------------------------------------------")
print("\n 2 - Quais são os grupos de causa de morte mais frequentes e como se distribuem entre homens e mulheres? \n")
print("\n-----------------------------------------------------")

def classifica_causa(cid):
    c = cid[0]
    if c == 'I':
        return 'Doenças circulatórias'
    elif c == 'J':
        return 'Doenças respiratórias'
    elif c == 'C' or c == 'D':
        return 'Neoplasias'
    elif c in ['V', 'W', 'X', 'Y']:
        return 'Causas externas'
    elif c == 'U':
        return 'COVID-19'
    else:
        return 'Outras causas'

df_completo_2 = df_completo_1.copy()
df_completo_2['GRUPO_CAUSA'] = df_completo_2['CAUSABAS'].apply(classifica_causa)

frequencias = df_completo_2['GRUPO_CAUSA'].value_counts()
df_2 = pd.crosstab(df_completo_2['GRUPO_CAUSA'], df_completo_2['SEXO_DESC'])

print("Grupos de causa de morte mais frequentes:\n", frequencias)
print("\nDistribuição entre homens e mulheres:\n", df_2)

print("\n-----------------------------------------------------")

# =============================================================================
# QUESTÃO 3
# =============================================================================

print("\n-----------------------------------------------------")
print("\n 3 - A média de idade dos óbitos varia por grupo de causa de morte e por sexo? \n")
print("\n-----------------------------------------------------")

def classifica_causa(cid):
    cid = str(cid).upper()
    if cid.startswith("U07"):
        return 'COVID-19'
    elif cid.startswith("I"):
        return 'Doenças circulatórias'
    elif cid.startswith("J"):
        return 'Doenças respiratórias'
    elif cid.startswith("C") or cid[:2] in ["D0", "D1", "D2", "D3", "D4"]:
        return 'Neoplasias'
    elif cid[0] in ["V", "W", "X", "Y"]:
        return "Causas externas"
    else:
        return "Outras causas"

df_completo_3 = df_completo_2.copy()
df_completo_3["GRUPO_CAUSA"] = df_completo_3["CAUSABAS"].apply(classifica_causa)

saidaCross = pd.crosstab(
    index=df_completo_3["GRUPO_CAUSA"],
    columns=df_completo_3["SEXO_DESC"],
    values=df_completo_3["IDADE_ANOS"],
    aggfunc="mean"
)

saidaGroup = df_completo_3.groupby("GRUPO_CAUSA")["IDADE_ANOS"].mean().sort_values(ascending=False)

print("Média de IDADE_ANOS por grupo de causa de morte e sexo:\n", saidaCross)
print("\nMédia geral de IDADE_ANOS por GRUPO_CAUSA (maior → menor):\n", saidaGroup)

print("\n-----------------------------------------------------")

# =============================================================================
# QUESTÃO 4
# =============================================================================

print("\n-----------------------------------------------------")
print("\n 4 - Como variam temperatura, precipitação acumulada e umidade relativa entre os municípios do INMET no RJ? \n")
print("\n-----------------------------------------------------")

df_completo_4 = df_completo_3.copy()

df_completo_4['temp_media']    = df_completo_4['temp_media'].astype(float)
df_completo_4['precip_media']  = df_completo_4['precip_media'].astype(float)
df_completo_4['umidade_media'] = df_completo_4['umidade_media'].astype(float)

df_completo_4['FAIXA_UMIDADE'] = pd.cut(df_completo_4['umidade_media'], bins=4)

resumo_rj = df_completo_4.groupby('municipio_inmet').agg({
    'temp_media':    'mean',
    'precip_media':  'mean',
    'umidade_media': 'mean'
}).sort_values(by='temp_media', ascending=False)

print("\nTemperatura, precipitação acumulada e umidade relativa por município do INMET no RJ:\n")
print(resumo_rj)

print("\n-----------------------------------------------------")

# =============================================================================
# QUESTÃO 5
# =============================================================================

print("\n-----------------------------------------------------")
print("\n 5 - Como se distribui a intensidade das chuvas diárias por município e qual é a temperatura média associada a cada nível de precipitação? \n")
print("\n-----------------------------------------------------")

df_completo_5 = df_completo_4.copy()

bins   = [0, 1, 10, 25, 50, 200]
labels = [
    'Sem chuva ou chuva muito fraca',
    'Chuva fraca',
    'Chuva moderada',
    'Chuva forte',
    'Chuva muito forte'
]

df_completo_5["FAIXA_CHUVA"] = pd.cut(
    df_completo_5['precip_media'],
    bins=bins,
    labels=labels,
    include_lowest=True
)

tabela_chuva_municipio = pd.crosstab(
    index=df_completo_5["municipio_inmet"],
    columns=df_completo_5["FAIXA_CHUVA"],
    normalize="index"
) * 100

tabela_temp_estruturada = pd.crosstab(
    index=df_completo_5["municipio_inmet"],
    columns=df_completo_5["FAIXA_CHUVA"],
    values=df_completo_5["temp_media"],
    aggfunc="mean"
).round(2)

tabela_chuva_municipio["Chuva forte ou muito forte"] = (
    tabela_chuva_municipio.get("Chuva forte", 0) +
    tabela_chuva_municipio.get("Chuva muito forte", 0)
)

tabela_chuva_municipio = tabela_chuva_municipio.sort_values(
    by="Chuva forte ou muito forte",
    ascending=False
)

freq_FAIXA_CHUVA     = (df_completo_5["FAIXA_CHUVA"].value_counts(normalize=True) * 100).round(2)
temp_med_FAIXA_CHUVA = df_completo_5.groupby("FAIXA_CHUVA")["temp_media"].mean().round(2)

print("\nProporção de dias com chuva forte ou muito forte por município:\n",
      tabela_chuva_municipio["Chuva forte ou muito forte"])
print("\nFrequência percentual geral de FAIXA_CHUVA:\n", freq_FAIXA_CHUVA)
print("\nTemperatura média por faixa de chuva:\n", temp_med_FAIXA_CHUVA)
print("\nTemperatura média por município e faixa de chuva:\n", tabela_temp_estruturada)

print("\n-----------------------------------------------------")

# =============================================================================
# QUESTÃO 6
# =============================================================================

print("\n-----------------------------------------------------")
print("\n 6 - Qual é o perfil racial e de sexo dos óbitos domiciliares de pessoas com mais de 79 anos, excluindo causas externas? \n")
print("\n-----------------------------------------------------")

df_completo_6 = df_completo_5.copy()

demais_causa        = df_completo_6[df_completo_6['GRUPO_CAUSA'] != 'Causas externas']
demais_causa_79     = demais_causa[demais_causa['IDADE_ANOS'] > 79]
demais_causa_79_local = demais_causa_79[demais_causa_79['LOCAL_DESC'] == 'Domicílio']

raca_sexo = demais_causa_79_local.groupby(['RACA_DESC', 'SEXO_DESC'])['CODMUNRES'].size()

print("\nPerfil racial e de sexo dos óbitos domiciliares de pessoas"
      " com mais de 79 anos, excluindo causas externas:\n")
print(raca_sexo)

print("\n-----------------------------------------------------")


# =============================================================================
# QUESTÃO 7
# =============================================================================

print("\n-----------------------------------------------------")
print("\n 7 - Municípios com maior precipitação acumulada e temperatura mais elevada apresentam maior volume ou perfil diferente de mortalidade? \n")
print("\n-----------------------------------------------------")

df_completo_7 = df_completo_6.copy()

clima_unico = df_completo_7.drop_duplicates(subset=['municipio_inmet', 'Data Medicao_date'])

df_maior_precip = clima_unico.groupby('municipio_inmet').agg({
    'precip_media': 'sum',
    'temp_media':   'max',
}).sort_values(by='precip_media', ascending=False)

df_volume_mort = df_completo_7.groupby('municipio_inmet').size().rename('Total_Obitos')

perfil_causa = df_completo_7.groupby('municipio_inmet').agg({
    'GRUPO_CAUSA': pd.Series.mode
})

df_analise_final = pd.concat([df_maior_precip, df_volume_mort, perfil_causa], axis=1)

print("Municípios com maior precipitação acumulada e temperatura mais elevada"
      " apresentam maior volume ou perfil diferente de mortalidade?\n")
print(df_analise_final)

print("\n-----------------------------------------------------")

# =============================================================================
# QUESTÃO 8
# =============================================================================

print("\n-----------------------------------------------------")
print("\n 8 - Como a mortalidade por doenças respiratórias e circulatórias se distribui ao longo dos meses de 2024 e existe sazonalidade nesse padrão? \n")
print("\n-----------------------------------------------------")

df_completo_8 = df_completo_7.copy()
df_completo_8['MES_INMET'] = pd.to_datetime(df_completo_8['Data Medicao']).dt.month

df_completo_8_circ = df_completo_8[df_completo_8['GRUPO_CAUSA'] == 'Doenças circulatórias'].copy()
freq_doencas_circ  = df_completo_8_circ['MES_INMET'].value_counts().sort_index()

df_completo_8_resp = df_completo_8[df_completo_8['GRUPO_CAUSA'] == 'Doenças respiratórias'].copy()
freq_doencas_resp  = df_completo_8_resp['MES_INMET'].value_counts().sort_index()

print("\nDistribuição mensal de 2024 — doenças circulatórias:\n", freq_doencas_circ)
print("\nDistribuição mensal de 2024 — doenças respiratórias:\n", freq_doencas_resp)

print("\n-----------------------------------------------------")