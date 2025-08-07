import random
import uuid
import os
import pandas as pd
from faker import Faker
from . import config

# Inicializa o Faker com a localidade definida no config
faker = Faker(config.FAKER_LOCALE)

def gerar_feedbacks_com_faker(n: int, setor: str) -> list:
    """Gera uma lista de feedbacks fictícios usando parâmetros do config."""
    if setor not in ['hotelaria', 'material_construcao']:
        print(f"Alerta: Setor '{setor}' inválido. Ignorando.")
        return []

    # Utiliza o dicionário de textos do config
    textos_feedback = config.TEXTOS_FEEDBACK
    
    def gerar_nome_hotel():
      return f"Hotel {faker.last_name()} {random.choice(config.SUFIXOS_HOTEIS)}"

    def gerar_nome_loja_construcao():
      prefixo = random.choice(config.PREFIXOS_LOJAS)
      sufixo = random.choice(config.SUFIXOS_LOJAS)
      return f"{prefixo} {faker.word().capitalize()} {sufixo}"

    feedbacks_gerados = []

    for _ in range(n):
        rating = faker.random_int(min=1, max=5)
        categoria_texto = 'positivo' if rating >= 4 else 'neutro' if rating == 3 else 'negativo'
        
        local_gerado = gerar_nome_hotel() if setor == 'hotelaria' else gerar_nome_loja_construcao()
        texto_template = random.choice(textos_feedback[setor][categoria_texto])
        
        texto_final = texto_template.format(
            nome=faker.name(), 
            local=local_gerado, 
            produto=random.choice(config.LISTA_PRODUTOS_CONSTRUCAO)
        )

        feedback = {
            'ID': str(uuid.uuid4()),
            'Setor': setor.replace('_', ' ').title(),
            'Canal': random.choice(config.CANAIS_FEEDBACK),
            'Data': faker.date_time_between(start_date=config.FEEDBACK_START_DATE, end_date='now').strftime('%Y-%m-%d %H:%M:%S'),
            'Rating': rating,
            'Local_Loja': local_gerado,
            'Texto_Original': texto_final
        }
        feedbacks_gerados.append(feedback)

    return feedbacks_gerados


def adicionar_novos_feedbacks(num_hotel: int, num_construcao: int):
    """
    Gera uma quantidade definida de feedbacks para cada setor e os adiciona ao arquivo CSV.
    """
    print(f"Iniciando geração de {num_hotel} feedbacks de hotelaria e {num_construcao} de construção...")

    # Usa os parâmetros recebidos em vez dos valores do config
    feedbacks_hoteleiros = gerar_feedbacks_com_faker(num_hotel, 'hotelaria')
    feedbacks_construcao = gerar_feedbacks_com_faker(num_construcao, 'material_construcao')

    todos_novos_feedbacks = feedbacks_hoteleiros + feedbacks_construcao
    
    # Verifica se algum feedback foi realmente gerado
    if not todos_novos_feedbacks:
        print("Nenhum feedback foi gerado. Operação cancelada.")
        return

    novos_feedbacks_df = pd.DataFrame(todos_novos_feedbacks)

    try:
        if os.path.exists(config.NOME_ARQUIVO_CSV):
            print(f"Adicionando {len(novos_feedbacks_df)} novos feedbacks ao arquivo existente...")
            novos_feedbacks_df.to_csv(config.NOME_ARQUIVO_CSV, mode='a', index=False, sep=';', header=False, encoding='utf-8')
        else:
            print(f"Arquivo '{config.NOME_ARQUIVO_CSV}' não encontrado. Criando novo arquivo...")
            novos_feedbacks_df.to_csv(config.NOME_ARQUIVO_CSV, index=False, sep=';', encoding='utf-8')
            
        print(f"\n✅ Sucesso! {len(novos_feedbacks_df)} novos feedbacks foram adicionados.")
    except Exception as e:
        print(f"\n❌ Ocorreu um erro ao salvar o arquivo: {e}")
        print("Verifique se o arquivo não está aberto em outro programa.")


# O bloco de execução principal agora usa os valores do config como padrão
if __name__ == '__main__':
    # Isso permite que o script ainda seja executável de forma independente com valores padrão
    adicionar_novos_feedbacks(
        num_hotel=config.NOVOS_FEEDBACKS_HOTELARIA, 
        num_construcao=config.NOVOS_FEEDBACKS_CONSTRUCAO
    )