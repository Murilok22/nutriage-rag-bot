import os
from dotenv import load_dotenv
from telegram import Update
from telegram.constants import ChatAction
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
)

from database import (
    buscar_historico_recente,
    inicializar_banco,
    salvar_atendimento,
)
from knowledge_base import inicializar_base_conhecimento
from main import analisar_com_gemini

load_dotenv()
TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")


async def comando_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message:
        return

    mensagem_boas_vindas = (
        "Olá! Sou o assistente de suporte e triagem do Nubank. 💜\n\n"
        "Como posso te ajudar hoje? Pode me enviar sua dúvida ou problema que estou pronto para te responder!"
    )
    await update.message.reply_text(mensagem_boas_vindas)


async def responder_mensagem(
    update: Update, context: ContextTypes.DEFAULT_TYPE
):
    if not update.message or not update.message.text:
        return

    texto_cliente = update.message.text
    chat_id = update.message.chat_id

    print(f"\n📩 Nova mensagem do Telegram: '{texto_cliente}'")

    try:
        # 1. Feedback visual imediato para o usuário no Telegram
        await context.bot.send_chat_action(
            chat_id=chat_id, action=ChatAction.TYPING
        )

        # 2. Busca histórico reduzido (1 interação é suficiente para manter contexto com menos latência)
        historico_conversa = buscar_historico_recente(limite=1)

        # 3. Processamento assíncrono com fallback de modelos
        resultado = await analisar_com_gemini(texto_cliente, historico_conversa)

        salvar_atendimento(texto_cliente, resultado.model_dump())

        print(f"📌 Categoria: {resultado.categoria.value}")
        print(f"🚨 Prioridade: {resultado.prioridade.value}")

        await context.bot.send_message(
            chat_id=chat_id, text=resultado.resposta_sugerida
        )
        print("✅ Resposta enviada com sucesso!")

    except Exception as e:
        print(f"❌ Erro no processamento: {e}")


if __name__ == "__main__":
    inicializar_banco()
    inicializar_base_conhecimento()

    print("🤖 Bot Nu_py_bot rodando com otimização de latência e quotas...")
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

    app.add_handler(CommandHandler("start", comando_start))
    app.add_handler(
        MessageHandler(filters.TEXT & (~filters.COMMAND), responder_mensagem)
    )

    app.run_polling()