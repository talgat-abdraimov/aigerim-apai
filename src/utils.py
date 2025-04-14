import io

from telegram.ext import ContextTypes

from constants import GRAMMAR_PROMPT
from decorators import logit
from open_ai import create_text_completion, get_transcription


@logit
async def completion_call(context: ContextTypes.DEFAULT_TYPE) -> str:
    job = context.job

    messages = [
        {'role': 'developer', 'content': GRAMMAR_PROMPT},
        {'role': 'user', 'content': job.data['text']},
    ]

    try:
        completion = await create_text_completion('gpt-4.1-nano-2025-04-14', messages)

    except ValueError as e:
        completion = e.args[0]

    except Exception:
        completion = 'An error occurred. Please try again later.'

    await context.bot.send_message(job.data['chat_id'], completion)


@logit
async def get_transcription_text(context: ContextTypes.DEFAULT_TYPE) -> None:
    job = context.job

    file = await context.bot.get_file(job.data['file_id'])

    file_data = io.BytesIO()
    try:
        await file.download_to_memory(file_data)
        file_data.seek(0)

        transcription = await get_transcription(file_data)

        await context.bot.send_message(job.data['chat_id'], transcription)

    except Exception:
        await context.bot.send_message(job.data['chat_id'], 'An error occurred. Please try again later.')

    finally:
        file_data.close()
