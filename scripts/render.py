#!/usr/bin/env python3
"""Render the profile README artwork: banner (tonight's moon), Threat Harbour
card, and section phase icons. Standard library only; run daily by
.github/workflows/moon.yml.

    python3 scripts/render.py            # moon = now (UTC)
    python3 scripts/render.py --date 2026-11-24
"""
import argparse
import base64
import json
import math
import random
import urllib.request
from datetime import datetime, timedelta, timezone
from pathlib import Path
from xml.sax.saxutils import escape

ROOT = Path(__file__).resolve().parent.parent
ASSETS = ROOT / "assets"
METRICS_URL = ("https://raw.githubusercontent.com/aaadarsh1337/threat-harbour/"
               "main/analysis/metrics.json")

# Palette lifted from aaadarsh1337.github.io (night = default, dawn = light).
THEMES = {
    "night": dict(bg="#0b0e13", bg1="#0f1318", bg3="#1a2029", rule="#1d232c",
                  fg="#e1e5ea", fg2="#b6bec8", muted="#939eab", faint="#84909c",
                  bone="#eef0f3", moon="#ece8de", shade="#1f2225",
                  edge="#ece8de38", lily="#cf7c71", lantern="#d2b177",
                  tide="#8bb3ad", stem="#3a4a3c", glow="#ece8de", glow_a=0.10,
                  stars=True),
    "dawn": dict(bg="#edeff1", bg1="#e6e9ec", bg3="#d6dbe0", rule="#d3d8de",
                 fg="#141920", fg2="#39424d", muted="#535d69", faint="#626c78",
                 bone="#2a2f36", moon="#fffdf6", shade="#d3d9df",
                 edge="#14192040", lily="#a23f35", lantern="#6a4e12",
                 tide="#2f6660", stem="#8a9a86", glow="#e6c48c", glow_a=0.22,
                 stars=False),
}

# Same constants the portfolio uses for its live moon.
SYNODIC = 29.530588853
EPOCH_NEW = datetime(2000, 1, 6, 18, 14, tzinfo=timezone.utc)
FULL_MOON_NAMES = ["Wolf", "Snow", "Worm", "Pink", "Flower", "Strawberry",
                   "Buck", "Sturgeon", "Harvest", "Hunter's", "Beaver", "Cold"]


# --------------------------------------------------------------------- moon
def moon_state(when):
    age = ((when - EPOCH_NEW).total_seconds() / 86400) % SYNODIC
    theta = 2 * math.pi * age / SYNODIC
    lit = (1 - math.cos(theta)) / 2
    eighth = SYNODIC / 8
    names = ["new moon", "waxing crescent", "first quarter", "waxing gibbous",
             "full moon", "waning gibbous", "last quarter", "waning crescent"]
    name = names[int(((age + eighth / 2) % SYNODIC) // eighth)]
    to_full = (SYNODIC / 2 - age) % SYNODIC
    to_new = (SYNODIC - age) % SYNODIC
    full = when + timedelta(days=to_full)
    return dict(age=age, theta=theta, lit=lit, name=name, full=full,
                new=when + timedelta(days=to_new),
                full_name=FULL_MOON_NAMES[full.month - 1] + " Moon")


def lit_path(cx, cy, r, theta):
    """Path of the sunlit part of a disc, northern-hemisphere view."""
    k = math.cos(theta)
    rx = abs(k) * r
    top, bot = f"{cx:.2f} {cy - r:.2f}", f"{cx:.2f} {cy + r:.2f}"
    if theta < math.pi:      # waxing: lit limb on the right
        limb, term = 1, (0 if k > 0 else 1)
    else:                    # waning: lit limb on the left
        limb, term = 0, (1 if k > 0 else 0)
    return (f"M{top}A{r:.2f} {r:.2f} 0 0 {limb} {bot}"
            f"A{rx:.2f} {r:.2f} 0 0 {term} {top}Z")


def moon_svg(cx, cy, r, theta, t, uid, detail=True):
    """Moon disc: dark side, lit side, faint maria, rim."""
    out = [f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{t["shade"]}"/>']
    out.append(f'<clipPath id="lit{uid}"><path d="{lit_path(cx, cy, r, theta)}"/></clipPath>')
    out.append(f'<path d="{lit_path(cx, cy, r, theta)}" fill="{t["moon"]}"/>')
    if detail:
        # Maria, roughly where they sit on the near side.
        maria = [(-0.28, -0.30, 0.30, 0.22, 20), (0.18, -0.38, 0.22, 0.16, -15),
                 (0.30, 0.02, 0.20, 0.26, 10), (-0.12, 0.10, 0.18, 0.14, 0),
                 (-0.42, 0.18, 0.16, 0.24, 25), (0.05, 0.45, 0.14, 0.09, 0)]
        g = [f'<filter id="soft{uid}"><feGaussianBlur stdDeviation="{r * 0.05:.1f}"/></filter>',
             f'<g clip-path="url(#lit{uid})"><g filter="url(#soft{uid})" '
             f'fill="{t["shade"]}" opacity="0.10">']
        for dx, dy, rx, ry, rot in maria:
            g.append(f'<ellipse cx="{cx + dx * r:.1f}" cy="{cy + dy * r:.1f}" '
                     f'rx="{rx * r:.1f}" ry="{ry * r:.1f}" '
                     f'transform="rotate({rot} {cx + dx * r:.1f} {cy + dy * r:.1f})"/>')
        g.append("</g></g>")
        out += g
    out.append(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{t["edge"]}" stroke-width="1"/>')
    return "\n".join(out)


# -------------------------------------------------------------------- fonts
def font_css():
    def face(name, file):
        b64 = base64.b64encode((ASSETS / "fonts" / file).read_bytes()).decode()
        return (f"@font-face{{font-family:'{name}';"
                f"src:url(data:font/woff2;base64,{b64}) format('woff2')}}")
    return "".join([face("PSerif", "serif.woff2"), face("PMono", "mono.woff2"),
                    face("PMonoB", "mono-bold.woff2")])


SERIF = "font-family:'PSerif',Georgia,serif"
MONO = "font-family:'PMono',ui-monospace,Menlo,monospace"
MONOB = "font-family:'PMonoB',ui-monospace,Menlo,monospace"


# ------------------------------------------------------------------- lilies
def lily(cx, cy, s, t, rng, ground):
    """A red spider lily: an umbel of recurved petals and long stamens."""
    out = []
    sway = rng.uniform(-6, 6) * s
    out.append(f'<path d="M{cx:.1f} {cy:.1f}Q{cx + sway:.1f} {(cy + ground) / 2:.1f} '
               f'{cx + sway * 0.4:.1f} {ground:.1f}" stroke="{t["stem"]}" '
               f'stroke-width="{1.6 * s:.2f}" fill="none" stroke-linecap="round"/>')
    flowers = rng.randint(5, 7)
    for i in range(flowers):
        a = math.radians(-180 + (i + 0.5) * 180 / flowers + rng.uniform(-8, 8))
        fx = cx + math.cos(a) * 7 * s
        fy = cy + math.sin(a) * 5 * s
        # petals: short, curling back
        for p in range(4):
            pa = a + math.radians(rng.uniform(-50, 50))
            L = rng.uniform(7, 10) * s
            ex, ey = fx + math.cos(pa) * L, fy + math.sin(pa) * L
            qx = fx + math.cos(pa - 0.9) * L * 0.8
            qy = fy + math.sin(pa - 0.9) * L * 0.8 - 2 * s
            out.append(f'<path d="M{fx:.1f} {fy:.1f}Q{qx:.1f} {qy:.1f} {ex:.1f} {ey:.1f}" '
                       f'stroke="{t["lily"]}" stroke-width="{2.4 * s:.2f}" fill="none" '
                       f'stroke-linecap="round"/>')
        # stamens: long, sweeping up and out
        for _ in range(3):
            sa = a + math.radians(rng.uniform(-25, 25))
            L = rng.uniform(20, 27) * s
            ex = fx + math.cos(sa) * L
            ey = fy + math.sin(sa) * L * 0.85 - 6 * s
            qx = fx + math.cos(sa) * L * 0.55
            qy = fy + math.sin(sa) * L * 0.2
            out.append(f'<path d="M{fx:.1f} {fy:.1f}Q{qx:.1f} {qy:.1f} {ex:.1f} {ey:.1f}" '
                       f'stroke="{t["lily"]}" stroke-width="{0.8 * s:.2f}" fill="none" '
                       f'stroke-linecap="round" opacity="0.9"/>')
            out.append(f'<circle cx="{ex:.1f}" cy="{ey:.1f}" r="{1.1 * s:.2f}" fill="{t["lily"]}"/>')
    return "\n".join(out)


# ------------------------------------------------------------------- banner
def banner(theme, m):
    t = THEMES[theme]
    W, H = 1200, 400
    mx, my, mr = 945, 158, 94
    rng = random.Random(1337)   # fixed seed: stars and lilies never move
    tonight = f"Tonight · {m['name']} · {round(m['lit'] * 100)}% lit".upper()
    full = m["full"].strftime("%-d %b")
    nxt = (f"full tonight · the {m['full_name']}" if m["name"] == "full moon"
           else f"next full moon {full} · {m['full_name']}")

    s = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" '
         f'role="img" aria-label="Adarsh Pillai. Offensive security, reverse engineering, CTF. '
         f'{escape(tonight.capitalize())}.">',
         f"<style>{font_css()}"
         ".tw{animation:tw 4s ease-in-out infinite}"
         "@keyframes tw{0%,100%{opacity:var(--o)}50%{opacity:.08}}"
         "@media (prefers-reduced-motion:reduce){.tw{animation:none}}</style>",
         "<defs>",
         f'<linearGradient id="sky" x1="0" y1="0" x2="0" y2="1">'
         f'<stop offset="0" stop-color="{t["bg"]}"/><stop offset="1" stop-color="{t["bg1"]}"/></linearGradient>',
         f'<radialGradient id="halo"><stop offset="0" stop-color="{t["glow"]}" stop-opacity="{t["glow_a"]}"/>'
         f'<stop offset="1" stop-color="{t["glow"]}" stop-opacity="0"/></radialGradient>',
         f'<linearGradient id="mist" x1="0" y1="0" x2="0" y2="1">'
         f'<stop offset="0" stop-color="{t["bg1"]}" stop-opacity="0"/>'
         f'<stop offset="1" stop-color="{t["bg3"]}" stop-opacity="0.55"/></linearGradient>',
         f'<clipPath id="card"><rect width="{W}" height="{H}" rx="14"/></clipPath>',
         "</defs>",
         '<g clip-path="url(#card)">',
         f'<rect width="{W}" height="{H}" fill="url(#sky)"/>']

    if t["stars"]:
        for _ in range(90):
            x, y = rng.uniform(0, W), rng.uniform(0, H * 0.78)
            if (x - mx) ** 2 + (y - my) ** 2 < (mr + 30) ** 2:
                continue
            r = rng.choice([0.6, 0.7, 0.8, 0.9, 1.1, 1.4])
            o = rng.uniform(0.25, 0.7)
            cls = ' class="tw"' if rng.random() < 0.3 else ""
            delay = f"animation-delay:{rng.uniform(0, 4):.1f}s;" if cls else ""
            s.append(f'<circle{cls} cx="{x:.1f}" cy="{y:.1f}" r="{r}" fill="{t["moon"]}" '
                     f'opacity="{o:.2f}" style="--o:{o:.2f};{delay}"/>')

    s.append(f'<circle cx="{mx}" cy="{my}" r="{mr * 2.4}" fill="url(#halo)"/>')
    s.append(moon_svg(mx, my, mr, m["theta"], t, theme))

    # ground mist + lilies
    ground = H + 4
    s.append(f'<rect y="{H - 120}" width="{W}" height="120" fill="url(#mist)"/>')
    lr = random.Random(29)
    # (x, y, scale, opacity): smaller and fainter ones read as further away
    spots = [(598, 360, 0.7, 0.45), (690, 354, 0.8, 0.55), (1150, 356, 0.75, 0.5),
             (858, 362, 0.7, 0.45), (640, 370, 1.0, 0.85), (760, 350, 1.15, 0.9),
             (905, 348, 1.2, 0.95), (1030, 364, 1.05, 0.9), (1110, 372, 1.3, 1)]
    for x, y, sc, op in spots:
        s.append(f'<g opacity="{op}">{lily(x, y, sc, t, lr, ground)}</g>')

    # text
    x0 = 76
    s.append(f'<text x="{x0}" y="118" style="{MONO};font-size:16px;letter-spacing:2.4px" '
             f'fill="{t["lantern"]}">{escape(tonight)}</text>')
    s.append(f'<text x="{x0 - 3}" y="204" style="{SERIF};font-size:78px" '
             f'fill="{t["bone"]}">Adarsh Pillai</text>')
    s.append(f'<text x="{x0}" y="254" style="{MONO};font-size:20px" fill="{t["fg2"]}">'
             'Offensive security · Reverse engineering · CTF</text>')
    s.append(f'<rect x="{x0}" y="282" width="44" height="1.5" fill="{t["lily"]}"/>')
    s.append(f'<text x="{x0}" y="318" style="{MONO};font-size:16.5px" fill="{t["muted"]}">'
             'aaadarsh1337 · jackthereaper1337 · Hasher2009</text>')
    s.append(f'<text x="{mx}" y="{my + mr + 36}" text-anchor="middle" '
             f'style="{MONO};font-size:15px;letter-spacing:0.5px" fill="{t["faint"]}">'
             f'{escape(nxt)}</text>')
    s.append("</g>")
    s.append(f'<rect x="0.5" y="0.5" width="{W - 1}" height="{H - 1}" rx="14" fill="none" '
             f'stroke="{t["rule"]}"/>')
    s.append("</svg>")
    return "\n".join(s)


# ------------------------------------------------------------ harbour card
def harbour(theme, d):
    t = THEMES[theme]
    W, H = 1200, 350

    def n(v):
        return f"{int(v):,}"

    cutoff = datetime.strptime(d["analysis_cutoff_utc"], "%Y-%m-%dT%H:%M:%SZ")
    start = datetime.strptime(d["observation_period"]["start"], "%Y-%m-%d")
    live = f"LIVE SENSOR · DATA TO {cutoff.strftime('%-d %b %Y, %H:%M').upper()} UTC"
    stats = [(n(d["sources"]["unique_source_ips"]), "unique source IPs"),
             (n(d["sessions"]["unique_session_ids"]), "sessions"),
             (n(d["commands"]["input_events"]), "commands typed"),
             (n(d["downloads_uploads"]["file_download_events"]), "payload downloads")]
    days = sorted(d["collection"]["per_day_utc"].items())[-70:]

    s = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" '
         f'role="img" aria-label="Threat Harbour: {n(d["totals"]["total_events"])} SSH events '
         f'since {start.strftime("%-d %b %Y")}.">',
         f"<style>{font_css()}"
         ".p{animation:p 2.4s ease-out infinite;transform-origin:center;transform-box:fill-box}"
         "@keyframes p{0%{opacity:.7;transform:scale(1)}100%{opacity:0;transform:scale(3)}}"
         "@media (prefers-reduced-motion:reduce){.p{animation:none;opacity:0}}</style>",
         f'<rect x="0.5" y="0.5" width="{W - 1}" height="{H - 1}" rx="14" fill="{t["bg"]}" '
         f'stroke="{t["rule"]}"/>']
    x0 = 56
    s.append(f'<circle class="p" cx="{x0 + 5}" cy="54" r="5" fill="{t["tide"]}"/>')
    s.append(f'<circle cx="{x0 + 5}" cy="54" r="5" fill="{t["tide"]}"/>')
    s.append(f'<text x="{x0 + 20}" y="59.5" style="{MONO};font-size:15px;letter-spacing:1.6px" '
             f'fill="{t["tide"]}">{escape(live)}</text>')
    s.append(f'<text x="{x0 - 2}" y="134" style="{SERIF};font-size:68px" fill="{t["bone"]}">'
             f'{n(d["totals"]["total_events"])}</text>')
    s.append(f'<text x="{x0}" y="170" style="{MONO};font-size:17px" fill="{t["muted"]}">'
             f'SSH events since {start.strftime("%-d %b %Y")}</text>')

    # 2x2 stats on the right
    gx, gy, cw, rh = 640, 104, 270, 70
    for i, (val, label) in enumerate(stats):
        x, y = gx + (i % 2) * cw, gy + (i // 2) * rh
        s.append(f'<rect x="{x - 18}" y="{y - 26}" width="1.5" height="40" fill="{t["rule"]}"/>')
        s.append(f'<text x="{x}" y="{y}" style="{MONOB};font-size:26px" fill="{t["fg"]}">{val}</text>')
        s.append(f'<text x="{x}" y="{y + 23}" style="{MONO};font-size:15px" '
                 f'fill="{t["faint"]}">{label}</text>')

    # blades: events per day
    cx0, cx1, base, top = x0, W - 56, 300, 222
    peak = max(v for _, v in days) or 1
    step = (cx1 - cx0) / len(days)
    for i, (_, v) in enumerate(days):
        h = max(2, (v / peak) * (base - top))
        x = cx0 + i * step + step * 0.25
        last = i == len(days) - 1
        s.append(f'<rect x="{x:.1f}" y="{base - h:.1f}" width="{max(1.5, step * 0.5):.1f}" '
                 f'height="{h:.1f}" rx="1" fill="{t["lily"] if last else t["moon"] if theme == "night" else t["fg2"]}" '
                 f'opacity="{1 if last else 0.32}"/>')
    s.append(f'<rect x="{cx0}" y="{base + 1}" width="{cx1 - cx0}" height="1" fill="{t["rule"]}"/>')
    s.append(f'<text x="{cx0}" y="{base + 28}" style="{MONO};font-size:14px" fill="{t["faint"]}">'
             f'{datetime.strptime(days[0][0], "%Y-%m-%d").strftime("%-d %b")}</text>')
    s.append(f'<text x="{cx1}" y="{base + 28}" text-anchor="end" style="{MONO};font-size:14px" '
             f'fill="{t["faint"]}">events per day · {datetime.strptime(days[-1][0], "%Y-%m-%d").strftime("%-d %b")}</text>')
    s.append("</svg>")
    return "\n".join(s)


# --------------------------------------------------------------- phase icons
def phase_icon(lit_fraction, waning):
    """Small tile like the portfolio favicon: works on light and dark pages."""
    t = THEMES["night"]
    theta = math.acos(1 - 2 * lit_fraction)
    if waning:
        theta = 2 * math.pi - theta
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32" width="32" height="32">'
            f'<rect width="32" height="32" rx="7" fill="{t["bg"]}"/>'
            f'<circle cx="16" cy="16" r="9.5" fill="#1c2027"/>'
            f'<path d="{lit_path(16, 16, 9.5, theta)}" fill="{t["moon"]}"/></svg>\n')


# ---------------------------------------------------------------------- main
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--date", help="YYYY-MM-DD (UTC noon); default now")
    ap.add_argument("--metrics", help="local metrics.json instead of fetching")
    a = ap.parse_args()
    when = (datetime.strptime(a.date, "%Y-%m-%d").replace(hour=12, tzinfo=timezone.utc)
            if a.date else datetime.now(timezone.utc))
    m = moon_state(when)
    for theme in THEMES:
        (ASSETS / f"banner-{theme}.svg").write_text(banner(theme, m))

    for i, (frac, waning) in enumerate([(0.22, False), (0.5, False), (0.8, False),
                                        (1.0, False), (0.22, True)], 1):
        (ASSETS / f"phase-{i}.svg").write_text(phase_icon(frac, waning))

    try:
        if a.metrics:
            d = json.loads(Path(a.metrics).read_text())
        else:
            with urllib.request.urlopen(METRICS_URL, timeout=30) as r:
                d = json.load(r)
        for theme in THEMES:
            (ASSETS / f"harbour-{theme}.svg").write_text(harbour(theme, d))
    except Exception as e:  # keep yesterday's card rather than failing the run
        print(f"harbour card skipped: {e}")
    print(f"{when:%Y-%m-%d}: {m['name']}, {m['lit']:.0%} lit, age {m['age']:.1f}d")


if __name__ == "__main__":
    main()
