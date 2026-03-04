import streamlit as st
import pandas as pd
import warnings

warnings.simplefilter("ignore", UserWarning)

st.set_page_config(layout="wide")

# =========================
# FUNÇÃO PARA CARREGAMENTO
# =========================
@st.cache_data
def load_data():

    # ===== EVENTOS 2025 =====
    eventos_path = "classificacoes_eventos_computacao_2025.xlsx"
    eventos_df = pd.read_excel(
        eventos_path,
        engine="openpyxl"
    )

    # Normalizar nomes de colunas
    eventos_df.columns = eventos_df.columns.str.strip()

    # Garantir colunas esperadas
    if "Sigla" not in eventos_df.columns:
        eventos_df.rename(columns={eventos_df.columns[0]: "Sigla"}, inplace=True)

    if "Título" not in eventos_df.columns:
        eventos_df.rename(columns={eventos_df.columns[1]: "Título"}, inplace=True)

    if "Estrato" not in eventos_df.columns  :
        eventos_df.rename(columns={eventos_df.columns[-1]: "Estrato"}, inplace=True)


    # ===== PERIÓDICOS COMPUTAÇÃO 2026 =====
    periodicos_path = "classificacoes_publicadas_computacao_2026_1768259614570.xlsx"
    periodicos_df = pd.read_excel(periodicos_path)

    periodicos_df.columns = periodicos_df.columns.str.strip()

    return eventos_df, periodicos_df


# =========================
# LOAD
# =========================
try:
    eventos_df, periodicos_df = load_data()
except Exception as e:
    st.error(f"Erro ao carregar arquivos: {e}")
    st.stop()


# =========================
# INTERFACE
# =========================
st.title("Consulta Qualis CAPES – Computação 2025/2026")

tab1, tab2 = st.tabs(["Periódicos (2026)", "Eventos (2025)"])


# =========================
# PERIÓDICOS
# =========================
with tab1:

    st.header("Consulta de Periódicos - Computação 2026")

    search_term_periodicos = st.text_input(
        "Digite o termo de busca (Título ou ISSN):",
        key="periodicos"
    )

    if search_term_periodicos:

        search_results = periodicos_df[
            periodicos_df.astype(str)
            .apply(lambda row: row.str.contains(search_term_periodicos, case=False, na=False))
            .any(axis=1)
        ]

        st.write(f"Resultados encontrados: {len(search_results)}")
        st.dataframe(search_results, width='stretch')#use_container_width=True)

    else:
        st.write("Digite um termo para buscar periódicos.")
        st.dataframe(periodicos_df, width='stretch')#use_container_width=True)


# =========================
# EVENTOS
# =========================
with tab2:

    st.header("Consulta de Eventos - Computação 2025")

    search_term_eventos = st.text_input(
        "Digite o termo de busca (Título ou Sigla):",
        key="eventos"
    )

    if search_term_eventos:

        search_results = eventos_df[
            eventos_df.astype(str)
            .apply(lambda row: row.str.contains(search_term_eventos, case=False, na=False))
            .any(axis=1)
        ]

        st.write(f"Resultados encontrados: {len(search_results)}")
        st.dataframe(search_results, width='stretch') #use_container_width=True)

    else:
        st.write("Digite um termo para buscar eventos.")
        st.dataframe(eventos_df, width='stretch') # use_container_width=True)
