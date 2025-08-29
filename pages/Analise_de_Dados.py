import streamlit as st
import pandas as pd
import numpy as np
from scipy import stats
from statsmodels.stats.proportion import proportion_confint, proportions_ztest
import plotly.express as px
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import seaborn as sns


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

    st.caption("Aplicação prática com o conjunto de dados de marketing bancário.")

    # --------------------------
    # Preparação do alvo binário
    # --------------------------
    def detect_target(dados):
        candidates = ["y", "deposit", "subscribed", "target", "response"]
        for c in candidates:
            if c in dados.columns:
                if dados[c].dropna().nunique() == 2:
                    return c
        for c in dados.columns:
            if dados[c].dropna().nunique() == 2:
                return c
        return None
    
    target_col = detect_target(dados)
    if target_col is None:
        st.error("Não encontrei uma coluna binária de resposta (ex.: 'y', 'deposit'). Verifique o dataset.")
        st.stop()
    
    dados[target_col] = dados[target_col].astype(str).str.lower().str.strip()
    positives = ["yes", "sim", "1", "true", "t", "y"]
    dados["_target_"] = dados[target_col].apply(lambda x: 1 if x in positives or x=="1" else 0)
    st.info(f"Coluna alvo detectada: **{target_col}** (convertida para 0/1 em `_target_`).")
    
    # colunas categóricas e numéricas
    cat_cols = [c for c in dados.columns if dados[c].dtype == "object" and c not in [target_col]]
    num_cols = [c for c in dados.columns if np.issubdtype(dados[c].dtype, np.number) and c != "_target_"]
    
    # --------------------------
    # Escolha do parâmetro
    # --------------------------
    st.subheader("Escolha do parâmetro para analisar")
    mode = st.radio(
        "Parâmetro principal:",
        ["Taxa de conversão (proporção)", "Média de variável numérica"],
        horizontal=True
    )
    
    # --------------------------
    # BLOCO A — PROPORÇÕES
    # --------------------------
    if mode == "Taxa de conversão (proporção)":
        st.markdown("""
        **Justificativa**:  
        Como a resposta é binária (contratou depósito: *sim/não*), o parâmetro natural é a **proporção de conversão**.  
        Para estimá-la, usamos **Intervalo de Confiança (IC) para proporção** (método de Wilson a 95%).  
        Para comparar grupos (ex.: *houve contato prévio?*), usamos **teste Z para duas proporções**, adequado para amostras grandes e resposta binária.
        """)
    
        # Visão geral — proporção global
        conv_rate = dados["_target_"].mean()
        n = dados["_target_"].count()
        ci_low, ci_high = proportion_confint(count=dados["_target_"].sum(), nobs=n, alpha=0.05, method="wilson")
    
        st.markdown("### Proporção global de conversão")
        kpi1, kpi2, kpi3 = st.columns(3)
        kpi1.metric("Taxa de conversão", f"{100*conv_rate:.2f}%")
        kpi2.metric("IC 95% (Wilson) — limite inferior", f"{100*ci_low:.2f}%")
        kpi3.metric("IC 95% (Wilson) — limite superior", f"{100*ci_high:.2f}%")
    
        fig_g = go.Figure()
        fig_g.add_trace(go.Bar(x=["Conversão"], y=[100*conv_rate], name="Taxa (%)"))
        fig_g.add_shape(type="line", x0=-0.5, x1=0.5, y0=100*ci_low, y1=100*ci_low)
        fig_g.add_shape(type="line", x0=-0.5, x1=0.5, y0=100*ci_high, y1=100*ci_high)
        fig_g.update_layout(yaxis_title="%", title="Taxa global de conversão com IC95% (linhas)")
        st.plotly_chart(fig_g, use_container_width=True)
    
        st.divider()
        st.markdown("### Comparação de grupos (duas proporções)")
    
        small_cats = [c for c in cat_cols if dados[c].nunique()<=8]
        if not small_cats:
            st.warning("Não há colunas categóricas com até 8 categorias para comparar.")
        else:
            grp_col = st.selectbox("Escolha uma variável categórica para comparar", small_cats, index=0)
            sub = dados[[grp_col, "_target_"]].dropna().copy()
            order = sub[grp_col].value_counts().index.tolist()
            bars, ci_l, ci_u = [], [], []
            for lvl in order:
                s = sub.loc[sub[grp_col]==lvl, "_target_"]
                p = s.mean()
                low, high = proportion_confint(s.sum(), s.count(), alpha=0.05, method="wilson")
                bars.append(100*p); ci_l.append(100*low); ci_u.append(100*high)
    
            fig = go.Figure()
            fig.add_trace(go.Bar(x=order, y=bars, name="Taxa de conversão (%)"))
            fig.update_traces(error_y=dict(type="data", array=np.array(ci_u)-np.array(bars),
                                           arrayminus=np.array(bars)-np.array(ci_l)))
            fig.update_layout(title=f"Taxa de conversão por {grp_col} (IC95% Wilson)", yaxis_title="%")
            st.plotly_chart(fig, use_container_width=True)
    
            lvls = order[:]
            if len(lvls) >= 2:
                st.markdown("#### Teste Z para duas proporções")
                c1, c2 = st.columns(2)
                with c1:
                    a = st.selectbox("Grupo A", lvls, index=0)
                with c2:
                    b = st.selectbox("Grupo B", lvls, index=1)
    
                sA = sub.loc[sub[grp_col]==a, "_target_"]
                sB = sub.loc[sub[grp_col]==b, "_target_"]
                count = np.array([sA.sum(), sB.sum()])
                nobs  = np.array([sA.count(), sB.count()])
                zstat, pval = proportions_ztest(count, nobs, alternative="two-sided")
                pA, pB = sA.mean(), sB.mean()
                se = np.sqrt(pA*(1-pA)/nobs[0] + pB*(1-pB)/nobs[1])
                diff = pA - pB
                ci_d = (diff - 1.96*se, diff + 1.96*se)
    
                st.write(f"**H0**: p₍{a}₎ = p₍{b}₎  •  **H1**: p₍{a}₎ ≠ p₍{b}₎")
                st.write(f"Estatística Z = {zstat:.3f}  •  p-valor = {pval:.4g}")
                st.write(f"IC95% para (p₍{a}₎ − p₍{b}₎): {100*ci_d[0]:.2f}% a {100*ci_d[1]:.2f}%")
    
                alpha = 0.05
                if pval < alpha:
                    concl = f"Rejeitamos H0: a taxa de conversão difere entre **{a}** e **{b}** (p = {pval:.4g})."
                else:
                    concl = f"Não rejeitamos H0: não há evidência de diferença de conversão entre **{a}** e **{b}** (p = {pval:.4g})."
                st.success(concl)
    
            st.markdown("#### Teste de independência (Qui-quadrado)")
            tab = pd.crosstab(sub[grp_col], sub["_target_"])
            chi2, p_chi, dof, _ = stats.chi2_contingency(tab)
            st.write(f"**H0**: {grp_col} e conversão são independentes.")
            st.write(f"Qui² = {chi2:.3f}  •  gl = {dof}  •  p-valor = {p_chi:.4g}")
            if p_chi < 0.05:
                st.info(f"Rejeitamos H0: evidência de associação entre **{grp_col}** e conversão.")
            else:
                st.info(f"Não rejeitamos H0: sem evidência de associação entre **{grp_col}** e conversão.")
    
    # --------------------------
    # BLOCO B — MÉDIAS
    # --------------------------
    else:
        st.markdown("""
        **Justificativa**:  
        Para avaliar se clientes que **contrataram** vs **não contrataram** diferem em alguma **métrica contínua** (ex.: idade, saldo, duração da chamada), estimamos:
        - **IC 95% para a média** (assumindo amostra grande; pelo TCL o IC *t* é apropriado).  
        - **Teste t de Welch** para diferença de médias entre os grupos (não assume variâncias iguais).
        """)
    
        if not num_cols:
            st.warning("Não encontrei colunas numéricas para analisar.")
            st.stop()
    
        num_col = st.selectbox("Escolha a variável numérica", num_cols, index=0)
    
        sub = dados[[num_col, "_target_"]].dropna().copy()
        sub["grupo"] = np.where(sub["_target_"]==1, "Assinou", "Não assinou")
    
        def ci_mean(series, alpha=0.05):
            s = series.dropna()
            m = s.mean()
            se = stats.sem(s, nan_policy="omit")
            tcrit = stats.t.ppf(1 - alpha/2, df=len(s)-1)
            return m, (m - tcrit*se, m + tcrit*se)
    
        stats_g = sub.groupby("grupo")[num_col].apply(lambda s: pd.Series(ci_mean(s))).reset_index()
        stats_g[[num_col, "IC"]] = pd.DataFrame(stats_g[0].tolist(), index=stats_g.index)
        stats_g[["IC_low", "IC_high"]] = pd.DataFrame(stats_g["IC"].tolist(), index=stats_g.index)
        stats_g = stats_g[["grupo", num_col, "IC_low", "IC_high"]].rename(columns={num_col:"media"})
    
        cA, cB = st.columns(2)
        with cA:
            st.dataframe(stats_g, use_container_width=True)
        with cB:
            figm = go.Figure()
            figm.add_trace(go.Bar(x=stats_g["grupo"], y=stats_g["media"], name="Média"))
            figm.update_traces(error_y=dict(type="data",
                                            array=stats_g["IC_high"]-stats_g["media"],
                                            arrayminus=stats_g["media"]-stats_g["IC_low"]))
            figm.update_layout(title=f"Média de {num_col} por grupo (IC95%)", yaxis_title=num_col)
            st.plotly_chart(figm, use_container_width=True)
    
        x = sub.loc[sub["grupo"]=="Assinou", num_col]
        y = sub.loc[sub["grupo"]=="Não assinou", num_col]
        tstat, pval = stats.ttest_ind(x, y, equal_var=False, nan_policy="omit")
    
        nx, ny = x.count(), y.count()
        vx, vy = x.var(ddof=1), y.var(ddof=1)
        diff = x.mean() - y.mean()
        se = np.sqrt(vx/nx + vy/ny)
        df_w = (vx/nx + vy/ny)**2 / ((vx**2)/((nx**2)*(nx-1)) + (vy**2)/((ny**2)*(ny-1)))
        tcrit = stats.t.ppf(0.975, df=df_w)
        ci_diff = (diff - tcrit*se, diff + tcrit*se)
    
        st.markdown("#### Teste t de Welch — diferença de médias entre grupos")
        st.write(f"**H0**: μ(Assinou) = μ(Não assinou)  •  **H1**: μ(Assinou) ≠ μ(Não assinou)")
        st.write(f"t = {tstat:.3f}  •  gl ≈ {df_w:.1f}  •  p-valor = {pval:.4g}")
        st.write(f"IC95% para diferença de médias (Assinou − Não assinou): {ci_diff[0]:.3g} a {ci_diff[1]:.3g}")
    
        if pval < 0.05:
            st.success(f"Rejeitamos H0: a média de **{num_col}** difere entre quem assinou e quem não assinou (p = {pval:.4g}).")
        else:
            st.info(f"Não rejeitamos H0: não há evidência de diferença em **{num_col}** entre os grupos (p = {pval:.4g}).")
    
    # --------------------------
    # Observações finais (metodologia)
    # --------------------------
    with st.expander("Notas metodológicas (para o relatório)"):
        st.markdown("""
        - **IC de proporção (Wilson 95%)**: preferido ao Wald tradicional por ter melhor cobertura, especialmente quando p está longe de 0.5 ou amostras moderadas.
        - **Teste Z para duas proporções**: resposta binária, amostras independentes; usa aproximação normal (amostras grandes).
        - **Qui-quadrado de independência**: avalia associação entre a variável categórica e a conversão (tabela de contingência).
        - **IC da média e teste t de Welch**: apropriados para comparar médias com possíveis variâncias diferentes e amostras desbalanceadas.
        - Assumimos **independência entre observações** e que não há forte viés de seleção além do observado.
        """)
        
