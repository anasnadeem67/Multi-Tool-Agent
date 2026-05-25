"""
Execution log.
add_log writes to the plain mem dict (passed as first arg).
agent.py copies mem["logs"] -> st.session_state.logs after run completes.
This is reliable because tools run in asyncio context where st.session_state is not safe.
"""

from datetime import datetime


def add_log(mem: dict, action: str, detail: str) -> None:
    if "logs" not in mem:
        mem["logs"] = []
    mem["logs"].append({
        "time":   datetime.now().strftime("%H:%M:%S"),
        "action": action,
        "detail": detail,
    })
