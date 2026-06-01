import pandas as pd

def classificar_estacao(data):
    if pd.isna(data):
        return 'desconhecido'

    mes = data.month
    dia = data.day

    if (mes == 12 and dia >= 21) or (1 <= mes <= 2) or (mes == 3 and dia < 20):
        return 'verao'
    elif (mes == 3 and dia >= 20) or (4 <= mes <= 5) or (mes == 6 and dia < 21):
        return 'outono'
    elif (mes == 6 and dia >= 21) or (7 <= mes <= 8) or (mes == 9 and dia < 23):
        return 'inverno'
    elif (mes == 9 and dia >= 23) or (10 <= mes <= 11) or (mes == 12 and dia < 21):
        return 'primavera'
    return 'desconhecido'

def classificar_temperatura(temp):
    if temp < 0:
        return 'frio_extremo'
    elif temp < 20:
        return 'frio'
    elif temp < 25:
        return 'termico'
    elif temp < 35:
        return 'quente'
    else:
        return 'muito_quente'

def classificar_umidade(um):
    if um < 30:
        return 'muito_seco'
    elif um < 80:
        return 'normal'
    else:
        return 'muito_umido'

def engenharia_de_features(df):
    df = df.copy()
    if 'TEMPERATURA MEDIA, DIARIA (AUT)(Â°C)' in df.columns:
        df['TEMPERATURA_MEDIA'] = df['TEMPERATURA MEDIA, DIARIA (AUT)(Â°C)']
        df['temperatura_classe'] = df['TEMPERATURA_MEDIA'].apply(classificar_temperatura)
        
    if 'UMIDADE RELATIVA DO AR, MEDIA DIARIA (AUT)(%)' in df.columns:
        df['UMIDADE_MEDIA'] = df['UMIDADE RELATIVA DO AR, MEDIA DIARIA (AUT)(%)']
        df['umidade_classe'] = df['UMIDADE_MEDIA'].apply(classificar_umidade)

    if not df.empty and 'nu_idade' in df.columns:
        df['faixa_etaria'] = pd.cut(df['nu_idade'], bins=[0, 10, 40, 65, 150], labels=['<10', '10-40', '40-65', '>65'])
        df['clima_extremo'] = ((df['TEMPERATURA_MEDIA'] > 35) | (df['TEMPERATURA_MEDIA'] < 0)).astype(int) # Marca 1 para clima extremo e 0 para condições normais.

    df['risco_obito'] = 'Desconhecido'

    if 'data' in df.columns:
        df['estacao_ano'] = pd.to_datetime(df['data'], errors='coerce').apply(classificar_estacao)

    # NOVO: Região como string padronizada
    if 'Região' in df.columns:
        df['regiao'] = df['Região'].astype(str).str.lower().str.strip()


    # Crianças e idosos em calor extremo e muito seco
    cond1 = (df['faixa_etaria'].isin(['<10', '>65'])) & (df['temperatura_classe'] == 'muito_quente') & (df['umidade_classe'] == 'muito_seco')
    df.loc[cond1, 'risco_obito'] = 'Muito Alto'

    # Adultos jovens em calor extremo e muito seco
    cond2 = (df['faixa_etaria'].isin(['10-40', '40-65'])) & (df['temperatura_classe'] == 'muito_quente') & (df['umidade_classe'] == 'muito_seco')
    df.loc[cond2, 'risco_obito'] = 'Alto'

    # Crianças e idosos em frio extremo
    cond3 = (df['faixa_etaria'].isin(['<10', '>65'])) & (df['temperatura_classe'] == 'frio_extremo')
    df.loc[cond3, 'risco_obito'] = 'Muito Alto'

    # Adultos jovens em frio extremo
    cond4 = (df['faixa_etaria'].isin(['10-40', '40-65'])) & (df['temperatura_classe'] == 'frio_extremo')
    df.loc[cond4, 'risco_obito'] = 'Alto'

    # Ausência de climas extremos
    cond5 = (df['temperatura_classe'] == 'termico') & (df['umidade_classe'] == 'normal')
    df.loc[cond5, 'risco_obito'] = 'Baixo'

    return df
