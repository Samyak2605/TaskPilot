from datetime import date, timedelta

from taskpilot.models import Priority, Task
from taskpilot.prioritization import find_missing_details, rank_tasks

TODAY = date(2026, 11, 17)


def test_overdue_ranks_before_normal_task():
    tasks = [Task(title="Later", due_date=TODAY + timedelta(days=8)), Task(title="Late", due_date=TODAY - timedelta(days=1))]
    assert rank_tasks(tasks, TODAY)[0].task.title == "Late"


def test_tomorrow_receives_expected_urgency():
    result = rank_tasks([Task(title="Due soon", due_date=TODAY + timedelta(days=1), priority=Priority.MEDIUM)], TODAY)[0]
    assert result.score == 98


def test_missing_deadline_is_warning_not_blocker():
    task = Task(title="No date")
    assert rank_tasks([task], TODAY)[0].score == 33
    assert any(w.field == "due_date" for w in find_missing_details([task]))


def test_same_urgency_uses_lower_effort_as_tiebreaker():
    tasks = [Task(title="Long", due_date=TODAY + timedelta(days=2), estimated_minutes=90), Task(title="Short", due_date=TODAY + timedelta(days=2), estimated_minutes=30)]
    assert rank_tasks(tasks, TODAY)[0].task.title == "Short"


def test_empty_list_is_valid():
    assert rank_tasks([], TODAY) == []

