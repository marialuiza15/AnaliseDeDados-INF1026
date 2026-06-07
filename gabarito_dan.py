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
# 1- Qual é o perfil (faixa etária, sexo, raça/cor) dos óbitos não fetais no RJ em 2024? 
# Requisitos atendidos: Req 3, Req 4b, Req 5.1,Req 6a,Req 7.2,Req 8a
# Objetivo: Identificar as faixas etárias, sexo e raça/cor predominantes entre os óbitos, revelando quais grupos populacionais concentram maior mortalidade.

print('\n1 — Perfil dos óbitos não fetais no RJ em 2024')

df_obitos_nao_fetais=dfSUS[dfSUS["TIPOBITO"]== '2'].copy()


def calcula_idade_anos(idade):
    idade = str(idade).zfill(3)

    unidade = idade[0]
    valor = int(idade[1:])

    if unidade == "4":
        return valor
    else:
        return 0
    
df_obitos_nao_fetais["IDADE_ANOS"]=df_obitos_nao_fetais["IDADE"].apply(calcula_idade_anos)

df_obitos_nao_fetais["FAIXA_ETARIA"]=pd.cut(
    df_obitos_nao_fetais["IDADE_ANOS"],
    bins=[0,14,29,59,79,120],
    labels=['Criança/Adolescente','Jovem','Adulto','Idoso','Muito idoso'],
    include_lowest=True
)  
mapa_sexo = {
    "1": "Masculino",
    "2": "Feminino",
    "0": "Ignorado"
}

mapa_raca = {
    "1": "Branca",
    "2": "Preta",
    "3": "Amarela",
    "4": "Parda",
    "5": "Indígena",
    "9": "Ignorado"
}

df_obitos_nao_fetais["SEXO_DESC"] = df_obitos_nao_fetais["SEXO"].map(mapa_sexo)
df_obitos_nao_fetais["RACA_DESC"] = df_obitos_nao_fetais["RACACOR"].map(mapa_raca).fillna("Ignorado")

print("o total de óbitos não fetais: ",df_obitos_nao_fetais["SEXO_DESC"].count())
print("a idade média dos óbitos não fetais: ",df_obitos_nao_fetais["IDADE_ANOS"].mean().round() )
print("a idade mínima e a idade máxima: ", df_obitos_nao_fetais["IDADE_ANOS"].min(),df_obitos_nao_fetais["IDADE_ANOS"].max())
print("a frequência absoluta de FAIXA_ETARIA:\n",df_obitos_nao_fetais["FAIXA_ETARIA"].value_counts() )
print("a frequência absoluta de SEXO_DESC:\n",df_obitos_nao_fetais["SEXO_DESC"].value_counts())
print("a frequência absoluta de RACA_DESC:\n",df_obitos_nao_fetais["RACA_DESC"].value_counts())

df_obitos_nao_fetais["FAIXA_ETARIA"].value_counts().plot(kind='bar')
plt.show()

# 3- A média de idade dos óbitos varia por grupo de causa de morte e por sexo?
# Requisitos atendidos: Req 2,Req 9a.2.
# Objetivo: Investigar se diferentes causas de morte atingem faixas etárias distintas e se esse padrão varia entre os sexos.


def classifica_causa(cid):
    cid=str(cid).upper()

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

df_obitos_nao_fetais["GRUPO_CAUSA"]=df_obitos_nao_fetais["CAUSABAS"].apply(classifica_causa)

saidaCross=pd.crosstab(
    index=df_obitos_nao_fetais["GRUPO_CAUSA"],
    columns=df_obitos_nao_fetais["SEXO_DESC"],
    values=df_obitos_nao_fetais["IDADE_ANOS"],
    aggfunc="mean"
)

saidaGroup=df_obitos_nao_fetais.groupby("GRUPO_CAUSA")["IDADE_ANOS"].mean().sort_values(ascending=False)
print("a MÉDIA de IDADE_ANOS para cada combinação entre grupo de causa de morte e sexo:\n ",saidaCross)
print("média geral de IDADE_ANOS por GRUPO_CAUSA ordenada da maior para a menor média\n ",saidaGroup)

# 5- Como se distribui a intensidade das chuvas diárias por município e qual é a temperatura média associada a cada nível de precipitação?
# Requisitos atendidos: Req 4b,Req 6b,Req 9b.2.
# Objetivo: Identificar quais municípios apresentam maior proporção de dias com chuva forte ou muito forte e qual a temperatura média em cada cenário pluviométrico.

print('\n5 — Intensidade das chuvas diárias por município e temperatura média')

dfINMET['PRECIPITACAO TOTAL, DIARIO (AUT)(mm)'] = (
    dfINMET['PRECIPITACAO TOTAL, DIARIO (AUT)(mm)']
    .astype(str)
    .str.replace(",", ".", regex=False)
)

dfINMET['PRECIPITACAO TOTAL, DIARIO (AUT)(mm)'] = pd.to_numeric(dfINMET['PRECIPITACAO TOTAL, DIARIO (AUT)(mm)'], errors="coerce")

dfINMET["FAIXA_CHUVA"]=pd.cut(
    dfINMET['PRECIPITACAO TOTAL, DIARIO (AUT)(mm)'],
    bins=[0,1,10,25,50,200],
    labels=['Sem chuva ou chuva muito fraca','Chuva fraca','Chuva moderada','Chuva forte','Chuva muito forte'],
    include_lowest=True
)
dfINMET["TEMPERATURA MEDIA, DIARIA (AUT)(°C)"] = (
    dfINMET["TEMPERATURA MEDIA, DIARIA (AUT)(°C)"]
    .astype(str)
    .str.replace(",", ".", regex=False)
)

dfINMET["TEMPERATURA MEDIA, DIARIA (AUT)(°C)"] = pd.to_numeric(
    dfINMET["TEMPERATURA MEDIA, DIARIA (AUT)(°C)"],
    errors="coerce"
)
tabela_chuva_municipio = pd.crosstab(
    index=dfINMET["municipio_inmet"],
    columns=dfINMET["FAIXA_CHUVA"],
    normalize="index"
) * 100


tabela_temp_estruturada = pd.crosstab(
    index=[
        dfINMET["municipio_inmet"],
        dfINMET["FAIXA_CHUVA"]
    ],
    columns=dfINMET["UF"],
    values=dfINMET["TEMPERATURA MEDIA, DIARIA (AUT)(°C)"],
    aggfunc="mean"
).round(2)

tabela_chuva_municipio["Chuva forte ou muito forte"] = (
    tabela_chuva_municipio.get("Chuva forte", 0) +
    tabela_chuva_municipio.get("Chuva muito forte", 0)
)

print("frequência percentual geral de FAIXA_CHUVA:\n",(dfINMET["FAIXA_CHUVA"].value_counts(normalize=True) * 100).round(2))

print("Distribuição percentual da intensidade de chuva por município:\n",tabela_chuva_municipio)

print("Temperatura média por faixa de chuva:\n",dfINMET.groupby("FAIXA_CHUVA")["TEMPERATURA MEDIA, DIARIA (AUT)(°C)"].mean().round(2))

print("Temperatura média por município e faixa de chuva:\n", tabela_temp_estruturada)

print("Municípios com maior proporção de dias de chuva forte ou muito forte:\n", tabela_chuva_municipio.sort_values(by="Chuva forte ou muito forte", ascending=False).head(10))


# 7- Municípios com maior precipitação acumulada e temperatura mais elevada apresentam maior volume ou perfil diferente de mortalidade?
# Requisitos atendidos: Req 1,Req 8c,Req 9b.2 .
# Objetivo: Investigar se municípios com condições climáticas mais extremas (mais chuva, temperaturas mais altas) apresentam padrões de mortalidade diferentes.
# -----------------------------------------------------------------------------
# 7) Municípios com maior precipitação acumulada e temperatura mais elevada
#    apresentam maior volume ou perfil diferente de mortalidade?
#
#    Usando as bases dfSUS, dfINMET e dfIBGE, faça a integração entre os dados
#    de mortalidade e os dados meteorológicos por município.
#
#    Para isso, utilize as funções já preparadas no projeto:
#      - criar_depara_inmet_ibge_sus()
#      - cruzar_sus_com_inmet()
#
#    Armazene o resultado integrado em df_mortalidade_clima.
#
#    Em seguida, agrupe os dados por município e calcule:
#      - total de óbitos não fetais
#      - precipitação acumulada no município
#      - temperatura média do município
#      - idade média dos óbitos
#
#    Depois, crie uma coluna PERFIL_CLIMATICO classificando os municípios
#    conforme precipitação acumulada e temperatura média:
#
#      - 'Mais chuvoso e mais quente'
#            quando a precipitação acumulada for acima da mediana
#            E a temperatura média for acima da mediana
#
#      - 'Mais chuvoso e menos quente'
#            quando a precipitação acumulada for acima da mediana
#            E a temperatura média for menor ou igual à mediana
#
#      - 'Menos chuvoso e mais quente'
#            quando a precipitação acumulada for menor ou igual à mediana
#            E a temperatura média for acima da mediana
#
#      - 'Menos chuvoso e menos quente'
#            quando a precipitação acumulada for menor ou igual à mediana
#            E a temperatura média for menor ou igual à mediana
#
#    Mostre:
#      - a tabela agregada por município
#      - os 10 municípios com maior precipitação acumulada
#      - os 10 municípios com maior temperatura média
#      - a média de óbitos e a idade média dos óbitos por PERFIL_CLIMATICO
#
#    Por fim, faça um pd.crosstab estruturado entre:
#      index = [PERFIL_CLIMATICO, município]
#      columns = grupo de causa de morte
#      values = IDADE_ANOS
#      aggfunc = 'mean'
#
#    Requisitos atendidos:
#      Req 1    - Integração/concatenação entre bases
#      Req 8c   - Agrupamento estruturado com mais de uma variável
#      Req 9b.2 - Cruzamento estruturado com medida de outra variável
#
#    Objetivo:
#      Investigar se municípios com condições climáticas mais extremas,
#      como maior precipitação acumulada e temperatura média mais elevada,
#      apresentam maior volume de óbitos ou perfil diferente de mortalidade.
# -----------------------------------------------------------------------------

print('\n7 — Mortalidade em municípios com maior chuva acumulada e maior temperatura')

# SEU CÓDIGO AQUI