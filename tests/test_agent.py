from taskpilot.agent import TaskAgent
from taskpilot.llm_client import LLMReply, LLMServiceError, ToolCall
from taskpilot.models import Task


class MockLLM:
    def __init__(self, replies): self.replies = iter(replies)
    def complete(self, messages, tools): return next(self.replies)


def test_agent_executes_mocked_tool_then_returns_final_message():
    llm = MockLLM([LLMReply(None, [ToolCall("call-1", "rank_tasks", "{}")]), LLMReply("Start with the due task.", [])])
    result = TaskAgent(llm).run([Task(title="Assignment")])
    assert result.activity[0]["tool"] == "rank_tasks"
    assert result.checklist and result.final_message == "Start with the due task."


def test_agent_stops_at_configured_limit():
    loop = LLMReply(None, [ToolCall("call", "find_missing_details", "{}")])
    result = TaskAgent(MockLLM([loop, loop]), max_steps=2).run([Task(title="Assignment")])
    assert result.stopped_at_limit is True


def test_agent_handles_empty_tasks_without_calling_llm():
    result = TaskAgent(MockLLM([])).run([])
    assert result.checklist == []


def test_api_error_is_exposed_by_client_boundary():
    class FailingLLM:
        def complete(self, messages, tools): raise LLMServiceError("rate limited")
    import pytest
    with pytest.raises(LLMServiceError):
        TaskAgent(FailingLLM()).run([Task(title="Assignment")])

