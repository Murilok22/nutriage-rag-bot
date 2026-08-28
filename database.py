import sqlite3

# NOME DO ARQUIVO DO BANCO DE DADOS
# O SQLite salva tudo em um arquivo local no seu computador.
NOME_BANCO = "triagem_suporte.db"


def inicializar_banco():
    """Cria a tabela no banco de dados se ela ainda não existir.

    Esta função deve ser executada quando a aplicação é ligada.
    """
    # 1. Conecta ao arquivo do banco (se o arquivo não existir, o SQLite cria ele na hora)
    conn = sqlite3.connect(NOME_BANCO)

    # 2. O 'cursor' é o nosso "agente" que executa os comandos SQL dentro do banco
    cursor = conn.cursor()

    # 3. Comando SQL para criar a tabela chamada 'historico_atendimento'
    # TEXT = Texto | INTEGER = Número Inteiro | DATETIME = Data e Hora
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS historico_atendimento (
            id INTEGER PRIMARY KEY AUTOINCREMENT,  -- ID único que aumenta sozinho (1, 2, 3...)
            data_hora DATETIME DEFAULT CURRENT_TIMESTAMP, -- Salva a hora exata do atendimento
            mensagem_cliente TEXT,                -- O texto original que o cliente mandou
            categoria TEXT,                       -- A categoria vinda da IA (ex: PIX)
            prioridade TEXT,                      -- A prioridade vinda da IA (ex: URGENTE)
            resumo TEXT,                          -- Resumo de 15 palavras gerado pela IA
            acao_interna TEXT,                    -- A instrução técnica para a equipe
            resposta_sugerida TEXT               -- A resposta gerada no tom Nubank
        )
    """)

    # 4. 'commit()' confirma e salva as alterações feitas no arquivo do banco
    conn.commit()

    # 5. Fecha a conexão para não consumir memória do computador
    conn.close()


def salvar_atendimento(mensagem: str, triagem_dict: dict):
    """Recebe a mensagem do cliente e o dicionário com o resultado da IA

    e insere uma nova linha na tabela do banco de dados.
    """
    # 1. Abre a conexão com o banco de dados
    conn = sqlite3.connect(NOME_BANCO)
    cursor = conn.cursor()

    # 2. Comando SQL de Inserção ('INSERT INTO')
    # Os '?' são placeholders (ponto de interrogação) para evitar ataques de SQL Injection
    # e garantir a segurança dos dados.
    cursor.execute(
        """
        INSERT INTO historico_atendimento 
        (mensagem_cliente, categoria, prioridade, resumo, acao_interna, resposta_sugerida)
        VALUES (?, ?, ?, ?, ?, ?)
    """,
        (
            mensagem,
            triagem_dict.get("categoria"),
            triagem_dict.get("prioridade"),
            triagem_dict.get("resumo_executivo"),
            triagem_dict.get("acao_interna"),
            triagem_dict.get("resposta_sugerida"),
        ),
    )

    # 3. Salva a nova linha e fecha o banco
    conn.commit()
    conn.close()
    
    # Bloco de teste individual do banco de dados
if __name__ == "__main__":
    print("1. Criando o banco de dados e a tabela...")
    inicializar_banco()

    # Dados simulados para testar se a gravação funciona
    mensagem_ficticia = (
        "Teste: Minha compra no Pix não foi aprovada mas saiu do saldo!"
    )
    dados_ia_ficticios = {
        "categoria": "PIX",
        "prioridade": "URGENTE",
        "resumo_executivo": "Pix debitado da conta mas transação não concluída.",
        "acao_interna": "Verificar logs da API de Pix e estornar valor.",
        "resposta_sugerida": "Sinto muito! Já estamos verificando sua transação Pix e faremos o estorno.",
    }

    print("2. Salvando atendimento simulado no SQLite...")
    salvar_atendimento(mensagem_ficticia, dados_ia_ficticios)

    print("✅ Sucesso! Os dados foram criados e salvos no arquivo 'triagem_suporte.db'.")

def buscar_historico_recente(limite: int = 3) -> str:
    """Busca as últimas mensagens trocadas para dar contexto à IA."""
    conn = sqlite3.connect(NOME_BANCO)
    cursor = conn.cursor()

    # Busca as últimas 'N' mensagens salvas ordenadas do mais antigo para o mais recente
    cursor.execute(
        """
        SELECT mensagem_cliente, resposta_sugerida 
        FROM historico_atendimento 
        ORDER BY id DESC LIMIT ?
    """,
        (limite,),
    )

    registros = cursor.fetchall()
    conn.close()

    # Inverte a ordem para ficar na linha do tempo correta
    registros.reverse()

    historico_texto = ""
    for msg_cliente, resp_bot in registros:
        historico_texto += f"Cliente: {msg_cliente}\nBot: {resp_bot}\n---\n"

    return historico_texto