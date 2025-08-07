# main.py
# Importa as funções principais dos seus módulos refatorados
from scripts.gerarFeedback import adicionar_novos_feedbacks
from scripts.classificador_ia import classificar_feedbacks_pendentes
from scripts.dashboard import main as executar_dashboard

def exibir_menu():
    print("\n--- Painel de Controle da Análise de Feedbacks ---")
    print("1. Gerar novos feedbacks e adicionar à base")
    print("2. Classificar feedbacks pendentes com IA")
    print("3. Gerar e exibir dashboard de análise")
    print("4. Sair")
    return input("Escolha uma opção: ")

def main():
    while True:
        escolha = exibir_menu()
        if escolha == '1':
            adicionar_novos_feedbacks()
        elif escolha == '2':
            classificar_feedbacks_pendentes()
        elif escolha == '3':
            executar_dashboard()
        elif escolha == '4':
            print("Saindo...")
            break
        else:
            print("Opção inválida. Tente novamente.")

if __name__ == '__main__':
    main()