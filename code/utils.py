from loguru import logger
from openai import APIConnectionError, APIStatusError, AsyncOpenAI, RateLimitError

from config import settings

openai = AsyncOpenAI(api_key=settings.openai_api_key)


async def get_completion(prompt: str, text: str) -> str:
    try:
        completion = await openai.chat.completions.create(
            messages=[
                {'role': 'system', 'content': prompt},
                {'role': 'user', 'content': text},
            ],
            stream=True,
            model='gpt-4o-mini',
            temperature=0.1,
            max_tokens=500,
        )

        response = ''
        async for chunk in completion:
            content = chunk.choices[0].delta.content

            if isinstance(content, str) and content:
                response += content

        return response

    except APIConnectionError as e:
        logger.error('The server could not be reached', error_detail=e.__cause__)
        raise ValueError('The server could not be reached')

    except RateLimitError as e:
        logger.error('API rate limit exceeded', error_detail=e.__cause__)

        raise ValueError('API rate limit exceeded. Please try again later')

    except APIStatusError as e:
        logger.error('An error occurred', error_detail=e, status_code=e.status_code, response=e.response)

        raise ValueError('An error occurred. Please try again later')
