
import pytest
from pydantic import ValidationError

from taskpilot.models import Task


def test_valid_task_keeps_optional_deadline_optional():
    task = Task(title="Read notes")
    assert task.due_date is None


def test_invalid_date_is_rejected():
    with pytest.raises(ValidationError):
        Task(title="Invalid", due_date="not-a-date")


def test_blank_title_is_rejected():
    with pytest.raises(ValidationError):
        Task(title="   ")

