#!/usr/bin/env python3
"""Build GitHub-safe native SVG studio assets (no foreignObject)."""
from __future__ import annotations

import base64
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets"
MONOGRAM_URI = (
    "data:image/svg+xml;base64,"
    + base64.b64encode((ASSETS / "ak-monogram.svg").read_bytes()).decode()
)


def read_live_slots(path: Path) -> dict[str, str]:
    if not path.exists():
        return {}
    text = path.read_text(encoding="utf-8", errors="replace")
    return {
        m.group(1): m.group(2)
        for m in re.finditer(r"<!-- LIVE:(\w+) -->(.*?)<!-- /LIVE:\1 -->", text, re.S)
    }


def slot(key: str, default: str, live: dict[str, str]) -> str:
    return live.get(key, default)


def hero_svg(live: dict[str, str]) -> str:
    return f'''<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" viewBox="0 0 1200 380" fill="none" aria-labelledby="t d">
  <title id="t">Akrm Qubati — Designer OS</title>
  <desc id="d">Native SVG hero — GitHub-safe, no foreignObject</desc>
  <defs>
    <linearGradient id="aurora" x1="0" y1="0" x2="1" y2="0"><stop offset="0%" stop-color="#f8b4d9"/><stop offset="50%" stop-color="#d8b4fe"/><stop offset="100%" stop-color="#a5f3fc"/></linearGradient>
    <linearGradient id="violet" x1="0" y1="0" x2="1" y2="0"><stop offset="0%" stop-color="#7c3aed"/><stop offset="100%" stop-color="#4b1ab1"/></linearGradient>
    <radialGradient id="meshA" cx="12%" cy="28%" r="55%"><stop offset="0%" stop-color="#4b1ab1" stop-opacity=".55"/><stop offset="100%" stop-color="#4b1ab1" stop-opacity="0"/></radialGradient>
    <radialGradient id="meshB" cx="88%" cy="22%" r="48%"><stop offset="0%" stop-color="#06b6d4" stop-opacity=".35"/><stop offset="100%" stop-color="#06b6d4" stop-opacity="0"/></radialGradient>
    <radialGradient id="meshC" cx="50%" cy="95%" r="55%"><stop offset="0%" stop-color="#7c3aed" stop-opacity=".3"/><stop offset="100%" stop-color="#7c3aed" stop-opacity="0"/></radialGradient>
    <style>
      text{{font-family:ui-sans-serif,system-ui,-apple-system,"Segoe UI",Roboto,Helvetica,Arial,sans-serif}}
      @media (prefers-reduced-motion:reduce){{.motion{{display:none!important}}}}
    </style>
  </defs>
  <rect width="1200" height="380" fill="#0a0814"/>
  <rect width="1200" height="380" fill="url(#meshA)"/>
  <rect width="1200" height="380" fill="url(#meshB)"/>
  <rect width="1200" height="380" fill="url(#meshC)"/>
  <rect x="1" y="1" width="1198" height="378" rx="14" stroke="url(#violet)" stroke-opacity=".35" fill="none"/>
  <image href="{MONOGRAM_URI}" x="48" y="88" width="148" height="148" clip-path="circle(74px at 74px 74px)"/>
  <circle cx="122" cy="162" r="78" fill="none" stroke="url(#aurora)" stroke-opacity=".35" stroke-width="1.5" class="motion">
    <animateTransform attributeName="transform" type="rotate" from="0 122 162" to="360 122 162" dur="24s" repeatCount="indefinite"/>
  </circle>
  <rect x="230" y="88" width="200" height="26" rx="13" fill="#7c3aed" fill-opacity=".15" stroke="#7c3aed" stroke-opacity=".35"/>
  <circle cx="248" cy="101" r="4" fill="#22d3ee" class="motion"><animate attributeName="opacity" values="1;.3;1" dur="2s" repeatCount="indefinite"/></circle>
  <text x="262" y="106" fill="#a78bfa" font-size="11" font-weight="600">DESIGNER OS · ONLINE</text>
  <text x="230" y="148" fill="url(#aurora)" font-size="40" font-weight="700">Akrm Qubati</text>
  <text x="230" y="178" fill="#a78bfa" font-size="15" font-weight="500">akrmcodes · Sana'a, Yemen</text>
  <g class="motion">
    <text x="230" y="218" fill="#f5f3ff" font-size="18" font-weight="600" opacity="0">Full-Stack Web &amp; Mobile<animate attributeName="opacity" values="0;0;1;1;0;0" keyTimes="0;.24;.25;.49;.5;1" dur="16s" repeatCount="indefinite"/></text>
    <text x="230" y="218" fill="#f5f3ff" font-size="18" font-weight="600" opacity="0">UI/UX Systems &amp; Prototypes<animate attributeName="opacity" values="0;0;0;0;1;1;0;0" keyTimes="0;.49;.5;.74;.75;.99;1;1" dur="16s" repeatCount="indefinite"/></text>
    <text x="230" y="218" fill="#f5f3ff" font-size="18" font-weight="600" opacity="0">API &amp; AI Integrations<animate attributeName="opacity" values="1;1;0;0;0;0;0;0" keyTimes="0;.24;.25;.49;.5;.74;.75;1" dur="16s" repeatCount="indefinite"/></text>
    <text x="230" y="218" fill="#f5f3ff" font-size="18" font-weight="600" opacity="0">Performance &amp; Accessibility<animate attributeName="opacity" values="0;0;0;0;0;0;1;1" keyTimes="0;.74;.75;.99;1;1;1;1" dur="16s" repeatCount="indefinite"/></text>
  </g>
  <rect x="230" y="242" width="170" height="32" rx="8" fill="#7c3aed" fill-opacity=".12" stroke="#7c3aed" stroke-opacity=".25"/>
  <text x="315" y="263" text-anchor="middle" fill="#e9d5ff" font-size="12" font-weight="600">akrm.codes@gmail.com</text>
  <rect x="412" y="242" width="100" height="32" rx="8" fill="#7c3aed" fill-opacity=".12" stroke="#7c3aed" stroke-opacity=".25"/>
  <text x="462" y="263" text-anchor="middle" fill="#c4b5fd" font-size="12" font-weight="600">LinkedIn</text>
  <rect x="524" y="242" width="90" height="32" rx="8" fill="#7c3aed" fill-opacity=".12" stroke="#7c3aed" stroke-opacity=".25"/>
  <text x="569" y="263" text-anchor="middle" fill="#c4b5fd" font-size="12" font-weight="600">Twitter</text>
  <rect x="626" y="242" width="110" height="32" rx="8" fill="#7c3aed" fill-opacity=".12" stroke="#7c3aed" stroke-opacity=".25"/>
  <text x="681" y="263" text-anchor="middle" fill="#c4b5fd" font-size="12" font-weight="600">Portfolio</text>
  <text x="230" y="310" fill="#a78bfa" font-size="13" font-style="italic">"Crafting code through a designer's lens."</text>
  <rect x="230" y="330" width="340" height="3" rx="1.5" fill="url(#aurora)" opacity=".8"/>
</svg>'''


def card(x, y, w, h, title):
    return f'''
  <rect x="{x}" y="{y}" width="{w}" height="{h}" rx="12" fill="#141024" stroke="url(#violet)" stroke-opacity=".28"/>
  <text x="{x+16}" y="{y+24}" fill="#a78bfa" font-size="10" font-weight="700" letter-spacing="1.2">{title}</text>'''


def stat_box(x, y, key, label, live, default):
    val = slot(key, default, live)
    return f'''
  <rect x="{x}" y="{y}" width="110" height="72" rx="10" fill="#7c3aed" fill-opacity=".1" stroke="#7c3aed" stroke-opacity=".2"/>
  <text x="{x+55}" y="{y+38}" text-anchor="middle" fill="#f5f3ff" font-size="26" font-weight="700"><!-- LIVE:{key} -->{val}<!-- /LIVE:{key} --></text>
  <text x="{x+55}" y="{y+58}" text-anchor="middle" fill="#a78bfa" font-size="9" font-weight="600">{label}</text>'''


def lang_row(x, y, i, live, defaults):
    name = slot(f"lang{i}_name", defaults["name"], live)
    pct = slot(f"lang{i}_pct", defaults["pct"], live).replace("%", "")
    try:
        bw = max(0, min(200, int(float(pct) * 2)))
    except ValueError:
        bw = 80
    return f'''
  <text x="{x}" y="{y}" fill="#c4b5fd" font-size="11"><!-- LIVE:lang{i}_name -->{name}<!-- /LIVE:lang{i}_name --></text>
  <text x="{x+200}" y="{y}" fill="#a78bfa" font-size="11"><!-- LIVE:lang{i}_pct -->{pct}%<!-- /LIVE:lang{i}_pct --></text>
  <rect x="{x}" y="{y+6}" width="200" height="6" rx="3" fill="#7c3aed" fill-opacity=".15"/>
  <!-- LIVE:lang{i}_bar --><rect x="{x}" y="{y+6}" width="{bw}" height="6" rx="3" fill="url(#violet)"/><!-- /LIVE:lang{i}_bar -->'''


def dashboard_svg(live: dict[str, str]) -> str:
    langs = [
        {"name": "TypeScript", "pct": "42"},
        {"name": "Dart", "pct": "28"},
        {"name": "JavaScript", "pct": "18"},
    ]
    building = slot("building", "Next.js design systems", live)
    parts = [
        '''<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" viewBox="0 0 1200 560" fill="none" aria-labelledby="t d">
  <title id="t">Studio Dashboard</title>
  <desc id="d">Native SVG dashboard with live telemetry slots</desc>
  <defs>
    <linearGradient id="aurora" x1="0" y1="0" x2="1" y2="0"><stop offset="0%" stop-color="#f8b4d9"/><stop offset="50%" stop-color="#d8b4fe"/><stop offset="100%" stop-color="#a5f3fc"/></linearGradient>
    <linearGradient id="violet" x1="0" y1="0" x2="1" y2="0"><stop offset="0%" stop-color="#7c3aed"/><stop offset="100%" stop-color="#4b1ab1"/></linearGradient>
    <style>text{font-family:ui-sans-serif,system-ui,-apple-system,"Segoe UI",Roboto,Helvetica,Arial,sans-serif}@media (prefers-reduced-motion:reduce){.motion{animation:none!important}}</style>
  </defs>
  <rect width="1200" height="560" rx="14" fill="#0f0c1c"/>
  <rect x="1" y="1" width="1198" height="558" rx="13" stroke="url(#violet)" stroke-opacity=".3" fill="none"/>''',
        card(20, 20, 360, 220, "IDENTITY"),
        f'  <image href="{MONOGRAM_URI}" x="36" y="48" width="64" height="64"/>',
        '  <text x="120" y="72" fill="#f5f3ff" font-size="20" font-weight="700">Akrm Qubati</text>',
        '  <text x="120" y="94" fill="#a78bfa" font-size="12">Designer-Engineer</text>',
        '  <text x="120" y="112" fill="#a78bfa" font-size="11">Sana\'a, Yemen</text>',
        '  <text x="36" y="160" fill="#c4b5fd" font-size="11">Crafting code through a designer\'s lens.</text>',
        '  <text x="36" y="180" fill="#c4b5fd" font-size="11">Web, mobile, and systems that feel</text>',
        '  <text x="36" y="200" fill="#c4b5fd" font-size="11">as good as they function.</text>',
        card(400, 20, 780, 220, "LIVE TELEMETRY"),
    ]
    sx, sy = 420, 60
    for i, (k, lbl, d) in enumerate([
        ("stars", "STARS", "6"), ("repos", "REPOS", "21"), ("streak", "STREAK", "0"),
        ("commits", "COMMITS", "0"), ("followers", "FOLLOWERS", "6"), ("prs", "PRS", "0"),
    ]):
        parts.append(stat_box(sx + (i % 3) * 120, sy + (i // 3) * 88, k, lbl, live, d))
    parts.append(card(20, 260, 1160, 80, "STACK"))
    skills = "React  ·  Next.js  ·  TypeScript  ·  Tailwind  ·  Laravel  ·  Node  ·  Python  ·  Flutter  ·  Firebase  ·  Figma  ·  Docker  ·  OpenAI"
    parts.append(f'  <text x="36" y="310" fill="#c4b5fd" font-size="12" font-weight="500">{skills}</text>')
    parts.append(card(20, 360, 520, 180, "TOP LANGUAGES"))
    ly = 400
    for i, d in enumerate(langs, 1):
        parts.append(lang_row(36, ly, i, live, d))
        ly += 36
    parts.append(card(560, 360, 300, 180, "BUILDING NOW"))
    parts.append('  <circle cx="576" cy="392" r="5" fill="#ff5f57"/><circle cx="594" cy="392" r="5" fill="#febc2e"/><circle cx="612" cy="392" r="5" fill="#28c840"/>')
    parts.append(f'  <text x="576" y="420" fill="#7c3aed" font-size="11" font-family="ui-monospace,monospace">$ akrm — focus</text>')
    parts.append(f'  <text x="576" y="440" fill="#22d3ee" font-size="11" font-family="ui-monospace,monospace">→ <!-- LIVE:building -->{building}<!-- /LIVE:building --></text>')
    parts.append(card(880, 360, 300, 180, "ACTIVITY"))
    contrib = slot("contributions", "0", live)
    parts.append(f'  <text x="896" y="400" fill="#a78bfa" font-size="11">Contributions: <!-- LIVE:contributions -->{contrib}<!-- /LIVE:contributions --></text>')
    hx, hy = 896, 420
    pattern = [0, 1, 2, 3, 1, 0, 2, 1, 3, 2, 1, 0, 2, 3, 1, 0, 1, 2, 0, 1, 3, 2, 1, 0, 2, 1, 3, 0]
    colors = ["#1a1530", "#4b1ab1", "#7c3aed", "#a5f3fc"]
    for i, p in enumerate(pattern):
        cx = hx + (i % 14) * 14
        cy = hy + (i // 14) * 14
        parts.append(f'  <rect x="{cx}" y="{cy}" width="10" height="10" rx="2" fill="{colors[p]}"/>')
    parts.append("</svg>")
    return "\n".join(parts)


def wrap_text(desc: str, max_len: int = 42) -> list[str]:
    words = desc.split()
    lines, cur = [], ""
    for w in words:
        test = f"{cur} {w}".strip()
        if len(test) > max_len and cur:
            lines.append(cur)
            cur = w
        else:
            cur = test
    if cur:
        lines.append(cur)
    return lines[:2] or ["—"]


def project_panel(x, i, live, defaults):
    name = slot(f"repo{i}_name", defaults["name"], live)
    desc = slot(f"repo{i}_desc", defaults["desc"], live)
    stars = slot(f"repo{i}_stars", defaults["stars"], live)
    lang = slot(f"repo{i}_lang", defaults["lang"], live)
    lines = wrap_text(desc)
    body = [
        f'  <rect x="{x}" y="48" width="376" height="292" rx="12" fill="#141024" stroke="url(#violet)" stroke-opacity=".28"/>',
        f'  <rect x="{x}" y="48" width="376" height="100" rx="12" fill="url(#g{i})"/>',
        f'  <rect x="{x+12}" y="60" width="72" height="22" rx="6" fill="#7c3aed" fill-opacity=".35"/>',
        f'  <text x="{x+48}" y="75" text-anchor="middle" fill="#f5f3ff" font-size="10" font-weight="700"><!-- LIVE:repo{i}_lang -->{lang}<!-- /LIVE:repo{i}_lang --></text>',
        f'  <text x="{x+340}" y="75" text-anchor="end" fill="#fbbf24" font-size="10">★ <!-- LIVE:repo{i}_stars -->{stars}<!-- /LIVE:repo{i}_stars --></text>',
        f'  <text x="{x+16}" y="172" fill="#f5f3ff" font-size="15" font-weight="700"><!-- LIVE:repo{i}_name -->{name}<!-- /LIVE:repo{i}_name --></text>',
    ]
    ty = 196
    for line in lines:
        body.append(f'  <text x="{x+16}" y="{ty}" fill="#a78bfa" font-size="11">{line}</text>')
        ty += 18
    return "\n".join(body)


def projects_svg(live: dict[str, str]) -> str:
    defaults = [
        {"name": "daily_expense_tracker", "desc": "Cross-platform expense tracking app built with Flutter.", "stars": "3", "lang": "Dart"},
        {"name": "ZeroHunger-Monorepo", "desc": "Full-stack monorepo for a hunger-relief platform.", "stars": "1", "lang": "TypeScript"},
        {"name": "Hudson-Furnishing", "desc": "Modern furnishing showcase with Next.js and Tailwind.", "stars": "1", "lang": "TypeScript"},
    ]
    parts = [
        '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 360" fill="none" aria-labelledby="t d">
  <title id="t">Featured Projects</title>
  <desc id="d">Native SVG project filmstrip</desc>
  <defs>
    <linearGradient id="violet" x1="0" y1="0" x2="1" y2="0"><stop offset="0%" stop-color="#7c3aed"/><stop offset="100%" stop-color="#4b1ab1"/></linearGradient>
    <linearGradient id="g1" x1="0" y1="0" x2="1" y2="1"><stop offset="0%" stop-color="#1a1530"/><stop offset="100%" stop-color="#4b1ab1"/></linearGradient>
    <linearGradient id="g2" x1="0" y1="0" x2="1" y2="1"><stop offset="0%" stop-color="#0f172a"/><stop offset="100%" stop-color="#06b6d4"/></linearGradient>
    <linearGradient id="g3" x1="0" y1="0" x2="1" y2="1"><stop offset="0%" stop-color="#1a1033"/><stop offset="100%" stop-color="#7c3aed"/></linearGradient>
    <style>text{font-family:ui-sans-serif,system-ui,-apple-system,"Segoe UI",Roboto,Helvetica,Arial,sans-serif}</style>
  </defs>
  <rect width="1200" height="360" rx="14" fill="#0f0c1c"/>
  <rect x="1" y="1" width="1198" height="358" rx="13" stroke="url(#violet)" stroke-opacity=".3" fill="none"/>
  <text x="24" y="32" fill="#a78bfa" font-size="11" font-weight="700" letter-spacing="1.4">FEATURED REPOSITORIES</text>''',
    ]
    for i, d in enumerate(defaults, 1):
        parts.append(project_panel(20 + (i - 1) * 392, i, live, d))
    parts.append("</svg>")
    return "\n".join(parts)


def write_studio_svgs(data: dict | None = None) -> None:
    live_dash = read_live_slots(ASSETS / "studio-dashboard.svg")
    live_proj = read_live_slots(ASSETS / "studio-projects.svg")
    live = {**live_dash, **live_proj}
    if data:
        live.update({
            "stars": str(data.get("stars", 0)),
            "repos": str(data.get("repos", 0)),
            "streak": str(data.get("streak", 0)),
            "commits": str(data.get("commits", 0)),
            "followers": str(data.get("followers", 0)),
            "prs": str(data.get("prs", 0)),
            "contributions": str(data.get("contributions", 0)),
            "building": data.get("building", "Next.js design systems"),
        })
        for i, lang in enumerate(data.get("languages", [])[:3], start=1):
            live[f"lang{i}_name"] = lang["name"]
            live[f"lang{i}_pct"] = f"{lang['pct']}%"
        for i, repo in enumerate(data.get("top_repos", [])[:3], start=1):
            live[f"repo{i}_name"] = repo["name"]
            live[f"repo{i}_desc"] = repo["description"].replace("&", "&amp;").replace("<", "&lt;")
            live[f"repo{i}_stars"] = str(repo["stars"])
            live[f"repo{i}_lang"] = repo["language"]
    (ASSETS / "studio-hero.svg").write_text(hero_svg(live), encoding="utf-8")
    (ASSETS / "studio-dashboard.svg").write_text(dashboard_svg(live), encoding="utf-8")
    (ASSETS / "studio-projects.svg").write_text(projects_svg(live), encoding="utf-8")


def main() -> None:
    write_studio_svgs()
    print("Built native studio SVGs (GitHub-safe).")


if __name__ == "__main__":
    main()
