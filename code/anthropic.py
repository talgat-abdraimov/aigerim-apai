import httpx
from httpx import HTTPError
from zimran.http_client import AsyncHttpClient

PROMPT_MAPPER = {
    'grammar': """You are tasked with improving the grammar and clarity of a given text while preserving its original meaning. Here is the text you need to correct:
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
                """,
    'paraphrase': """
        You are tasked with rewriting a given text in your own words while maintaining its original meaning. This process is often called paraphrasing. Here is the original text you need to rewrite:

        <original_text>
        {text}
        </original_text>

        Your goal is to create a new version of this text that expresses the same ideas and information, but uses different words and sentence structures. Follow these guidelines:

        1. Understand the original text thoroughly before beginning to rewrite.
        2. Maintain the original meaning and key points of the text.
        3. Use your own words and phrasing as much as possible.
        4. Keep the same tone and style (formal, casual, technical, etc.) as the original.
        5. Ensure the rewritten text flows naturally and is coherent.
        6. Do not add new information or omit important details from the original.
        7. If there are any specialized terms or proper nouns that cannot be changed, keep them as they are.

        Provide only the corrected text in your answer, without any explanations or comments.

        Here are some additional tips to help you effectively rewrite the text:

        - Start by identifying the main ideas and key points of the original text.
        - Consider changing the sentence structure (e.g., combining or splitting sentences, changing from active to passive voice or vice versa).
        - Use synonyms and alternative phrases where appropriate.
        - Rearrange the order of ideas if it helps to improve flow, but ensure the logical progression is maintained.
        - Read your rewritten text to ensure it captures the essence of the original and sounds natural.

        Remember, the goal is to create a new text that conveys the same information and ideas as the original, but in a fresh way using your own words.

    """,
    'summarize': """
        You are tasked with summarizing a given text into a maximum of 10 bullet points. Here's the text you need to summarize:

        <text_to_summarize>
        {text}
        </text_to_summarize>

        Please follow these steps to create your summary:

        1. Carefully read and analyze the entire text.
        2. Identify the main ideas, key points, and essential information.
        3. Create concise bullet points that capture these main ideas and key information.
        4. Ensure that each bullet point is clear, informative, and directly related to the content of the text.
        5. Limit your summary to a maximum of 10 bullet points. If the text is short or simple, you may use fewer bullet points, but never exceed 10.
        6. Use the same language as the original text for your summary.
        7. Avoid repetition and try to cover different aspects of the text in each bullet point.
        8. If the text contains numerical data or statistics, include the most significant ones in your summary.

        Provide only the summarized text in your answer, without any explanations or comments. Each bullet point should be on a new line and start with a • character.

        Remember, your goal is to provide a concise yet comprehensive overview of the text that captures its essence and main points.
    """,
}


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

    async def messages(self: 'Anthropic', prompt_name: str, content: str) -> str:
        content = PROMPT_MAPPER[prompt_name].format(text=content)

        payload = {
            'model': 'claude-3-5-sonnet-20240620',
            'messages': [{'role': 'user', 'content': content}],
            'max_tokens': 500,
            'temperature': 0.1,
        }

        response: httpx.Response = await self.post('/v1/messages', json=payload, headers=self.headers)

        try:
            response.raise_for_status()

        except HTTPError:
            if response.status_code == 529:
                raise ValueError('API rate limit exceeded. Please try again later')

            raise ValueError('An error occurred. Please try again later')

        data = response.json()

        return data['content'][0]['text']
