import random
import uuid
import os
import pandas as pd
from datetime import datetime
from faker import Faker
from pathlib import Path

# Inicializa o Faker para gerar dados em Português do Brasil
faker = Faker('pt_BR')

def gerar_feedbacks_com_faker(n: int, setor: str) -> list:
    """
    Gera uma lista de feedbacks fictícios usando a biblioteca Faker.
    (Esta função é a mesma da resposta anterior, sem modificações)
    """
    if setor not in ['hotelaria', 'material_construcao']:
        print(f"Alerta: Setor '{setor}' inválido. Ignorando.")
        return []

    canais = ['Website', 'Aplicativo', 'Email', 'Totem na Loja', 'Telefone', 'Redes Sociais', 'Reclame Aqui']

    textos_feedback = {
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
    
    def gerar_nome_hotel():
      sufixos = ['Palace', 'Resort', 'Plaza', 'Hotel', 'Inn', 'Comfort']
      return f"Hotel {faker.last_name()} {random.choice(sufixos)}"

    def gerar_nome_loja_construcao():
      prefixos = ['Constrói', 'Mega', 'Depósito', 'Center']
      sufixos = ['Materiais', '& Cia', 'Tudo', 'Construção']
      return f"{random.choice(prefixos)} {faker.word().capitalize()} {random.choice(sufixos)}"

    feedbacks_gerados = []
    lista_produtos = ['cimento', 'tijolos', 'porcelanato', 'tinta', 'argamassa', 'torneiras']

    for _ in range(n):
        rating = faker.random_int(min=1, max=5)
        categoria_texto = 'positivo' if rating >= 4 else 'neutro' if rating == 3 else 'negativo'
        
        local_gerado = gerar_nome_hotel() if setor == 'hotelaria' else gerar_nome_loja_construcao()
        texto_template = random.choice(textos_feedback[setor][categoria_texto])
        
        texto_final = texto_template.format(nome=faker.name(), local=local_gerado, produto=random.choice(lista_produtos))

        feedback = {
            'ID': str(uuid.uuid4()),
            'Setor': setor.replace('_', ' ').title(),
            'Canal': random.choice(canais),
            'Data': faker.date_time_between(start_date='-1y', end_date='now').strftime('%Y-%m-%d %H:%M:%S'),
            'Rating': rating,
            'Local_Loja': local_gerado,
            'Texto_Original': texto_final
        }
        feedbacks_gerados.append(feedback)

    return feedbacks_gerados

# --- BLOCO PRINCIPAL PARA GERAR E SALVAR EM CSV ---
if __name__ == '__main__':
    NOME_ARQUIVO_CSV = Path(__file__).resolve().parent.parent / 'data' / 'feedbacks_gerados.csv'
    NOVOS_FEEDBACKS_HOTELARIA = 5
    NOVOS_FEEDBACKS_CONSTRUCAO = 5

    print("Iniciando geração de novos feedbacks...")

    feedbacks_hoteleiros = gerar_feedbacks_com_faker(NOVOS_FEEDBACKS_HOTELARIA, 'hotelaria')
    feedbacks_construcao = gerar_feedbacks_com_faker(NOVOS_FEEDBACKS_CONSTRUCAO, 'material_construcao')

    todos_novos_feedbacks = feedbacks_hoteleiros + feedbacks_construcao
    novos_feedbacks_df = pd.DataFrame(todos_novos_feedbacks)

    if os.path.exists(NOME_ARQUIVO_CSV):
        print(f"Arquivo '{NOME_ARQUIVO_CSV}' encontrado. Lendo dados existentes...")
        df_existente = pd.read_csv(NOME_ARQUIVO_CSV, quotechar='"', encoding="utf-8", on_bad_lines='skip')
        print("Adicionando novos feedbacks ao arquivo CSV...")
        df_final = pd.concat([df_existente, novos_feedbacks_df], ignore_index=True)
    else:
        print(f"Arquivo '{NOME_ARQUIVO_CSV}' não encontrado. Criando um novo arquivo...")
        df_final = novos_feedbacks_df

    try:
        if os.path.exists(NOME_ARQUIVO_CSV):
            print(f"Arquivo '{NOME_ARQUIVO_CSV}' encontrado. Adicionando novos feedbacks ao final...")
            novos_feedbacks_df.to_csv(NOME_ARQUIVO_CSV, mode='a', index=False, sep=';', header=False)
        else:
            print(f"Arquivo '{NOME_ARQUIVO_CSV}' não encontrado. Criando novo arquivo...")
            novos_feedbacks_df.to_csv(NOME_ARQUIVO_CSV, index=False, sep=';')
            
        print(f"\nSucesso! {len(novos_feedbacks_df)} novos feedbacks foram adicionados em '{NOME_ARQUIVO_CSV}'.")
    except Exception as e:
        print(f"\nOcorreu um erro ao salvar o arquivo: {e}")
        print("Verifique se o arquivo não está aberto em outro programa.")
