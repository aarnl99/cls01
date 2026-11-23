#!/usr/bin/env python3
"""Builds the conference transportation pages in /events from events.json.

Run from the repo root:  python3 tools/event-pages/build.py
Edit events.json to add an event or update dates, then run this again.
The /tools folder is blocked from the public site in _redirects.
"""
import html
import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(ROOT, "events")
SITE = "https://clsgt.com"

BASE_CSS = open(os.path.join(HERE, "base.css"), encoding="utf-8").read()

EXTRA_CSS = """
  /* EVENT PAGES */
  html { scroll-behavior: smooth; }
  img { max-width: 100%; display: block; }

  /* Photo hero */
  .ev-hero { margin-top: 82px; position: relative; overflow: hidden; background: var(--black); color: var(--white); }
  .ev-hero-bg { position: absolute; inset: 0; background-size: cover; background-position: center; transform: scale(1.02); }
  .ev-hero::before { content: ""; position: absolute; inset: 0; z-index: 1;
    background: linear-gradient(90deg, rgba(12,12,12,0.94) 0%, rgba(12,12,12,0.78) 42%, rgba(12,12,12,0.35) 100%),
                linear-gradient(0deg, rgba(12,12,12,0.65) 0%, rgba(12,12,12,0) 45%); }
  .ev-hero-inner { position: relative; z-index: 2; max-width: 1200px; margin: 0 auto; padding: 88px 24px 96px;
    display: grid; grid-template-columns: 1.25fr 0.9fr; gap: 56px; align-items: end; }
  .ev-crumbs { display: flex; flex-wrap: wrap; gap: 8px; font-size: 13px; color: rgba(255,255,255,0.55); margin-bottom: 28px; }
  .ev-crumbs a { color: rgba(255,255,255,0.55); text-decoration: none; }
  .ev-crumbs a:hover { color: var(--white); }
  .ev-eyebrow { display: inline-flex; align-items: center; gap: 10px; font-size: 12px; font-weight: 700; letter-spacing: 0.12em;
    text-transform: uppercase; color: var(--white); background: rgba(196,30,30,0.9); padding: 7px 14px; border-radius: 50px; margin-bottom: 22px; }
  .ev-eyebrow i { width: 7px; height: 7px; border-radius: 50%; background: var(--white); display: inline-block; }
  .ev-hero h1 { font-size: clamp(36px, 5.2vw, 66px); font-weight: 800; line-height: 1.02; letter-spacing: -0.04em; margin-bottom: 20px; max-width: 640px; }
  .ev-hero-lead { font-size: 18px; line-height: 1.65; color: rgba(255,255,255,0.78); max-width: 560px; margin-bottom: 34px; }
  .ev-hero-ctas { display: flex; flex-wrap: wrap; gap: 12px; }
  .ev-btn-ghost { color: var(--white); border: 1px solid rgba(255,255,255,0.35); padding: 14px 28px; border-radius: 50px; font-size: 15px; font-weight: 600;
    text-decoration: none; transition: background 0.15s; display: inline-block; }
  .ev-btn-ghost:hover { background: rgba(255,255,255,0.1); }

  /* Event pass card */
  .ev-pass { background: var(--white); color: var(--black); border-radius: 22px; overflow: hidden; box-shadow: 0 30px 80px rgba(0,0,0,0.45); }
  .ev-pass-top { background: var(--red); color: var(--white); padding: 18px 24px; display: flex; justify-content: space-between; align-items: center; gap: 12px; }
  .ev-pass-top span { font-size: 11px; font-weight: 800; letter-spacing: 0.14em; text-transform: uppercase; }
  .ev-countdown { font-size: 12px; font-weight: 700; background: rgba(255,255,255,0.18); padding: 5px 11px; border-radius: 50px; white-space: nowrap; }
  .ev-pass-name { padding: 22px 24px 6px; font-size: 22px; font-weight: 800; letter-spacing: -0.02em; line-height: 1.2; }
  .ev-pass-rows { padding: 6px 24px 22px; }
  .ev-pass-row { display: grid; grid-template-columns: 34px 1fr; gap: 12px; padding: 14px 0; border-bottom: 1px dashed var(--gray-light); }
  .ev-pass-row:last-child { border-bottom: none; }
  .ev-pass-ico { width: 34px; height: 34px; border-radius: 10px; background: rgba(196,30,30,0.08); display: flex; align-items: center; justify-content: center; }
  .ev-pass-ico svg { width: 17px; height: 17px; stroke: var(--red); }
  .ev-pass-lbl { font-size: 11px; font-weight: 700; letter-spacing: 0.1em; text-transform: uppercase; color: var(--gray-mid); margin-bottom: 3px; }
  .ev-pass-val { font-size: 15px; font-weight: 700; line-height: 1.35; }
  .ev-pass-sub { font-size: 13px; color: var(--gray-mid); margin-top: 2px; line-height: 1.45; }

  /* Source note under hero */
  .ev-source { background: var(--white); border-bottom: 1px solid var(--gray-light); }
  .ev-source p { max-width: 1200px; margin: 0 auto; padding: 16px 24px; font-size: 13px; color: var(--gray-mid); line-height: 1.6; }
  .ev-source a { color: var(--black); }

  /* Plan cards */
  .plan-grid { display: grid; grid-template-columns: repeat(3,1fr); gap: 18px; }
  .plan-card { background: var(--white); border: 1px solid var(--gray-light); border-radius: 20px; padding: 30px 28px; position: relative; transition: transform 0.18s, box-shadow 0.18s; }
  .plan-card:hover { transform: translateY(-3px); box-shadow: 0 18px 40px rgba(0,0,0,0.07); }
  .plan-ico { width: 52px; height: 52px; border-radius: 16px; background: var(--red); display: flex; align-items: center; justify-content: center; margin-bottom: 22px; }
  .plan-ico svg { width: 24px; height: 24px; stroke: var(--white); }
  .plan-card h3 { font-size: 19px; font-weight: 800; letter-spacing: -0.02em; margin-bottom: 10px; }
  .plan-card p { font-size: 15px; color: var(--gray-mid); line-height: 1.65; }

  /* Split photo section */
  .split { display: grid; grid-template-columns: 1fr 1fr; gap: 56px; align-items: center; }
  .split-photo { position: relative; border-radius: 24px; overflow: hidden; aspect-ratio: 4 / 3.2; background: var(--gray-light); }
  .split-photo img { width: 100%; height: 100%; object-fit: cover; }
  .split-photo-tag { position: absolute; left: 18px; bottom: 18px; background: rgba(255,255,255,0.95); border-radius: 14px; padding: 12px 16px; }
  .split-photo-tag strong { display: block; font-size: 22px; font-weight: 800; letter-spacing: -0.02em; }
  .split-photo-tag span { font-size: 12px; color: var(--gray-mid); }
  .why-list { list-style: none; display: grid; gap: 14px; margin-top: 8px; }
  .why-list li { font-size: 16px; color: var(--charcoal); line-height: 1.55; padding-left: 34px; position: relative; }
  .why-list li::before { content: "✓"; position: absolute; left: 0; top: 1px; width: 22px; height: 22px; border-radius: 50%;
    background: rgba(196,30,30,0.1); color: var(--red); font-size: 12px; font-weight: 800; display: flex; align-items: center; justify-content: center; }
  .mini-stats { display: flex; gap: 32px; flex-wrap: wrap; margin-top: 32px; padding-top: 28px; border-top: 1px solid var(--gray-light); }
  .mini-stats strong { display: block; font-size: 30px; font-weight: 800; letter-spacing: -0.03em; color: var(--black); }
  .mini-stats span { font-size: 13px; color: var(--gray-mid); }

  /* Steps */
  .steps3 { display: grid; grid-template-columns: repeat(3,1fr); gap: 18px; counter-reset: s; }
  .step3 { background: var(--gray-bg); border-radius: 20px; padding: 28px; border: 1px solid var(--gray-light); }
  .step3-num { font-size: 13px; font-weight: 800; color: var(--red); letter-spacing: 0.08em; margin-bottom: 14px; }
  .step3 h3 { font-size: 18px; font-weight: 800; letter-spacing: -0.02em; margin-bottom: 8px; }
  .step3 p { font-size: 15px; color: var(--gray-mid); line-height: 1.6; }

  /* Fleet tiles */
  .fleet-tiles { display: grid; grid-template-columns: repeat(6,1fr); gap: 12px; }
  .fleet-tile { background: var(--gray-bg); border: 1px solid var(--gray-light); border-radius: 16px; padding: 20px 16px; text-align: center; }
  .fleet-tile svg { width: 30px; height: 30px; stroke: var(--black); margin: 0 auto 12px; }
  .fleet-tile strong { display: block; font-size: 14px; font-weight: 700; margin-bottom: 4px; }
  .fleet-tile span { font-size: 12px; color: var(--gray-mid); }

  /* Dark quote section */
  .ev-quote { background: var(--black); color: var(--white); padding: 96px 24px; }
  .ev-quote-wrap { max-width: 1200px; margin: 0 auto; display: grid; grid-template-columns: 1fr 1.05fr; gap: 56px; align-items: start; }
  .ev-quote .section-label { color: #ff6b6b; }
  .ev-quote h2 { font-size: clamp(30px, 3.6vw, 46px); font-weight: 800; letter-spacing: -0.035em; line-height: 1.08; margin-bottom: 16px; }
  .ev-quote-lead { font-size: 17px; color: rgba(255,255,255,0.65); line-height: 1.65; margin-bottom: 28px; max-width: 460px; }
  .ev-quote .why-list li { color: rgba(255,255,255,0.85); font-size: 15px; }
  .ev-quote .why-list li::before { background: rgba(255,255,255,0.12); color: var(--white); }
  .ev-quote-phone { margin-top: 32px; font-size: 14px; color: rgba(255,255,255,0.55); }
  .ev-quote-phone a { display: block; font-size: 26px; font-weight: 800; color: var(--white); text-decoration: none; letter-spacing: -0.02em; margin-top: 4px; }
  .ev-form { background: var(--white); color: var(--black); border-radius: 22px; padding: 30px; display: flex; flex-direction: column; gap: 12px; box-shadow: 0 30px 80px rgba(0,0,0,0.35); }
  .ev-form-title { font-size: 18px; font-weight: 800; letter-spacing: -0.02em; margin-bottom: 4px; }
  .ev-form .form-row { display: grid; grid-template-columns: 1fr 1fr; gap: 12px; }
  .ev-form input, .ev-form select, .ev-form textarea { width: 100%; font: inherit; font-size: 15px; padding: 13px 14px; border: 1px solid var(--gray-light);
    border-radius: 12px; background: var(--gray-bg); color: var(--black); -webkit-appearance: none; appearance: none; }
  .ev-form select { background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='12' height='8' viewBox='0 0 12 8'%3E%3Cpath d='M1 1l5 5 5-5' fill='none' stroke='%236B6B6B' stroke-width='2'/%3E%3C/svg%3E");
    background-repeat: no-repeat; background-position: right 14px center; padding-right: 36px; }
  .ev-form textarea { min-height: 96px; resize: vertical; }
  .ev-form input:focus, .ev-form select:focus, .ev-form textarea:focus { outline: 2px solid rgba(196,30,30,0.3); border-color: var(--red); background-color: var(--white); }
  .ev-form button { background: var(--red); color: var(--white); font: inherit; font-size: 16px; font-weight: 700; padding: 16px 28px; border: none; border-radius: 50px; cursor: pointer; margin-top: 4px; }
  .ev-form button:hover { background: var(--red-dark); }
  .ev-form .quote-note { font-size: 13px; color: var(--gray-mid); text-align: center; }
  .ev-form .quote-note a { color: var(--black); }
  .ev-form .cls-form-status { font-size: 14px; color: var(--black); text-align: center; }

  /* Event cards with photo */
  .ev-list { display: grid; grid-template-columns: repeat(3,1fr); gap: 20px; }
  .ev-card { display: flex; flex-direction: column; background: var(--white); border: 1px solid var(--gray-light); border-radius: 20px; overflow: hidden;
    text-decoration: none; color: var(--black); transition: transform 0.18s, box-shadow 0.18s, border-color 0.18s; }
  .ev-card:hover { transform: translateY(-4px); box-shadow: 0 22px 50px rgba(0,0,0,0.09); border-color: transparent; }
  .ev-card-img { position: relative; aspect-ratio: 16 / 9; overflow: hidden; background: var(--charcoal); }
  .ev-card-img img { width: 100%; height: 100%; object-fit: cover; transition: transform 0.4s; }
  .ev-card:hover .ev-card-img img { transform: scale(1.05); }
  .ev-card-img::after { content: ""; position: absolute; inset: 0; background: linear-gradient(0deg, rgba(0,0,0,0.45), rgba(0,0,0,0) 60%); }
  .ev-cal { position: absolute; z-index: 2; left: 14px; top: 14px; background: var(--white); border-radius: 12px; overflow: hidden; text-align: center; min-width: 64px; box-shadow: 0 6px 18px rgba(0,0,0,0.2); }
  .ev-cal b { display: block; background: var(--red); color: var(--white); font-size: 11px; font-weight: 800; letter-spacing: 0.12em; padding: 4px 8px; }
  .ev-cal span { display: block; font-size: 13px; font-weight: 800; padding: 6px 10px; white-space: nowrap; }
  .ev-card-city { position: absolute; z-index: 2; left: 16px; bottom: 12px; color: var(--white); font-size: 12px; font-weight: 700; letter-spacing: 0.08em; text-transform: uppercase; }
  .ev-card-body { padding: 22px 22px 24px; display: flex; flex-direction: column; flex: 1; }
  .ev-card h3 { font-size: 19px; font-weight: 800; letter-spacing: -0.02em; line-height: 1.25; margin-bottom: 8px; }
  .ev-card p { font-size: 14px; color: var(--gray-mid); line-height: 1.6; flex: 1; }
  .ev-card-meta { display: flex; justify-content: space-between; align-items: center; margin-top: 18px; padding-top: 16px; border-top: 1px solid var(--gray-light); font-size: 13px; }
  .ev-card-meta span { color: var(--gray-mid); }
  .ev-card-meta strong { color: var(--red); font-weight: 700; }

  /* Index hero (illustration) */
  .ix-hero { margin-top: 82px; position: relative; overflow: hidden; background: #f3ece4; }
  .ix-hero-bg { position: absolute; inset: 0; background: url('/hero.jpg') center 60% / cover no-repeat; }
  .ix-hero::before { content: ""; position: absolute; inset: 0; z-index: 1;
    background: linear-gradient(90deg, rgba(255,255,255,0.97) 0%, rgba(255,255,255,0.9) 38%, rgba(255,255,255,0.15) 75%, rgba(255,255,255,0) 100%); }
  .ix-hero-inner { position: relative; z-index: 2; max-width: 1200px; margin: 0 auto; padding: 96px 24px 104px; }
  .ix-hero h1 { font-size: clamp(38px, 5.4vw, 68px); font-weight: 800; line-height: 1.02; letter-spacing: -0.045em; max-width: 640px; margin-bottom: 20px; }
  .ix-hero h1 em { font-style: normal; color: var(--red); }
  .ix-hero p { font-size: 18px; line-height: 1.65; color: var(--charcoal); max-width: 540px; margin-bottom: 34px; }
  .ix-hero .ev-crumbs, .ix-hero .ev-crumbs a { color: var(--gray-mid); }
  .ix-hero .ev-crumbs a:hover { color: var(--black); }
  .ix-stats { display: flex; gap: 40px; flex-wrap: wrap; margin-top: 44px; }
  .ix-stats strong { display: block; font-size: 30px; font-weight: 800; letter-spacing: -0.03em; }
  .ix-stats span { font-size: 13px; color: var(--gray-mid); }
  .ix-group { margin-top: 56px; }
  .ix-group:first-of-type { margin-top: 8px; }
  .ix-group-h { display: flex; align-items: center; gap: 16px; margin-bottom: 22px; }
  .ix-group-h h3 { font-size: 14px; font-weight: 800; letter-spacing: 0.1em; text-transform: uppercase; color: var(--black); white-space: nowrap; }
  .ix-group-h div { flex: 1; height: 1px; background: var(--gray-light); }
  .reasons { display: grid; grid-template-columns: repeat(3,1fr); gap: 18px; }
  .reason { background: var(--white); border-radius: 20px; padding: 30px 28px; border: 1px solid var(--gray-light); }
  .reason strong { display: block; font-size: 40px; font-weight: 800; letter-spacing: -0.04em; color: var(--red); line-height: 1; margin-bottom: 14px; }
  .reason h3 { font-size: 18px; font-weight: 800; margin-bottom: 8px; letter-spacing: -0.02em; }
  .reason p { font-size: 15px; color: var(--gray-mid); line-height: 1.6; }

  /* Phones and tablets */
  @media (max-width: 1020px) {
    .fleet-tiles { grid-template-columns: repeat(3,1fr); }
    .ev-list { grid-template-columns: repeat(2,1fr); }
  }
  @media (max-width: 960px) {
    .nav-links, .nav-right { display: none; }
    .nav-hamburger { display: flex; }
    .ev-hero-inner { grid-template-columns: 1fr; gap: 36px; padding: 64px 20px 56px; }
    .ev-hero::before { background: linear-gradient(180deg, rgba(12,12,12,0.82) 0%, rgba(12,12,12,0.9) 100%); }
    .split { grid-template-columns: 1fr; gap: 32px; }
    .ev-quote-wrap { grid-template-columns: 1fr; gap: 36px; }
    .plan-grid, .steps3, .reasons { grid-template-columns: 1fr; }
    .ix-hero::before { background: linear-gradient(180deg, rgba(255,255,255,0.95) 0%, rgba(255,255,255,0.88) 100%); }
    .ix-hero-inner { padding: 64px 20px 72px; }
  }
  @media (max-width: 640px) {
    nav { width: calc(100% - 20px); padding: 0 14px; }
    .ev-hero, .ix-hero { margin-top: 76px; }
    .section { padding: 64px 20px; }
    .ev-hero-lead, .ix-hero p { font-size: 16px; }
    .ev-hero-ctas a { flex: 1 1 100%; text-align: center; }
    .ev-pass-name { font-size: 19px; }
    .ev-list { grid-template-columns: 1fr; }
    .fleet-tiles { grid-template-columns: repeat(2,1fr); }
    .ev-form { padding: 22px; }
    .ev-form .form-row { grid-template-columns: 1fr; }
    .ev-quote { padding: 72px 20px; }
    .ix-stats { gap: 24px; }
    .mini-stats { gap: 22px; }
  }
"""


LOGO_SVG = (
    '<svg viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="2.2" '
    'stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/>'
    '<path d="M2 12h20M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 '
    '15.3 15.3 0 0 1 4-10z"/></svg>'
)

LOCAL_BUSINESS = {
    "@type": "LocalBusiness",
    "@id": SITE + "/#cls-global-transportation",
    "name": "CLS Global Transportation",
    "url": SITE,
    "telephone": "+16504608778",
}


def e(text):
    return html.escape(str(text), quote=True)


def head(title, description, path, ld_blocks):
    ld = "\n".join(
        '<script type="application/ld+json">\n' + json.dumps(b, indent=2, ensure_ascii=False) + "\n</script>"
        for b in ld_blocks
    )
    url = SITE + path
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="google-site-verification" content="7jbHhe_Yhm05NuSiomC2O0QaMhTyOEO22_0uCEOFywg">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{e(title)}</title>
<meta name="description" content="{e(description)}">
<link rel="canonical" href="{url}">
<meta property="og:type" content="website">
<meta property="og:title" content="{e(title)}">
<meta property="og:description" content="{e(description)}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{SITE}/img-events.jpg">
<meta name="twitter:card" content="summary_large_image">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap" rel="stylesheet">
<style>
{BASE_CSS}
{EXTRA_CSS}
</style>
{ld}
<link rel="icon" href="/favicon.ico" sizes="48x48">
<link rel="icon" type="image/svg+xml" href="/favicon.svg">
<link rel="icon" type="image/png" sizes="32x32" href="/favicon-32x32.png">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<link rel="manifest" href="/site.webmanifest">
</head>
<body>
"""


def nav(quote_href="#quote"):
    return f"""
<nav>
  <a href="/index.html" class="nav-logo">
    <div class="nav-logo-icon">
      {LOGO_SVG}
    </div>
    <div class="nav-logo-text">
      <strong>CLS Global</strong>
      <span>Transportation</span>
    </div>
  </a>
  <ul class="nav-links">
    <li><a href="/corporate-shuttle.html">Corporate</a></li>
    <li><a href="/university.html">University</a></li>
    <li><a href="/events-charter.html" class="active">Events &amp; Charter</a></li>
    <li><a href="/fleet.html">Fleet</a></li>
    <li><a href="/index.html#tech">Technology</a></li>
    <li><a href="/about.html">About</a></li>
  </ul>
  <div class="nav-right">
    <a href="tel:6504608778" class="nav-phone">650.460.8778</a>
    <a href="{quote_href}" class="btn-red">Get a Quote</a>
  </div>
  <button class="nav-hamburger" id="navHamburger" aria-label="Menu">
    <span></span><span></span><span></span>
  </button>
</nav>
<div class="mobile-menu" id="mobileMenu">
  <a href="/corporate-shuttle.html">Corporate</a>
  <a href="/university.html">University</a>
  <a href="/events-charter.html">Events &amp; Charter</a>
  <a href="/events/">Conference Transportation</a>
  <a href="/fleet.html">Fleet</a>
  <a href="/about.html">About</a>
  <a href="tel:6504608778">650.460.8778</a>
  <a href="{quote_href}" class="mobile-cta">Get a Quote</a>
</div>
"""


def footer():
    return """
<footer>
  <div class="footer-top">
    <div class="footer-brand">
      <strong>CLS Global Transportation</strong>
      <p>The Bay Area's transportation partner for corporate shuttles, campus transit, and events since 2011. Serving San Francisco, the Peninsula, South Bay, and East Bay.</p>
      <div class="footer-contact">
        <a href="tel:6504608778"><strong>650.460.8778</strong></a><span style="color:inherit"> Call or Text</span>
        <a href="/contact">Contact us</a>
      </div>
    </div>
    <div class="footer-col">
      <h5>Corporate</h5>
      <a href="/corporate-shuttle.html">Commuter Shuttles</a>
      <a href="/corporate-shuttle.html">Inter-Campus</a>
      <a href="/corporate-shuttle.html">Last Mile</a>
      <a href="/corporate-shuttle.html">Parking Shuttles</a>
    </div>
    <div class="footer-col">
      <h5>University &amp; Gov</h5>
      <a href="/university.html">University Transit</a>
      <a href="/government.html">Municipal Shuttles</a>
      <a href="/government.html#ada">ADA &amp; Paratransit</a>
    </div>
    <div class="footer-col">
      <h5>Events &amp; Charter</h5>
      <a href="/events/">Conference Transportation</a>
      <a href="/events-charter.html">Airport Service</a>
      <a href="/events-charter.html">Sedan &amp; SUV</a>
      <a href="/events-charter.html">Limo Service</a>
      <a href="/events-charter.html">Sporting Events</a>
    </div>
    <div class="footer-col">
      <h5>Company</h5>
      <a href="/about.html">About CLS</a>
      <a href="/safety-technology.html">Safety &amp; Tech</a>
      <a href="/fleet.html">Fleet</a>
      <a href="/careers.html">Careers</a>
      <a href="/privacy-policy">Privacy Policy</a>
    </div>
  </div>
  <div class="footer-bottom">
    <span>CLS Global Transportation, Inc. All rights reserved.</span>
    <span>Bay Area's Transportation Partner Since 2011</span>
  </div>
</footer>

<script src="/contact.js"></script>
<script>
  document.querySelectorAll('.faq-q').forEach(function (q) {
    q.addEventListener('click', function () {
      var item = q.parentElement;
      var wasOpen = item.classList.contains('open');
      document.querySelectorAll('.faq-item').forEach(function (i) { i.classList.remove('open'); });
      if (!wasOpen) item.classList.add('open');
    });
  });
  var btn = document.getElementById('navHamburger');
  var menu = document.getElementById('mobileMenu');
  if (btn && menu) {
    btn.addEventListener('click', function () { btn.classList.toggle('open'); menu.classList.toggle('open'); });
    menu.querySelectorAll('a').forEach(function (a) {
      a.addEventListener('click', function () { btn.classList.remove('open'); menu.classList.remove('open'); });
    });
  }
</script>
</body>
</html>
"""



ICONS = {
    "calendar": '<svg viewBox="0 0 24 24" fill="none" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="4" width="18" height="18" rx="2"/><path d="M16 2v4M8 2v4M3 10h18"/></svg>',
    "pin": '<svg viewBox="0 0 24 24" fill="none" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 10c0 7-9 13-9 13S3 17 3 10a9 9 0 0 1 18 0z"/><circle cx="12" cy="10" r="3"/></svg>',
    "people": '<svg viewBox="0 0 24 24" fill="none" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M23 21v-2a4 4 0 0 0-3-3.87M16 3.13a4 4 0 0 1 0 7.75"/></svg>',
    "flag": '<svg viewBox="0 0 24 24" fill="none" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M4 15s1-1 4-1 5 2 8 2 4-1 4-1V3s-1 1-4 1-5-2-8-2-4 1-4 1z"/><path d="M4 22v-7"/></svg>',
    "bus": '<svg viewBox="0 0 24 24" fill="none" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="3" width="18" height="15" rx="3"/><path d="M3 11h18M7 18v3M17 18v3"/><circle cx="7.5" cy="14.5" r="1"/><circle cx="16.5" cy="14.5" r="1"/></svg>',
    "plane": '<svg viewBox="0 0 24 24" fill="none" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M17.8 19.2 16 11l3.5-3.5C21 6 21.5 4 21 3c-1-.5-3 0-4.5 1.5L13 8 4.8 6.2c-.5-.1-.9.1-1.1.5l-.3.5c-.2.5-.1 1 .3 1.3L9 12l-2 3H4l-1 1 3 2 2 3 1-1v-3l3-2 3.5 5.3c.3.4.8.5 1.3.3l.5-.2c.4-.3.6-.7.5-1.2z"/></svg>',
    "glass": '<svg viewBox="0 0 24 24" fill="none" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M8 22h8M12 15v7M5 3h14l-1 6a6 6 0 0 1-12 0z"/></svg>',
    "car": '<svg viewBox="0 0 24 24" fill="none" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M5 17h14v-5l-2-5H7l-2 5z"/><path d="M3 12h18M5 17v2M19 17v2"/><circle cx="8" cy="14.5" r="1"/><circle cx="16" cy="14.5" r="1"/></svg>',
    "van": '<svg viewBox="0 0 24 24" fill="none" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M2 17V7a2 2 0 0 1 2-2h11l5 5v7z"/><path d="M15 5v5h5M2 11h13"/><circle cx="7" cy="17.5" r="2"/><circle cx="17" cy="17.5" r="2"/></svg>',
    "access": '<svg viewBox="0 0 24 24" fill="none" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="4" r="2"/><path d="M12 7v6h5l2 5M12 10H8"/><path d="M8.5 13.5a5 5 0 1 0 6.5 6"/></svg>',
}


def plan_icon(title):
    t = title.lower()
    if "airport" in t or "sjc" in t or "sfo" in t:
        return ICONS["plane"]
    if "dinner" in t or "party" in t or "event" in t or "reception" in t:
        return ICONS["glass"]
    if "shuttle" in t:
        return ICONS["bus"]
    return ICONS["car"]


def quote_form(ev):
    """Same form name and fields as the charter form on the home page, so
    entries land in the same Netlify form and Slack channel. The label names the event."""
    label = f"Event quote: {ev['name']}"
    date_val = ev.get("start_date") if ev.get("dates_confirmed") else ""
    return f"""
<section class="ev-quote" id="quote">
  <div class="ev-quote-wrap">
    <div>
      <div class="section-label">Get a Quote</div>
      <h2>Planning rides for {e(ev['short'])}? Let's map it out.</h2>
      <p class="ev-quote-lead">Tell us your dates, how many people, and where they need to go. We send back a plan and a price, usually within 24 hours.</p>
      <ul class="why-list">
        <li>Hotel shuttles, airport runs, and dinner rides in one plan</li>
        <li>Fixed pricing quoted upfront, no surge pricing</li>
        <li>Certificate of insurance for your venue, often the same day</li>
        <li>One direct dispatch number, open 24/7</li>
      </ul>
      <div class="ev-quote-phone">Rather talk it through? Call or text<a href="tel:6504608778">650.460.8778</a></div>
    </div>
    <form class="ev-form" name="charter-quote" method="POST" data-netlify="true" netlify-honeypot="bot-field" onsubmit="return clsSendForm(event);">
      <div class="ev-form-title">Request a quote for {e(ev['short'])}</div>
      <input type="hidden" name="form-name" value="charter-quote">
      <input type="hidden" name="form_label" value="{e(label)}">
      <p hidden><label>Leave this empty: <input name="bot-field"></label></p>
      <div class="form-row">
        <input type="text" name="name" placeholder="Your name" required aria-label="Your name">
        <input type="tel" name="phone" placeholder="Phone number" aria-label="Phone number">
      </div>
      <input type="email" name="email" placeholder="Work email" required aria-label="Work email">
      <select name="occasion" aria-label="What is the occasion?">
        <option selected>Conference or Convention</option>
        <option>Corporate Retreat or Offsite</option>
        <option>Airport Transfer</option>
        <option>Something else</option>
      </select>
      <div class="form-row">
        <input type="date" name="event_date" value="{e(date_val)}" aria-label="First day you need rides" title="First day you need rides">
        <input type="text" name="group_size" placeholder="How many people?" aria-label="How many people?">
      </div>
      <div class="form-row">
        <input type="text" name="pickup" placeholder="Pickup (hotel, SFO, office)" aria-label="Pickup location">
        <input type="text" name="dropoff" placeholder="Drop-off (venue, dinner)" aria-label="Drop-off location">
      </div>
      <select name="vehicle" aria-label="Vehicle">
        <option value="" disabled selected>Vehicle, if you know (optional)</option>
        <option>Not sure, recommend one</option>
        <option>Executive Sprinter (10 to 14)</option>
        <option>Limo Bus (up to 26)</option>
        <option>Mini Coach (up to 37)</option>
        <option>Motorcoach (40 to 57)</option>
        <option>ADA Coach</option>
        <option>Sedan, SUV or Limo</option>
      </select>
      <textarea name="notes" placeholder="Which days? Hotel loop, airport pickups, a dinner or party? Tell us what you have in mind."></textarea>
      <button type="submit">Send My Request</button>
      <p class="cls-form-status" role="status" style="display:none;"></p>
      <p class="quote-note">Or <a href="/contact">contact us</a></p>
    </form>
  </div>
</section>
"""


def ev_card(o):
    return f"""      <a class="ev-card" href="/events/{o['slug']}">
        <div class="ev-card-img">
          <img src="/{e(o['image'])}" alt="CLS vehicle ready for a Bay Area conference group" loading="lazy" width="572" height="322">
          <div class="ev-cal"><b>{e(o['cal'][0])}</b><span>{e(o['cal'][1])}</span></div>
          <div class="ev-card-city">{e(o['city_short'])}</div>
        </div>
        <div class="ev-card-body">
          <h3>{e(o['name'])}</h3>
          <p>{e(o['card_line'])}</p>
          <div class="ev-card-meta"><span>{e(o['venue_short'])}</span><strong>See plan ›</strong></div>
        </div>
      </a>"""


FLEET = [
    ("car", "Sedan and SUV", "1 to 6 riders"),
    ("van", "Executive Sprinter", "10 to 14 riders"),
    ("glass", "Limo Bus", "Up to 26 riders"),
    ("bus", "Mini Coach", "Up to 37 riders"),
    ("bus", "Motorcoach", "40 to 57 riders"),
    ("access", "ADA Coach", "Accessible setups"),
]

COUNTDOWN_JS = """
<script>
  document.querySelectorAll('[data-start]').forEach(function (el) {
    var start = new Date(el.getAttribute('data-start') + 'T00:00:00');
    var days = Math.ceil((start - new Date()) / 86400000);
    if (days > 1) el.textContent = 'In ' + days + ' days';
    else if (days >= -4) el.textContent = 'Happening now';
    else el.style.display = 'none';
  });
</script>
"""


def event_page(ev, all_events):
    path = f"/events/{ev['slug']}"
    title = ev["seo_title"]
    desc = ev["meta"]
    crumbs = {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": SITE + "/"},
            {"@type": "ListItem", "position": 2, "name": "Conference Transportation", "item": SITE + "/events/"},
            {"@type": "ListItem", "position": 3, "name": ev["name"], "item": SITE + path},
        ],
    }
    service = {
        "@context": "https://schema.org",
        "@type": "Service",
        "name": f"{ev['name']} Transportation",
        "serviceType": "Event Transportation",
        "description": desc,
        "provider": LOCAL_BUSINESS,
        "areaServed": ev["area_served"],
        "url": SITE + path,
    }
    own = ev.get("faqs", [])
    has_booking_q = any("book" in q[0].lower() for q in own)
    faqs = own + [f for f in common_faqs(ev) if not (has_booking_q and f[0].startswith("How early should we book"))]
    faq_ld = {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faqs
        ],
    }

    countdown = f'<span class="ev-countdown" data-start="{e(ev["start_date"])}"></span>' if ev["dates_confirmed"] else ""
    plans = "\n".join(
        f'      <div class="plan-card"><div class="plan-ico">{plan_icon(h)}</div><h3>{e(h)}</h3><p>{e(p)}</p></div>'
        for h, p in ev["plans"]
    )
    fleet = "\n".join(
        f'      <div class="fleet-tile">{ICONS[i]}<strong>{e(n)}</strong><span>{e(c)}</span></div>' for i, n, c in FLEET
    )
    getting = "\n".join(
        f'      <div class="step3"><h3>{e(h)}</h3><p>{e(p)}</p></div>' for h, p in ev["getting"]
    )
    others = [o for o in all_events if o["slug"] != ev["slug"]][:3]
    other_cards = "\n".join(ev_card(o) for o in others)
    split_img = "img-corporate.jpg" if ev["image"] == "img-executive.jpg" else "img-executive.jpg"

    body = f"""
<section class="ev-hero">
  <div class="ev-hero-bg" style="background-image:url('/{e(ev['image'])}');"></div>
  <div class="ev-hero-inner">
    <div>
      <div class="ev-crumbs"><a href="/index.html">Home</a><span>›</span><a href="/events/">Conference Transportation</a><span>›</span><span>{e(ev['short'])}</span></div>
      <div class="ev-eyebrow"><i></i>{e(ev['tag'])}</div>
      <h1>{e(ev['h1'])}</h1>
      <p class="ev-hero-lead">{e(ev['intro'])}</p>
      <div class="ev-hero-ctas">
        <a href="#quote" class="btn-red-lg">Get a Quote for {e(ev['short'])}</a>
        <a href="tel:6504608778" class="ev-btn-ghost">Call 650.460.8778</a>
      </div>
    </div>
    <div class="ev-pass">
      <div class="ev-pass-top"><span>Event at a glance</span>{countdown}</div>
      <div class="ev-pass-name">{e(ev['name'])}</div>
      <div class="ev-pass-rows">
        <div class="ev-pass-row"><div class="ev-pass-ico">{ICONS['calendar']}</div><div><div class="ev-pass-lbl">Dates</div><div class="ev-pass-val">{e(ev['dates_text'])}</div></div></div>
        <div class="ev-pass-row"><div class="ev-pass-ico">{ICONS['pin']}</div><div><div class="ev-pass-lbl">Venue</div><div class="ev-pass-val">{e(ev['venue'])}</div><div class="ev-pass-sub">{e(ev['city'])}</div></div></div>
        <div class="ev-pass-row"><div class="ev-pass-ico">{ICONS['people']}</div><div><div class="ev-pass-lbl">Crowd size</div><div class="ev-pass-val">{e(ev['attendance'])}</div><div class="ev-pass-sub">{e(ev.get('attendance_note',''))}</div></div></div>
        <div class="ev-pass-row"><div class="ev-pass-ico">{ICONS['flag']}</div><div><div class="ev-pass-lbl">Hosted by</div><div class="ev-pass-val">{e(ev['organizer'])}</div></div></div>
      </div>
    </div>
  </div>
</section>
<div class="ev-source"><p>Event details come from the organizer's website, <a href="{e(ev['official_url'])}" rel="nofollow noopener" target="_blank">{e(ev['official_label'])}</a>. Please check there for the latest. CLS Global Transportation is an independent company and is not affiliated with or endorsed by {e(ev['organizer'])}.</p></div>

<section class="section">
  <div class="section-inner">
    <div class="section-label">How We Help</div>
    <h2>{e(ev['plans_h2'])}</h2>
    <p class="section-sub">{e(ev['plans_sub'])}</p>
    <div class="plan-grid">
{plans}
    </div>
  </div>
</section>

<section class="section" style="background:var(--white);">
  <div class="section-inner">
    <div class="section-label">Getting Around</div>
    <h2>Getting around during {e(ev['name'])}</h2>
    <p class="section-sub">A few things to know before you plan rides for your team.</p>
    <div class="steps3">
{getting}
    </div>
  </div>
</section>

<section class="section">
  <div class="section-inner split">
    <div class="split-photo">
      <img src="/{split_img}" alt="CLS Global Transportation vehicles and driver" loading="lazy" width="1024" height="572">
      <div class="split-photo-tag"><strong>5,000+</strong><span>events managed</span></div>
    </div>
    <div>
      <div class="section-label">Why CLS</div>
      <h2>A Bay Area company that has done this since 2011.</h2>
      <ul class="why-list">
        <li>Our own employee drivers, not gig drivers or subcontractors</li>
        <li>Live GPS tracking on every vehicle</li>
        <li>A written run plan before your event</li>
        <li>ADA accessible coaches when you need them</li>
      </ul>
      <div class="mini-stats">
        <div><strong>15+</strong><span>years in the Bay Area</span></div>
        <div><strong>24/7</strong><span>dispatch</span></div>
        <div><strong>1 to 57</strong><span>riders per vehicle</span></div>
      </div>
    </div>
  </div>
</section>

<section class="section" style="background:var(--white);">
  <div class="section-inner">
    <div class="section-label">How It Works</div>
    <h2>Three steps. Then we take it from there.</h2>
    <p class="section-sub">You tell us what the week looks like. We plan the rides and run them.</p>
    <div class="steps3">
      <div class="step3"><div class="step3-num">STEP 1</div><h3>Tell us your plans</h3><p>Dates, headcount, hotels, and any dinners or parties. A rough idea is fine to start.</p></div>
      <div class="step3"><div class="step3-num">STEP 2</div><h3>Get a plan and a price</h3><p>We pick the right vehicles and send a run plan with a fixed price, usually within 24 hours.</p></div>
      <div class="step3"><div class="step3-num">STEP 3</div><h3>We run it live</h3><p>On event days, our dispatch team watches every vehicle and is one call away the whole time.</p></div>
    </div>
  </div>
</section>

<section class="section">
  <div class="section-inner">
    <div class="section-label">The Fleet</div>
    <h2>The right size vehicle for every group.</h2>
    <p class="section-sub">From one executive to a full hotel loop. <a href="/fleet.html" style="color:var(--black);font-weight:600;">See the full fleet</a></p>
    <div class="fleet-tiles">
{fleet}
    </div>
  </div>
</section>
{faq_html(faqs)}
{quote_form(ev)}
<section class="section">
  <div class="section-inner">
    <div class="section-label">More Bay Area Events</div>
    <h2>Other big conferences we can help with.</h2>
    <p class="section-sub"><a href="/events/" style="color:var(--black);font-weight:600;">See all upcoming Bay Area conferences ›</a></p>
    <div class="ev-list">
{other_cards}
    </div>
  </div>
</section>
"""
    return head(title, desc, path, [crumbs, service, faq_ld]) + nav() + body + COUNTDOWN_JS + footer()


def index_page(events):
    path = "/events/"
    title = "Bay Area Conference Transportation 2027: Shuttles and Car Service | CLS"
    desc = ("Transportation for the biggest San Francisco and Bay Area conferences in 2027. "
            "Hotel shuttles, airport pickups, VIP cars, and group charters from CLS Global Transportation.")
    first = [ev for ev in events if ev["start_date"] < "2027-05-01"]
    later = [ev for ev in events if ev["start_date"] >= "2027-05-01"]
    groups = [("Winter and spring 2027", first), ("Summer and fall 2027", later)]
    group_html = "\n".join(
        f"""    <div class="ix-group">
      <div class="ix-group-h"><h3>{e(name)}</h3><div></div></div>
      <div class="ev-list">
{chr(10).join(ev_card(ev) for ev in evs)}
      </div>
    </div>"""
        for name, evs in groups if evs
    )
    item_list = {
        "@context": "https://schema.org",
        "@type": "ItemList",
        "name": "Bay Area conference transportation",
        "itemListElement": [
            {"@type": "ListItem", "position": i + 1, "url": SITE + "/events/" + ev["slug"], "name": ev["name"] + " Transportation"}
            for i, ev in enumerate(events)
        ],
    }
    body = f"""
<section class="ix-hero">
  <div class="ix-hero-bg"></div>
  <div class="ix-hero-inner">
    <div class="ev-crumbs"><a href="/index.html">Home</a><span>›</span><a href="/events-charter.html">Events &amp; Charter</a><span>›</span><span>Conference Transportation</span></div>
    <div class="ev-eyebrow"><i></i>Bay Area Conferences 2027</div>
    <h1>Big conference in town? <em>We'll get your people there.</em></h1>
    <p>When a big conference comes to San Francisco or San Jose, hotels fill up, traffic slows down, and rideshare prices jump. CLS plans hotel shuttles, airport pickups, VIP cars, and group charters so your team gets where it needs to be.</p>
    <div class="hero-cta-row">
      <a href="#events" class="btn-red-lg">See Upcoming Events</a>
      <a href="tel:6504608778" class="btn-ghost-light">Call 650.460.8778</a>
    </div>
    <div class="ix-stats">
      <div><strong>5,000+</strong><span>events managed</span></div>
      <div><strong>Since 2011</strong><span>in the Bay Area</span></div>
      <div><strong>24/7</strong><span>dispatch</span></div>
    </div>
  </div>
</section>

<section class="section" id="events">
  <div class="section-inner">
    <div class="section-label">Upcoming Events</div>
    <h2>The Bay Area's biggest conferences, coming up.</h2>
    <p class="section-sub">Pick your event to see the dates, the venue, and how we can help. Dates come from each organizer's website. CLS is an independent company and is not affiliated with these events.</p>
{group_html}
  </div>
</section>

<section class="section" style="background:var(--white);">
  <div class="section-inner">
    <div class="section-label">Why Book Early</div>
    <h2>Conference weeks fill up fast.</h2>
    <p class="section-sub">The teams that plan rides early get the vehicles, the times, and the prices they want.</p>
    <div class="reasons">
      <div class="reason"><strong>01</strong><h3>Hotels sell out</h3><p>Big events push guests to hotels across the Bay. A shuttle plan keeps a spread out team together.</p></div>
      <div class="reason"><strong>02</strong><h3>Rideshare gets pricey</h3><p>When thousands of people leave a venue at once, wait times and prices jump. Our pricing is fixed upfront.</p></div>
      <div class="reason"><strong>03</strong><h3>Vehicles book up</h3><p>Coaches and Sprinters are in demand during big conference weeks. Booking early locks in your vehicles.</p></div>
    </div>
  </div>
</section>

<div class="cta-strip" id="quote">
  <div class="cta-strip-inner">
    <div>
      <h2>Going to a conference that is not listed?</h2>
      <p>We move groups to events all over the Bay Area. Tell us the event, the dates, and your headcount.</p>
    </div>
    <a href="/charter-quote" class="btn-white-solid">Get an Event Quote</a>
  </div>
</div>
"""
    return head(title, desc, path, [item_list]) + nav('/charter-quote') + body + footer()


def faq_html(faqs):
    items = "\n".join(
        f"""      <div class="faq-item">
        <div class="faq-q">{e(q)} <span class="faq-icon">+</span></div>
        <div class="faq-a">{e(a)}</div>
      </div>"""
        for q, a in faqs
    )
    return f"""
<section class="section" style="background:var(--white);">
  <div class="section-inner" style="max-width:760px;">
    <div class="section-label">Common Questions</div>
    <h2>Things planners ask us.</h2>
    <div class="faq-list">
{items}
    </div>
  </div>
</section>
"""


def common_faqs(ev):
    return [
        (f"How early should we book transportation for {ev['short']}?",
         "As early as you can. Hotels, venues, and vehicles all get booked up during big conference weeks in the Bay Area. "
         "For groups of 100 or more, we suggest reaching out at least two to three months ahead. "
         "If you are closer than that, call us anyway and we will tell you what is open."),
        ("Can you run a shuttle loop between our hotel and the venue?",
         "Yes. We plan the loop around your session times, pick the right size vehicles, and put it in a written run plan before the event. "
         "Every vehicle is tracked live with GPS, and our dispatch team watches the whole thing."),
        ("Do you handle SFO, OAK, and SJC airport pickups?",
         "Yes. We can meet arriving guests, speakers, and executives at any Bay Area airport and bring them to their hotel or straight to the venue."),
        ("Is CLS the official transportation provider for this event?",
         f"No. CLS Global Transportation is an independent Bay Area transportation company. We are not affiliated with {ev['organizer']} or {ev['name']}. "
         "We work directly with companies, sponsors, and groups who are attending and need their own rides."),
        ("Can you provide a certificate of insurance for our venue?",
         "Yes. CLS carries full commercial insurance and can name your venue or company as an additional insured, often the same day you ask."),
    ]


def main():
    data = json.load(open(os.path.join(HERE, "events.json"), encoding="utf-8"))
    events = sorted(data["events"], key=lambda ev: ev["sort"])
    os.makedirs(OUT, exist_ok=True)
    for ev in events:
        with open(os.path.join(OUT, ev["slug"] + ".html"), "w", encoding="utf-8") as f:
            f.write(event_page(ev, events))
    with open(os.path.join(OUT, "index.html"), "w", encoding="utf-8") as f:
        f.write(index_page(events))
    print(f"Built {len(events)} event pages and the events index in /events")


if __name__ == "__main__":
    main()
