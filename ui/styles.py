"""All CSS — clean white editorial theme."""

CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@700;800&family=DM+Mono:wght@400;500&family=DM+Sans:wght@300;400;500&display=swap');

:root {
    --bg:       #f5f5f0;
    --surface:  #ffffff;
    --surface2: #f0f0eb;
    --border:   #e0e0d8;
    --accent:   #1a1a2e;
    --accent2:  #e63946;
    --blue:     #1d6fa4;
    --green:    #2d7a4f;
    --red:      #e63946;
    --yellow:   #f5c518;
    --text:     #111111;
    --muted:    #888888;
    --serif:    'Syne', sans-serif;
    --mono:     'DM Mono', monospace;
    --sans:     'DM Sans', sans-serif;
}

html, body,
[data-testid="stAppViewContainer"],
[data-testid="stAppViewBlockContainer"],
[data-testid="stMainBlockContainer"],
[data-testid="block-container"],
.main, .block-container,
div[class*="main"] {
    background: var(--bg) !important;
    color: var(--text) !important;
    font-family: var(--sans);
}

[data-testid="stHeader"] {
    background: var(--bg) !important;
}

[data-testid="stSidebar"] {
    background: var(--surface) !important;
    border-right: 1px solid var(--border);
}
[data-testid="stSidebar"] * {
    color: var(--text) !important;
}

.agent-header {
    border-bottom: 3px solid var(--accent);
    padding-bottom: 0.8rem;
    margin-bottom: 1.5rem;
}
.agent-title {
    font-family: var(--serif);
    font-size: 2rem;
    font-weight: 800;
    letter-spacing: -0.5px;
    color: var(--accent);
    line-height: 1.15;
}
.agent-title .bolt { color: var(--accent2); }
.agent-meta {
    font-family: var(--mono);
    font-size: 0.6rem;
    color: var(--muted);
    letter-spacing: 2px;
    text-transform: uppercase;
    margin-top: 0.25rem;
}

.section-label {
    font-family: var(--mono);
    font-size: 0.62rem;
    letter-spacing: 3px;
    text-transform: uppercase;
    color: var(--accent);
    border-left: 3px solid var(--accent);
    padding-left: 0.6rem;
    margin-bottom: 0.8rem;
}

.stat-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 12px;
    margin-bottom: 1.5rem;
}
.stat-box {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 8px;
    padding: 16px 16px 14px;
    text-align: center;
}
.stat-box.active {
    border-color: var(--accent);
    box-shadow: 0 2px 12px rgba(26,26,46,0.08);
}
.stat-value {
    font-family: var(--mono);
    font-size: 2.2rem;
    font-weight: 500;
    color: var(--muted);
    line-height: 1;
}
.stat-box.active .stat-value { color: var(--accent); }
.stat-label {
    font-family: var(--mono);
    font-size: 0.58rem;
    letter-spacing: 2px;
    text-transform: uppercase;
    color: var(--muted);
    margin-top: 6px;
}

[data-testid="stTextInput"] input,
[data-testid="stTextArea"] textarea {
    background: var(--surface) !important;
    color: var(--text) !important;
    border: 1px solid var(--border) !important;
    border-radius: 6px !important;
    font-family: var(--sans) !important;
    font-size: 0.93rem !important;
}
[data-testid="stTextInput"] input:focus,
[data-testid="stTextArea"] textarea:focus {
    border-color: var(--accent) !important;
    box-shadow: 0 0 0 2px rgba(26,26,46,0.08) !important;
}
[data-testid="stTextInput"] label,
[data-testid="stTextArea"] label,
[data-testid="stSelectbox"] label {
    color: var(--muted) !important;
    font-family: var(--mono) !important;
    font-size: 0.68rem !important;
    letter-spacing: 1.5px !important;
    text-transform: uppercase !important;
}

[data-testid="stSelectbox"] > div > div {
    background: var(--surface) !important;
    border: 1px solid var(--border) !important;
    color: var(--text) !important;
}

[data-testid="stCheckbox"] label {
    color: var(--text) !important;
    font-family: var(--sans) !important;
    font-size: 0.88rem !important;
    text-transform: none !important;
    letter-spacing: 0 !important;
}

[data-testid="stButton"] button {
    background: var(--accent) !important;
    color: #fff !important;
    font-family: var(--mono) !important;
    font-size: 0.78rem !important;
    font-weight: 500 !important;
    letter-spacing: 2px !important;
    text-transform: uppercase !important;
    border: none !important;
    border-radius: 6px !important;
    padding: 0.6rem 1.5rem !important;
    transition: all 0.15s !important;
}
[data-testid="stButton"] button:hover {
    background: #2d2d4e !important;
    transform: translateY(-1px) !important;
}

[data-testid="stDownloadButton"] button {
    background: var(--surface) !important;
    color: var(--accent) !important;
    border: 1px solid var(--accent) !important;
    font-family: var(--mono) !important;
    font-size: 0.72rem !important;
    letter-spacing: 1.5px !important;
}

.tool-card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 8px;
    padding: 1.1rem 1.3rem;
    margin-bottom: 0.8rem;
    position: relative;
    overflow: hidden;
}
.tool-card::before {
    content: '';
    position: absolute;
    left: 0; top: 0; bottom: 0;
    width: 3px;
}
.tool-card.search::before  { background: var(--blue); }
.tool-card.excel::before   { background: var(--green); }
.tool-card.email::before   { background: var(--accent2); }
.tool-card.agent::before   { background: var(--accent); }
.tool-card.error::before   { background: var(--red); }
.tool-name {
    font-family: var(--mono);
    font-size: 0.62rem;
    letter-spacing: 2px;
    text-transform: uppercase;
    margin-bottom: 0.4rem;
}
.tool-name.search  { color: var(--blue); }
.tool-name.excel   { color: var(--green); }
.tool-name.email   { color: var(--accent2); }
.tool-name.agent   { color: var(--accent); }
.tool-name.error   { color: var(--red); }
.tool-content {
    font-size: 0.88rem;
    color: var(--text);
    line-height: 1.75;
}

.badge {
    display: inline-block;
    font-family: var(--mono);
    font-size: 0.6rem;
    letter-spacing: 1.5px;
    text-transform: uppercase;
    padding: 3px 10px;
    border-radius: 20px;
    margin-right: 6px;
}
.badge-ok   { background: rgba(45,122,79,0.1);  color: var(--green);  border: 1px solid rgba(45,122,79,0.3); }
.badge-warn { background: rgba(245,197,24,0.1); color: #997a00;       border: 1px solid rgba(245,197,24,0.4); }
.badge-err  { background: rgba(230,57,70,0.1);  color: var(--red);    border: 1px solid rgba(230,57,70,0.3); }
.badge-info { background: rgba(29,111,164,0.1); color: var(--blue);   border: 1px solid rgba(29,111,164,0.3); }

.log-wrap {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 8px;
    padding: 0.8rem 1rem;
}
.log-entry {
    font-family: var(--mono);
    font-size: 0.72rem;
    padding: 0.35rem 0;
    border-bottom: 1px solid var(--border);
    display: flex;
    gap: 0.8rem;
    align-items: baseline;
}
.log-entry:last-child { border-bottom: none; }
.log-time   { color: var(--muted); min-width: 65px; flex-shrink: 0; }
.log-action { color: var(--accent); min-width: 110px; flex-shrink: 0; font-weight: 500; }
.log-detail { color: #444; flex: 1; }

hr { border-color: var(--border) !important; margin: 1.2rem 0 !important; }
[data-testid="stExpander"] {
    background: var(--surface) !important;
    border: 1px solid var(--border) !important;
    border-radius: 8px !important;
}
[data-testid="stExpander"] summary { color: var(--text) !important; }
.block-container { padding-top: 1.5rem !important; }
[data-testid="stSpinner"] { color: var(--accent) !important; }
[data-testid="stAlert"] {
    background: var(--surface) !important;
    border: 1px solid var(--border) !important;
    color: var(--text) !important;
}
.empty-state {
    color: var(--muted);
    font-family: var(--mono);
    font-size: 0.78rem;
    padding: 2.5rem;
    border: 1.5px dashed var(--border);
    border-radius: 8px;
    text-align: center;
}
</style>
"""
