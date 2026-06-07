# -*- coding: utf-8 -*-
"""
EXERCÍCIO DE REVISÃO P2 — PANDAS
VIGILÂNCIA EPIDEMIOLÓGICA EM SAÚDE AMBIENTAL
Sistema de Informações sobre Mortalidade (SIM) · INMET · IBGE
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

################################################################################
# Nome completo:
# Matrícula:
# Declaração de autoria:
################################################################################

import pandas as pd
import matplotlib.pyplot as plt

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.float_format', '{:.2f}'.format)


"""
CONTEXTO:
O Ministério da Saúde, em parceria com o INMET e o IBGE, consolidou registros
de mortalidade, dados meteorológicos de estações automáticas e o cadastro
oficial de municípios brasileiros, com o objetivo de subsidiar a vigilância
epidemiológica em saúde ambiental.

A análise integra três dimensões:

1. Registros de mortalidade (SIM — Sistema de Informações sobre Mortalidade)
   Cada linha representa uma declaração de óbito (DO). As variáveis incluem
   data e local do óbito, características demográficas do falecido (sexo,
   raça/cor, escolaridade), causa básica de morte (código CID-10) e
   indicadores sobre o processo assistencial.

2. Condições meteorológicas (INMET — Instituto Nacional de Meteorologia)
   Dados diários de estações automáticas: precipitação total, temperatura
   média e umidade relativa do ar. Cada linha corresponde a um par
   (data, estação). A temperatura é armazenada com vírgula como separador
   decimal e deve ser convertida para float antes do uso.

3. Referência municipal (IBGE)
   Cadastro oficial com código de 7 dígitos, nome do município e UF.
   Para cruzamento com o campo CODMUNRES do SIM (6 dígitos), é necessário
   truncar o código do IBGE removendo o dígito verificador final (// 10).


DICIONÁRIO DE VARIÁVEIS RELEVANTES — dfSUS
──────────────────────────────────────────────────────────────────────────────
TIPOBITO    Tipo de óbito: 1 = fetal · 2 = não-fetal
DTOBITO     Data do óbito — formato DDMMAAAA (string) → converter para datetime
DTNASC      Data de nascimento — formato DDMMAAAA (string) → converter
IDADE       Código de idade:
                1º dígito = unidade (4 = anos · 3 = meses · 2 = dias · 1 = horas)
                Demais dígitos = valor
                Exemplo: 477 → 77 anos  |  340 → 40 meses  |  210 → 10 dias
SEXO        1 = Masculino · 2 = Feminino · 0 = Ignorado
RACACOR     1 = Branca · 2 = Preta · 3 = Amarela · 4 = Parda · 5 = Indígena · 9 = Ignorado
LOCOCOR     Local de ocorrência:
                1 = Hospital · 2 = Outro estab. de saúde · 3 = Domicílio
                4 = Via pública · 5 = Outros · 9 = Ignorado
CAUSABAS    Causa básica de morte (CID-10) — string alfanumérica
CODMUNRES   Código IBGE de 6 dígitos do município de residência do falecido
COVID_CLAS  Classificação COVID-19: 0 = não classificado · 1 = confirmado
──────────────────────────────────────────────────────────────────────────────

DICIONÁRIO DE VARIÁVEIS RELEVANTES — dfINMET
──────────────────────────────────────────────────────────────────────────────
Data Medicao                              Data da medição (datetime ou string)
PRECIPITACAO TOTAL, DIARIO (AUT)(mm)      Precipitação diária total em mm (numérico)
TEMPERATURA MEDIA, DIARIA (AUT)(°C)       Temperatura média diária em °C
                                          ⚠ Armazenada com vírgula — converter para float
UMIDADE RELATIVA DO AR, MEDIA DIARIA (AUT)(%)   Umidade relativa média (%)
codigo_estacao_inmet                      Código da estação automática
Regiao                                    Macro-região brasileira
municipio_inmet                           Município da estação
UF                                        Unidade federativa
──────────────────────────────────────────────────────────────────────────────

DICIONÁRIO DE VARIÁVEIS RELEVANTES — dfIBGE
──────────────────────────────────────────────────────────────────────────────
Código Município Completo    Código IBGE de 7 dígitos
Nome_Município               Nome oficial do município
UF                           Unidade federativa
──────────────────────────────────────────────────────────────────────────────


ARQUIVOS:
    dfSUS   ← DO_RJ_2024.csv     (ou equivalente fornecido pela professora)
    dfINMET ← inmet_consolidado.csv
    dfIBGE  ← municipios_ibge.csv

Atenção: os nomes dos arquivos e a forma de carregamento podem ser ajustados
         conforme os arquivos disponibilizados no ambiente de prova.
"""


# =============================================================================
# CARREGANDO DADOS
# =============================================================================

# Ajuste os caminhos conforme necessário:
from leituras.leitura_INMET import junta_clima
from leituras.leitura_IBGE import municipios_rj_unicos
from leituras.leitura_SUS import junta_sus

from scripts.cruzamento import criar_depara_inmet_ibge_sus, cruzar_sus_com_inmet


dfINMET = junta_clima()
dfIBGE = municipios_rj_unicos()
dfSUS = junta_sus()

print('\n==============================================')
print('Revisão P2 — Vigilância Epidemiológica / SIM · INMET · IBGE')
print('==============================================\n')

# =============================================================================
# QUESTÃO 1 — Limpeza e inspeção inicial dos dados
# =============================================================================

print('\n==============================================')
print('Questão 1 — Limpeza e inspeção inicial dos dados')
print('==============================================')


# -----------------------------------------------------------------------------
# 1.a) Em dfINMET, a coluna de temperatura está armazenada com VÍRGULA como
#      separador decimal (ex.: "23,4").
#
#      Converta a coluna 'TEMPERATURA MEDIA, DIARIA (AUT)(°C)' para float
#      usando .str.replace() seguido de .astype(float).
#      Armazene o resultado na MESMA coluna.
#
#      Mostre as estatísticas descritivas (.describe()) da coluna
#      ANTES e DEPOIS da conversão (dica: faça o describe antes de converter,
#      guarde em uma variável, converta, depois mostre os dois).
# -----------------------------------------------------------------------------

print('\n1.a — Conversão da temperatura: vírgula → float')
# SEU CÓDIGO AQUI
estatisticas_antes = dfINMET['TEMPERATURA MEDIA, DIARIA (AUT)(°C)'].describe()

dfINMET['TEMPERATURA MEDIA, DIARIA (AUT)(°C)'] = dfINMET['TEMPERATURA MEDIA, DIARIA (AUT)(°C)'].str.replace(',', '.').astype(float) #muda a virgula por ponto e converte para float.
estatisticas_depois = dfINMET['TEMPERATURA MEDIA, DIARIA (AUT)(°C)'].describe()

print("antes: ", estatisticas_antes) #variavel qualitativa
print("depois: ", estatisticas_depois) #variavel quantitativa


# # -----------------------------------------------------------------------------
# # 1.b) Em dfSUS, as colunas DTOBITO e DTNASC estão no formato DDMMAAAA
# #      (ex.: "01012024" = 1º de janeiro de 2024).
# #
# #      Converta ambas para datetime usando pd.to_datetime() com format='%d%m%Y'.
# #      Salve os resultados nas mesmas colunas.
# #
# #      A partir de DTNASC, crie as colunas:
# #          ANO_NASC  — ano do óbito (int)
# #          MES_NASC  — mês do óbito (int, 1 a 12)
# #
# #      Mostre:
# #          - o paciente mais velho e o mais novo na base (min e max de DTNASC)
# #          - a frequência de ANO_NASC
# # -----------------------------------------------------------------------------

print('\n1.b — Conversão de datas e criação de ANO_NASC e MES_NASC')
# SEU CÓDIGO AQUI

dfSUS['DTOBITO_formatada'] = pd.to_datetime(dfSUS['DTOBITO'], format='%d%m%Y')
dfSUS['DTNASC_formatada'] = pd.to_datetime(dfSUS['DTNASC'], format='%d%m%Y')

dfSUS['ANO_NASC']=dfSUS['DTNASC_formatada'].dt.year
dfSUS['MES_NASC']=dfSUS['DTNASC_formatada'].dt.month

antigo = dfSUS['DTNASC_formatada'].min()
recente = dfSUS['DTNASC_formatada'].max()

freq = dfSUS['ANO_NASC'].value_counts()

print(antigo)
print(recente)
print(freq)



# # -----------------------------------------------------------------------------
# # 1.c) Em dfSUS, a coluna IDADE usa um código composto:
# #          1º dígito = unidade  (4 = anos · 3 = meses · 2 = dias · 1 = horas)
# #          Demais dígitos = valor numérico
# #      Exemplos: 477 → 77 anos · 340 → 40 meses · 210 → 10 dias
# #
# #      Crie a função decodifica_idade(valor) que:
# #          - converta o valor para string de 3 dígitos (zfill(3))
# #          - extraia o 1º dígito (unidade) e os demais (valor)
# #          - retorne o valor em ANOS (float) se unidade == 4
# #          - retorne NaN para qualquer outra unidade (idade < 1 ano)
# #          - retorne NaN em caso de erro
# #
# #      Aplique com .apply() na coluna IDADE e armazene em IDADE_ANOS (float).
# #
# #      Mostre as estatísticas descritivas de IDADE_ANOS e
# #      quantos registros ficaram como NaN (idade < 1 ano).
# # -----------------------------------------------------------------------------

print('\n1.c — Decodificação da coluna IDADE → IDADE_ANOS')
# SEU CÓDIGO AQUI

def decodifica_idade(valor):
    valor = str(valor).zfill(3)
    primeiro_dig = valor[0]
    demais_dig = valor[1:]

    if primeiro_dig=='4':
        return float(demais_dig)
    else:
        return None

dfSUS['IDADE_ANOS'] = dfSUS['IDADE'].apply(decodifica_idade)
estatisticas_desc = dfSUS['IDADE_ANOS'].describe()
qtd_nan = dfSUS['IDADE_ANOS'].isna().sum()
print(estatisticas_desc)
print("\n", qtd_nan)


# # -----------------------------------------------------------------------------
# # 1.d) Em dfSUS, as colunas SEXO, RACACOR e LOCOCOR armazenam códigos numéricos.
# #      Crie os dicionários abaixo e use .map() para criar colunas legíveis:
# #
# #          SEXO_DESC  ← {1:'Masculino', 2:'Feminino', 0:'Ignorado'}
# #          RACA_DESC  ← {1:'Branca', 2:'Preta', 3:'Amarela',
# #                         4:'Parda', 5:'Indígena', 9:'Ignorado'}
# #          LOCAL_DESC ← {1:'Hospital', 2:'Outro estab. saúde',
# #                         3:'Domicílio', 4:'Via pública',
# #                         5:'Outros', 9:'Ignorado'}
# #
# #      Atenção: converta as colunas originais para int antes do map
# #               (use .astype(float).astype('Int64') para lidar com NaN).
# #
# #      Mostre value_counts() de cada nova coluna.
# # -----------------------------------------------------------------------------

print('\n1.d — Mapeamento de códigos: SEXO_DESC, RACA_DESC, LOCAL_DESC')
# SEU CÓDIGO AQUI

sexo_dic = {1:'Masculino', 2:'Feminino', 0:'Ignorado'}
raca_dic = {1:'Branca', 2:'Preta', 3:'Amarela', 4:'Parda', 5:'Indígena', 9:'Ignorado'}
local_dic = {1:'Hospital', 2:'Outro estab. saúde', 3:'Domicílio', 4:'Via pública', 5:'Outros', 9:'Ignorado'}

dfSUS['SEXO'] = dfSUS['SEXO'].astype(float).astype('Int64')
dfSUS['RACACOR'] = dfSUS['RACACOR'].astype(float).astype('Int64')
dfSUS['LOCOCOR'] = dfSUS['LOCOCOR'].astype(float).astype('Int64')

dfSUS['SEXO_DESC'] = dfSUS['SEXO'].map(sexo_dic)
dfSUS['RACA_DESC'] = dfSUS['RACACOR'].map(sexo_dic)
dfSUS['LOCAL_DESC'] = dfSUS['LOCOCOR'].map(sexo_dic)

freq_sexo = dfSUS['SEXO_DESC'].value_counts()
freq_raca = dfSUS['RACA_DESC'].value_counts()
freq_desc = dfSUS['LOCAL_DESC'].value_counts()

print(pd.DataFrame({
    'freq_sexo': freq_sexo,
    'freq_raca': freq_raca,
    'freq_desc': freq_desc
}))

# # =============================================================================
# # QUESTÃO 2 — Análise das condições meteorológicas
# # =============================================================================

print('\n==============================================')
print('Questão 2 — Análise das condições meteorológicas')
print('==============================================')


# # -----------------------------------------------------------------------------
# # 2.a) Em dfINMET, faça um gráfico de dispersão entre
# #      PRECIPITACAO TOTAL, DIARIO (AUT)(mm)  (eixo x)  e
# #      TEMPERATURA MEDIA, DIARIA (AUT)(°C)   (eixo y).
# #
# #      Calcule a correlação entre as duas variáveis para:
# #          i)  todos os registros
# #          ii) apenas os dias com precipitação > 0 (dias chuvosos)
# #
# #      Exiba os dois valores de correlação em um único print comparativo.
# # -----------------------------------------------------------------------------

print('\n2.a — Dispersão e correlação: precipitação x temperatura')
# SEU CÓDIGO AQUI

dfINMET_copy = dfINMET.dropna(subset=['PRECIPITACAO TOTAL, DIARIO (AUT)(mm)', 'TEMPERATURA MEDIA, DIARIA (AUT)(°C)'])

dfINMET_copy.plot.scatter(
    x='PRECIPITACAO TOTAL, DIARIO (AUT)(mm)', 
    y='TEMPERATURA MEDIA, DIARIA (AUT)(°C)', 
    color='blue', 
    marker='o', 
    s=50
    )
plt.show()

dfINMET_copy['PRECIPITACAO TOTAL, DIARIO (AUT)(mm)'] = dfINMET_copy['PRECIPITACAO TOTAL, DIARIO (AUT)(mm)'].astype(str).str.replace(',', '.').astype(float)
dfINMET_copy['TEMPERATURA MEDIA, DIARIA (AUT)(°C)'] = dfINMET_copy['TEMPERATURA MEDIA, DIARIA (AUT)(°C)'].astype(str).str.replace(',', '.').astype(float)

correlacao = dfINMET_copy['PRECIPITACAO TOTAL, DIARIO (AUT)(mm)'].corr(dfINMET_copy['TEMPERATURA MEDIA, DIARIA (AUT)(°C)'])

cond = dfINMET_copy['PRECIPITACAO TOTAL, DIARIO (AUT)(mm)']>0 #retorna true e false #dias com chuva

correlacao = dfINMET_copy[cond]['PRECIPITACAO TOTAL, DIARIO (AUT)(mm)'].corr(dfINMET_copy['TEMPERATURA MEDIA, DIARIA (AUT)(°C)'])
print(correlacao)

# # -----------------------------------------------------------------------------
# # 2.b) Agrupando dfINMET por municipio_inmet, calcule em um único .agg() com dicionário:
# #          - média de temperatura
# #          - total (soma) de precipitação
# #          - média de umidade relativa
# #
# #      Ordene pelo maior total de precipitação.
# #      Mostre o resultado completo.
# # -----------------------------------------------------------------------------

print('\n2.b — Estatísticas meteorológicas por municipio_inmet')
# SEU CÓDIGO AQUI

def converte(v):
    return float(str(v).replace(',', '.'))


dfINMET_copy = dfINMET.copy()
dfINMET_copy['TEMPERATURA MEDIA, DIARIA (AUT)(°C)'] = dfINMET_copy['TEMPERATURA MEDIA, DIARIA (AUT)(°C)'].apply(converte)
dfINMET_copy['PRECIPITACAO TOTAL, DIARIO (AUT)(mm)'] = dfINMET_copy['PRECIPITACAO TOTAL, DIARIO (AUT)(mm)'].apply(converte)
dfINMET_copy['UMIDADE RELATIVA DO AR, MEDIA DIARIA (AUT)(%)'] = dfINMET_copy['UMIDADE RELATIVA DO AR, MEDIA DIARIA (AUT)(%)'].apply(converte)

dfINMET_municipio_inmet = dfINMET_copy.groupby('municipio_inmet').agg({
    'TEMPERATURA MEDIA, DIARIA (AUT)(°C)': 'mean',
    'PRECIPITACAO TOTAL, DIARIO (AUT)(mm)':'sum',
    'UMIDADE RELATIVA DO AR, MEDIA DIARIA (AUT)(%)': 'mean',
})

dfINMET_municipio_inmet = dfINMET_municipio_inmet.sort_values('PRECIPITACAO TOTAL, DIARIO (AUT)(mm)', ascending=False)

print(dfINMET_municipio_inmet)


# # -----------------------------------------------------------------------------
# # 2.c) Em dfINMET, converta 'Data Medicao' para datetime (se ainda não for).
# #      Crie a coluna MES_INMET extraindo o mês (1 a 12).
# #
# #      Classifique cada mês em 'Chuvoso' (meses 11, 12, 1, 2, 3)
# #      ou 'Seco' (demais meses) e armazene em ESTACAO_CHUVA.
# #      (Use .isin() com a lista de meses chuvosos.)
# #
# #      Compare — por ESTACAO_CHUVA e municipio_inmet juntos (groupby com lista) —
# #      a média de temperatura e a média de precipitação.
# #      Mostre os resultados ordenados por municipio_inmet.
# # -----------------------------------------------------------------------------

print('\n2.c — Temperatura e precipitação: estação chuvosa vs. seca por municipio_inmet')
# SEU CÓDIGO AQUI

dfINMET_copy = dfINMET.copy()
dfINMET_copy['MES_INMET'] = pd.to_datetime(dfINMET_copy['Data Medicao']).dt.month

def converte(v):
    return float(str(v).replace(',', '.'))

dfINMET_copy['TEMPERATURA MEDIA, DIARIA (AUT)(°C)'] = dfINMET_copy['TEMPERATURA MEDIA, DIARIA (AUT)(°C)'].apply(converte)
dfINMET_copy['PRECIPITACAO TOTAL, DIARIO (AUT)(mm)'] = dfINMET_copy['PRECIPITACAO TOTAL, DIARIO (AUT)(mm)'].apply(converte)

lista_classif = [11,12,1,2,3]
condicao = dfINMET_copy['MES_INMET'].isin(lista_classif)
dfINMET_copy.loc[condicao, 'ESTACAO_CHUVA'] = 'Chuvoso'
dfINMET_copy.loc[~condicao, 'ESTACAO_CHUVA'] = 'Seco'

dfINMET_copy_g = dfINMET_copy.groupby(['ESTACAO_CHUVA', 'municipio_inmet']).agg({
    'TEMPERATURA MEDIA, DIARIA (AUT)(°C)': 'mean',
    'PRECIPITACAO TOTAL, DIARIO (AUT)(mm)': 'mean',
})

print(dfINMET_copy_g.sort_values('municipio_inmet'))

# # =============================================================================
# # QUESTÃO 3 — Perfil de mortalidade
# # =============================================================================

print('\n==============================================')
print('Questão 3 — Perfil de mortalidade')
print('==============================================')


# # -----------------------------------------------------------------------------
# # 3.a) Em dfSUS, usando IDADE_ANOS, crie a coluna FAIXA_ETARIA com pd.cut
# #      e os seguintes intervalos e rótulos:
# #
# #          0  até 14  →  'Criança/Adolescente'
# #         14  até 29  →  'Jovem'
# #         29  até 59  →  'Adulto'
# #         59  até 79  →  'Idoso'
# #         79  até 120 →  'Muito idoso'
# #
# #      Mostre a frequência absoluta de cada faixa.
# #      Faça um gráfico de barras verticais com a frequência de FAIXA_ETARIA.
# # -----------------------------------------------------------------------------

print('\n3.a — FAIXA_ETARIA com pd.cut')
# SEU CÓDIGO AQUI

bins = [0,14,29,59,79,120]
labels = ['Criança/Adolescente','Jovem','Adulto','Idoso','Muito idoso']

dfSUS['FAIXA_ETARIA'] = pd.cut(dfSUS['IDADE_ANOS'], bins=bins, labels=labels)

freq = dfSUS['FAIXA_ETARIA'].value_counts()

freq.plot(kind='bar')
plt.show()

print(freq)


# # -----------------------------------------------------------------------------
# # 3.b) Em dfSUS, crie a coluna GRUPO_CAUSA classificando CAUSABAS pelo
# #      primeiro caractere (letra inicial do CID-10):
# #
# #          Começa com 'I'           →  'Doenças circulatórias'
# #          Começa com 'J'           →  'Doenças respiratórias'
# #          Começa com 'C' ou 'D0'-'D4' →  'Neoplasias'
# #          Começa com V, W, X ou Y  →  'Causas externas'
# #          Começa com 'U07'         →  'COVID-19'
# #          Demais                   →  'Outras causas'
# #
# #      Crie a função classifica_causa(cid) e aplique com .apply().
# #
# #      Faça um pd.crosstab entre GRUPO_CAUSA e SEXO_DESC,
# #      com totais de linha e coluna (margins=True).
# # -----------------------------------------------------------------------------

print('\n3.b — GRUPO_CAUSA e crosstab por sexo')
# SEU CÓDIGO AQUI

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

dfSUS['GRUPO_CAUSA'] = dfSUS['CAUSABAS'].apply(classifica_causa)

df = pd.crosstab(dfSUS['GRUPO_CAUSA'], dfSUS['SEXO_DESC'])

print(df.head(3))

# # -----------------------------------------------------------------------------
# # 3.c) Filtrando apenas óbitos NÃO FETAIS (TIPOBITO == '2'):
# #
# #      3.c-1) Mostre os 10 códigos de CAUSABAS mais frequentes,
# #             com sua frequência absoluta e relativa (%).
# #
# #      3.c-2) Mostre a distribuição de LOCAL_DESC (value_counts)
# #             e faça um gráfico de barras horizontais com o resultado.
# #
# #      3.c-3) Mostre a média de IDADE_ANOS por LOCAL_DESC,
# #             ordenada da maior para a menor média.
# # -----------------------------------------------------------------------------

print('\n3.c — Causas, local e idade nos óbitos não fetais')
# SEU CÓDIGO AQUI

cond = dfSUS['TIPOBITO'] == '2'

df_naofetais = dfSUS.loc[cond]

top10_causabas_freqAbs = df_naofetais['CAUSABAS'].value_counts().head(10)
top10_causabas_freqRel = top10_causabas_freqAbs/top10_causabas_freqAbs.sum() * 100
print(top10_causabas_freqAbs , top10_causabas_freqRel)

dist_local = df_naofetais['LOCAL_DESC'].value_counts()

dist_local.plot(kind='bar')
plt.show()

df = dfSUS.groupby('LOCAL_DESC').agg({
    'IDADE_ANOS': 'mean'
}).sort_values(by='IDADE_ANOS', ascending=False)

print(df)

# # =============================================================================
# # QUESTÃO 4 — Integração entre bases de dados
# # =============================================================================

print('\n==============================================')
print('Questão 4 — Integração entre bases de dados')
print('==============================================')


# # -----------------------------------------------------------------------------
# # 4.a) O código de município no dfIBGE tem 7 dígitos (incluindo dígito verificador).
# #      O campo CODMUNRES do dfSUS tem 6 dígitos (sem o dígito verificador).
# #
# #      Crie em dfIBGE a coluna 'cod_6dig' removendo o último dígito:
# #          dfIBGE['cod_6dig'] = dfIBGE['Código Município Completo'] // 10
# #      (garanta que a coluna seja int antes da operação)
# #
# #      Converta CODMUNRES de dfSUS para int (use .astype(float).astype('Int64')).
# #
# #      Faça um merge de dfSUS com dfIBGE usando:
# #          left_on='CODMUNRES', right_on='cod_6dig', how='left'
# #
# #      Armazene o resultado em dfMerge.
# #      Mostre quantas linhas têm o campo Nome_Município preenchido (não-nulo)
# #      e quantas ficaram sem correspondência.
# # -----------------------------------------------------------------------------

print('\n4.a — Merge dfSUS + dfIBGE por código de município')
# SEU CÓDIGO AQUI

dfIBGE['Código Município Completo'] = dfIBGE['Código Município Completo'].astype('float').astype('Int64')

dfIBGE['cod_6dig'] = dfIBGE['Código Município Completo'] // 10

dfSUS['CODMUNRES'] = dfSUS['CODMUNRES'].astype('float').astype('Int64')

dfMerge = pd.merge(dfSUS, dfIBGE, left_on='CODMUNRES', right_on='cod_6dig', how='left')

qtd_null = dfMerge['Nome_Município'].isnull().sum()
qtd_notnull = dfMerge['Nome_Município'].notnull().sum()

print(qtd_null, qtd_notnull)

# # -----------------------------------------------------------------------------
# # 4.b) Usando dfMerge, agrupe por Nome_Município e calcule, em um único .agg():
# #          - total de óbitos (count de DTOBITO)
# #          - causa mais frequente (lambda: .mode()[0] se não vazio, else NaN)
# #          - média de IDADE_ANOS
# #
# #      Ordene pelo maior total de óbitos.
# #      Mostre os 15 municípios com mais óbitos.
# # -----------------------------------------------------------------------------

print('\n4.b — Óbitos, causa mais frequente e idade média por município')
# SEU CÓDIGO AQUI

dfMerge['DTOBITO'] = pd.to_datetime(dfMerge['DTOBITO'], format='%d%m%Y')

dfMerge_ag = dfMerge.groupby('Nome_Município').agg({
    'DTOBITO': 'mean',
    'GRUPO_CAUSA': pd.Series.mode,
    'IDADE_ANOS': 'mean',
    'CODMUNRES': 'count'
})

dfMerge_ag_ord = dfMerge_ag.sort_values('CODMUNRES', ascending=False).head(15)

print(dfMerge_ag_ord)

# # -----------------------------------------------------------------------------
# # 4.c) Em dfINMET, o campo municipio_inmet contém o nome do município da estação.
# #
# #      Crie dfClimaMun agrupando dfINMET por municipio_inmet:
# #          - média de temperatura
# #          - total de precipitação
# #          - média de umidade
# #
# #      Crie dfMortalidademunicipio_inmet agrupando dfMerge pela coluna 'municipio_inmet' do IBGE
# #      (coluna 'municipio_inmet_y' se surgir sufixo, ajuste conforme necessário):
# #          - total de óbitos (count de DTOBITO)
# #          - média de IDADE_ANOS
# #
# #      Concatene dfClimaMun e dfMortalidademunicipio_inmet (axis=1, usando o índice municipio_inmet).
# #      Armazene em dfmunicipio_inmet
# #      Mostre dfmunicipio_inmet completo.
# # -----------------------------------------------------------------------------

print('\n4.c — Integração clima x mortalidade por UF')
# SEU CÓDIGO AQUI

dfINMET['PRECIPITACAO TOTAL, DIARIO (AUT)(mm)'] = dfINMET['PRECIPITACAO TOTAL, DIARIO (AUT)(mm)'].replace(',','.', regex=True).astype('float')
dfINMET['TEMPERATURA MEDIA, DIARIA (AUT)(°C)'] = dfINMET['TEMPERATURA MEDIA, DIARIA (AUT)(°C)'].replace(',','.', regex=True).astype('float')
dfINMET['UMIDADE RELATIVA DO AR, MEDIA DIARIA (AUT)(%)'] = dfINMET['UMIDADE RELATIVA DO AR, MEDIA DIARIA (AUT)(%)'].replace(',','.', regex=True).astype('float')

dfClimaMun = dfINMET.groupby('municipio_inmet').agg({
    'PRECIPITACAO TOTAL, DIARIO (AUT)(mm)': 'mean',
    'TEMPERATURA MEDIA, DIARIA (AUT)(°C)': 'sum',
    'UMIDADE RELATIVA DO AR, MEDIA DIARIA (AUT)(%)' : 'mean'
})

dfMortalidademunicipio_inmet = dfMerge.groupby('municipio_inmet').agg({
    'DTOBITO': 'count',
    'IDADE_ANOS': 'mean'
})

dfmunicipio_inmet = pd.concat([dfClimaMun, dfMortalidademunicipio_inmet], axis=1)

print(dfmunicipio_inmet)
# # =============================================================================
# # QUESTÃO 5 — Categorias de precipitação e indicador de vulnerabilidade climática
# # =============================================================================

# print('\n==============================================')
# print('Questão 5 — Categorias de chuva e vulnerabilidade climática')
# print('==============================================')


# # -----------------------------------------------------------------------------
# # 5.a) Em dfINMET, crie a coluna INTENSIDADE_CHUVA classificando
# #      a precipitação diária com pd.cut e bins manuais:
# #
# #          -0.1 até  0   →  'Sem chuva'
# #           0   até  5   →  'Chuva fraca'
# #           5   até 25   →  'Chuva moderada'
# #          25   até 50   →  'Chuva forte'
# #          50   até 999  →  'Chuva muito forte'
# #
# #      (use include_lowest=True e right=True no pd.cut)
# #
# #      Mostre a frequência absoluta de cada categoria.
# #      Mostre um gráfico de barras verticais com essa frequência.
# # -----------------------------------------------------------------------------

# print('\n5.a — Coluna INTENSIDADE_CHUVA por faixas de precipitação')

# # SEU CÓDIGO AQUI


# # -----------------------------------------------------------------------------
# # 5.b) Faça um pd.crosstab entre UF e INTENSIDADE_CHUVA.
# #
# #      Mostre também a versão normalizada por LINHA (normalize='index'),
# #      multiplicada por 100 e arredondada para 1 casa decimal,
# #      para revelar a PROPORÇÃO de cada tipo de chuva por UF.
# #
# #      Interprete em um print qual UF apresenta maior proporção de dias
# #      sem chuva e qual apresenta maior proporção de chuva muito forte.
# # -----------------------------------------------------------------------------

# print('\n5.b — Crosstab UF x INTENSIDADE_CHUVA (absoluto e proporção por linha %)')

# # SEU CÓDIGO AQUI


# # -----------------------------------------------------------------------------
# # 5.c) Usando dfUF (construído em 4.c), crie a coluna RISCO_CLIMATICO
# #      com TRÊS categorias, seguindo a lógica de precedência abaixo:
# #
# #      Passo 1 — Marque como 'Atenção' quando PELO MENOS UMA for verdadeira:
# #          Condição P: precipitação total acima da mediana do grupo
# #          Condição T: temperatura média acima de 26 °C
# #
# #      Passo 2 — Sobreponha 'Risco elevado' quando:
# #          Condição P E Condição T forem verdadeiras simultaneamente
# #
# #      Demais casos: 'Baixo risco'.
# #
# #      Mostre a frequência de RISCO_CLIMATICO.
# #      Mostre dfUF com a nova coluna.
# # -----------------------------------------------------------------------------

# print('\n5.c — Coluna RISCO_CLIMATICO em dfUF')

# # SEU CÓDIGO AQUI


# # =============================================================================
# # QUESTÃO 6 — Grupo de atenção prioritária
# # =============================================================================

# print('\n==============================================')
# print('Questão 6 — Grupo de atenção prioritária')
# print('==============================================')


# # -----------------------------------------------------------------------------
# # 6.a) A partir de dfMerge, crie dfGrupoPrioritario contendo apenas os óbitos
# #      que atendem SIMULTANEAMENTE a todos os critérios abaixo:
# #
# #          TIPOBITO      == '2'           (óbito não fetal)
# #          LOCAL_DESC    == 'Domicílio'   (faleceu em casa)
# #          FAIXA_ETARIA  == 'Muito idoso' (acima de 79 anos)
# #          GRUPO_CAUSA   != 'Causas externas'
# #
# #      Remova colunas com mais de 80% de valores ausentes de dfGrupoPrioritario
# #      usando o seguinte padrão:
# #          thresh = int(0.2 * len(dfGrupoPrioritario))
# #          dfGrupoPrioritario = dfGrupoPrioritario.dropna(axis=1, thresh=thresh)
# #
# #      Mostre a quantidade de óbitos no grupo e os primeiros registros
# #      das colunas: Nome_Município, SEXO_DESC, RACA_DESC, IDADE_ANOS,
# #                   GRUPO_CAUSA, CAUSABAS, DTOBITO.
# # -----------------------------------------------------------------------------

# print('\n6.a — Construção do dfGrupoPrioritario')

# # SEU CÓDIGO AQUI


# # -----------------------------------------------------------------------------
# # 6.b) Mostre, para dfGrupoPrioritario:
# #
# #      6.b-1) Um gráfico de barras verticais com a quantidade de óbitos
# #             por GRUPO_CAUSA.
# #
# #      6.b-2) A média e o desvio padrão de IDADE_ANOS por SEXO_DESC
# #             e GRUPO_CAUSA juntos (groupby com lista de colunas),
# #             ordenado pela maior média de IDADE_ANOS.
# #
# #      6.b-3) A distribuição mensal de óbitos (frequência de MES_OBITO),
# #             mostrando em qual mês concentra-se o maior número de mortes
# #             do grupo prioritário.
# # -----------------------------------------------------------------------------

# print('\n6.b — Análise do grupo prioritário: causas, idade e sazonalidade')

# # SEU CÓDIGO AQUI


# # -----------------------------------------------------------------------------
# # 6.c) Mostre a quantidade de óbitos do grupo prioritário no cruzamento:
# #          [GRUPO_CAUSA]  ×  [RACA_DESC, SEXO_DESC]
# #
# #      Use pd.crosstab com margins=True.
# #      Substitua os valores NaN por '-'.
# #
# #      Em seguida, usando dfUF (Q4.c), mostre a média de temperatura e
# #      o total de precipitação para as UFs que aparecem no grupo prioritário.
# #      (filtre dfUF pelas UFs presentes em dfGrupoPrioritario['UF_y'])
# # -----------------------------------------------------------------------------

# print('\n6.c — Grupo prioritário: causa × raça/sexo e contexto climático das UFs')

# # SEU CÓDIGO AQUI


# # =============================================================================
# # QUESTÃO 7 — PONTO EXTRA (0,5 pt)
# # =============================================================================

# print('\n==============================================')
# print('Questão 7 — Síntese interpretativa (PONTO EXTRA — 0,5 pt)')
# print('==============================================')

# # -----------------------------------------------------------------------------
# # 7) Escolha UMA das perguntas abaixo e redija entre 3 e 5 linhas.
# #    Indique qual pergunta escolheu.
# #    Use expressões como "na amostra", "os dados sugerem", "aparece associado".
# #    NÃO afirme causalidade.
# #
# #    PERGUNTA A — Com base em Q2.a e Q2.c:
# #        A correlação entre precipitação e temperatura é positiva ou negativa?
# #        O que os dados sugerem sobre a diferença de temperatura entre a estação
# #        chuvosa e a seca na amostra? Esse padrão é uniforme entre as UFs?
# #
# #    PERGUNTA B — Com base em Q3.b e Q6.b:
# #        Quais grupos de causas se destacam nos óbitos domiciliares de muito idosos?
# #        O que os dados sugerem sobre a distribuição por sexo e raça/cor nesse
# #        grupo? Esse resultado merece atenção do ponto de vista da saúde pública?
# #
# #    PERGUNTA C — Com base em Q4.c e Q5.c:
# #        O que os dados sugerem sobre a relação entre condições climáticas (chuva
# #        e temperatura) e o volume de mortalidade por UF? As UFs classificadas
# #        como 'Risco elevado' em Q5.c apresentam padrão distinto de mortalidade?
# # -----------------------------------------------------------------------------

# print('\nPergunta escolhida (A, B ou C):')
# print('ESCREVA AQUI A LETRA DA PERGUNTA ESCOLHIDA')

# print('\nResposta:')
# print('ESCREVA AQUI SUA ANÁLISE')