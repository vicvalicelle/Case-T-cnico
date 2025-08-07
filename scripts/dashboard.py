import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import seaborn as sns
from . import config

# Configura o backend do Matplotlib a partir do config
matplotlib.use(config.MATPLOTLIB_BACKEND) 

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

def plotar_kpis_gerais(df):
    """Imprime os KPIs gerais de satisfação e sentimento."""
    avg_rating = df['Rating'].mean()
    if 'Sentimento' in df.columns:
        sentiment_distribution = df['Sentimento'].value_counts(normalize=True) * 100
        print("\n[1. KPIs Gerais]")
        print(f"Índice de Satisfação Médio (Rating): {avg_rating:.2f} de 5")
        print("Distribuição de Sentimento:")
        print(sentiment_distribution.round(2).to_string())

def plotar_grafico_pareto(df):
    """Gera e exibe um gráfico de Pareto das reclamações."""
    df_negativo = df[(df['Sentimento'] == 'Negativo') & (df['Subcategoria'].notna())].copy()
    if df_negativo.empty: return

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
    
    plt.title('Gráfico de Pareto: Causas Principais de Reclamações', fontsize=16)
    fig.tight_layout()
    plt.show()

def plotar_rating_por_dia_semana(df):
    """Gera um gráfico da média de rating por dia da semana."""
    print("\nGerando Análise de Satisfação por Dia da Semana...")
    df['Dia_Semana'] = df['Data'].dt.day_name()
    
    rating_por_dia = df.groupby('Dia_Semana')['Rating'].mean().reindex(config.DIAS_SEMANA_ORDEM)
    rating_por_dia.index = rating_por_dia.index.map(config.DIAS_SEMANA_PT)
    
    plt.figure(figsize=config.FIGSIZE_PADRAO)
    rating_por_dia.plot(kind='line', marker='o', linestyle='--', color='indigo')
    plt.title('Média de Satisfação por Dia da Semana', fontsize=16)
    plt.xlabel('Dia da Semana'); plt.ylabel('Rating Médio (1-5)')
    plt.ylim(1, 5); plt.grid(True, which='both', linestyle='--', linewidth=0.5)
    plt.tight_layout(); plt.show()

def calcular_e_exibir_health_score(df):
    """Calcula e exibe um score de saúde ponderado para cada loja/hotel."""
    print("\nCalculando Índice de Saúde da Loja/Hotel (Health Score)...")
    
    resultados = []
    pesos = config.PESOS_HEALTH_SCORE

    for loja in df['Local_Loja'].unique():
        df_loja = df[df['Local_Loja'] == loja]
        rating_norm = (df_loja['Rating'].mean() - 1) / 4
        pct_negativo = (df_loja['Sentimento'] == 'Negativo').sum() / len(df_loja)
        pct_urg_alta = (df_loja['Urgencia'] == 'Alta').sum() / len(df_loja)
        
        score = (pesos['rating'] * rating_norm) - (pesos['negativo'] * pct_negativo) - (pesos['urgencia'] * pct_urg_alta)
        resultados.append({'Loja/Hotel': loja, 'Health_Score': score * 100})

    health_scores = pd.DataFrame(resultados).sort_values(by='Health_Score', ascending=False).round(2)
    
    print("\n--- Índice de Saúde da Loja/Hotel (Health Score) ---")
    print(health_scores.to_string(index=False))

    plt.figure(figsize=config.FIGSIZE_GRANDE)
    sns.barplot(data=health_scores, x='Health_Score', y='Loja/Hotel', palette=config.PALETA_HEALTH_SCORE, hue='Loja/Hotel', legend=False)
    plt.title('Ranking de Saúde por Loja/Hotel', fontsize=16)
    plt.xlabel('Health Score (quanto maior, melhor)'); plt.ylabel('Loja / Hotel')
    plt.tight_layout(); plt.show()

def main():
    """Função principal que orquestra a geração do dashboard."""
    print("--- INICIANDO GERAÇÃO DO DASHBOARD ---")
    df = carregar_dados()
    
    if df is not None:
        plotar_kpis_gerais(df)
        plotar_grafico_pareto(df)
        plotar_rating_por_dia_semana(df)
        calcular_e_exibir_health_score(df)

if __name__ == '__main__':
    main()