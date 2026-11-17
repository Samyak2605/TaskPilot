"""Allowlisted local functions and their LLM-visible schemas."""

import json
from datetime import date
from typing import Any, ClassVar

from pydantic import BaseModel, ConfigDict, Field, ValidationError

from .models import RankedTask, Task
from .prioritization import find_missing_details, rank_tasks


class ToolArguments(BaseModel):
    model_config = ConfigDict(extra="forbid")
    tasks: list[Task] | None = Field(default=None, max_length=20)


TOOL_SCHEMAS = [
    {"type": "function", "function": {"name": "rank_tasks", "description": "Rank the supplied student tasks with TaskPilot's deterministic deadline and stated-priority rules.", "parameters": ToolArguments.model_json_schema()}},
    {"type": "function", "function": {"name": "find_missing_details", "description": "Find absent or unclear deadline, effort, and description details in the supplied tasks.", "parameters": ToolArguments.model_json_schema()}},
    {"type": "function", "function": {"name": "format_checklist", "description": "Format the processed tasks as a clean checklist after ranking and warnings have been obtained.", "parameters": ToolArguments.model_json_schema()}},
]


class ToolRegistry:
    """Executes only the three named local functions; never arbitrary model code."""

    allowed_tools: ClassVar[set[str]] = {"rank_tasks", "find_missing_details", "format_checklist"}

    def __init__(self, today: date | None = None):
        self.today = today
        self.ranked: list[RankedTask] = []
        self.warnings: list[dict[str, Any]] = []

    def execute(self, name: str, raw_arguments: str | dict[str, Any], context_tasks: list[Task]) -> dict[str, Any]:
        if name not in self.allowed_tools:
            raise ValueError(f"Unknown or disallowed tool: {name}")
        try:
            data = json.loads(raw_arguments) if isinstance(raw_arguments, str) else raw_arguments
            args = ToolArguments.model_validate(data)
        except (json.JSONDecodeError, ValidationError) as exc:
            raise ValueError(f"Invalid arguments for {name}: {exc}") from exc
        tasks = args.tasks if args.tasks is not None else context_tasks
        if name == "rank_tasks":
            self.ranked = rank_tasks(tasks, self.today)
            return {"ranked_tasks": [item.model_dump(mode="json") for item in self.ranked]}
        if name == "find_missing_details":
            self.warnings = [warning.model_dump() for warning in find_missing_details(tasks)]
            return {"warnings": self.warnings}
        source = self.ranked or rank_tasks(tasks, self.today)
        return {"checklist": [item.model_dump(mode="json") for item in source]}

