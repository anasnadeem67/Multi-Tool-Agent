from tools.search     import make_search_tool
from tools.excel_tool import make_excel_tool
from tools.email_tool import make_email_tool


def make_all_tools(mem: dict) -> list:
    """Return all agent tools sharing the same session-state dict."""
    return [
        make_search_tool(mem),
        make_excel_tool(mem),
        make_email_tool(mem),
    ]
