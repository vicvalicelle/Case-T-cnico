from scripts.gerarFeedback import adicionar_novos_feedbacks
from scripts.classificador_ia import classificar_feedbacks_pendentes
from scripts.dashboard import main as executar_dashboard 

def exibir_menu():
    """Exibe o menu de opções para o usuário."""
    print("\n--- Painel de Controle da Análise de Feedbacks ---")
    print("1. Gerar novos feedbacks e adicionar à base")
    print("2. Classificar feedbacks pendentes com IA")
    print("3. Gerar e exibir dashboard de análise")
    print("4. Sair")
    return input("Escolha uma opção (1-4): ")


def main():
    """Função principal que orquestra a execução do projeto."""
    while True:
        escolha = exibir_menu()
        
        if escolha == '1':
            print("\n--- Geração de Novos Feedbacks ---")
            try:
                # Pede ao usuário a quantidade para cada setor
                num_hotel = int(input("Quantos feedbacks de HOTELARIA você quer gerar? "))
                num_construcao = int(input("Quantos feedbacks de MATERIAL DE CONSTRUÇÃO você quer gerar? "))
                
                # Valida se os números não são negativos
                if num_hotel < 0 or num_construcao < 0:
                    print("❌ Erro: Por favor, insira um número não negativo.")
                    continue

                print("\nIniciando a geração de feedbacks...")
                # Chama a função com os valores fornecidos pelo usuário
                adicionar_novos_feedbacks(num_hotel=num_hotel, num_construcao=num_construcao)

            except ValueError:
                print("❌ Erro: Entrada inválida. Por favor, digite apenas números inteiros.")
            
            print("\nOperação concluída.")
            
        elif escolha == '2':
            print("\nIniciando a classificação com IA...")
            classificar_feedbacks_pendentes()
            print("\nOperação concluída.")
            
        elif escolha == '3':
            print("\nIniciando a geração do dashboard...")
            executar_dashboard()
            print("\nOperação concluída.")
            
        elif escolha == '4':
            print("Saindo do programa...")
            break
            
        else:
            print("Opção inválida. Por favor, tente novamente.")

if __name__ == '__main__':
    main()