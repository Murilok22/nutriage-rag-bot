# 🔮 NuTriage Bot — Agente Assíncrono de Triagem Inteligente (RAG + Gemini API)

> Projeto de automação com Inteligência Artificial Generativa e Python focado em triagem instantânea de solicitações, resposta contextualizada via RAG (Retrieval-Augmented Generation) e automação de suporte operacional em canais de mensageria (Telegram).

---

## 📌 Visão Geral e Contexto de Negócio

No cenário de um banco digital como o **Nubank**, a agilidade no atendimento ao cliente é crítica. Receber milhares de solicitações diárias exige uma triagem rápida para identificar emergências (fraudes, roubos, perdas) e aplicar a priorização correta, mantendo a resposta alinhada às políticas oficiais e ao tom de voz humano da empresa.

### O Problema
- **Sobrecarga operacional:** Triagem manual de chamados consome tempo precioso das equipes de CX.
- **Risco de latência em emergências:** Solicitações críticas podem ficar retidas na mesma fila de dúvidas simples.
- **Alucinações de IA:** Modelos generativos puros podem inventar regras ou prazos não oficiais.
- **Limites de API (Rate Limits):** Picos de requisições em APIs gratuitas acionam erros `429 (RESOURCE_EXHAUSTED)` que interrompem o serviço.

### A Solução
Desenvolvimento de um **Agente Assíncrono com RAG e IA em Python** que:
1. **Atua em tempo real:** Escuta mensagens enviadas de forma assíncrona pelo Telegram.
2. **Elimina Alucinações (RAG Vetorial):** Busca artigos oficiais no **ChromaDB** para embasar a resposta da IA.
3. **Resiliência e FinOps:** Utiliza o modelo **Gemini 3.5 Flash Lite** com *Fallback* automático para contornar limites de cota (429).
4. **Contrato de Dados Estrito (Pydantic):** Garante respostas estruturadas com categorias, prioridades e ações internas padronizadas.
5. **Guardrails de Escopo:** Recusa solicitações fora do escopo financeiro/Nubank.

---

## 🏗️ Arquitetura da Solução

```text
[ Cliente no Telegram ]
          │
          │ (Mensagem de Texto)
          ▼
[ Bot Python - Async Listener ] ──▶ (python-telegram-bot)
          │
          ├──▶ 1. Histórico Recente ──▶ [ Banco SQLite ]
          │
          ├──▶ 2. Busca Semântica ────▶ [ ChromaDB Vector DB ]
          │
          ▼
[ Motor de IA - main.py ] ───────▶ [ Google Gemini 3.5 Flash Lite ]
          │                            │
          │                            ├── [Falha 429] ──▶ Fallback Automático
          │                            └── [Sucesso] ───▶ Saída Pydantic (JSON)
          ▼
[ Persistência no SQLite ] ───────▶ [ Resposta Formatada no Telegram ]


📂 Estrutura do Repositório
Plaintext

nutriage-rag-bot/
├── bot_telegram.py     # Listener assíncrono do Telegram (Handling & Typing)
├── main.py             # Agente de IA, Pydantic Schema, Guardrails e Fallback
├── knowledge_base.py   # Gerenciador de embeddings e buscas vetoriais (ChromaDB)
├── ingestao_urls.py    # Script de raspagem e carga da base de conhecimento
├── database.py         # Persistência local de atendimentos e históricos (SQLite)
├── schemas.py          # Definição do contrato de dados da triagem (Pydantic)
├── requirements.txt    # Dependências do projeto
├── .env.example        # Modelo de variáveis de ambiente
└── README.md           # Documentação completa do projeto

🛠️ Tech Stack & Ferramentas

    Linguagem: Python 3.10+ (asyncio)

    LLM Provider: Google GenAI SDK (google-genai), modelo gemini-3.5-flash-lite

    Vector Store & RAG: ChromaDB

    Validação & Schemas: Pydantic (Structured Outputs)

    Interface de Mensageria: python-telegram-bot

    Banco de Dados Local: SQLite3

🚀 Como Executar o Projeto

    1. Clonar o Repositório:
    Bash

    git clone [https://github.com/Murilok22/nutriage-rag-bot.git](https://github.com/Murilok22/nutriage-rag-bot.git)
    cd nutriage-rag-bot

    2. Configurar o Ambiente Virtual:
    Bash

    python -m venv venv
    source venv/bin/activate  # Linux/Mac
    .\venv\Scripts\activate   # Windows
    pip install -r requirements.txt

    3. Configurar as Variáveis de Ambiente:
    Crie um arquivo .env baseado no .env.example:
    Snippet de código

    GEMINI_API_KEY=sua_chave_gemini_aqui
    TELEGRAM_BOT_TOKEN=seu_token_telegram_aqui

    4. Executar a Aplicação:
    Bash

    python bot_telegram.py


🤝 Autor

Desenvolvido por Murilo Oliveira Silva

    LinkedIn: in/murilooliveiras

    E-mail: murilomos@hotmail.com