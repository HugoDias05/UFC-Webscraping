import streamlit as st
import pandas as pd
import numpy as np

# --- Configuração da Página ---
st.set_page_config(
    page_title="Explorar por Categoria de Peso",
    layout="wide"
)

# Use o decorador de cache para carregar os dados apenas uma vez
@st.cache_data
def load_data(file_path):
    """Carrega os dados limpos do CSV."""
    try:
        df = pd.read_csv(file_path)
        # Preenche valores NaN em colunas numéricas com 0
        for col in df.columns:
            if df[col].dtype in [np.float64, np.int64]:
                df[col] = df[col].fillna(0)
        return df
    except FileNotFoundError:
        st.error(f"Erro: O arquivo '{file_path}' não foi encontrado. O script de coleta deve estar rodando/concluído.")
        return pd.DataFrame()

# Mapeamento aproximado das categorias de peso do UFC (em lbs)
PESO_MAP = {
    'Todos': 0,
    'Peso Pesado (265 lbs)': 265,
    'Meio Pesado (205 lbs)': 205,
    'Peso Médio (185 lbs)': 185,
    'Meio Médio (170 lbs)': 170,
    'Peso Leve (155 lbs)': 155,
    'Peso Pena (145 lbs)': 145,
    'Peso Galo (135 lbs)': 135,
    'Peso Mosca (125 lbs)': 125,
    'Peso Palha Feminino (115 lbs)': 115
}

# Carrega o DataFrame limpo
DATA_FILE = 'dados_ufc_limpos.csv' 
df_lutadores = load_data(DATA_FILE)

# --- Título Principal ---
st.title("⚖️ Explorar e Filtrar Lutadores por Categoria de Peso")
st.markdown("Use o filtro lateral para ver a lista de lutadores de uma categoria específica.")

# Verifica se os dados foram carregados
if not df_lutadores.empty:
    
    # --- 2. BARRA LATERAL PARA FILTRO ---
    st.sidebar.header("Filtro de Categoria")
    
    # Seletor de Categoria
    selected_category = st.sidebar.selectbox(
        'Selecione a Categoria de Peso:',
        list(PESO_MAP.keys())
    )
    
    # -----------------------------------------------------------
    # Aplicação do Filtro
    # -----------------------------------------------------------
    
    df_filtered = df_lutadores.copy()
    
    if selected_category != 'Todos':
        weight_limit = PESO_MAP[selected_category]
        # Filtra pelo peso exato (em libras)
        df_filtered = df_filtered[df_filtered['Weight'] == weight_limit]

    # Ordena por vitórias para ter um ranking mais lógico
    df_filtered = df_filtered.sort_values(by=['Wins', 'SLpM'], ascending=[False, False])
    
    
    # --- 3. EXIBIÇÃO DA TABELA PRINCIPAL ---
    
    st.subheader(f"Lutadores Encontrados: {len(df_filtered)} ({selected_category})")
    
    # Exibir a tabela interativa
    st.dataframe(
        df_filtered[[
            'Nome', 
            'Wins', 
            'Losses', 
            'Weight', 
            'STANCE', 
            'SLpM', 
            'Str. Acc.', 
            'TD Avg.', 
            'TD Def.'
        ]],
        use_container_width=True,
        hide_index=True
    )

else:
    st.warning("Aguardando o carregamento dos dados completos.")