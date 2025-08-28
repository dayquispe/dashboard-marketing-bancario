import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from scipy import stats

# Título principal da página
st.title("📊 Análise de Dados")

# Macro-abas
aba1, aba2, aba3 = st.tabs(["📑 Dados", "📊 Exploração", "📈 Inferência"])

# -----------------------------------------------------------
# ABA 1 - DADOS
# -----------------------------------------------------------
with aba1:
    st.header("📑 Apresentação dos Dados")
    
    sub1, sub2, sub3 = st.tabs([
        "Explicação do Dataset",
        "Tipos de Variáveis",
        "Perguntas de Análise"
    ])
    
    with sub1:
        st.subheader("Explicação sobre o conjunto de dados")
        url = "https://raw.githubusercontent.com/dayquispe/dashboard-marketing-bancario/refs/heads/main/dados_tratados.csv"
        dados = pd.read_csv(url)
        
        st.markdown("""
        Este conjunto de dados vem de uma campanha de marketing de um banco português, 
        em que clientes foram contatados para avaliar a adesão a depósitos a prazo.  
        Após o tratamento, as variáveis representam informações demográficas, 
        financeiras e comportamentais dos clientes, além de detalhes da campanha de marketing.
        """)

        st.dataframe(dados.head())

    with sub2:
        if 'dados' in locals():
            st.subheader("🔎 Identificação dos Tipos de Variáveis")

            st.markdown("### 📑 Dicionário de Variáveis")

            # Qualitativas
            st.markdown("#### 🎭 Variáveis Qualitativas")
            with st.expander("trabalho (nominal)"):
                st.write("Tipo de emprego do cliente (ex.: admin., technician, services).")
            with st.expander("estado_civil (nominal)"):
                st.write("Estado civil do cliente (ex.: single, married, divorced).")
            with st.expander("educacao (ordinal)"):
                st.write("Nível de escolaridade do cliente (ex.: primary < secondary < tertiary).")
            with st.expander("inadimplente (nominal)"):
                st.write("Se o cliente possui inadimplência (yes/no).")
            with st.expander("emprestimo_habitacao (nominal)"):
                st.write("Se o cliente possui empréstimo habitacional (yes/no).")
            with st.expander("emprestimo_pessoal (nominal)"):
                st.write("Se o cliente possui empréstimo pessoal (yes/no).")
            with st.expander("contato (nominal)"):
                st.write("Tipo de contato realizado (ex.: celular, telefone fixo, unknown).")
            with st.expander("mes (ordinal)"):
                st.write("Mês do último contato da campanha (ex.: jan, feb, …).")
            with st.expander("resultado_campanha_anterior (nominal)"):
                st.write("Resultado de campanhas anteriores (ex.: success, failure, unknown).")
            with st.expander("deposito (nominal - alvo)"):
                st.write("Variável alvo: indica se o cliente contratou o depósito (yes/no).")

            # Quantitativas
            st.markdown("#### 🔢 Variáveis Quantitativas")
            with st.expander("idade (discreta)"):
                st.write("Idade do cliente em anos (números inteiros).")
            with st.expander("saldo (contínua)"):
                st.write("Saldo médio anual da conta, em euros (valores decimais).")
            with st.expander("dia (discreta)"):
                st.write("Dia do mês em que o cliente foi contatado.")
            with st.expander("duracao (discreta)"):
                st.write("Duração da ligação em segundos.")
            with st.expander("campanha (discreta)"):
                st.write("Número de contatos feitos nesta campanha.")
            with st.expander("dias_desde_campanha (discreta)"):
                st.write("Número de dias desde o último contato em campanha anterior (-1 = não havia campanha).")
            with st.expander("campanhas_anteriores (discreta)"):
                st.write("Número de contatos feitos em campanhas anteriores.")

            st.markdown("#### 📊 Tipos detectados automaticamente no DataFrame")
            st.dataframe(dados.dtypes.rename("Tipo de Dados"))
        else:
            st.info("Carregue o dataset na aba anterior.")

            
    with sub3:
        st.subheader("Definição das principais perguntas de análise")
        st.markdown("""
        - Quais características dos clientes mais influenciam a decisão de contratar um depósito?  
        - O saldo médio dos clientes varia conforme o sucesso da campanha?  
        - Existe relação entre nível de escolaridade e adesão?  
        - A duração da ligação tem impacto direto na taxa de sucesso?  
        - Campanhas anteriores afetam a probabilidade de resposta positiva?  
        """)

# -----------------------------------------------------------
# ABA 2 - EXPLORAÇÃO
# -----------------------------------------------------------

with aba2:
    st.header("📊 Análise Exploratória")

    sub1, sub2, sub3, sub4 = st.tabs([
        "Tendência Central",
        "Distribuição",
        "Dispersão",
        "Correlação"
    ])


    with sub1:
        # --- Separar numéricas e categóricas ---
        numeric_cols = dados.select_dtypes(include=['int64', 'float64']).columns
        categorical_cols = dados.select_dtypes(include=['object', 'category']).columns

        # --- Medidas centrais numéricas ---
        numeric_summary = dados[numeric_cols].agg(['mean', 'median', 'std', 'var']).T
        numeric_summary['mode'] = dados[numeric_cols].mode().iloc[0]

        # --- Moda das categóricas ---
        cat_mode_df = dados[categorical_cols].mode()
        categorical_modes = cat_mode_df.iloc[0] if not cat_mode_df.empty else None

        # --- Dashboard ---
        st.subheader("Análise de Medidas Centrais")

        st.subheader("Medidas Centrais - Variáveis Numéricas")
        st.dataframe(numeric_summary)

        st.subheader("Moda - Variáveis Categóricas")
        if categorical_modes is not None:
            st.dataframe(categorical_modes)
        else:
            st.warning("Nenhuma moda encontrada para variáveis categóricas.")

        # --- Interpretação automática ---
        st.subheader("📌 Interpretação dos Resultados")

        explicacao = """
        - **Idade**: média de ~41 anos, mediana 38 e moda 31 → a distribuição é levemente enviesada, há clientes mais velhos puxando a média.
        - **Saldo**: média ~1517, mediana 542 e moda 0 → muitos clientes têm saldo zerado, mas existem outliers com saldo muito alto.
        - **Duração das ligações**: média 373s, mediana 255s → a maioria das ligações é curta, mas algumas muito longas aumentam a média.
        - **Campanhas**: mediana 2 e moda 1 → maioria dos clientes foi contatada 1 a 2 vezes.
        - **Dias desde campanha anterior**: moda -1 → significa que a maior parte dos clientes nunca havia sido contatada antes.
        - **Campanhas anteriores**: moda 0 → reforça que a maior parte nunca participou de campanhas passadas.

        🔹 **Perfil categórico mais comum**: cliente casado, com ensino secundário, sem inadimplência, sem empréstimos, contato via celular, mês de maio, resultado anterior desconhecido, e não fez depósito.
        """

        st.markdown(explicacao)
    
    with sub2: 
        st.subheader("Distribuição dos Dados - Dashboard Interativo")

        # --- Sidebar para escolher variável ---
        opcao = st.sidebar.selectbox(
            "Escolha a variável para visualizar:",
            ["idade", "saldo", "duracao", "trabalho", "estado_civil", "educacao", "contato", "mes"]
        )

        # --- Gráficos e interpretação ---
        if opcao in ["idade", "saldo", "duracao"]:  # variáveis numéricas
            fig, axes = plt.subplots(1, 2, figsize=(12, 4))
            
            # Histograma com curva de densidade
            sns.histplot(dados[opcao], bins=40, kde=True, ax=axes[0], color="skyblue")
            axes[0].set_title(f"Histograma - {opcao}")
            
            # Densidade (KDE) sozinha para reforçar a distribuição
            sns.kdeplot(dados[opcao], fill=True, ax=axes[1], color="salmon")
            axes[1].set_title(f"Densidade - {opcao}")
            
            st.pyplot(fig)
            
            # Interpretação simples focada em formato
            if opcao == "idade":
                st.markdown("👤 **Idade**: Distribuição levemente assimétrica à direita, "
                            "com concentração entre 30 e 40 anos.")
            elif opcao == "saldo":
                st.markdown("💰 **Saldo**: Distribuição fortemente assimétrica à direita, "
                            "a maioria dos clientes tem saldo próximo de zero.")
            elif opcao == "duracao":
                st.markdown("⏱️ **Duração da chamada**: A maioria das ligações é curta (até 500s), "
                            "mas há uma cauda longa com chamadas extensas.")

        else:  # variáveis categóricas
            fig, ax = plt.subplots(figsize=(8, 4))
            sns.countplot(x=dados[opcao], order=dados[opcao].value_counts().index, palette="viridis", ax=ax)
            plt.xticks(rotation=30)
            ax.set_title(f"Distribuição - {opcao}")
            st.pyplot(fig)
            
            # Interpretação categórica
            if opcao == "trabalho":
                st.markdown("💼 **Trabalho**: Maioria em 'management', seguido por 'blue-collar' e 'technician'.")
            elif opcao == "estado_civil":
                st.markdown("💍 **Estado civil**: Predominância de casados, seguidos por solteiros e divorciados.")
            elif opcao == "educacao":
                st.markdown("📚 **Educação**: Predomínio de secundário, depois terciário e primário.")
            elif opcao == "contato":
                st.markdown("☎️ **Contato**: A maior parte foi via celular, poucos via telefone fixo.")
            elif opcao == "mes":
                st.markdown("📅 **Mês de contato**: Pico em maio, caindo nos outros meses.")

    with sub3:
        st.subheader("Dispersão dos Dados - Variância e Desvio Padrão")

        variaveis = ["idade", "saldo", "duracao"]

        for col in variaveis:
            media = dados[col].mean()
            variancia = dados[col].var()
            desvio = dados[col].std()

            fig, axes = plt.subplots(1, 2, figsize=(14, 5))

            # --- Histograma com média e desvio padrão ---
            sns.histplot(dados[col], bins=30, kde=True, ax=axes[0], color="skyblue")
            axes[0].axvline(media, color="red", linestyle="--", label=f"Média = {media:.2f}")
            axes[0].axvline(media + desvio, color="green", linestyle=":", label=f"+1 DP = {media+desvio:.2f}")
            axes[0].axvline(media - desvio, color="green", linestyle=":", label=f"-1 DP = {media-desvio:.2f}")
            axes[0].set_title(f"Histograma - {col}")
            axes[0].legend()

            # --- Boxplot para outliers ---
            sns.boxplot(x=dados[col], ax=axes[1], color="salmon")
            axes[1].set_title(f"Boxplot - {col}")

            st.pyplot(fig)

            # --- Interpretação focada em dispersão ---
            st.markdown(f"📊 **{col.upper()}**")
            if col == "idade":
                st.markdown(f"- Média: {media:.1f} | DP: {desvio:.1f} | Variância: {variancia:.1f}  \n"
                            "- Idades concentradas em torno da média (30–50 anos).  \n"
                            "- Outliers acima de 70 anos.")
            elif col == "saldo":
                st.markdown(f"- Média: {media:.1f} | DP: {desvio:.1f} | Variância: {variancia:.1f}  \n"
                            "- Grande dispersão: DP bem maior que a média.  \n"
                            "- Forte presença de outliers (saldos muito altos).")
            elif col == "duracao":
                st.markdown(f"- Média: {media:.1f}s | DP: {desvio:.1f}s | Variância: {variancia:.1f}  \n"
                            "- A maioria abaixo de 500s, mas há dispersão muito alta.  \n"
                            "- Muitos outliers (ligações de 2000s ou mais).")
            st.markdown("---")

    with sub4:
        # --- Correlação entre variáveis numéricas ---
        with st.expander("📊 Correlação entre Variáveis Numéricas"):
            st.subheader("Mapa de Correlação")
            fig, ax = plt.subplots(figsize=(6, 4))
            corr = dados[["idade", "saldo", "duracao"]].corr()
            sns.heatmap(corr, annot=True, cmap="coolwarm", center=0, ax=ax)
            ax.set_title("Mapa de Correlação entre Variáveis Numéricas")
            st.pyplot(fig)

            st.markdown("""
            **Interpretação**  
            - As correlações são **baixas**, praticamente nulas.  
            - **Idade x Saldo** mostra leve relação positiva (0.11), mas muito fraca.  
            - **Idade x Duração** e **Saldo x Duração** praticamente não têm associação.  
            👉 Ou seja, idade, saldo e duração não são bons preditores diretos uns dos outros.
            """)

        # --- Duração das chamadas por Estado Civil ---
        with st.expander("💍 Duração das Chamadas por Estado Civil"):
            st.subheader("Boxplot - Duração vs Estado Civil")
            fig, ax = plt.subplots(figsize=(7, 5))
            sns.boxplot(x="estado_civil", y="duracao", data=dados, palette="Set2", ax=ax)
            ax.set_title("Duração das chamadas por Estado Civil")
            st.pyplot(fig)

            st.markdown("""
            **Interpretação**  
            - A **mediana da duração** das ligações é bastante parecida entre solteiros, casados e divorciados.  
            - Todos os grupos apresentam muitos **outliers** (ligações muito longas, acima de 2000s).  
            - Isso sugere que o **estado civil não é um fator determinante** para o tempo de ligação.
            """)

        # --- Saldo por tipo de trabalho ---
        with st.expander("💼 Saldo por Tipo de Trabalho"):
            st.subheader("Distribuição do Saldo por Trabalho")
            fig, ax = plt.subplots(figsize=(10, 5))
            sns.violinplot(x="trabalho", y="saldo", data=dados, palette="muted", ax=ax)
            ax.set_title("Saldo por Trabalho")
            plt.xticks(rotation=30)
            st.pyplot(fig)

            st.markdown("""
            **Interpretação**  
            - A maioria dos clientes, independentemente do trabalho, possui **saldo próximo de zero**.  
            - Alguns grupos como **aposentados (retired)** e **management** mostram maiores variações, com outliers chegando a saldos muito altos.  
            - Isso indica que a **ocupação pode influenciar** no saldo bancário, mas de forma desigual e com muita dispersão.
            """)

        # --- Contato por mês ---
        with st.expander("☎️ Frequência de Contato por Mês"):
            st.subheader("Heatmap - Contato vs Mês")
            fig, ax = plt.subplots(figsize=(8, 5))
            contato_mes = dados.groupby(["mes", "contato"]).size().unstack(fill_value=0)
            sns.heatmap(contato_mes, annot=True, fmt="d", cmap="Blues", ax=ax)
            ax.set_title("Frequência: Contato por Mês")
            st.pyplot(fig)

            st.markdown("""
            **Interpretação**  
            - O maior volume de contatos ocorre em **maio (may)**, principalmente via celular.  
            - O canal **telefone fixo** tem bem menos chamadas em todos os meses.  
            - Em alguns meses (jul e nov), aparece um grande número de contatos classificados como **unknown**.  
            - Isso sugere que **campanhas de marketing são sazonais**, com picos claros em determinados meses.
            """)
        
with aba3:
        # =====================
    # Layout do Dashboard
    # =====================
    st.title("📈 Intervalos de Confiança e Testes de Hipótese")

    # --- Escolha do parâmetro ---
    st.subheader("🔎 Parâmetro escolhido: Idade dos clientes")
    st.markdown("""
    A variável **idade** foi escolhida porque é numérica contínua, 
    o que permite calcular Intervalo de Confiança da média e aplicar Teste de Hipótese.
    """)

    # --- Estatísticas ---
    media = dados["idade"].mean()
    desvio = dados["idade"].std()
    n = len(dados["idade"])
    alpha = 0.05

    # Intervalo de confiança (95%)
    ic = stats.t.interval(0.95, df=n-1, loc=media, scale=desvio/(n**0.5))

    # Teste de hipótese (t-test contra 40 anos)
    t_stat, p_val = stats.ttest_1samp(dados["idade"], 40)

    # =====================
    # Visualizações
    # =====================
    fig, ax = plt.subplots(figsize=(8,5))
    sns.histplot(dados["idade"], bins=30, kde=True, color="skyblue", ax=ax)
    ax.axvline(media, color="red", linestyle="--", label=f"Média {media:.2f}")
    ax.axvline(ic[0], color="green", linestyle=":", label=f"IC 95% = [{ic[0]:.2f}, {ic[1]:.2f}]")
    ax.axvline(ic[1], color="green", linestyle=":")
    ax.legend()
    ax.set_title("Distribuição da Idade com Intervalo de Confiança")
    st.pyplot(fig)

    # =====================
    # Resultados
    # =====================
    st.subheader("📊 Resultados Estatísticos")

    st.markdown(f"""
    - **Média amostral:** {media:.2f} anos  
    - **Desvio padrão:** {desvio:.2f}  
    - **Intervalo de confiança (95%):** {ic[0]:.2f} a {ic[1]:.2f} anos  
    - **Hipótese nula (H₀):** μ = 40 anos  
    - **Hipótese alternativa (H₁):** μ ≠ 40 anos  
    - **Estatística t:** {t_stat:.2f}  
    - **p-valor:** {p_val:.4f}  
    """)

    # =====================
    # Interpretação
    # =====================
    st.subheader("📝 Interpretação")

    if p_val < alpha:
        st.markdown(f"""
        ✅ Como **p-valor = {p_val:.4f} < 0.05**, rejeitamos H₀.  
        Isso significa que a **idade média dos clientes é estatisticamente diferente de 40 anos**.  
        O IC 95% [{ic[0]:.2f}, {ic[1]:.2f}] confirma que a média populacional não inclui o valor 40.
        """)
    else:
        st.markdown(f"""
        ❌ Como **p-valor = {p_val:.4f} ≥ 0.05**, não rejeitamos H₀.  
        Isso significa que **não há evidência suficiente** para afirmar que a idade média difere de 40 anos.  
        O IC 95% [{ic[0]:.2f}, {ic[1]:.2f}] contém o valor 40.
        """)
