from leituras.leitura_INMET import junta_clima
from leituras.leitura_IBGE import junta_ibge
from leituras.leitura_SUS import junta_sus

df_clima = junta_clima()
df_ibge = junta_ibge()
df_saude = junta_sus()

