"""Reusable HTML snippet builders."""

import streamlit as st


def render_header() -> None:
    st.markdown("""
    <div class="agent-header">
      <div class="agent-title">MULTI<span class="bolt">⚡</span>TOOL AGENT</div>
      <div class="agent-meta">OpenAI Agents SDK · OpenRouter gpt-3.5-turbo · SQLite + Excel · Intermediate Task 1</div>
    </div>
    """, unsafe_allow_html=True)


def render_tool_card(kind: str, label: str, content: str) -> None:
    safe = content.replace("\n", "<br>").replace("##", "<strong>").replace("**", "")
    st.markdown(f"""
    <div class="tool-card {kind}">
        <div class="tool-name {kind}">{label}</div>
        <div class="tool-content">{safe}</div>
    </div>
    """, unsafe_allow_html=True)


def render_badge_row(searched: bool, saved: bool, emailed: bool) -> None:
    badges = []
    if searched:
        badges.append('<span class="badge badge-info">🔍 Searched</span>')
    if saved:
        badges.append('<span class="badge badge-ok">🗄 Saved to DB</span>')
    if emailed:
        badges.append('<span class="badge badge-ok">📧 Email Sent</span>')
    if badges:
        st.markdown("<br>" + " ".join(badges), unsafe_allow_html=True)


def render_log_entries(logs: list) -> None:
    if not logs:
        st.markdown(
            '<p style="color:#aaa;font-family:monospace;font-size:0.78rem;padding:0.5rem 0">'
            'No logs yet. Run the agent to see activity.</p>',
            unsafe_allow_html=True,
        )
        return
    html = ""
    for entry in reversed(logs[-25:]):
        html += (
            f'<div class="log-entry">'
            f'<span class="log-time">{entry["time"]}</span>'
            f'<span class="log-action">{entry["action"]}</span>'
            f'<span class="log-detail">{entry["detail"]}</span>'
            f'</div>'
        )
    st.markdown(html, unsafe_allow_html=True)
