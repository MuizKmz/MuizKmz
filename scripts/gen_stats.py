"""Renders assets/stats.svg — the live STATUS WINDOW — from the GitHub GraphQL API.

  python scripts/gen_stats.py          # needs GH_TOKEN (CI provides it)
  python scripts/gen_stats.py --demo   # mock data, for local checks

LV = full years since the career start (same rule as the eportfolio hero),
the EXP bar = progress toward the next year.
"""

import json
import os
import sys
import urllib.request
from datetime import date, datetime, timezone

from hud import (DIM, LAV, LINE, MUTED, P, PALE, PL, WHITE, Doc, backdrop, brackets,
                 glitch_text, measure, pulse_dot, sweep_rule, tear_lines)

LOGIN = os.environ.get("LOGIN", "MuizKmz")
CAREER_START = date(2023, 5, 1)  # first role — keep in sync with the eportfolio
CLASS = "SOFTWARE ENGINEER"

QUERY = """query($login:String!){
  user(login:$login){
    followers{ totalCount }
    pullRequests{ totalCount }
    contributionsCollection{ contributionCalendar{ totalContributions
      weeks{ contributionDays{ date contributionCount } } } }
    repositories(first:100, ownerAffiliations:OWNER, isFork:false){
      totalCount
      nodes{ languages(first:10, orderBy:{field:SIZE,direction:DESC}){ edges{ size node{ name } } } }
    }
  }
}"""


def fetch():
    req = urllib.request.Request(
        "https://api.github.com/graphql",
        data=json.dumps({"query": QUERY, "variables": {"login": LOGIN}}).encode(),
        headers={"Authorization": f"Bearer {os.environ['GH_TOKEN']}",
                 "Content-Type": "application/json", "User-Agent": "profile-stats"})
    with urllib.request.urlopen(req) as r:
        body = json.load(r)
    if body.get("errors"):
        raise SystemExit(json.dumps(body["errors"]))
    u = body["data"]["user"]
    cal = u["contributionsCollection"]["contributionCalendar"]
    days = [dd for w in cal["weeks"] for dd in w["contributionDays"]]
    langs = {}
    for repo in u["repositories"]["nodes"]:
        for e in repo["languages"]["edges"]:
            langs[e["node"]["name"]] = langs.get(e["node"]["name"], 0) + e["size"]
    return {
        "repos": u["repositories"]["totalCount"],
        "prs": u["pullRequests"]["totalCount"],
        "contributions": cal["totalContributions"],
        "days": [(dd["date"], dd["contributionCount"]) for dd in days],
        "langs": sorted(langs.items(), key=lambda kv: -kv[1])[:5],
    }


DEMO = {
    "repos": 10, "prs": 10, "contributions": 894,
    "days": [(f"d{i}", (i * 7) % 5 if i % 6 else 0) for i in range(365)],
    "langs": [("Python", 591), ("TypeScript", 288), ("Vue", 48), ("JavaScript", 30), ("Java", 30)],
}


def streaks(days):
    longest = cur = 0
    for _, c in days:
        cur = cur + 1 if c > 0 else 0
        longest = max(longest, cur)
    # current streak: allow today to still be empty
    tail = 0
    seq = [c for _, c in days]
    if seq and seq[-1] == 0:
        seq = seq[:-1]
    for c in reversed(seq):
        if c == 0:
            break
        tail += 1
    active = sum(1 for _, c in days if c > 0)
    return longest, tail, active


def career(today):
    months = (today.year - CAREER_START.year) * 12 + (today.month - CAREER_START.month)
    lv = months // 12
    prog = min((months % 12) / 12 + today.day / 30 / 12, .99)
    return lv, months // 12, months % 12, prog


def fmt(n):
    return f"{n/1000:.1f}k".replace(".0k", "k") if n >= 1000 else str(n)


def render(s, today):
    lv, yrs, mos, prog = career(today)
    longest, current, active = streaks(s["days"])

    d = Doc(1000, 300, f"Status window for {LOGIN}: level {lv} {CLASS}, "
                       f"{s['contributions']} contributions in the last year", seed=61)
    backdrop(d, glow=(.2, .45))
    brackets(d, 0, 0, 1000, 300, L=18, inset=14, op=.8)

    pulse_dot(d, 44, 46, 3)
    d.T(56, 50, "[ STATUS ]", "monob", 12, PL, 3)
    d.T(170, 50, f"PLAYER: {LOGIN.upper()}", "mono", 12, LAV, 3)
    d.T(956, 50, f"SYNCED {today.isoformat()}", "mono", 10, DIM, 2, "end")
    sweep_rule(d, 44, 66, 912)

    # ── left: level + EXP ──
    d.T(44, 128, "LV.", "disp7", 18, LAV, 1)
    glitch_text(d, 92, 136, f"{lv:02d}", "disp", 62, WHITE, 1, dur=4.8, offset=.9, strength=.8)
    d.T(44, 166, "CLASS", "mono", 10, MUTED, 2)
    d.T(110, 166, CLASS, "monob", 12, PALE, 2)
    d.T(44, 188, "TITLE", "mono", 10, MUTED, 2)
    d.T(110, 188, "FULL-STACK · AI · IOT", "monob", 12, PALE, 1.5)

    bx, by, bw = 44, 226, 296
    d.T(bx, by - 10, f"EXP {yrs}Y {mos}M", "mono", 11, LAV, 1.5)
    d.T(bx + bw, by - 10, f"NEXT LV {round(prog*100)}%", "mono", 11, LAV, 1.5, "end")
    gid = d.uid("xp")
    d.defs.append(f'''<linearGradient id="{gid}" x1="0" y1="0" x2="1" y2="0">
  <stop offset="0" stop-color="#a78bfa"/><stop offset=".6" stop-color="#6366f1"/><stop offset="1" stop-color="{P}"/></linearGradient>''')
    d.add(f'<rect x="{bx}" y="{by}" width="{bw}" height="5" rx="2.5" fill="#2a1350"/>')
    fw = bw * prog
    d.add(f'<rect x="{bx}" y="{by}" width="{fw:.1f}" height="5" rx="2.5" fill="url(#{gid})">'
          f'<animate attributeName="width" from="0" to="{fw:.1f}" dur="1.8s" fill="freeze"/></rect>')
    d.add(f'<circle cx="{bx+fw:.1f}" cy="{by+2.5}" r="3.5" fill="{PALE}" opacity=".95"/>')
    for k in range(13):
        tx = bx + bw * k / 12
        d.add(f'<rect x="{tx:.1f}" y="{by+9}" width="1" height="{5 if k % 3 == 0 else 3}" fill="{DIM}"/>')
    d.T(bx, by + 34, f"SINCE {CAREER_START.strftime('%b %Y').upper()}  ·  1 LV = 1 YEAR SHIPPING", "mono", 9, DIM, 1.5)

    d.add(f'<rect x="376" y="96" width="1" height="170" fill="{LINE}"/>')
    d.add(f'<rect x="660" y="96" width="1" height="170" fill="{LINE}"/>')

    # ── middle: attributes ──
    d.T(404, 104, "ATTRIBUTES", "monob", 11, PL, 3)
    d.T(636, 104, "12 MO", "mono", 9, DIM, 2, "end")
    attrs = [
        ("CONTRIBUTIONS", fmt(s["contributions"])),
        ("ACTIVE DAYS", str(active)),
        ("LONGEST STREAK", f"{longest}D"),
        ("CURRENT STREAK", f"{current}D"),
        ("PULL REQUESTS", fmt(s["prs"])),
        ("REPOSITORIES", str(s["repos"])),
    ]
    for i, (k, v) in enumerate(attrs):
        y = 134 + i * 24
        d.add(f'<g style="animation:rise .7s ease-out {i*.1:.1f}s backwards">')
        d.T(404, y, k, "mono", 11, LAV, 1.5)
        d.add(f'<rect x="{404 + measure(k, "mono", 11, 1.5) + 8:.0f}" y="{y-4}" width="{636 - 404 - measure(k, "mono", 11, 1.5) - 16 - measure(v, "disp7", 14, .5):.0f}" height="1" fill="{LINE}"/>')
        d.T(636, y, v, "disp7", 14, WHITE, .5, "end")
        d.add("</g>")

    # ── right: language affinity ──
    d.T(688, 104, "SKILL AFFINITY", "monob", 11, PL, 3)
    langs = s["langs"]
    total = sum(v for _, v in langs) or 1
    shades = [P, "#8b5cf6", "#6366f1", "#c084fc", "#7c3aed"]
    for i, (name, v) in enumerate(langs):
        y = 134 + i * 28
        pct = v / total
        d.T(688, y, name.upper(), "mono", 10, LAV, 1.2)
        d.T(956, y, f"{pct*100:.1f}%", "mono", 10, MUTED, 1, "end")
        d.add(f'<rect x="688" y="{y+6}" width="268" height="4" rx="2" fill="#1c0b36"/>')
        w = max(268 * pct, 4)
        d.add(f'<rect x="688" y="{y+6}" width="{w:.1f}" height="4" rx="2" fill="{shades[i % 5]}">'
              f'<animate attributeName="width" from="0" to="{w:.1f}" dur="1.2s" begin="{.2+i*.12:.2f}s" fill="freeze"/></rect>')

    d.css.append("@keyframes rise{from{opacity:0;transform:translateY(6px)}to{opacity:1;transform:none}}")
    tear_lines(d, 0, 80, 1000, 200, n=2, dur=6)
    return d


if __name__ == "__main__":
    demo = "--demo" in sys.argv
    stats = DEMO if demo else fetch()
    today = datetime.now(timezone.utc).date()
    render(stats, today).save("assets/stats.svg")
    print("wrote assets/stats.svg", "(demo)" if demo else "")
