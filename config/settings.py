"""
Central configuration — change model / paths here only.
"""

import os
from dotenv import load_dotenv

# ── Excel ───────────────────────────────────────────────
EXCEL_PATH    = "research_results.xlsx"
EXCEL_HEADERS = ["#", "Query", "Title / Source", "Summary", "URL / Reference", "Saved At", "Tags"]
COLUMN_WIDTHS = [5, 28, 30, 55, 45, 20, 22]

# ── Token limit — keeps requests within free-tier credits ──
MAX_TOKENS = 1024


def get_model():
    """
    Build and return the OpenAIChatCompletionsModel.
    Called lazily (only when agent needs it) so .env
    is guaranteed to be loaded before AsyncOpenAI is created.
    """
    load_dotenv()  # safe to call multiple times — idempotent

    # ✅ FIX: Suppress "OPENAI_API_KEY is not set" tracing warnings
    if not os.getenv("OPENAI_API_KEY"):
        os.environ["OPENAI_API_KEY"] = "dummy-not-used"

    from openai import AsyncOpenAI
    from agents.models.openai_chatcompletions import OpenAIChatCompletionsModel

    api_key = os.getenv("OPENROUTER_API_KEY", "").strip()
    if not api_key:
        raise EnvironmentError(
            "OPENROUTER_API_KEY not found.\n"
            "Create a .env file in the project root:\n"
            "  OPENROUTER_API_KEY=sk-or-xxxxxxxxxx"
        )

    client = AsyncOpenAI(
        api_key=api_key,
        base_url="https://openrouter.ai/api/v1",
    )

    return OpenAIChatCompletionsModel(
        model=os.getenv("MODEL", "openai/gpt-3.5-turbo"),
        openai_client=client,
    )


def get_model_settings():
    """
    ✅ FIX: max_tokens must be passed via ModelSettings to Runner,
    NOT as a kwarg to OpenAIChatCompletionsModel.
    Returns a ModelSettings object with max_tokens=1024.
    """
    from agents import ModelSettings
    return ModelSettings(max_tokens=MAX_TOKENS)
