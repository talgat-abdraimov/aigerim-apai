import sys

from loguru import logger
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters

from config import settings
from decorators import logit, validate
from utils import completion_call, get_transcription_text


@logit
@validate
async def text_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    data = {
        'user_id': update.effective_user.id,
        'text': update.message.text,
        'chat_id': update.effective_chat.id,
    }

    await context.bot.send_chat_action(update.effective_chat.id, 'typing')

    context.job_queue.run_once(completion_call, 1, data=data, chat_id=update.effective_chat.id)


@logit
@validate
async def start_handler(update: Update, _: ContextTypes.DEFAULT_TYPE) -> None:
    username = update.effective_user.full_name or update.effective_user.username

    logger.info('User <{username}> started the bot.', username=username)

    await update.message.reply_text(
        "Send me a text message to correct. I'll replace it with the correct one."
    )


@logit
@validate
async def help_handler(update: Update, _: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        'I can help you with the following commands:\n'
        '/help - Show this help message\n'
        'OR Just send me a text message to correct. I will do my best to help you.'
    )


@logit
@validate
async def voice_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    logger.info('User <{username}> sent a voice message.', username=update.effective_user.username)

    message = update.message

    audio_file = await context.bot.get_file(message.voice.file_id if message.voice else message.audio.file_id)
    if audio_file.file_size > 5_000_000:  # 5MB
        await update.message.reply_text('The audio message is too large. Please try again.')

        return

    await context.bot.send_chat_action(update.effective_chat.id, 'typing')

    data = {'file_id': audio_file.file_id, 'chat_id': update.effective_chat.id}

    context.job_queue.run_once(get_transcription_text, 1, data=data, chat_id=update.effective_chat.id)


def run_telegram_bot(token: str):
    app = ApplicationBuilder().token(token).build()

    app.add_handler(CommandHandler('start', start_handler))
    app.add_handler(CommandHandler('help', help_handler))
    app.add_handler(MessageHandler(filters.VOICE, voice_handler))
    app.add_handler(MessageHandler(filters.TEXT, text_handler))

    app.run_polling()


if __name__ == '__main__':
    logger.remove()
    logger.add(sys.stdout, level='INFO', serialize=True)

    logger.info('Starting the bot...')

    if settings.sentry_dsn:
        logger.info('Sentry is enabled.')

        import sentry_sdk
        from sentry_sdk.integrations.loguru import LoguruIntegration

        sentry_sdk.init(
            settings.sentry_dsn,
            sample_rate=0.2,
            traces_sample_rate=0.1,
            profiles_sample_rate=0.5,
            integrations=[LoguruIntegration()],
        )

    run_telegram_bot(settings.bot_token)
