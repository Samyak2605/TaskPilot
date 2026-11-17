"""Bounded orchestration of Groq-selected, locally executed TaskPilot tools."""

import json
from typing import Any, Protocol

from .llm_client import LLMReply
from .models import AgentResult, Task
from .tools import TOOL_SCHEMAS, ToolRegistry


class AgentLLM(Protocol):
    def complete(self, messages: list[dict[str, Any]], tools: list[dict[str, Any]]) -> LLMReply: ...


class TaskAgent:
    def __init__(self, llm: AgentLLM, max_steps: int = 4, registry: ToolRegistry | None = None):
        self.llm, self.max_steps, self.registry = llm, max_steps, registry or ToolRegistry()

    def run(self, tasks: list[Task]) -> AgentResult:
        if not tasks:
            return AgentResult(checklist=[], final_message="Add at least one task before prioritizing.", activity=[])
        compact = [task.model_dump(mode="json") for task in tasks]
        messages: list[dict[str, Any]] = [
            {"role": "system", "content": "You are TaskPilot's routing agent. Decide which of the provided local tools to call. Use rank_tasks and find_missing_details before format_checklist when useful. Tool arguments may be {} because the validated task context is supplied below. Never claim a tool ran unless you called it. Give a short user-facing recommendation after tools finish."},
            {"role": "user", "content": f"Validated task context: {json.dumps(compact)}"},
        ]
        activity: list[dict[str, Any]] = []
        final_message = ""
        for step in range(self.max_steps):
            reply = self.llm.complete(messages, TOOL_SCHEMAS)
            assistant_message: dict[str, Any] = {"role": "assistant", "content": reply.content or ""}
            if reply.tool_calls:
                assistant_message["tool_calls"] = [{"id": call.id, "type": "function", "function": {"name": call.name, "arguments": call.arguments}} for call in reply.tool_calls]
            messages.append(assistant_message)
            if not reply.tool_calls:
                final_message = reply.content or "The local task analysis is ready."
                return AgentResult(checklist=self.registry.ranked, final_message=final_message, activity=activity)
            for call in reply.tool_calls:
                try:
                    result = self.registry.execute(call.name, call.arguments, tasks)
                    activity.append({"step": step + 1, "tool": call.name, "status": "completed", "result": result})
                    content = json.dumps(result, default=str)
                except ValueError as exc:
                    content = json.dumps({"error": str(exc)})
                    activity.append({"step": step + 1, "tool": call.name, "status": "rejected", "result": {"error": str(exc)}})
                messages.append({"role": "tool", "tool_call_id": call.id, "name": call.name, "content": content})
        return AgentResult(checklist=self.registry.ranked, final_message="The agent stopped after the configured safety limit. The completed local results are shown below.", activity=activity, stopped_at_limit=True)

