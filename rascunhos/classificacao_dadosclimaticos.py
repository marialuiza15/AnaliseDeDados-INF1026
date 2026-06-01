import pandas as pd
import os

def classificar_umidade(umidade):
    """
    Classifica a umidade relativa do ar conforme as categorias definidas:
    - < 30% → "muito seco"
    - >= 30% e < 80% → "normal"
    - >= 80% → "muito úmido"
    """
    if umidade < 30:
        return "muito seco"
    elif 30 <= umidade < 80:
        return "normal"
    else:
        return "muito úmido"

def classificar_temperatura(temperatura):
    """
    Classifica a temperatura média diária conforme as categorias definidas:
    - < 0°C → "frio extremo"
    - >= 0°C e < 20°C → "frio"
    - >= 20°C e < 25°C → "térmico"
    - >= 25°C e < 35°C → "quente"
    - >= 35°C → "muito quente"
    """
    if temperatura < 0:
        return "frio extremo"
    elif 0 <= temperatura < 20:
        return "frio"
    elif 20 <= temperatura < 25:
        return "térmico"
    elif 25 <= temperatura < 35:
        return "quente"
    else:
        return "muito quente"

def processar_dados_climaticos(df):
    """
    Processa um DataFrame com dados climáticos, adicionando colunas de classificação
    """

    if 'UMIDADE RELATIVA DO AR, MEDIA DIARIA [AUT][%]' in df.columns:
        df['classificacao_umidade'] = df['UMIDADE RELATIVA DO AR, MEDIA DIARIA [AUT][%]'].apply(classificar_umidade)
    
    if 'TEMPERATURA MEDIA, DIARIA [AUT][°C]' in df.columns:
        df['classificacao_temperatura'] = df['TEMPERATURA MEDIA, DIARIA [AUT][°C]'].apply(classificar_temperatura)
    
    return df

estacoes_mg = {
    "A549": "AGUAS VERMELHAS",
    "A534": "AIMORES",
    "A504": "ALFENAS",
    "A508": "ALMENARA",
    "A566": "ARACUAI",
    "A505": "ARAXA",
    "A565": "BAMBUI",
    "A502": "BARBACENA",
    "A521": "BELO HORIZONTE (PAMPULHA)",
    "F501": "BELO HORIZONTE - CERCADINHO",
    "A544": "BURITIS",
    "A530": "CALDAS",
    "A519": "CAMPINA VERDE",
    "A541": "CAPELINHA",
    "A503": "CARANGOLA",
    "A554": "CARATINGA",
    "A548": "CHAPADA GAUCHA",
    "A520": "CONCEICAO DAS ALAGOAS",
    "A501": "CONTAGEM",
    "A557": "CORONEL PACHECO",
    "A538": "CURVELO",
    "A537": "DIAMANTINA",
    "A564": "DIVINOPOLIS",
    "A536": "DORES DO INDAIA",
    "A543": "ESPINOSA",
    "A535": "FLORESTAL",
    "A524": "FORMIGA",
    "A532": "GOVERNADOR VALADARES",
    "A533": "GUANHAES",
    "A546": "GUARDA-MOR",
    "A555": "IBIRITE (ROLA MOCA)",
    "A550": "ITAOBIM",
    "A512": "ITUIUTABA",
    "A559": "JANUARIA",
    "A553": "JOAO PINHEIRO",
    "A518": "JUIZ DE FORA",
    "A567": "MACHADO",
    "A556": "MANHUACU",
    "A540": "MANTENA",
    "A531": "MARIA DA FE",
    "A539": "MOCAMBINHO",
    "A526": "MONTALVANIA",
    "A509": "MONTE VERDE",
    "A506": "MONTES CLAROS",
    "A517": "MURIAE",
    "A563": "NOVA PORTEIRINHA (JANAUBA)",
    "A570": "OLIVEIRA",
    "A513": "OURO BRANCO",
    "A571": "PARACATU",
    "A529": "PASSA QUATRO",
    "A516": "PASSOS",
    "A562": "PATOS DE MINAS",
    "A523": "PATROCINIO",
    "A545": "PIRAPORA",
    "A560": "POMPEU",
    "A551": "RIO PARDO DE MINAS",
    "A525": "SACRAMENTO",
    "A552": "SALINAS",
    "A514": "SAO JOAO DEL REI",
    "A547": "SAO ROMAO",
    "A561": "SAO SEBASTIAO DO PARAISO",
    "A522": "SERRA DOS AIMORES",
    "A569": "SETE LAGOAS",
    "A527": "TEOFILO OTONI",
    "A511": "TIMOTEO",
    "A528": "TRES MARIAS",
    "A568": "UBERABA",
    "A507": "UBERLANDIA",
    "A542": "UNAI",
    "A515": "VARGINHA",
    "A510": "VICOSA"
}

def adicionar_coluna_local(df, nome_arquivo, codigo):
    """
    Adiciona coluna 'local' ao DataFrame baseado no código da estação no nome do arquivo
    """

    if codigo in estacoes_mg:
        df['local'] = estacoes_mg[codigo]
    else:
        df['local'] = None  

    return df

def processar_arquivo_climatico(caminho_arquivo):
    """
    Processa um arquivo climático completo:
    1. Carrega o CSV
    2. Adiciona a coluna 'local'
    3. Classifica temperatura e umidade
    """
    try:
        df = pd.read_csv(caminho_arquivo, sep=None, engine='python', skiprows=10, on_bad_lines='skip')
    except Exception as e:
        print(f"Erro ao carregar o arquivo {caminho_arquivo}: {str(e)}")
        return None

    nome_arquivo = os.path.basename(caminho_arquivo)

    codigo_estacao = None

    try:
        partes = nome_arquivo.split("_")
        if len(partes) > 2:
            codigo_estacao = partes[1]
    except Exception as e:
        print(f"Erro ao extrair código da estação: {str(e)}")

    nome_estacao = estacoes_mg[codigo_estacao]
    print(f"Estação correspondente ao código {codigo_estacao}: {nome_estacao}")

    df = adicionar_coluna_local(df, nome_arquivo, codigo_estacao)

    df = processar_dados_climaticos(df)

    return df

def processar_diretorio_climatico(diretorio_entrada, diretorio_saida=None):
    """
    Processa todos os arquivos CSV em um diretório, adicionando as colunas:
    - local (baseado no código no nome do arquivo)
    - classificacao_umidade
    - classificacao_temperatura
    """
    if diretorio_saida is None:
        diretorio_saida = diretorio_entrada

    os.makedirs(diretorio_saida, exist_ok=True)

    for arquivo in os.listdir(diretorio_entrada):
        if arquivo.endswith('.csv'):
            caminho_completo = os.path.join(diretorio_entrada, arquivo)
            
            try:
                df_processado = processar_arquivo_climatico(caminho_completo)

                nome_saida = f"processado_{arquivo}"
                caminho_saida = os.path.join(diretorio_saida, nome_saida)
                df_processado.to_csv(caminho_saida, index=False)
                
                print(f"Arquivo processado: {arquivo} -> {nome_saida}")
                
            except Exception as e:
                print(f"Erro ao processar {arquivo}: {str(e)}")

#usar para processar todos os arquivos:
processar_diretorio_climatico(r"analise-clima-doencas-mg/dados_clima_mg", r"analise-clima-doencas-mg/rascunhos/arquivos")