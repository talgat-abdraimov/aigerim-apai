import sys
from functools import wraps

import emoji
from loguru import logger
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters

from anthropic import Anthropic
from config import settings

anthropic = Anthropic(api_key=settings.anthropic_api_key)


def logging(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except Exception as e:
            logger.error('An error occurred: {e}', e=e, function=func.__name__)

    return wrapper


def validate(func):
    @wraps(func)
    async def wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE):
        if update.effective_user.is_bot:
            logger.warning(
                'User <{username}> is a bot. ',
                username=update.effective_user.full_name,
                message=update.message.text,
            )

            await update.message.reply_text("I don't talk to bots.")

            return

        if emoji.is_emoji(update.message.text):
            logger.warning(
                'User <{username}> sent an emoji: {message}',
                username=update.effective_user.full_name,
                message=update.message.text,
            )

            await update.message.reply_text(update.message.text)

            return

        return await func(update, context)

    return wrapper


@logging
@validate
async def text_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    answer = await update.message.reply_text("Your message is in progress. I'll notify you when it's done.")

    data = {
        'user_id': update.effective_user.id,
        'text': update.message.text,
        'message_id': answer.message_id,
        'chat_id': answer.chat_id,
        'prompt_name': 'grammar',
    }

    context.job_queue.run_once(anthropic_api_call, 1, data=data, chat_id=update.effective_chat.id)


@logging
@validate
async def summary_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    answer = await update.message.reply_text("Your message is in progress. I'll notify you when it's done.")

    data = {
        'user_id': update.effective_user.id,
        'text': ''.join(update.message.text.split('/summary')[1:]).strip(),
        'message_id': answer.message_id,
        'chat_id': answer.chat_id,
        'prompt_name': 'summarize',
    }

    context.job_queue.run_once(anthropic_api_call, 1, data=data, chat_id=update.effective_chat.id)


@logging
@validate
async def paraphrase_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    answer = await update.message.reply_text("Your message is in progress. I'll notify you when it's done.")

    data = {
        'user_id': update.effective_user.id,
        'text': ''.join(update.message.text.split('/paraphrase')[1:]).strip(),
        'message_id': answer.message_id,
        'chat_id': answer.chat_id,
        'prompt_name': 'paraphrase',
    }

    context.job_queue.run_once(anthropic_api_call, 1, data=data, chat_id=update.effective_chat.id)


@logging
async def anthropic_api_call(context: ContextTypes.DEFAULT_TYPE) -> str:
    job = context.job

    text = job.data['text']

    try:
        corrected_message = await anthropic.messages(job.data['prompt_name'], text)
    except Exception as e:
        logger.error('An error occurred: {e}', e=e)

        corrected_message = 'An error occurred while processing your message. Please try again'

    await context.bot.editMessageText(corrected_message, job.data['chat_id'], job.data['message_id'])


@logging
async def start_handler(update: Update, _: ContextTypes.DEFAULT_TYPE) -> None:
    username = update.effective_user.full_name or update.effective_user.username

    logger.info('User <{username}> started the bot.', username=username)

    await update.message.reply_text('Send me a text message to correct.')


def run_telegram_bot(token: str):
    app = ApplicationBuilder().token(token).build()

    app.add_handler(CommandHandler('start', start_handler))
    app.add_handler(CommandHandler('summary', summary_handler))
    app.add_handler(CommandHandler('paraphrase', paraphrase_handler))
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
            traces_sample_rate=0.1,
            profiles_sample_rate=0.5,
            integrations=[LoguruIntegration()],
        )

    run_telegram_bot(settings.bot_token)
