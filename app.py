import streamlit as st
import pandas as pd

# Load the dataframes (assuming they are available in the Colab environment)

eventos_df = pd.read_excel('09012022_CLASSIFICACAODEEVENTOSPARA20172020.xlsx', sheet_name='Lista', header=None)
eventos_df.columns = ['Sigla', 'Título', 'Estrato']
eventos_df = eventos_df.drop(eventos_df.index[1])
eventos_df = eventos_df.drop(eventos_df.index[0])
#eventos_df = eventos_df.drop(eventos_df.index[1])
eventos_df = eventos_df.reset_index(drop=True)
#eventos_df

periodicos_df = pd.read_excel('classificacoes_publicadas_ciencia_da_computacao_2022_1721678829186.xlsx')
#periodicos_df
# In a real Streamlit app, you would load your data here.
# For this example, we'll assume eventos_df and periodicos_df are already created from previous steps.
# Make sure these dataframes are accessible to the Streamlit app.
# In a production setting, you might load them from a file or database.

# Assuming the dataframes are available in the environment where this script is run
# You might need to adjust how these are accessed based on your setup.
try:
    eventos_df = pd.DataFrame(eventos_df)
    periodicos_df = pd.DataFrame(periodicos_df)
except NameError:
    st.error("Dataframes 'eventos_df' or 'periodicos_df' not found. Please run the data loading cells.")
    st.stop()


st.title('Consulta de Eventos e Periódicos de Computação segundo Qualis Capes (2017-2020)')

# Create tabs
tab1, tab2 = st.tabs(["Periódicos", "Eventos"])

with tab1:
    st.header("Consulta de Periódicos")
    search_term_periodicos = st.text_input('Digite o termo de busca para Periódicos (Título ou ISSN):')

    if search_term_periodicos:
        # Perform case-insensitive search on 'Título' and 'ISSN' for periodicals
        search_results_periodicos = periodicos_df[
            periodicos_df['Título'].str.contains(search_term_periodicos, case=False, na=False) |
            periodicos_df['ISSN'].astype(str).str.contains(search_term_periodicos, case=False, na=False)
        ]
        st.write(f"Resultados da busca por '{search_term_periodicos}' em Periódicos:")
        st.dataframe(search_results_periodicos)
    else:
        st.write("Digite um termo para buscar periódicos.")
        st.dataframe(periodicos_df)

with tab2:
    st.header("Consulta de Eventos")
    search_term_eventos = st.text_input('Digite o termo de busca para Eventos (Título ou Sigla):')

    if search_term_eventos:
        # Perform case-insensitive search on 'Título' and 'Sigla' for events
        search_results_eventos = eventos_df[
            eventos_df['Título'].str.contains(search_term_eventos, case=False, na=False) |
            eventos_df['Sigla'].str.contains(search_term_eventos, case=False, na=False)
        ]
        st.write(f"Resultados da busca por '{search_term_eventos}' em Eventos:")
        st.dataframe(search_results_eventos)
    else:
        st.write("Digite um termo para buscar eventos.")
        st.dataframe(eventos_df)
