"""Shared drawing kit for the profile's "SYSTEM HUD" SVGs.

Every SVG embeds only the glyphs it actually uses (Orbitron + JetBrains Mono,
both SIL OFL — see scripts/fonts/), so the cards render identically on GitHub
without depending on the viewer's installed fonts.
"""

import base64
import io
import random
from pathlib import Path
from xml.sax.saxutils import escape

from fontTools.subset import Options, Subsetter
from fontTools.ttLib import TTFont

FONT_DIR = Path(__file__).parent / "fonts"

# palette — lifted from the eportfolio (rgba(168,85,247) / rgba(133,39,227) family)
BG0 = "#05020c"
BG1 = "#0d0520"
PANEL = "#0b0418"
P = "#a855f7"      # primary purple
PD = "#8527e3"     # deep purple
PL = "#c084fc"     # light purple
LAV = "#c4b5fd"    # lavender text
PALE = "#e9d5ff"
WHITE = "#f5f3ff"
IND = "#6366f1"
MAG = "#ff2bd6"    # glitch channel A
CYAN = "#22e5ff"   # glitch channel B
MUTED = "#8b7aa8"
DIM = "#4c3a6e"
LINE = "#24123f"

FONTS = {
    "disp": ("HudDisplay", "orbitron-latin-900-normal.woff2"),
    "disp7": ("HudDisplay7", "orbitron-latin-700-normal.woff2"),
    "mono": ("HudMono", "jetbrains-mono-latin-400-normal.woff2"),
    "monob": ("HudMonoB", "jetbrains-mono-latin-700-normal.woff2"),
}
FALLBACK = {
    "disp": "'Arial Black', Impact, sans-serif",
    "disp7": "'Arial Black', sans-serif",
    "mono": "ui-monospace, Menlo, Consolas, monospace",
    "monob": "ui-monospace, Menlo, Consolas, monospace",
}

_tt_cache = {}


def _tt(key):
    if key not in _tt_cache:
        _tt_cache[key] = TTFont(str(FONT_DIR / FONTS[key][1]))
    return _tt_cache[key]


def measure(text, key, size, ls=0.0):
    """Exact advance width of `text` in px (letter-spacing added per glyph)."""
    f = _tt(key)
    cmap = f.getBestCmap()
    hmtx = f["hmtx"]
    upm = f["head"].unitsPerEm
    space = hmtx[cmap[32]][0]
    total = 0
    for ch in text:
        g = cmap.get(ord(ch))
        total += hmtx[g][0] if g else space
    return total * size / upm + ls * len(text)


class Doc:
    """Collects SVG body, ids and the glyphs used per font."""

    def __init__(self, w, h, title, seed=7):
        self.w, self.h, self.title = w, h, title
        self.parts, self.defs, self.css = [], [], []
        self.used = {k: set() for k in FONTS}
        self._id = 0
        self.rng = random.Random(seed)

    def uid(self, p="i"):
        self._id += 1
        return f"{p}{self._id}"

    def add(self, s):
        self.parts.append(s)

    def text(self, x, y, s, key="mono", size=12, fill=LAV, ls=0, anchor="start",
             extra="", cls=""):
        self.used[key].update(s)
        fam = f"{FONTS[key][0]}, {FALLBACK[key]}"
        c = f' class="{cls}"' if cls else ""
        return (f'<text{c} x="{x:.1f}" y="{y:.1f}" font-family="{fam}" font-size="{size}" '
                f'letter-spacing="{ls}" fill="{fill}" text-anchor="{anchor}" {extra}>'
                f"{escape(s)}</text>")

    def T(self, *a, **k):
        self.add(self.text(*a, **k))

    def _font_css(self):
        out = []
        for key, (fam, fn) in FONTS.items():
            chars = self.used[key]
            if not chars:
                continue
            f = TTFont(str(FONT_DIR / fn), recalcTimestamp=False)
            opts = Options()
            opts.flavor = "woff2"
            opts.layout_features = ["kern"]
            opts.name_IDs = []
            opts.notdef_outline = False
            sub = Subsetter(options=opts)
            sub.populate(text="".join(sorted(chars)) + " ")
            sub.subset(f)
            buf = io.BytesIO()
            f.flavor = "woff2"
            f.save(buf)
            b64 = base64.b64encode(buf.getvalue()).decode()
            out.append(f"@font-face{{font-family:'{fam}';"
                       f"src:url(data:font/woff2;base64,{b64}) format('woff2');}}")
        return "\n".join(out)

    def render(self):
        style = self._font_css() + "\n" + "\n".join(self.css) + (
            "\n@media (prefers-reduced-motion: reduce){*{animation:none!important}}")
        return (
            f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {self.w} {self.h}" '
            f'width="{self.w}" height="{self.h}" role="img" aria-label="{escape(self.title)}">\n'
            f"<title>{escape(self.title)}</title>\n<defs>\n<style>\n{style}\n</style>\n"
            + "\n".join(self.defs) + "\n</defs>\n" + "\n".join(self.parts) + "\n</svg>\n")

    def save(self, path):
        Path(path).parent.mkdir(parents=True, exist_ok=True)
        Path(path).write_text(self.render(), encoding="utf-8")


# ── reusable pieces ──────────────────────────────────────────────

def backdrop(d, x=0, y=0, w=None, h=None, rx=14, glow=(0.5, 0.45), grid=True):
    w = w or d.w
    h = h or d.h
    g, gl, sl, clip = d.uid("bg"), d.uid("gl"), d.uid("sl"), d.uid("cp")
    d.defs.append(f'''<linearGradient id="{g}" x1="0" y1="0" x2="1" y2="1">
  <stop offset="0" stop-color="{BG0}"/><stop offset=".55" stop-color="{BG1}"/><stop offset="1" stop-color="{BG0}"/></linearGradient>
<radialGradient id="{gl}" cx="{glow[0]}" cy="{glow[1]}" r=".6">
  <stop offset="0" stop-color="{PD}" stop-opacity=".30"/><stop offset=".55" stop-color="{IND}" stop-opacity=".06"/><stop offset="1" stop-color="{PD}" stop-opacity="0"/></radialGradient>
<pattern id="{sl}" width="4" height="4" patternUnits="userSpaceOnUse"><rect width="4" height="1" fill="#ffffff" opacity=".035"/></pattern>
<clipPath id="{clip}"><rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}"/></clipPath>''')
    d.add(f'<g clip-path="url(#{clip})">')
    d.add(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="url(#{g})"/>')
    d.add(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="url(#{gl})"/>')
    if grid:
        gp = d.uid("gp")
        d.defs.append(f'<pattern id="{gp}" width="40" height="40" patternUnits="userSpaceOnUse">'
                      f'<path d="M40 0H0V40" fill="none" stroke="{P}" stroke-opacity=".07" stroke-width="1"/></pattern>')
        d.add(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="url(#{gp})"/>')
    d.add(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="url(#{sl})"/>')
    d.add("</g>")
    d.add(f'<rect x="{x+.75}" y="{y+.75}" width="{w-1.5}" height="{h-1.5}" rx="{rx}" fill="none" '
          f'stroke="{P}" stroke-opacity=".28" stroke-width="1.5"/>')
    return clip


def brackets(d, x, y, w, h, L=22, inset=14, color=P, op=.85, sw=2):
    a, b, c, e = x + inset, y + inset, x + w - inset, y + h - inset
    p = (f"M{a} {b+L}V{b}H{a+L} M{c-L} {b}H{c}V{b+L} "
         f"M{c} {e-L}V{e}H{c-L} M{a+L} {e}H{a}V{e-L}")
    d.add(f'<path d="{p}" fill="none" stroke="{color}" stroke-opacity="{op}" stroke-width="{sw}"/>')


def sweep_rule(d, x, y, w, dur=4.5, color=P, base=LINE):
    gid = d.uid("sw")
    d.defs.append(f'''<linearGradient id="{gid}" gradientUnits="userSpaceOnUse" x1="0" y1="0" x2="260" y2="0">
  <stop offset="0" stop-color="{color}" stop-opacity="0"/><stop offset=".5" stop-color="{PALE}" stop-opacity=".95"/><stop offset="1" stop-color="{color}" stop-opacity="0"/>
  <animateTransform attributeName="gradientTransform" type="translate" values="{x-280} 0; {x+w+20} 0" dur="{dur}s" repeatCount="indefinite"/></linearGradient>''')
    d.add(f'<rect x="{x}" y="{y}" width="{w}" height="1" fill="{base}"/>')
    d.add(f'<rect x="{x}" y="{y-.5}" width="{w}" height="2" fill="url(#{gid})"/>')


def pulse_dot(d, cx, cy, r=3.5, color=P, dur=1.6):
    d.add(f'<circle cx="{cx}" cy="{cy}" r="{r*2.6}" fill="{color}" opacity="0">'
          f'<animate attributeName="r" values="{r};{r*3}" dur="{dur}s" repeatCount="indefinite"/>'
          f'<animate attributeName="opacity" values=".55;0" dur="{dur}s" repeatCount="indefinite"/></circle>')
    d.add(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{color}"/>')


def diamond(d, cx, cy, s=4, fill=P, op=1):
    d.add(f'<rect x="{cx-s/2}" y="{cy-s/2}" width="{s}" height="{s}" fill="{fill}" opacity="{op}" '
          f'transform="rotate(45 {cx} {cy})"/>')


def glitch_text(d, x, y, s, key="disp", size=40, fill=WHITE, ls=0, anchor="start",
                dur=3.4, offset=0.0, glow=True, height=None, strength=1.0):
    """Text with an RGB-split tear: calm most of the time, then short bursts
    where magenta/cyan slices jump sideways (SMIL, discrete — works in <img>)."""
    w = measure(s, key, size, ls)
    left = x - (w / 2 if anchor == "middle" else w if anchor == "end" else 0)
    hgt = height or size * 1.05
    top = y - size * 0.86
    flt = ""
    if glow:
        fid = d.uid("gw")
        d.defs.append(f'<filter id="{fid}" x="-20%" y="-60%" width="140%" height="220%">'
                      f'<feGaussianBlur stdDeviation="{size/9:.1f}" result="b"/>'
                      f'<feColorMatrix in="b" values="0 0 0 0 .66  0 0 0 0 .33  0 0 0 0 .97  0 0 0 .85 0"/>'
                      f'<feMerge><feMergeNode/><feMergeNode in="SourceGraphic"/></feMerge></filter>')
        flt = f' filter="url(#{fid})"'

    # keyTimes: idle → burst frames → idle
    kt = "0;.62;.64;.66;.69;.71;.83;.85;.87;1"

    def band(seed_shift):
        r = random.Random(f"{s}|{seed_shift}|{offset}")
        ys, hs, xs = [], [], []
        for i in range(10):
            if i in (0, 5, 9):
                ys.append(top); hs.append(0); xs.append(0)
            else:
                yy = top + r.uniform(0, hgt * .8)
                ys.append(yy)
                hs.append(r.uniform(hgt * .08, hgt * .32))
                xs.append(r.choice([-1, 1]) * r.uniform(4, 11) * strength)
        return ys, hs, xs

    out = [f'<g{flt}>', d.text(x, y, s, key, size, fill, ls, anchor), "</g>"]
    for color, sh in ((MAG, 1), (CYAN, 2)):
        cid = d.uid("gc")
        ys, hs, xs = band(sh)
        d.defs.append(
            f'<clipPath id="{cid}"><rect x="{left-30:.1f}" y="{top:.1f}" width="{w+60:.1f}" height="0">'
            f'<animate attributeName="y" values="{";".join(f"{v:.1f}" for v in ys)}" keyTimes="{kt}" '
            f'calcMode="discrete" dur="{dur}s" begin="{offset}s" repeatCount="indefinite"/>'
            f'<animate attributeName="height" values="{";".join(f"{v:.1f}" for v in hs)}" keyTimes="{kt}" '
            f'calcMode="discrete" dur="{dur}s" begin="{offset}s" repeatCount="indefinite"/>'
            f"</rect></clipPath>")
        tx = ";".join(f"{v:.1f} 0" for v in xs)
        out.append(
            f'<g clip-path="url(#{cid})" style="mix-blend-mode:screen">'
            f'<g><animateTransform attributeName="transform" type="translate" values="{tx}" keyTimes="{kt}" '
            f'calcMode="discrete" dur="{dur}s" begin="{offset}s" repeatCount="indefinite"/>'
            + d.text(x, y, s, key, size, color, ls, anchor) + "</g></g>")
        # always-on faint chromatic fringe
    fr = 1.2 * strength
    out.insert(0, f'<g opacity=".45" style="mix-blend-mode:screen">'
               + d.text(x - fr, y, s, key, size, MAG, ls, anchor)
               + d.text(x + fr, y, s, key, size, CYAN, ls, anchor) + "</g>")
    d.add("\n".join(out))
    return w


def tear_lines(d, x, y, w, h, n=3, dur=5.0):
    """Occasional full-width horizontal tear bars across a panel."""
    for i in range(n):
        yy = y + d.rng.uniform(.1, .9) * h
        ww = d.rng.uniform(.25, .7) * w
        xx = x + d.rng.uniform(0, w - ww)
        col = (MAG, CYAN, PALE)[i % 3]
        b = d.rng.uniform(0, dur)
        d.add(f'<rect x="{xx:.0f}" y="{yy:.0f}" width="{ww:.0f}" height="{d.rng.choice([1,2,2,3])}" '
              f'fill="{col}" opacity="0">'
              f'<animate attributeName="opacity" values="0;.7;0;.45;0" keyTimes="0;.02;.035;.05;1" '
              f'dur="{dur}s" begin="{b:.2f}s" repeatCount="indefinite"/></rect>')


def embers(d, x, y, w, h, n=26, color=PL):
    for _ in range(n):
        cx = x + d.rng.uniform(0, w)
        cy = y + h - d.rng.uniform(0, h * .35)
        r = d.rng.uniform(.6, 1.8)
        rise = d.rng.uniform(h * .45, h * .95)
        drift = d.rng.uniform(-18, 18)
        dur = d.rng.uniform(5, 11)
        b = -d.rng.uniform(0, dur)
        d.add(f'<circle cx="{cx:.0f}" cy="{cy:.0f}" r="{r:.1f}" fill="{color}">'
              f'<animateTransform attributeName="transform" type="translate" values="0 0; {drift:.0f} {-rise:.0f}" '
              f'dur="{dur:.1f}s" begin="{b:.1f}s" repeatCount="indefinite"/>'
              f'<animate attributeName="opacity" values="0;.9;.6;0" dur="{dur:.1f}s" begin="{b:.1f}s" repeatCount="indefinite"/></circle>')


def pill(d, x, y, s, size=11, h=24, key="mono", fill="#2a0e4d", stroke=P, text=PALE, pad=11):
    w = measure(s, key, size) + pad * 2
    d.add(f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h}" rx="3" fill="{fill}" '
          f'fill-opacity=".55" stroke="{stroke}" stroke-opacity=".45"/>')
    d.T(x + pad, y + h / 2 + size * .36, s, key, size, text)
    return w


def wrap(text, key, size, maxw, ls=0):
    words, lines, cur = text.split(), [], ""
    for wd in words:
        t = (cur + " " + wd).strip()
        if measure(t, key, size, ls) <= maxw:
            cur = t
        else:
            lines.append(cur)
            cur = wd
    if cur:
        lines.append(cur)
    return lines
