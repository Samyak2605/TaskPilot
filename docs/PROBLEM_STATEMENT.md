# CHECKPOINT 1 — PROBLEM STATEMENT

## TaskPilot: Agentic AI-Powered Task Prioritization and Study Planner

### Problem, relevance, and users

Students receive assignments, practicals, exams, projects, revision work, and personal tasks in mixed notes and messages. A manual list does not reveal urgency, effort, or missing information. The resulting uncertainty can delay the work that matters most. TaskPilot targets college students who need a short, explainable plan from a natural-language task note.

### Current approach and proposed solution

The typical approach is an unstructured note, mental sorting, or a manually maintained checklist. TaskPilot accepts structured tasks in its core stage and natural language in its enhanced stage. It shows extracted tasks for human correction, computes a transparent rank, flags gaps, and returns an ordered checklist.

### Baseline and enhancement

**Existing/core baseline being implemented in this new repository:** title, description, optional deadline/effort/priority, task list, deterministic Python sorting, and a simple interface. It is not represented as a previously deployed application.

**Agentic AI enhancement:** a Groq model extracts tasks, an LLM selects from approved function schemas, Python executes local tools, tool observations return to the model, and a bounded loop produces the final recommendation. Agentic AI is appropriate because it adds controlled multi-step routing to flexible language input; deterministic Python retains responsibility for numeric priorities.

### Main functions and objectives

- Capture and validate up to 20 tasks.
- Extract task data from natural English without inventing unknown facts.
- Let users review and correct data.
- Prioritize transparently, identify missing information, and explain results.
- Demonstrate controlled tool selection, execution, observation, and error handling.

### Scope

Version one includes task entry, extraction, review/editing, local ranking and warning tools, Streamlit presentation, offline demo, tests, and documentation. It excludes authentication, persistence, payments, calendar APIs, RAG, multiple agents, cloud deployment, and notifications.

### Expected outcomes and success criteria

Students can see an ordered list and reason for every rank. Success means a valid task list can be reviewed, local ranking works even with missing deadlines, warnings are shown, model-chosen calls remain restricted to the registry, the agent cannot loop indefinitely, and tests demonstrate the critical paths. This project makes no claims about surveys, productivity gains, or research statistics.

