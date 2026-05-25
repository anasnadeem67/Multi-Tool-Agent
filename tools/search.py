"""
web_search tool.
mem is a plain Python dict (NOT st.session_state).
Updates to mem work reliably across asyncio thread boundaries.
"""

import re
import json
import requests
from agents import function_tool
from utils.logger import add_log

HEADERS = {"User-Agent": "MultiToolAgent/1.0 (research bot)"}
TIMEOUT = 10


def _clean_html(text: str) -> str:
    return re.sub(r"<[^>]+>", "", text).strip()


def make_search_tool(mem: dict):

    @function_tool
    def web_search(query: str) -> str:
        """
        Search the web for information on any topic.
        Returns structured results with title, snippet, and URL.
        Always call this first when researching a topic.
        """
        results = []

        # 1. Wikipedia REST
        try:
            slug = query.strip().replace(" ", "_")
            r = requests.get(
                f"https://en.wikipedia.org/api/rest_v1/page/summary/{slug}",
                headers=HEADERS, timeout=TIMEOUT,
            )
            if r.status_code == 200:
                w = r.json()
                if w.get("extract") and w["type"] != "disambiguation":
                    results.append({
                        "title":   w.get("title", query),
                        "snippet": w["extract"][:700],
                        "url":     w.get("content_urls", {}).get("desktop", {}).get("page", ""),
                        "source":  "Wikipedia",
                    })
        except Exception:
            pass

        # 2. Wikipedia OpenSearch
        try:
            r = requests.get(
                "https://en.wikipedia.org/w/api.php",
                params={"action": "opensearch", "search": query, "limit": 5, "format": "json"},
                headers=HEADERS, timeout=TIMEOUT,
            )
            if r.status_code == 200:
                data = r.json()
                titles = data[1] if len(data) > 1 else []
                descs  = data[2] if len(data) > 2 else []
                urls   = data[3] if len(data) > 3 else []
                for title, desc, url in zip(titles, descs, urls):
                    if desc and not any(r2["title"].lower() == title.lower() for r2 in results):
                        results.append({"title": title, "snippet": desc[:400], "url": url, "source": "Wikipedia Search"})
        except Exception:
            pass

        # 3. Wikipedia Full-Text
        try:
            r = requests.get(
                "https://en.wikipedia.org/w/api.php",
                params={"action": "query", "list": "search", "srsearch": query,
                        "srlimit": 4, "format": "json", "srprop": "snippet|titlesnippet"},
                headers=HEADERS, timeout=TIMEOUT,
            )
            if r.status_code == 200:
                for item in r.json().get("query", {}).get("search", []):
                    title   = item.get("title", "")
                    snippet = _clean_html(item.get("snippet", ""))
                    if snippet and not any(r2["title"].lower() == title.lower() for r2 in results):
                        results.append({
                            "title": title, "snippet": snippet[:400],
                            "url": f"https://en.wikipedia.org/wiki/{title.replace(' ', '_')}",
                            "source": "Wikipedia Full-Text",
                        })
        except Exception:
            pass

        # 4. DuckDuckGo
        try:
            r = requests.get(
                "https://api.duckduckgo.com/",
                params={"q": query, "format": "json", "no_html": 1, "skip_disambig": 1},
                headers=HEADERS, timeout=8,
            )
            if r.status_code == 200:
                data = r.json()
                if data.get("AbstractText"):
                    if not any(data["AbstractText"][:60] in r2["snippet"] for r2 in results):
                        results.append({
                            "title": data.get("AbstractSource", "DuckDuckGo"),
                            "snippet": data["AbstractText"][:500],
                            "url": data.get("AbstractURL", ""),
                            "source": "DuckDuckGo",
                        })
                for topic in data.get("RelatedTopics", [])[:3]:
                    if isinstance(topic, dict) and topic.get("Text"):
                        results.append({
                            "title": _clean_html(topic["Text"])[:60],
                            "snippet": topic["Text"][:300],
                            "url": topic.get("FirstURL", ""),
                            "source": "DuckDuckGo Related",
                        })
        except Exception:
            pass

        if not results:
            add_log(mem, "WEB_SEARCH", f"No results: '{query}'")
            return json.dumps({"query": query, "results": [], "count": 0, "status": "no_results"})

        # Update plain dict - works reliably across threads
        mem["search_count"] = mem.get("search_count", 0) + 1
        mem["last_results"] = results

        sources = list(set(r["source"] for r in results))
        add_log(mem, "WEB_SEARCH", f"'{query}' -> {len(results)} results | {', '.join(sources)}")

        return json.dumps({"query": query, "results": results[:6], "count": len(results), "status": "success"})

    return web_search
