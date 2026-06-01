import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv('arquivos/dados_A701_D_2010-01-01_2023-12-31.csv', sep=';', skiprows=9, decimal=',')

df['Data Medicao'] = pd.to_datetime(df['Data Medicao'])

df['Ano'] = df['Data Medicao'].dt.year
df['Mes'] = df['Data Medicao'].dt.month

df = df.rename(columns={
    'TEMPERATURA MEDIA, DIARIA (AUT)(°C)': 'Temperatura',
    'UMIDADE RELATIVA DO AR, MEDIA DIARIA (AUT)(%)': 'Umidade'
})

plt.figure(figsize=(15, 5))
plt.subplot(1, 2, 1)
sns.violinplot(y=df['Temperatura'], inner='quartile')
plt.title('Distribuição de Temperatura (°C)')
plt.ylabel('Temperatura')

plt.subplot(1, 2, 2)
sns.violinplot(y=df['Umidade'], inner='quartile')
plt.title('Distribuição de Umidade Relativa (%)')
plt.ylabel('Umidade')
plt.tight_layout()
plt.show()

plt.figure(figsize=(15, 5))
plt.subplot(1, 2, 1)
sns.histplot(df['Temperatura'], kde=True, bins=30)
plt.title('Distribuição de Temperatura (°C)')

plt.subplot(1, 2, 2)
sns.histplot(df['Umidade'], kde=True, bins=30)
plt.title('Distribuição de Umidade Relativa (%)')
plt.tight_layout()
plt.show()

plt.figure(figsize=(15, 5))
sns.scatterplot(x='Temperatura', y='Umidade', data=df, alpha=0.6)
plt.title('Relação entre Temperatura e Umidade')
plt.show()

df_mensal = df.groupby(['Ano', 'Mes']).agg({
    'Temperatura': 'mean',
    'Umidade': 'mean'
}).reset_index()

df_mensal['Data'] = pd.to_datetime(df_mensal['Ano'].astype(str) + pd.to_timedelta(df_mensal['Mes'].sub(1).astype(str) + 'M'))

plt.figure(figsize=(15, 8))
plt.subplot(2, 1, 1)
sns.lineplot(x='Data', y='Temperatura', data=df_mensal)
plt.title('Temperatura Média Mensal')
plt.xticks(rotation=45)

plt.subplot(2, 1, 2)
sns.lineplot(x='Data', y='Umidade', data=df_mensal)
plt.title('Umidade Média Mensal')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

plt.figure(figsize=(15, 6))
plt.subplot(1, 2, 1)
sns.barplot(x='Mes', y='Temperatura', data=df, ci=None)
plt.title('Temperatura Média por Mês')
plt.xlabel('Mês')
plt.ylabel('Temperatura Média (°C)')

plt.subplot(1, 2, 2)
sns.barplot(x='Mes', y='Umidade', data=df, ci=None)
plt.title('Umidade Média por Mês')
plt.xlabel('Mês')
plt.ylabel('Umidade Média (%)')
plt.tight_layout()
plt.show()