import pandas as pd

def transformar_dados_ufc(df):
    """
    Limpa e transforma colunas do DataFrame para formatos numéricos utilizáveis.
    """
    df_clean = df.copy()

    # --- 1. Limpeza de Percentuais (Str. Acc., Str. Def, TD Acc., TD Def.) ---
    percentual_cols = ['Str. Acc.', 'Str. Def', 'TD Acc.', 'TD Def.']
    for col in percentual_cols:
        # Remove o símbolo de % e converte para float (ex: '50%' -> 0.50)
        df_clean[col] = df_clean[col].astype(str).str.replace('%', '', regex=False).str.strip()
        df_clean[col] = pd.to_numeric(df_clean[col], errors='coerce') / 100.0

    # --- 2. Limpeza de Peso (Weight) ---
    # Remove ' lbs.' e converte para float. Você pode converter para KG aqui também,
    # mas manteremos em libras por enquanto para simplicidade.
    df_clean['Weight'] = df_clean['Weight'].astype(str).str.replace(' lbs.', '', regex=False).str.strip()
    df_clean['Weight'] = pd.to_numeric(df_clean['Weight'], errors='coerce')

    # --- 3. Limpeza de Alcance (Reach) ---
    # Remove aspas (") e converte para numérico
    df_clean['Reach'] = df_clean['Reach'].astype(str).str.replace('"', '', regex=False).str.strip()
    df_clean['Reach'] = pd.to_numeric(df_clean['Reach'], errors='coerce')

    # --- 4. Limpeza e Conversão de Altura (Height) ---
    # Conversão de pés e polegadas (ex: 5' 7") para polegadas totais.
    def converter_altura(altura_str):
        if pd.isna(altura_str) or 'N/A' in altura_str or 'None' in altura_str:
            return None
        
        try:
            # Separa os pés (') e as polegadas (")
            partes = altura_str.replace('"', '').split("'")
            feet = float(partes[0].strip())
            inches = float(partes[1].strip())
            # 1 pé = 12 polegadas
            total_inches = (feet * 12) + inches
            return total_inches
        except:
            return None

    df_clean['Height_in_inches'] = df_clean['Height'].apply(converter_altura)
    # Remove a coluna original 'Height' após a conversão
    df_clean = df_clean.drop(columns=['Height'])

    # --- 5. Conversão de Recorde (Recorde) ---
    # Cria colunas separadas para vitórias, derrotas e empates
    df_clean[['Wins', 'Losses', 'Draws']] = df_clean['Recorde'].str.split('-', expand=True).fillna(0)
    df_clean['Wins'] = pd.to_numeric(df_clean['Wins'], errors='coerce')
    df_clean['Losses'] = pd.to_numeric(df_clean['Losses'], errors='coerce')
    df_clean['Draws'] = pd.to_numeric(df_clean['Draws'], errors='coerce')
    df_clean = df_clean.drop(columns=['Recorde']) # Remove a coluna original

    # Converte outras colunas SLpM, SApM, TD Avg., Sub. Avg. para numérico
    numeric_cols_to_convert = ['SLpM', 'SApM', 'TD Avg.', 'Sub. Avg.']
    for col in numeric_cols_to_convert:
        df_clean[col] = pd.to_numeric(df_clean[col], errors='coerce')

    return df_clean

# --- Execução da Transformação ---
# Assumindo que você carregou o CSV
df_bruto = pd.read_csv('dados_ufc_brutos.csv') 
df_limpo = transformar_dados_ufc(df_bruto)

# Salva a versão limpa (Data Mart)
df_limpo.to_csv('dados_ufc_limpos.csv', index=False)
print("Dados limpos e transformados salvos em 'dados_ufc_limpos.csv'.")