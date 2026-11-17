# Assessment Preparation

1. **What is Agentic AI?** An LLM system that can decide actions, call tools, observe results, and continue toward an outcome under controls.
2. **How is it different from a chatbot?** A chatbot normally only generates text; TaskPilot’s LLM requests registered actions and receives their results.
3. **What makes TaskPilot agentic?** The `TaskAgent` performs model-selected local calls, returns observations, and supports multiple bounded rounds.
4. **What is function calling?** An API mechanism where the model returns a structured request for a named function and arguments.
5. **How does the LLM decide?** It sees the tool descriptions and validated task context and returns a tool call.
6. **What is a tool schema?** A machine-readable name, description, and JSON argument contract in `TOOL_SCHEMAS`.
7. **What is orchestration?** `TaskAgent.run` coordinates prompt, tool-call parsing, execution, observations, and stopping.
8. **What is an observation?** A local tool result returned to the model in a `tool` message.
9. **Role of LLM?** Extract language and select/interpret tool workflow; it does not calculate scores.
10. **Role of Python?** Validate data, execute safe tools, compute rankings, and render the app.
11. **Why deterministic ranking?** Scores are transparent, repeatable, and do not depend on model hallucinations.
12. **Why Pydantic?** It rejects bad task/tool data before it reaches planning code.
13. **Missing deadlines?** TaskPilot ranks them with 25 urgency points and warns the user; it never invents a date.
14. **Prevent arbitrary execution?** A fixed allowlist accepts only three local functions; there is no `eval` or shell path.
15. **Prevent infinite loops?** `AGENT_MAX_STEPS`, default four, ends the loop.
16. **API key protection?** It is read from `.env`, ignored by Git, and not displayed in logs.
17. **Errors?** Groq and validation errors become controlled messages; bad calls are rejected.
18. **Testing?** Pytest unit tests validate models/rules/tools and mocked agent integration without a key.
19. **Limitations?** No persistent storage; real language quality depends on model; ambiguous dates remain blank.
20. **Future extension?** Add user-approved persistence/calendar links, reminders, accessibility checks, and user evaluation.

