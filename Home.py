import streamlit as st
import plotly.express as px
import pandas as pd

# -------------------
# CONFIGURAÇÃO INICIAL
# -------------------
st.set_page_config(
    page_title="Meu Dashboard Profissional",
    page_icon="💼",
    layout="wide"
)

# Criando as abas
abas = st.tabs(["🏠 Home", "🎓 Formação e Experiência", "🛠️ Skills"])

# -------------------
# HOME
# -------------------
with abas[0]:
    col1, col2 = st.columns([1, 3])

    with col1:
        st.image("minha-img-dashboard.jpg", width=180)  # coloque sua foto ou link da imagem
    with col2:
        st.title("Olá, eu sou Dayana Ticona Quispe 👋")
        st.subheader("Objetivo Profissional")
        st.write("Tenho grande interesse em **Análise de Dados**, área na qual gostaria muito de "
         "trabalhar e me desenvolver. No futuro, também pretendo atuar com **Machine Learning** "
         "e outras tecnologias avançadas que envolvem inteligência artificial.")
        
        st.markdown("""
        🔗 **Conecte-se comigo**  
        - [LinkedIn](https://www.linkedin.com/in/dayana-ticona-quispe/)  
        - [GitHub](https://github.com/dayquispe)  
        """)

    st.markdown("---")
    nome = st.text_input("Digite seu nome para uma saudação personalizada:")
    if nome:
        st.success(f"Bem-vindo(a), {nome}! 🚀 Vamos explorar meu portfólio juntos.")


# -------------------
# FORMAÇÃO E EXPERIÊNCIA
# -------------------
with abas[1]:
    st.title("🎓 Formação e Experiência")

    # Subtópicos organizados em abas dentro da aba principal
    sub_abas = st.tabs(["💼 Experiência Profissional", "📜 Certificados", "📊 Dashboards & Projetos"])

    # -------- Experiência Profissional --------
    with sub_abas[0]:
        st.subheader("💼 Experiência Profissional")
        
        with st.expander("Vendedora e Assistente Administrativa - Negócio Familiar (MEI) (2023-2024)"):
            st.write("""
            - Atendimento ao cliente, auxiliando na venda de produtos e na resolução de dúvidas. 
            - Organização de mercadorias, controle de estoque e exposição dos itens. 
            - Apoio nas tarefas administrativas do negócio e recebimentos de pagamentos. 
            - Contribuição direta para o funcionamento e crescimento do pequeno empreendimento familiar.
            """)

    # -------- Certificados --------
    with sub_abas[1]:
        st.subheader("📜 Certificados")
        with st.expander("Certificação Lógica de programação: praticando com desafios"):
            st.write("Curso voltado para a prática da lógica de programação, com resolução de desafios, implementação de soluções e desenvolvimento de projetos. A proposta é reforçar conceitos fundamentais, melhorar o raciocínio lógico e preparar o aluno para criar um portfólio sólido e evoluir nas habilidades de programação.")
            st.markdown("[🔗 Ver Certificado](https://cursos.alura.com.br/user/ticonadayana375q7/course/logica-programacao-praticando-desafios/certificate)")
        with st.expander("Certificação Java: aplicando a Orientação a Objetos - Plataforma Alura"):
            st.write("Curso de Java com foco em Orientação a Objetos: conceitos fundamentais, modelagem com classes e métodos, herança, polimorfismo e uso de interfaces.")
            st.markdown("[🔗 Ver Certificado](https://cursos.alura.com.br/user/ticonadayana375q7/course/java-aplicando-orientacao-objetos/certificate)")
        
        with st.expander("Certificação Java: criando a sua primeira aplicação"):
            st.write("Curso de Java voltado para prática: criação de projetos no IntelliJ, compilação e execução, tipos de dados, leitura com Scanner e controle de fluxo com condicionais e loops.")
            st.markdown("[🔗 Ver Certificado](https://cursos.alura.com.br/user/ticonadayana375q7/course/java-criando-primeira-aplicacao/certificate)")
        
        with st.expander("Certificação Pandas: conhecendo a biblioteca"):
            st.write("Curso de Data Science com Pandas: análise exploratória, criação de gráficos, seleção e tratamento de dados (nulos, remoção de colunas/linhas) e construção de novas variáveis.")
            st.markdown("[🔗 Ver Certificado](https://cursos.alura.com.br/user/ticonadayana375q7/course/pandas-conhecendo-biblioteca/certificate)")

        with st.expander("Certificação Estatística com Python: resumindo e analisando dados"):
            st.write("Curso focado em estatística aplicada à análise de dados, com uso do Python para: análise exploratória, compreensão de diferentes tipos de variáveis, cálculo de medidas de tendência central e dispersão, avaliação da distribuição dos dados e identificação de padrões relevantes. Também foi trabalhada a visualização de dados com gráficos e a aplicação prática da estatística como suporte à tomada de decisão baseada em evidências.")
            st.markdown("[🔗 Ver Certificado](https://cursos.alura.com.br/user/ticonadayana375q7/course/estatistica-python-resumindo-analisando-dados/certificate)")

    # -------- Dashboards & Projetos --------
    with sub_abas[2]:
        st.subheader("📊 Dashboards & Projetos com Streamlit")

        with st.expander("Dashboard-de-vendas-com-streamlit-alura"):
            st.write("Dashboard interativo de vendas desenvolvido em Python com Streamlit, Pandas e Plotly, exibindo métricas, gráficos e mapas para análise de receita, quantidade de vendas e desempenho de vendedores.")
            st.markdown("[🔗 Acesse o dashboard](https://dashboard-de-vendas-com-app-alura-nbkknxxydjsxzrarhrkbgy.streamlit.app/)")

        with st.expander("Dashboard imersao-dados-python-alura-2025"):
            st.write("Criado um dashboard interativo para analisar e explorar tendências de salários no mercado de dados. A aplicação permite filtrar informações por ano, senioridade, tipo de contrato e tamanho da empresa, oferecendo insights de forma clara e visual.")
            st.markdown("[🔗 Acesse o dashboard](https://imersao-dados-python-com-alura-em2025.streamlit.app/)")

with abas[2]:
    # =========================
    # Dados das Skills
    # =========================
    skills = {
        "Habilidade": [
            "Microsoft Office (Word, Excel, PowerPoint)",
            "Lógica de Programação",
            "Python",
            "SQL",
            "Java",
            "JavaScript",
            "Trabalho em Equipe",
            "Pontualidade",
            "Facilidade de Aprendizado",
            "Organização",
            "Responsabilidade"
        ],
        "Categoria": [
            "Ferramentas", "Programação", "Programação", "Programação",
            "Programação", "Programação", "Pessoal", "Pessoal",
            "Pessoal", "Pessoal", "Pessoal"
        ],
        "Nível (autoavaliação)": [
            6, 7, 7, 6, 4, 4, 8, 8, 7, 8, 8  # escala 1 a 10
        ]
    }

    df = pd.DataFrame(skills)

    # =========================
    # Layout do Dashboard
    # =========================
    st.title("💼 Dashboard de Skills")
    st.write("Resumo das minhas habilidades profissionais e pessoais.")

    # Mostrar tabela
    st.subheader("📋 Lista de Habilidades")
    st.dataframe(df)

    # Gráfico de barras
    st.subheader("📊 Distribuição das Habilidades por Categoria")
    fig_bar = px.bar(df, x="Habilidade", y="Nível (autoavaliação)", color="Categoria",
                    title="Nível de Proficiência por Habilidade")
    st.plotly_chart(fig_bar)


    # Destaque
    st.subheader("⭐ Destaques")
    st.write("""
    - **Pontos fortes**: Trabalho em equipe, pontualidade, organização e responsabilidade.  
    - **Área técnica**: Boa base em lógica de programação, Python e SQL, com noções de Java e JavaScript.  
    - **Ferramentas**: Conhecimento em Microsoft Office para apoio em documentação e relatórios.
    """)