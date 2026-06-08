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
# Requisitos atendidos: Req 3, Req 4b, Req 5.1, Req 6a, Req 7.2, Req 8a
# Objetivo: Identificar as faixas etárias, sexo e raça/cor predominantes entre os óbitos,
#           revelando quais grupos populacionais concentram maior mortalidade.

# SEU CÓDIGO AQUI


# =============================================================================
# QUESTÃO 2
# =============================================================================

print("\n-----------------------------------------------------")
print("\n 2 - Quais são os grupos de causa de morte mais frequentes e como se distribuem entre homens e mulheres? \n")
print("\n-----------------------------------------------------")
# Requisitos atendidos: Req 3, Req 5.3, Req 6b, Req 9a.1
# Objetivo: Identificar as causas que lideram a mortalidade no RJ e verificar
#           se há diferença na frequência entre homens e mulheres.

# SEU CÓDIGO AQUI


# =============================================================================
# QUESTÃO 3
# =============================================================================

print("\n-----------------------------------------------------")
print("\n 3 - A média de idade dos óbitos varia por grupo de causa de morte e por sexo? \n")
print("\n-----------------------------------------------------")
# Requisitos atendidos: Req 2, Req 9a.2
# Objetivo: Investigar se diferentes causas de morte atingem faixas etárias distintas
#           e se esse padrão varia entre os sexos.

# SEU CÓDIGO AQUI


# =============================================================================
# QUESTÃO 4
# =============================================================================

print("\n-----------------------------------------------------")
print("\n 4 - Como variam temperatura, precipitação acumulada e umidade relativa entre os municípios do INMET no RJ? \n")
print("\n-----------------------------------------------------")
# Requisitos atendidos: Req 3, Req 4a, Req 5.1, Req 7.1, Req 8b
# Objetivo: Caracterizar o perfil climático dos municípios fluminenses e verificar
#           a existência de correlação entre temperatura e precipitação.

# SEU CÓDIGO AQUI


# =============================================================================
# QUESTÃO 5
# =============================================================================

print("\n-----------------------------------------------------")
print("\n 5 - Como se distribui a intensidade das chuvas diárias por município e qual é a temperatura média associada a cada nível de precipitação? \n")
print("\n-----------------------------------------------------")
# Requisitos atendidos: Req 4b, Req 6b, Req 9b.2
# Objetivo: Identificar quais municípios apresentam maior proporção de dias com chuva forte
#           ou muito forte e qual a temperatura média em cada cenário pluviométrico.

# SEU CÓDIGO AQUI


# =============================================================================
# QUESTÃO 6
# =============================================================================

print("\n-----------------------------------------------------")
print("\n 6 - Qual é o perfil racial e de sexo dos óbitos domiciliares de pessoas com mais de 79 anos, excluindo causas externas? \n")
print("\n-----------------------------------------------------")
# Requisitos atendidos: Req 5.3, Req 5.4, Req 7.2, Req 9b.1
# Objetivo: Identificar vulnerabilidades específicas da população muito idosa que falece
#           em domicílio, investigando quais grupos raciais e de sexo são mais afetados.

# SEU CÓDIGO AQUI


# =============================================================================
# QUESTÃO 7
# =============================================================================

print("\n-----------------------------------------------------")
print("\n 7 - Municípios com maior precipitação acumulada e temperatura mais elevada apresentam maior volume ou perfil diferente de mortalidade? \n")
print("\n-----------------------------------------------------")
# Requisitos atendidos: Req 1, Req 8c, Req 9b.2
# Objetivo: Investigar se municípios com condições climáticas mais extremas apresentam
#           padrões de mortalidade diferentes dos demais.

# SEU CÓDIGO AQUI


# =============================================================================
# QUESTÃO 8
# =============================================================================

print("\n-----------------------------------------------------")
print("\n 8 - Como a mortalidade por doenças respiratórias e circulatórias se distribui ao longo dos meses de 2024 e existe sazonalidade nesse padrão? \n")
print("\n-----------------------------------------------------")
# Requisitos atendidos: Req 5.3, Req 8c, Req 9a.1, Req 7
# Objetivo: Investigar se os óbitos por causas respiratórias e circulatórias aumentam
#           em meses frios, conectando o padrão temporal de mortalidade com as condições
#           climáticas analisadas nas perguntas anteriores.

# SEU CÓDIGO AQUI