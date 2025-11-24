import streamlit as st
import pandas as pd
import numpy as np

# --- Configuração da Página ---
st.set_page_config(
    page_title="Dashboard UFC Stats (Análise)",
    layout="wide"
)

# Use o decorador de cache para carregar os dados apenas uma vez
@st.cache_data
def load_data(file_path):
    """Carrega os dados limpos do CSV."""
    try:
        df = pd.read_csv(file_path)
        # Preenche valores NaN em colunas numéricas com 0 para evitar erros no display
        for col in df.columns:
            if df[col].dtype in [np.float64, np.int64]:
                df[col] = df[col].fillna(0)
        return df
    except FileNotFoundError:
        # Se o arquivo ainda estiver sendo gerado pelo script, usamos uma mensagem de aviso
        st.error(f"Erro: O arquivo '{file_path}' não foi encontrado. O script de coleta deve estar rodando/concluído.")
        return pd.DataFrame()

# Carrega o DataFrame limpo
DATA_FILE = 'dados_ufc_limpos.csv' 
df_lutadores = load_data(DATA_FILE)

# --- Título Principal ---
st.title("📊 Análise de Lutadores do UFC: Comparação")
st.markdown("Use a barra lateral para selecionar dois lutadores para análise lado a lado.")

# Verifica se os dados foram carregados
if not df_lutadores.empty:
    
    fighter_names = sorted(df_lutadores['Nome'].unique().tolist())
    
    # --- 2. BARRA LATERAL PARA SELEÇÃO E COMPARAÇÃO ---
    st.sidebar.header("🥊 Seleção de Lutadores")
    
    # Seletor 1
    selected_fighter_1 = st.sidebar.selectbox(
        'Lutador A (Para Pesquisar, Clique e Digite):',
        fighter_names,
        index=fighter_names.index('Arman Tsarukyan') if 'Arman Tsarukyan' in fighter_names else 0 # Sugestão de lutador 1
    )
    
    # Seletor 2
    selected_fighter_2 = st.sidebar.selectbox(
        'Lutador B (Comparar com):',
        fighter_names,
        index=fighter_names.index('Charles Oliveira') if 'Charles Oliveira' in fighter_names else 1 # Sugestão de lutador 2
    )

    # Filtra os dados
    fighter_data_1 = df_lutadores[df_lutadores['Nome'] == selected_fighter_1].iloc[0]
    fighter_data_2 = df_lutadores[df_lutadores['Nome'] == selected_fighter_2].iloc[0]

    # --- 3. LAYOUT DE COMPARAÇÃO (Main Content) ---
    
    st.header(f"Comparando **{selected_fighter_1}** vs **{selected_fighter_2}**")
    st.markdown("---")

    col_stats_1, col_center, col_stats_2 = st.columns([5, 1, 5])

    # Coluna 1: Lutador A
    with col_stats_1:
        st.subheader(selected_fighter_1)
        st.caption(f"Recorde: {int(fighter_data_1['Wins'])} - {int(fighter_data_1['Losses'])} - {int(fighter_data_1['Draws'])}")
        
        # Stats Físicas
        st.markdown("**Características Físicas**")
        st.info(f"Altura: {fighter_data_1['Height_in_inches']:.1f} in / Peso: {int(fighter_data_1['Weight'])} lbs / Base: {fighter_data_1['STANCE']}")

        # Stats de Luta
        st.markdown("**Métricas de Luta**")
        st.metric("Golpes Desferidos (SLpM)", f"{fighter_data_1['SLpM']:.2f}", help="Significant Strikes Landed per Minute")
        st.metric("Precisão de Golpes (Str. Acc.)", f"{fighter_data_1['Str. Acc.'] * 100:.0f}%")
        st.metric("Quedas Média (TD Avg.)", f"{fighter_data_1['TD Avg.']:.2f}")

    # Coluna Central: VS
    with col_center:
        st.markdown("<h1 style='text-align: center; margin-top: 100px;'>VS</h1>", unsafe_allow_html=True)


    # Coluna 2: Lutador B
    with col_stats_2:
        st.subheader(selected_fighter_2)
        st.caption(f"Recorde: {int(fighter_data_2['Wins'])} - {int(fighter_data_2['Losses'])} - {int(fighter_data_2['Draws'])}")
        
        # Stats Físicas
        st.markdown("**Características Físicas**")
        st.info(f"Altura: {fighter_data_2['Height_in_inches']:.1f} in / Peso: {int(fighter_data_2['Weight'])} lbs / Base: {fighter_data_2['STANCE']}")
        
        # Stats de Luta
        st.markdown("**Métricas de Luta**")
        st.metric("Golpes Desferidos (SLpM)", f"{fighter_data_2['SLpM']:.2f}")
        st.metric("Precisão de Golpes (Str. Acc.)", f"{fighter_data_2['Str. Acc.'] * 100:.0f}%")
        st.metric("Quedas Média (TD Avg.)", f"{fighter_data_2['TD Avg.']:.2f}")

else:
    st.warning("Aguardando o carregamento dos dados completos.")

# ... O código de comparação por st.metric (col_stats_1, col_center, col_stats_2) termina aqui ...


st.markdown("---")
    
    # --- 4. SEÇÃO DE GRÁFICOS DE COMPARAÇÃO ---
st.header("Análise Gráfica de Performance")
    
    # Métricas para Comparação em Gráfico
metrics_to_compare = [
    'SLpM',          # Golpes Desferidos por Minuto
    'Str. Acc.',     # Precisão de Golpes
    'TD Avg.',       # Quedas Desferidas Média
    'TD Def.',       # Defesa de Quedas
]
    
    # Cria um DataFrame para a visualização
comparison_df = pd.DataFrame({
    'Lutador': [selected_fighter_1, selected_fighter_2],
    'SLpM (Golpes/min)': [fighter_data_1['SLpM'], fighter_data_2['SLpM']],
    'Str. Acc. (%)': [fighter_data_1['Str. Acc.'] * 100, fighter_data_2['Str. Acc.'] * 100],
    'Str. Def (%)': [fighter_data_1['Str. Def'] * 100, fighter_data_2['Str. Def'] * 100],
    'TD Avg. (Quedas/luta)': [fighter_data_1['TD Avg.'], fighter_data_2['TD Avg.']],
    'TD Def. (%)': [fighter_data_1['TD Def.'] * 100, fighter_data_2['TD Def.'] * 100],
    'TD Acc. (%)': [fighter_data_1['TD Acc.'] * 100, fighter_data_2['TD Acc.'] * 100]
})
    
    # Transpõe o DataFrame para que as métricas sejam as colunas e seja fácil plotar
comparison_df_T = comparison_df.set_index('Lutador').T.reset_index()
comparison_df_T = comparison_df_T.rename(columns={'index': 'Métrica'})
    
    # Cria o gráfico usando o Streamlit Bar Chart
    # Usaremos colunas para separar as visualizações e melhorar o layout
    
st.subheader("Comparação de Média por Minuto (SLpM vs TD Avg)")
    
    # Gráfico 1: Agressividade
chart_data = comparison_df[['Lutador', 'SLpM (Golpes/min)', 'TD Avg. (Quedas/luta)']].set_index('Lutador')
st.bar_chart(chart_data)

st.subheader("Comparação de Precisão e Defesa")
    
col_chart_1, col_chart_2 = st.columns(2)
    
with col_chart_1:
    st.caption("Precisão de Golpes vs Defesa de Golpes")
    chart_data_accuracy = comparison_df[['Lutador', 'Str. Acc. (%)', 'Str. Def (%)']].set_index('Lutador')
    st.bar_chart(chart_data_accuracy)
        
with col_chart_2:
    st.caption("Precisão de Quedas vs Defesa de Quedas")
    chart_data_td = comparison_df[['Lutador', 'TD Acc. (%)', 'TD Def. (%)']].set_index('Lutador')
    st.bar_chart(chart_data_td)

