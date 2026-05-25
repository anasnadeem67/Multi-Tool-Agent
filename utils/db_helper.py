"""
SQLite database helper.
Covers the "Save to DB" requirement properly.
Excel = human-readable export, SQLite = actual database storage.
Both are saved on every research result.
"""

import sqlite3
from datetime import datetime
from pathlib import Path

DB_PATH = "research_results.db"


def init_db() -> None:
    """Create tables if they don't exist."""
    conn = sqlite3.connect(DB_PATH)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS research_results (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            query       TEXT    NOT NULL,
            title       TEXT    NOT NULL,
            summary     TEXT,
            url         TEXT,
            tags        TEXT,
            saved_at    TEXT    NOT NULL
        )
    """)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS agent_logs (
            id        INTEGER PRIMARY KEY AUTOINCREMENT,
            action    TEXT NOT NULL,
            detail    TEXT,
            logged_at TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()


def insert_result(query: str, title: str, summary: str, url: str = "", tags: str = "") -> int:
    """Insert one research result. Returns the new row id."""
    conn = sqlite3.connect(DB_PATH)
    cur = conn.execute(
        "INSERT INTO research_results (query, title, summary, url, tags, saved_at) "
        "VALUES (?, ?, ?, ?, ?, ?)",
        (query, title, summary, url, tags, datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
    )
    row_id = cur.lastrowid
    conn.commit()
    conn.close()
    return row_id


def get_all_results() -> list[dict]:
    """Fetch all rows as list of dicts."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    rows = conn.execute(
        "SELECT * FROM research_results ORDER BY id"
    ).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def get_results_since_id(since_id: int) -> list[dict]:
    """Fetch only rows with id > since_id (new rows added in this session)."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    rows = conn.execute(
        "SELECT * FROM research_results WHERE id > ? ORDER BY id",
        (since_id,),
    ).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def get_max_id() -> int:
    """Return current highest row id (0 if empty)."""
    conn = sqlite3.connect(DB_PATH)
    row = conn.execute("SELECT COALESCE(MAX(id), 0) FROM research_results").fetchone()
    conn.close()
    return row[0]


# Init on import
init_db()
