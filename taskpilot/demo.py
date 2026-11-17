"""Clearly-labelled deterministic demo extraction for no-key demonstrations."""

import re
from datetime import date, timedelta

from .models import Priority, Task


def demo_extract(text: str, today: date | None = None) -> list[Task]:
    """Small predictable parser for the offline demo only; it is not LLM extraction."""
    today = today or date.today()
    clauses = [part.strip(" .") for part in re.split(r",(?: and)?|\band\b", text, flags=re.IGNORECASE) if part.strip()]
    tasks: list[Task] = []
    for clause in clauses[:20]:
        due = None
        lowered = clause.lower()
        if "tomorrow" in lowered:
            due = today + timedelta(days=1)
        elif "next week" in lowered:
            due = today + timedelta(days=7)
        elif "this weekend" in lowered:
            due = today + timedelta(days=(5 - today.weekday()) % 7)
        priority = Priority.HIGH if any(word in lowered for word in ["urgent", "important", "high priority"]) else Priority.MEDIUM
        title = re.sub(r"\b(by|before)\s+(tomorrow|next week|this weekend)\b.*", "", clause, flags=re.IGNORECASE).strip()
        title = re.sub(r"^(i have to|i need to|please)\s+", "", title, flags=re.IGNORECASE)
        if title:
            tasks.append(Task(title=title.capitalize(), due_date=due, priority=priority))
    return tasks

