"""
save_to_db tool - uses plain mem dict for reliable cross-thread state.
"""

import json
from agents import function_tool
from utils.excel_helper import append_to_excel
from utils.db_helper    import insert_result
from utils.logger       import add_log
from config.settings    import EXCEL_PATH, EXCEL_HEADERS


def make_excel_tool(mem: dict):

    @function_tool
    def save_to_db(
        query:   str,
        title:   str,
        summary: str,
        url:     str = "",
        tags:    str = "",
    ) -> str:
        """
        Save a research finding to the database (SQLite) AND export to Excel.
        Call this after every web_search for important results.

        Args:
          title:   concise headline, max 60 chars
          summary: 2-3 sentence insight, max 400 chars
          url:     source URL when available
          tags:    comma-separated keywords
        """
        try:
            db_id     = insert_result(query, title, summary, url, tags)
            excel_row = append_to_excel(query, title, summary, url, tags)

            # Update plain dict - reliable across asyncio threads
            mem["save_count"] = mem.get("save_count", 0) + 1

            add_log(mem, "SAVE_TO_DB", f"DB row #{db_id} | Excel row #{excel_row} — '{title[:40]}'")

            return json.dumps({
                "status":    "saved",
                "db_id":     db_id,
                "excel_row": excel_row,
                "storage":   ["SQLite (research_results.db)", "Excel (research_results.xlsx)"],
                "message":   f"Saved to DB (id={db_id}) and Excel (row={excel_row})",
            })

        except Exception as exc:
            add_log(mem, "SAVE_TO_DB", f"ERROR: {exc}")
            return json.dumps({"error": str(exc), "status": "error"})

    return save_to_db
