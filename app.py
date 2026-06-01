import streamlit as st
import pandas as pd
import joblib
from scripts.features import engenharia_de_features

# Carrega modelo e encoder
modelo = joblib.load("modelo_risco.joblib")
le = joblib.load("label_encoder.joblib")

st.title("Previsão de Risco de Óbito por Condições Climáticas")

# Entradas do usuário
idade = st.slider("Idade", 0, 120, 30)
data = st.date_input("Data da medição")
temperatura = st.number_input("Temperatura (°C)", value=25.0)
umidade = st.number_input("Umidade (%)", value=70.0)
regiao = st.text_input("Região (nome padronizado)", value="belo horizonte")

# Monta DataFrame com os dados do usuário
df = pd.DataFrame([{
    'nu_idade': idade,
    'data': data,
    'TEMPERATURA MEDIA, DIARIA (AUT)(Â°C)': temperatura,
    'UMIDADE RELATIVA DO AR, MEDIA DIARIA (AUT)(%)': umidade,
    'Região': regiao
}])

# Aplica features
df_proc = engenharia_de_features(df)

# Faz predição
X = df_proc[['TEMPERATURA_MEDIA', 'UMIDADE_MEDIA', 'faixa_etaria', 'clima_extremo', 'estacao_ano', 'regiao']]
for col in X.columns:
    X[col] = X[col].astype(str)
    X[col] = le[col].transform(X[col])

pred = modelo.predict(X)
st.success(f"Risco previsto: {le['risco_obito'].inverse_transform(pred)[0]}")
