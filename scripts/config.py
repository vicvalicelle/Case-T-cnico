# config.py
from pathlib import Path

# --- Configurações Gerais ---
# Caminho para a pasta 'data', relativo à raiz do projeto
DATA_DIR = Path(__file__).resolve().parent.parent / 'data'
NOME_ARQUIVO_CSV = DATA_DIR / 'feedbacks_gerados.csv'
NOME_ARQUIVO_ENV = Path(__file__).resolve().parent.parent / 'chave.env'

# --- Configurações da IA (classificador_ia.py) ---
MODELO_IA = 'z-ai/glm-4.5-air:free'

# --- Configurações do Gerador (gerarFeedback.py) ---
NOVOS_FEEDBACKS_HOTELARIA = 5
NOVOS_FEEDBACKS_CONSTRUCAO = 5

# --- Configurações do Dashboard (dashboard.py) ---
# Cores, paletas, etc., podem ser adicionadas aqui
PALETA_SENTIMENTO = {'Positivo': 'seagreen', 'Negativo': 'crimson', 'Neutro': 'royalblue'}