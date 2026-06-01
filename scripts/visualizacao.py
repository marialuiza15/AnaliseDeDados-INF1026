import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import ConfusionMatrixDisplay

def plot_distribuicao_causas(df, titulo='Distribuição das causas de óbito'):
    plt.figure(figsize=(5, 2))  # Tamanho reduzido
    ordem = df['capitulo_cid_causa_basica'].value_counts().head(10).index
    sns.countplot(data=df, y='capitulo_cid_causa_basica', order=ordem, hue='capitulo_cid_causa_basica', palette='magma', legend=False)
    plt.title(titulo)
    plt.xlabel('Número de óbitos')
    plt.ylabel('Causa (Capítulo CID)')
    plt.tight_layout()
    plt.show()

def mostrar_matriz_confusao(modelo, X_test, y_test_enc, le_y):
    ConfusionMatrixDisplay.from_estimator(
        modelo, X_test, y_test_enc,
        display_labels=le_y.classes_,
        xticks_rotation='vertical',
        cmap='Blues',
        values_format='d'
    )
    plt.title('Matriz de Confusão - Previsão das Causas de Óbito')
    plt.show()

def plot_casos_por_mes(df):
    df['mes'] = pd.to_datetime(df['data']).dt.month
    plt.figure(figsize=(7, 2.5))  # Tamanho reduzido
    sns.countplot(data=df, x='mes', hue='capitulo_cid_causa_basica', palette='Set2')
    plt.title('Óbitos por mês e causa (top 4)')
    plt.xlabel('Mês')
    plt.ylabel('Número de óbitos')
    plt.legend(title='Causa')
    plt.tight_layout()
    plt.show()