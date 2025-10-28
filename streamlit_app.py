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
    st.sidebar.markdown(f"**Atividade programada:** {atividade}")
    st.sidebar.markdown(f"**Suplementação prevista:** {suplementacao}")
else:
    atividade = st.sidebar.selectbox("Selecione a atividade", ATIVIDADES)
    suplementacao = st.sidebar.text_input("Suplementação")

peso = st.sidebar.number_input("Peso (kg)", min_value=20.0, max_value=200.0, value=92.7)
concluido = st.sidebar.checkbox("Treino concluído (ticado)")
suplementos_tomados = st.sidebar.multiselect(
    "Quais suplementos você tomou hoje?",
    ["Cardarine", "MK-677", "Lipo-6", "Whey", "Creatina", "ZMA", "Ômega 3", "Multivitamínico", "Recuperação"]
)
obs = st.sidebar.text_area("Observações", max_chars=200)

if st.sidebar.button("Salvar registro do dia"):
    new_row = {
        "Data": input_date.strftime("%d/%m/%Y"),
        "Peso (kg)": peso,
        "Atividade": atividade,
        "Suplementação": suplementacao,
        "Concluído": concluido,
        "Suplementos Tomados": ", ".join(suplementos_tomados),
        "Observação": obs,
    }
    st.session_state['registro'] = pd.concat([
        st.session_state['registro'],
        pd.DataFrame([new_row])
    ], ignore_index=True)
    st.sidebar.success("Registro salvo!")

# Visualização dos registros e gráficos
st.header("Progresso registrado")
reg_df = st.session_state['registro']

if not reg_df.empty:
    st.dataframe(reg_df)
    st.subheader("Evolução Peso x Meta")
    reg_df_merged = pd.merge(reg_df, plano_df[["Data", "Meta Peso (kg)"]], on="Data", how="left")
    fig, ax = plt.subplots(figsize=(10, 4))
    ax.plot(reg_df_merged["Data"], reg_df_merged["Peso (kg)"], label="Peso real", marker="o", color='blue')
    ax.plot(reg_df_merged["Data"], reg_df_merged["Meta Peso (kg)"], label="Meta semanal", linestyle="--", color='orange')
    ax.set_xticklabels(reg_df_merged["Data"], rotation=45)
    ax.set_ylabel("Peso (kg)")
    ax.legend()
    st.pyplot(fig)

# Exportação simples em PDF do ciclo
def generate_pdf(df):
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    c.drawString(60, 800, "Projeto 8 Semanas – Sprint Triathlon Evolution (Resumo)")
    c.drawString(60, 780, "Progresso dos treinos, suplementação e metas semanais:")
    y = 755
    for idx, row in df.tail(20).iterrows():
        status = "✔️" if row["Concluído"] else "❌"
        out = f"{row['Data']} | {row['Atividade']} | Sup.: {row['Suplementação']} | Peso: {row['Peso (kg)']}kg | {status} | {row['Suplementos Tomados']} | {row['Observação']}"
        c.drawString(50, y, out)
        y -= 14
        if y < 100:
            c.showPage()
            y = 800
    c.save()
    buffer.seek(0)
    return buffer

st.subheader("Exportação de Relatório (PDF)")
if st.button("Gerar PDF"):
    pdf = generate_pdf(reg_df)
    st.download_button(
        label="Download do relatório PDF",
        data=pdf,
        file_name="Projeto_8_Semanas_Sprint_Triathlon_Evolution.pdf",
        mime="application/pdf"
    )

st.caption("Treino e suplementação integrados - tique, metas, observação, exportação PDF.")
