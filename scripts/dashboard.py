import pandas as pd
import matplotlib
matplotlib.use('TkAgg') 
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import seaborn as sns
from . import config

# --- Funções de Lógica de Dados ---
def carregar_dados():
    """Carrega e prepara os dados do CSV."""
    try:
        df = pd.read_csv(config.NOME_ARQUIVO_CSV, sep=';', encoding='utf-8')
        df['Data'] = pd.to_datetime(df['Data'])
        df['Rating'] = pd.to_numeric(df['Rating'])
        print(f"✅ Arquivo carregado com sucesso de: {config.NOME_ARQUIVO_CSV}")
        return df
    except FileNotFoundError:
        print(f"❌ ERRO: Arquivo '{config.NOME_ARQUIVO_CSV}' não encontrado.")
        return None

# --- Funções de Visualização (cada gráfico vira uma função) ---

def plotar_kpis_gerais(df):
    avg_rating = df['Rating'].mean()
    if 'Sentimento' in df.columns:
        sentiment_distribution = df['Sentimento'].value_counts(normalize=True) * 100
        print("\n[1. KPIs Gerais]")
        print(f"Índice de Satisfação Médio (Rating): {avg_rating:.2f} de 5")
        print("Distribuição de Sentimento:")
        print(sentiment_distribution.round(2).to_string())

def plotar_grafico_pareto(df):
    df_negativo = df[(df['Sentimento'] == 'Negativo') & (df['Subcategoria'].notna())].copy()
    if df_negativo.empty:
        print("Aviso: Nenhum feedback negativo com subcategoria para gerar o Gráfico de Pareto.")
        return None
        
    contagem_subcat = df_negativo['Subcategoria'].value_counts().reset_index()
    contagem_subcat.columns = ['Subcategoria', 'Contagem']
    contagem_subcat['Percentual_Acumulado'] = (contagem_subcat['Contagem'].cumsum() / contagem_subcat['Contagem'].sum()) * 100
    
    fig, ax1 = plt.subplots(figsize=config.FIGSIZE_GRANDE)
    ax1.bar(contagem_subcat['Subcategoria'], contagem_subcat['Contagem'], color='cornflowerblue')
    ax1.set_xlabel('Subcategoria do Problema', fontsize=12)
    ax1.set_ylabel('Número de Ocorrências', color='cornflowerblue', fontsize=12)
    plt.xticks(rotation=45, ha="right")

    ax2 = ax1.twinx()
    ax2.plot(contagem_subcat['Subcategoria'], contagem_subcat['Percentual_Acumulado'], color='crimson', marker='o', ms=5)
    ax2.set_ylabel('Percentual Acumulado (%)', color='crimson', fontsize=12)
    ax2.yaxis.set_major_formatter(mtick.PercentFormatter(xmax=100.0))
    
    ax1.set_title('Gráfico de Pareto: Causas Principais de Reclamações', fontsize=16)
    fig.tight_layout()
    return fig

def plotar_mapa_calor(df):
    df_negativo = df[(df['Sentimento'] == 'Negativo') & (df['Subcategoria'].notna())].copy()
    if df_negativo.empty:
        return None
        
    crosstab_loja_problema = pd.crosstab(df_negativo['Local_Loja'], df_negativo['Subcategoria'])
    
    fig, ax = plt.subplots(figsize=config.FIGSIZE_GRANDE)
    sns.heatmap(crosstab_loja_problema, annot=True, fmt='d', cmap='Reds', linewidths=.5, ax=ax)
    ax.set_title('Mapa de Calor: Ocorrências de Problemas por Loja/Hotel', fontsize=16)
    ax.set_xlabel('Subcategoria do Problema')
    ax.set_ylabel('Loja / Hotel')
    plt.setp(ax.get_xticklabels(), rotation=30, ha="right")
    plt.setp(ax.get_yticklabels(), rotation=0)
    fig.tight_layout()
    return fig

def plotar_rating_por_dia_semana(df):
    df['Dia_Semana'] = df['Data'].dt.day_name()
    rating_por_dia = df.groupby('Dia_Semana')['Rating'].mean().reindex(config.DIAS_SEMANA_ORDEM)
    rating_por_dia.index = rating_por_dia.index.map(config.DIAS_SEMANA_PT)
    
    fig, ax = plt.subplots(figsize=config.FIGSIZE_PADRAO)
    rating_por_dia.plot(kind='line', marker='o', linestyle='--', color='indigo', ax=ax)
    ax.set_title('Média de Satisfação por Dia da Semana', fontsize=16)
    ax.set_xlabel('Dia da Semana')
    ax.set_ylabel('Rating Médio (1-5)')
    ax.set_ylim(1, 5)
    ax.grid(True, which='both', linestyle='--', linewidth=0.5)
    fig.tight_layout()
    return fig

def plotar_problemas_por_canal(df):
    df_negativo = df[(df['Sentimento'] == 'Negativo') & (df['Categoria'].notna())].copy()
    if df_negativo.empty:
        return None
    
    g = sns.catplot(data=df_negativo, y='Categoria', col='Canal', col_wrap=3, 
                    kind='count', palette=config.PALETA_PROBLEMAS_CANAL, sharex=False, height=5, aspect=1.2)
    g.fig.suptitle('Perfil de Problemas por Canal de Comunicação', y=1.03, fontsize=16)
    g.set_titles("Canal: {col_name}")
    g.set_xlabels("Número de Reclamações")
    g.set_ylabels("Categoria do Problema")
    plt.tight_layout()
    return g.fig

def calcular_e_exibir_health_score(df):
    resultados = []
    pesos = config.PESOS_HEALTH_SCORE

    for loja in df['Local_Loja'].unique():
        df_loja = df[df['Local_Loja'] == loja]
        if len(df_loja) < 3: continue

        rating_norm = (df_loja['Rating'].mean() - 1) / 4
        pct_negativo = (df_loja['Sentimento'] == 'Negativo').sum() / len(df_loja)
        pct_urg_alta = (df_loja['Urgencia'] == 'Alta').sum() / len(df_loja)
        
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

def analisar_pontos_fortes(df):
    df_positivo = df[(df['Sentimento'] == 'Positivo') & (df['Subcategoria'].notna())].copy()
    if df_positivo.empty:
        return None
    
    pontos_fortes = df_positivo['Subcategoria'].value_counts().head(10).reset_index()
    pontos_fortes.columns = ['Subcategoria', 'Quantidade de Elogios']
    return pontos_fortes

def criar_quadro_honra(df):
    df_funcionarios = df[(df['Sentimento'] == 'Positivo') & (df['Menciona_Empregado'] != 'Não')].copy()
    if df_funcionarios.empty:
        return None
        
    quadro_honra = df_funcionarios.groupby('Menciona_Empregado').agg(
        Qtd_Elogios=('ID', 'count'),
        Rating_Medio=('Rating', 'mean')
    ).sort_values(by='Qtd_Elogios', ascending=False).reset_index()
    
    quadro_honra['Rating_Medio'] = quadro_honra['Rating_Medio'].round(2)
    return quadro_honra

def main():
    """Função principal que orquestra a geração do dashboard no modo script."""
    print("--- INICIANDO GERAÇÃO DO DASHBOARD (MODO SCRIPT) ---")
    df = carregar_dados()
    
    if df is not None:
        # Imprime os resultados de todas as análises textuais
        plotar_kpis_gerais(df)
        
        print("\n--- Quadro de Honra dos Funcionários ---")
        quadro_df = criar_quadro_honra(df)
        if quadro_df is not None:
            print(quadro_df.to_string(index=False))

        print("\n--- Principais Pontos Fortes (Motivos de Elogio) ---")
        fortes_df = analisar_pontos_fortes(df)
        if fortes_df is not None:
            print(fortes_df.to_string(index=False))

        # Corrigido para capturar a figura do health score
        health_scores_df, fig_health_score = calcular_e_exibir_health_score(df) 
        print("\n--- Índice de Saúde da Loja/Hotel ---")
        if health_scores_df is not None:
            print(health_scores_df.to_string(index=False))
        
        # Nota: os gráficos serão exibidos em janelas separadas devido ao 'plt.show()' implícito ao rodar o script
        print("\nGerando gráficos... (feche cada janela de gráfico para continuar)")
        
        fig_pareto = plotar_grafico_pareto(df)
        if fig_pareto: plt.show()
        
        fig_mapa = plotar_mapa_calor(df)
        if fig_mapa: plt.show()

        # ADICIONADO: Chamada para o gráfico de Health Score
        if fig_health_score: plt.show()
        
        # ADICIONADO: Chamada para o gráfico de satisfação por dia da semana
        fig_semana = plotar_rating_por_dia_semana(df)
        if fig_semana: plt.show()

        # ADICIONADO: Chamada para o gráfico de problemas por canal
        fig_canal = plotar_problemas_por_canal(df)
        if fig_canal: plt.show()


if __name__ == '__main__':
    main()