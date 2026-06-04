import pandas as pd

arquivo_entrada = r"C:\Users\user\Desktop\PYTHON\AnaliseDeDados-INF1026\dados\SUS\DO24OPEN.csv"
arquivo_saida = r"C:\Users\user\Desktop\PYTHON\AnaliseDeDados-INF1026\dados\SUS\DO24OPEN_RJ_RES_OU_OCOR.csv"

primeiro_chunk = True
total_linhas = 0

for chunk in pd.read_csv(
    arquivo_entrada,
    sep=";",
    dtype=str,
    chunksize=100_000,
    low_memory=False
):
    # Remove colunas vazias tipo Unnamed
    chunk = chunk.loc[:, ~chunk.columns.str.contains("^Unnamed")]

    # Garante que as colunas existem como texto
    chunk["CODMUNRES"] = chunk["CODMUNRES"].astype(str).str.strip()
    chunk["CODMUNOCOR"] = chunk["CODMUNOCOR"].astype(str).str.strip()

    # Filtro: residente no RJ OU óbito ocorrido no RJ
    filtro_rj = (
        chunk["CODMUNRES"].str.startswith("33", na=False) |
        chunk["CODMUNOCOR"].str.startswith("33", na=False)
    )

    chunk_rj = chunk[filtro_rj]

    if not chunk_rj.empty:
        chunk_rj.to_csv(
            arquivo_saida,
            sep=";",
            index=False,
            mode="w" if primeiro_chunk else "a",
            header=primeiro_chunk,
            encoding="utf-8-sig"
        )

        total_linhas += len(chunk_rj)
        primeiro_chunk = False

print(f"Arquivo salvo em: {arquivo_saida}")
print(f"Total de linhas no novo arquivo: {total_linhas}")