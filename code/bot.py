import sys

import emoji
from loguru import logger
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters

from anthropic import Anthropic
from config import settings

anthropic = Anthropic(api_key=settings.anthropic_api_key)


async def text_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if emoji.is_emoji(update.message.text):
        logger.warning(
            f'User <{update.effective_user.full_name or update.effective_user.username}> sent an emoji: {update.message.text}'
        )

        await update.message.reply_text(update.message.text)

        return

    answer = await update.message.reply_text("Your message is in progress. I'll notify you when it's done.")

    data = {
        'user_id': update.effective_user.id,
        'text': update.message.text,
        'message_id': answer.message_id,
        'chat_id': answer.chat_id,
    }

    username = update.effective_user.full_name or update.effective_user.username
    logger.info(f'User <{username}> sent a message: {data["text"]}')

    context.job_queue.run_once(anthropic_api_call, 1, data=data, chat_id=update.effective_chat.id)


async def anthropic_api_call(context: ContextTypes.DEFAULT_TYPE) -> str:
    job = context.job

    text = job.data['text']

    corrected_message = await anthropic.messages(text)

    await context.bot.editMessageText(corrected_message, job.data['chat_id'], job.data['message_id'])


async def not_text_handler(update: Update, _: ContextTypes.DEFAULT_TYPE) -> None:
    username = update.effective_user.full_name or update.effective_user.username

    logger.warning(f'User <{username}> sent a non-text message: {update.message}')

    await update.message.reply_text('Please send me a text message.')


async def start_handler(update: Update, _: ContextTypes.DEFAULT_TYPE) -> None:
    username = update.effective_user.full_name or update.effective_user.username

    logger.info(f'User <{username}> started the bot.')

    await update.message.reply_text('Send me a text message to correct.')


def run_telegram_bot(token: str):
    app = ApplicationBuilder().token(token).build()

    app.add_handler(
        CommandHandler('start', start_handler, filters=filters.ChatType.PRIVATE & filters.Command('start'))
    )
    app.add_handler(MessageHandler(filters.TEXT, text_handler))
    app.add_handler(MessageHandler(filters.COMMAND, not_text_handler))
    app.add_handler(MessageHandler(~filters.TEXT, not_text_handler))

    app.run_polling()


if __name__ == '__main__':
    logger.remove()
    logger.add(sys.stdout, level='INFO', serialize=True)

    logger.info('Starting the bot...')
    run_telegram_bot(settings.bot_token)
