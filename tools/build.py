#!/usr/bin/env python3
"""Generator for the static site: `python3 tools/build.py` rewrites the HTML pages in the repo root.

Content (apps, texts, legal documents) lives in this file; styles and scripts live in assets/.
"""
import math, os, sys, html

ROOT = sys.argv[1] if len(sys.argv) > 1 else os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = "https://anton.antonchik.com"
UPDATED = "23 November 2026"
UPDATED_ISO = "2026-11-23"
KOFI = "https://ko-fi.com/K3K56CCST"
DEV_EMAIL = "support@antonchik.com"

# ---------------------------------------------------------------- icons
I = {
 "arrow": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 12h14M13 6l6 6-6 6"/></svg>',
 "ext": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M7 17 17 7M8 7h9v9"/></svg>',
 "mail": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="3" y="5" width="18" height="14" rx="3"/><path d="m4 7 8 6 8-6"/></svg>',
 "shield": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 3 5 6v6c0 4.2 3 7.6 7 9 4-1.4 7-4.8 7-9V6l-7-3Z"/><path d="m9 12 2 2 4-4"/></svg>',
 "doc": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M14 3H7a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2V8l-5-5Z"/><path d="M14 3v5h5M9 13h6M9 17h4"/></svg>',
 "life": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="12" cy="12" r="9"/><circle cx="12" cy="12" r="4"/><path d="m5.6 5.6 3.6 3.6M14.8 14.8l3.6 3.6M18.4 5.6l-3.6 3.6M9.2 14.8l-3.6 3.6"/></svg>',
 "navcalc": '<img src="/assets/apps/navcalc.webp" alt="NavCalc app icon" width="512" height="512" decoding="async">',
 "pilotiq": '<img src="/assets/apps/pilotiq.webp" alt="Pilotiq app icon" width="512" height="512" decoding="async">',
 "pkg": '<svg viewBox="0 0 32 32" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="m16 3.5 11 6v13l-11 6-11-6v-13l11-6Z" fill="currentColor" fill-opacity=".12"/><path d="m5 9.5 11 6 11-6M16 15.5v13"/></svg>',
 "apple": '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M16.37 12.6c-.02-2.3 1.88-3.4 1.96-3.46-1.07-1.56-2.73-1.78-3.32-1.8-1.41-.14-2.76.83-3.47.83-.72 0-1.82-.81-3-.79-1.54.02-2.96.9-3.76 2.27-1.6 2.78-.41 6.9 1.15 9.16.76 1.1 1.67 2.34 2.86 2.3 1.15-.05 1.58-.74 2.97-.74 1.38 0 1.77.74 2.98.72 1.23-.02 2.01-1.12 2.76-2.23.87-1.28 1.23-2.52 1.25-2.58-.03-.01-2.4-.92-2.42-3.66l.04-.02ZM14.1 5.86c.63-.77 1.06-1.83.94-2.9-.91.04-2.01.61-2.66 1.37-.58.67-1.1 1.76-.96 2.8 1.02.08 2.05-.52 2.68-1.27Z"/></svg>',
 "play": '<svg viewBox="0 0 24 24" fill="none" aria-hidden="true"><path d="M4.2 2.9 13.5 12l-9.3 9.1c-.3-.2-.5-.6-.5-1.1V4c0-.5.2-.9.5-1.1Z" fill="#5cf0a6"/><path d="m16.6 8.9-3.1 3.1-9.3-9.1c.3-.2.8-.2 1.3.1l11.1 5.9Z" fill="#9fd8ff"/><path d="M16.6 15.1 5.5 21c-.5.3-1 .3-1.3.1l9.3-9.1 3.1 3.1Z" fill="#ff8fa3"/><path d="m20.3 10.9-3.7-2-3.1 3.1 3.1 3.1 3.7-2c1-.6 1-1.6 0-2.2Z" fill="#ffc27a"/></svg>',
 "huawei": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="4" y="6" width="16" height="14" rx="3"/><path d="M8.5 6a3.5 3.5 0 0 1 7 0M9 11c0 1.7 1.3 3 3 3s3-1.3 3-3"/></svg>',
 "mark": '<svg viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg" aria-hidden="true"><defs><linearGradient id="lgF" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#a3b7ea"/><stop offset="1" stop-color="#5f7cc6"/></linearGradient></defs><path d="M31.7 85.6A38.3 38.3 0 1 1 68.3 85.6L60.6 62.5H39.4Z" fill="url(#lgF)"/><path d="M50 27.5 57 59H43Z" fill="#ffcf33"/><g fill="none" stroke="#0a3492" stroke-width="7" stroke-linecap="round" stroke-linejoin="round"><path d="M31.7 85.6A38.3 38.3 0 1 1 68.3 85.6"/><path d="M31.7 85.6 50 13.7 68.3 85.6M39.4 62.5H60.6"/></g></svg>',
}

# ---------------------------------------------------------------- data
APPS = {
 "navcalc": dict(
   name="NavCalc", slug="navcalc", page="/navcalcapp_support/", tint="t-navcalc",
   tagline="The flight navigation computer, rebuilt for your pocket.",
   short="A precise navigation calculator for pilots and aviation students — unit conversions, geodesy, wind triangles, ISA and a complete aviation reference in one calm interface.",
   category="Aviation · Utilities", email="navcalc@antonchik.com",
   platforms="iOS · AppGallery",
   stores=[("apple","Download on the","App Store","https://apps.apple.com/app/navcalc/id1586660769"),
           ("huawei","Explore it on","AppGallery","https://appgallery.cloud.huawei.com/ag/n/app/C104806419")],
   features=[
     ("Unit conversions","Distance, height, speed, time, pressure, temperature and more — switch between unit systems instantly, without ambiguity."),
     ("Geodesy","Direct and inverse geodetic problems, magnetic variation for any location, intersection of two radials and distance to the horizon."),
     ("Flight tasks","Wind triangle, crosswind and headwind components, holding pattern entries and parameters of turn."),
     ("Atmosphere","ISA values at altitude, TAS from IAS, QFE ⇄ QNH conversion and cold-temperature altimeter corrections."),
     ("Reference","Aircraft, airline and airport data, the phonetic alphabet with Morse code and a large handbook of aviation abbreviations."),
     ("AIRAC calendar","Always know when the next AIRAC cycle becomes effective — and the dates of the ones after it."),
   ],
   faq=[
     ("Are the calculations suitable for real flight planning?","NavCalc is built carefully against published standards (including ICAO Doc 7488 for the atmosphere model), but it is a training and reference aid. Always verify results against approved sources and your aircraft documentation."),
     ("Which standards does NavCalc use?","All common aviation units are supported. Atmosphere calculations follow the ICAO Standard Atmosphere (Doc 7488)."),
     ("I found a wrong value or a missing abbreviation.","Thank you — please email the details (what you entered, what you expected, and your app version) and it will be corrected in a future update."),
   ],
   legal=[("Privacy Policy","/privacy/navcalc/")],
 ),
 "pilotiq": dict(
   name="Pilotiq", slug="pilotiq", page="/pilotiq_support/", tint="t-pilotiq",
   tagline="Your copilot for the ULC theory exam.",
   short="Exam preparation for Polish pilot licence theory exams at ULC — PPL(A), PPL(H), PL(G) and PL(FB). Hundreds of questions across every subject, with PPL(A) and PPL(H) also available in English.",
   category="Education · Aviation", email="pilotiq@antonchik.com",
   platforms="iOS · Android",
   stores=[("apple","Download on the","App Store","https://apps.apple.com/app/pilotiq/id6446788760"),
           ("play","Get it on","Google Play","https://play.google.com/store/apps/details?id=antonchik.anton.pilotiq")],
   features=[
     ("Four licences","Aeroplane PPL(A), helicopter PPL(H), glider PL(G) and balloon PL(FB) — each with its own question bank."),
     ("Exam tests","Hundreds of exam-style questions in air law, communications, meteorology, navigation, flight planning, aircraft general knowledge and more."),
     ("Detailed results","After each test you see every answer you gave, so you know exactly where to focus next."),
     ("Up-to-date database","Questions follow the current ULC requirements and reflect examinations held in Poland."),
     ("Subscription","Unlock the full question bank with an auto-renewing subscription — cancel any time in your store account."),
     ("Polish &amp; English","All exams in Polish; PPL(A) and PPL(H) are also available in English."),
   ],
   faq=[
     ("How do I cancel my subscription?","Subscriptions are managed by the store. On iPhone: Settings → your name → Subscriptions → Pilotiq → Cancel. On Android: Google Play → Profile → Payments &amp; subscriptions → Subscriptions → Pilotiq → Cancel. Cancel at least 24 hours before the renewal date to avoid the next charge."),
     ("How do I restore my purchase on a new device?","Sign in with the same Apple ID or Google account you used to subscribe, open Pilotiq and use “Restore purchases”. If it does not work, email support with the date of purchase."),
     ("Can I get a refund?","Payments are processed by Apple or Google, so refunds are handled by them: request one at reportaproblem.apple.com or through your Google Play order history."),
     ("I think an answer in the question bank is wrong.","Please email the question text and the answer you believe is correct — every report is reviewed."),
   ],
   legal=[("Terms of Service","/terms/pilotiq/"),("Privacy Policy","/privacy/pilotiq/")],
 ),
}
ORDER = ["navcalc","pilotiq"]

PKGS = [
 ("isa","International Standard Atmosphere for Dart &amp; Flutter. Physical characteristics of a standard or customised atmosphere at any altitude up to 80 km, according to ICAO Doc 7488.","https://pub.dev/packages/isa"),
 ("measures","Type-safe units of measure. Comfortable handling of everyday units, seamless conversions and code that is unambiguous about what a number means.","https://pub.dev/packages/measures"),
]

# ---------------------------------------------------------------- chrome
FONTS = '<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin><link href="https://fonts.googleapis.com/css2?family=Geist:wght@300..700&family=Geist+Mono:wght@400;500&family=Instrument+Serif:ital@0;1&display=swap" rel="stylesheet">'

def head(title, desc, path, body_cls=""):
    url = SITE + path
    return f'''<!DOCTYPE html>
<html lang="en" class="no-js">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{html.escape(title)}</title>
<meta name="description" content="{html.escape(desc)}">
<link rel="canonical" href="{url}">
<meta name="theme-color" content="#f6f7fb">
<meta property="og:type" content="website">
<meta property="og:title" content="{html.escape(title)}">
<meta property="og:description" content="{html.escape(desc)}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{SITE}/assets/og.png">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="/favicon.ico" sizes="48x48">
<link rel="icon" href="/assets/logo.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<link rel="manifest" href="/site.webmanifest">
{FONTS}
<link rel="stylesheet" href="/assets/site.css">
<script defer src="/assets/site.js"></script>
</head>
<body class="{body_cls}">
<div class="ambient" aria-hidden="true"></div>
<header class="nav">
  <div class="nav__inner">
    <a class="brand" href="/" aria-label="Anton Antonchik — home"><span class="brand__mark">{I["mark"]}</span><span>Anton Antonchik</span></a>
    <nav class="nav__links" aria-label="Primary">
      <a href="/#apps">Apps</a><a href="/#open-source">Open source</a><a href="/support/">Support</a><a href="/legal/">Legal</a>
    </nav>
    <a class="btn btn--sm btn--primary" href="mailto:{DEV_EMAIL}">Contact</a>
  </div>
</header>
<main>
'''

def foot():
    apps = "".join(f'<li><a href="{APPS[k]["page"]}">{APPS[k]["name"]}</a></li>' for k in ORDER)
    return f'''</main>
<footer class="footer">
  <div class="wrap">
    <div class="footer__grid">
      <div>
        <a class="brand" href="/"><span class="brand__mark">{I["mark"]}</span><span>Anton Antonchik</span></a>
        <p class="muted" style="max-width:34ch;margin:18px 0 0;font-size:14.5px">Independent developer of mobile apps and open-source Dart packages. Built with care, supported personally.</p>
      </div>
      <div><h4>Apps</h4><ul>{apps}</ul></div>
      <div><h4>Help</h4><ul><li><a href="/support/">Support</a></li><li><a href="mailto:{DEV_EMAIL}">{DEV_EMAIL}</a></li><li><a href="{KOFI}" target="_blank" rel="noopener">Support my work</a></li></ul></div>
      <div><h4>Legal</h4><ul><li><a href="/legal/">All documents</a></li><li><a href="/privacy/navcalc/">Privacy · NavCalc</a></li><li><a href="/privacy/pilotiq/">Privacy · Pilotiq</a></li><li><a href="/terms/pilotiq/">Terms · Pilotiq</a></li></ul></div>
    </div>
    <div class="footer__big" aria-hidden="true">Antonchik</div>
    <div class="footer__bottom">
      <span>© <span data-year>2026</span> Anton Antonchik · <a href="https://antonchik.com">antonchik.com</a></span>
      <span class="status"><i></i>All systems normal</span>
    </div>
  </div>
</footer>
</body>
</html>
'''

def write(path, content):
    p = os.path.join(ROOT, path.strip("/")) if path.endswith(".html") else os.path.join(ROOT, path.strip("/"), "index.html")
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, "w") as f: f.write(content)

def stores_html(app):
    out = []
    for icon, small, big, href in app["stores"]:
        out.append(f'<a class="store" href="{href}" target="_blank" rel="noopener">{I[icon]}<span><small>{small}</small><strong>{big}</strong></span></a>')
    return '<div class="stores">' + "".join(out) + '</div>' if out else ""

def chips(app, overview=True, support=True):
    s = f'<a class="link-chip link-chip--accent" href="{app["page"]}">Overview {I["arrow"]}</a>' if overview else ""
    if support: s += f'<a class="link-chip" href="{app["page"]}#support">{I["life"]}Support</a>'
    for t, h in app["legal"]:
        s += f'<a class="link-chip" href="{h}">{I["shield"] if "Privacy" in t else I["doc"]}{t}</a>'
    return s

# ---------------------------------------------------------------- instrument
def instrument():
    """Interactive wind triangle (north-up plotting disc). Vectors are drawn by assets/live.js."""
    C, R = 230, 196
    MONO = 'font-family="Geist Mono, monospace"'
    g = []
    for d in range(0, 360, 5):
        l = 14 if d % 30 == 0 else (8 if d % 10 == 0 else 4)
        a = math.radians(d)
        x1, y1 = C + R*math.sin(a), C - R*math.cos(a)
        x2, y2 = C + (R-l)*math.sin(a), C - (R-l)*math.cos(a)
        op = ".5" if d % 30 == 0 else ".22"
        g.append(f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="#0a3492" stroke-opacity="{op}"/>')
    for d in range(0, 360, 30):
        a = math.radians(d)
        x, y = C + (R+16)*math.sin(a), C - (R+16)*math.cos(a)
        t = {0: "N", 90: "E", 180: "S", 270: "W"}.get(d, f"{d//10:02d}")
        col, op = ("#dc1038", "1") if d == 0 else ("#0a3492", "1" if d % 90 == 0 else ".5")
        g.append(f'<text x="{x:.1f}" y="{y:.1f}" fill="{col}" fill-opacity="{op}" {MONO} font-size="{14 if d % 90 == 0 else 12}" text-anchor="middle" dominant-baseline="central">{t}</text>')
    plane = "M0 -20C1.9 -20 2.6 -17 2.6 -14L2.6 -5L18 3L18 6.5L2.6 2.5L2.4 11L7 14.5L7 17L0 15.5L-7 17L-7 14.5L-2.4 11L-2.6 2.5L-18 6.5L-18 3L-2.6 -5L-2.6 -14C-2.6 -17 -1.9 -20 0 -20Z"
    cell = lambda cid, lab, out=False: f'<div class="wt__cell{" wt__cell--out" if out else ""}"><small id="{cid}-l">{lab}</small><b id="{cid}">—</b></div>'
    return f'''<div class="card wt rise" data-d="3" id="wt">
  <div class="wt__head"><span class="eyebrow"><span class="dot"></span>Live · Wind triangle</span><span class="wt__tas js-only" id="wt-tas" role="group" aria-label="True airspeed, knots"><span>TAS</span><button type="button" data-tas="120" aria-pressed="false">120</button><button type="button" data-tas="250" class="is-on" aria-pressed="true">250</button><button type="button" data-tas="450" aria-pressed="false">450</button><span>kt</span></span></div>
  <svg class="wt__svg" id="wt-svg" viewBox="-8 -8 476 476" role="group" aria-label="Interactive wind triangle: drag the heading marker on the ring or the tip of the wind arrow">
    <defs><clipPath id="wt-clip"><circle cx="230" cy="230" r="178"/></clipPath></defs>
    <circle cx="230" cy="230" r="196" fill="none" stroke="#0a3492" stroke-opacity=".14"/>
    {"".join(g)}
    <circle cx="230" cy="230" r="70" fill="none" stroke="#0a3492" stroke-opacity=".1" stroke-dasharray="2 6"/>
    <circle cx="230" cy="230" r="140" fill="none" stroke="#0a3492" stroke-opacity=".1" stroke-dasharray="2 6"/>
    <text id="wt-r1" x="235" y="156" fill="#7c859b" {MONO} font-size="10">125</text><text id="wt-r2" x="235" y="86" fill="#7c859b" {MONO} font-size="10">250 kt</text>
    <path d="M230 52v356M52 230h356" stroke="#0a3492" stroke-opacity=".05"/>
    <g clip-path="url(#wt-clip)"><g id="wt-streaks"></g></g>
    <g id="wt-dyn"></g>
    <g id="wt-plane" transform="translate(230 230) rotate(34) scale(.8)"><path d="{plane}" fill="#0a3492" stroke="#fff" stroke-width="1.4" stroke-linejoin="round"/></g>
    <g class="wt__h js-only" id="wt-hA" tabindex="0" role="slider" aria-label="Heading, degrees" aria-valuemin="1" aria-valuemax="360" aria-valuenow="34"><circle r="24" fill="transparent"/><circle class="wt__pulse" r="11" fill="none" stroke="#0a3492"/><circle r="9" fill="#0a3492" stroke="#fff" stroke-width="2"/><circle r="2.6" fill="#fff"/></g>
    <g class="wt__h js-only" id="wt-hG" tabindex="0" role="slider" aria-label="Wind: left and right change direction, up and down change speed" aria-valuemin="0" aria-valuemax="100" aria-valuenow="70"><circle r="26" fill="transparent"/><circle class="wt__pulse" r="15" fill="none" stroke="#7890c8"/><circle r="15" fill="#7890c8" fill-opacity=".16" stroke="#7890c8" stroke-width="1.4"/></g>
  </svg>
  <div class="wt__grid js-only" aria-live="off">
    {cell("wt-hdg","Heading")}{cell("wt-wind","Wind")}{cell("wt-hw","Headwind")}
    {cell("wt-trk","Track",True)}{cell("wt-gs","Groundspeed",True)}{cell("wt-drift","Drift",True)}
  </div>
  <p class="wt__hint js-only">Drag the <b>heading</b> marker or the tip of the <b>wind</b> arrow — the triangle is solved live.</p>
</div>'''

DEMOS = {
 "navcalc": '''<div class="demo js-only" id="cv">
          <div class="demo__bar"><span>NavCalc</span><small>Converter · live preview</small></div>
          <div class="demo__body">
            <div class="demo__tabs" id="cv-tabs" role="tablist" aria-label="Quantity"></div>
            <div id="cv-rows" class="cv-rows"></div>
            <p class="demo__note">Type in any field — the others follow.</p>
          </div>
        </div>''',
 "pilotiq": '''<div class="demo js-only" id="qz-box">
          <div class="demo__bar"><span>Exam simulator</span><small id="qz-n">Sample · 1/3</small></div>
          <div class="demo__body" id="qz"></div>
        </div>''',
}

LIVE = {
 "isa": '''<div class="live js-only">
          <div class="live__top"><span>Altitude</span><b id="isa-alt">—</b></div>
          <input class="rng" id="isa-h" type="range" min="0" max="20000" step="100" value="3000" aria-label="Altitude in metres">
          <div class="live__cells live__cells--4">
            <div class="live__cell"><small>Temperature</small><b id="isa-t">—</b></div>
            <div class="live__cell"><small>Pressure</small><b id="isa-p">—</b></div>
            <div class="live__cell"><small>Density</small><b id="isa-rho">—</b></div>
            <div class="live__cell"><small>Sound speed</small><b id="isa-a">—</b></div>
          </div>
          <div class="live__foot" id="isa-layer">—</div>
        </div>''',
 "measures": '''<div class="live js-only">
          <div class="live__top"><span>Pressure (QNH)</span><b id="ms-v">—</b></div>
          <input class="rng" id="ms-h" type="range" min="950" max="1050" step="1" value="1013" aria-label="Pressure in hectopascals">
          <div class="live__cells live__cells--3">
            <div class="live__cell"><small>inHg</small><b id="ms-inhg">—</b></div>
            <div class="live__cell"><small>mmHg</small><b id="ms-mmhg">—</b></div>
            <div class="live__cell"><small>psi</small><b id="ms-psi">—</b></div>
          </div>
          <div class="live__foot">One value, every unit — no ambiguity about what a number means.</div>
        </div>''',
}

# ---------------------------------------------------------------- pages
def page_index():
    desc = "Anton Antonchik — independent developer of NavCalc and Pilotiq, and open-source Dart packages. App support, privacy policies and terms."
    s = head("Anton Antonchik — Independent App Developer", desc, "/")
    s += f'''<section class="hero">
  <div class="grid-bg" aria-hidden="true"></div>
  <div class="wrap">
    <div class="hero__grid">
      <div>
        <span class="eyebrow rise"><span class="dot"></span>Aviation engineer · Independent developer · Flutter</span>
        <h1 class="rise" data-d="1">Precise software<br>for <span class="serif grad">people who&nbsp;fly.</span></h1>
        <p class="lead rise" data-d="2">I design and build focused mobile apps and open-source Dart packages — for pilots, students and anyone who values calm, accurate tools that simply work.</p>
        <div class="hero__cta rise" data-d="3">
          <a class="btn btn--primary" href="#apps">Explore apps {I["arrow"]}</a>
          <a class="btn" href="/support/">Get support</a>
        </div>
      </div>
      {instrument()}
    </div>
    <div class="stats reveal">
      <div class="stat"><div class="stat__v">2</div><div class="stat__l">Mobile apps</div></div>
      <div class="stat"><div class="stat__v">2</div><div class="stat__l">Packages on pub.dev</div></div>
      <div class="stat"><div class="stat__v">4</div><div class="stat__l">Exams in Pilotiq</div></div>
      <div class="stat"><div class="stat__v">1:1</div><div class="stat__l">Personal support</div></div>
    </div>
  </div>
</section>

<section class="section" id="apps">
  <div class="wrap">
    <div class="section-head">
      <span class="eyebrow reveal"><span class="idx">01</span> / Apps</span>
      <h2 class="reveal">Tools that earn their place on your <span class="serif">home screen.</span></h2>
      <p class="lead reveal" data-d="1">Every app is small on purpose: one job, done precisely, with no clutter. Try a live preview of each right here.</p>
    </div>
    <div class="bento">
'''
    for i, k in enumerate(ORDER):
        a = APPS[k]
        feats = "".join(f'<li><span class="n">{j+1:02d}</span><span><b>{t}</b>{d}</span></li>' for j,(t,d) in enumerate(a["features"][:4]))
        st = stores_html(a) or f'<div class="meta-row" style="margin:0"><span class="tag"><i></i>Available on {a["platforms"]}</span></div>'
        s += f'''      <article class="card app app--hero {a["tint"]} reveal">
        <div style="display:flex;flex-direction:column;gap:22px">
          <div class="app__top"><div class="app-icon">{I[k]}</div><div><div class="app__name">{a["name"]}</div><div class="tags"><span class="tag"><i></i>{a["category"].replace("&","&amp;")}</span><span class="tag">{a["platforms"]}</span></div></div></div>
          <p class="app__desc" style="font-size:17px">{a["short"]}</p>
          {st}
          <div class="app__links">{chips(a)}</div>
        </div>
        <div class="app__demo">{DEMOS[k]}<ul class="feature-list nojs-only">{feats}</ul></div>
      </article>
'''
    s += '''    </div>
  </div>
</section>

<section class="section" id="open-source">
  <div class="wrap">
    <div class="section-head">
      <span class="eyebrow reveal"><span class="idx">02</span> / Open source</span>
      <h2 class="reveal">The maths behind the apps, <span class="serif">shared.</span></h2>
      <p class="lead reveal" data-d="1">The engineering core of my aviation apps is published as open-source packages for the Dart &amp; Flutter community. Move the sliders — this is the same maths.</p>
    </div>
    <div class="pkgs">
'''
    for i,(n,d,u) in enumerate(PKGS):
        s += f'''      <article class="card pkg reveal" data-d="{i}">
        <div class="pkg__head"><div class="app__top"><div class="app-icon t-oss">{I["pkg"]}</div><span class="pkg__name">{n}</span></div><a class="link-chip" href="{u}" target="_blank" rel="noopener">pub.dev {I["ext"]}</a></div>
        <p>{d}</p>
        {LIVE[n]}
        <div class="term"><code><span class="p">$</span>flutter pub add {n}</code><button class="copy" type="button" data-copy="flutter pub add {n}">Copy</button></div>
      </article>
'''
    s += f'''    </div>
  </div>
</section>

<section class="section" id="support">
  <div class="wrap">
    <div class="section-head">
      <span class="eyebrow reveal"><span class="idx">03</span> / Support</span>
      <h2 class="reveal">A real person <span class="serif">on the other end.</span></h2>
      <p class="lead reveal" data-d="1">Questions, bug reports, feature ideas — write directly. Every message is read and answered personally.</p>
    </div>
    {support_cards()}
    <div style="margin-top:28px" class="reveal"><a class="btn" href="/support/">Support centre &amp; FAQ {I["arrow"]}</a></div>
  </div>
</section>

<section class="section" id="legal">
  <div class="wrap">
    <div class="section-head">
      <span class="eyebrow reveal"><span class="idx">04</span> / Legal</span>
      <h2 class="reveal">Transparent by <span class="serif">default.</span></h2>
      <p class="lead reveal" data-d="1">Privacy policies and terms for every app, written in plain language.</p>
    </div>
    {docs_table()}
  </div>
</section>

<script defer src="/assets/live.js"></script>
<section class="wrap">
  <div class="card band reveal">
    <div class="grid-lines" aria-hidden="true"></div><div class="band__glow" aria-hidden="true"></div>
    <span class="eyebrow"><span class="dot"></span>Open for ideas</span>
    <h2>Have an idea for the next <span class="serif grad">great tool?</span></h2>
    <p class="lead">Feature requests from real users shape every release. If something would make your flying — or your day — easier, I would love to hear about it.</p>
    <div class="hero__cta"><a class="btn btn--primary" href="mailto:{DEV_EMAIL}">{I["mail"]} Write to me</a><a class="btn" href="{KOFI}" target="_blank" rel="noopener">Support my work</a></div>
  </div>
</section>
'''
    s += foot()
    write("/", s)

def support_cards():
    out = '<div class="support-grid">'
    for i,k in enumerate(ORDER):
        a = APPS[k]
        out += f'''<div class="card contact {a["tint"]} reveal" data-d="{i}">
  <div class="app__top"><div class="app-icon">{I[k]}</div><h3>{a["name"]}</h3></div>
  <div class="mail">{a["email"]}</div>
  <a class="btn btn--sm" href="mailto:{a["email"]}?subject={a["name"]}%20support">{I["mail"]} Email support</a>
</div>'''
    out += f'''<div class="card contact t-oss reveal" data-d="2">
  <div class="app__top"><div class="app-icon">{I["mail"]}</div><h3>General</h3></div>
  <div class="mail">{DEV_EMAIL}</div>
  <a class="btn btn--sm" href="mailto:{DEV_EMAIL}">{I["mail"]} Get in touch</a>
</div>'''
    return out + '</div>'

DOCS = [
  ("Privacy Policy","NavCalc","/privacy/navcalc/"),
  ("Privacy Policy","Pilotiq","/privacy/pilotiq/"),
  ("Terms of Service","Pilotiq","/terms/pilotiq/"),
]
def docs_table():
    out = '<div class="docs reveal">'
    for t,a,h in DOCS:
        out += f'<a class="doc" href="{h}"><span class="doc__t">{t}</span><span class="doc__m">{a}</span><span class="doc__m">Updated {UPDATED}</span><span class="doc__arrow">{I["arrow"]}</span></a>'
    return out + '</div>'

GENERAL_FAQ = [
 ("How do I report a bug?","Email the support address of the app with a short description, the steps to reproduce it, your device model, OS version and app version. Screenshots help a lot."),
 ("How do I manage or cancel a subscription?","Subscriptions are billed by Apple or Google. iPhone/iPad: Settings → your name → Subscriptions. Android: Google Play → Profile → Payments &amp; subscriptions → Subscriptions. Cancel at least 24 hours before renewal to avoid the next charge."),
 ("How do I restore a purchase?","Make sure you are signed in with the same Apple ID or Google account used for the purchase, then use “Restore purchases” inside the app."),
 ("How do I request a refund?","Refunds are processed by the store: <a href=\"https://reportaproblem.apple.com\" target=\"_blank\" rel=\"noopener\">reportaproblem.apple.com</a> for the App Store, or your order history in Google Play."),
 ("How do I delete my data?","The apps do not require an account and keep your data on your device. Deleting the app removes it. To delete any correspondence you have sent to support, email the app’s support address with the subject “Data deletion” — it will be removed within 30 days."),
 ("How quickly will I get an answer?","Usually within a few business days. Messages are answered in English, Polish or Russian."),
]

def faq_html(items, title="Frequently asked"):
    q = "".join(f'<details><summary>{a}</summary><div class="ans"><p>{b}</p></div></details>' for a,b in items)
    return f'<div class="faq reveal"><div><span class="eyebrow">FAQ</span><h3 style="margin-top:14px">{title}</h3></div><div>{q}</div></div>'

def simple_hero(crumb, eyebrow, h1, lead):
    return f'''<section class="page-hero">
  <div class="grid-bg" aria-hidden="true"></div>
  <div class="wrap">
    <div class="crumbs rise"><a href="/">Home</a><span>/</span><span>{crumb}</span></div>
    <div class="app-hero"><div>
      <span class="eyebrow rise" data-d="1"><span class="dot"></span>{eyebrow}</span>
      <h1 class="rise" data-d="1">{h1}</h1>
      <p class="lead rise" data-d="2">{lead}</p>
    </div></div>
  </div>
</section>
'''

def page_support():
    s = head("Support — Anton Antonchik", "Get help with NavCalc and Pilotiq: contact support, manage subscriptions, restore purchases and delete your data.", "/support/")
    s += simple_hero("Support", "Support centre", 'How can I <span class="serif grad">help?</span>', "Choose your app below to reach its support inbox directly. Most questions about purchases and data are answered in the FAQ.")
    s += f'<section class="section" style="padding-top:64px"><div class="wrap">{support_cards()}{faq_html(GENERAL_FAQ)}</div></section>\n'
    s += foot()
    write("/support/", s)

def page_legal():
    s = head("Legal — Anton Antonchik", "Privacy policies and terms of service for NavCalc and Pilotiq.", "/legal/")
    s += simple_hero("Legal", "Documents", 'Legal &amp; <span class="serif grad">privacy.</span>', "Everything you need to know about how the apps work with your data, and the terms that apply to them.")
    s += f'<section class="section" style="padding-top:64px"><div class="wrap">{docs_table()}</div></section>\n'
    s += foot()
    write("/legal/", s)

def page_app(k):
    a = APPS[k]
    s = head(f'{a["name"]} — {a["tagline"]}', a["short"], a["page"], a["tint"])
    feats = "".join(f'<article class="card feature reveal" data-d="{i%3}"><span class="n">{i+1:02d}</span><h3>{t}</h3><p>{d}</p></article>' for i,(t,d) in enumerate(a["features"]))
    stores = stores_html(a) or f'<div class="meta-row"><span class="tag"><i></i>Available on {a["platforms"]}</span></div>'
    legal_dd = " · ".join(f'<a href="{h}">{t}</a>' for t,h in a["legal"])
    cat = a["category"].replace("&","&amp;")
    s += f'''<section class="page-hero">
  <div class="grid-bg" aria-hidden="true"></div>
  <div class="wrap">
    <div class="crumbs rise"><a href="/">Home</a><span>/</span><a href="/#apps">Apps</a><span>/</span><span>{a["name"]}</span></div>
    <div class="app-hero">
      <div>
        <div class="app-icon app-icon--lg rise" data-d="1">{I[k]}</div>
        <h1 class="rise" data-d="1">{a["name"]}</h1>
        <p class="lead rise" data-d="2" style="font-size:clamp(19px,2vw,23px);color:var(--text);margin:0 0 12px">{a["tagline"]}</p>
        <p class="lead rise" data-d="2" style="margin:0">{a["short"]}</p>
        <div class="rise" data-d="3" style="margin-top:30px">{stores}</div>
      </div>
      <div class="card spec rise" data-d="4">
        <dl>
          <dt>Category</dt><dd>{cat}</dd>
          <dt>Platforms</dt><dd>{a["platforms"]}</dd>
          <dt>Developer</dt><dd>Anton Antonchik</dd>
          <dt>Support</dt><dd><a href="mailto:{a["email"]}">{a["email"]}</a></dd>
          <dt>Legal</dt><dd>{legal_dd}</dd>
        </dl>
      </div>
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="section-head">
      <span class="eyebrow reveal"><span class="idx">01</span> / Features</span>
      <h2 class="reveal">Everything you need. <span class="serif">Nothing you don’t.</span></h2>
    </div>
    <div class="features">{feats}</div>
  </div>
</section>

<section class="section" id="support">
  <div class="wrap">
    <div class="section-head">
      <span class="eyebrow reveal"><span class="idx">02</span> / Support</span>
      <h2 class="reveal">Need a hand with <span class="serif">{a["name"]}?</span></h2>
      <p class="lead reveal" data-d="1">Write to the support inbox below — include your device, OS and app version if you are reporting a problem.</p>
    </div>
    <div class="split">
      <div class="card panel reveal">
        <span class="eyebrow">Email support</span>
        <div class="mail-big">{a["email"]}</div>
        <p>Answered personally, usually within a few business days.</p>
        <div><a class="btn btn--primary" href="mailto:{a["email"]}?subject={a["name"]}%20support">Write to support {I["arrow"]}</a></div>
      </div>
      <div class="card panel reveal" data-d="1">
        <span class="eyebrow">Documents</span>
        <h3>Privacy &amp; terms</h3>
        <p>How {a["name"]} handles your data and the conditions that apply to its use.</p>
        <div class="app__links">{chips(a, overview=False, support=False)}</div>
      </div>
    </div>
    {faq_html(a["faq"] + GENERAL_FAQ[:1], "Questions about " + a["name"])}
  </div>
</section>

<section class="wrap">
  <div class="card band {a["tint"]} reveal">
    <div class="grid-lines" aria-hidden="true"></div><div class="band__glow" aria-hidden="true"></div>
    <span class="eyebrow"><span class="dot"></span>Enjoying {a["name"]}?</span>
    <h2>A short review helps <span class="serif grad">more than you think.</span></h2>
    <p class="lead">Ratings in the App Store and Google Play help other people discover the app — and keep an independent developer going.</p>
    <div class="hero__cta"><a class="btn btn--primary" href="{KOFI}" target="_blank" rel="noopener">Support my work {I["arrow"]}</a><a class="btn" href="/#apps">Other apps</a></div>
  </div>
</section>
'''
    s += foot()
    write(a["page"], s)

# ---------------------------------------------------------------- legal docs
def legal_page(path, title, app, sections, intro, body_cls):
    toc = "".join(f'<li><a href="#s{i+1}">{t}</a></li>' for i,(t,_) in enumerate(sections))
    body = "".join(f'<h2 id="s{i+1}"><span class="n">{i+1:02d}</span>{t}</h2>{c}' for i,(t,c) in enumerate(sections))
    s = head(f"{title} — {app}", f"{title} for the {app} mobile application by Anton Antonchik.", path, body_cls)
    s += f'''<section class="page-hero">
  <div class="grid-bg" aria-hidden="true"></div>
  <div class="wrap">
    <div class="crumbs rise"><a href="/">Home</a><span>/</span><a href="/legal/">Legal</a><span>/</span><span>{app}</span></div>
    <div style="margin-top:36px"><span class="eyebrow rise" data-d="1"><span class="dot"></span>{app}</span></div>
    <h1 class="rise" data-d="1" style="font-size:clamp(44px,7vw,92px);letter-spacing:-.05em;margin:22px 0 0">{title}</h1>
    <div class="meta-row rise" data-d="2"><span class="tag">Effective {UPDATED}</span><span class="tag">Last updated {UPDATED}</span></div>
    <div class="doc-layout">
      <aside class="toc"><h4>Contents</h4><ol>{toc}</ol></aside>
      <article class="prose">
        <div class="callout">{intro}</div>
        {body}
      </article>
    </div>
  </div>
</section>
'''
    s += foot()
    write(path, s)

def privacy(k, ads, purchases, huawei=False):
    a = APPS[k]; n = a["name"]; e = a["email"]
    third = [
      ("Apple App Store / Google Play" + (" / Huawei AppGallery" if huawei else ""), "Distribution of the App" + (", processing of purchases and subscriptions" if purchases else "") + ". The stores may provide aggregated, anonymous download and crash statistics.", "<a href=\"https://www.apple.com/legal/privacy/\" target=\"_blank\" rel=\"noopener\">Apple</a> · <a href=\"https://policies.google.com/privacy\" target=\"_blank\" rel=\"noopener\">Google</a>" + (" · <a href=\"https://consumer.huawei.com/en/privacy/privacy-policy/\" target=\"_blank\" rel=\"noopener\">Huawei</a>" if huawei else "")),
      ("Google Firebase (Analytics, Crashlytics)", "Anonymous usage statistics and crash reports that help improve stability.", "<a href=\"https://firebase.google.com/support/privacy\" target=\"_blank\" rel=\"noopener\">Firebase</a>"),
    ]
    if ads:
        third.append(("Google AdMob", "Displaying advertisements in the free version of the App. AdMob may use the device advertising identifier, IP address and approximate location to show and measure ads.", "<a href=\"https://policies.google.com/technologies/ads\" target=\"_blank\" rel=\"noopener\">Google Ads</a>"))
    rows = "".join(f"<tr><td><strong>{t}</strong></td><td>{p}</td><td>{l}</td></tr>" for t,p,l in third)
    sections = [
      ("Who we are", f"<p>{n} (the “App”) is developed and published by <strong>Anton Antonchik</strong>, an independent developer (“I”, “we”, “us”). I am the controller of any personal data processed in connection with the App. You can reach me at any time at <a href=\"mailto:{e}\">{e}</a>.</p>"),
      ("Summary", "<ul><li>The App does <strong>not</strong> require an account and does not ask for your name, email address or phone number.</li><li>Data you enter in the App is stored <strong>locally on your device</strong>.</li><li>I do <strong>not</strong> sell your personal data.</li><li>Limited technical data may be processed by the third-party services listed below.</li></ul>"),
      ("Information we process", "<h3>Data stored on your device</h3><p>Settings, preferences and content you create in the App are stored locally on your device and are not transmitted to me.</p><h3>Technical and diagnostic data</h3><p>To keep the App stable, anonymous diagnostic information may be collected automatically: device model, operating system version, app version, crash logs and general usage events. This information does not identify you personally.</p>" + ("<h3>Advertising data</h3><p>If the App shows ads, the advertising partner may process your device’s advertising identifier, IP address and approximate (not precise) location. On iOS you will be asked for permission before any tracking, via App Tracking Transparency.</p>" if ads else "") + ("<h3>Purchases</h3><p>Purchases and subscriptions are processed entirely by the store. I never receive your payment card details; I only receive confirmation that a purchase is active.</p>" if purchases else "") + "<h3>Support correspondence</h3><p>If you email me, I receive your email address and the contents of your message. I use them only to answer you.</p>"),
      ("How and why we use data", "<ul><li>To provide the App and its features (performance of a contract).</li><li>To diagnose crashes and improve the App (legitimate interest).</li>" + ("<li>To show advertising that funds the free version (consent, where required by law).</li>" if ads else "") + ("<li>To unlock paid content you have purchased (performance of a contract).</li>" if purchases else "") + "<li>To reply to your support requests (legitimate interest).</li></ul>"),
      ("Third-party services", f"<p>The App relies on the following providers, each acting under its own privacy policy. Depending on the platform and version, not every service is active in every build.</p><div class=\"table-scroll\"><table><thead><tr><th>Service</th><th>Purpose</th><th>Policy</th></tr></thead><tbody>{rows}</tbody></table></div>"),
      ("Data retention", "<p>Data stored on your device remains there until you delete it or uninstall the App. Diagnostic data is retained by the providers for the periods set out in their policies (typically up to 90 days for crash reports). Support emails are kept for as long as needed to resolve your request and then deleted.</p>"),
      ("Your rights", f"<p>Depending on where you live (including under the EU/UK GDPR and the CCPA), you may have the right to access, correct, delete or export your personal data, to object to or restrict processing, and to withdraw consent at any time. To exercise these rights, email <a href=\"mailto:{e}\">{e}</a>. You also have the right to lodge a complaint with your local data protection authority.</p>"),
      ("Deleting your data", f"<ul><li><strong>In-app data:</strong> uninstall the App — all locally stored data is removed.</li><li><strong>Support emails:</strong> write to <a href=\"mailto:{e}?subject=Data%20deletion\">{e}</a> with the subject “Data deletion”. Your correspondence will be deleted within 30 days.</li>" + ("<li><strong>Advertising identifier:</strong> reset or limit it in your device settings (iOS: Settings → Privacy &amp; Security → Tracking; Android: Settings → Google → Ads).</li>" if ads else "") + "</ul>"),
      ("Children", "<p>The App is not directed to children under 13 (or the equivalent minimum age in your country), and I do not knowingly collect personal data from children. If you believe a child has provided personal data, please get in touch and it will be deleted.</p>"),
      ("Security", "<p>I use reasonable technical and organisational measures to protect information. Data handled by third-party providers is protected by their own security programmes. No method of transmission or storage is completely secure, however.</p>"),
      ("International transfers", "<p>Third-party providers may process data on servers outside your country, including in the United States. Such transfers rely on appropriate safeguards such as the European Commission’s Standard Contractual Clauses.</p>"),
      ("Changes to this policy", "<p>This policy may be updated from time to time. The “Last updated” date at the top of this page shows when it was last revised. Material changes will be highlighted in the App or on this page.</p>"),
      ("Contact", f"<p>Questions about this policy or your data: <a href=\"mailto:{e}\">{e}</a>.<br>Developer: Anton Antonchik · <a href=\"{SITE}\">{SITE.replace('https://','')}</a></p>"),
    ]
    intro = f"<strong>In short:</strong> {n} works without an account, keeps your data on your device, and never sells personal information. This page explains the details."
    legal_page(f"/privacy/{k}/", "Privacy Policy", n, sections, intro, a["tint"])

def terms_pilotiq():
    e = APPS["pilotiq"]["email"]
    sections = [
      ("Agreement", "<p>This Terms of Service Agreement (“Agreement”) is between you (“User” or “you”) and <strong>Anton Antonchik</strong>, the developer of the Pilotiq mobile application (“Pilotiq”, “we”, “our” or “us”; the “App”) for iOS and Android. By downloading or using the App, you agree to be bound by this Agreement. If you do not agree, do not use the App.</p><p>If you obtained the App from the Apple App Store, this Agreement supplements Apple’s <a href=\"https://www.apple.com/legal/internet-services/itunes/dev/stdeula/\" target=\"_blank\" rel=\"noopener\">Licensed Application End User License Agreement</a>.</p>"),
      ("Use of the App", "<p>We grant you a limited, non-exclusive, non-transferable, revocable licence to use the App for your personal, non-commercial use. You may not modify, copy, distribute, transmit, display, perform, reproduce, publish, license, create derivative works from, transfer or sell any information, software, products or services obtained from the App.</p>"),
      ("Educational purpose", "<p>The App is a study aid for the PPL theory examination. It does not replace approved training, official ULC materials or instruction by a certified flight instructor. Passing practice tests does not guarantee passing the official examination.</p>"),
      ("Subscription and payment", "<p>The App offers an auto-renewing subscription (“Subscription”). Payment is charged to your Apple ID or Google Play account at confirmation of purchase. By purchasing the Subscription, you authorise the store to charge the subscription fee and any applicable taxes on a recurring basis until you cancel. Prices are shown in the App before purchase and may change; if they do, you will be notified in advance and may cancel.</p>"),
      ("Auto-renewal and cancellation", "<p>The Subscription renews automatically unless cancelled at least 24 hours before the end of the current period. Your account will be charged for renewal within 24 hours before the end of the current period. You can manage and cancel the Subscription in your App Store or Google Play account settings. Any unused portion of a free trial, if offered, is forfeited when you purchase a Subscription.</p>"),
      ("Refunds", "<p>Payments are processed by Apple or Google, and refunds are governed by their policies. You can request a refund at <a href=\"https://reportaproblem.apple.com\" target=\"_blank\" rel=\"noopener\">reportaproblem.apple.com</a> or via your Google Play order history.</p>"),
      ("Privacy", "<p>Your use of the App is also governed by the <a href=\"/privacy/pilotiq/\">Pilotiq Privacy Policy</a>, which is incorporated into this Agreement by reference.</p>"),
      ("Intellectual property", "<p>The App, its content (including the question database and explanations) and all related intellectual property rights are owned by us or our licensors. You may not use any trademarks, logos or other proprietary designations without our prior written consent.</p>"),
      ("Disclaimer of warranties", "<p>The App is provided “as is” and “as available”, without warranties of any kind, whether express or implied. We do not warrant that the App or its content will be error-free, complete or uninterrupted, or that defects will be corrected.</p>"),
      ("Limitation of liability", "<p>To the maximum extent permitted by law, we shall not be liable for any indirect, incidental, special, punitive or consequential damages arising out of or in connection with this Agreement or the use of the App, even if advised of the possibility of such damages. Nothing in this Agreement limits liability that cannot be limited under applicable consumer law.</p>"),
      ("Governing law", "<p>This Agreement is governed by the laws of the Republic of Poland, without regard to conflict-of-law principles. If you are a consumer, you also benefit from any mandatory provisions of the law of your country of residence.</p>"),
      ("Changes and termination", "<p>We may modify this Agreement at any time; material changes will be announced in the App or on this page, and continued use after the changes take effect constitutes acceptance. We may suspend or terminate your access to the App if you breach this Agreement.</p>"),
      ("Entire agreement", "<p>This Agreement, together with the Privacy Policy and the applicable store terms, constitutes the entire agreement between you and us regarding the App and supersedes all prior communications and proposals.</p>"),
      ("Contact", f"<p>Questions about these terms: <a href=\"mailto:{e}\">{e}</a>.</p>"),
    ]
    intro = "<strong>In short:</strong> Pilotiq is a personal study aid. Subscriptions renew automatically and are managed — and cancelled — in your App Store or Google Play account."
    legal_page("/terms/pilotiq/", "Terms of Service", "Pilotiq", sections, intro, "t-pilotiq")

def redirect(path, to):
    write(path, f'<!DOCTYPE html><html lang="en"><head><meta charset="utf-8"><title>Redirecting…</title><link rel="canonical" href="{SITE}{to}"><meta http-equiv="refresh" content="0; url={to}"><meta name="robots" content="noindex"></head><body style="background:#f6f7fb;color:#0b1533;font-family:system-ui;padding:40px"><a href="{to}" style="color:#0a3492">Continue to {to}</a></body></html>\n')

def page_404():
    s = head("Page not found — Anton Antonchik", "This page does not exist.", "/404.html")
    s += f'''<section class="page-hero" style="min-height:70vh">
  <div class="grid-bg" aria-hidden="true"></div>
  <div class="wrap">
    <span class="eyebrow rise"><span class="dot" style="background:var(--crimson);box-shadow:0 0 0 4px rgba(220,16,56,.15)"></span>Error 404 · Off course</span>
    <h1 class="rise" data-d="1" style="font-size:clamp(56px,11vw,150px);letter-spacing:-.055em;margin:24px 0">Lost <span class="serif grad">signal.</span></h1>
    <p class="lead rise" data-d="2">The page you were looking for has moved or never existed. Let’s get you back on course.</p>
    <div class="hero__cta rise" data-d="3"><a class="btn btn--primary" href="/">Back to home {I["arrow"]}</a><a class="btn" href="/support/">Support</a></div>
  </div>
</section>
'''
    s += foot()
    write("/404.html", s)

page_index(); page_support(); page_legal()
for k in ORDER: page_app(k)
privacy("navcalc", ads=True, purchases=False, huawei=True)
privacy("pilotiq", ads=False, purchases=True)
terms_pilotiq()
redirect("/pilotiq_tos/", "/terms/pilotiq/")
page_404()

urls = ["/","/support/","/legal/"] + [APPS[k]["page"] for k in ORDER] + ["/privacy/navcalc/","/privacy/pilotiq/","/terms/pilotiq/"]
with open(os.path.join(ROOT,"sitemap.xml"),"w") as f:
    f.write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + "".join(f"  <url><loc>{SITE}{u}</loc><lastmod>{UPDATED_ISO}</lastmod></url>\n" for u in urls) + "</urlset>\n")
with open(os.path.join(ROOT,"robots.txt"),"w") as f:
    f.write(f"User-agent: *\nAllow: /\n\nSitemap: {SITE}/sitemap.xml\n")
print("ok")
