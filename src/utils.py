import io

from telegram import MessageEntity
from telegram.ext import ContextTypes

from constants import GRAMMAR_PROMPT
from open_ai import create_text_completion, get_transcription


async def completion_call(context: ContextTypes.DEFAULT_TYPE) -> str:
    job = context.job

    messages = [
        {'role': 'developer', 'content': GRAMMAR_PROMPT},
        {'role': 'user', 'content': job.data['text']},
    ]

    try:
        completion = await create_text_completion('gpt-4.1-nano-2025-04-14', messages)

        entities = [MessageEntity(type=MessageEntity.BLOCKQUOTE, offset=0, length=len(completion))]

        await context.bot.send_message(job.data['chat_id'], completion, entities=entities)

    except Exception:
        await context.bot.send_message(job.data['chat_id'], 'An error occurred. Please try again later.')


async def get_transcription_text(context: ContextTypes.DEFAULT_TYPE) -> None:
    job = context.job

    file = await context.bot.get_file(job.data['file_id'])

    file_data = io.BytesIO()
    try:
        await file.download_to_memory(file_data)
        file_data.seek(0)

        transcription = await get_transcription(file_data)

        entities = [MessageEntity(type=MessageEntity.BLOCKQUOTE, offset=0, length=len(transcription))]

        await context.bot.send_message(job.data['chat_id'], transcription, entities=entities)

    except Exception:
        await context.bot.send_message(job.data['chat_id'], 'An error occurred. Please try again later.')

    finally:
        file_data.close()
