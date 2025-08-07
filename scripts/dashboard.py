# dashboard.py (versão completa e corrigida)

import pandas as pd
import matplotlib
# GARANTE QUE OS GRÁFICOS APARECERÃO AO RODAR O SCRIPT
matplotlib.use('TkAgg') 
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import seaborn as sns
# Importa a configuração do arquivo .config na mesma pasta
from .config import NOME_ARQUIVO_CSV

# --- Funções de Lógica de Dados ---
def carregar_dados():
    """Carrega e prepara os dados do CSV."""
    try:
        df = pd.read_csv(NOME_ARQUIVO_CSV, sep=';', encoding='utf-8')
        df['Data'] = pd.to_datetime(df['Data'])
        df['Rating'] = pd.to_numeric(df['Rating'])
        print(f"✅ Arquivo carregado com sucesso de: {NOME_ARQUIVO_CSV}")
        return df
    except FileNotFoundError:
        print(f"❌ ERRO: Arquivo '{NOME_ARQUIVO_CSV}' não encontrado.")
        return None

# --- Funções de Visualização (cada gráfico vira uma função) ---
def plotar_kpis_gerais(df):
    """Imprime os KPIs gerais de satisfação e sentimento."""
    avg_rating = df['Rating'].mean()
    # Verifica se a coluna 'Sentimento' existe antes de usar
    if 'Sentimento' in df.columns:
        sentiment_distribution = df['Sentimento'].value_counts(normalize=True) * 100
        print("\n[1. KPIs Gerais]")
        print(f"Índice de Satisfação Médio (Rating): {avg_rating:.2f} de 5")
        print("Distribuição de Sentimento:")
        print(sentiment_distribution.round(2).to_string())
    else:
        print("\n[1. KPIs Gerais]")
        print(f"Índice de Satisfação Médio (Rating): {avg_rating:.2f} de 5")
        print("Aviso: Coluna 'Sentimento' não encontrada para análise de distribuição.")

def plotar_grafico_pareto(df):
    """Gera e exibe um gráfico de Pareto das reclamações."""
    # Filtra por feedbacks negativos que tenham Subcategoria
    df_negativo = df[(df['Sentimento'] == 'Negativo') & (df['Subcategoria'].notna())].copy()
    if df_negativo.empty:
        print("Aviso: Nenhum feedback negativo com subcategoria para gerar o Gráfico de Pareto.")
        return

    contagem_subcat = df_negativo['Subcategoria'].value_counts().reset_index()
    contagem_subcat.columns = ['Subcategoria', 'Contagem']
    contagem_subcat['Percentual_Acumulado'] = (contagem_subcat['Contagem'].cumsum() / contagem_subcat['Contagem'].sum()) * 100

    fig, ax1 = plt.subplots(figsize=(15, 8))
    # AQUI ESTÁ A LÓGICA DE DESENHO DO GRÁFICO DE BARRAS
    ax1.bar(contagem_subcat['Subcategoria'], contagem_subcat['Contagem'], color='cornflowerblue')
    ax1.set_xlabel('Subcategoria do Problema', fontsize=12)
    ax1.set_ylabel('Número de Ocorrências', color='cornflowerblue', fontsize=12)
    ax1.tick_params(axis='y', labelcolor='cornflowerblue')
    plt.xticks(rotation=45, ha="right")

    ax2 = ax1.twinx()
    # AQUI ESTÁ A LÓGICA DE DESENHO DO GRÁFICO DE LINHA
    ax2.plot(contagem_subcat['Subcategoria'], contagem_subcat['Percentual_Acumulado'], color='crimson', marker='o', ms=5)
    ax2.set_ylabel('Percentual Acumulado (%)', color='crimson', fontsize=12)
    ax2.tick_params(axis='y', labelcolor='crimson')
    ax2.yaxis.set_major_formatter(mtick.PercentFormatter(xmax=100.0))
    ax2.set_ylim([0, 110])

    plt.title('Gráfico de Pareto: Causas Principais de Reclamações', fontsize=16)
    fig.tight_layout()
    plt.show() # Mostra o gráfico

def plotar_mapa_calor(df):
    """Gera e exibe um mapa de calor de problemas vs. lojas."""
    df_negativo = df[(df['Sentimento'] == 'Negativo') & (df['Subcategoria'].notna())].copy()
    if df_negativo.empty:
        print("Aviso: Nenhum feedback negativo com subcategoria para gerar o Mapa de Calor.")
        return
        
    crosstab_loja_problema = pd.crosstab(df_negativo['Local_Loja'], df_negativo['Subcategoria'])
    
    plt.figure(figsize=(16, 9))
    # AQUI ESTÁ A LÓGICA DE DESENHO DO MAPA DE CALOR
    sns.heatmap(crosstab_loja_problema, annot=True, fmt='d', cmap='Reds', linewidths=.5)
    plt.title('Mapa de Calor: Ocorrências de Problemas por Loja/Hotel', fontsize=16)
    plt.xlabel('Subcategoria do Problema')
    plt.ylabel('Loja / Hotel')
    plt.xticks(rotation=30, ha="right")
    plt.yticks(rotation=0)
    plt.tight_layout()
    plt.show() # Mostra o gráfico

# --- Bloco de Execução ---
def main():
    """Função principal que orquestra a geração do dashboard."""
    print("--- INICIANDO GERAÇÃO DO DASHBOARD ---")
    df = carregar_dados()
    
    if df is not None:
        plotar_kpis_gerais(df)
        
        # As funções de plotagem agora filtram os dados internamente
        plotar_grafico_pareto(df)
        plotar_mapa_calor(df)
        # ... outras funções de plotagem podem ser chamadas aqui

if __name__ == '__main__':
    main()