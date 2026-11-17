"""Streamlit interface for TaskPilot."""


import streamlit as st
from pydantic import ValidationError

from taskpilot.agent import TaskAgent
from taskpilot.config import Settings
from taskpilot.demo import demo_extract
from taskpilot.llm_client import GroqClient, LLMServiceError
from taskpilot.models import Priority, Task
from taskpilot.prioritization import find_missing_details, rank_tasks

SAMPLE = "Finish my DBMS assignment by tomorrow, revise Operating Systems before Friday, prepare for my DSA quiz next week, and finish my Python project this weekend."


def _init_state() -> None:
    st.session_state.setdefault("tasks", [])
    st.session_state.setdefault("result", None)
    st.session_state.setdefault("source", "")


def _as_rows(tasks: list[Task]) -> list[dict]:
    return [{"title": task.title, "description": task.description or "", "due_date": task.due_date, "estimated_minutes": task.estimated_minutes, "priority": task.priority.value} for task in tasks]


def _parse_rows(rows: list[dict]) -> list[Task]:
    return [Task.model_validate({**row, "description": row.get("description") or None, "due_date": row.get("due_date") or None, "estimated_minutes": row.get("estimated_minutes") or None}) for row in rows if str(row.get("title", "")).strip()]


def _show_results(result) -> None:
    checklist = result.checklist
    urgent = sum(item.score >= 90 for item in checklist)
    missing = sum(len(item.warnings) for item in checklist)
    effort = sum(item.task.estimated_minutes or 0 for item in checklist)
    a, b, c, d = st.columns(4)
    a.metric("Tasks", len(checklist)); b.metric("Urgent", urgent); c.metric("Details to add", missing); d.metric("Known effort", f"{effort} min")
    st.subheader("Your prioritized checklist")
    for position, item in enumerate(checklist, 1):
        task = item.task
        label = f"{position}. {task.title}  ·  {item.score}/115"
        with st.container(border=True):
            st.markdown(f"**{label}**")
            st.caption(f"{task.priority.value.title()} priority · Deadline: {task.due_date or 'Not specified'} · Effort: {str(task.estimated_minutes) + ' min' if task.estimated_minutes else 'Not specified'}")
            st.write(item.explanation)
            for warning in item.warnings:
                st.warning(warning.message, icon="⚠️")
    st.info(result.final_message)
    with st.expander("Agent activity trace"):
        if result.activity:
            for event in result.activity:
                st.markdown(f"**Step {event['step']} — `{event['tool']}`:** {event['status']}")
                st.json(event["result"], expanded=False)
        else:
            st.write("Offline demo used deterministic local tools. No LLM tool selection occurred.")


st.set_page_config(page_title="TaskPilot", page_icon="✦", layout="wide")
st.markdown("""<style>
.block-container {max-width: 1080px; padding-top: 2.5rem;} h1 {color: #233baf;} div[data-testid='stMetric'] {background: #f5f7ff; border-radius: 14px; padding: 12px;}
</style>""", unsafe_allow_html=True)
_init_state()
settings = Settings.from_env()

st.title("TaskPilot ✦")
st.subheader("Your AI-powered study and productivity planner.")
st.write("Describe what you need to do in everyday language. Review the extracted tasks, then let a controlled AI agent select local planning tools.")

with st.container(border=True):
    text = st.text_area("What do you need to complete?", placeholder="Tell TaskPilot what you need to complete. For example: Finish my DBMS assignment by tomorrow, revise OS by Friday, and prepare for my DSA quiz next week.", height=145, key="input")
    left, middle, right = st.columns([2, 2, 1])
    extract = left.button("Extract tasks", type="primary", use_container_width=True)
    sample = middle.button("Load sample tasks", use_container_width=True)
    clear = right.button("Clear", use_container_width=True)

if clear:
    st.session_state.tasks, st.session_state.result, st.session_state.input = [], None, ""
    st.rerun()
if sample:
    st.session_state.input = SAMPLE
    st.rerun()
if extract:
    if not text.strip():
        st.warning("Enter a task description first.")
    else:
        try:
            if settings.groq_api_key:
                st.session_state.tasks = GroqClient(settings).extract_tasks(text)
                st.session_state.source = "LLM extraction via Groq"
            else:
                st.session_state.tasks = demo_extract(text)
                st.session_state.source = "Deterministic offline demo — not LLM extraction"
            st.session_state.result = None
            if not st.session_state.tasks:
                st.warning("No actionable tasks were extracted. Please try more specific wording.")
        except LLMServiceError as exc:
            st.error(str(exc))

if st.session_state.tasks:
    st.subheader("Review extracted tasks")
    st.caption(st.session_state.source)
    edited = st.data_editor(_as_rows(st.session_state.tasks), num_rows="dynamic", use_container_width=True, key="task_editor", column_config={"priority": st.column_config.SelectboxColumn(options=[p.value for p in Priority]), "due_date": st.column_config.DateColumn(format="YYYY-MM-DD"), "estimated_minutes": st.column_config.NumberColumn(min_value=1, max_value=1440)})
    try:
        st.session_state.tasks = _parse_rows(edited)
    except ValidationError as exc:
        st.error(f"Please correct the task details: {exc.errors()[0]['msg']}")
    if st.button("Run Agentic AI prioritization", type="primary", use_container_width=True):
        if not st.session_state.tasks:
            st.warning("Keep at least one valid task.")
        elif not settings.groq_api_key:
            st.info("Offline demo mode is active. It runs the same deterministic ranking and warning tools, but does not claim LLM tool selection.")
            ranked = rank_tasks(st.session_state.tasks)
            from taskpilot.models import AgentResult
            st.session_state.result = AgentResult(checklist=ranked, final_message="Offline demo complete. Add GROQ_API_KEY to enable live LLM extraction and agent tool selection.", activity=[])
        else:
            try:
                with st.spinner("The agent is selecting and running approved local tools…"):
                    st.session_state.result = TaskAgent(GroqClient(settings), settings.agent_max_steps).run(st.session_state.tasks)
            except LLMServiceError as exc:
                st.error(str(exc))

if st.session_state.result:
    _show_results(st.session_state.result)
elif st.session_state.tasks:
    warnings = find_missing_details(st.session_state.tasks)
    if warnings:
        st.caption(f"{len(warnings)} detail(s) can be improved before prioritization.")

with st.expander("Example inputs"):
    st.markdown("- **Urgent:** `Submit my DBMS assignment by tomorrow, high priority.`\n- **Different deadlines:** `Revise OS by Friday and finish Python project next week.`\n- **No deadline:** `Organize my project notes.`\n- **Similar urgency:** `Prepare DSA quiz by Friday and finish networks lab by Friday.`\n- **Unclear:** `Work on that thing for class.`")

