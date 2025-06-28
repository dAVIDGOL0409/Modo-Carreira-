import streamlit as st
import json
import random

st.set_page_config(page_title="Assistente de Modo Carreira", layout="wide")
st.title("⚽ IA do Modo Carreira FIFA")

# Sessões importantes
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "titulares" not in st.session_state:
    st.session_state.titulares = []
if "reservas" not in st.session_state:
    st.session_state.reservas = []

# Função para notícia aleatória
def gerar_noticia_aleatoria(ano, time):
    noticias = [
        f"{ano}: Escândalo no VAR gera polêmica após jogo entre {time} e rival direto.",
        f"{ano}: Estádio do {time} será ampliado para comportar mais 20 mil torcedores.",
        f"{ano}: Jovem da base do {time} ganha prêmio de revelação do campeonato.",
        f"{ano}: Treinador do {time} é eleito técnico do mês pela terceira vez consecutiva.",
        f"{ano}: {time} sofre com surto de lesões e tem que improvisar goleiro na zaga.",
        f"{ano}: Federação anuncia mudanças no calendário e revolta clubes da liga.",
        f"{ano}: Árbitro suspenso após atuação polêmica em partida do {time}.",
        f"{ano}: Nova regra de impedimento é testada em partida oficial e gera confusão.",
        f"{ano}: Inteligência artificial passa a analisar desempenho tático em tempo real.",
        f"{ano}: Crise financeira atinge clube tradicional e preocupa torcida.",
        f"{ano}: Torcida do {time} organiza mosaico histórico no clássico local.",
        f"{ano}: Relatório aponta {time} como clube que mais evoluiu fisicamente na temporada.",
        f"{ano}: Ídolo do {time} anuncia aposentadoria e recebe homenagens no estádio.",
        f"{ano}: FIFA anuncia nova premiação para jogada mais bonita da temporada.",
        f"{ano}: Jogo do {time} é interrompido por invasão de drone em campo."
    ]
    return random.choice(noticias)

# Dados da carreira
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

# Plataforma
platform = st.radio("Qual sua plataforma?", ["PC", "Console"])

# PC: Upload
if platform == "PC":
    st.subheader("📄 Upload da Carreira")
    uploaded_file = st.file_uploader("Envie o arquivo (.csv ou .json)", type=["csv", "json"])
    if uploaded_file:
        file_type = uploaded_file.name.split(".")[-1]
        import pandas as pd
        if file_type == "json":
            carreira_data = json.load(uploaded_file)
        elif file_type == "csv":
            df = pd.read_csv(uploaded_file)
            for _, row in df.iterrows():
                carreira_data["jogadores"].append({
                    "nome": row["nome"],
                    "idade": row["idade"],
                    "overall": row["overall"],
                    "potencial": row["potencial"],
                    "posição": row["posição"],
                    "moral": row["moral"],
                    "tempo_de_jogo": row["tempo_de_jogo"],
                    "foto": row.get("foto", "")  # Campo opcional
                })

        carreira_data["time"] = st.text_input("Qual seu time?", "Time Padrão")
        carreira_data["temporada"] = st.text_input("Temporada atual", "2028-2029")
        carreira_data["verba"] = st.number_input("Verba disponível (milhões)", value=50000000)

# Console: Manual
else:
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
        foto = st.text_input("URL da foto do jogador (opcional)")
        if st.button("Adicionar jogador"):
            carreira_data["jogadores"].append({
                "nome": nome,
                "idade": idade,
                "overall": overall,
                "potencial": potencial,
                "posição": posicao,
                "moral": moral,
                "tempo_de_jogo": tempo_jogo,
                "foto": foto
            })
            st.success("Jogador adicionado!")

# Exibir jogadores com fotos
st.markdown("---")
st.subheader("📸 Elenco Atual com Fotos")
for jogador in carreira_data["jogadores"]:
    col1, col2 = st.columns([1, 4])
    with col1:
        if jogador.get("foto"):
            st.image(jogador["foto"], width=60)
    with col2:
        st.markdown(f"**{jogador['nome']}** | {jogador['posição']} | Overall: {jogador['overall']} | Moral: {jogador['moral']}")

# Aba de contratação e controle financeiro
st.markdown("---")
st.subheader("💰 Contratação de Jogadores")
with st.expander("Simular contratação"):
    jogador_nome = st.text_input("Nome do jogador a contratar")
    valor = st.number_input("Valor da contratação (milhões)", 0)
    if st.button("Contratar jogador"):
        if valor <= carreira_data["verba"]:
            carreira_data["verba"] -= valor
            st.success(f"{jogador_nome} contratado por {valor} milhões!")
        else:
            st.error("Verba insuficiente para essa contratação.")
st.info(f"💼 Verba restante: R$ {carreira_data['verba']:,} milhões")

# Escalação titular e reservas
st.markdown("---")
st.subheader("📋 Escalação Titular e Reservas")
titulares = st.multiselect("Escolha os titulares", [j["nome"] for j in carreira_data["jogadores"]])
reservas = [j["nome"] for j in carreira_data["jogadores"] if j["nome"] not in titulares]
st.session_state.titulares = titulares
st.session_state.reservas = reservas

col1, col2 = st.columns(2)
with col1:
    st.markdown("### 🟢 Titulares")
    for t in titulares:
        st.markdown(f"- {t}")
with col2:
    st.markdown("### 🟡 Reservas")
    for r in reservas:
        st.markdown(f"- {r}")

# Notícia Aleatória
st.markdown("---")
st.subheader("📰 Notícia Aleatória da Temporada")
ano_atual = carreira_data["temporada"].split("-")[0] if carreira_data["temporada"] else "2028"
if carreira_data["time"]:
    st.info(gerar_noticia_aleatoria(ano_atual, carreira_data["time"]))

# Chatbot funcional
st.markdown("---")
st.subheader("💬 Assistente de Carreira (Chatbot)")
user_input = st.text_input("Pergunte algo para o assistente:")

prompt_base = f"""
Você é um assistente técnico no modo carreira do FIFA. 
Responda com base nesses dados:

DADOS DA CARREIRA:
{json.dumps(carreira_data, indent=2)}

TITULARES: {st.session_state.titulares}
RESERVAS: {st.session_state.reservas}

Pergunta: {user_input}
"""

if user_input:
    import openai
    openai.api_key = "SUA_API_KEY_AQUI"

    response = openai.ChatCompletion.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "Você é um assistente técnico no modo carreira do FIFA."},
            {"role": "user", "content": prompt_base}
        ],
        temperature=0.7,
    )

    resposta = response["choices"][0]["message"]["content"]
    st.session_state.chat_history.append(("Você", user_input))
    st.session_state.chat_history.append(("IA", resposta))

for remetente, mensagem in st.session_state.chat_history:
    st.markdown(f"**{remetente}:** {mensagem}")
