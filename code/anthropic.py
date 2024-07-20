import httpx
from httpx import HTTPError
from zimran.http_client import AsyncHttpClient

PROMPT = """
You are tasked with improving the grammar and clarity of a given text while preserving its original meaning. Here is the text you need to correct:

<original_text>
{text}
</original_text>

Your task is to rewrite this text into a clear, grammatically correct version while maintaining the original meaning as closely as possible. Follow these steps:

1. Carefully read the original text to fully understand its meaning and intent.
2. Identify any spelling mistakes, punctuation errors, verb tense issues, word choice problems, and other grammatical mistakes.
3. Rewrite the text, correcting all identified errors while preserving the original meaning.
4. Ensure that the corrected version is clear and easily understandable.
5. Double-check that you haven't altered the original meaning or added any new information.

When correcting the text, pay attention to:
- Proper capitalization
- Correct punctuation usage
- Subject-verb agreement
- Consistent verb tenses
- Appropriate word choice
- Sentence structure and clarity

Your goal is to improve the text's grammar and clarity without changing its core message or adding new information. You may make minor changes to the text structure if necessary to improve clarity, but be careful not to alter the original meaning.

Provide only the corrected text in your answer, without any explanations or comments.

Always answer in the same language as the original text.
"""


class Anthropic(AsyncHttpClient):
    def __init__(self: 'Anthropic', api_key: str) -> None:
        super().__init__(base_url='https://api.anthropic.com')

        self.api_key = api_key

    @property
    def headers(self: 'Anthropic') -> dict:
        return {
            'x-api-key': self.api_key,
            'anthropic-version': '2023-06-01',
            'content-type': 'application/json',
        }

    async def messages(self: 'Anthropic', content: str) -> str:
        payload = {
            'model': 'claude-3-5-sonnet-20240620',
            'messages': [{'role': 'user', 'content': PROMPT.format(text=content)}],
            'max_tokens': 100,
            'temperature': 0.1,
        }

        try:
            response: httpx.Response = await self.post('/v1/messages', json=payload, headers=self.headers)

            response.raise_for_status()

        except HTTPError as error:
            raise ValueError(f'An error occurred: {error}')

        data = response.json()

        return data['content'][0]['text']
