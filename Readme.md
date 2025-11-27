# Projeto de Portfólio: Análise de Estatísticas de Lutadores do UFC

Este projeto demonstra habilidades completas em **Engenharia de Dados** (Web Scraping, ETL e **CDC**) e **Visualização Interativa** (Streamlit). O objetivo é coletar, limpar e analisar estatísticas detalhadas de todos os lutadores ativos e inativos presentes no banco de dados do UFCStats, com foco na **eficiência operacional** do pipeline de coleta.

---

### 🚀 Visão Geral e Arquitetura do Projeto

A solução foi estruturada em três etapas principais, refletindo um pipeline de dados robusto com foco em otimização:

1.  **Coleta (Web Scraping CDC):** Extração de dados em massa, aplicando a lógica de **Change Data Capture (CDC)** para coletar **apenas** alterações e novos registros.
   O script `webscraping.py` implementa a lógica de **Upsert (Update + Insert)** da seguinte forma:

* **Identificação de Novas Entradas:** O script detecta automaticamente lutadores recém-adicionados ao site, realizando a **inserção (Insert)** de novos registros.
* **Atualização Eficiente:** Para garantir a atualização do registro de lutadores existentes (cujo histórico de lutas pode ter mudado), o pipeline utiliza a **amostragem randômica (Sampling)** de um pequeno *subset* de URLs.
    * **Vantagem:** Essa amostragem simula a detecção de alteração de dados (**CDC**) e permite que os dados antigos sejam sobrescritos com as informações mais frescas (**Update**), sem precisar raspar todos os milhares de lutadores.
2.  **Transformação (ETL/Limpeza):** Padronização e enriquecimento dos dados.
3.  **Visualização (Dashboard):** Criação de um painel interativo para análise de performance e comparação.

---

### 🌟 Diferencial Sênior: Change Data Capture (CDC)

O pipeline de Web Scraping não realiza mais um *Full Refresh* (Coleta Total) em todas as execuções, o que economiza tempo e recursos de forma significativa.



---

### ⚙️ Tecnologias Utilizadas

* **Python:** Linguagem principal para desenvolvimento do pipeline.
* **Web Scraping:** `requests` (para requisições HTTP) e `BeautifulSoup` (para parsing do HTML).
* **Hash/CDC:** `hashlib` e `random` para controle de mudança e amostragem eficiente.
* **Análise de Dados:** `pandas` (para manipulação, limpeza e transformação de dados, incluindo a lógica de **Upsert/Merge**).
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

* **Eficiência (CDC):** Implementação da lógica de Upsert para **Atualizar** registros existentes e **Inserir** novos, evitando a raspagem desnecessária de dados estáticos.
* **Escalabilidade:** Implementação de um loop alfabético (`A-Z`) com o parâmetro `page=all` para garantir a coleta do universo completo de links.
* **Robustez:** Uso de **`time.sleep(2)`** entre requisições para evitar bloqueio do servidor (Web Scraping ético).
* **Dados Coletados:** Estatísticas físicas, recorde (Wins-Losses-Draws), métricas de performance (SLpM, Str. Acc., TD Avg, etc.) e **Histórico de Lutas**.

#### 2. Transformação (Limpeza)

* **Padronização:** Conversão de métricas (`Altura`, `Peso`, etc.) para unidades consistentes (ex: polegadas para altura).
* **Enriquecimento:** Criação da coluna **`Recorde_Completo`** (`W-L-D`) a partir das colunas separadas de vitórias, derrotas e empates.
* **Output:** O pipeline final gera o arquivo **`dados_ufc_limpos.csv`**, que alimenta o dashboard.

---

### 💾 Como Executar o Projeto Localmente

1.  **Clone o repositório:**
    ```bash
    git clone [https://github.com/HugoDias05/UFC-Webscraping](https://github.com/HugoDias05/UFC-Webscraping)
    ```

2.  **Instale as dependências:**
    ```bash
    pip install streamlit pandas requests beautifulsoup4 numpy
    ```

3.  **Execute o pipeline de coleta (AVISO: A primeira execução pode levar tempo para coletar todos os dados, mas as execuções seguintes serão rápidas devido ao CDC!):**
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
* [**LinkedIn**](https://linkedin.com/in/hugoduartedias)
