import sys

from loguru import logger
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters

from config import settings
from constants import PROMPT_MAPPER, Prompt
from decorators import logging, validate
from utils import get_completion


@logging
@validate
async def text_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    answer = await update.message.reply_text("Your message is in progress. I'll notify you when it's done.")

    data = {
        'user_id': update.effective_user.id,
        'text': update.message.text,
        'message_id': answer.message_id,
        'chat_id': answer.chat_id,
        'prompt': PROMPT_MAPPER[Prompt.grammar],
    }

    context.job_queue.run_once(completion_call, 1, data=data, chat_id=update.effective_chat.id)


@logging
@validate
async def summary_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    answer = await update.message.reply_text("Your message is in progress. I'll notify you when it's done.")

    data = {
        'user_id': update.effective_user.id,
        'text': update.message.text,
        'message_id': answer.message_id,
        'chat_id': answer.chat_id,
        'prompt': PROMPT_MAPPER[Prompt.summarize],
    }

    context.job_queue.run_once(completion_call, 1, data=data, chat_id=update.effective_chat.id)


@logging
@validate
async def paraphrase_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    answer = await update.message.reply_text("Your message is in progress. I'll notify you when it's done.")

    data = {
        'user_id': update.effective_user.id,
        'text': update.message.text,
        'message_id': answer.message_id,
        'chat_id': answer.chat_id,
        'prompt': PROMPT_MAPPER[Prompt.paraphrase],
    }

    context.job_queue.run_once(completion_call, 1, data=data, chat_id=update.effective_chat.id)


@logging
async def completion_call(context: ContextTypes.DEFAULT_TYPE) -> str:
    job = context.job

    prompt = job.data['prompt']
    text = job.data['text']

    try:
        completion = await get_completion(prompt, text)

    except ValueError as e:
        completion = e.args[0]

    except Exception:
        completion = 'An error occurred. Please try again later.'

    await context.bot.editMessageText(completion, job.data['chat_id'], job.data['message_id'])


@logging
@validate
async def start_handler(update: Update, _: ContextTypes.DEFAULT_TYPE) -> None:
    username = update.effective_user.full_name or update.effective_user.username

    logger.info('User <{username}> started the bot.', username=username)

    await update.message.reply_text('Send me a text message to correct.')


@logging
@validate
async def help_handler(update: Update, _: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        'I can help you with the following commands:\n'
        '/summary <text> - Summarize the text\n'
        '/paraphrase <text> - Paraphrase the text\n'
        '/help - Show this help message\n'
        'OR Just send me a text message to correct.'
    )


def run_telegram_bot(token: str):
    app = ApplicationBuilder().token(token).build()

    app.add_handler(CommandHandler('start', start_handler))
    app.add_handler(CommandHandler('summary', summary_handler))
    app.add_handler(CommandHandler('paraphrase', paraphrase_handler))
    app.add_handler(CommandHandler('help', help_handler))
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
