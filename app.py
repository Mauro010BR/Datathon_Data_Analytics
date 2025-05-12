import streamlit as st
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
import pickle
import gzip

@st.cache_data
def carregar_dados():
    with gzip.open("df_vagas\df_final_vagas_part1.pkl.gz", "rb") as f:
        df_vagas_part1 = pickle.load(f)
    with gzip.open("df_vagas\df_final_vagas_part2.pkl.gz", "rb") as f:
        df_vagas_part2 = pickle.load(f)
    df_vagas = pd.concat([df_vagas_part1, df_vagas_part2], ignore_index=True)

    with gzip.open("df_applicants\df_final_candidatos_part1.pkl.gz", "rb") as f:
        df_candidatos_part1 = pickle.load(f)
    with gzip.open("df_applicants\df_final_candidatos_part2.pkl.gz", "rb") as f:
        df_candidatos_part2 = pickle.load(f)
    df_candidatos = pd.concat([df_candidatos_part1, df_candidatos_part2], ignore_index=True)

    with open("df_applicants\df_applicants.pkl", "rb") as f:
        df_applicants = pickle.load(f)
    with open("df_vagas\df_vagas.pkl", "rb") as f:  # Adicionando o df_vagas
        df_vagas_additional = pickle.load(f)
    return df_vagas, df_candidatos, df_applicants, df_vagas_additional

def recomendar_candidatos_cosine(codigo_vaga_input, df_candidatos_final, df_vagas_final, df_applicants, top_n=5):
   
    vaga_embed = df_vagas_final[df_vagas_final['codigo_vaga'] == codigo_vaga_input]
    if vaga_embed.empty:
        return pd.DataFrame()

    embedding_cols_vaga = [col for col in df_vagas_final.columns if 'embedding' in col]
    embedding_cols_candidatos = [col for col in df_candidatos_final.columns if 'embedding' in col]

    vaga_vector = vaga_embed[embedding_cols_vaga].values
    candidatos_vectors = df_candidatos_final[embedding_cols_candidatos].values

    sim_scores = cosine_similarity(candidatos_vectors, vaga_vector).flatten()
    df_candidatos_final['score_cosine'] = sim_scores
    df_candidatos_final['score_cosine_percentual'] = (df_candidatos_final['score_cosine'] * 100).round(2).astype(str) + '%'

    df_applicants['codigo_profissional'] = df_applicants['codigo_profissional'].astype(int)

    candidatos_com_info = df_candidatos_final.merge(
        df_applicants[['codigo_profissional', 'objetivo_profissional']], 
        on='codigo_profissional', 
        how='left'
    )

    candidatos_com_info.rename(columns={'score_cosine_percentual': 'compatibilidade'}, inplace=True)

    return candidatos_com_info.sort_values('score_cosine', ascending=False).head(top_n)[
        ['codigo_profissional','objetivo_profissional','compatibilidade','quantidade_prospect']
    ]

st.set_page_config(page_title="Recrutamento Inteligente", page_icon="🔍", layout="wide")
st.markdown("""
    <style>
        .css-1v3fvcr {
            background-color: #4CAF50;
        }
        .css-ffhzg2 {
            color: white;
        }
        .css-1u5mt4t {
            color: #4CAF50;
        }
        .streamlit-expanderHeader {
            font-size: 20px;
        }
        .streamlit-expanderContent {
            color: #4CAF50;
        }
        .css-1kc6g0f {
            padding-top: 0px;
        }
        .stButton > button {
            background-color: #4CAF50;
            color: white;
        }
        .stButton > button:hover {
            background-color: #45a049;
        }
        .image-container {
            position: absolute;
            top: 0;
            left: 0;
        }    
    </style>
""", unsafe_allow_html=True)

col1, col2 = st.columns([1, 6])  

with col1:
    st.image("images/logo_decision.jpg", width=200)

with col2:
    st.markdown("<div style='margin-top: 20px;'></div>", unsafe_allow_html=True)  # Move o texto para baixo
    st.title("🔍 Recrutador Inteligente")
    st.markdown("""
        Bem-vindo, **Tech Hunters**! 🚀  
        Utilize nossa ferramenta inteligente de similaridade para encontrar rapidamente o **candidato ideal** para a vaga que você está buscando.  
        Combinamos a tecnologia de ponta com a análise de dados para ajudá-lo a fazer o melhor match entre **candidatos e vagas**, otimizando seu processo de recrutamento.
    """)

df_vagas, df_candidatos, df_applicants, df_vagas_additional = carregar_dados()

st.subheader("📋 Tabela de Vagas")

search_term = st.text_input("🔎 Pesquise nas vagas:", "", key="search_vagas")

if search_term:
    df_vagas_filtered = df_vagas_additional[df_vagas_additional.apply(lambda row: row.astype(str).str.contains(search_term, case=False).any(), axis=1)]
else:
    df_vagas_filtered = df_vagas_additional

df_vagas_filtered['codigo_vaga'] = df_vagas_filtered['codigo_vaga'].astype(str)
st.dataframe(df_vagas_filtered)

codigo_vagas = df_vagas['codigo_vaga'].unique()
codigo_vaga_input = st.selectbox("💼 Selecione o código da vaga:", codigo_vagas)

top_n = st.slider("👥 Quantos candidatos deseja ver?", min_value=1, max_value=20, value=5)

if st.button("🔍 Recomendar Candidatos"):
    resultado = recomendar_candidatos_cosine(codigo_vaga_input, df_candidatos.copy(), df_vagas, df_applicants, top_n)
    if resultado.empty:
        st.warning("⚠️ Nenhum candidato encontrado para esta vaga.")
    else:
        st.success("Candidatos recomendados com sucesso! 🎯")
        resultado['codigo_profissional'] = resultado['codigo_profissional'].astype(str)
        st.dataframe(resultado)