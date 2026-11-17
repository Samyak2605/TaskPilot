# Baseline and Agentic AI Enhancement

TaskPilot is newly implemented in two visible stages; the baseline is not a claim of a prior deployed product.

| Capability | TaskPilot Core baseline | Agentic AI enhancement |
|---|---|---|
| Input | Structured task records | Natural English plus structured records |
| Understanding | User supplies fields | Groq extracts proposed fields |
| Decision | Python sorts by fixed rules | LLM selects which approved tool to request |
| Execution | Direct Python functions | Validated local tool registry and observations |
| Output | Ordered list | Explained checklist plus activity trace |
| Safety | Model validation | Validation, allowlist, bounded loop, no arbitrary code |

The baseline remains essential: `prioritization.py` calculates scores consistently. The enhancement does not delegate numerical rules to a model; it makes the interaction agentic by letting the LLM decide which registered local functions to use and by continuing after tool observations.

