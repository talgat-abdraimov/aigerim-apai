import asyncio
from functools import lru_cache

import language_tool_python


@lru_cache(maxsize=1)
def get_tool() -> language_tool_python.LanguageTool:
    """Return cached LanguageTool instance."""
    return language_tool_python.LanguageTool('auto')


async def correct_text(text: str) -> str:
    """Correct text using LanguageTool."""
    tool = get_tool()
    matches = await asyncio.to_thread(tool.check, text)
    return language_tool_python.utils.correct(text, matches)
