"""Configuration loaded safely from environment variables."""

import os
from dataclasses import dataclass

from dotenv import load_dotenv


@dataclass(frozen=True)
class Settings:
    groq_api_key: str | None
    groq_model: str = "openai/gpt-oss-20b"
    timezone: str = "Asia/Kolkata"
    agent_max_steps: int = 4

    @classmethod
    def from_env(cls) -> "Settings":
        load_dotenv()
        raw_steps = os.getenv("AGENT_MAX_STEPS", "4")
        try:
            steps = max(1, min(int(raw_steps), 8))
        except ValueError:
            steps = 4
        return cls(
            groq_api_key=os.getenv("GROQ_API_KEY") or None,
            groq_model=os.getenv("GROQ_MODEL", "openai/gpt-oss-20b"),
            timezone=os.getenv("APP_TIMEZONE", "Asia/Kolkata"),
            agent_max_steps=steps,
        )

