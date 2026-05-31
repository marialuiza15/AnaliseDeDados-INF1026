import os
import pandas as pd

DATASET = "utkarshxy/who-worldhealth-statistics-2020-complete"
DOWNLOAD_DIR = "./who_dataset"

os.makedirs(DOWNLOAD_DIR, exist_ok=True)

# Baixa o dataset via CLI do kaggle
os.system(f"kaggle datasets download -d {DATASET} -p {DOWNLOAD_DIR} --unzip")

# ─── Leitura dos arquivos ─────────────────────────────────────────────────────
print("Carregando bases de dados...")

df_transito    = pd.read_csv(os.path.join(DOWNLOAD_DIR, "roadTrafficDeaths.csv"))
df_mortalidade = pd.read_csv(os.path.join(DOWNLOAD_DIR, "under5MortalityRate.csv"))

print("Bases carregadas com sucesso!\n")

# ─── Inspeção inicial ─────────────────────────────────────────────────────────
bases = {
    "TRÂNSITO — roadTrafficDeaths.csv":          df_transito,
    "MORTALIDADE <5 ANOS — under5MortalityRate": df_mortalidade,
}

for titulo, df in bases.items():
    print("=" * 60)
    print(titulo)
    print("=" * 60)
    print(f"Shape: {df.shape}")
    print(df.head())
    print(f"\nColunas: {df.columns.tolist()}\n")