"""
INTERMEDIATE TASK 1: Multi-Tool Agent
Run:  streamlit run agent.py

v4 — Stats fix (root cause):
  Tools run inside asyncio.run() which spawns a new event loop.
  st.session_state is NOT reliably writable from that context.
  FIX: pass a plain Python dict (run_mem) to tools.
       After agent finishes, copy run_mem back into st.session_state.
       This is the only reliable pattern.
"""

from dotenv import load_dotenv
load_dotenv()

import asyncio
from pathlib import Path

import streamlit as st
from agents import Agent, Runner, RunConfig

from config.settings import get_model, get_model_settings, EXCEL_PATH
from tools import make_all_tools
from ui.styles import CSS
from ui.components import render_header, render_tool_card, render_badge_row, render_log_entries
from utils.db_helper import get_max_id, get_all_results

# ── Page config ────────────────────────────────────────────
st.set_page_config(
    page_title="Multi-Tool Agent",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.markdown(CSS, unsafe_allow_html=True)
st.markdown("""
<style>
[data-testid="collapsedControl"] { display: none !important; }
section[data-testid="stSidebar"]  { display: none !important; }
[data-testid="stHeader"]          { display: none !important; }
.block-container                  { padding-top: 2rem !important; }
</style>
""", unsafe_allow_html=True)

# ── Session state init ─────────────────────────────────────
for key, default in {
    "logs":                [],
    "search_count":        0,
    "save_count":          0,
    "email_count":         0,
    "session_start_db_id": None,
    "last_answer":         "",
}.items():
    if key not in st.session_state:
        st.session_state[key] = default

if st.session_state.session_start_db_id is None:
    st.session_state.session_start_db_id = get_max_id()

# ── Agent runner ───────────────────────────────────────────
def run_agent(prompt: str) -> tuple[str, dict]:
    """
    Run agent with a plain dict as shared memory.
    Returns (answer, run_mem) so caller can merge into session_state.
    """
    run_mem = {
        "search_count":        0,
        "save_count":          0,
        "email_count":         0,
        "logs":                [],
        "session_start_db_id": st.session_state.session_start_db_id,
    }

    def make_agent():
        return Agent(
            name="MultiToolAgent",
            instructions="""You are an intelligent research agent with three tools.

TOOLS:
  web_search(query)
  save_to_db(query, title, summary, url, tags)
  send_email(to_address, subject, body)

STRICT RULES:
  - ALWAYS call web_search first.
  - ALWAYS call save_to_db EXACTLY 5 TIMES — one call per unique finding.
    Never save fewer than 5 rows. If results are weak, search again with a simpler query.
  - Use WHATEVER search results are returned — never say "I couldn't find".
  - send_email: ONLY if user provided a recipient email address.
    - send_all_db=False → sends ONLY the rows saved in THIS session (current search)

WORKFLOW:
  1. web_search(topic)
  2. [if results < 5] web_search(broader/simpler topic) to get more findings
  3. save_to_db exactly 5 times — one unique finding per call
  4. send_email if recipient address was given
  5. Respond with structured summary

OUTPUT FORMAT:
  ## Summary
  [2-3 paragraphs]

  ## Key Findings
  - finding 1
  - finding 2
  - finding 3
  - finding 4
  - finding 5

  ## Saved to Database
  [confirm all 5 DB ids + Excel rows]""",
            tools=make_all_tools(run_mem),
            model=get_model(),
        )

    async def _run():
        result = await Runner.run(make_agent(), prompt, run_config=RunConfig(model_settings=get_model_settings()))
        return result.final_output

    answer = asyncio.run(_run())
    return answer, run_mem


# ══════════════════════════════════════════════════════════
#  UI
# ══════════════════════════════════════════════════════════

render_header()

# ── Live stat dashboard ────────────────────────────────────
sc = st.session_state.search_count
sv = st.session_state.save_count
em = st.session_state.email_count
lg = len(st.session_state.logs)

st.markdown(f"""
<div class="stat-grid">
  <div class="stat-box {'active' if sc > 0 else ''}">
    <div class="stat-value">{sc}</div>
    <div class="stat-label">Searches Run</div>
  </div>
  <div class="stat-box {'active' if sv > 0 else ''}">
    <div class="stat-value">{sv}</div>
    <div class="stat-label">Rows Saved to DB</div>
  </div>
  <div class="stat-box {'active' if em > 0 else ''}">
    <div class="stat-value">{em}</div>
    <div class="stat-label">Emails Sent</div>
  </div>
  <div class="stat-box {'active' if lg > 0 else ''}">
    <div class="stat-value">{lg}</div>
    <div class="stat-label">Agent Logs</div>
  </div>
</div>
""", unsafe_allow_html=True)

st.markdown("---")

input_col, output_col = st.columns([5, 4], gap="large")

# ── Input form ─────────────────────────────────────────────
with input_col:
    st.markdown('<div class="section-label">Research Query</div>', unsafe_allow_html=True)

    topic = st.text_input(
        "SEARCH TOPIC",
        placeholder="e.g.  AI in healthcare  |  Python frameworks  |  Climate change",
    )
    depth = st.selectbox(
        "RESEARCH DEPTH",
        ["Quick Overview", "Detailed Analysis", "Comprehensive Report"],
        index=1,
    )

    st.markdown('<div class="section-label" style="margin-top:1.2rem">Email (Optional)</div>',
                unsafe_allow_html=True)

    e1, e2 = st.columns([3, 2])
    with e1:
        recipient = st.text_input("RECIPIENT EMAIL", placeholder="someone@gmail.com")
    with e2:
        custom_subject = st.text_input("SUBJECT OVERRIDE", placeholder="Auto if empty")

    st.markdown('<div class="section-label" style="margin-top:1.2rem">Excel Tags</div>',
                unsafe_allow_html=True)
    tags = st.text_input("TAGS", placeholder="AI, research, 2024")

    st.markdown("<br>", unsafe_allow_html=True)

    btn_col1, btn_col2 = st.columns([3, 1])
    with btn_col1:
        run_btn = st.button("⚡  RUN AGENT", use_container_width=True)
    with btn_col2:
        clear_btn = st.button("CLEAR", use_container_width=True)

    if clear_btn:
        st.session_state.logs                = []
        st.session_state.search_count        = 0
        st.session_state.save_count          = 0
        st.session_state.email_count         = 0
        st.session_state.last_answer         = ""
        st.session_state.session_start_db_id = get_max_id()
        st.rerun()

# ── Output panel ───────────────────────────────────────────
with output_col:
    st.markdown('<div class="section-label">Agent Output</div>', unsafe_allow_html=True)
    output_slot = st.empty()

    if st.session_state.last_answer:
        with output_slot.container():
            render_tool_card("agent", "Agent Response", st.session_state.last_answer)
            render_badge_row(
                searched=st.session_state.search_count > 0,
                saved=st.session_state.save_count > 0,
                emailed=st.session_state.email_count > 0,
            )
            if Path(EXCEL_PATH).exists():
                st.markdown("<br>", unsafe_allow_html=True)
                with open(EXCEL_PATH, "rb") as f:
                    st.download_button(
                        label="⬇ DOWNLOAD EXCEL",
                        data=f.read(),
                        file_name=EXCEL_PATH,
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                        use_container_width=True,
                    )
    else:
        output_slot.markdown("""
        <div class="empty-state">
            Enter a topic and click RUN AGENT
            <span style="font-size:2.5rem;display:block;margin-top:0.5rem;opacity:0.2">⚡</span>
        </div>
        """, unsafe_allow_html=True)

# ── Agent run ──────────────────────────────────────────────
if run_btn:
    if not topic.strip():
        st.warning("Please enter a search topic.")
    else:
        depth_map = {
            "Quick Overview":       "Search once, save EXACTLY 5 key results, give a short summary.",
            "Detailed Analysis":    "Search the topic thoroughly, save EXACTLY 5 findings, give a detailed analysis.",
            "Comprehensive Report": "Search with multiple queries, save EXACTLY 5 findings, write a comprehensive report.",
        }
        parts = [f"Research this topic: '{topic.strip()}'", depth_map[depth]]
        if tags.strip():
            parts.append(f"Tag all saved DB rows with: {tags.strip()}")
        if recipient.strip():
            subj = custom_subject.strip() or f"Research Report: {topic.strip()[:50]}"
            parts.append(
                f"After saving, call send_email with: "
                f"to_address='{recipient.strip()}', subject='{subj}', "
                f"send_all_db=false, "
                f"and a professional body summarising the research findings."
            )

        with st.spinner("⚡ Agent running..."):
            try:
                answer, run_mem = run_agent(" ".join(parts))

                # ✅ MERGE run_mem back into session_state AFTER agent completes
                # This is the reliable way - no async context issues
                st.session_state.search_count  += run_mem.get("search_count", 0)
                st.session_state.save_count    += run_mem.get("save_count", 0)
                st.session_state.email_count   += run_mem.get("email_count", 0)
                st.session_state.logs          += run_mem.get("logs", [])
                st.session_state.last_answer    = answer

                st.rerun()  # re-render with updated stats

            except Exception as exc:
                with output_col:
                    with output_slot.container():
                        render_tool_card("error", "Error", str(exc))

# ── Execution log ──────────────────────────────────────────
st.markdown("---")
st.markdown('<div class="section-label">Execution Log</div>', unsafe_allow_html=True)
st.markdown('<div class="log-wrap">', unsafe_allow_html=True)
render_log_entries(st.session_state.logs)
st.markdown('</div>', unsafe_allow_html=True)

# ── DB viewer ──────────────────────────────────────────────
with st.expander("🗄  View Database Records"):
    all_rows = get_all_results()
    if all_rows:
        st.markdown(f"**{len(all_rows)} total records in SQLite DB**")
        header  = "| # | Query | Title | Summary | Tags | Saved At |\n|---|---|---|---|---|---|"
        rows_md = "\n".join(
            f"| {r['id']} | {r['query'][:30]} | {r['title'][:35]} "
            f"| {r['summary'][:60]}… | {r.get('tags','')} | {r['saved_at']} |"
            for r in all_rows
        )
        st.markdown(header + "\n" + rows_md)
    else:
        st.markdown("*No records yet. Run the agent to save results.*")
