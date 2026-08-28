import chromadb

# Criamos um banco vetorial persistente (salvo na pasta ./chroma_db)
chroma_client = chromadb.PersistentClient(path="./chroma_db")
colecao = chroma_client.get_or_create_collection(name="suporte_nubank")


def inicializar_base_conhecimento():
    """Popula o ChromaDB com artigos e diretrizes oficiais se a coleção estiver vazia."""
    if colecao.count() == 0:
        artigos = [
            # ID 1: MED / Pix Fraude
            "O Mecanismo Especial de Devolução (MED) permite contestar fraudes ou golpes em Pix em até 80 dias. O acionamento é feito pelo app selecionando a transação e tocando em 'Relatar um problema'.",
            # ID 2: Pix Noturno
            "O limite padrão para transferências Pix no período noturno (das 20h às 06h) é de R$ 1.000. O cliente pode alterar esse limite pelo aplicativo no menu 'Meus Limites Pix', levando de 24h a 48h para aprovação por segurança.",
            # ID 3: Segunda Via de Cartão
            "Para pedir a 2ª via do cartão de crédito sem custos por perda, roubo ou danos, acesse a aba 'Meus Cartões' no app, selecione o cartão físico e toque em 'Configurar' -> 'Pedir 2ª via'.",
            # ID 4: Cancelamento de Compras / Estorno
            "O Nubank não tem autonomia para cancelar compras no cartão diretamente. O cancelamento deve ser solicitado ao estabelecimento comercial. Caso o lojista não resolva em até 15 dias, o cliente pode abrir uma contestação pelo app anexando os comprovantes de contato.",
        ]

        ids = ["doc_med", "doc_pix_noturno", "doc_segunda_via", "doc_estorno"]

        colecao.add(documents=artigos, ids=ids)
        print("📚 Base de conhecimento (ChromaDB) inicializada com sucesso!")


def buscar_contexto_relevante(query: str, top_k: int = 1) -> str:
    """Busca o trecho de artigo mais relevante semanticamente para a dúvida do cliente."""
    resultados = colecao.query(query_texts=[query], n_results=top_k)

    # Retorna o texto do documento encontrado
    if resultados["documents"] and resultados["documents"][0]:
        return resultados["documents"][0][0]
    return ""