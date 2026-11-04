"""Builds every SVG in ../assets for the IbramDawwaGmbH profile README.

Run:  python tools/build_assets.py
Edit the CONTENT section to change text, services or stack, then run again.
Fonts are Google Fonts subsets (SIL Open Font License), embedded so GitHub renders them.
"""
import base64
import math
import random
from pathlib import Path
from xml.sax.saxutils import escape

ROOT = Path(__file__).resolve().parent
OUT = ROOT.parent / "assets"
OUT.mkdir(exist_ok=True)

# ---------------------------------------------------------------- brand
INK, PANEL, RAISE = "#0d0d0d", "#171717", "#222120"
PAPER, STONE, MUTE = "#fcf7f3", "#d3ccc5", "#958e88"
EMBER, EMBER_DEEP = "#ff6a3a", "#e8572a"
LINE_DARK = "rgba(252,247,243,.14)"

# ---------------------------------------------------------------- content
HEADLINE = ["MOST AGENCIES AUTOMATE.", "MOST STUDIOS CREATE.", "WE DO BOTH."]
HUD = ["IBRAM & DAWWA GMBH", "KI-SYSTEME × KI-STUDIO", "REGENSBURG · DE"]
TYPING = [
    "AI voicebots that answer when your team is busy",
    "Chatbots that qualify leads around the clock",
    "Workflows that move data without copy-and-paste",
    "Campaign visuals for 9:16, 4:5 and 1:1",
    "Brand films rendered in code",
]
UNITS = {
    "systems": ("(A) I&D SYSTEMS", ["AUTOMATION &", "AI AGENTS"], "ibramdawwa.de/systems", [
        "AI voicebots & phone assistants",
        "AI chatbots that qualify leads 24/7",
        "Workflow automation",
        "CRM & API integrations",
        "Dashboards & reporting",
    ]),
    "studio": ("(B) I&D STUDIO", ["AI MEDIA &", "WEBSITES"], "ibramdawwa.de/studio", [
        "AI media production in 9:16 · 4:5 · 1:1",
        "Campaign visuals for ads",
        "Websites, staged with motion",
        "SEO, checked against sources",
        "Brand films rendered in code",
    ]),
}
HEADERS = {
    "units": ("(01)", "TWO UNITS. ONE TEAM.", "SYSTEMS × STUDIO"),
    "flow": ("(02)", "FROM CHAOS TO ORDER", "HOW A LEAD MOVES"),
    "oss": ("(03)", "OPEN SOURCE", "PROOF OF WORK"),
    "studio": ("(04)", "STUDIO WORK", "CASE STUDIES"),
    "stack": ("(05)", "STACK", "TOOL-AGNOSTIC"),
    "activity": ("(06)", "ACTIVITY", "UPDATED DAILY"),
    "founder": ("(07)", "WHO BUILDS THIS", "REGENSBURG"),
}
STACK = ["Claude · MCP", "Python", "TypeScript", "JavaScript", "Next.js", "React",
         "Remotion", "GSAP", "WordPress · PHP", "Voice AI", "CRM APIs", "GitHub Actions"]
BADGES = {
    "web": ("web", "ibramdawwa.de"),
    "linkedin": ("linkedin", "Ibrahim Anjro"),
    "instagram": ("instagram", "@ai.with.ibrahim"),
    "call": ("book", "Strategy call"),
    "email": ("email", "info@ibramdawwa-gmbh.de"),
}
FOOTER = ["REPLY WITHIN 1 BUSINESS DAY", "EU-FIRST DATA PROCESSING", "BUILT IN REGENSBURG"]


# ---------------------------------------------------------------- helpers
def font(name, file):
    data = base64.b64encode((ROOT / "fonts" / file).read_bytes()).decode()
    return f"@font-face{{font-family:'{name}';src:url(data:font/woff2;base64,{data}) format('woff2');}}"


FONT_DISPLAY = font("IDDisplay", "archivo.woff2")
FONT_MONO = font("IDMono", "jbmono.woff2")
FONT_BODY = font("IDBody", "dmsans.woff2")
D = "font-family:IDDisplay,'Arial Narrow',Arial,sans-serif;font-weight:800"
M = "font-family:IDMono,ui-monospace,Consolas,monospace;font-weight:500"
B = "font-family:IDBody,'Segoe UI',Arial,sans-serif"
MONO_W = 0.6  # JetBrains Mono advance width per em


def svg(w, h, body, css="", fonts=(), label=""):
    style = "".join(fonts) + css + "@media (prefers-reduced-motion:reduce){*{animation:none!important}}"
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" '
            f'role="img" aria-label="{escape(label)}"><title>{escape(label)}</title>'
            f"<style>{style}</style>{body}</svg>")


def t(x, y, s, style, fill, anchor="start", extra=""):
    return f'<text x="{x}" y="{y}" style="{style}" fill="{fill}" text-anchor="{anchor}" {extra}>{escape(s)}</text>'


def dedupe(times, values):
    """SMIL keyTimes must strictly increase for Firefox; keep the last value at each time."""
    out = {}
    for tm, v in zip(times, values):
        out[round(tm, 6)] = v
    return list(out.keys()), list(out.values())


def write(name, content):
    (OUT / name).write_text(content, encoding="utf-8")
    print(f"{name:28s} {len(content.encode()) / 1024:6.1f} KB")


# ---------------------------------------------------------------- hero
def hero(theme):
    W, H = 1280, 420
    dark = theme == "dark"
    bg = INK if dark else PAPER
    fg = PAPER if dark else INK
    hud = MUTE if dark else "#6f6862"
    acc = EMBER if dark else EMBER_DEEP
    rnd = random.Random(7)
    layers = []
    for li, (count, rmin, rmax, dist) in enumerate([(260, .8, 1.6, 0), (150, 1.2, 2.4, 70), (45, 2, 3.4, 92)]):
        pts = []
        for _ in range(count):
            if rnd.random() < .72:  # dense cloud upper right, like the site's particle field
                x = rnd.gauss(W * .70, W * .14)
                y = rnd.gauss(H * .36, H * .17)
            else:
                x, y = rnd.uniform(0, W), rnd.uniform(0, H * .9)
            if 0 < x < W and 0 < y < H:
                pts.append((round(x, 1), round(y, 1), round(rnd.uniform(rmin, rmax), 2), round(rnd.uniform(.5, 1), 2)))
        lines, edges = [], []
        if dist:
            deg = [0] * len(pts)
            for i, a in enumerate(pts):
                for j in range(i + 1, len(pts)):
                    b = pts[j]
                    d = math.dist(a[:2], b[:2])
                    if d < dist and deg[i] < 3 and deg[j] < 3:
                        deg[i] += 1
                        deg[j] += 1
                        op = round(.5 * (1 - d / dist) + .1, 2)
                        lines.append(f'<line x1="{a[0]}" y1="{a[1]}" x2="{b[0]}" y2="{b[1]}" stroke-opacity="{op}"/>')
                        edges.append((a, b))
        dots = []
        for k, (x, y, r, a) in enumerate(pts):
            cls = ' class="tw"' if k % 3 == 0 else ""
            delay = f' style="animation-delay:-{rnd.uniform(0, 4):.1f}s"' if cls else ""
            dots.append(f'<circle cx="{x}" cy="{y}" r="{r}" fill-opacity="{a}"{cls}{delay}/>')
        pulses = []
        if li == 1:  # data pulses travelling along the network, as on the homepage
            for n, (a, b) in enumerate(sorted(edges, key=lambda e: -math.dist(e[0][:2], e[1][:2]))[:7]):
                pid = f"e{theme}{n}"
                pulses.append(f'<path id="{pid}" d="M{a[0]} {a[1]} L{b[0]} {b[1]}" fill="none"/>'
                              f'<circle r="3.6" fill="{PAPER if dark else acc}"><animateMotion dur="{1.6 + n * .25:.2f}s" '
                              f'begin="{n * .4:.1f}s" repeatCount="indefinite"><mpath href="#{pid}"/></animateMotion></circle>')
        layers.append(f'<g class="l{li}"><g stroke="{acc}" stroke-width=".7">{"".join(lines)}</g>'
                      f'<g fill="{acc}">{"".join(dots)}</g>{"".join(pulses)}</g>')

    css = (".l0{animation:d0 24s ease-in-out infinite alternate}.l1{animation:d1 18s ease-in-out infinite alternate}"
           ".l2{animation:d2 14s ease-in-out infinite alternate}"
           "@keyframes d0{to{transform:translate(-10px,6px)}}@keyframes d1{to{transform:translate(16px,-9px)}}"
           "@keyframes d2{to{transform:translate(-22px,-12px)}}"
           ".tw{animation:tw 4s ease-in-out infinite}@keyframes tw{50%{opacity:.15}}"
           ".r{animation:up 1s cubic-bezier(.2,.7,.2,1) backwards}"
           "@keyframes up{from{opacity:0;transform:translateY(16px)}}"
           ".glow{animation:br 7s ease-in-out infinite;transform-origin:896px 150px}@keyframes br{50%{transform:scale(1.18);opacity:.7}}")
    hudrow = (t(56, 48, HUD[0], M + ";font-size:12px;letter-spacing:2px", hud)
              + t(W / 2, 48, HUD[1], M + ";font-size:12px;letter-spacing:2px", hud, "middle")
              + t(W - 56, 48, HUD[2], M + ";font-size:12px;letter-spacing:2px", hud, "end")
              + f'<line x1="56" y1="64" x2="{W - 56}" y2="64" stroke="{hud}" stroke-opacity=".25"/>')
    head = ""
    for i, line in enumerate(HEADLINE):
        col = acc if i == len(HEADLINE) - 1 else fg
        head += t(52, 252 + i * 62, line, D + f";font-size:68px;letter-spacing:.5px;animation-delay:{.15 + i * .18:.2f}s", col, extra='class="r"')
    cta = t(W - 56, 374, "→ ibramdawwa.de", M + ";font-size:14px;letter-spacing:1px", acc, "end")
    body = (f'<rect width="{W}" height="{H}" fill="{bg}"/>'
            f'<defs><radialGradient id="g{theme}"><stop offset="0" stop-color="{acc}" stop-opacity="{.16 if dark else .10}"/>'
            f'<stop offset="1" stop-color="{acc}" stop-opacity="0"/></radialGradient></defs>'
            f'<circle class="glow" cx="896" cy="150" r="420" fill="url(#g{theme})"/>'
            + "".join(layers) + hudrow + head + cta)
    write(f"hero-{theme}.svg", svg(W, H, body, css, (FONT_DISPLAY, FONT_MONO),
                                   "Ibram & Dawwa: Most agencies automate. Most studios create. We do both."))


# ---------------------------------------------------------------- typing line
def typing():
    W, H, X0, Y, FS = 720, 52, 28, 33, 19
    cw = FS * MONO_W
    tx = X0 + 2 * cw  # after "> "
    TYPE, DEL, HOLD, GAP = .045, .02, 1.8, .35
    # build the timeline
    events, now, starts = [], 0.0, []
    for s in TYPING:
        starts.append(now)
        for n in range(len(s) + 1):
            events.append((now, len(starts) - 1, n))
            now += TYPE
        now += HOLD
        for n in range(len(s) - 1, -1, -1):
            events.append((now, len(starts) - 1, n))
            now += DEL
        now += GAP
    total = now

    def kt(v):
        return f"{v / total:.5f}"

    texts, clips = [], []
    for i, s in enumerate(TYPING):
        ev = [(tm, n) for tm, li, n in events if li == i]
        times = [0.0] + [tm for tm, _ in ev]
        widths = [0] + [round(n * cw, 2) for _, n in ev]
        times, widths = dedupe(times, widths)
        clips.append(f'<clipPath id="c{i}"><rect x="{tx}" y="0" height="{H}" width="0">'
                     f'<animate attributeName="width" dur="{total:.2f}s" repeatCount="indefinite" calcMode="discrete" '
                     f'values="{";".join(map(str, widths))}" keyTimes="{";".join(kt(x) for x in times)}"/></rect></clipPath>')
        texts.append(f'<g clip-path="url(#c{i})">{t(tx, Y, s, M + f";font-size:{FS}px", STONE)}</g>')
    ctimes = [0.0] + [tm for tm, _, _ in events]
    cx = [tx] + [round(tx + n * cw + 2, 2) for _, _, n in events]
    ctimes, cx = dedupe(ctimes, cx)
    caret = (f'<rect class="cr" x="{tx}" y="{Y - FS + 3}" width="{cw:.1f}" height="{FS + 2}" fill="{EMBER}">'
             f'<animate attributeName="x" dur="{total:.2f}s" repeatCount="indefinite" calcMode="discrete" '
             f'values="{";".join(map(str, cx))}" keyTimes="{";".join(kt(x) for x in ctimes)}"/></rect>')
    css = ".cr{animation:bl 1s steps(1) infinite}@keyframes bl{50%{opacity:0}}"
    body = (f'<rect width="{W}" height="{H}" rx="{H / 2}" fill="{INK}" stroke="{LINE_DARK}"/>'
            f'<defs>{"".join(clips)}</defs>' + t(X0, Y, ">", M + f";font-size:{FS}px", EMBER) + "".join(texts) + caret)
    write("typing.svg", svg(W, H, body, css, (FONT_MONO,), "What we build: " + "; ".join(TYPING)))


# ---------------------------------------------------------------- unit cards
def unit(key):
    W, H = 620, 340
    label, title, url, items = UNITS[key]
    css = ".glow{animation:br 6s ease-in-out infinite;transform-box:fill-box;transform-origin:center}" \
          "@keyframes br{50%{transform:scale(1.22);opacity:.65}}"
    rows = ""
    for i, it in enumerate(items):
        y = 206 + i * 28
        rows += t(36, y, f"{i + 1:02d}", M + ";font-size:12px", MUTE) + t(72, y, it, B + ";font-size:16px", STONE)
    body = (f'<defs><clipPath id="k"><rect width="{W}" height="{H}" rx="14"/></clipPath>'
            f'<radialGradient id="gl"><stop offset="0" stop-color="{EMBER}" stop-opacity=".22"/>'
            f'<stop offset="1" stop-color="{EMBER}" stop-opacity="0"/></radialGradient></defs>'
            f'<g clip-path="url(#k)"><rect width="{W}" height="{H}" fill="{PANEL}"/>'
            f'<circle class="glow" cx="{W - 40}" cy="{H + 10}" r="230" fill="url(#gl)"/></g>'
            f'<rect x=".5" y=".5" width="{W - 1}" height="{H - 1}" rx="14" fill="none" stroke="{LINE_DARK}"/>'
            + t(36, 52, label, M + ";font-size:13px;letter-spacing:2px", EMBER)
            + t(W - 36, 52, url + " →", M + ";font-size:12px", MUTE, "end")
            + t(34, 112, title[0], D + ";font-size:46px", PAPER)
            + t(34, 160, title[1], D + ";font-size:46px", EMBER)
            + rows)
    write(f"unit-{key}.svg", svg(W, H, body, css, (FONT_DISPLAY, FONT_MONO, FONT_BODY),
                                 f"{label}: " + ", ".join(items)))


# ---------------------------------------------------------------- chaos to order flow
def flow(theme):
    W, H = 1280, 330
    dark = theme == "dark"
    bg, box, stroke = (INK, PANEL, LINE_DARK) if dark else (PAPER, "#ffffff", "rgba(13,13,13,.16)")
    fg, sub = (STONE, MUTE) if dark else ("#2b2927", "#6f6862")
    acc = EMBER if dark else EMBER_DEEP
    wire = "rgba(252,247,243,.22)" if dark else "rgba(13,13,13,.22)"
    mono = M + ";font-size:13px;letter-spacing:1.5px"
    inputs = ["ANRUF", "CHAT", "FORMULAR", "E-MAIL"]
    agent = (470, 150, 190, 64)
    ay = agent[1] + agent[3] / 2
    parts, paths, pulses = [], [], []
    for i, name in enumerate(inputs):
        y = 92 + i * 56
        parts.append(f'<rect x="60" y="{y}" width="160" height="38" rx="6" fill="{box}" stroke="{stroke}"/>'
                     + t(140, y + 24, name, mono, fg, "middle"))
        pid = f"in{theme}{i}"
        paths.append(f'<path id="{pid}" d="M220 {y + 19} C 340 {y + 19}, 350 {ay}, {agent[0]} {ay}"/>')
        pulses.append((pid, 2.4, i * .6))
    paths.append(f'<path id="a{theme}" d="M{agent[0] + agent[2]} {ay} L780 {ay}"/>')
    paths.append(f'<path id="b{theme}" d="M930 {ay} L1030 {ay}"/>')
    pulses += [(f"a{theme}", 1.2, 0), (f"a{theme}", 1.2, .6), (f"b{theme}", 1.2, .3)]
    pulse_svg = "".join(
        f'<circle r="4" fill="{acc}"><animateMotion dur="{d}s" begin="{b}s" repeatCount="indefinite">'
        f'<mpath href="#{p}"/></animateMotion></circle>' for p, d, b in pulses)
    ax, ayy, aw, ah = agent
    agent_svg = (f'<rect x="{ax}" y="{ayy}" width="{aw}" height="{ah}" rx="8" fill="{acc}"/>'
                 + t(ax + aw / 2, ayy + 39, "KI-AGENT", D + ";font-size:28px;letter-spacing:1px", INK, "middle")
                 + f'<rect class="ring" x="{ax}" y="{ayy}" width="{aw}" height="{ah}" rx="8" fill="none" stroke="{acc}" stroke-width="2"/>')
    crm = (f'<rect x="780" y="{ay - 19}" width="150" height="38" rx="6" fill="{box}" stroke="{stroke}"/>'
           + t(855, ay + 5, "CRM", mono, fg, "middle"))
    report = (f'<rect x="1030" y="{ay - 19}" width="190" height="38" rx="6" fill="{box}" stroke="{acc}"/>'
              + t(1125, ay + 5, "REPORT", mono, acc, "middle"))
    counts = [47, 38, 29, 21, 13, 6, 2, 0]
    n = len(counts)
    cyc = 6.4
    nums = ""
    for i, c in enumerate(counts):
        base = "1" if i == 0 else "0"
        kts = "0;" + (f"{i / n:.4f};" if i else "") + f"{(i + 1) / n:.4f}" if i < n - 1 else "0;" + f"{i / n:.4f}"
        vals = ("1;0" if i == 0 else "0;1;0") if i < n - 1 else "0;1"
        nums += (f'<text x="1125" y="128" style="{D};font-size:44px" fill="{acc if c == 0 else fg}" text-anchor="middle" opacity="{base}">{c}'
                 f'<animate attributeName="opacity" dur="{cyc}s" repeatCount="indefinite" calcMode="discrete" values="{vals}" keyTimes="{kts}"/></text>')
    counter = t(1125, 84, "UNGELESEN", M + ";font-size:11px;letter-spacing:2px", sub, "middle") + nums
    stages = (t(140, 318, "(01) CHAOS", mono, sub, "middle")
              + t(565, 318, "(02) ORDNUNG", mono, sub, "middle")
              + t(1125, 318, "(03) OUTPUT", mono, sub, "middle"))
    headline = t(60, 50, "47 UNGELESEN. SECHS TOOLS. KEIN WORKFLOW.", M + ";font-size:13px;letter-spacing:1.5px", sub)
    css = ".ring{animation:rg 2.4s ease-out infinite;transform-box:fill-box;transform-origin:center}" \
          "@keyframes rg{0%{opacity:.9;transform:scale(1)}100%{opacity:0;transform:scale(1.18)}}"
    body = (f'<rect width="{W}" height="{H}" rx="14" fill="{bg}"/>'
            f'<g fill="none" stroke="{wire}" stroke-width="1.3">{"".join(paths)}</g>'
            + headline + "".join(parts) + agent_svg + crm + report + counter + stages + pulse_svg)
    write(f"flow-{theme}.svg", svg(W, H, body, css, (FONT_DISPLAY, FONT_MONO),
                                   "Calls, chats, forms and emails flow into an AI agent, then the CRM, then a report."))


# ---------------------------------------------------------------- section headers
def header(key):
    W, H = 1280, 72
    num, title, right = HEADERS[key]
    body = (f'<rect width="{W}" height="{H}" rx="10" fill="{INK}"/>'
            f'<rect x="0" y="{H - 3}" width="120" height="3" fill="{EMBER}"><animate attributeName="width" '
            f'values="120;260;120" dur="5s" repeatCount="indefinite"/></rect>'
            + t(28, 45, num, M + ";font-size:15px", EMBER)
            + t(84, 48, title, D + ";font-size:32px;letter-spacing:.5px", PAPER)
            + t(W - 28, 44, right, M + ";font-size:12px;letter-spacing:2px", MUTE, "end"))
    write(f"h-{key}.svg", svg(W, H, body, "", (FONT_DISPLAY, FONT_MONO), f"{num} {title}"))


# ---------------------------------------------------------------- badges
def badge(key):
    label, value = BADGES[key]
    fs, pad, H = 12, 11, 30
    cw = fs * MONO_W
    lw = round(len(label) * cw + pad * 2)
    vw = round(len(value) * cw + pad * 2)
    W = lw + vw
    body = (f'<defs><clipPath id="r"><rect width="{W}" height="{H}" rx="5"/></clipPath></defs>'
            f'<g clip-path="url(#r)"><rect width="{lw}" height="{H}" fill="{RAISE}"/>'
            f'<rect x="{lw}" width="{vw}" height="{H}" fill="{EMBER}"/></g>'
            + t(pad, 19.5, label, M + f";font-size:{fs}px", STONE)
            + t(lw + pad, 19.5, value, M + f";font-size:{fs}px;font-weight:600", INK))
    write(f"badge-{key}.svg", svg(W, H, body, "", (FONT_MONO,), f"{label}: {value}"))


# ---------------------------------------------------------------- stack strip
def stack():
    W, fs, pad, gap, ch = 1280, 14, 16, 10, 38
    cw = fs * MONO_W
    rows, row, width = [], [], 0
    for item in STACK:
        w = round(len(item) * cw + pad * 2)
        if row and width + gap + w > W - 40:
            rows.append((row, width))
            row, width = [], 0
        width += (gap if row else 0) + w
        row.append((item, w))
    rows.append((row, width))
    if len(rows) > 1:  # balance the rows so nothing sits alone on the last line
        per = math.ceil(len(STACK) / len(rows))
        sized = [(item, round(len(item) * cw + pad * 2)) for item in STACK]
        rows = [(chunk, sum(w for _, w in chunk) + gap * (len(chunk) - 1))
                for chunk in (sized[i:i + per] for i in range(0, len(sized), per))]
    H =24 + len(rows) * (ch + 12)
    body = f'<rect width="{W}" height="{H}" rx="14" fill="{INK}"/>'
    for r, (items, total) in enumerate(rows):
        x = (W - total) / 2
        y = 18 + r * (ch + 12)
        for i, (item, w) in enumerate(items):
            body += (f'<rect class="c" style="animation-delay:{(r * 6 + i) * .35:.2f}s" x="{x:.1f}" y="{y}" width="{w}" height="{ch}" rx="{ch / 2}" '
                     f'fill="{PANEL}" stroke="{LINE_DARK}"/>' + t(round(x + w / 2, 1), y + 24, item, M + f";font-size:{fs}px", STONE, "middle"))
            x += w + gap
    css = ".c{animation:hl 8.4s ease-in-out infinite}@keyframes hl{0%,8%,100%{stroke:rgba(252,247,243,.14)}4%{stroke:#ff6a3a}}"
    write("stack.svg", svg(W, H, body, css, (FONT_MONO,), "Stack: " + ", ".join(STACK)))


# ---------------------------------------------------------------- footer
def footer():
    W, H = 1280, 80
    s = M + ";font-size:12px;letter-spacing:2px"
    body = (f'<rect width="{W}" height="{H}" rx="12" fill="{INK}"/>'
            + t(40, 45, FOOTER[0], s, MUTE)
            + f'<circle cx="{W / 2 - 128}" cy="41" r="4" fill="{EMBER}"><animate attributeName="r" values="4;7;4" dur="2s" repeatCount="indefinite"/>'
              f'<animate attributeName="fill-opacity" values="1;.35;1" dur="2s" repeatCount="indefinite"/></circle>'
            + t(W / 2 + 10, 45, FOOTER[1], s, PAPER, "middle")
            + t(W - 40, 45, FOOTER[2], s, MUTE, "end"))
    write("footer.svg", svg(W, H, body, "", (FONT_MONO,), " · ".join(FOOTER)))


if __name__ == "__main__":
    for th in ("dark", "light"):
        hero(th)
        flow(th)
    typing()
    for k in UNITS:
        unit(k)
    for k in HEADERS:
        header(k)
    for k in BADGES:
        badge(k)
    stack()
    footer()
