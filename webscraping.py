import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

# --- CONSTANTES GLOBAIS ---
BASE_INDEX_URL = "http://ufcstats.com/statistics/fighters" 
ALFABETO = [chr(i) for i in range(ord('A'), ord('Z') + 1)] # Lista de A a Z
BASE_DETAIL_URL = "http://ufcstats.com/fighter-details/"

# --------------------------------------------------------------------------------
# 1. FUNÇÃO DE EXTRAÇÃO DE LINKS (por letra)
# --------------------------------------------------------------------------------

def extrair_links_por_letra(letra):
    """
    Baixa a página de índice para uma letra específica, forçando o parâmetro 'page=all'.
    """
    # CORREÇÃO CRUCIAL: Constrói a URL completa com char=X e page=all
    url_por_letra = f"{BASE_INDEX_URL}?char={letra}&page=all" 
    fighter_urls = set()

    try:
        response = requests.get(url_por_letra)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        links = soup.find_all('a', href=True)
        
        for link in links:
            href = link['href']
            # Garante que é um link de detalhes de lutador
            if BASE_DETAIL_URL in href: 
                fighter_urls.add(href)

        print(f"✅ Letra {letra}: {len(fighter_urls)} links encontrados.")
        return list(fighter_urls)

    except Exception as e:
        print(f"❌ Erro ao extrair links para a letra {letra}: {e}")
        return []

# --------------------------------------------------------------------------------
# 2. FUNÇÃO DE EXTRAÇÃO DE DETALHES (por lutador)
# --------------------------------------------------------------------------------

def extrair_stats_do_lutador_v2(url):
    """
    Baixa a página de detalhes do lutador e extrai as estatísticas e o Recorde.
    """
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # --- 1. Extração do Nome do Lutador ---
        nome_element = soup.find('span', class_='b-content__title-highlight')
        nome_lutador = nome_element.text.strip() if nome_element else "Nome não encontrado"
        
        # --- 2. Extração do Recorde (Wins-Losses-Draws) ---
        recorde_element = soup.find('span', class_='b-content__title-record')
        recorde_texto = recorde_element.text.strip() if recorde_element else "Recorde não encontrado"
        
        recorde = recorde_texto.replace('Record:', '').strip()
        
        # --- 3. Extração das Estatísticas Principais ---
        stats_list = soup.find_all('li', class_='b-list__box-list-item')
        
        stats_dict = {}
        for item in stats_list:
            partes = item.text.split(':')
            if len(partes) == 2:
                chave = partes[0].strip()
                valor = partes[1].strip()
                stats_dict[chave] = valor
                
        # --- 4. Consolidação dos Dados ---
        stats_dict['Nome'] = nome_lutador
        stats_dict['Recorde'] = recorde 
        
        return stats_dict

    except Exception as e:
        print(f"Erro ao extrair dados da URL {url}: {e}")
        return None

# --------------------------------------------------------------------------------
# 3. FUNÇÃO PIPELINE PRINCIPAL (Coordena a coleta total)
# --------------------------------------------------------------------------------

def pipeline_coleta_completa():
    
    todos_os_dados = []
    urls_lutadores_completos = set() 
    
    # --- ETAPA 1: COLETAR TODOS OS LINKS POR ALFABETO ---
    print("Iniciando coleta de links em TODAS as páginas do alfabeto (A-Z)...")
    
    for letra in ALFABETO:
        # CORREÇÃO: Chama a função extrair_links_por_letra com o argumento 'letra'
        links_da_letra = extrair_links_por_letra(letra) 
        
        urls_lutadores_completos.update(links_da_letra)
        
        # 🛑 DELAY ENTRE AS PÁGINAS DE ÍNDICE
        time.sleep(1) 
        
    urls_lista = list(urls_lutadores_completos)
    print(f"\n✅ Coleta de links finalizada. Total de lutadores únicos encontrados: {len(urls_lista)}")
    print("----------------------------------------------------------------------")
    
    
    # --- ETAPA 2: COLETAR OS DETALHES DE CADA LUTADOR ---
    print("Iniciando coleta de detalhes...")
    
    for i, url in enumerate(urls_lista): 
        # ATENÇÃO: É vital manter o time.sleep(2) para não sobrecarregar o site!
        print(f"Coletando dados do lutador {i+1}/{len(urls_lista)}: {url}")
        
        dados_lutador = extrair_stats_do_lutador_v2(url)
        
        if dados_lutador:
            todos_os_dados.append(dados_lutador)
            
        # 🛑 DELAY ENTRE PÁGINAS DE DETALHE
        time.sleep(2)
        
    # --- FINALIZAÇÃO E RETORNO CORRIGIDO ---
    if todos_os_dados:
        df_final = pd.DataFrame(todos_os_dados)
        print("\n✅ Pipeline de Coleta FINALIZADO.")
        print(f"DataFrame com {len(df_final)} lutadores criado com sucesso.")
        return df_final
    else:
        print("\n❌ Nenhum dado de lutador foi coletado. Retornando DataFrame vazio.")
        return pd.DataFrame()


# --------------------------------------------------------------------------------
# 4. EXECUÇÃO PRINCIPAL
# --------------------------------------------------------------------------------

if __name__ == "__main__":
    
    print("Iniciando Projeto de Web Scraping e Data Engineering do UFC...")
    
    # Executa o Pipeline de Coleta Total
    df_stats_brutos = pipeline_coleta_completa()

    # Salva os dados brutos em um arquivo CSV 
    if not df_stats_brutos.empty:
        df_stats_brutos.to_csv('dados_ufc_brutos.csv', index=False)
        print("\nOs dados brutos foram salvos em 'dados_ufc_brutos.csv'.")
    else:
        print("\nNão foi possível salvar os dados brutos, pois o DataFrame está vazio.")