from leituras.leitura_INMET import junta_clima
from leituras.leitura_IBGE import municipios_rj_unicos
from leituras.leitura_SUS import junta_sus

df_clima = junta_clima()
df_ibge = municipios_rj_unicos()
df_saude = junta_sus()

