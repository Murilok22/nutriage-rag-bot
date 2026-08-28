import asyncio
import json
import logging
import os
import warnings
from dotenv import load_dotenv
from google import genai
from google.genai import types
from knowledge_base import (
    buscar_contexto_relevante,
    inicializar_base_conhecimento,
)
from schemas import TriagemTicket

warnings.filterwarnings("ignore")
logging.getLogger("google.genai").setLevel(logging.ERROR)
load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

TEMPERATURE = 0.1

PROMPT_SISTEMA = """
Você é o agente inteligente de triagem e suporte técnico exclusivo do Nubank.

[SUA PERSONALIDADE E TOM DE VOZ]
- Empático, humano, transparente, direto e seguro (estilo 'roxinho').

[REGRA DE OURO - LIMITAÇÃO STRICTA DE ESCOPO (GUARDRAILS)]
1. Seu ÚNICO objetivo é responder sobre assuntos relacionados ao Nubank.
2. Se o cliente fizer perguntas FORA do escopo financeiro/Nubank, RECUSE educadamente.
3. NUNCA invente prazos, valores de taxas ou procedimentos técnicos que não estejam explícitos na [BASE DE CONHECIMENTO - NUBANK].
4. Se a informação não constar na base, instrua o cliente a falar diretamente no chat do app oficial.

[REGRAS DE TRIAGEM]
1. Mensagens sobre roubo, perda de cartão, golpe no Pix ou invasão de conta têm prioridade URGENTE.
2. Na 'acao_interna', especifique o procedimento operacional técnico.
3. Na 'resposta_sugerida', responda ao cliente de forma objetiva e acolhedora.
"""


async def analisar_com_gemini(
    mensagem_cliente: str, historico: str = "", tentativas: int = 2
) -> TriagemTicket:
    """Processa a mensagem com fallback automático de modelo para contornar Rate Limits."""
    contexto_rag = buscar_contexto_relevante(mensagem_cliente)

    prompt_completo = f"""
    {PROMPT_SISTEMA}
    
    [BASE DE CONHECIMENTO - NUBANK]
    {contexto_rag if contexto_rag else "Nenhum artigo específico encontrado."}
    
    [HISTÓRICO RECENTE]
    {historico}
    """

    # Lista de modelos por ordem de prioridade de uso de cota
    modelos = ["gemini-3.5-flash-lite", "gemini-3.5-flash", "gemini-3-flash"]

    for modelo in modelos:
        try:
            response = await client.aio.models.generate_content(
                model=modelo,
                contents=f"{prompt_completo}\n\nNova Mensagem do cliente: {mensagem_cliente}",
                config=types.GenerateContentConfig(
                    temperature=TEMPERATURE,
                    response_mime_type="application/json",
                    response_schema=TriagemTicket,
                ),
            )

            dados_dict = json.loads(response.text)
            return TriagemTicket(**dados_dict)

        except Exception as e:
            erro_str = str(e)
            if "429" in erro_str or "RESOURCE_EXHAUSTED" in erro_str:
                print(f"⚠️ Cota do modelo '{modelo}' esgotada. Alternando para o próximo...")
                continue  # Tenta o próximo modelo da lista
            elif "503" in erro_str or "UNAVAILABLE" in erro_str:
                await asyncio.sleep(1)
                continue
            else:
                raise e

    raise Exception("❌ Todos os modelos excederam o limite de quota diária/minuto.")