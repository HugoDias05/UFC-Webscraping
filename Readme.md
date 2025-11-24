# Projeto de Portfólio: Análise de Estatísticas de Lutadores do UFC

Este projeto demonstra habilidades completas em **Engenharia de Dados** (Web Scraping e ETL) e **Visualização Interativa** (Streamlit). O objetivo é coletar, limpar e analisar estatísticas detalhadas de todos os lutadores ativos e inativos presentes no banco de dados do UFCStats.

---

### 🚀 Visão Geral e Arquitetura do Projeto

A solução foi estruturada em três etapas principais, refletindo um pipeline de dados robusto:

1.  **Coleta (Web Scraping):** Extração em massa de dados de todas as páginas do índice de lutadores (A-Z).
2.  **Transformação (ETL/Limpeza):** Padronização e enriquecimento dos dados.
3.  **Visualização (Dashboard):** Criação de um painel interativo para análise de performance e comparação.



---

### ⚙️ Tecnologias Utilizadas

* **Python:** Linguagem principal para desenvolvimento do pipeline.
* **Web Scraping:** `requests` (para requisições HTTP) e `BeautifulSoup` (para parsing do HTML).
* **Análise de Dados:** `pandas` (para manipulação, limpeza e transformação de dados).
* **Visualização e Front-End:** **Streamlit** (para construir o dashboard web interativo).

---

### 📊 Funcionalidades do Dashboard

O aplicativo Streamlit possui uma estrutura multi-página (`Home.py`, `01_📊_Análise...py`, `02_⚖️_Explorar...py`) e oferece os seguintes recursos de análise:

| Página | Funcionalidade | Descrição |
| :--- | :--- | :--- |
| **Home** | Apresentação | Tela inicial com **apresentação do desenvolvedor** (Hugo Dias) e detalhamento do projeto (Portfólio). |
| **Análise de Lutadores** | **Comparação 1v1** | Permite selecionar dois lutadores para visualizar suas métricas lado a lado. |
| **Filtro por Peso** | **Filtro de Categoria** | Tabela interativa que permite filtrar todos os lutadores por **Peso Pesado, Peso Leve,** etc. |

---

### 🏗️ Estrutura do Pipeline de Dados (ETL)

O pipeline de dados é executado em `webscraping.py` (Coleta) e, em seguida, pelo seu script de transformação (Limpeza).

#### 1. Coleta (`webscraping.py`)

* **Escalabilidade:** Implementação de um loop alfabético (`A-Z`) com o parâmetro `page=all` para garantir a coleta de **todos** os milhares de lutadores.
* **Robustez:** Uso de **`time.sleep(2)`** entre requisições para evitar bloqueio do servidor (Web Scraping ético).
* **Dados Coletados:** Estatísticas físicas, recorde (Wins-Losses-Draws), métricas de performance (SLpM, Str. Acc., TD Avg, etc.) e **Histórico de Lutas (Tabela Tapology)**.

#### 2. Transformação (Limpeza)

* **Padronização:** Conversão de métricas (`Altura`, `Peso`, etc.) para unidades consistentes (ex: polegadas para altura).
* **Enriquecimento:** Criação da coluna **`Recorde_Completo`** (`W-L-D`) a partir das colunas separadas de vitórias, derrotas e empates.
* **Output:** O pipeline final gera o arquivo **`dados_ufc_limpos.csv`**, que alimenta o dashboard.

---

### 💾 Como Executar o Projeto Localmente

1.  **Clone o repositório:**
    ```bash
    git clone https://github.com/HugoDias05/UFC-Webscraping
    ```

2.  **Instale as dependências:**
    ```bash
    pip install streamlit pandas requests beautifulsoup4 numpy
    ```

3.  **Execute o pipeline de coleta (AVISO: Leva algumas horas por conta da quantidade de Lutadores presentes no UFC!):**
    ```bash
    python webscraping.py
    ```

4.  **Inicie o Dashboard:**
    ```bash
    streamlit run Home.py
    ```
    O aplicativo será aberto automaticamente no seu navegador.

---

### 📧 Desenvolvedor

**Hugo Dias**
*  [[**LinkedIn**](https://linkedin.com/in/hugoduartedias)]
