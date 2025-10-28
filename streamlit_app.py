import streamlit as st
import pandas as pd
import datetime
import matplotlib.pyplot as plt
from io import BytesIO
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

st.set_page_config(page_title="Projeto 8 Semanas – Sprint Triathlon Evolution", layout="wide")
st.title("Projeto 8 Semanas – Sprint Triathlon Evolution")

# Dados locais
if "df" not in st.session_state:
    st.session_state.df = pd.DataFrame(columns=[
        "Data", "Peso (kg)", "Treino Concluído", "Energia", "Sono", "Notas"
    ])

# Painel lateral - registro diário
st.sidebar.header("Registro Diário")
today = datetime.date.today()
input_date = st.sidebar.date_input("Data", value=today, max_value=today)
peso = st.sidebar.number_input("Peso (kg)", min_value=20.0, max_value=200.0, value=92.7, step=0.1)
treino_ok = st.sidebar.checkbox("Treino concluído")
energia = st.sidebar.slider("Energia (0-10)", 0, 10, 7)
sono = st.sidebar.slider("Sono (horas)", 0, 12, 7)
notas = st.sidebar.text_area("Notas", max_chars=200)

if st.sidebar.button("Salvar registro"):
    new_row = {
        "Data": input_date.strftime("%Y-%m-%d"),
        "Peso (kg)": peso,
        "Treino Concluído": treino_ok,
        "Energia": energia,
        "Sono": sono,
        "Notas": notas,
    }
    st.session_state.df = st.session_state.df.append(new_row, ignore_index=True)
    st.sidebar.success("Registro salvo!")

# Visualização principal
st.header("Resumo Semanal")
df = st.session_state.df
if df.empty:
    st.info("Nenhum dado registrado.")
else:
    df["Data"] = pd.to_datetime(df["Data"])
    df = df.sort_values(by="Data")
    df.set_index("Data", inplace=True)
    st.dataframe(df)

    st.subheader("Progresso de Peso")
    fig, ax = plt.subplots(figsize=(10, 4))
    ax.plot(df.index, df["Peso (kg)"], marker='o', color='blue')
    ax.set_xlabel("Data")
    ax.set_ylabel("Peso (kg)")
    st.pyplot(fig)

# Gerador de PDF do progresso
def generate_pdf():
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    c.drawString(80, 800, "Projeto 8 Semanas – Sprint Triathlon Evolution (Resumo)")
    c.drawString(80, 780, f"Peso inicial: 92,7 kg | Meta: 80 kg | Data início: 02/11/25")
    c.drawString(80, 765, "Progresso registrado:")
    y = 750
    for idx, row in df.tail(15).iterrows():
        out = f"{idx.date()} | Peso: {row['Peso (kg)']}kg | Energia: {row['Energia']} | Sono: {row['Sono']}h"
        c.drawString(80, y, out)
        y -= 14
        if y < 100:
            c.showPage()
            y = 800
    c.save()
    buffer.seek(0)
    return buffer

st.subheader("Exportação de Relatório (PDF)")
if st.button("Gerar PDF"):
    pdf = generate_pdf()
    st.download_button(
        label="Download do relatório PDF",
        data=pdf,
        file_name="Projeto_8_Semanas_Sprint_Triathlon_Evolution.pdf",
        mime="application/pdf"
    )

st.caption("App local - sem Google - sincronização somente na sessão Streamlit")
