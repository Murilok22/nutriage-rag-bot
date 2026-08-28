from enum import Enum
from pydantic import BaseModel, Field


class CategoriaEnum(str, Enum):
    PIX = "PIX"
    CARTAO_FRAUDE = "CARTAO_FRAUDE"
    FATURA_COBRANCA = "FATURA_COBRANCA"
    CONTA_ACESSO = "CONTA_ACESSO"
    OUTROS = "OUTROS"


class PrioridadeEnum(str, Enum):
    BAIXA = "BAIXA"
    MEDIA = "MEDIA"
    ALTA = "ALTA"
    URGENTE = "URGENTE"


class TriagemTicket(BaseModel):
    categoria: CategoriaEnum = Field(
        description="Categoria principal do problema do cliente."
    )
    prioridade: PrioridadeEnum = Field(
        description="Urgência do atendimento baseada na gravidade."
    )
    resumo_executivo: str = Field(
        description="Resumo do problema em no máximo 15 palavras."
    )
    acao_interna: str = Field(
        description="Instrução técnica interna para a equipe (ex: 'Bloquear cartão via API', 'Transferir para time de Fraude')."
    )
    resposta_sugerida: str = Field(
        description="Resposta empática e direta enviada ao cliente no tom Nubank."
    )