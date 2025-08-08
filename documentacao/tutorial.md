## Guia Completo de Desenvolvimento do Protótipos: Do Ambiente ao Dashboard

### Fase 1: Configuração do Ambiente de Desenvolvimento (Windows)

Antes de começar a programar, prepare sua máquina com as ferramentas essenciais.

**1. Instale o Python**

1.  Acesse o site oficial: [python.org/downloads/windows/](https://www.python.org/downloads/windows/)
2.  Baixe o instalador mais recente para Windows.
3.  **Passo crucial:** Na tela de instalação, marque a caixa **"Add Python to PATH"** antes de clicar em "Install Now".

**2. Instale o Visual Studio Code (VS Code)**

1.  Acesse o site oficial: [code.visualstudio.com](https://code.visualstudio.com/)
2.  Baixe e execute o instalador para Windows.

**3. Configure o VS Code para Python**

1.  Abra o VS Code.
2.  No menu lateral, clique no ícone de **Extensões** (quatro quadrados).
3.  Pesquise por **"Python"** (procure pela extensão oficial, publicada pela Microsoft).
4.  Clique em **Instalar**.

### Fase 2: Controle de Versão com Git e GitHub

Gerenciar o código do seu projeto é fundamental. Aqui estão os dois fluxos de trabalho principais.

**Cenário 1: Clonando o Projeto Existente do GitHub**

Use este método para colaborar em projetos ou baixar códigos de outros.

1.  **Copie a URL:**

      * No GitHub, vá para a página do repositório.
      * Clique no botão verde **"\< \> Code"** e copie a URL (HTTPS é a mais recomendada para iniciantes).

2.  **Clone o Repositório:**

      * Abra seu terminal na pasta onde deseja salvar o projeto.
      * Execute o comando `clone` com a URL copiada.
        ```bash
        git clone <URL_DO_REPOSITORIO_COPIADA>
        ```
      * O Git baixará todos os arquivos e o histórico do projeto, já configurando a conexão remota.

### Fase 3: Desenvolvimento do Protótipo de Análise

Agora, vamos focar nos scripts Python do seu protótipo.

**1. Instalação das Dependências**

Para que todos os componentes do seu protótipo funcionem, instale todas as bibliotecas necessárias de uma só vez. Abra o terminal na pasta do seu projeto e execute:

```bash
pip install pandas openpyxl faker requests python-dotenv streamlit plotly matplotlib seaborn wordcloud scikit-learn
```

**2. Configuração da Chave de API (Para o Classificador)**

Para usar serviços externos como a OpenRouter de forma segura, nunca exponha sua chave de API no código.

1.  Na pasta raiz do seu projeto, crie um arquivo chamado `.env`.

2.  Dentro deste arquivo, adicione sua chave da seguinte forma:

    ```.env
    OPENROUTER_API_KEY="sua_chave_secreta_aqui"
    ```

**3. Executando os Componentes do Protótipo**

**A. Gerador de Exemplos:**

  * **Função:** Criar dados fictícios para teste.
  * **Bibliotecas Principais:** `pandas`, `faker`.
  * **Como Rodar:** Execute o script Python diretamente no terminal.
    ```bash
    python nome_do_script_gerador.py
    ```

**B. Classificador Automático:**

  * **Função:** Classificar textos usando a API da OpenRouter.
  * **Bibliotecas Principais:** `pandas`, `requests`, `python-dotenv`.
  * **Como Rodar:** Execute o script que contém a lógica de classificação.
    ```bash
    python nome_do_script_classificador.py
    ```

**C. Analise e Dashboard Interativo:**

  * **Função:** Visualizar os dados e as análises de forma interativa.
  * **Bibliotecas Principais:** `streamlit`, `pandas`, `plotly`, `sklearn`.
  * **Como Rodar:** Use o comando específico do Streamlit.
    ```bash
    streamlit run nome_do_script_dashboard.py
    ```
    *O Streamlit abrirá uma nova aba no seu navegador com o dashboard funcionando.*