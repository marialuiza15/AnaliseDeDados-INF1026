from leituras.leitura_INMET import junta_clima
from leituras.leitura_IBGE import municipios_rj_unicos
from leituras.leitura_SUS import junta_sus

df_clima = junta_clima()
df_ibge = municipios_rj_unicos()
df_saude = junta_sus()

df_ibge["UF"] = "RJ"

# Amostras de cada DataFrame para conhecimento das colunas e dados

print("\nColunas INMET:")
print(df_clima.head(1), 
      "\nColunas do clima INMET:", df_clima.columns.tolist(), 
      "\nTotal de linhas INMET:", len(df_clima), 
      "\nTotal de estações INMET:", df_clima["codigo_estacao_inmet"].nunique(),
      "\nTotal de municípios INMET:", df_clima["municipio_inmet"].nunique(),
      "\nLista de municípios INMET:", df_clima["municipio_inmet"].drop_duplicates().tolist())


print("\nColunas IBGE:")
print(df_ibge.head(1), 
      "\nColunas do IBGE:", df_ibge.columns.tolist(), 
      "\nTotal de linhas IBGE:", len(df_ibge), 
      "\nTotal de municípios IBGE:", df_ibge["Código Município Completo"].nunique())

print("\nColunas SUS:")
print(df_saude.head(1), 
      "\nColunas do SUS:", df_saude.columns.tolist(), 
      "\nTotal de linhas SUS:", len(df_saude), 
      "\nTotal de municípios SUS:", df_saude["CODMUNOCOR"].nunique())

