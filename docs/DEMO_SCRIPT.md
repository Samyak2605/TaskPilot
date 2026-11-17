# Demonstration Script

1. “TaskPilot helps students decide what to work on first when their work is scattered in ordinary notes.”
2. “The baseline is a normal validated task list with transparent Python ranking. It is newly implemented here, not claimed as a previous product.”
3. Enter: “Finish my DBMS assignment by tomorrow, revise OS by Friday, and prepare for my DSA quiz next week.”
4. “With a Groq key, the LLM extracts a proposed structured list. I can correct every title, deadline, effort estimate, and priority before the agent runs.”
5. Click **Run Agentic AI prioritization**. “The LLM receives only the three defined local tool schemas and selects one. Python validates it, executes it locally, and returns the observation.”
6. Open **Agent activity trace** and point out selected tools and returned data, not hidden chain-of-thought.
7. Explain score: overdue 100, within one day 90, 2–3 days 75, 4–7 days 60, later 40, missing 25; high/medium/low add 15/8/0.
8. “The loop has a maximum of four rounds. Unknown tools, malformed arguments, and missing credentials are handled safely.”
9. “Offline demo mode is available without a key and clearly does not claim LLM selection.”
10. Close with limitations: no persistence/calendar and ambiguous dates are not fabricated.

