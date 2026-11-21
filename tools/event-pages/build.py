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
  .facts-grid { display:grid; grid-template-columns:repeat(4,1fr); gap:16px; margin-top:8px; }
  @media (max-width: 900px) { .facts-grid { grid-template-columns:repeat(2,1fr); } }
  @media (max-width: 520px) { .facts-grid { grid-template-columns:1fr; } }
  .fact { background:var(--gray-bg); border:1px solid var(--gray-light); border-radius:14px; padding:20px; }
  .fact-lbl { font-size:11px; font-weight:700; letter-spacing:0.1em; text-transform:uppercase; color:var(--gray-mid); margin-bottom:8px; }
  .fact-val { font-size:17px; font-weight:700; color:var(--black); line-height:1.35; }
  .fact-note { font-size:13px; color:var(--gray-mid); margin-top:6px; line-height:1.5; }
  .badge-unconfirmed { display:inline-block; font-size:11px; font-weight:700; color:#8a5a00; background:#fff4d6; border:1px solid #f1d58a; border-radius:50px; padding:3px 10px; margin-top:8px; }
  .event-note { font-size:13px; color:var(--gray-mid); margin-top:20px; line-height:1.6; }
  .event-note a { color:var(--gray-mid); }
  .plan-grid { display:grid; grid-template-columns:repeat(3,1fr); gap:16px; }
  @media (max-width: 900px) { .plan-grid { grid-template-columns:1fr; } }
  .plan-card { background:var(--white); border:1px solid var(--gray-light); border-radius:16px; padding:26px; }
  .plan-card h3 { font-size:18px; font-weight:700; margin-bottom:10px; letter-spacing:-0.01em; }
  .plan-card p { font-size:15px; color:var(--gray-mid); line-height:1.6; }
  .why-list { list-style:none; display:grid; grid-template-columns:1fr 1fr; gap:14px 32px; }
  @media (max-width: 760px) { .why-list { grid-template-columns:1fr; } }
  .why-list li { font-size:15px; color:var(--charcoal); line-height:1.55; padding-left:28px; position:relative; }
  .why-list li::before { content:"✓"; position:absolute; left:0; top:0; color:var(--red); font-weight:800; }
  .ev-quote-wrap { display:grid; grid-template-columns:1fr 1.1fr; gap:48px; align-items:start; }
  @media (max-width: 900px) { .ev-quote-wrap { grid-template-columns:1fr; gap:28px; } }
  .ev-quote-wrap h2 { margin-bottom:14px; }
  .ev-form { background:var(--white); border:1px solid var(--gray-light); border-radius:18px; padding:28px; display:flex; flex-direction:column; gap:12px; }
  .ev-form .form-row { display:grid; grid-template-columns:1fr 1fr; gap:12px; }
  @media (max-width: 520px) { .ev-form .form-row { grid-template-columns:1fr; } }
  .ev-form input, .ev-form select, .ev-form textarea { width:100%; font:inherit; font-size:15px; padding:13px 14px; border:1px solid var(--gray-light); border-radius:10px; background:var(--gray-bg); color:var(--black); }
  .ev-form textarea { min-height:96px; resize:vertical; }
  .ev-form input:focus, .ev-form select:focus, .ev-form textarea:focus { outline:2px solid rgba(196,30,30,0.35); border-color:var(--red); background:var(--white); }
  .ev-form button { background:var(--red); color:var(--white); font:inherit; font-size:15px; font-weight:700; padding:15px 28px; border:none; border-radius:50px; cursor:pointer; }
  .ev-form button:hover { background:var(--red-dark); }
  .ev-form .quote-note { font-size:13px; color:var(--gray-mid); }
  .ev-form .quote-note a { color:var(--black); }
  .ev-form .cls-form-status { font-size:14px; color:var(--black); }
  .ev-list { display:grid; grid-template-columns:repeat(2,1fr); gap:16px; }
  @media (max-width: 800px) { .ev-list { grid-template-columns:1fr; } }
  .ev-card { display:block; background:var(--white); border:1px solid var(--gray-light); border-radius:16px; padding:26px; text-decoration:none; color:var(--black); transition:border-color 0.15s, transform 0.15s; }
  .ev-card:hover { border-color:var(--red); transform:translateY(-2px); }
  .ev-card-date { font-size:12px; font-weight:700; letter-spacing:0.08em; text-transform:uppercase; color:var(--red); margin-bottom:10px; }
  .ev-card h3 { font-size:20px; font-weight:800; letter-spacing:-0.02em; margin-bottom:8px; }
  .ev-card p { font-size:14px; color:var(--gray-mid); line-height:1.55; }
  .ev-card-more { display:inline-block; margin-top:14px; font-size:14px; font-weight:700; color:var(--black); }
  @media (max-width: 960px) {
    .nav-links, .nav-right { display:none; }
    .nav-hamburger { display:flex; }
    .page-hero { padding:56px 24px 64px; }
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
    "email": "res@clsgt.com",
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


def nav():
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
    <a href="#quote" class="btn-red">Get a Quote</a>
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
  <a href="#quote" class="mobile-cta">Get a Quote</a>
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
        <a href="mailto:res@clsgt.com">res@clsgt.com</a>
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


def quote_form(ev):
    """Same form name and fields as the charter form on the home page, so
    entries land in the same Netlify form and Slack channel. The label names the event."""
    label = f"Event quote: {ev['name']}"
    date_val = ev.get("start_date") if ev.get("dates_confirmed") else ""
    return f"""
<section class="section" id="quote" style="background:var(--gray-bg);">
  <div class="section-inner">
    <div class="ev-quote-wrap">
      <div>
        <div class="section-label">Get a Quote</div>
        <h2>Planning transportation for {e(ev['short'])}?</h2>
        <p class="section-sub">Tell us your dates, how many people, and where they need to go. We will send back a plan and a price, usually within 24 hours.</p>
        <ul class="why-list" style="grid-template-columns:1fr; margin-top:8px;">
          <li>Hotel shuttles, airport runs, and dinner transfers in one plan</li>
          <li>Fixed pricing quoted upfront, no surge pricing</li>
          <li>Certificate of insurance for your venue, often the same day</li>
          <li>One direct dispatch number, open 24/7</li>
        </ul>
      </div>
      <form class="ev-form" name="charter-quote" method="POST" data-netlify="true" netlify-honeypot="bot-field" onsubmit="return clsSendForm(event);">
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
        <p class="quote-note">Prefer to talk? Call or text <a href="tel:6504608778">650.460.8778</a> or email <a href="mailto:res@clsgt.com">res@clsgt.com</a>.</p>
      </form>
    </div>
  </div>
</section>
"""


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


def event_page(ev, all_events):
    path = f"/events/{ev['slug']}"
    title = f"{ev['name']} Transportation: Shuttles, Airport and Car Service | CLS"
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
    faqs = ev.get("faqs", []) + common_faqs(ev)
    faq_ld = {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faqs
        ],
    }

    badge = "" if ev["dates_confirmed"] else '<div class="badge-unconfirmed">Not yet confirmed by the organizer</div>'
    facts = f"""
    <div class="facts-grid">
      <div class="fact"><div class="fact-lbl">Dates</div><div class="fact-val">{e(ev['dates_text'])}</div>{badge}</div>
      <div class="fact"><div class="fact-lbl">Venue</div><div class="fact-val">{e(ev['venue'])}</div><div class="fact-note">{e(ev['city'])}</div></div>
      <div class="fact"><div class="fact-lbl">Crowd size</div><div class="fact-val">{e(ev['attendance'])}</div><div class="fact-note">{e(ev.get('attendance_note',''))}</div></div>
      <div class="fact"><div class="fact-lbl">Hosted by</div><div class="fact-val">{e(ev['organizer'])}</div></div>
    </div>
    <p class="event-note">Event details come from the organizer's website, <a href="{e(ev['official_url'])}" rel="nofollow noopener" target="_blank">{e(ev['official_label'])}</a>. Please check there for the latest. CLS Global Transportation is an independent company and is not affiliated with or endorsed by {e(ev['organizer'])}.</p>
"""
    plans = "\n".join(
        f'      <div class="plan-card"><h3>{e(h)}</h3><p>{e(p)}</p></div>' for h, p in ev["plans"]
    )
    others = [o for o in all_events if o["slug"] != ev["slug"]][:4]
    other_cards = "\n".join(
        f"""      <a class="ev-card" href="/events/{o['slug']}"><div class="ev-card-date">{e(o['dates_text'])}</div><h3>{e(o['name'])}</h3><p>{e(o['venue'])}, {e(o['city'])}</p><span class="ev-card-more">Transportation for {e(o['short'])} ›</span></a>"""
        for o in others
    )

    body = f"""
<section class="page-hero">
  <div class="page-hero-inner">
    <div class="breadcrumb">
      <a href="/index.html">Home</a><span>›</span>
      <a href="/events/">Conference Transportation</a><span>›</span>
      <span>{e(ev['short'])}</span>
    </div>
    <div class="page-hero-tag">{e(ev['tag'])}</div>
    <h1>{e(ev['h1'])}</h1>
    <p>{e(ev['intro'])}</p>
    <div class="hero-cta-row">
      <a href="#quote" class="btn-red-lg">Get a Quote for {e(ev['short'])}</a>
      <a href="tel:6504608778" class="btn-ghost-light">Call 650.460.8778</a>
    </div>
  </div>
</section>

<section class="section" style="background:var(--white);">
  <div class="section-inner">
    <div class="section-label">About the Event</div>
    <h2>{e(ev['name'])} at a glance</h2>
{facts}
  </div>
</section>

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
    <div class="section-label">Why CLS</div>
    <h2>A Bay Area company that has done this since 2011.</h2>
    <ul class="why-list">
      <li>Bay Area based since 2011, with more than 5,000 events managed</li>
      <li>Our own employee drivers, not gig drivers or subcontractors</li>
      <li>Live GPS tracking on every vehicle</li>
      <li>Written run plan before your event, and dispatch open 24/7</li>
      <li>Sedans, SUVs, Sprinters, limo buses, mini coaches, and full motorcoaches</li>
      <li>ADA accessible coaches when you need them</li>
    </ul>
  </div>
</section>
{faq_html(faqs)}
{quote_form(ev)}
<section class="section" style="background:var(--white);">
  <div class="section-inner">
    <div class="section-label">More Bay Area Events</div>
    <h2>Other big conferences we can help with.</h2>
    <div class="ev-list">
{other_cards}
    </div>
    <p class="event-note"><a href="/events/">See all upcoming Bay Area conferences</a></p>
  </div>
</section>
"""
    return head(title, desc, path, [crumbs, service, faq_ld]) + nav() + body + footer()


def index_page(events):
    path = "/events/"
    title = "Bay Area Conference Transportation 2027: Shuttles and Car Service | CLS"
    desc = ("Transportation for the biggest San Francisco and Bay Area conferences in 2027. "
            "Hotel shuttles, airport pickups, VIP cars, and group charters from CLS Global Transportation.")
    cards = "\n".join(
        f"""      <a class="ev-card" href="/events/{ev['slug']}"><div class="ev-card-date">{e(ev['dates_text'])}{'' if ev['dates_confirmed'] else ' (expected)'}</div><h3>{e(ev['name'])}</h3><p>{e(ev['venue'])}, {e(ev['city'])}. {e(ev['card_line'])}</p><span class="ev-card-more">Transportation for {e(ev['short'])} ›</span></a>"""
        for ev in events
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
<section class="page-hero">
  <div class="page-hero-inner">
    <div class="breadcrumb">
      <a href="/index.html">Home</a><span>›</span>
      <a href="/events-charter.html">Events &amp; Charter</a><span>›</span>
      <span>Conference Transportation</span>
    </div>
    <div class="page-hero-tag">Bay Area Conferences 2027</div>
    <h1>Getting your team to the Bay Area's biggest conferences.</h1>
    <p>When a big conference comes to San Francisco or San Jose, hotels fill up, traffic slows down, and rideshare prices jump. CLS plans hotel shuttles, airport pickups, VIP cars, and group charters so your people get where they need to be.</p>
    <div class="hero-cta-row">
      <a href="#quote" class="btn-red-lg">Get an Event Quote</a>
      <a href="tel:6504608778" class="btn-ghost-light">Call 650.460.8778</a>
    </div>
  </div>
</section>

<section class="section" style="background:var(--white);">
  <div class="section-inner">
    <div class="section-label">Upcoming Events</div>
    <h2>Big Bay Area conferences coming up.</h2>
    <p class="section-sub">Pick your event to see dates, the venue, and how we can help. Dates come from each organizer's website. CLS is an independent company and is not affiliated with these events.</p>
    <div class="ev-list">
{cards}
    </div>
  </div>
</section>

<div class="cta-strip" id="quote">
  <div class="cta-strip-inner">
    <div>
      <h2>Going to a conference that is not listed?</h2>
      <p>We move groups to events all over the Bay Area. Tell us the event, the dates, and your headcount.</p>
    </div>
    <a href="/index.html#quote" class="btn-white-solid">Get an Event Quote</a>
  </div>
</div>
"""
    return head(title, desc, path, [item_list]) + nav() + body + footer()


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
