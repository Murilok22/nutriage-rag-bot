import uuid
import bs4
import chromadb
import requests

# 1. Conecta ao ChromaDB local existente
chroma_client = chromadb.PersistentClient(path="./chroma_db")
colecao = chroma_client.get_or_create_collection(name="suporte_nubank")

# Lista de URLs oficiais fornecida
URLS_NUBANK = [
    "https://nubank.com.br/nu/conta",
    "https://blog.nubank.com.br/login-nubank-site/",
    "https://nubank.com.br/etica-compliance-e-impacto",
    "https://nubank.com.br/perguntas",
    "https://nubank.com.br/nubank-cancelando-contas-entenda-quando-acontece",
    "https://nubank.com.br/novo-desenrola-brasil-2026",
    "https://nubank.com.br/o-nubank-vai-fechar-noticia-falsa",
    "https://nubank.com.br/croma",
    "https://nubank.com.br/ultravioleta",
    "https://nubank.com.br/nu",
    "https://nubank.com.br/empresas",
    "https://nubank.com.br/empresas/emprestimos",
    "https://nubank.com.br/empresas/investimentos",
    "https://nubank.com.br/empresas/gestao-de-impostos",
    "https://nubank.com.br/empresas/solucoes-para-cobranca",
    "https://nubank.com.br/nu/caixinhas",
    "https://nubank.com.br/nu/emprestimos",
    "https://blog.nubank.com.br/nubank-seguranca/",
    "https://app.nubank.com.br/roubo/",
    "https://denunciargolpes.nubank.com.br/pt/nubankdenuncias",
    "https://nubank.com.br/ajuda-e-seguranca/central-de-protecao",
    "https://nubank.com.br/contatos",
]


def extrair_texto_url(url: str) -> str:
    """Faz o download da página HTML e extrai apenas o conteúdo textual relevante."""
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }
    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            soup = bs4.BeautifulSoup(response.text, "html.parser")

            # Remove scripts e estilos CSS para deixar texto puro
            for script in soup(["script", "style", "nav", "footer"]):
                script.decompose()

            texto = soup.get_text(separator=" ", strip=True)
            # Retorna trecho útil limpo (limitado para evitar estouro)
            return texto[:2000]
    except Exception as e:
        print(f"⚠️ Erro ao acessar {url}: {e}")
    return ""


def executar_ingestao():
    print("🚀 Iniciando raspagem e vetorização das URLs do Nubank...")

    for url in URLS_NUBANK:
        print(f"📥 Processando: {url}")
        conteudo = extrair_texto_url(url)

        if conteudo:
            # Gera ID único para cada página
            doc_id = str(uuid.uuid4())

            # Adiciona ao banco de dados vetorial
            colecao.add(
                documents=[conteudo],
                ids=[doc_id],
                metadatas=[{"fonte": url}],
            )

    print(
        f"\n✅ Concluído! O ChromaDB agora possui {colecao.count()} documentos catalogados."
    )


if __name__ == "__main__":
    executar_ingestao()