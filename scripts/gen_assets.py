"""Renders the static HUD assets in assets/. Run: python scripts/gen_assets.py
(The live STATUS card is rendered separately by gen_stats.py in CI.)"""

from hud import *  # noqa: F401,F403
from hud import Doc, measure, wrap

OUT = "assets"

# ── content ───────────────────────────────────────────────────────

NAME = "MUIZ KAMAROZAMAN"
ROLES = ["FULL-STACK", "AI AGENTS & RAG", "REAL-TIME IOT", "DEVOPS"]

SECTIONS = [
    # file, number, title, code, system message
    ("sec-status", "01", "STATUS", "_ PRF.001", "PLAYER PROFILE LOADED"),
    ("sec-skills", "02", "SKILLS", "_ SKL.002", "SKILL DATABASE UNLOCKED"),
    ("sec-projects", "03", "PROJECTS", "_ ARC.003", "PROJECT ARCHIVE OPENED"),
    ("sec-activity", "04", "QUEST LOG", "_ ACT.004", "ACTIVITY LOG SYNCED"),
    ("sec-contact", "05", "CONTACT", "_ GATE.005", "DUNGEON GATE DETECTED"),
]

SKILLS = [
    ("FRONTEND SYSTEMS", ["React", "Next.js", "Vue 3", "TypeScript", "Tailwind", "Vite"]),
    ("MOBILE", ["React Native", "Expo", "Flutter", "Kotlin", "Java"]),
    ("BACKEND LOGIC", ["Node.js", "NestJS", "Express", "Spring Boot", "FastAPI", "Laravel", "Prisma"]),
    ("AI & AGENTS", ["LLMs", "RAG", "LangGraph", "LangChain", "pgvector", "Pinecone", "MCP", "n8n"]),
    ("REAL-TIME IOT", ["MQTT", "Socket.IO", "ESP32", "RFID / EPC", "Telemetry", "OEE"]),
    ("DEVOPS & DATA", ["Docker", "AWS", "Huawei Cloud", "GH Actions", "Jenkins", "MySQL", "PostgreSQL", "Redis"]),
]

PROJECTS = [
    ("AIPLATFORM", "EAIP — Enterprise AI Platform",
     "Governed multi-tenant RAG + agent platform. Enterprise systems plug in as connectors and answers come back cited.",
     ["FastAPI", "LangGraph", "pgvector", "Next.js", "MCP"]),
    ("IOTPLATFORM", "Industrial IoT Monitoring",
     "MQTT telemetry into live dashboards, alert rules and OEE — pushed to web and mobile over Socket.IO.",
     ["TypeScript", "Node.js", "MQTT", "Socket.IO", "Expo"]),
    ("HAPPISAFE", "HappiSafe Insurtech Platform",
     "Dual insurer integration (REST/JWT + SOAP/mTLS), tokenised payments and a RAG support chatbot.",
     ["Spring Boot", "Redis", "Vue 3", "uni-app", "GPT-4o"]),
    ("POLESYNC", "PoleSyncTech Smart Pole",
     "Street poles as multi-sensor IoT nodes, with a RAG + text-to-SQL assistant for city authorities.",
     ["Laravel", "Vue 3", "n8n", "Pinecone", "MySQL"]),
    ("FROSTEDGE", "SmartArctic Smart Freezer",
     "Cold-chain monitoring: ESP32 temperature, power and GPS telemetry with real-time alerts.",
     ["ESP32", "IoT", "MySQL", "System Design"]),
    ("WMS", "RFID Warehouse System",
     "Item-level EPC tracking with a lifecycle state machine, FIFO allocation and an RFID handheld app.",
     ["NestJS", "Prisma", "React Native", "Kotlin", "Docker"]),
]

BUTTONS = [
    ("btn-portfolio", "PORTFOLIO", "muizkmz.vercel.app"),
    ("btn-github", "GITHUB", "@MuizKmz"),
    ("btn-linkedin", "LINKEDIN", "in/muizzuddin"),
    ("btn-email", "EMAIL", "send a message"),
]


# ── hero ──────────────────────────────────────────────────────────

def hero():
    d = Doc(1000, 380, "Muiz Kamarozaman — Software Engineer. Full-stack, AI agents & RAG, real-time IoT, DevOps.", seed=3)
    backdrop(d, glow=(.5, .5))
    embers(d, 20, 40, 960, 330, n=34)
    brackets(d, 0, 0, 1000, 380, L=26, inset=18)

    # top bar
    pulse_dot(d, 52, 52)
    d.T(66, 56, "[ SYSTEM ]", "monob", 12, PL, 3)
    d.T(176, 56, "PLAYER PROFILE LOADED", "mono", 12, LAV, 3)
    d.T(948, 56, "ID · MUIZKMZ  ///  [ S-CLASS ]", "mono", 12, MUTED, 2, "end")
    sweep_rule(d, 44, 72, 912)

    # side rails
    d.T(0, 0, "SECURE CHANNEL: ACTIVE", "mono", 9, DIM, 3,
        extra='transform="translate(30 290) rotate(-90)"')
    d.T(0, 0, "GATE STATUS: OPEN", "mono", 9, DIM, 3,
        extra='transform="translate(976 110) rotate(90)"')

    d.T(500, 128, "SOFTWARE ENGINEER  ·  JOHOR BAHRU, MY", "mono", 13, LAV, 6, "middle")

    # name
    size = 64
    while measure(NAME, "disp", size, 3) > 800:
        size -= 1
    gid = d.uid("ng")
    d.defs.append(f'''<linearGradient id="{gid}" x1="0" y1="0" x2="0" y2="1">
  <stop offset="0" stop-color="#ffffff"/><stop offset=".6" stop-color="{PALE}"/><stop offset="1" stop-color="{PL}"/></linearGradient>''')
    glitch_text(d, 500, 212, NAME, "disp", size, f"url(#{gid})", 3, "middle", dur=3.6)

    # rule + diamonds
    rid = d.uid("rr")
    d.defs.append(f'''<linearGradient id="{rid}" x1="0" y1="0" x2="1" y2="0">
  <stop offset="0" stop-color="{P}" stop-opacity="0"/><stop offset=".5" stop-color="{P}"/><stop offset="1" stop-color="{P}" stop-opacity="0"/></linearGradient>''')
    d.add(f'<rect x="200" y="240" width="600" height="1" fill="url(#{rid})"/>')
    diamond(d, 500, 240.5, 7, PL)

    # roles row
    key, sz, ls, gap = "disp7", 13, 3.5, 34
    widths = [measure(r, key, sz, ls) for r in ROLES]
    total = sum(widths) + gap * (len(ROLES) - 1)
    x = 500 - total / 2
    for i, (r, w) in enumerate(zip(ROLES, widths)):
        d.T(x, 278, r, key, sz, PALE, ls)
        x += w
        if i < len(ROLES) - 1:
            diamond(d, x + gap / 2 - ls / 2, 273.5, 5, P)
            x += gap

    # bottom HUD
    d.T(52, 336, ">", "monob", 13, P)
    d.T(70, 336, "building real-time systems", "mono", 13, PL)
    cx = 70 + measure("building real-time systems", "mono", 13) + 6
    d.add(f'<rect x="{cx:.0f}" y="324" width="8" height="15" fill="{PL}">'
          f'<animate attributeName="opacity" values="1;0;1" keyTimes="0;.5;1" calcMode="discrete" dur="1.05s" repeatCount="indefinite"/></rect>')
    # signal bars
    for i in range(5):
        hh = 4 + i * 3
        d.add(f'<rect x="{874 + i*7}" y="{338-hh}" width="4" height="{hh}" fill="{P}" opacity="{.95 if i < 4 else .25}"/>')
    d.T(866, 336, "SYNC", "mono", 10, MUTED, 2, "end")

    tear_lines(d, 0, 90, 1000, 260, n=4, dur=4.6)
    d.save(f"{OUT}/hero.svg")


# ── section headers ───────────────────────────────────────────────

def section(fn, num, title, code, msg):
    d = Doc(1000, 86, f"{num} {title} — {msg}", seed=int(num))
    # outlined number
    d.T(4, 54, num, "disp", 46, "none", 0, extra=f'stroke="{P}" stroke-width="1.4" stroke-opacity=".9"')
    tw = glitch_text(d, 96, 50, title, "disp", 30, WHITE, 2.5, dur=4.2, offset=int(num) * .37, strength=.7)
    d.T(96 + tw + 14, 50, code, "mono", 12, MUTED, 1)

    # system notification chip
    label = msg
    lw = measure(label, "monob", 11, 2)
    w = lw + 120
    x = 1000 - w - 2
    d.add(f'<rect x="{x:.1f}" y="22" width="{w:.1f}" height="34" fill="#0a0318" fill-opacity=".95" '
          f'stroke="#6450ff" stroke-opacity=".55"/>')
    gid = d.uid("tg")
    d.defs.append(f'''<linearGradient id="{gid}" x1="0" y1="0" x2="1" y2="0">
  <stop offset="0" stop-color="#785aff" stop-opacity="0"/><stop offset=".5" stop-color="#785aff" stop-opacity=".95"/><stop offset="1" stop-color="#785aff" stop-opacity="0"/></linearGradient>''')
    d.add(f'<rect x="{x:.1f}" y="22" width="{w:.1f}" height="1" fill="url(#{gid})"/>')
    pulse_dot(d, x + 16, 39, 3)
    d.T(x + 28, 43, "SYSTEM", "monob", 10, PL, 2)
    d.add(f'<rect x="{x+92:.1f}" y="30" width="1" height="18" fill="{DIM}"/>')
    d.T(x + 104, 43.5, label, "monob", 11, PALE, 2)
    # scan sweep through the chip
    cid = d.uid("cc")
    d.defs.append(f'<clipPath id="{cid}"><rect x="{x:.1f}" y="22" width="{w:.1f}" height="34"/></clipPath>')
    d.add(f'<g clip-path="url(#{cid})"><rect x="{x:.1f}" y="22" width="40" height="34" fill="{P}" opacity=".12">'
          f'<animate attributeName="x" values="{x-40:.0f};{x+w:.0f}" dur="3.2s" repeatCount="indefinite"/></rect></g>')

    sweep_rule(d, 0, 78, 1000, dur=5 + int(num) * .3)
    d.save(f"{OUT}/{fn}.svg")


# ── skills ────────────────────────────────────────────────────────

def skills():
    cols, bw, gap, pad = 3, 304, 18, 20
    # layout pass to get heights
    def box_rows(items):
        x, rows = 0, 1
        for s in items:
            w = measure(s, "mono", 11) + 22
            if x + w > bw - 32:
                rows += 1
                x = 0
            x += w + 8
        return rows

    rowsets = [box_rows(i) for _, i in SKILLS]
    bh = 70 + max(rowsets) * 32
    H = 64 + 2 * bh + gap + 24
    d = Doc(1000, H, "Skill database — frontend, mobile, backend, AI & agents, real-time IoT, DevOps & data", seed=11)
    backdrop(d, glow=(.5, .3))
    nodes = sum(len(i) for _, i in SKILLS)
    d.T(pad + 6, 42, "// SKILL_DATABASE", "monob", 12, PL, 3)
    d.T(1000 - pad - 6, 42, f"{len(SKILLS):02d} TREES  ·  {nodes} NODES", "mono", 11, MUTED, 2, "end")

    for i, (name, items) in enumerate(SKILLS):
        c, r = i % cols, i // cols
        x = pad + c * (bw + gap)
        y = 64 + r * (bh + gap)
        d.add(f'<rect x="{x}" y="{y}" width="{bw}" height="{bh}" fill="#13062a" fill-opacity=".55" '
              f'stroke="{P}" stroke-opacity=".22"/>')
        d.add(f'<rect x="{x}" y="{y}" width="3" height="{bh}" fill="{P}" opacity=".8"/>')
        brackets(d, x, y, bw, bh, L=10, inset=0, op=.75, sw=1.5)
        d.T(x + 18, y + 30, name, "disp7", 12, WHITE, 2.4)
        d.T(x + bw - 16, y + 30, f"SKL-{i+1:02d}", "mono", 10, DIM, 1, "end")
        d.add(f'<rect x="{x+18}" y="{y+42}" width="{bw-36}" height="1" fill="{LINE}"/>')
        d.add(f'<rect x="{x+18}" y="{y+42}" width="36" height="1" fill="{P}"/>')
        px, py = x + 18, y + 54
        for s in items:
            w = measure(s, "mono", 11) + 22
            if px + w > x + bw - 14:
                px = x + 18
                py += 32
            pill(d, px, py, s)
            px += w + 8
    tear_lines(d, 0, 60, 1000, H - 80, n=2, dur=6)
    d.save(f"{OUT}/skills.svg")


# ── projects ──────────────────────────────────────────────────────

def projects():
    pad, gap, cw, ch = 20, 20, 470, 172
    rows = (len(PROJECTS) + 1) // 2
    H = 64 + rows * ch + (rows - 1) * gap + 24
    d = Doc(1000, H, "Project archive — EAIP, Industrial IoT, HappiSafe, PoleSyncTech Smart Pole, SmartArctic, RFID WMS", seed=21)
    backdrop(d, glow=(.5, .6))
    d.T(pad + 6, 42, "// PROJECT_LOG", "monob", 12, PL, 3)
    d.T(1000 - pad - 6, 42, f"{len(PROJECTS):02d} FILES  ·  CLEARANCE: PROFESSIONAL", "mono", 11, MUTED, 2, "end")

    for i, (code, title, desc, tags) in enumerate(PROJECTS):
        x = pad + (i % 2) * (cw + gap)
        y = 64 + (i // 2) * (ch + gap)
        d.add(f'<rect x="{x}" y="{y}" width="{cw}" height="{ch}" fill="#12052a" fill-opacity=".6" '
              f'stroke="{P}" stroke-opacity=".25"/>')
        # top glow edge
        gid = d.uid("pe")
        d.defs.append(f'''<linearGradient id="{gid}" x1="0" y1="0" x2="1" y2="0">
  <stop offset="0" stop-color="{P}"/><stop offset=".6" stop-color="{P}" stop-opacity=".15"/><stop offset="1" stop-color="{P}" stop-opacity="0"/></linearGradient>''')
        d.add(f'<rect x="{x}" y="{y}" width="{cw}" height="2" fill="url(#{gid})"/>')
        brackets(d, x, y, cw, ch, L=12, inset=0, op=.8, sw=1.5)

        d.T(x + 20, y + 30, f"FILE {i+1:02d}", "mono", 10, MUTED, 2)
        d.T(x + 84, y + 30, code, "monob", 10, P, 2.4)
        tag = "[ PROFESSIONAL ]"
        d.T(x + cw - 18, y + 30, tag, "mono", 9, DIM, 1.5, "end")

        tsz = 17
        while measure(title, "disp7", tsz, .6) > cw - 40:
            tsz -= .5
        d.T(x + 20, y + 62, title, "disp7", tsz, WHITE, .6)

        for j, line in enumerate(wrap(desc, "mono", 12, cw - 40)[:3]):
            d.T(x + 20, y + 88 + j * 18, line, "mono", 12, LAV)

        px = x + 20
        for t in tags:
            w = measure(t, "mono", 10) + 18
            if px + w > x + cw - 16:
                break
            pill(d, px, y + ch - 36, t, size=10, h=21, pad=9, fill="#2a0e4d")
            px += w + 6

        # idle scan line drifting down each card, staggered
        d.add(f'<rect x="{x+1}" y="{y}" width="{cw-2}" height="1" fill="{PL}" opacity="0">'
              f'<animate attributeName="y" values="{y};{y+ch}" dur="5s" begin="{i*.8:.1f}s" repeatCount="indefinite"/>'
              f'<animate attributeName="opacity" values="0;.35;.35;0" keyTimes="0;.1;.85;1" dur="5s" begin="{i*.8:.1f}s" repeatCount="indefinite"/></rect>')

    tear_lines(d, 0, 60, 1000, H - 80, n=3, dur=5.5)
    d.save(f"{OUT}/projects.svg")


# ── portal (shared by gate CTA + contact) ─────────────────────────

def portal(d, cx, cy, r):
    gid = d.uid("pg")
    d.defs.append(f'''<radialGradient id="{gid}" cx=".5" cy=".5" r=".5">
  <stop offset="0" stop-color="#ffffff" stop-opacity=".9"/><stop offset=".25" stop-color="{PL}" stop-opacity=".75"/>
  <stop offset=".6" stop-color="{PD}" stop-opacity=".35"/><stop offset="1" stop-color="{PD}" stop-opacity="0"/></radialGradient>''')
    d.add(f'<circle cx="{cx}" cy="{cy}" r="{r*1.25}" fill="url(#{gid})">'
          f'<animate attributeName="r" values="{r*1.1};{r*1.35};{r*1.1}" dur="3.2s" repeatCount="indefinite"/></circle>')
    for k, (rr, dash, dur, sw, op) in enumerate([(r, "6 10", 14, 1.6, .9), (r * .78, "2 6", 9, 1.2, .7),
                                                 (r * 1.18, "40 14 4 14", 22, 1, .5)]):
        direction = "0" if k % 2 == 0 else "360"
        end = "360" if k % 2 == 0 else "0"
        d.add(f'<circle cx="{cx}" cy="{cy}" r="{rr:.1f}" fill="none" stroke="{PL}" stroke-opacity="{op}" '
              f'stroke-width="{sw}" stroke-dasharray="{dash}">'
              f'<animateTransform attributeName="transform" type="rotate" values="{direction} {cx} {cy}; {end} {cx} {cy}" '
              f'dur="{dur}s" repeatCount="indefinite"/></circle>')
    d.add(f'<circle cx="{cx}" cy="{cy}" r="{r*.42:.1f}" fill="{BG0}" stroke="{PALE}" stroke-opacity=".8"/>')
    diamond(d, cx, cy, r * .22, PALE)


def gate_cta():
    d = Doc(1000, 150, "Enter the portfolio at muizkmz.vercel.app", seed=31)
    backdrop(d, glow=(.18, .5), grid=False)
    brackets(d, 0, 0, 1000, 150, L=16, inset=12, op=.7, sw=1.5)
    portal(d, 110, 75, 38)
    pulse_dot(d, 196, 47, 3, "#4ade80")
    d.T(208, 51, "GATE DETECTED", "monob", 11, "#86efac", 3)
    d.T(346, 51, "·  PORTFOLIO SITE  ·  LIVE", "mono", 11, MUTED, 3)
    glitch_text(d, 196, 94, "ENTER THE PORTFOLIO", "disp", 30, WHITE, 2, dur=4.4, offset=1.1, strength=.8)
    d.T(196, 122, "muizkmz.vercel.app", "monob", 13, PL, 1)
    d.T(376, 122, "ABOUT · SKILLS · PROJECTS · CAREER LOG", "mono", 10, DIM, 2)
    # arrow chevrons
    for k in range(3):
        x = 880 + k * 22
        d.add(f'<path d="M{x} 58 L{x+16} 75 L{x} 92" fill="none" stroke="{PL}" stroke-width="3">'
              f'<animate attributeName="opacity" values=".15;1;.15" dur="1.4s" begin="{k*.18:.2f}s" repeatCount="indefinite"/></path>')
    tear_lines(d, 180, 20, 800, 110, n=2, dur=5)
    d.save(f"{OUT}/gate.svg")


def contact():
    d = Doc(1000, 170, "Contact — gate status open, secure channel active", seed=41)
    backdrop(d, glow=(.85, .5))
    brackets(d, 0, 0, 1000, 170, L=18, inset=14, op=.8)
    d.T(44, 52, "// GATE", "monob", 12, PL, 3)
    glitch_text(d, 44, 100, "OPEN A CHANNEL", "disp", 34, WHITE, 2.5, dur=3.9, offset=.6)
    d.T(44, 132, "IoT · AI · Mobile · Full-Stack · DevOps — say hi, I reply.", "mono", 13, LAV)
    pulse_dot(d, 600, 62, 3, "#4ade80")
    d.T(612, 66, "GATE STATUS: OPEN", "monob", 11, "#86efac", 2)
    pulse_dot(d, 600, 88, 3)
    d.T(612, 92, "SECURE CHANNEL: ACTIVE", "monob", 11, PALE, 2)
    d.T(612, 118, "LOC  JOHOR BAHRU · GMT+8", "mono", 11, MUTED, 2)
    portal(d, 900, 88, 32)
    tear_lines(d, 0, 20, 1000, 130, n=2, dur=5.2)
    d.save(f"{OUT}/contact.svg")


def buttons():
    for fn, label, sub in BUTTONS:
        d = Doc(240, 56, f"{label.title()} — {sub}", seed=len(label))
        gid = d.uid("bb")
        d.defs.append(f'''<linearGradient id="{gid}" x1="0" y1="0" x2="1" y2="1">
  <stop offset="0" stop-color="{PD}" stop-opacity=".38"/><stop offset="1" stop-color="#581c87" stop-opacity=".55"/></linearGradient>''')
        d.add(f'<rect x="1" y="1" width="238" height="54" fill="{BG0}"/>')
        d.add(f'<rect x="1" y="1" width="238" height="54" fill="url(#{gid})" stroke="{P}" stroke-opacity=".65"/>')
        brackets(d, 1, 1, 238, 54, L=8, inset=0, color=PALE, op=.9, sw=1.5)
        d.T(18, 26, label, "disp7", 13, WHITE, 2.4)
        d.T(18, 43, sub, "mono", 10, LAV, .5)
        d.add(f'<path d="M210 20 L220 28 L210 36" fill="none" stroke="{PL}" stroke-width="2.2">'
              f'<animate attributeName="opacity" values=".3;1;.3" dur="1.6s" repeatCount="indefinite"/></path>')
        d.add(f'<rect x="1" y="1" width="30" height="54" fill="{PALE}" opacity=".08">'
              f'<animate attributeName="x" values="-30;240" dur="3.6s" begin="{len(label)*.2:.1f}s" repeatCount="indefinite"/></rect>')
        d.save(f"{OUT}/{fn}.svg")


def divider():
    d = Doc(1000, 28, "")
    gid = d.uid("dv")
    d.defs.append(f'''<linearGradient id="{gid}" x1="0" y1="0" x2="1" y2="0">
  <stop offset="0" stop-color="{P}" stop-opacity="0"/><stop offset=".5" stop-color="{P}" stop-opacity=".75"/><stop offset="1" stop-color="{P}" stop-opacity="0"/></linearGradient>''')
    d.add(f'<rect x="0" y="14" width="1000" height="1" fill="url(#{gid})"/>')
    sweep_rule(d, 100, 14, 800, dur=6, base="none")
    for k, x in enumerate((470, 500, 530)):
        diamond(d, x, 14.5, 6 if x == 500 else 4, PL if x == 500 else P, 1 if x == 500 else .7)
    d.T(40, 18, "///", "mono", 10, DIM, 2)
    d.T(960, 18, "///", "mono", 10, DIM, 2, "end")
    d.save(f"{OUT}/divider.svg")


def footer():
    d = Doc(1000, 110, "Quest continues — keep building, keep learning, keep improving", seed=51)
    backdrop(d, glow=(.5, .5), grid=False)
    pulse_dot(d, 44, 42, 3)
    d.T(56, 46, "[ SYSTEM ]", "monob", 11, PL, 3)
    d.T(160, 46, "QUEST CONTINUES  —  DAILY QUEST: SHIP SOMETHING", "mono", 11, LAV, 2)
    d.T(956, 46, "END OF FILE", "mono", 10, DIM, 3, "end")
    d.T(500, 82, "KEEP BUILDING  ·  KEEP LEARNING  ·  KEEP IMPROVING", "disp7", 13, PALE, 4, "middle")
    sweep_rule(d, 44, 60, 912, dur=5.5)
    d.save(f"{OUT}/footer.svg")


if __name__ == "__main__":
    hero()
    for s in SECTIONS:
        section(*s)
    skills()
    projects()
    gate_cta()
    contact()
    buttons()
    divider()
    footer()
    print("assets rendered")
