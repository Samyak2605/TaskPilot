# Development Blog

## 2026-11-17 — Building the first release

TaskPilot was selected as a focused educational Agentic AI project: students need help turning a note into a defensible next action, while the scope can remain small enough to explain. The first design decision was to preserve a non-agentic core. Streamlit was selected for a single-file Python UI and fast review/editing flow. Python owns the score calculation because scores should be reproducible; the LLM is used for language interpretation and tool routing instead.

The agent design uses Groq local function calling, rather than an agent framework. It gives the model three schemas while keeping execution inside a small allowlisted registry. Pydantic validates both user/model task data and tool arguments. Observations become tool messages; four steps cap the loop. The UI deliberately does not show private reasoning, only calls and returned local data.

An offline demo was added because an API key is not available in a fresh repository. It is deliberately labelled deterministic and does not pretend to be AI extraction or agent tool selection. Tests use a mocked LLM so they are independent of credentials. The actual test suite passed; Ruff encountered an execution-environment cache permission issue, recorded in testing notes. Future work includes live key validation, persistence, user feedback, and accessibility testing. This journal documents the current build only and does not invent earlier sessions, metrics, or commits.

