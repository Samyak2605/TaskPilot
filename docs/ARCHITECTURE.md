# Architecture

```mermaid
sequenceDiagram
  participant S as Student
  participant UI as Streamlit UI
  participant G as Groq
  participant A as TaskAgent
  participant T as Local ToolRegistry
  S->>UI: Natural-language task note
  UI->>G: Structured extraction request
  G-->>UI: JSON task candidates
  UI->>UI: Pydantic validation and editable review
  UI->>A: Validated tasks
  A->>G: Tool schemas + task context
  G-->>A: Tool call request
  A->>T: Allowlisted, validated call
  T-->>A: Observation
  A->>G: Tool observation
  G-->>A: More calls or final recommendation
  A-->>UI: Checklist and non-private activity log
```

The UI is `app.py`. `llm_client.py` owns Groq requests. `agent.py` is the bounded orchestrator. `tools.py` is the allowlisted local registry. `models.py` validates data before execution, and `prioritization.py` owns transparent scoring. A no-key UI path uses only deterministic local code and labels itself accordingly.

