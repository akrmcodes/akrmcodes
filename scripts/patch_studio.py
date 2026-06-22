#!/usr/bin/env python3
"""Fetch GitHub data and patch LIVE:* slots in studio SVG assets."""
from __future__ import annotations

import json
import os
import re
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOKEN = os.environ.get("GH_TOKEN", "")
USER = os.environ.get("GH_USER", "akrmcodes")


def api(path: str) -> dict:
    headers = {"Accept": "application/vnd.github+json", "User-Agent": "akrmcodes-studio-sync"}
    if TOKEN:
        headers["Authorization"] = f"Bearer {TOKEN}"
    req = urllib.request.Request(f"https://api.github.com{path}", headers=headers)
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.loads(resp.read().decode())


def graphql(query: str, variables: dict | None = None) -> dict:
    if not TOKEN:
        return {}
    payload = json.dumps({"query": query, "variables": variables or {}}).encode()
    req = urllib.request.Request(
        "https://api.github.com/graphql",
        data=payload,
        headers={
            "Authorization": f"Bearer {TOKEN}",
            "Content-Type": "application/json",
            "User-Agent": "akrmcodes-studio-sync",
        },
    )
    with urllib.request.urlopen(req, timeout=30) as resp:
        body = json.loads(resp.read().decode())
    if body.get("errors"):
        raise RuntimeError(body["errors"])
    return body["data"]


def patch_slot(text: str, key: str, value: str) -> str:
    return re.sub(
        rf"<!-- LIVE:{re.escape(key)} -->.*?<!-- /LIVE:{re.escape(key)} -->",
        f"<!-- LIVE:{key} -->{value}<!-- /LIVE:{key} -->",
        text,
        flags=re.S,
    )


def esc(s: str | None) -> str:
    if not s:
        return ""
    return (
        str(s)
        .replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )


def fetch_data() -> dict:
    user = api(f"/users/{USER}")
    repos = api(f"/users/{USER}/repos?per_page=100&sort=updated")
    owned = [r for r in repos if not r.get("fork")]
    owned.sort(key=lambda r: r.get("stargazers_count", 0), reverse=True)

    total_stars = sum(r.get("stargazers_count", 0) for r in owned)

    gq = graphql(
        """
        query($login: String!) {
          user(login: $login) {
            followers { totalCount }
            repositories(ownerAffiliations: OWNER) { totalCount }
            contributionsCollection {
              totalCommitContributions
              totalPullRequestContributions
              contributionCalendar { totalContributions }
            }
          }
        }
        """,
        {"login": USER},
    )
    gu = (gq.get("user") or {}) if gq else {}
    cc = gu.get("contributionsCollection") or {}

    langs: dict[str, int] = {}
    for r in owned:
        lang = (r.get("language") or "Other")
        langs[lang] = langs.get(lang, 0) + 1
    lang_sorted = sorted(langs.items(), key=lambda x: x[1], reverse=True)[:3]
    lang_total = sum(c for _, c in lang_sorted) or 1
    languages = [
        {"name": name, "pct": max(1, round(count / lang_total * 100))}
        for name, count in lang_sorted
    ]
    while len(languages) < 3:
        languages.append({"name": "—", "pct": 0})

    top = []
    for r in owned[:3]:
        top.append(
            {
                "name": r["name"],
                "description": (r.get("description") or "No description provided.")[:120],
                "stars": r.get("stargazers_count", 0),
                "language": r.get("language") or "—",
            }
        )
    while len(top) < 3:
        top.append({"name": "—", "description": "—", "stars": 0, "language": "—"})

    return {
        "stars": total_stars,
        "repos": gu.get("repositories", {}).get("totalCount") or user.get("public_repos", len(owned)),
        "streak": 0,
        "commits": cc.get("totalCommitContributions", 0),
        "followers": gu.get("followers", {}).get("totalCount") or user.get("followers", 0),
        "prs": cc.get("totalPullRequestContributions", 0),
        "contributions": (cc.get("contributionCalendar") or {}).get("totalContributions", 0),
        "building": "Next.js design systems",
        "languages": languages,
        "top_repos": top,
    }


def main() -> None:
    import importlib.util

    builder_path = Path(__file__).with_name("build_native_studio.py")
    if not builder_path.is_file():
        raise FileNotFoundError(
            "Missing scripts/build_native_studio.py — commit it with patch_studio.py."
        )
    spec = importlib.util.spec_from_file_location("build_native_studio", builder_path)
    if spec is None or spec.loader is None:
        raise ImportError(f"Cannot load builder module from {builder_path}")
    builder = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(builder)

    data = fetch_data()
    (ROOT / "profile" / "dashboard-data.json").write_text(
        json.dumps(data, indent=2) + "\n", encoding="utf-8"
    )
    builder.write_studio_svgs(data)
    print("Studio assets patched successfully (native SVG).")


if __name__ == "__main__":
    main()
