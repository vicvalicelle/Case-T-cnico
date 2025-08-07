import pandas as pd
import requests
import json
import os
from dotenv import load_dotenv
import time
from .config import NOME_ARQUIVO_ENV, NOME_ARQUIVO_CSV, MODELO_IA

# --- Configurações ---
load_dotenv(dotenv_path=NOME_ARQUIVO_ENV)
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

# A função de chamada da API permanece a mesma
def classificar_feedback_com_ia(texto_feedback: str, setor: str) -> dict | None:
    """
    Envia o texto de um feedback para a API da OpenRouter para classificação.
    """
    if not OPENROUTER_API_KEY:
        print(f"Erro: Chave de API da OpenRouter não encontrada. Verifique seu arquivo '{NOME_ARQUIVO_ENV}'")
        return None
    prompt = f"""
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
    try:
        response = requests.post(
            url="https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {OPENROUTER_API_KEY}",
                "Content-Type": "application/json"
            },
            data=json.dumps({
                "model": MODELO_IA,
                "messages": [{"role": "user", "content": prompt}],
                "temperature": 0.2,
            })
        )
        response.raise_for_status()
        ai_response_str = response.json()['choices'][0]['message']['content']
        if ai_response_str.strip().startswith("```json"):
            ai_response_str = ai_response_str.strip()[7:-3]
        return json.loads(ai_response_str)
    except requests.exceptions.RequestException as e:
        print(f"Erro na chamada da API: {e}")
        print(f"Response Body: {response.text if 'response' in locals() else 'N/A'}")
        return None
    except json.JSONDecodeError:
        print(f"Erro: A IA não retornou um JSON válido. Resposta recebida:\n{ai_response_str}")
        return None
    except (KeyError, IndexError):
        print(f"Erro: Formato da resposta da API inesperado. Resposta recebida:\n{response.text}")
        return None

# A lógica principal de processamento do CSV agora está nesta função
def classificar_feedbacks_pendentes():
    """
    Lê o arquivo CSV, encontra feedbacks pendentes, classifica-os com a IA e salva o arquivo.
    """
    try:
        df = pd.read_csv(NOME_ARQUIVO_CSV, sep=';', encoding='utf-8')
    except FileNotFoundError:
        print(f"Erro: O arquivo '{NOME_ARQUIVO_CSV}' não foi encontrado.")
        return
    except Exception as e:
        print(f"Ocorreu um erro ao ler o arquivo CSV: {e}")
        return
    
    # Prepara a coluna 'Status' se não existir ou se tiver valores nulos
    if 'Status' not in df.columns:
        df['Status'] = 'Pendente'
    else:
        df['Status'] = df['Status'].fillna('Pendente')

    colunas_ia = [
        'Sentimento', 'Sentiment_Score', 'Categoria', 'Subcategoria', 'Tags',
        'Menciona_Empregado', 'Urgencia', 'Palavras_Chave', 'Sugestao_Acao',
        'Rascunho_Resposta', 'Status'
    ]
    # Garante que as colunas da IA existam no DataFrame
    for col in colunas_ia:
        if col not in df.columns:
            df[col] = pd.Series(dtype='object')
            
    feedbacks_para_classificar = df[df['Status'] != 'Classificado'].copy()

    if feedbacks_para_classificar.empty:
        print("✅ Nenhum novo feedback para classificar.")
        return

    print(f"🔎 Encontrados {len(feedbacks_para_classificar)} feedbacks para classificar...")
    for index, row in feedbacks_para_classificar.iterrows():
        id_feedback = row.get('ID', 'ID não encontrado')
        print(f"\n🧠 Processando feedback ID: {id_feedback}...")

        resultado_ia = classificar_feedback_com_ia(row['Texto_Original'], row['Setor'])

        if resultado_ia:
            for coluna in colunas_ia:
                valor = resultado_ia.get(coluna)
                if isinstance(valor, list):
                    df.loc[index, coluna] = ", ".join(map(str, valor))
                else:
                    df.loc[index, coluna] = valor
            print(f"  -> ✅ Status: Classificado com sucesso!")
        else:
            print(f"  -> ❌ Status: Falha na classificação. Será tentado novamente na próxima execução.")
        
        time.sleep(5)

    try:
        df.to_csv(NOME_ARQUIVO_CSV, index=False, sep=';', encoding='utf-8')
        print(f"\n💾 Planilha '{NOME_ARQUIVO_CSV}' atualizada com sucesso.")
    except Exception as e:
        print(f"\n❌ Erro ao salvar o CSV. Verifique se ele não está aberto. Erro: {e}")


# Bloco de execução principal, agora mais limpo
if __name__ == '__main__':
    classificar_feedbacks_pendentes()