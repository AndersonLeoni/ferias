import streamlit as st
import pandas as pd
import datetime
from google.oauth2 import service_account
import gspread
from gspread_dataframe import set_with_dataframe
import matplotlib.pyplot as plt
from io import BytesIO

import json
import os
from google.oauth2 import service_account
key_dict = json.loads(os.environ["GOOGLE_CREDENTIALS"])
creds = service_account.Credentials.from_service_account_info(key_dict)


# Configurações do App
st.set_page_config(page_title="Projeto 8 Semanas – Sprint Triathlon Evolution", layout="wide")
st.title("Projeto 8 Semanas – Sprint Triathlon Evolution")
st.markdown("""<style>
    .block-container {padding: 1rem 2rem;}
    </style>""", unsafe_allow_html=True)

# Google Sheets Configurações
SCOPES = ["https://www.googleapis.com/auth/spreadsheets",
          "https://www.googleapis.com/auth/drive"]

@st.cache_resource(ttl=3600)
def get_gsheet_client():
    creds = None
    try:
        creds = Credentials.from_service_account_info(
            st.secrets["gcp_service_account"], scopes=SCOPES)
    except Exception as e:
        st.error(f"Erro ao carregar credenciais Google: {e}")
        st.stop()
    return gspread.authorize(creds)

@st.cache_data(ttl=300)
def create_or_open_spreadsheet(client):
    try:
        sh_title = "8Semanas-TriSprint-Evolution"
        try:
            sh = client.open(sh_title)
        except gspread.exceptions.SpreadsheetNotFound:
            sh = client.create(sh_title)
            # Compartilhar com email do usuário para edição se necessário
            sh.share(st.secrets["user_email"], perm_type='user', role='writer')
        return sh
    except Exception as e:
        st.error(f"Erro abrir/criar planilha Google: {e}")
        st.stop()

# Início integração Google Sheets
client = get_gsheet_client()
spreadsheet = create_or_open_spreadsheet(client)

# Função para carregar dados ou criar abas iniciais
def load_data():
    try:
        worksheet = spreadsheet.worksheet("Registros")
        df = pd.DataFrame(worksheet.get_all_records())
        return df
    except gspread.exceptions.WorksheetNotFound:
        worksheet = spreadsheet.add_worksheet(title="Registros", rows="1000", cols="20")
        df = pd.DataFrame(columns=["Data", "Peso (kg)", "Peso / Weight (kg)", "Treino Concluído", "Workout Completed", "Energia", "Energy", "Sono", "Sleep", "Notas", "Notes"])
        set_with_dataframe(worksheet, df)
        return df

def save_data(df):
    worksheet = spreadsheet.worksheet("Registros")
    worksheet.clear()
    set_with_dataframe(worksheet, df)

# Carrega os dados para o app
df = load_data()

# Painel lateral - input de dados diário
st.sidebar.header("Registro Diário / Daily Log")
today = datetime.date.today()

col1, col2 = st.sidebar.columns(2)
input_date = col1.date_input("Data / Date", value=today, max_value=today)
peso_pt = col2.number_input("Peso (kg)", min_value=20.0, max_value=200.0, value=92.7, step=0.1)

col3, col4 = st.sidebar.columns(2)
treino_concluido = col3.checkbox("Treino concluído / Workout Completed")
energia = col4.slider("Energia / Energy (0-10)", 0, 10, 7)

col5, col6 = st.sidebar.columns(2)
sono = col5.slider("Sono / Sleep (hours)", 0, 12, 7)
notas = col6.text_area("Notas / Notes", max_chars=200)

if st.sidebar.button("Salvar registro / Save log"):
    new_row = {"Data": input_date.strftime("%Y-%m-%d"),
               "Peso (kg)": peso_pt,
               "Peso / Weight (kg)": peso_pt,
               "Treino Concluído": treino_concluido,
               "Workout Completed": treino_concluido,
               "Energia": energia,
               "Energy": energia,
               "Sono": sono,
               "Sleep": sono,
               "Notas": notas,
               "Notes": notas}
    df = df.append(new_row, ignore_index=True)
    save_data(df)
    st.sidebar.success("Registro salvo! / Log saved!")

# Seção principal - visualização e análise
st.header("Resumo Semanal / Weekly Summary")

if df.empty:
    st.info("Nenhum dado registrado. / No data logged yet.")
else:
    df["Data"] = pd.to_datetime(df["Data"])
    df = df.sort_values(by="Data")
    df.set_index("Data", inplace=True)

    # Mostrar tabela bilíngue lado a lado
    col_pt, col_en = st.columns(2)

    with col_pt:
        st.subheader("Dados em Português")
        st.dataframe(df[["Peso (kg)", "Treino Concluído", "Energia", "Sono", "Notas"]].rename(columns={
            "Peso (kg)": "Peso (kg)",
            "Treino Concluído": "Treino Concluído",
            "Energia": "Energia",
            "Sono": "Sono",
            "Notas": "Notas"
        }))

    with col_en:
        st.subheader("[translate:Data in English]")
        st.dataframe(df[["Peso / Weight (kg)", "Workout Completed", "Energy", "Sleep", "Notes"]].rename(columns={
            "Peso / Weight (kg)": "Weight (kg)",
            "Workout Completed": "Workout Completed",
            "Energy": "Energy",
            "Sleep": "Sleep",
            "Notes": "Notes"
        }))

    # Gráfico de progresso de peso e treino
    st.subheader("Progresso de Peso e Treinos / Weight & Workout Progress")
    fig, ax = plt.subplots(figsize=(12, 4))
    ax.plot(df.index, df["Peso (kg)"], label="Peso (kg)", color="blue")
    ax.plot(df.index, df["Peso / Weight (kg)"], label="Weight (kg)", color="green", linestyle="--")
    ax.set_xlabel("Data / Date")
    ax.set_ylabel("Peso / Weight (kg)")
    ax.legend()
    st.pyplot(fig)

    # Mais análises podem ser adicionadas aqui...

# Exportação PDF (exemplo simples)
import pdfkit
import os

if st.button("Exportar relatório PDF / Export PDF"):
    pdf_file = "Projeto_8Semanas_Sprint_Triathlon_Evolution.pdf"
    html_content = st.markdown("""
    <h1>Projeto 8 Semanas – Sprint Triathlon Evolution</h1>
    <p>Relatório gerado em: {}</p>
    <!-- Mais detalhes do relatório podem ser inclusos aqui -->
    """.format(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    options = {
        'page-size': 'A4',
        'encoding': "UTF-8",
    }
    pdfkit.from_string(html_content.get_value(), pdf_file, options=options)
    st.success(f"Relatório exportado: {pdf_file}")

