
# 🟣 Agente Inteligente de Triagem e CX para Atendimento de Suporte (Nubank)

> Projeto de automação com Inteligência Artificial e Python focado em otimização de Experiência do Cliente (CX), triagem instantânea de solicitações e automação de suporte operacional em canais de comunicação contínua (Telegram).

---

## 📌 Visão Geral e Contexto de Negócio

No cenário de um banco digital em escala como o **Nubank**, a agilidade no atendimento de suporte é crítica. Receber milhares de solicitações diárias em diversos canais exige uma triagem rápida para identificar situações de emergência (como fraudes, roubos ou bloqueios indesejados) e encaminhá-las com a prioridade correta, mantendo o tom de voz humano e transparente que é marca registrada da empresa.

### O Problema
- **Sobrecarga operacional:** Triagem manual de tickets de suporte consome tempo precioso da equipe de CX.
- **Risco de latência em emergências:** Solicitações críticas (ex: cartão roubado) podem ficar na mesma fila de dúvidas simples de cadastro.
- **Falta de padronização estruturada:** Atendimentos em canais abertos frequentemente carecem de dados estruturados para análise posterior.

### A Solução
Desenvolvimento de um **Agente de Triagem com IA em Python** que:
1. **Atua em tempo real:** Escuta mensagens enviadas em canais do Telegram.
2. **Processa e Estrutura com LLM:** Utiliza o **Google Gemini 2.5 Flash** para extrair intenção, prioridade e gerar uma pré-resposta no tom Nubank.
3. **Garante Contrato de Dados (Pydantic):** Força a saída da IA em um formato JSON estritamente tipado.
4. **Persiste para Analytics:** Salva as interações e classificações em um banco **SQLite** para relatórios futuros.

---

## 🏗️ Arquitetura da Solução

```text
[ Cliente no Telegram ]
          │
          │ (Mensagem de Texto)
          ▼
[ Bot Python - Async Listener ] ── (PythonTelegramBot)
          │
          ▼
[ Agente de IA - Gemini ] ─────── (google-genai + Pydantic Schema)
          │
          ├──▶ 1. Persistência Estruturada ──▶ [ Banco SQLite ]
          │
          └──▶ 2. Resposta Formatada ────────▶ [ Cliente no Telegram ]



Plaintext

nubank-cx-agent/
├── bot_telegram.py   # Código Python principal (Bot + Gemini + SQLite)
├── schemas.py        # Validação de dados (Pydantic)
├── database.py       # Gerenciamento do banco (SQLite)
├── README.md         # Documentação completa em Markdown
├── .env              # Plaintext para suas chaves privadas (NÃO vai pro GitHub)
├── .env.example      # Plaintext modelo para o repositório
└── requirements.txt  # Plaintext com as dependências do projeto