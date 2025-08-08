import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import seaborn as sns
import os
from . import config 

# Type Hinting para clareza
from typing import Optional, Tuple

# bibliotecas de IA
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report

# LÓGICA DE DADOS
def carregar_dados() -> Optional[pd.DataFrame]:
    """Carrega e prepara os dados do CSV."""
    try:
        df = pd.read_csv(config.NOME_ARQUIVO_CSV, sep=';', encoding='utf-8')
        df[config.COLS.DATA] = pd.to_datetime(df[config.COLS.DATA], errors='coerce')
        df[config.COLS.RATING] = pd.to_numeric(df[config.COLS.RATING], errors='coerce')
        
        # Garante que todas as colunas necessárias existam
        colunas_necessarias = [getattr(config.COLS, attr) for attr in dir(config.COLS) if not attr.startswith('__')]
        for col in colunas_necessarias:
            if col not in df.columns:
                df[col] = None
                
        return df.dropna(subset=[config.COLS.DATA, config.COLS.RATING])
    except FileNotFoundError:
        return None

# FUNÇÕES DE ANÁLISE (TEXTUAL)
def analisar_kpis_gerais(df):
    avg_rating = df['Rating'].mean()
    sentiment_distribution = df['Sentimento'].value_counts(normalize=True).mul(100)
    print("\n--- [1.1] KPIs Gerais ---")
    print(f"📊 Índice de Satisfação Médio (Rating): {avg_rating:.2f} de 5")
    print("📊 Distribuição de Sentimento:"); print(sentiment_distribution.round(2).to_string())

def analisar_pontos_fortes(df: pd.DataFrame) -> Optional[pd.DataFrame]:
    """Retorna um DataFrame com as subcategorias mais elogiadas."""
    df_positivo = df[(df[config.COLS.SENTIMENTO] == config.SENTIMENTS.POS) & (df[config.COLS.SUBCATEGORIA].notna())].copy()
    if df_positivo.empty: return None
    
    pontos_fortes = df_positivo[config.COLS.SUBCATEGORIA].value_counts().head(10).reset_index()
    pontos_fortes.columns = ['Subcategoria', 'Quantidade de Elogios']
    return pontos_fortes

def criar_quadro_honra(df: pd.DataFrame) -> Optional[pd.DataFrame]:
    """Retorna um DataFrame com o ranking de funcionários elogiados."""
    df_funcionarios = df[(df[config.COLS.SENTIMENTO] == config.SENTIMENTS.POS) & (df[config.COLS.FUNCIONARIO].notna()) & (df[config.COLS.FUNCIONARIO] != 'Não')].copy()
    if df_funcionarios.empty: return None
    
    quadro_honra = df_funcionarios.groupby(config.COLS.FUNCIONARIO).agg(
        Qtd_Elogios=(config.COLS.ID, 'count'), 
        Rating_Medio=(config.COLS.RATING, 'mean')
    ).sort_values(by='Qtd_Elogios', ascending=False).reset_index()
    quadro_honra['Rating_Medio'] = quadro_honra['Rating_Medio'].round(2)
    return quadro_honra

# FUNÇÕES DE PLOTAGEM (GRÁFICOS)
def plotar_tendencia_rating_mensal(df: pd.DataFrame) -> Optional[plt.Figure]:
    """Gera um gráfico da tendência mensal do rating."""
    df_temporal = df.set_index(config.COLS.DATA).copy()
    rating_mensal = df_temporal[config.COLS.RATING].resample('ME').mean()
    
    fig, ax = plt.subplots(figsize=config.FIGSIZE_PADRAO)
    ax.plot(rating_mensal.index, rating_mensal, marker='o', linestyle='-')
    ax.set_title('Tendência de Satisfação (Rating Médio Mensal)')
    ax.set_ylabel('Rating Médio'); ax.set_xlabel('Mês')
    ax.set_ylim(1, 5)
    ax.grid(True, linestyle='--')
    fig.tight_layout()
    return fig

def plotar_grafico_pareto(df: pd.DataFrame) -> Optional[plt.Figure]:
    """Gera um gráfico de Pareto para as causas de reclamações."""
    df_negativo = df[(df[config.COLS.SENTIMENTO] == config.SENTIMENTS.NEG) & (df[config.COLS.SUBCATEGORIA].notna())]
    if df_negativo.empty: return None

    contagem = df_negativo[config.COLS.SUBCATEGORIA].value_counts().reset_index()
    contagem.columns = ['Subcategoria', 'Contagem']
    contagem['Percentual_Acumulado'] = (contagem['Contagem'].cumsum() / contagem['Contagem'].sum()) * 100
    
    fig, ax1 = plt.subplots(figsize=config.FIGSIZE_GRANDE)
    sns.barplot(data=contagem, x='Subcategoria', y='Contagem', color='cornflowerblue', ax=ax1)
    ax1.set_xlabel('Causa do Problema'); ax1.set_ylabel('Ocorrências', color='cornflowerblue')
    ax1.tick_params(axis='x', rotation=45)

    ax2 = ax1.twinx()
    sns.lineplot(data=contagem, x='Subcategoria', y='Percentual_Acumulado', color='crimson', marker='o', sort=False, ax=ax2)
    ax2.set_ylabel('Percentual Acumulado (%)', color='crimson')
    ax2.yaxis.set_major_formatter(mtick.PercentFormatter(xmax=100.0))
    ax2.set_ylim(0, 110)

    ax1.set_title('Análise de Pareto: Principais Causas de Reclamações')
    fig.tight_layout()
    return fig

def plotar_mapa_calor_problemas_loja(df: pd.DataFrame) -> Optional[plt.Figure]:
    """
    Gera um mapa de calor mostrando a relação entre unidades e subcategorias de problemas.
    """
    df_negativo = df[
        (df[config.COLS.SENTIMENTO] == config.SENTIMENTS.NEG) &
        (df[config.COLS.SUBCATEGORIA].notna()) &
        (df[config.COLS.LOCAL].notna())
    ].copy()

    if df_negativo.empty or len(df_negativo[config.COLS.LOCAL].unique()) < 2:
        return None
    
    crosstab = pd.crosstab(df_negativo[config.COLS.LOCAL], df_negativo[config.COLS.SUBCATEGORIA])
    
    fig, ax = plt.subplots(figsize=config.FIGSIZE_GRANDE)
    sns.heatmap(crosstab, annot=True, fmt='d', cmap='Reds', linewidths=.5, ax=ax)
    ax.set_title('Mapa de Calor: Ocorrências de Problemas por Unidade', fontsize=16)
    ax.set_xlabel('Subcategoria do Problema')
    ax.set_ylabel('Unidade')
    plt.setp(ax.get_xticklabels(), rotation=30, ha="right")
    fig.tight_layout()
    return fig

def plotar_rating_por_dia_semana(df: pd.DataFrame) -> Optional[plt.Figure]:
    """
    Gera um gráfico de linha da média de satisfação por dia da semana.
    """
    if df.empty or config.COLS.DATA not in df.columns:
        return None
        
    df_copy = df.copy()
    df_copy['Dia_Semana'] = df_copy[config.COLS.DATA].dt.day_name()
    
    rating_por_dia = df_copy.groupby('Dia_Semana')[config.COLS.RATING].mean().reindex(config.DIAS_SEMANA_ORDEM)
    rating_por_dia.index = rating_por_dia.index.map(config.DIAS_SEMANA_PT)
    
    fig, ax = plt.subplots(figsize=config.FIGSIZE_PADRAO)
    rating_por_dia.plot(kind='line', marker='o', linestyle='--', color='indigo', ax=ax)
    ax.set_title('Média de Satisfação por Dia da Semana', fontsize=16)
    ax.set_xlabel('Dia da Semana')
    ax.set_ylabel('Rating Médio (1-5)')
    ax.set_ylim(1, 5)
    ax.grid(True, linestyle='--')
    fig.tight_layout()
    return fig

def plotar_problemas_por_canal(df: pd.DataFrame) -> Optional[plt.Figure]:
    """
    Gera gráficos de barras dos problemas por categoria para cada canal.
    """

    df_negativo = df[
        (df[config.COLS.SENTIMENTO] == config.SENTIMENTS.NEG) &
        (df[config.COLS.CATEGORIA].notna())
    ].copy()

    if df_negativo.empty or config.COLS.CANAL not in df_negativo.columns:
        return None
        
    g = sns.catplot(
        data=df_negativo, 
        y=config.COLS.CATEGORIA, 
        col=config.COLS.CANAL, 
        col_wrap=3,
        kind='count', 
        palette=config.PALETA_PROBLEMAS_CANAL, 
        sharex=False,
        height=5,
        aspect=1.2
    )
    g.fig.suptitle('Perfil de Problemas por Canal de Comunicação', y=1.03, fontsize=16)
    g.set_titles("Canal: {col_name}")
    g.set_xlabels("Nº de Reclamações")
    g.set_ylabels("Categoria do Problema")
    plt.tight_layout(rect=[0, 0, 1, 0.97])
    return g.fig

def calcular_e_exibir_health_score(df: pd.DataFrame) -> Optional[Tuple[pd.DataFrame, plt.Figure]]:
    """
    Calcula e plota o Health Score para cada unidade.
    """
    resultados = []
    pesos = config.PESOS_HEALTH_SCORE

    for loja in df[config.COLS.LOCAL].unique():
        df_loja = df[df[config.COLS.LOCAL] == loja]
        if len(df_loja) < 3:
            continue

        rating_norm = (df_loja[config.COLS.RATING].mean() - 1) / 4
        pct_negativo = (df_loja[config.COLS.SENTIMENTO] == config.SENTIMENTS.NEG).sum() / len(df_loja)
        pct_urg_alta = (df_loja[config.COLS.URGENCIA] == config.URGENCIA.ALTA).sum() / len(df_loja)
        
        score = (pesos['rating'] * rating_norm) - (pesos['negativo'] * pct_negativo) - (pesos['urgencia'] * pct_urg_alta)
        resultados.append({'Loja/Hotel': loja, 'Health_Score': score * 100})

    if not resultados:
        return None, None

    health_scores = pd.DataFrame(resultados).sort_values(by='Health_Score', ascending=False).round(2)
    
    fig, ax = plt.subplots(figsize=config.FIGSIZE_GRANDE)
    sns.barplot(data=health_scores, x='Health_Score', y='Loja/Hotel', palette=config.PALETA_HEALTH_SCORE, hue='Loja/Hotel', legend=False, ax=ax)
    ax.set_title('Ranking de Saúde por Loja/Hotel', fontsize=16)
    ax.set_xlabel('Health Score (quanto maior, melhor)')
    ax.set_ylabel('Loja / Hotel')
    fig.tight_layout()
    return health_scores, fig

# FUNÇÕES DE ANÁLISE DIAGNÓSTICA E PREDITIVA
def analisar_principais_termos_negativos(df: pd.DataFrame, n_termos: int = 15) -> Optional[pd.DataFrame]:
    """
    Extrai os termos (n-gramas) mais comuns de feedbacks negativos.
    """
    textos_negativos = df[df[config.COLS.SENTIMENTO] == config.SENTIMENTS.NEG][config.COLS.TEXTO].dropna()
    if textos_negativos.empty:
        return None
        
    try:
        vec = CountVectorizer(ngram_range=(2, 3), stop_words=['de', 'a', 'o', 'que', 'e', 'do', 'da', 'em', 'um']).fit(textos_negativos)
        sum_words = vec.transform(textos_negativos).sum(axis=0)
        words_freq = sorted([(word, sum_words[0, idx]) for word, idx in vec.vocabulary_.items()], key=lambda x: x[1], reverse=True)
        return pd.DataFrame(words_freq[:n_termos], columns=['Termo Específico', 'Frequência'])
    except Exception:
        return None

def plotar_matriz_correlacao(df: pd.DataFrame) -> Optional[plt.Figure]:
    """
    Cria um mapa de calor com as correlações entre as métricas numéricas.
    """
    df_corr = df.copy()
    
    mapa_sentimento = {config.SENTIMENTS.POS: 1, config.SENTIMENTS.NEUTRO: 0, config.SENTIMENTS.NEG: -1}
    mapa_urgencia = {config.URGENCIA.ALTA: 3, config.URGENCIA.MEDIA: 2, config.URGENCIA.BAIXA: 1}
    
    df_corr['Sentimento_Num'] = df_corr[config.COLS.SENTIMENTO].map(mapa_sentimento)
    df_corr['Urgencia_Num'] = df_corr[config.COLS.URGENCIA].map(mapa_urgencia)
    
    colunas_numericas = df_corr.select_dtypes(include=['number']).columns
    if len(colunas_numericas) < 2:
        return None
        
    correlacoes = df_corr[colunas_numericas].corr()
    
    fig, ax = plt.subplots(figsize=config.FIGSIZE_GRANDE)
    sns.heatmap(correlacoes, annot=True, cmap='coolwarm', fmt=".2f", linewidths=.5, ax=ax)
    ax.set_title('Matriz de Correlação das Métricas', fontsize=16)
    fig.tight_layout()
    return fig

def treinar_e_avaliar_modelo_urgencia(df: pd.DataFrame) -> Optional[Tuple[object, object, str]]:
    """
    Treina um modelo para prever a 'Urgencia' com base no texto.
    Retorna o modelo, o vetorizador e o relatório de classificação.
    """

    df_modelo = df[[config.COLS.TEXTO, config.COLS.URGENCIA]].dropna()
    
    if len(df_modelo[config.COLS.URGENCIA].unique()) < 2 or len(df_modelo) < 50:
        return None, None, None

    X_train, X_test, y_train, y_test = train_test_split(
        df_modelo[config.COLS.TEXTO], 
        df_modelo[config.COLS.URGENCIA], 
        test_size=0.25, 
        random_state=42, 
        stratify=df_modelo[config.COLS.URGENCIA]
    )
    
    tfidf = TfidfVectorizer(max_features=2000, ngram_range=(1,2)).fit(X_train)
    X_train_tfidf = tfidf.transform(X_train)
    X_test_tfidf = tfidf.transform(X_test)
    
    model = LogisticRegression(multi_class='ovr', solver='liblinear', class_weight='balanced').fit(X_train_tfidf, y_train)
    
    report = classification_report(y_test, model.predict(X_test_tfidf))
    return model, tfidf, report

# FUNÇÃO PRINCIPAL PARA RELATÓRIO ESTÁTICO
def executar_analise_completa():
    """Orquestra a geração completa do relatório de análise estática."""
    print("--- INICIANDO GERAÇÃO DE RELATÓRIO ESTÁTICO ---")
    if not os.path.exists(config.PASTA_GRAFICOS):
        os.makedirs(config.PASTA_GRAFICOS)
    
    df = carregar_dados()
    if df is None:
        print("\nAnálise interrompida: dados não carregados.")
        return

    # análises textuais
    print("\n--- [1.2] Principais Pontos Fortes ---")
    df_fortes = analisar_pontos_fortes(df)
    print(df_fortes.to_string(index=False) if df_fortes is not None else "N/A")
    
    print("\n--- [1.3] Quadro de Honra ---")
    df_honra = criar_quadro_honra(df)
    print(df_honra.to_string(index=False) if df_honra is not None else "N/A")
    
    # gráficos
    print("\nGerando e salvando gráficos...")
    graficos_a_gerar = {
        '01_tendencia_mensal.png': plotar_tendencia_rating_mensal,
        '02_pareto_reclamacoes.png': plotar_grafico_pareto,
        '03_mapa_calor_problemas.png': plotar_mapa_calor_problemas_loja,
        '04_correlacao.png': plotar_matriz_correlacao
    }
    for nome_arquivo, funcao_plotagem in graficos_a_gerar.items():
        figura = funcao_plotagem(df)
        if figura:
            figura.savefig(os.path.join(config.PASTA_GRAFICOS, nome_arquivo))
            plt.close(figura)

    print(f"\n✅ Análise concluída! Gráficos salvos em: '{config.PASTA_GRAFICOS}'")

if __name__ == '__main__':
    executar_analise_completa()