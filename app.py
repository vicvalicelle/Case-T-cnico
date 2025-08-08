# app.py

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Importa as funções que você já criou e refatorou nos seus módulos
# Esta é a forma correta de importar quando 'app.py' está na raiz do projeto
from scripts import config
from scripts.dashboard import (
    carregar_dados,
    plotar_grafico_pareto,
    plotar_mapa_calor,
    plotar_rating_por_dia_semana,
    plotar_problemas_por_canal,
    calcular_e_exibir_health_score,
    analisar_pontos_fortes,
    criar_quadro_honra
)
from scripts.classificador_ia import classificar_feedback_com_ia

# --- Configuração da Página ---
# Define o título, ícone e layout da página. Deve ser o primeiro comando do Streamlit.
st.set_page_config(
    page_title="Análise de Feedbacks | Protótipo",
    page_icon="⭐",
    layout="wide"
)

# --- Caching de Dados ---
# O decorator @st.cache_data garante que os dados sejam carregados apenas uma vez,
# tornando o app muito mais rápido após a primeira carga.
@st.cache_data
def carregar_dados_cached():
    df = carregar_dados()
    return df

# --- Título e Carregamento dos Dados ---
st.title("👨‍💻 Protótipo: Dashboard de Análise de Feedbacks")
st.markdown("Esta aplicação interativa demonstra como a análise de dados e a IA podem transformar feedbacks de clientes em insights acionáveis para a sua marca.")

df_original = carregar_dados_cached()

# Se o carregamento de dados falhar, exibe um erro e para a execução.
if df_original is None:
    st.error("Não foi possível carregar os dados. Verifique o caminho e o nome do arquivo CSV em `config.py`.")
else:
    # --- Barra Lateral de Filtros ---
    st.sidebar.header("Filtros Interativos")
    
    # Cria uma lista de opções para o seletor de setor, incluindo 'Todos'
    opcoes_setor = ['Todos'] + list(df_original['Setor'].unique())
    setor = st.sidebar.selectbox(
        "Selecione o Setor:", 
        options=opcoes_setor,
        index=0 
    )

    # Filtra o dataframe principal com base na seleção do setor
    if setor != 'Todos':
        df_filtrado = df_original[df_original['Setor'] == setor].copy()
    else:
        df_filtrado = df_original.copy()

    # As opções de loja/hotel mudam dinamicamente com base no setor selecionado
    opcoes_loja = ['Todas'] + list(df_filtrado['Local_Loja'].unique())
    loja = st.sidebar.selectbox(
        "Selecione a Loja/Hotel:",
        options=opcoes_loja,
        index=0
    )

    # Aplica o segundo filtro de loja/hotel
    if loja != 'Todas':
        df_filtrado = df_filtrado[df_filtrado['Local_Loja'] == loja].copy()

    # --- Corpo da Página com Abas ---
    # Cria a estrutura de abas para organizar a informação
    tab_geral, tab_criticos, tab_fortes, tab_ia = st.tabs(["📊 Visão Geral", "🔥 Pontos Críticos", "💡 Pontos Fortes", "🤖 Demo da IA"])

    # --- Conteúdo da Aba 1: Visão Geral ---
    with tab_geral:
        st.header("O Pulso do Negócio")
        
        if not df_filtrado.empty:
            # Exibe os KPIs principais em colunas
            col1, col2, col3 = st.columns(3)
            col1.metric("Total de Feedbacks Analisados", f"{len(df_filtrado):,}")
            col2.metric("Rating Médio Geral", f"{df_filtrado['Rating'].mean():.2f} ⭐")
            col3.metric("Feedbacks Negativos", f"{(df_filtrado['Sentimento'] == 'Negativo').sum():,}")

            st.divider()

            st.subheader("Índice de Saúde por Loja/Hotel")
            health_scores_df, fig_health_score = calcular_e_exibir_health_score(df_filtrado)
            if health_scores_df is not None and fig_health_score is not None:
                # Exibe a tabela e o gráfico lado a lado
                col_tabela, col_grafico = st.columns([1, 2])
                with col_tabela:
                    st.dataframe(health_scores_df, use_container_width=True, hide_index=True)
                with col_grafico:
                    st.pyplot(fig_health_score)
            else:
                st.warning("Não há dados suficientes nos filtros selecionados para calcular o Health Score (cada loja precisa de pelo menos 3 feedbacks).")

            # --- ADICIONADO: Gráfico de satisfação por dia da semana ---
            st.divider()
            st.subheader("Variação da Satisfação Durante a Semana")
            fig_semana = plotar_rating_por_dia_semana(df_filtrado)
            if fig_semana:
                st.pyplot(fig_semana)
            else:
                st.info("Não há dados suficientes para exibir o gráfico de satisfação semanal.")
            # --- FIM DA ADIÇÃO ---

        else:
            st.warning("Nenhum dado encontrado para os filtros selecionados.")

    # --- Conteúdo da Aba 2: Pontos Críticos ---
    with tab_criticos:
        st.header("Análise Profunda dos Problemas")
        st.markdown("Identifique as principais causas de insatisfação para focar os esforços de melhoria onde realmente importa.")

        if not df_filtrado[df_filtrado['Sentimento'] == 'Negativo'].empty:
            # Gráfico de Pareto
            fig_pareto = plotar_grafico_pareto(df_filtrado)
            if fig_pareto:
                st.subheader("Gráfico de Pareto das Reclamações")
                st.pyplot(fig_pareto)
            
            # Mapa de Calor
            fig_calor = plotar_mapa_calor(df_filtrado)
            if fig_calor:
                st.subheader("Mapa de Calor (Loja vs. Problema)")
                st.pyplot(fig_calor)

            # --- ADICIONADO: Gráfico de problemas por canal ---
            fig_canal = plotar_problemas_por_canal(df_filtrado)
            if fig_canal:
                st.subheader("Perfil de Problemas por Canal de Comunicação")
                st.pyplot(fig_canal)
            # --- FIM DA ADIÇÃO ---
            
        else:
            st.info("Ótima notícia! Nenhum feedback negativo encontrado para os filtros selecionados.")
            
    # --- Conteúdo da Aba 3: Pontos Fortes ---
    with tab_fortes:
        st.header("Identificando o que Funciona para Replicar o Sucesso")
        
        if not df_filtrado[df_filtrado['Sentimento'] == 'Positivo'].empty:
            col_elogios, col_quadro = st.columns(2)

            with col_elogios:
                st.subheader("Principais Motivos de Elogio")
                df_fortes = analisar_pontos_fortes(df_filtrado)
                if df_fortes is not None:
                    st.dataframe(df_fortes, hide_index=True, use_container_width=True)
                else:
                    st.info("Não há feedbacks positivos com subcategoria para analisar.")

            with col_quadro:
                st.subheader("Quadro de Honra dos Funcionários")
                df_quadro_honra = criar_quadro_honra(df_filtrado)
                if df_quadro_honra is not None:
                    st.dataframe(df_quadro_honra, hide_index=True, use_container_width=True)
                else:
                    st.info("Nenhum funcionário foi elogiado nos feedbacks filtrados.")
        else:
            st.info("Nenhum feedback positivo encontrado para os filtros selecionados.")


    # --- Conteúdo da Aba 4: Demo da IA ---
    with tab_ia:
        st.header("Teste a Classificação da IA em Tempo Real")
        st.markdown("Escreva um feedback e veja como nosso sistema o classifica automaticamente em segundos.")
        
        texto_usuario = st.text_area(
            "Digite um feedback aqui:", 
            "O atendimento na recepção foi lento, mas o quarto era muito confortável.",
            height=150
        )
        setor_ia = st.radio("Selecione o setor para o feedback:", df_original['Setor'].unique(), horizontal=True)
        
        if st.button("Analisar Feedback com IA", type="primary"):
            if texto_usuario:
                with st.spinner("Analisando o feedback... A IA está trabalhando!"):
                    resultado = classificar_feedback_com_ia(texto_usuario, setor_ia)
                    if resultado:
                        st.success("Feedback classificado com sucesso!")
                        st.json(resultado)
                    else:
                        st.error("Ocorreu um erro ao classificar. A API pode estar indisponível. Tente novamente.")
            else:
                st.warning("Por favor, digite um texto para ser analisado.")