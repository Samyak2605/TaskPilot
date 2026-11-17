# Testing and Results

## Actual run — 2026-11-17

Command: `.venv/bin/python -m pytest -q`

Result: **15 passed** in 0.14s with pytest's cache provider disabled for the restricted execution environment. The check covered normal ranking, due-tomorrow, overdue, missing-deadline, similar-deadline, empty list, invalid date, blank title, invalid tool JSON, unknown tool, registry execution, successful mocked agent tool execution, maximum-loop stop, empty agent input, and mocked API error propagation.

`ruff check --no-cache .` was run after its safe formatting fixes and passed with no findings. The no-cache option avoids the restricted execution environment's cache limitation.

The live Groq path was not executed because no API credential was supplied. It is covered at the orchestration boundary through mocked LLM responses; live validation remains a manual post-key step. No result is claimed for it.

