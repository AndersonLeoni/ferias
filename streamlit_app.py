import streamlit as st
import pandas as pd

# Dados do plano 30 dias simplificado
plan = {
    "Dia": list(range(1,31)),
    "Treino": [
        "Corrida leve 30min + Core 20min",
        "Natação técnica 45min + alongamento",
        "Ciclismo moderado 60min + força funcional 30min",
        "Corrida intervalada 4x400m + Core 20min",
        "Yoga + alongamentos 45min + mobilidade",
        "Natação endurance 60min",
        "Ciclismo leve 70min + força leve 20min",
        "Corrida moderada 40min + Core avançado 30min",
        "Natação técnica 50min + alongamento",
        "Ciclismo intervalado 70min + força funcional 40min",
        "Corrida intervalada 5x400m + Core 30min",
        "Yoga + mobilidade e alongamento 50min",
        "Natação endurance 65min",
        "Ciclismo leve 80min + força leve 30min",
        "Corrida intervalada 6x400m + Core 40min",
        "Natação técnica + séries de velocidade 50min",
        "Duas sessões de ciclismo (60min + 30min)",
        "Corrida longa moderada 90min",
        "Treino de força funcional 45min + Core 30min",
        "Natação endurance 70min",
        "Corrida leve 40min + força leve 30min",
        "Yoga + alongamento relaxante 60min",
        "Ciclismo intervalado 90min + força funcional 45min",
        "Natação técnica 70min + mobilidade",
        "Corrida intervalada 8x400m + Core 40min",
        "Pedalada longa 100min + força leve 40min",
        "Treino de recuperação ativa (yoga + alongamento) 50min",
        "Corrida leve 30min + Core 20min",
        "Ciclismo leve 70min + força funcional 30min",
        "Natação endurance 80min"
    ],
    "Meta peso (kg)": [87]*7 + [84.5]*7 + [82]*7 + [80]*9
}

df_plan = pd.DataFrame(plan)

st.title("Ciclo de 30 dias - Treino e Suplementação")

# Exibir plano
st.subheader("Plano diário de treino")
st.dataframe(df_plan)

# Entrada de peso diário
st.subheader("Registro diário de peso")
day_input = st.number_input("Digite o dia (1-30)", min_value=1, max_value=30, value=1)
weight_input = st.number_input("Peso atual (kg)", min_value=40.0, max_value=150.0, format="%.1f")

if "weights" not in st.session_state:
    st.session_state.weights = {}

if st.button("Salvar peso"):
    st.session_state.weights[day_input] = weight_input
    st.success(f"Peso do dia {day_input} salvo: {weight_input} kg")

# Mostrar registro de pesos
if st.session_state.weights:
    st.subheader("Progresso registrado")
    weights_df = pd.DataFrame(list(st.session_state.weights.items()), columns=["Dia", "Peso (kg)"])
    st.dataframe(weights_df)

    # Traçar gráfico simples
    st.line_chart(weights_df.set_index("Dia"))

st.write("Use este app para acompanhar seu treino, suplementação e peso para atingir a meta 80 kg.")
st.write("Mais funcionalidades poderão ser adicionadas conforme necessidade.")
