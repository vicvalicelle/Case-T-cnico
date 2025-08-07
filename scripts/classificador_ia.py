import pandas as pd
import requests
import json
import os
from dotenv import load_dotenv
import time
from . import config

# --- Configurações ---
load_dotenv(dotenv_path=config.NOME_ARQUIVO_ENV)
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

def classificar_feedback_com_ia(texto_feedback: str, setor: str) -> dict | None:
    """Envia o texto para a API e retorna o JSON classificado."""
    if not OPENROUTER_API_KEY:
        print(f"Erro: Chave de API da OpenRouter não encontrada. Verifique seu arquivo '{config.NOME_ARQUIVO_ENV}'")
        return None
    
    # Monta o prompt usando o template e os dados do config
    prompt = config.PROMPT_CLASSIFICADOR.format(setor=setor, texto_feedback=texto_feedback)
    
    try:
        response = requests.post(
            url=config.API_URL,
            headers={
                "Authorization": f"Bearer {OPENROUTER_API_KEY}",
                "Content-Type": "application/json"
            },
            data=json.dumps({
                "model": config.MODELO_IA,
                "messages": [{"role": "user", "content": prompt}],
                "temperature": config.IA_TEMPERATURE,
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

def classificar_feedbacks_pendentes():
    """Lê o CSV, classifica feedbacks pendentes com a IA e salva o arquivo."""
    try:
        df = pd.read_csv(config.NOME_ARQUIVO_CSV, sep=';', encoding='utf-8')
    except FileNotFoundError:
        print(f"Erro: O arquivo '{config.NOME_ARQUIVO_CSV}' não foi encontrado.")
        return
    
    if 'Status' not in df.columns:
        df['Status'] = 'Pendente'
    else:
        df['Status'] = df['Status'].fillna('Pendente')

    # Garante que todas as colunas da IA existam no DataFrame
    for col in config.COLUNAS_IA:
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
            for coluna in config.COLUNAS_IA:
                valor = resultado_ia.get(coluna)
                if isinstance(valor, list):
                    df.loc[index, coluna] = ", ".join(map(str, valor))
                else:
                    df.loc[index, coluna] = valor
            print(f"  -> ✅ Status: Classificado com sucesso!")
        else:
            print(f"  -> ❌ Status: Falha na classificação.")
        
        time.sleep(config.API_CALL_DELAY_SECONDS)

    try:
        df.to_csv(config.NOME_ARQUIVO_CSV, index=False, sep=';', encoding='utf-8')
        print(f"\n💾 Planilha '{config.NOME_ARQUIVO_CSV.name}' atualizada com sucesso.")
    except Exception as e:
        print(f"\n❌ Erro ao salvar o CSV. Verifique se ele não está aberto. Erro: {e}")


if __name__ == '__main__':
    classificar_feedbacks_pendentes()