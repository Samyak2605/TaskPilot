"""Groq integration for extraction and agent tool selection."""

import json
from dataclasses import dataclass
from datetime import datetime
from typing import Any
from zoneinfo import ZoneInfo

from groq import Groq
from pydantic import ValidationError

from .config import Settings
from .models import Task


class LLMServiceError(RuntimeError):
    pass


@dataclass
class ToolCall:
    id: str
    name: str
    arguments: str


@dataclass
class LLMReply:
    content: str | None
    tool_calls: list[ToolCall]


class GroqClient:
    def __init__(self, settings: Settings):
        if not settings.groq_api_key:
            raise LLMServiceError("No GROQ_API_KEY is configured. Add it to .env, then try again.")
        self.settings = settings
        self.client = Groq(api_key=settings.groq_api_key, timeout=20.0, max_retries=1)

    def extract_tasks(self, text: str) -> list[Task]:
        today = datetime.now(ZoneInfo(self.settings.timezone)).date().isoformat()
        prompt = f"""Extract up to 20 actionable study/productivity tasks from the user's text. Today in {self.settings.timezone} is {today}. Return JSON only in this shape: {{\"tasks\": [{{\"title\": str, \"description\": str|null, \"due_date\": YYYY-MM-DD|null, \"estimated_minutes\": int|null, \"priority\": low|medium|high}}]}}. Do not invent missing facts. If a relative date is ambiguous, use null. User text: {text}"""
        try:
            response = self.client.chat.completions.create(model=self.settings.groq_model, messages=[{"role": "system", "content": "You extract task data carefully."}, {"role": "user", "content": prompt}], response_format={"type": "json_object"}, temperature=0)
            payload = json.loads(response.choices[0].message.content or "{}")
            return [Task.model_validate(item) for item in payload.get("tasks", [])]
        except (json.JSONDecodeError, ValidationError, Exception) as exc:
            if isinstance(exc, (json.JSONDecodeError, ValidationError)):
                raise LLMServiceError(f"The model returned invalid task data: {exc}") from exc
            raise LLMServiceError(f"Groq task extraction failed: {exc}") from exc

    def complete(self, messages: list[dict[str, Any]], tools: list[dict[str, Any]]) -> LLMReply:
        try:
            response = self.client.chat.completions.create(model=self.settings.groq_model, messages=messages, tools=tools, tool_choice="auto", temperature=0)
            message = response.choices[0].message
            calls = [ToolCall(id=call.id, name=call.function.name, arguments=call.function.arguments) for call in (message.tool_calls or [])]
            return LLMReply(content=message.content, tool_calls=calls)
        except Exception as exc:
            raise LLMServiceError(f"Groq agent request failed: {exc}") from exc

