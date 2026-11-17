import pytest

from taskpilot.models import Task
from taskpilot.tools import ToolRegistry


def test_registry_executes_rank_tool():
    output = ToolRegistry().execute("rank_tasks", "{}", [Task(title="Study")])
    assert len(output["ranked_tasks"]) == 1


def test_unknown_tool_is_rejected():
    with pytest.raises(ValueError, match="Unknown"):
        ToolRegistry().execute("delete_everything", "{}", [Task(title="Study")])


def test_invalid_tool_arguments_are_rejected():
    with pytest.raises(ValueError, match="Invalid arguments"):
        ToolRegistry().execute("rank_tasks", "{bad json", [Task(title="Study")])

