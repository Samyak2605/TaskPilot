# CHECKPOINT 3 — Agentic AI / Backend Concepts

TaskPilot uses a single, controlled agent—not a generic chatbot. The Groq model sees tool schemas and validated task context. `TaskAgent.run` asks it to select functions; `ToolRegistry.execute` validates the name and JSON/Pydantic arguments; the local function runs; the serialized result is appended as a tool observation; the model may choose another call. The loop is limited by `AGENT_MAX_STEPS`.

| Concept | Real TaskPilot implementation |
|---|---|
| LLM understanding | `GroqClient.extract_tasks` asks Groq for JSON task candidates using the configured local date/timezone. |
| Structured validation | `Task` rejects blank titles, invalid dates, out-of-range effort, and extra fields. |
| Function calling | `TOOL_SCHEMAS` exposes `rank_tasks`, `find_missing_details`, and `format_checklist`. |
| Tool selection | The model returns a named structured tool call; Python does not use a hardcoded if/else route to choose it. |
| Tool execution | The registry runs only prewritten local Python functions. |
| Observation | The JSON local result is sent back in a `role: tool` message. |
| Bounded decisions | `max_steps`, default 4, stops repeated calls safely. |
| Deterministic rules | `rank_tasks` calculates deadline points + explicit priority bonus, not LLM scores. |
| Error handling | Invalid JSON/arguments and unknown tools are rejected; Groq errors reach the UI as clear messages. |

No `eval`, shell execution, arbitrary Python, external agent framework, or unrestricted tools are exposed to the model.

