import streamlit as st
from scripts.analise import * 
from scripts.classificador_ia import classificar_feedback_com_ia

st.set_page_config(page_title="Análise de Feedbacks | Protótipo", page_icon="⭐", layout="wide")

@st.cache_data
def carregar_dados_cached():
    return carregar_dados()

st.title("👨‍💻 Protótipo: Dashboard de Análise de Feedbacks")
df_original = carregar_dados_cached()

if df_original is None:
    st.error("Arquivo de dados não encontrado. Use a opção 'Gerar Novos Feedbacks' no menu `main.py`.")
else:
    # BARRA LATERAL DE FILTROS
    st.sidebar.header("Filtros Interativos")
    opcoes_setor = ['Todos'] + list(df_original['Setor'].unique())
    setor = st.sidebar.selectbox("Selecione o Setor:", options=opcoes_setor)
    if setor != 'Todos':
        df_filtrado = df_original[df_original['Setor'] == setor].copy()
    else:
        df_filtrado = df_original.copy()
    opcoes_loja = ['Todas'] + list(df_filtrado['Local_Loja'].unique())
    loja = st.sidebar.selectbox("Selecione a Loja/Hotel:", options=opcoes_loja)
    if loja != 'Todas':
        df_filtrado = df_filtrado[df_filtrado['Local_Loja'] == loja].copy()

    # CORPO DA PÁGINA COM ABAS
    tab_geral, tab_criticos, tab_fortes, tab_ia = st.tabs(["📊 Visão Geral", "🔥 Pontos Críticos", "💡 Pontos Fortes", "🤖 Análise Preditiva e IA"])

    with tab_geral:
        st.header("O Pulso do Negócio")
        if not df_filtrado.empty:
            col1, col2, col3 = st.columns(3)
            col1.metric("Total de Feedbacks", f"{len(df_filtrado):,}")
            col2.metric("Rating Médio", f"{df_filtrado['Rating'].mean():.2f} ⭐")
            col3.metric("Feedbacks Negativos", f"{(df_filtrado['Sentimento'] == 'Negativo').sum():,}")
            st.divider()

            st.subheader("Índice de Saúde por Loja/Hotel")
            health_scores_df, fig_health = calcular_e_exibir_health_score(df_filtrado)
            if health_scores_df is not None:
                col_tabela, col_grafico = st.columns([1, 2])
                with col_tabela: st.dataframe(health_scores_df, use_container_width=True, hide_index=True)
                with col_grafico: st.pyplot(fig_health)
            else:
                st.warning("Dados insuficientes para calcular o Health Score.")
            st.divider()

            # Gráficos de Tendência Lado a Lado
            st.subheader("Variação da Satisfação no Tempo")
            col_semanal, col_mensal = st.columns(2)
            with col_semanal:
                st.markdown("###### Por Dia da Semana")
                fig_semana = plotar_rating_por_dia_semana(df_filtrado)
                if fig_semana: st.pyplot(fig_semana)
            with col_mensal:
                st.markdown("###### Por Mês")
                fig_mes = plotar_tendencia_rating_mensal(df_filtrado)
                if fig_mes: st.pyplot(fig_mes)
        else:
            st.warning("Nenhum dado encontrado para os filtros selecionados.")

    with tab_criticos:
        st.header("Análise Profunda dos Problemas")
        if not df_filtrado[df_filtrado['Sentimento'] == 'Negativo'].empty:
            fig_pareto = plotar_grafico_pareto(df_filtrado)
            if fig_pareto: st.subheader("Gráfico de Pareto das Reclamações"); st.pyplot(fig_pareto)
            
            # Análises de Causa Raiz Lado a Lado
            st.divider()
            col_termos, col_calor = st.columns(2)
            with col_termos:
                st.subheader("Termos Mais Comuns em Reclamações")
                df_termos = analisar_principais_termos_negativos(df_filtrado)
                if df_termos is not None: st.dataframe(df_termos, hide_index=True)
                else: st.info("Sem dados para análise de termos.")
            with col_calor:
                st.subheader("Mapa de Calor (Loja vs. Problema)")
                fig_calor = plotar_mapa_calor_problemas_loja(df_filtrado)
                if fig_calor: st.pyplot(fig_calor)
                else: st.info("Sem dados para o mapa de calor.")
            st.divider()
            
            fig_canal = plotar_problemas_por_canal(df_filtrado)
            if fig_canal: st.subheader("Perfil de Problemas por Canal"); st.pyplot(fig_canal)
        else:
            st.info("Ótima notícia! Nenhum feedback negativo encontrado para os filtros selecionados.")

    with tab_fortes:
        st.header("Identificando o que Funciona para Replicar o Sucesso")
        if not df_filtrado[df_filtrado['Sentimento'] == 'Positivo'].empty:
            col_elogios, col_quadro = st.columns(2)
            with col_elogios:
                st.subheader("Principais Motivos de Elogio")
                df_fortes = analisar_pontos_fortes(df_filtrado)
                if df_fortes is not None: st.dataframe(df_fortes, hide_index=True, use_container_width=True)
                else: st.info("Não há feedbacks positivos com subcategoria para analisar.")
            with col_quadro:
                st.subheader("Quadro de Honra dos Funcionários")
                df_quadro_honra = criar_quadro_honra(df_filtrado)
                if df_quadro_honra is not None: st.dataframe(df_quadro_honra, hide_index=True, use_container_width=True)
                else: st.info("Nenhum funcionário foi elogiado.")
        else:
            st.info("Nenhum feedback positivo encontrado para os filtros selecionados.")

    with tab_ia:
        st.header("Análise Preditiva e Demonstração da IA")
        
        # Relatório do Treinamento do Modelo
        st.subheader("Performance do Modelo de Previsão de Urgência")
        with st.spinner("Treinando modelo de IA..."):
            modelo, vetorizador, relatorio = treinar_e_avaliar_modelo_urgencia(df_original)
        if relatorio:
            with st.expander("Ver Relatório de Classificação do Modelo"):
                st.text(relatorio)
        else:
            st.warning("Não foi possível treinar o modelo (dados insuficientes).")
        st.divider()

        st.subheader("Teste a Classificação da IA em Tempo Real")
        texto_usuario = st.text_area("Digite um feedback aqui:", "O atendimento na recepção foi lento, mas o quarto era muito confortável.", height=100)
        setor_ia = st.radio("Selecione o setor para o feedback:", df_original['Setor'].unique(), horizontal=True)
        if st.button("Analisar Feedback com IA", type="primary"):
            if texto_usuario:
                with st.spinner("Analisando..."):
                    resultado = classificar_feedback_com_ia(texto_usuario, setor_ia)
                    if resultado: st.success("Feedback classificado!"); st.json(resultado)
                    else: st.error("Erro ao classificar. A API pode estar indisponível.")
            else:
                st.warning("Por favor, digite um texto para ser analisado.")