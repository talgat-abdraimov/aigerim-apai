from functools import wraps

import emoji
from loguru import logger
from telegram import Update
from telegram.ext import ContextTypes


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

        logger.info(
            'User {full_name} sent a message: {message}',
            full_name=update.effective_user.full_name,
            username=update.effective_user.username,
            message=update.message.text,
        )

        return await func(update, context)

    return wrapper
