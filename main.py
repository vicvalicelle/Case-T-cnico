import os
import time
import subprocess # Streamlit de forma independente
from scripts.gerarFeedback import adicionar_novos_feedbacks
from scripts.classificador_ia import classificar_feedbacks_pendentes
from scripts.analise import executar_analise_completa 

def limpar_tela():
    os.system('cls' if os.name == 'nt' else 'clear')

def exibir_menu():
    limpar_tela()
    print("=====================================================")
    print("      🤖 PAINEL DE CONTROLE DE ANÁLISE DE FEEDBACKS 🤖")
    print("=====================================================")
    print("\n--- ETAPAS DO PROJETO ---")
    print("  1. ➕ Gerar e Adicionar Novos Feedbacks")
    print("  2. 🧠 Classificar Feedbacks Pendentes com IA")
    print("  3. 📄 Gerar Relatório Estático de Análise (Salva os .png)")
    print("  4. 💻 DASHBOARD INTERATIVO (Streamlit)")
    
    print("\n--- FLUXOS AUTOMATIZADOS ---")
    print("  5. 🚀 Pipeline Completo (Classificar + Gerar Relatório)")
    
    print("\n-----------------------------------------------------")
    print("  6. 🚪 Sair")
    print("=====================================================")
    return input("   Escolha uma opção: ")

def main():
    while True:
        escolha = exibir_menu()
        
        if escolha == '1':
            print("\n--- [Opção 1] Geração de Novos Feedbacks ---")
            try:
                num_hotel = int(input("   Quantos feedbacks de HOTELARIA você quer gerar? "))
                num_construcao = int(input("   Quantos feedbacks de MATERIAL DE CONSTRUÇÃO você quer gerar? "))
                if num_hotel < 0 or num_construcao < 0:
                    print("\n❌ Erro: Por favor, insira um número não negativo.")
                else:
                    print("\n⏳ Iniciando a geração...")
                    adicionar_novos_feedbacks(num_hotel=num_hotel, num_construcao=num_construcao)
                    print("\n✅ Geração concluída!")
            except ValueError:
                print("\n❌ Erro: Entrada inválida. Digite apenas números inteiros.")
            
        elif escolha == '2':
            print("\n--- [Opção 2] Classificação com IA ---")
            print("⏳ Iniciando a classificação...")
            classificar_feedbacks_pendentes()
            print("\n✅ Classificação concluída!")
            
        elif escolha == '3':
            print("\n--- [Opção 3] Geração de Relatório Estático ---")
            print("⏳ Gerando relatório completo com gráficos e previsões...")
            executar_analise_completa() 
            print("\n✅ Relatório estático gerado!")
            
        elif escolha == '4':
            print("\n--- [Opção 4] Iniciando o Dashboard Interativo ---")
            print("Abra seu navegador em http://localhost:8501")
            print("(Pressione Ctrl+C neste terminal para parar o servidor do dashboard)")
            try:
                subprocess.run(["streamlit", "run", "app.py"], check=True)
            except FileNotFoundError:
                print("\n❌ Erro: O comando 'streamlit' não foi encontrado.")
                print("   Verifique se o Streamlit está instalado (`pip install streamlit`).")
            except subprocess.CalledProcessError as e:
                print(f"\n❌ Ocorreu um erro ao executar o dashboard: {e}")
            print("\nServidor do dashboard finalizado.")
            
        elif escolha == '5':
            print("\n--- [Opção 5] Executando Pipeline Completo ---")
            print("\nPasso 1/2: Classificando feedbacks pendentes...")
            classificar_feedbacks_pendentes()
            print("✅ Classificação concluída!")
            print("\nPasso 2/2: Gerando relatório estático...")
            executar_analise_completa()
            print("\n🚀 Pipeline completo! Agora você pode iniciar o dashboard (opção 4) para ver os resultados.")

        elif escolha == '6':
            print("\nSaindo do programa... Até mais! 👋")
            break
            
        else:
            print("\n❌ Opção inválida. Tente novamente.")
            time.sleep(2)
            continue

        input("\n[Pressione Enter para voltar ao menu]")

if __name__ == '__main__':
    main()