import streamlit as st
import json

st.set_page_config(page_title="Assistente de Modo Carreira", layout="centered")
st.title("⚽ IA do Modo Carreira FIFA")

platform = st.radio("Qual sua plataforma?", ["PC", "Console"])

carreira_data = {
    "time": "",
    "temporada": "",
    "verba": 0,
    "jogadores": [],
    "tabela": {
        "posição_atual": 0,
        "gols_marcados": 0,
        "gols_sofridos": 0,
        "partidas": 0,
        "últimos_resultados": []
    }
}

if platform == "PC":
    st.subheader("📤 Upload da Carreira")
    uploaded_file = st.file_uploader("Envie o arquivo convertido (.csv ou .json)", type=["csv", "json"])

    if uploaded_file:
        file_type = uploaded_file.name.split(".")[-1]

        if file_type == "json":
            carreira_data = json.load(uploaded_file)
        elif file_type == "csv":
            import pandas as pd
            df = pd.read_csv(uploaded_file)
            for _, row in df.iterrows():
                carreira_data["jogadores"].append({
                    "nome": row["nome"],
                    "idade": row["idade"],
                    "overall": row["overall"],
                    "potencial": row["potencial"],
                    "posição": row["posição"],
                    "moral": row["moral"],
                    "tempo_de_jogo": row["tempo_de_jogo"]
                })

        carreira_data["time"] = st.text_input("Qual seu time?", "Time Padrão")
        carreira_data["temporada"] = st.text_input("Temporada atual", "2028-2029")
        carreira_data["verba"] = st.number_input("Verba disponível (milhões)", value=50000000)

elif platform == "Console":
    st.subheader("📝 Preencha os dados abaixo")
    carreira_data["time"] = st.text_input("Qual seu time?")
    carreira_data["temporada"] = st.text_input("Temporada atual", "2028-2029")
    carreira_data["verba"] = st.number_input("Verba disponível (milhões)", value=30000000)

    st.markdown("### Situação da Tabela")
    carreira_data["tabela"]["posição_atual"] = st.slider("Posição na tabela", 1, 20)
    carreira_data["tabela"]["gols_marcados"] = st.number_input("Gols marcados", 0)
    carreira_data["tabela"]["gols_sofridos"] = st.number_input("Gols sofridos", 0)
    carreira_data["tabela"]["partidas"] = st.number_input("Partidas jogadas", 0)
    ultimos = st.text_input("Últimos 5 jogos (ex: V,E,D,D,V)").upper()
    carreira_data["tabela"]["últimos_resultados"] = ultimos.split(",") if ultimos else []

    st.markdown("### Adicione Jogadores (manual)")
    with st.expander("Adicionar jogador ao elenco"):
        nome = st.text_input("Nome do jogador")
        idade = st.number_input("Idade", 15, 45)
        overall = st.number_input("Overall", 50, 99)
        potencial = st.number_input("Potencial", 50, 99)
        posicao = st.selectbox("Posição", ["GK", "CB", "LB", "RB", "CM", "LM", "RM", "ST", "CAM", "CDM"])
        moral = st.selectbox("Moral", ["baixa", "média", "alta"])
        tempo_jogo = st.selectbox("Tempo de jogo", ["baixo", "médio", "alto", "muito alto"])

        if st.button("Adicionar jogador"):
            carreira_data["jogadores"].append({
                "nome": nome,
                "idade": idade,
                "overall": overall,
                "potencial": potencial,
                "posição": posicao,
                "moral": moral,
                "tempo_de_jogo": tempo_jogo
            })
            st.success("Jogador adicionado!")

st.markdown("---")
st.subheader("💬 Assistente de Carreira (Chatbot)")

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

user_input = st.text_input("Pergunte algo para o assistente:")

prompt_base = f"""Você é um assistente técnico virtual no modo carreira do FIFA. 
Baseado nos dados a seguir, responda como se fosse um treinador experiente:

DADOS DA CARREIRA:
{json.dumps(carreira_data, indent=2)}

Usuário perguntou: {user_input}
"""

if user_input:
    with st.spinner("Pensando..."):
        import openai
        openai.api_key = "SUA_API_KEY_AQUI"

        response = openai.ChatCompletion.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "Você é um assistente técnico de futebol no modo carreira do FIFA."},
                {"role": "user", "content": prompt_base}
            ],
            temperature=0.7,
        )

        resposta = response["choices"][0]["message"]["content"]
        st.session_state.chat_history.append(("Você", user_input))
        st.session_state.chat_history.append(("IA", resposta))

for remetente, mensagem in st.session_state.chat_history:
    st.markdown(f"**{remetente}:** {mensagem}")
