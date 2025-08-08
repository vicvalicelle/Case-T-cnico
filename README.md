# **Case Técnico: Análise Inteligente de Feedbacks Multicanais**

**Para:** Setores de Hotelaria All-Inclusive e Varejo de Construção

**Autor:** Victoria Valicelle

-----

### **1. O Problema (A Motivação)**

Empresas nos setores de varejo e hotelaria coletam um volume massivo de feedbacks de clientes através de múltiplos canais (NPS, Reclame Aqui, redes sociais, e-mails, etc.). Sem uma ferramenta adequada, esses dados valiosos ficam isolados e subutilizados. A análise manual é lenta, cara, sujeita a vieses e incapaz de fornecer uma visão consolidada em tempo real, impedindo uma tomada de decisão ágil e estratégica.

Para uma análise mais profunda da motivação e dos objetivos estratégicos, consulte o documento:

  * 📄 [Motivação e Futuros Passos](documentacao/motivacao.md)

### **2. A Solução (O Protótipo Funcional)**

Este projeto implementa um **"Analista de Feedback com IA"**, um protótipo funcional que demonstra como centralizar, categorizar e extrair insights acionáveis de feedbacks. A solução transforma dados brutos em inteligência de negócio através de duas frentes:

#### **Análise via Script (`main.py`)**

  * Um script que exibe os resultados diretamente no terminal. Ideal para relatórios rápidos.

#### **Dashboard Interativo (`app.py`)**

  * O coração do protótipo: uma aplicação web interativa construída com Streamlit, que permite a qualquer gestor explorar os dados de forma visual e intuitiva, sem precisar de conhecimento técnico.
  * **Principais Funcionalidades:**
      * **Visão Geral:** KPIs centralizados, como Rating Médio e volume de feedbacks.
      * **Análise de Pontos Críticos:** Gráfico de Pareto para identificar as principais causas de reclamações e um Mapa de Calor que cruza problemas por loja/hotel.
      * **Identificação de Pontos Fortes:** Análise dos principais motivos de elogio e um "Quadro de Honra" para os funcionários mais bem avaliados.
      * **IA em Ação:** Uma aba para testar a classificação de novos feedbacks em tempo real usando a IA generativa.

### **3. Tecnologias Utilizadas**

  * **🐍 Linguagem:** Python 3.10+
  * **🗂️ Análise de Dados:** Pandas
  * **📊 Visualização de Dados:** Matplotlib & Seaborn
  * **🌐 Dashboard Interativo:** Streamlit
  * **🤖 Inteligência Artificial:** API do Openrouter
  * **🔑 Gerenciamento de Chaves:** python-dotenv

### **4. Estrutura do Projeto**

```
Case-T-cnico/
├── data/
│   └── feedbacks_gerados.csv      # Dados de exemplo utilizados no projeto.
├── documentacao/
│   ├── motivacao.md               # O "porquê" do projeto e visão de futuro.
│   ├── proposta.md                # Proposta detalhada para evolução do protótipo para um produto enterprise.
│   └── tutorial.md                # Guia de instalação e uso passo a passo.
├── scripts/
│   ├── classificador_ia.py        # Módulo de comunicação com a API.
│   ├── config.py                  # Arquivo de configurações centrais.
│   └── dashboard.py               # Funções de lógica de negócio e geração de gráficos.
├── .gitignore                     # Arquivos e pastas a serem ignorados pelo Git.
├── app.py                         # Ponto de entrada para o dashboard interativo (Streamlit).
├── chave.env                      # Arquivo para armazenar a chave da API (NÃO ENVIAR PARA O GIT).
├── main.py                        # Ponto de entrada para a execução via script no terminal.
├── README.md                      # Este arquivo.
└── requirements.txt               # Lista de dependências Python para instalação.
```

### **5. Documentação Completa e Proposta de Valor**

Este repositório contém uma documentação aprofundada que vai além do código, apresentando a visão de negócio e o potencial de evolução desta solução.

  * [📄 Proposta de Evolução para Produção](documentacao/proposta.md): Uma análise completa de como transformar este protótipo em uma solução SaaS enterprise, incluindo arquitetura de produção, análise de ROI, modelo de precificação e um plano de implementação.

  * [💡 Motivação, Objetivos e Próximos Passos](documentacao/motivacao.md): Detalha o raciocínio por trás do projeto, os desafios de negócio que ele resolve e um roadmap de futuras funcionalidades.

  * [💻 Tutorial de Uso e Instalação](documentacao/tutorial.md): Um guia passo a passo para qualquer pessoa configurar e executar este projeto em sua própria máquina.

### **6. Créditos e Agradecimentos**

  * À minha mãe, por inspirar parte da ideia central que deu origem a este projeto.
  * A Hugo, pelo apoio fundamental e insights valiosos, principalmente no processo de modularização do código, que foi crucial para a organização do projeto.
  * Agradecimento à IA Gemini do Google e a OpenAI pela assistência na estruturação da documentação e no refinamento de trechos do código e integrações.