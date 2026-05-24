import kagglehub
import pandas as pd
import os
 
DATASET = "utkarshxy/who-worldhealth-statistics-2020-complete"
 
# ─── Download do dataset completo para disco ──────────────────────────────────
print("Baixando dataset da WHO...")
path = kagglehub.dataset_download(DATASET)
print(f"Dataset salvo em: {path}\n")
 
# ─── Leitura direta com pandas ────────────────────────────────────────────────
print("Carregando bases de dados...")
 
df_transito     = pd.read_csv(os.path.join(path, "roadTrafficDeaths.csv"))
df_saude        = pd.read_csv(os.path.join(path, "uhcCoverage.csv"))
df_expectativa  = pd.read_csv(os.path.join(path, "lifeExpectancyAtBirth.csv"))
df_medicos      = pd.read_csv(os.path.join(path, "medicalDoctors.csv"))
df_mortalidade  = pd.read_csv(os.path.join(path, "mortalityRatePoisoning.csv"))
 
print("Bases carregadas com sucesso!\n")
 
# ─── Inspeção inicial ─────────────────────────────────────────────────────────
bases = {
    "TRÂNSITO — roadTrafficDeaths.csv":           df_transito,
    "COBERTURA DE SAÚDE — uhcCoverage.csv":       df_saude,
    "EXPECTATIVA DE VIDA — lifeExpectancyAtBirth": df_expectativa,
    "MÉDICOS — medicalDoctors.csv":               df_medicos,
    "MORTALIDADE/ENVENENAMENTO — mortalityRatePoisoning": df_mortalidade,
}
 
for titulo, df in bases.items():
    print("=" * 60)
    print(titulo)
    print("=" * 60)
    print(f"Shape: {df.shape}")
    print(df.head())
    print(f"\nColunas: {df.columns.tolist()}\n")
 