import streamlit as st

st.set_page_config(
    page_title="Projeto UFC Data Engineering",
    layout="wide"
)

# --- Título Principal ---
st.title("🏆 Projeto de Portfólio: Análise de Estatísticas de Lutadores do UFC")
st.markdown("---")


## ⚙️ Sobre o Projeto
st.header("Data Pipeline e Dashboard Interativo")
st.write("""
Este dashboard é a culminação de um pipeline completo de coleta e tratamento de dados:
""")

col1, col2, col3 = st.columns(3)

with col1:
    st.subheader("1. Coleta (Web Scraping)")
    st.write("Utilização das bibliotecas **requests** e **BeautifulSoup** para extrair dados brutos de estatísticas do UFCStats.")

with col2:
    st.subheader("2. Transformação (Data Cleaning)")
    st.write("Processamento em **Pandas** para limpeza, conversão de formatos (ex: pés/polegadas para polegadas, porcentagens para float) e estruturação do conjunto de dados.")

with col3:
    st.subheader("3. Visualização (Front-End)")
    st.write("Desenvolvimento do painel interativo utilizando **Streamlit**, permitindo a busca e comparação de estatísticas de lutadores.")

st.markdown("---")
st.info("Navegue até a página **'Análise dos Lutadores'** no menu lateral para interagir com o dashboard!")


## 🧑‍💻 Sobre Mim
st.image("assets/foto perfil.png", caption="Foto de Perfil", width=200, output_format="PNG")
st.header("Hugo Dias")
st.write("""
Olá! Meu nome é Hugo, tenho 20 anos e estou atuando na área de Engenharia de Dados.
Este projeto demonstra minhas habilidades em **WebScraping-Pipelines** e **Visualização** utilizando Python.
Estou fazendo esse projeto pessoal, por conta de que gosto bastante do universo das lutas, então, uni o meu Hobby com minha profissão atual para fazer com muito empenho, espero que gostem!
""")
st.markdown(f"**LinkedIn:** https://linkedin.com/in/hugoduartedias")
st.markdown("---")