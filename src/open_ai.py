import io
import json
from typing import Any

from loguru import logger
from openai import AsyncOpenAI, OpenAIError
from openai.types.responses import Response as OpenAIResponse

from config import settings

client = AsyncOpenAI(api_key=settings.openai_api_key)


def get_client():
    global client

    if client is None:
        client = AsyncOpenAI(api_key=settings.openai_api_key)

    return client


async def create_text_completion(model_code: str, messages: list[dict[str, Any]]) -> OpenAIResponse:
    client = get_client()

    try:
        response: OpenAIResponse = await client.responses.create(
            input=messages,
            model=model_code,
            temperature=0.1,
            text={
                'format': {
                    'type': 'json_schema',
                    'name': 'completion',
                    'schema': {
                        'type': 'object',
                        'properties': {
                            'corrected_text': {'type': 'string'},
                        },
                        'required': ['corrected_text'],
                        'additionalProperties': False,
                    },
                    'strict': True,
                },
            },
        )

    except Exception as error:
        logger.error('Internal server error', error=error)

        raise Exception('Internal server error')

    data = json.loads(response.output_text)

    return data['corrected_text']


async def get_transcription(audio_file: io.BytesIO) -> str:
    client = get_client()

    try:
        response: OpenAIResponse = await client.audio.transcriptions.create(
            file=('demo', audio_file, 'audio/ogg'), model='gpt-4o-mini-transcribe', response_format='text'
        )

    except OpenAIError as error:
        logger.error('Provider error, please try again later', error=error)

        raise Exception('Provider error, please try again later')

    return response
