from pathlib import Path

# 1. CONFIGURAÇÕES GERAIS E DE CAMINHOS
DATA_DIR = Path(__file__).resolve().parent.parent / 'data'
NOME_ARQUIVO_CSV = DATA_DIR / 'feedbacks_gerados.csv'
NOME_ARQUIVO_ENV = Path(__file__).resolve().parent.parent / 'chave.env'

# 2. CONFIGURAÇÕES DO GERADOR DE FEEDBACK (gerarFeedback.py)
NOVOS_FEEDBACKS_HOTELARIA = 5
NOVOS_FEEDBACKS_CONSTRUCAO = 5
FAKER_LOCALE = 'pt_BR'
FEEDBACK_START_DATE = '-1y' # data para geração

# Listas de Conteúdo para Geração
CANAIS_FEEDBACK = ['Website', 'Aplicativo', 'Email', 'Totem na Loja', 'Telefone', 'Redes Sociais', 'Reclame Aqui']
LISTA_PRODUTOS_CONSTRUCAO = ['cimento', 'tijolos', 'porcelanato', 'tinta', 'argamassa', 'torneiras']
PREFIXOS_LOJAS = ['Constrói', 'Mega', 'Depósito', 'Center']
SUFIXOS_LOJAS = ['Materiais', '& Cia', 'Tudo', 'Construção']
SUFIXOS_HOTEIS = ['Palace', 'Resort', 'Plaza', 'Hotel', 'Inn', 'Comfort']

# Templates de Texto para Geração 
TEXTOS_FEEDBACK = {
    'hotelaria': {
        'positivo': ["Estadia fantástica! A equipe, especialmente {nome}, foi extremamente atenciosa.", "Processo de check-in rápido. Adorei a vista do quarto e o conforto da cama no {local}.", "Excelente localização e instalações. A área da piscina é maravilhosa."],
        'neutro': ["A estadia foi boa, mas o Wi-Fi no quarto era instável. O atendimento de {nome} na recepção foi ok.", "O hotel é bem localizado, porém o quarto era menor do que eu esperava."],
        'negativo': ["Decepcionante. O ar condicionado do quarto não funcionava e o atendente {nome} não resolveu.", "A limpeza do banheiro deixou a desejar. Encontrei cabelos no ralo.", "Péssimo atendimento na recepção, o funcionário parecia totalmente perdido."]
    },
    'material_construcao': {
        'positivo': ["Vendedor {nome} foi muito atencioso e com grande conhecimento, me ajudou a escolher o {produto} certo.", "Preços muito competitivos e a entrega foi realizada antes do prazo. Recomendo a loja {local}!", "Loja extremamente bem organizada, fácil encontrar os itens."],
        'neutro': ["A loja tem boa variedade, mas tive dificuldade para conseguir ajuda de um vendedor no setor de {produto}s.", "Encontrei o que precisava, mas o preço do {produto} estava um pouco acima da média."],
        'negativo': ["Péssimo atendimento. Esperei mais de 20 minutos e o vendedor {nome} não soube tirar minhas dúvidas sobre {produto}.", "A entrega do meu pedido de {produto} atrasou 5 dias e a loja não deu satisfação.", "Falta de estoque de {produto}. Anunciam no site, mas não tem na loja física."]
    }
}

# 3. CONFIGURAÇÕES DA IA (classificador_ia.py)
# Parâmetros da API 
MODELO_IA = 'z-ai/glm-4.5-air:free'
API_URL = "https://openrouter.ai/api/v1/chat/completions"
IA_TEMPERATURE = 0.2
API_CALL_DELAY_SECONDS = 5

# Estrutura e Prompt da IA
COLUNAS_IA = [
    'Sentimento', 'Sentiment_Score', 'Categoria', 'Subcategoria', 'Tags',
    'Menciona_Empregado', 'Urgencia', 'Palavras_Chave', 'Sugestao_Acao',
    'Rascunho_Resposta', 'Status'
]

PROMPT_CLASSIFICADOR = """
Você é um especialista em análise de feedback de clientes. Sua tarefa é analisar o feedback abaixo, que pertence ao setor de "{setor}".
Com base no texto, preencha os campos a seguir com precisão.

Texto do Feedback: "{texto_feedback}"

Sua resposta DEVE ser um único e válido objeto JSON, sem nenhum texto adicional antes ou depois. Use a seguinte estrutura:
{{
  "Sentimento": "Positivo, Negativo ou Neutro.",
  "Sentiment_Score": "Um número de 0.0 (totalmente negativo) a 1.0 (totalmente positivo).",
  "Categoria": "A principal categoria do feedback (ex: Atendimento, Instalações, Produto, Preço, Entrega, Limpeza, Processos).",
  "Subcategoria": "Um detalhe da categoria (ex: Recepção, Qualidade do Cimento, Atraso na Entrega, Limpeza do Quarto).",
  "Tags": "Uma lista de 3 a 5 palavras-chave ou termos curtos em formato de lista Python, como ['tag1', 'tag2'].",
  "Menciona_Empregado": "Se um nome de funcionário for mencionado, coloque o nome exato. Caso contrário, coloque 'Não'.",
  "Urgencia": "Avalie a urgência para a empresa resolver isso como 'Alta', 'Média' ou 'Baixa'.",
  "Palavras_Chave": "Uma lista com as 3 palavras ou expressões mais importantes do texto, como ['palavra1', 'palavra2'].",
  "Sugestao_Acao": "Uma sugestão de ação concreta e curta para a empresa (ex: 'Treinar equipe da recepção', 'Verificar estoque do produto X').",
  "Rascunho_Resposta": "Escreva um rascunho de resposta amigável e profissional para o cliente, com no máximo 40 palavras.",
  "Status": "Classificado"
}}
"""

# 4. CONFIGURAÇÕES DO DASHBOARD (dashboard.py)
# Estilo dos Gráficos
MATPLOTLIB_BACKEND = 'TkAgg'
FIGSIZE_PADRAO = (12, 6)
FIGSIZE_GRANDE = (16, 9)
PALETA_PROBLEMAS_CANAL = 'plasma'
PALETA_HEALTH_SCORE = 'viridis_r'

# Mapeamentos e Ordenações
DIAS_SEMANA_ORDEM = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
DIAS_SEMANA_PT = {'Monday': 'Segunda', 'Tuesday': 'Terça', 'Wednesday': 'Quarta', 'Thursday': 'Quinta', 'Friday': 'Sexta', 'Saturday': 'Sábado', 'Sunday': 'Domingo'}

# Pesos para Métricas
PESOS_HEALTH_SCORE = {
    'rating': 0.5,
    'negativo': 0.3,
    'urgencia': 0.2
}