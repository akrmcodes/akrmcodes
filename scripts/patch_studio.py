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


def apply_dashboard(path: Path, data: dict) -> None:
    text = path.read_text(encoding="utf-8")
    for key in ("stars", "repos", "streak", "commits", "followers", "prs", "contributions"):
        text = patch_slot(text, key, str(data.get(key, 0)))
    text = patch_slot(text, "building", esc(data.get("building", "")))
    for i, lang in enumerate(data.get("languages", [])[:3], start=1):
        text = patch_slot(text, f"lang{i}_name", esc(lang["name"]))
        text = patch_slot(text, f"lang{i}_pct", f"{lang['pct']}%")
        text = patch_slot(text, f"lang{i}_bar", f"{lang['pct']}%")
    path.write_text(text, encoding="utf-8")


def apply_projects(path: Path, data: dict) -> None:
    text = path.read_text(encoding="utf-8")
    for i, repo in enumerate(data.get("top_repos", [])[:3], start=1):
        text = patch_slot(text, f"repo{i}_name", esc(repo["name"]))
        text = patch_slot(text, f"repo{i}_desc", esc(repo["description"]))
        text = patch_slot(text, f"repo{i}_stars", str(repo["stars"]))
        text = patch_slot(text, f"repo{i}_lang", esc(repo["language"]))
    path.write_text(text, encoding="utf-8")


def main() -> None:
    data = fetch_data()
    (ROOT / "profile" / "dashboard-data.json").write_text(
        json.dumps(data, indent=2) + "\n", encoding="utf-8"
    )
    apply_dashboard(ROOT / "assets" / "studio-dashboard.svg", data)
    apply_projects(ROOT / "assets" / "studio-projects.svg", data)
    print("Studio assets patched successfully.")


if __name__ == "__main__":
    main()
