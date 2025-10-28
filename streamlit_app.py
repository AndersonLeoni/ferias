import streamlit as st
import pandas as pd
import datetime
import matplotlib.pyplot as plt
from io import BytesIO
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

st.set_page_config(page_title="Projeto 8 Semanas – Sprint Triathlon Evolution", layout="wide")
st.title("Projeto 8 Semanas – Sprint Triathlon Evolution")

# Estrutura do ciclo semanal e rotina de suplementos
DIAS = [
    "Segunda", "Terça", "Quarta", "Quinta", "Sexta", "Sábado", "Domingo"
]
ATIVIDADES = [
    "Ciclismo Progressivo",
    "Corrida Garmin Coach",
    "Natação Técnica",
    "Corrida Garmin Coach",
    "Força + Core",
    "Corrida Garmin Coach",
    "Recuperação Ativa"
]
SUPLEMENTOS = [
    ["Cardarine", "MK-677", "Lipo-6", "Whey", "Creatina"],
    ["Cardarine", "MK-677", "Whey", "Creatina"],
    ["Cardarine", "MK-677", "Whey", "Multivitamínico"],
    ["Cardarine", "MK-677", "Whey", "Creatina"],
    ["Cardarine", "MK-677", "ZMA", "Whey", "Creatina"],
    ["Cardarine", "MK-677", "Whey", "Creatina"],
    ["Ômega 3", "Multivitamínico", "Recuperação"]
]

data_inicio = datetime.date(2025, 11, 2)
semanas = 8

# Gera estrutura do plano semanal
dias_do_ciclo = []
for semana in range(semanas):
    for i, dia_semana in enumerate(DIAS):
        dia = data_inicio + datetime.timedelta(days=semana*7 + i)
        atividade = ATIVIDADES[i]
        meta = max(92.7 - ((semana+1)*1.6), 80)
        suplementos = ", ".join(SUPLEMENTOS[i])
        dias_do_ciclo.append({
            "Data": dia.strftime("%d/%m/%Y"),
            "Semana": semana+1,
            "Dia": dia_semana,
            "Atividade": atividade,
            "Suplementação": suplementos,
            "Meta Peso (kg)": round(meta, 1)
        })
plano_df = pd.DataFrame(dias_do_ciclo)

# Inicializa DataFrame de registro do usuário
if 'registro' not in st.session_state or st.session_state['registro'] is None:
    st.session_state['registro'] = pd.DataFrame(columns=[
        "Data", "Peso (kg)", "Atividade", "Suplementação", "Concluído", "Suplementos Tomados", "Observação"
    ])

# Visualização do plano semanal
st.subheader("Plano semanal do ciclo")
st.dataframe(plano_df)

st.sidebar.header("Registro Diário")
input_date = st.sidebar.date_input("Data")
atividade_info = plano_df[plano_df['Data'] == input_date.strftime("%d/%m/%Y")]

if not atividade_info.empty:
    atividade = atividade_info.iloc[0]['Atividade']
    suplementacao = atividade_info.iloc[0]['Suplementação']
    st.sidebar.markdown(f"
