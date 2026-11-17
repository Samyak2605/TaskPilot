"""Transparent deterministic TaskPilot Core priority rules."""

from datetime import date

from .models import MissingDetail, Priority, RankedTask, Task

PRIORITY_BONUS = {Priority.HIGH: 15, Priority.MEDIUM: 8, Priority.LOW: 0}


def urgency_points(due_date: date | None, today: date) -> tuple[int, str]:
    if due_date is None:
        return 25, "No deadline supplied"
    days = (due_date - today).days
    if days < 0:
        return 100, f"Overdue by {abs(days)} day(s)"
    if days <= 1:
        return 90, "Due within one day"
    if days <= 3:
        return 75, "Due in two to three days"
    if days <= 7:
        return 60, "Due within one week"
    return 40, "Due after one week"


def find_missing_details(tasks: list[Task]) -> list[MissingDetail]:
    warnings: list[MissingDetail] = []
    for task in tasks:
        if task.due_date is None:
            warnings.append(MissingDetail(task_id=task.id, task_title=task.title, field="due_date", message="Add a deadline for a more accurate ranking."))
        if task.estimated_minutes is None:
            warnings.append(MissingDetail(task_id=task.id, task_title=task.title, field="estimated_minutes", message="Add an effort estimate to improve planning."))
        if not task.description or len(task.description.strip()) < 8:
            warnings.append(MissingDetail(task_id=task.id, task_title=task.title, field="description", message="Add a little more detail so the task is easier to act on."))
    return warnings


def rank_tasks(tasks: list[Task], today: date | None = None) -> list[RankedTask]:
    """Rank tasks using documented urgency plus explicit priority only."""
    today = today or date.today()
    warnings = find_missing_details(tasks)
    by_id: dict[str, list[MissingDetail]] = {}
    for warning in warnings:
        by_id.setdefault(warning.task_id, []).append(warning)
    ranked: list[RankedTask] = []
    for task in tasks:
        urgency, deadline_explanation = urgency_points(task.due_date, today)
        score = urgency + PRIORITY_BONUS[task.priority]
        effort_note = f"; {task.estimated_minutes} min estimate" if task.estimated_minutes else ""
        ranked.append(RankedTask(
            task=task.model_copy(update={"urgency_score": score}), score=score,
            explanation=f"{deadline_explanation}; {task.priority.value} priority (+{PRIORITY_BONUS[task.priority]}){effort_note}.",
            warnings=by_id.get(task.id, []),
        ))
    # Lower effort wins only for equal score so it is a minor, visible tie-breaker.
    return sorted(ranked, key=lambda item: (-item.score, item.task.estimated_minutes or 10**9, item.task.title.lower()))

