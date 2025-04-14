import os
from dataclasses import dataclass


@dataclass
class Settings:
    bot_token: str
    openai_api_key: str
    sentry_dsn: str | None = None

    @staticmethod
    def from_env() -> 'Settings':
        return Settings(
            bot_token=os.getenv('BOT_TOKEN'),
            sentry_dsn=os.getenv('SENTRY_DSN'),
            openai_api_key=os.getenv('OPENAI_API_KEY'),
        )

    def __post_init__(self: 'Settings') -> None:
        if not self.bot_token:
            raise ValueError('BOT_TOKEN is required')

        if not self.openai_api_key:
            raise ValueError('OPENAI_API_KEY is required')


settings = Settings.from_env()
