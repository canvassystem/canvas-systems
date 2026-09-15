#!/usr/bin/env python3
"""
Canvas Systems site builder.

Generates every .html page in this folder from the shared header/footer defined
here plus the per-page content below. The output is plain static HTML — you can
edit the generated files directly and never run this again, but if you change
the nav, footer or contact details, edit them HERE and re-run:

    python3 build.py

Styling lives in assets/css/style.css, behaviour in assets/js/main.js.
"""

import re
from pathlib import Path

ROOT = Path(__file__).parent

# --------------------------------------------------------------------------
# Company details — single source of truth. Change once, rebuild.
# --------------------------------------------------------------------------
EMAIL = "info@canvassystems.om"
PHONE_DISPLAY = "+91 85475 41134"
PHONE_HREF = "+918547541134"
WHATSAPP = "918547541134"
HQ = "Kannur, Kerala, India"
BRANCHES = "Muscat, Oman &middot; Doha, Qatar"
# Contact-form submissions are emailed to this address via formsubmit.co.
# ONE-TIME SETUP: the first submission triggers an "Activate Form" email to
# this inbox — click the link in it once, then every enquiry arrives by email.
FORM_TO = "testm8667@gmail.com"

SERVICE_PAGES = [
    ("implementation.html", "Odoo Implementation"),
    ("customization.html", "Odoo Customization"),
    ("migration.html", "Data Migration &amp; Version Upgrades"),
    ("integration.html", "Odoo Integrations"),
    ("training.html", "Training &amp; User Adoption"),
    ("support.html", "Support &amp; AMC"),
]

# --------------------------------------------------------------------------
# Shared chrome
# --------------------------------------------------------------------------
LOGO = """<a href="index.html" class="logo">
      <span class="logo-mark"><svg viewBox="0 0 24 24" fill="none"><path d="M4 12L10 18L20 6" stroke="#fff" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"/></svg></span>
      <span>Canvas Systems<small>Odoo ERP Partner</small></span>
    </a>"""

IC_MAIL = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M3 6l9 7 9-7M3 6v12h18V6H3z"/></svg>'
IC_PHONE = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M22 16.9v3a2 2 0 01-2.2 2 19.8 19.8 0 01-8.6-3 19.5 19.5 0 01-6-6 19.8 19.8 0 01-3-8.7A2 2 0 014.2 2h3a2 2 0 012 1.7c.1.9.3 1.8.6 2.7a2 2 0 01-.5 2.1L8 9.9a16 16 0 006 6l1.4-1.4a2 2 0 012.1-.5c.9.3 1.8.5 2.7.6a2 2 0 011.8 2.3z"/></svg>'
IC_PIN = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 10c0 6-9 12-9 12s-9-6-9-12a9 9 0 0118 0z"/><circle cx="12" cy="10" r="3"/></svg>'
IC_CLOCK = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/></svg>'
IC_WA = '<svg viewBox="0 0 24 24" fill="currentColor"><path d="M12 2a10 10 0 00-8.6 15L2 22l5.2-1.4A10 10 0 1012 2zm5.5 14.1c-.2.6-1.2 1.2-1.7 1.2-.5.1-1 .1-1.6-.1-.4-.1-.9-.3-1.5-.6a11 11 0 01-4.2-3.9c-.3-.5-.7-1.2-.7-2s.4-1.2.6-1.4c.2-.2.4-.3.6-.3h.4c.1 0 .3 0 .5.4l.7 1.6c.1.1.1.3 0 .4l-.2.4-.3.3c-.1.1-.2.2-.1.4a6.6 6.6 0 003 2.6c.2.1.4.1.5-.1l.6-.7c.1-.2.3-.2.5-.1l1.6.8c.2.1.4.2.4.3s0 .5-.1.8z"/></svg>'
IC_LI = '<svg viewBox="0 0 24 24" fill="currentColor"><path d="M4.98 3.5a2.5 2.5 0 100 5 2.5 2.5 0 000-5zM3 9h4v12H3zM10 9h3.8v1.7h.05c.53-1 1.83-2.05 3.75-2.05C21.4 8.65 22 11 22 14.2V21h-4v-6c0-1.43-.03-3.27-2-3.27-2 0-2.3 1.56-2.3 3.17V21h-4z"/></svg>'


def head(title, desc, active, body_class=""):
    cls = f' class="{body_class}"' if body_class else ""
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title}</title>
<meta name="description" content="{desc}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:type" content="website">
<meta name="theme-color" content="#14304F">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Sora:wght@500;600;700;800&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="assets/css/style.css">
</head>
<body data-page="{active}"{cls}>

<a href="#main" class="skip">Skip to content</a>

<div class="announce">
  <div class="wrap">
    <span class="msg">Get a 30-minute Odoo assessment for your business.</span>
    <a href="contact.html" class="try">Book now</a>
  </div>
</div>

<header>
  <nav class="nav">
    {LOGO}
    <div class="nav-links centered" id="navLinks">
      <div class="nav-item{' active' if active in ('services', 'service') else ''}">
        <button type="button" aria-expanded="false">Services</button>
        <div class="dropdown">
          <div class="dropdown-title">Odoo services</div>
          <a href="services.html"><strong>All services</strong><span>The full delivery lifecycle</span></a>
          <a href="implementation.html"><strong>Implementation</strong><span>End-to-end ERP rollout</span></a>
          <a href="customization.html"><strong>Customization</strong><span>Modules built to your process</span></a>
          <a href="migration.html"><strong>Migration &amp; upgrades</strong><span>Move your data and version</span></a>
          <a href="integration.html"><strong>Integrations</strong><span>Connect your other systems</span></a>
          <a href="training.html"><strong>Training</strong><span>Get your team using it</span></a>
          <a href="support.html"><strong>Support &amp; AMC</strong><span>SLAs after go-live</span></a>
        </div>
      </div>
      <div class="nav-item{' active' if active in ('modules', 'pricing', 'comparisons') else ''}">
        <button type="button" aria-expanded="false">Odoo</button>
        <div class="dropdown">
          <div class="dropdown-title">Explore Odoo</div>
          <a href="modules.html"><strong>Modules</strong><span>Apps we implement</span></a>
          <a href="pricing.html"><strong>Pricing</strong><span>Packages and licensing</span></a>
          <a href="comparisons.html"><strong>Comparisons</strong><span>Odoo vs SAP, NetSuite, Zoho</span></a>
        </div>
      </div>
      <a href="industries.html"{' class="active"' if active == 'industries' else ''}>Industries</a>
      <a href="about.html"{' class="active"' if active == 'about' else ''}>About</a>
      <a href="contact.html"{' class="active"' if active == 'contact' else ''}>Contact</a>
    </div>
    <div class="nav-actions">
      <a href="tel:{PHONE_HREF}" class="btn btn-primary btn-sm">Call us</a>
    </div>
    <button class="nav-toggle" id="navToggle" aria-label="Toggle menu" aria-expanded="false" aria-controls="navLinks">
      <span></span><span></span><span></span>
    </button>
  </nav>
</header>

<div class="bg-anim" aria-hidden="true"><span></span><span></span><span></span><span></span></div>

<main id="main">
"""


FOOTER = f"""
</main>

<footer>
  <div class="wrap">
    <div class="footer-top">
      <div class="footer-brand">
        {LOGO}
        <p>Odoo ERP implementation, customization, integration, training and support for businesses worldwide. Headquartered in {HQ}, with branch offices in Oman and Qatar, delivering remotely and on-site across the GCC, Africa, Europe and Asia.</p>
        <div class="footer-social">
          <a href="#" aria-label="LinkedIn">{IC_LI}</a>
          <a href="https://wa.me/{WHATSAPP}" aria-label="WhatsApp" target="_blank" rel="noopener">{IC_WA}</a>
          <a href="mailto:{EMAIL}" aria-label="Email">{IC_MAIL}</a>
        </div>
      </div>
      <div class="footer-col">
        <h5>Services</h5>
        <a href="implementation.html">Implementation</a>
        <a href="customization.html">Customization</a>
        <a href="migration.html">Migration &amp; upgrades</a>
        <a href="integration.html">Integrations</a>
        <a href="training.html">Training</a>
        <a href="support.html">Support &amp; AMC</a>
      </div>
      <div class="footer-col">
        <h5>Odoo</h5>
        <a href="modules.html">Modules</a>
        <a href="pricing.html">Pricing</a>
        <a href="comparisons.html">Comparisons</a>
        <a href="industries.html">Industries</a>
        <a href="services.html">All services</a>
      </div>
      <div class="footer-col">
        <h5>Company</h5>
        <a href="about.html">About us</a>
        <a href="about.html#methodology">Methodology</a>
        <a href="about.html#faq">FAQ</a>
        <a href="contact.html">Contact</a>
      </div>
      <div class="footer-col">
        <h5>Contact</h5>
        <a href="mailto:{EMAIL}">{EMAIL}</a>
        <a href="tel:{PHONE_HREF}">{PHONE_DISPLAY}</a>
        <p>Head office: {HQ}</p>
        <p>Branches: {BRANCHES}</p>
        <p>Sunday–Thursday<br>8:30–17:30 GST</p>
      </div>
    </div>
    <div class="footer-bottom">
      <span>&copy; <span id="year">2026</span> Canvas Systems. All rights reserved.</span>
      <span>Odoo is a trademark of Odoo S.A. &middot; Canvas Systems is an independent implementation partner.</span>
    </div>
  </div>
</footer>

<a class="wa" href="https://wa.me/{WHATSAPP}" aria-label="Chat on WhatsApp" target="_blank" rel="noopener">{IC_WA}</a>

<script src="assets/js/main.js"></script>
</body>
</html>
"""


def page_hero(crumb, eyebrow, h1, sub, ctas=True):
    crumbs = '<a href="index.html">Home</a><span>/</span>' + crumb
    cta_html = """
      <div class="hero-ctas">
        <a href="contact.html" class="btn btn-white">Get your free assessment</a>
        <a href="services.html" class="btn btn-ghost">All services</a>
      </div>""" if ctas else ""
    return f"""
  <section class="page-hero">
    <div class="wrap">
      <div class="crumbs">{crumbs}</div>
      <div class="eyebrow">{eyebrow}</div>
      <h1>{h1}</h1>
      <p>{sub}</p>{cta_html}
    </div>
  </section>
"""


CTA_BANNER = """
  <section>
    <div class="cta-banner reveal">
      <div>
        <h2>Ready to see what Odoo can do for your business?</h2>
        <p>Book a free 30-minute assessment. We'll review your current systems and come back with a scoped module list, timeline and indicative investment.</p>
      </div>
      <div class="cta-actions">
        <a href="contact.html" class="btn btn-white">Get your free assessment</a>
        <a href="mailto:%s" class="btn btn-ghost">Email us</a>
      </div>
    </div>
  </section>
""" % EMAIL


def sidebar(related, note_title="Not sure where to start?",
            note="A 30-minute call is usually enough to tell you whether Odoo fits, which modules you need, and roughly what it costs."):
    links = "\n        ".join(f'<a href="{h}">{t}</a>' for h, t in related)
    return f"""<aside class="sidebar">
      <div class="side-card dark">
        <h4>{note_title}</h4>
        <p>{note}</p>
        <a href="contact.html" class="btn btn-white">Book a free assessment</a>
      </div>
      <div class="side-card">
        <h4>Related services</h4>
        <div class="side-links">
        {links}
        </div>
      </div>
      <div class="side-card">
        <h4>Talk to a consultant</h4>
        <p>Prefer to speak to someone directly? We reply within one business day.</p>
        <a href="mailto:{EMAIL}" class="btn btn-outline">{EMAIL}</a>
      </div>
    </aside>"""


# --------------------------------------------------------------------------
# Reusable content blocks
# --------------------------------------------------------------------------
MODULES = [
    ("Accounting &amp; Finance", "M12 2v20M17 5H9.5a3.5 3.5 0 000 7h5a3.5 3.5 0 010 7H6",
     "Chart of accounts, tax and VAT/GST filing, bank reconciliation, multi-currency and consolidated financial reports.", ""),
    ("Inventory", "M21 16V8l-9-5-9 5v8l9 5 9-5z",
     "Multi-warehouse, stock valuation, barcode scanning, lot and serial tracking, and automated reordering rules.", ""),
    ("Sales", "M3 3h2l2.6 12.4a2 2 0 002 1.6h7.7a2 2 0 002-1.6L21 7H6",
     "Quotation templates, sales orders, customer portal, price lists and invoicing for a faster order-to-cash cycle.", ""),
    ("Purchase", "M4 7h16v14H4zM9 3h6l1 4H8l1-4z",
     "RFQs, purchase orders, vendor price lists, and 3-way matching that keeps procurement costs under control.", ""),
    ("CRM", "M3 3v18h18M7 15l4-5 3 3 5-7",
     "Lead capture and scoring, pipeline stages, email and calendar integration, and forecast dashboards.", ""),
    ("Human Resources", "M5 21c0-4 3-6.5 7-6.5S19 17 19 21",
     "Employee records, recruitment, leave and attendance, appraisals, expenses, and country-specific payroll.", ""),
    ("Manufacturing", "M3 21V10l6-3v3l6-3v3l6-3v13H3z",
     "Bills of materials, routings, work orders, MRP scheduling, subcontracting and quality control points.", "Optional"),
    ("Point of Sale", "M3 4h18v12H3zM7 20h10M12 16v4",
     "Retail and restaurant POS with offline mode, loyalty programs, and live sync to inventory and accounting.", "Optional"),
    ("eCommerce &amp; Website", "M4 5h16v14H4zM4 9h16",
     "Storefront, product catalogue, payment providers and shipping connectors sharing one product and stock database.", "Optional"),
    ("Project &amp; Timesheets", "M4 5h16v14H4zM9 19V9",
     "Task planning, timesheets, billable rates and project costing — margin visibility on every job you deliver.", "Optional"),
    ("Field Service", "M3 16V6h11v10M14 10h4l3 3v3h-7",
     "Scheduling, dispatch, mobile worksheets and on-site invoicing for teams working away from the office.", "Optional"),
    ("Maintenance &amp; Quality", "M12 2l2.4 6.6L21 11l-6.6 2.4L12 20l-2.4-6.6L3 11l6.6-2.4L12 2z",
     "Preventive maintenance calendars, equipment records, and quality checks embedded in production flows.", "Optional"),
]


def modules_grid(limit=None):
    items = MODULES[:limit] if limit else MODULES
    out = []
    for name, path, desc, opt in items:
        opt_html = f'<span class="opt">{opt}</span>' if opt else ""
        out.append(f"""        <div class="mod">
          <div class="mod-head"><span class="ic"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="{path}"/></svg></span><h3>{name}</h3>{opt_html}</div>
          <p>{desc}</p>
        </div>""")
    return "\n".join(out)


INDUSTRIES = [
    ("Trading &amp; Distribution", "M3 21h18M5 21V7l7-4 7 4v14M9 21v-6h6v6", "Multi-warehouse stock, landed costs, price lists"),
    ("Manufacturing", "M3 21V10l6-3v3l6-3v3l6-3v13H3z", "BOMs, work orders, MRP, quality checks"),
    ("Retail &amp; Wholesale", "M3 9l1-5h16l1 5M4 9v11h16V9M4 9h16", "POS tied to live inventory and accounting"),
    ("Construction &amp; Real Estate", "M2 20h20M6 20V9l6-5 6 5v11M10 20v-5h4v5", "Project costing, subcontractors, retentions"),
    ("Logistics &amp; Transport", "M3 16V6h11v10M14 10h4l3 3v3h-7", "Fleet, dispatch, delivery cost tracking"),
    ("eCommerce", "M6 2l1.5 4h9L18 2M3 6h18l-2 12H5L3 6z", "Storefront, stock and finance on one database"),
    ("Healthcare &amp; Pharma", "M12 6v12M6 12h12", "Batch and expiry tracking, compliance records"),
    ("Education", "M12 3L2 8l10 5 10-5-10-5zM6 11v5l6 3 6-3v-5", "Admissions, fees, staff and asset management"),
    ("Hospitality &amp; Restaurants", "M6 3v8a3 3 0 006 0V3M9 11v10M17 3v18", "Restaurant POS, recipes, purchasing"),
    ("Professional Services", "M9 3h6l1 4H8l1-4zM4 7h16v14H4z", "Timesheets, billing, project profitability"),
    ("Oil, Gas &amp; Energy", "M12 3c3 4 5 6.5 5 9.5A5 5 0 017 12.5C7 9.5 9 7 12 3z", "Asset maintenance, contracts, HSE records"),
    ("Automotive &amp; Workshops", "M5 16V9h14v7M7 16v3M17 16v3", "Job cards, spare parts, service history"),
]


def industries_grid(limit=None):
    items = INDUSTRIES[:limit] if limit else INDUSTRIES
    out = []
    for name, path, sub in items:
        out.append(f"""        <a class="industry-card" href="contact.html">
          <div class="icon"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><path d="{path}"/></svg></div>
          <span>{name}</span>
          <small>{sub}</small>
        </a>""")
    return "\n".join(out)


PROCESS_STEPS = [
    ("1", "Week 1–2", "Discovery &amp; requirements",
     "Kick-off with stakeholders from every department, Business Process Review workshops, and a gap analysis against standard Odoo workflows.",
     "Deliverable: signed-off BRD"),
    ("2", "Week 3–6", "Configuration &amp; customization",
     "Environment setup, all modules configured to the BRD, language, currency and tax setup, chart of accounts, and branded invoices, quotations and POs.",
     "Milestone: configured system demo"),
    ("3", "Week 5–7", "Data migration",
     "Extraction templates for customers, suppliers, products and opening balances, then cleansing, validation and a pilot migration for your review.",
     "Milestone: data sign-off"),
    ("4", "Week 7–8", "User acceptance testing",
     "End-to-end testing of every configured workflow with your team, issues and gaps resolved, and formal client sign-off on UAT completion.",
     "Milestone: UAT sign-off"),
    ("5", "Week 8–9", "Training",
     "Role-based training for Finance, Sales, Inventory, HR and Management, train-the-trainer sessions, and hands-on practice on the staging environment.",
     "Deliverable: user manuals"),
    ("6", "Week 10–12", "Go-live &amp; hypercare",
     "Final data migration and cutover with our consultants alongside your team, then a four-week hypercare period and a post go-live optimization review.",
     "Outcome: live system + 4-week support"),
]


def process_track():
    out = []
    for num, week, title, body, deliv in PROCESS_STEPS:
        out.append(f"""        <div class="process-step">
          <div class="num">{num}</div>
          <div class="week">{week}</div>
          <h4>{title}</h4>
          <p>{body}</p>
          <div class="deliv">{deliv}</div>
        </div>""")
    return "\n".join(out)


AMC_PLANS = """
      <div class="plan-grid reveal">
        <div class="plan">
          <h3>Basic AMC</h3>
          <div class="sla">Response within 48 hours</div>
          <ul>
            <li><span class="tick">&#10003;</span> Email support during business hours</li>
            <li><span class="tick">&#10003;</span> Bug fixes and patches</li>
            <li><span class="tick">&#10003;</span> Odoo version updates</li>
          </ul>
          <a href="contact.html" class="btn btn-outline">Enquire</a>
        </div>
        <div class="plan featured">
          <h3>Standard AMC</h3>
          <div class="sla">Response within 24 hours</div>
          <ul>
            <li><span class="tick">&#10003;</span> Email and phone support</li>
            <li><span class="tick">&#10003;</span> Bug fixes plus minor enhancements</li>
            <li><span class="tick">&#10003;</span> Version updates with regression testing</li>
          </ul>
          <a href="contact.html" class="btn btn-primary">Enquire</a>
        </div>
        <div class="plan">
          <h3>Premium AMC</h3>
          <div class="sla">4-hour response SLA</div>
          <ul>
            <li><span class="tick">&#10003;</span> Dedicated account manager</li>
            <li><span class="tick">&#10003;</span> Priority bug fixes and enhancements</li>
            <li><span class="tick">&#10003;</span> Full upgrade management</li>
          </ul>
          <a href="contact.html" class="btn btn-outline">Enquire</a>
        </div>
      </div>
"""

""" Big gradient service panels stacked down the home page. """
PANELS = [
    ("p-magenta", "implementation.html", "Odoo", "Implementation",
     "A full six-phase rollout, from process workshops through to cutover, with a sign-off gate at every stage.",
     "M4 6h16M4 12h16M4 18h10", [1, 0, 0]),
    ("p-ocean", "customization.html", "Odoo", "Customization",
     "Custom modules built as separate, upgrade-safe code — never as edits to the Odoo core.",
     "M12 2l2.4 6.6L21 11l-6.6 2.4L12 20l-2.4-6.6L3 11l6.6-2.4L12 2z", [0, 1, 0]),
    ("p-violet", "migration.html", "Odoo", "Migration &amp; Upgrades",
     "Your records cleansed, mapped and pilot-loaded. Nothing goes live until the balances reconcile.",
     "M4 16l4-4 4 4 8-8M16 8h4v4", [0, 0, 1]),
    ("p-ember", "integration.html", "Odoo", "Integration",
     "Banks, payment gateways, marketplaces and tax portals connected to Odoo — and monitored after launch.",
     "M9.5 14.5l5-5M10.5 7.5l1.8-1.8a4 4 0 015.7 5.7l-1.8 1.8M13.5 16.5l-1.8 1.8a4 4 0 01-5.7-5.7l1.8-1.8", [1, 0, 1]),
    ("p-forest", "training.html", "Odoo", "Training",
     "Role-by-role training on your own data, with written manuals your team will actually open.",
     "M6.5 2H20v20H6.5A2.5 2.5 0 014 19.5v-15A2.5 2.5 0 016.5 2z", [0, 1, 1]),
    ("p-slate", "support.html", "Odoo", "Support &amp; AMC",
     "Four weeks of hypercare included, then an AMC ranging from 48-hour cover to a 4-hour SLA.",
     "M12 22a10 10 0 100-20 10 10 0 000 20zM9.1 9a3 3 0 015.8 1c0 2-3 3-3 3M12 17h.01", [1, 1, 0]),
]


# Panels that show a photo on the right instead of the abstract UI art.
PANEL_PHOTOS = {
    "implementation.html": "assets/img/implementation.png",
    "customization.html": "assets/img/customization.jpeg",
    "migration.html": "assets/img/migration.jpg",
    "integration.html": "assets/img/integration.jpg",
    "training.html": "assets/img/training.jpg",
    "support.html": "assets/img/support.jpg",
}


def photo_or_art(href, icon, tile_html):
    """Right-hand visual for a panel: a photo where we have one, else UI art."""
    photo = PANEL_PHOTOS.get(href)
    if photo:
        return f"""        <div class="panel-photo">
          <img src="{photo}" alt="" loading="lazy">
        </div>"""
    return f"""        <div class="panel-art" aria-hidden="true">
          <div class="art-icon"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="{icon}"/></svg></div>
          <div class="art-row m"></div>
          <div class="art-row"></div>
          <div class="art-row s"></div>
          <div class="art-tiles">{tile_html}</div>
        </div>"""


def panels():
    out = []
    for cls, href, kicker, title, copy, icon, tiles in PANELS:
        tile_html = "".join(
            f'<div class="art-tile{" on" if t else ""}"></div>' for t in tiles)
        out.append(f"""      <div class="panel {cls} reveal">
        <div>
          <div class="kicker">{kicker}</div>
          <h2>{title}</h2>
          <p>{copy}</p>
          <a href="{href}" class="btn-pill">Odoo {title}</a>
        </div>
{photo_or_art(href, icon, tile_html)}
      </div>""")
    return "\n".join(out)


CONTACT_FORM = f"""<form id="contactForm" class="reveal" method="POST" action="https://formsubmit.co/{FORM_TO}" novalidate>
        <input type="hidden" name="_subject" value="New enquiry — Canvas Systems website">
        <input type="hidden" name="_template" value="table">
        <input type="hidden" name="_captcha" value="false">
        <input type="text" name="_honey" style="display:none" tabindex="-1" autocomplete="off" aria-hidden="true">
        <h3>Request your free assessment</h3>
        <p class="form-sub">Free consultation &middot; No obligation &middot; Reply within one business day</p>
        <div class="row-2">
          <div class="field"><label for="name">Full name *</label><input type="text" id="name" name="name" autocomplete="name" required></div>
          <div class="field"><label for="company">Company *</label><input type="text" id="company" name="company" autocomplete="organization" required></div>
        </div>
        <div class="row-2">
          <div class="field"><label for="email">Work email *</label><input type="email" id="email" name="email" autocomplete="email" required></div>
          <div class="field"><label for="phone">Phone / WhatsApp</label><input type="tel" id="phone" name="phone" autocomplete="tel"></div>
        </div>
        <div class="row-2">
          <div class="field"><label for="country">Country</label><input type="text" id="country" name="country" autocomplete="country-name" placeholder="Where are you based?"></div>
          <div class="field">
            <label for="industry">Industry</label>
            <select id="industry" name="industry">
              <option>Trading &amp; Distribution</option>
              <option>Manufacturing</option>
              <option>Retail &amp; Wholesale</option>
              <option>Construction &amp; Real Estate</option>
              <option>Logistics &amp; Transport</option>
              <option>eCommerce</option>
              <option>Healthcare &amp; Pharma</option>
              <option>Education</option>
              <option>Hospitality &amp; Restaurants</option>
              <option>Professional Services</option>
              <option>Oil, Gas &amp; Energy</option>
              <option>Automotive &amp; Workshops</option>
              <option>Other</option>
            </select>
          </div>
        </div>
        <div class="row-2">
          <div class="field">
            <label for="users">Expected Odoo users</label>
            <select id="users" name="users">
              <option>1–10 users</option>
              <option>11–25 users</option>
              <option>26–50 users</option>
              <option>51–100 users</option>
              <option>100+ users</option>
            </select>
          </div>
          <div class="field">
            <label for="current">What are you running today?</label>
            <select id="current" name="current">
              <option>Manual processes / spreadsheets</option>
              <option>Legacy accounting software</option>
              <option>Separate systems per department</option>
              <option>Another ERP we want to move off</option>
              <option>Already on Odoo — need support</option>
            </select>
          </div>
        </div>
        <div class="field"><label for="message">What are you looking to do with Odoo? *</label><textarea id="message" name="message" required></textarea></div>
        <button type="submit" class="btn btn-primary" style="width:100%;">Send message</button>
        <p class="form-note">Your details are used only to respond to this enquiry and are never shared.</p>
        <p class="form-success" id="formSuccess" role="status">Message sent — we'll be in touch within one business day.</p>
        <p class="form-error" id="formError" role="alert">Couldn't send your message. Please try again, or email us directly at <a href="mailto:{EMAIL}">{EMAIL}</a>.</p>
      </form>"""


# ==========================================================================
# PAGES
# ==========================================================================
PAGES = {}

# ---------------------------------------------------------------- HOME ----
PAGES["index.html"] = dict(
    title="Canvas Systems | Odoo ERP Implementation Partner",
    desc="Canvas Systems implements, customizes and supports Odoo ERP for businesses worldwide. Implementation, migration, integration, training and AMC support. Live in 10–12 weeks.",
    active="home",
    # Light background, like the rest of the site. The dark theme is still in
    # style.css — set body_class="theme-dark" here to switch back.
    body_class="",
    body=f"""
  <section class="hero">
    <div class="hero-dash" aria-hidden="true">
      <div class="mockup">
        <div class="mockup-bar"><span></span><span></span><span></span></div>
        <div class="mockup-body">
          <div class="mockup-side">
            <div class="side-logo"></div>
            <i class="on"></i><i></i><i></i><i></i><i></i>
          </div>
          <div class="mockup-main">
            <div class="mockup-stats">
              <div class="mockup-stat"><div class="label">Open orders</div><div class="value">128</div></div>
              <div class="mockup-stat"><div class="label">Revenue MTD</div><div class="value up">+18%</div></div>
              <div class="mockup-stat"><div class="label">Stock alerts</div><div class="value">3</div></div>
            </div>
            <div class="mockup-chart">
              <div class="mockup-chart-head"><span class="t">Sales pipeline</span><span class="t">This quarter</span></div>
              <div class="bars">
                <i style="height:40%; animation-delay:.05s"></i>
                <i style="height:65%; animation-delay:.12s"></i>
                <i style="height:48%; animation-delay:.19s"></i>
                <i style="height:80%; animation-delay:.26s"></i>
                <i style="height:58%; animation-delay:.33s"></i>
                <i style="height:92%; animation-delay:.40s"></i>
                <i style="height:70%; animation-delay:.47s"></i>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
    <div class="wrap-wide hero-solo">
      <h1>Run your entire business on <span class="accent">one Odoo system.</span></h1>
      <p class="sub">One platform. Every department.</p>
      <div class="hero-ctas">
        <a href="contact.html" class="btn btn-primary">Get your free ERP assessment <span class="btn-icon">&rarr;</span></a>
        <a href="services.html" class="btn btn-outline">See how we work</a>
      </div>
    </div>
    <a class="scroll-cue" href="#services" aria-label="Scroll to services"><span></span></a>
  </section>

  <section id="services" class="panels-section">
    <div class="wrap-wide">
      <div class="panels">
{panels()}
      </div>
    </div>
  </section>
""",
)

# --------------------------------------------------------------- ABOUT ----
PAGES["about.html"] = dict(
    title="About Canvas Systems | Odoo ERP Partner",
    desc="Canvas Systems is an Odoo ERP implementation partner working with businesses worldwide — our methodology, our approach, and how we deliver.",
    active="about",
    body=f"""{page_hero('<a href="about.html">About</a>', "About us",
                        "An Odoo partner that plans before it configures",
                        "We are an ERP implementation team specializing exclusively in Odoo. We help businesses replace disconnected spreadsheets and legacy software with one integrated platform — and we do it on a fixed methodology with milestone sign-offs, so nobody is guessing what happens next.")}

  <section>
    <div class="wrap content-grid">
      <div class="prose reveal">
        <h2>Who we are</h2>
        <p>Canvas Systems is an Odoo implementation partner headquartered in {HQ}, working with companies across the GCC, Africa, Europe and Asia. We specialize in delivering end-to-end ERP solutions that help businesses streamline operations, improve visibility and grow sustainably.</p>
        <p>Odoo is a world-class open-source ERP platform used by over 12 million users globally, offering a fully integrated suite of business applications — from accounting and inventory to CRM, HR and eCommerce — under one unified system. Our job is to make that platform fit the way <em>your</em> business actually works.</p>

        <h3>What makes us different</h3>
        <ul class="ticks">
          <li><span class="tick">&#10003;</span><span><strong>Process-first, always.</strong> We run Business Process Review workshops and produce a signed-off requirements document before configuring anything. No template rollouts.</span></li>
          <li><span class="tick">&#10003;</span><span><strong>Functional and technical under one roof.</strong> The consultants who map your processes work alongside the developers who build the custom modules — no handover gap.</span></li>
          <li><span class="tick">&#10003;</span><span><strong>Localization is part of setup.</strong> Tax regimes, e-invoicing, currencies, languages and banking formats are configured during Phase 2, not raised as a change request later.</span></li>
          <li><span class="tick">&#10003;</span><span><strong>We stay after go-live.</strong> Four weeks of hypercare is included in every implementation, followed by an AMC with a defined response SLA.</span></li>
          <li><span class="tick">&#10003;</span><span><strong>Bilingual delivery.</strong> Interface, documents, training and support in English and Arabic from the same team.</span></li>
        </ul>

        <div class="callout">
          <strong>Our operating principle</strong>
          Software should adapt to your business. If a workflow works well today, we configure Odoo around it. If it doesn't, we say so during discovery — before it gets encoded into a system you'll live with for a decade.
        </div>

        <h3 id="methodology">How we deliver</h3>
        <p>Every implementation follows the same six phases, each with a defined deliverable and a sign-off gate. You always know which phase you're in, what we're waiting on, and what comes next.</p>
        <ol class="steps">
          <li><strong>Discovery &amp; requirements (Week 1–2)</strong>Kick-off with stakeholders, process review workshops, and a gap analysis against standard Odoo. Ends with a signed-off Business Requirements Document.</li>
          <li><strong>Configuration &amp; customization (Week 3–6)</strong>Environment setup, module configuration to the BRD, tax and currency setup, chart of accounts, and branded document templates.</li>
          <li><strong>Data migration (Week 5–7)</strong>Extraction templates, cleansing and validation, then a pilot migration you review and sign off before the final load.</li>
          <li><strong>User acceptance testing (Week 7–8)</strong>End-to-end testing of every workflow with your team, gaps resolved, formal UAT sign-off.</li>
          <li><strong>Training (Week 8–9)</strong>Role-based sessions, train-the-trainer, written manuals, and hands-on practice on a staging environment.</li>
          <li><strong>Go-live &amp; hypercare (Week 10–12)</strong>Final migration and cutover with our consultants alongside your team, then four weeks of dedicated hypercare.</li>
        </ol>

        <h3>Engagement terms</h3>
        <p>Implementations are quoted as a fixed scope after a scoping session, so the number you approve is the number you pay. Standard payment terms are 40% at kick-off, 40% at go-live and 20% at project closure. Odoo licensing is billed separately by user count and edition, and all figures are quoted exclusive of local tax.</p>
      </div>
      {sidebar([("services.html", "All services"), ("pricing.html", "Pricing &amp; packages"),
                ("comparisons.html", "Odoo vs other ERPs"), ("industries.html", "Industries we serve")])}
    </div>
  </section>

  <section class="soft" id="faq">
    <div class="wrap">
      <div class="section-head reveal">
        <div class="eyebrow">FAQ</div>
        <h2>Frequently asked questions</h2>
      </div>
      <div class="faq-list reveal">
        <details><summary>How much does an Odoo implementation cost?</summary><p>Implementation is quoted as a fixed scope after a scoping session, and depends on the number of modules and users, how much custom development is needed, and how much data has to be migrated. Odoo licensing is separate and billed annually by user count and edition. See the <a href="pricing.html">pricing page</a> for package structures.</p></details>
        <details><summary>How long does an implementation take?</summary><p>A full six-phase implementation typically runs 10–12 weeks from kick-off, subject to your team's availability and how quickly data can be provided. A focused rollout on a smaller module set can go live noticeably faster.</p></details>
        <details><summary>Do you work with clients outside your home country?</summary><p>Yes — the majority of our delivery is remote. Discovery workshops, training and go-live can be run over video, and we travel for the phases where being in the room genuinely helps. Multi-country, multi-currency and multi-company setups are routine work for us.</p></details>
        <details><summary>Can Odoo handle our local tax and e-invoicing rules?</summary><p>In most cases yes. Odoo ships localization packages for a large number of countries covering chart of accounts, tax codes and statutory reports. Where a specific e-invoicing portal or regulator format is required, we build or configure the connector during implementation.</p></details>
        <details><summary>Which languages do you support?</summary><p>Odoo's interface, reports and printed documents run in dozens of languages, including full right-to-left Arabic. Our team delivers training, manuals and support in English and Arabic.</p></details>
        <details><summary>Cloud or on-premise — which do you recommend?</summary><p>Either works. We deploy on Odoo's cloud, a private cloud, or your own servers depending on your IT policy and data residency requirements, and make a recommendation during discovery based on your team size and internal IT capability.</p></details>
        <details><summary>Community or Enterprise edition?</summary><p>It depends on which apps you need. Community covers a lot of ground at no licence cost; Enterprise adds accounting automation, studio, mobile apps, and official support. We'll recommend an edition during scoping and show you the cost difference before you commit.</p></details>
        <details><summary>What happens after go-live?</summary><p>Four weeks of hypercare is included with every implementation. After that you move onto a Basic, Standard or Premium AMC depending on the response time your operation needs — see <a href="support.html">Support &amp; AMC</a>.</p></details>
      </div>
    </div>
  </section>
{CTA_BANNER}
""",
)

# ------------------------------------------------------------ SERVICES ----
PAGES["services.html"] = dict(
    title="Odoo Services | Canvas Systems",
    desc="End-to-end Odoo services: consulting, implementation, customization, data migration, integrations, training, support and version upgrades.",
    active="services",
    body=f"""{page_hero('<a href="services.html">Services</a>', "Services",
                        "Every stage of your Odoo journey, one partner",
                        "Most ERP projects fail somewhere in the handovers — between the consultant who scoped it, the developer who built it, and the team left running it. We cover the whole lifecycle so there are no handovers to fall through.")}

  <section>
    <div class="wrap">
      <div class="section-head reveal">
        <div class="eyebrow">Core services</div>
        <h2>What we do</h2>
        <p>Engage us for a full implementation, or for a single piece of work on a system you already run.</p>
      </div>
      <div class="grid-3 reveal">
        <a class="card" href="implementation.html">
          <div class="icon"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="3" width="7" height="7" rx="1.5"/><rect x="14" y="3" width="7" height="7" rx="1.5"/><rect x="3" y="14" width="7" height="7" rx="1.5"/><rect x="14" y="14" width="7" height="7" rx="1.5"/></svg></div>
          <h3>Implementation</h3>
          <p>End-to-end rollout across six phases — discovery, configuration, migration, UAT, training, go-live and hypercare.</p>
          <span class="more">Learn more</span>
        </a>
        <a class="card" href="customization.html">
          <div class="icon"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 2l2.4 6.6L21 11l-6.6 2.4L12 20l-2.4-6.6L3 11l6.6-2.4L12 2z"/></svg></div>
          <h3>Customization &amp; development</h3>
          <p>Custom modules, fields, automated workflows, and branded reports for processes standard Odoo doesn't cover.</p>
          <span class="more">Learn more</span>
        </a>
        <a class="card" href="migration.html">
          <div class="icon"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M4 16l4-4 4 4 8-8"/><path d="M16 8h4v4"/></svg></div>
          <h3>Migration &amp; upgrades</h3>
          <p>Data moved cleanly off your legacy system, or your existing Odoo lifted onto a newer version with testing.</p>
          <span class="more">Learn more</span>
        </a>
        <a class="card" href="integration.html">
          <div class="icon"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="6" cy="12" r="2.5"/><circle cx="18" cy="6" r="2.5"/><circle cx="18" cy="18" r="2.5"/><path d="M8.2 10.8L15.8 7.2M8.2 13.2L15.8 16.8"/></svg></div>
          <h3>Integrations</h3>
          <p>Banks, payment gateways, e-invoicing portals, marketplaces, shipping carriers and any REST or SOAP API.</p>
          <span class="more">Learn more</span>
        </a>
        <a class="card" href="training.html">
          <div class="icon"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M4 19.5A2.5 2.5 0 016.5 17H20"/><path d="M6.5 2H20v20H6.5A2.5 2.5 0 014 19.5v-15A2.5 2.5 0 016.5 2z"/></svg></div>
          <h3>Training &amp; adoption</h3>
          <p>Role-based training, train-the-trainer sessions and written manuals so the system survives staff turnover.</p>
          <span class="more">Learn more</span>
        </a>
        <a class="card" href="support.html">
          <div class="icon"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 22a10 10 0 100-20 10 10 0 000 20z"/><path d="M9.1 9a3 3 0 015.8 1c0 2-3 3-3 3"/><path d="M12 17h.01"/></svg></div>
          <h3>Support &amp; AMC</h3>
          <p>Annual Maintenance Contracts from business-hours email cover through to a dedicated manager on a 4-hour SLA.</p>
          <span class="more">Learn more</span>
        </a>
      </div>
    </div>
  </section>

  <section class="soft">
    <div class="wrap">
      <div class="section-head reveal">
        <div class="eyebrow">Also available</div>
        <h2>Specialist engagements</h2>
        <p>Shorter, targeted pieces of work for teams who don't need a full implementation.</p>
      </div>
      <div class="grid-4 reveal">
        <div class="card"><h3>ERP consultancy</h3><p>An independent review of whether Odoo fits, which edition you need, and what it would take to get there.</p></div>
        <div class="card"><h3>Project rescue</h3><p>A stalled or failed implementation audited, re-scoped and taken to completion.</p></div>
        <div class="card"><h3>Hosting &amp; deployment</h3><p>Cloud, private cloud or on-premise setup with backups, monitoring and staging environments.</p></div>
        <div class="card"><h3>Licensing advice</h3><p>Community vs Enterprise, user counts and app selection — sized so you don't over-buy.</p></div>
        <div class="card"><h3>Health check</h3><p>A review of an existing Odoo instance: performance, data quality, unused modules and upgrade readiness.</p></div>
        <div class="card"><h3>Report building</h3><p>Custom dashboards and printed reports built to the numbers your managers actually ask for.</p></div>
        <div class="card"><h3>Dedicated developers</h3><p>Odoo developers embedded with your in-house team on a monthly basis.</p></div>
        <div class="card"><h3>Process automation</h3><p>Approval chains, scheduled actions and automated notifications built on Odoo's automation engine.</p></div>
      </div>
    </div>
  </section>

  <section>
    <div class="wrap">
      <div class="section-head reveal">
        <div class="eyebrow">Our methodology</div>
        <h2>Six phases from kickoff to go-live</h2>
        <p>The same structure applies whether you are implementing three modules or twelve.</p>
      </div>
      <div class="process-track reveal">
{process_track()}
      </div>
    </div>
  </section>
{CTA_BANNER}
""",
)

# -------------------------------------------------------------- MODULES ---
PAGES["modules.html"] = dict(
    title="Odoo Modules We Implement | Canvas Systems",
    desc="The Odoo modules Canvas Systems implements — accounting, inventory, sales, purchase, CRM, HR, manufacturing, POS, eCommerce, projects, field service and more.",
    active="modules",
    body=f"""{page_hero('<a href="modules.html">Modules</a>', "Field of expertise",
                        "One platform, every department",
                        "Odoo's strength is that the modules share one database. A sales order reserves stock, triggers a purchase, posts to the ledger and updates the dashboard without anyone re-keying it. These are the apps we deploy most.")}

  <section>
    <div class="wrap">
      <div class="mod-grid reveal">
{modules_grid()}
      </div>
    </div>
  </section>

  <section class="soft">
    <div class="wrap">
      <div class="section-head reveal">
        <div class="eyebrow">How we scope</div>
        <h2>Which modules do you actually need?</h2>
        <p>More modules is not better. Every app you switch on is one more thing to configure, test, train and maintain.</p>
      </div>
      <div class="grid-3 reveal">
        <div class="card"><div class="step-n">START</div><h3>The operational core</h3><p>Most businesses go live on Sales, Inventory, Purchase and Accounting. That alone removes the majority of double entry and gives you real-time stock and margin.</p></div>
        <div class="card"><div class="step-n">THEN</div><h3>The growth layer</h3><p>CRM, HR and Projects follow once the core is stable — typically a second phase four to eight weeks after go-live.</p></div>
        <div class="card"><div class="step-n">LAST</div><h3>The specialist apps</h3><p>Manufacturing, POS, eCommerce and Field Service are deep modules. They deserve their own discovery rather than being bundled into an initial rollout.</p></div>
      </div>
      <div class="process-note reveal" style="max-width:820px; margin-left:auto; margin-right:auto;">
        <span aria-hidden="true">&#9432;</span>
        <div><strong>A note on licensing.</strong> Odoo Community covers a great deal at no licence cost. Enterprise adds accounting automation, Studio, mobile apps, and official support. We'll show you the cost difference for your specific app list during scoping — see <a href="pricing.html">pricing</a>.</div>
      </div>
    </div>
  </section>
{CTA_BANNER}
""",
)

# ----------------------------------------------------------- INDUSTRIES ---
PAGES["industries.html"] = dict(
    title="Industries We Serve | Odoo ERP by Canvas Systems",
    desc="Odoo ERP configured for trading, manufacturing, retail, construction, logistics, eCommerce, healthcare, education, hospitality, professional services, energy and automotive.",
    active="industries",
    body=f"""{page_hero('<a href="industries.html">Industries</a>', "Industry expertise",
                        "Odoo configured for how your sector actually works",
                        "A distributor and a manufacturer need very different things from the same inventory module. We start each project from a configuration shaped by the problems your industry runs into, then tailor from there.")}

  <section>
    <div class="wrap">
      <div class="industries-grid reveal">
{industries_grid()}
      </div>
    </div>
  </section>

  <section class="soft">
    <div class="wrap">
      <div class="section-head reveal">
        <div class="eyebrow">Sector detail</div>
        <h2>What we typically build, by sector</h2>
      </div>
      <div class="grid-2 reveal">
        <div class="card">
          <h3>Trading &amp; Distribution</h3>
          <p>Multi-warehouse stock with landed-cost allocation so margin reflects freight and duty. Customer-specific price lists, backorder handling, and reordering rules that stop the stockouts and the dead stock at the same time.</p>
        </div>
        <div class="card">
          <h3>Manufacturing</h3>
          <p>Multi-level bills of materials, routings and work centres, MRP scheduling against real capacity, subcontracting flows, and quality control points embedded in production rather than tracked on a clipboard.</p>
        </div>
        <div class="card">
          <h3>Retail &amp; Wholesale</h3>
          <p>POS terminals that keep selling when the internet drops and sync to the same stock and ledger as the back office. Loyalty schemes, multi-store transfers, and daily cash reconciliation.</p>
        </div>
        <div class="card">
          <h3>Construction &amp; Real Estate</h3>
          <p>Project-level costing against budget, subcontractor management, progress billing and retentions, and equipment allocation across sites — so you know which jobs actually made money.</p>
        </div>
        <div class="card">
          <h3>Logistics &amp; Transport</h3>
          <p>Fleet records and maintenance schedules, dispatch and route planning, driver assignment, and per-delivery cost tracking that ties fuel and maintenance back to the job.</p>
        </div>
        <div class="card">
          <h3>eCommerce</h3>
          <p>Storefront and marketplace channels sharing one product catalogue and stock pool, with payment gateways, shipping carriers and automatic invoice generation.</p>
        </div>
        <div class="card">
          <h3>Healthcare &amp; Pharma</h3>
          <p>Lot, batch and expiry tracking with FEFO picking, controlled-substance records, supplier compliance documentation, and audit trails on every stock movement.</p>
        </div>
        <div class="card">
          <h3>Professional Services</h3>
          <p>Timesheets against tasks, billable and non-billable rates, milestone invoicing, and per-project profitability visible while the work is still running.</p>
        </div>
      </div>
    </div>
  </section>

  <section>
    <div class="wrap">
      <div class="section-head reveal">
        <div class="eyebrow">Not listed?</div>
        <h2>Most businesses fit Odoo — the question is how</h2>
        <p>If your sector isn't above, it usually means the interesting work is in the detail rather than the module list. Tell us how you operate and we'll tell you honestly whether Odoo is the right answer.</p>
      </div>
      <p style="text-align:center;"><a href="contact.html" class="btn btn-primary">Talk to a consultant</a></p>
    </div>
  </section>
{CTA_BANNER}
""",
)

# -------------------------------------------------------------- PRICING ---
PAGES["pricing.html"] = dict(
    title="Odoo Implementation Pricing | Canvas Systems",
    desc="How Odoo implementation is priced: fixed-scope packages, licensing, AMC support tiers and payment terms.",
    active="pricing",
    body=f"""{page_hero('<a href="pricing.html">Pricing</a>', "Pricing",
                        "What an Odoo project actually costs",
                        "Two separate costs go into any Odoo project: the software licence you pay Odoo, and the implementation you pay us. Here is how both work, and what drives them up or down.")}

  <section>
    <div class="wrap">
      <div class="section-head reveal">
        <div class="eyebrow">Implementation packages</div>
        <h2>Fixed-scope packages</h2>
        <p>Quoted after a scoping session, so the number you approve is the number you pay. Change requests are priced separately and approved before work starts.</p>
      </div>
      <div class="plan-grid reveal">
        <div class="plan">
          <h3>Essentials</h3>
          <div class="who">Small teams going live on the core</div>
          <div class="price"><span class="ph">[X,XXX]</span></div>
          <div class="price-note">Indicative — confirmed after scoping</div>
          <ul>
            <li><span class="tick">&#10003;</span> Accounting, Sales, Inventory</li>
            <li><span class="tick">&#10003;</span> Local tax &amp; currency configuration</li>
            <li><span class="tick">&#10003;</span> Standard reports and documents</li>
            <li><span class="tick">&#10003;</span> Master data migration</li>
            <li><span class="tick">&#10003;</span> Remote training</li>
            <li><span class="tick">&#10003;</span> 2 weeks post go-live support</li>
          </ul>
          <a href="contact.html" class="btn btn-outline">Request a quote</a>
        </div>
        <div class="plan featured">
          <h3>Growth</h3>
          <div class="who">Full six-phase implementation</div>
          <div class="price"><span class="ph">[X,XXX]</span></div>
          <div class="price-note">Indicative — confirmed after scoping</div>
          <ul>
            <li><span class="tick">&#10003;</span> Everything in Essentials</li>
            <li><span class="tick">&#10003;</span> Purchase, CRM and HR modules</li>
            <li><span class="tick">&#10003;</span> Full data migration with pilot load</li>
            <li><span class="tick">&#10003;</span> Branded document templates</li>
            <li><span class="tick">&#10003;</span> Role-based training on-site or remote</li>
            <li><span class="tick">&#10003;</span> 4 weeks hypercare</li>
          </ul>
          <a href="contact.html" class="btn btn-primary">Request a quote</a>
        </div>
        <div class="plan">
          <h3>Enterprise</h3>
          <div class="who">Multi-entity or manufacturing scope</div>
          <div class="price">Custom</div>
          <div class="price-note">Scoped against your requirements</div>
          <ul>
            <li><span class="tick">&#10003;</span> Everything in Growth</li>
            <li><span class="tick">&#10003;</span> Manufacturing, POS, eCommerce or Field Service</li>
            <li><span class="tick">&#10003;</span> Custom module development</li>
            <li><span class="tick">&#10003;</span> Third-party and banking integrations</li>
            <li><span class="tick">&#10003;</span> Multi-company &amp; multi-currency setup</li>
            <li><span class="tick">&#10003;</span> Dedicated project manager</li>
          </ul>
          <a href="contact.html" class="btn btn-outline">Talk to us</a>
        </div>
      </div>
      <p class="terms-note">All prices exclusive of local tax and of the Odoo licence subscription.<br>Standard payment terms: 40% at kick-off, 40% at go-live, 20% at project closure.</p>
    </div>
  </section>

  <section class="soft">
    <div class="wrap">
      <div class="section-head reveal">
        <div class="eyebrow">What moves the number</div>
        <h2>The five things that drive implementation cost</h2>
        <p>If you want a cheaper project, these are the levers — and we will tell you which ones are safe to pull.</p>
      </div>
      <div class="grid-3 reveal">
        <div class="card"><div class="step-n">01</div><h3>Number of modules</h3><p>Each app needs configuration, testing and training. Going live on four modules instead of eight is the single biggest saving available.</p></div>
        <div class="card"><div class="step-n">02</div><h3>Custom development</h3><p>Standard Odoo is cheap; bespoke modules are not. We flag every gap during discovery so you can decide what's worth building.</p></div>
        <div class="card"><div class="step-n">03</div><h3>Data condition</h3><p>Clean exports migrate quickly. Fifteen years of inconsistent spreadsheets take real effort to cleanse and reconcile.</p></div>
        <div class="card"><div class="step-n">04</div><h3>Integrations</h3><p>A documented REST API is a day's work. An undocumented legacy system with no export is a project of its own.</p></div>
        <div class="card"><div class="step-n">05</div><h3>Users and locations</h3><p>Training effort scales with headcount and sites; multi-company and multi-currency add configuration and testing.</p></div>
        <div class="card"><div class="step-n">&#8210;</div><h3>What doesn't change it</h3><p>Our methodology. You get the same six phases and the same sign-off gates whether the project is small or large.</p></div>
      </div>
    </div>
  </section>

  <section>
    <div class="wrap">
      <div class="section-head reveal">
        <div class="eyebrow">Licensing</div>
        <h2>Community vs Enterprise</h2>
        <p>The licence is paid to Odoo S.A., not to us. We'll size it honestly — over-buying users is the most common mistake we see.</p>
      </div>
      <div class="table-scroll reveal">
        <table>
          <thead><tr><th scope="col">&nbsp;</th><th scope="col" class="hl">Community</th><th scope="col">Enterprise</th></tr></thead>
          <tbody>
            <tr><td class="rowlabel">Licence cost</td><td class="hl">Free, open source</td><td>Per user, per year</td></tr>
            <tr><td class="rowlabel">Core apps</td><td class="hl">Sales, CRM, Inventory, Purchase, Projects, basic accounting</td><td>All Community apps plus the Enterprise set</td></tr>
            <tr><td class="rowlabel">Full accounting automation</td><td class="hl">Limited</td><td>Bank sync, follow-ups, automated reconciliation</td></tr>
            <tr><td class="rowlabel">Studio (no-code customization)</td><td class="hl">Not included</td><td>Included</td></tr>
            <tr><td class="rowlabel">Mobile apps</td><td class="hl">Browser only</td><td>Native iOS and Android</td></tr>
            <tr><td class="rowlabel">Odoo.sh hosting</td><td class="hl">Self-hosted</td><td>Available</td></tr>
            <tr><td class="rowlabel">Vendor support</td><td class="hl">Community forums</td><td>Official Odoo support included</td></tr>
            <tr><td class="rowlabel">Best suited to</td><td class="hl">Lean teams with in-house IT and standard processes</td><td>Finance-heavy, multi-entity or regulated operations</td></tr>
          </tbody>
        </table>
      </div>
    </div>
  </section>

  <section class="soft">
    <div class="wrap">
      <div class="section-head reveal">
        <div class="eyebrow">After go-live</div>
        <h2>Annual Maintenance Contracts</h2>
        <p>Priced annually against the size of your deployment and the response time you need.</p>
      </div>
{AMC_PLANS}
    </div>
  </section>
{CTA_BANNER}
""",
)

# ---------------------------------------------------------- COMPARISONS ---
PAGES["comparisons.html"] = dict(
    title="Odoo vs SAP, NetSuite, Dynamics, Zoho &amp; ERPNext | Canvas Systems",
    desc="How Odoo compares against SAP Business One, Oracle NetSuite, Microsoft Dynamics 365, Zoho One, ERPNext and staying on spreadsheets.",
    active="comparisons",
    body=f"""{page_hero('<a href="comparisons.html">Comparisons</a>', "Comparisons",
                        "How Odoo stacks up against the alternatives",
                        "We only implement Odoo, so treat this as an informed but interested opinion. Where another platform is genuinely the better fit, we'd rather tell you at the first call than nine weeks into a project.")}

  <section>
    <div class="wrap">
      <div class="section-head reveal">
        <div class="eyebrow">At a glance</div>
        <h2>Odoo vs traditional enterprise ERP</h2>
        <p>Against SAP, Oracle and Microsoft's mid-market suites, the differences that matter are cost structure, time to value, and how much you can change later.</p>
      </div>
      <div class="table-scroll reveal">
        <table>
          <thead><tr><th scope="col">&nbsp;</th><th scope="col" class="hl">Odoo with Canvas Systems</th><th scope="col">Traditional ERP (SAP / Oracle / Dynamics)</th></tr></thead>
          <tbody>
            <tr><td class="rowlabel">Licensing model</td><td class="hl">Open-source core; Community free or Enterprise per user</td><td>Proprietary, per-seat, multi-year commitments</td></tr>
            <tr><td class="rowlabel">Total cost of ownership</td><td class="hl">Substantially lower over five years</td><td>High licence, infrastructure and consulting cost</td></tr>
            <tr><td class="rowlabel">Implementation time</td><td class="hl">10–12 weeks for a full rollout</td><td>Commonly 9–18 months</td></tr>
            <tr><td class="rowlabel">Scope of apps</td><td class="hl">One integrated suite — no separate subscriptions</td><td>Multiple products, often separately licensed</td></tr>
            <tr><td class="rowlabel">Customization</td><td class="hl">Source available; custom modules are routine</td><td>Restricted, expensive, upgrade-sensitive</td></tr>
            <tr><td class="rowlabel">Deployment</td><td class="hl">Cloud or on-premise, your choice</td><td>Frequently cloud-only on newer editions</td></tr>
            <tr><td class="rowlabel">Growing later</td><td class="hl">Add modules as you need them</td><td>Contract renegotiation, sometimes re-implementation</td></tr>
            <tr><td class="rowlabel">Exit risk</td><td class="hl">Open database schema, your data stays portable</td><td>Proprietary formats and heavy switching costs</td></tr>
          </tbody>
        </table>
      </div>
    </div>
  </section>

  <section class="soft">
    <div class="wrap">
      <div class="section-head reveal">
        <div class="eyebrow">Head to head</div>
        <h2>Odoo against specific platforms</h2>
      </div>
      <div class="grid-2 reveal">
        <div class="card">
          <h3>Odoo vs SAP Business One</h3>
          <p><strong>SAP wins on:</strong> deep manufacturing pedigree, and boardroom familiarity in large groups.</p>
          <p><strong>Odoo wins on:</strong> licence cost, breadth of non-finance apps included, speed of change after go-live, and a far shorter implementation. For a business under a few hundred users, the SAP premium is rarely repaid.</p>
        </div>
        <div class="card">
          <h3>Odoo vs Oracle NetSuite</h3>
          <p><strong>NetSuite wins on:</strong> mature multi-subsidiary consolidation and a large partner ecosystem in North America.</p>
          <p><strong>Odoo wins on:</strong> cost at every user count, on-premise as an option, and customization that doesn't require a specialist scripting language. NetSuite renewals also tend to move in one direction.</p>
        </div>
        <div class="card">
          <h3>Odoo vs Microsoft Dynamics 365</h3>
          <p><strong>Dynamics wins on:</strong> native Microsoft 365 and Power BI integration if your organization is already deeply invested there.</p>
          <p><strong>Odoo wins on:</strong> total cost, a single unified suite instead of separately licensed modules, and much lighter implementation overhead.</p>
        </div>
        <div class="card">
          <h3>Odoo vs Zoho One</h3>
          <p><strong>Zoho wins on:</strong> price at small scale and very fast self-service setup for simple needs.</p>
          <p><strong>Odoo wins on:</strong> real manufacturing and inventory depth, proper double-entry accounting, and the ability to keep going as you scale. Zoho's apps are separate products that integrate; Odoo's share one database.</p>
        </div>
        <div class="card">
          <h3>Odoo vs ERPNext</h3>
          <p><strong>ERPNext wins on:</strong> being fully open source with no paid edition at all.</p>
          <p><strong>Odoo wins on:</strong> app breadth, UI maturity, localization coverage, and the size of the partner and developer market you can hire from later.</p>
        </div>
        <div class="card">
          <h3>Odoo vs spreadsheets</h3>
          <p><strong>Spreadsheets win on:</strong> nothing, past about twenty staff — though they are genuinely fine below that.</p>
          <p><strong>Odoo wins on:</strong> one version of the truth, an audit trail, stock that reflects reality, and month-end that takes hours instead of weeks. The real cost of spreadsheets is the decisions made on stale numbers.</p>
        </div>
      </div>
    </div>
  </section>

  <section>
    <div class="wrap">
      <div class="section-head reveal">
        <div class="eyebrow">Honest advice</div>
        <h2>When Odoo is the wrong choice</h2>
      </div>
      <div class="grid-3 reveal">
        <div class="card"><h3>Heavily regulated niche verticals</h3><p>If your industry has a dominant specialist system with certification requirements Odoo can't meet, buy the specialist system.</p></div>
        <div class="card"><h3>Very large enterprises</h3><p>Above roughly a thousand users with complex global consolidation, the tier-one suites earn their price.</p></div>
        <div class="card"><h3>Teams unwilling to change process</h3><p>ERP fails when nobody will alter how they work. That is not a software problem, and no platform fixes it.</p></div>
      </div>
    </div>
  </section>
{CTA_BANNER}
""",
)

# -------------------------------------------------------------- CONTACT ---
PAGES["contact.html"] = dict(
    title="Contact Canvas Systems | Odoo ERP Partner",
    desc="Book a free 30-minute Odoo ERP assessment with Canvas Systems. We reply within one business day.",
    active="contact",
    body=f"""{page_hero('<a href="contact.html">Contact</a>', "Get in touch",
                        "Tell us about your business",
                        "Share a bit about your operations and where Odoo needs to fit. We'll come back with a scoped module list, an indicative timeline and next steps — not a generic quote.", ctas=False)}

  <section>
    <div class="wrap contact-grid">
      <div class="contact-info reveal">
        <div class="eyebrow">Contact details</div>
        <h2>Talk to a consultant</h2>
        <p>We work with clients across several time zones and run most sessions over video. If you'd rather start with a written summary, email is fine too.</p>

        <div class="contact-detail">
          <div class="icon">{IC_MAIL}</div>
          <div><div class="label">Email</div><a class="val" href="mailto:{EMAIL}">{EMAIL}</a></div>
        </div>
        <div class="contact-detail">
          <div class="icon">{IC_PHONE}</div>
          <div><div class="label">Phone / WhatsApp</div><div class="val">{PHONE_DISPLAY}</div></div>
        </div>
        <div class="contact-detail">
          <div class="icon">{IC_PIN}</div>
          <div><div class="label">Head office</div><div class="val">{HQ}</div></div>
        </div>
        <div class="contact-detail">
          <div class="icon">{IC_PIN}</div>
          <div><div class="label">Branches</div><div class="val">{BRANCHES}</div></div>
        </div>
        <div class="contact-detail">
          <div class="icon">{IC_CLOCK}</div>
          <div><div class="label">Hours</div><div class="val">Sunday–Thursday, 8:30–17:30 GST</div></div>
        </div>

        <div class="contact-promise">
          <strong>What happens next</strong>
          We reply within one business day, book a 30-minute call to understand your processes, then send a scoped module list and indicative timeline. No obligation, no pressure.
        </div>
      </div>

      {CONTACT_FORM}
    </div>
  </section>

  <section class="soft">
    <div class="wrap">
      <div class="section-head reveal">
        <div class="eyebrow">Before you call</div>
        <h2>What's useful to have ready</h2>
        <p>None of this is required — but the more of it you can bring, the more specific our first answer can be.</p>
      </div>
      <div class="grid-4 reveal">
        <div class="card"><h3>Headcount by department</h3><p>Roughly how many people will need a login, and in which functions.</p></div>
        <div class="card"><h3>Current systems</h3><p>What you run today for accounting, stock and CRM — and what you'd keep.</p></div>
        <div class="card"><h3>Biggest pain point</h3><p>The one process that costs you the most time or money right now.</p></div>
        <div class="card"><h3>Target date</h3><p>Any deadline driving this — a financial year, an audit, a lease, a launch.</p></div>
      </div>
    </div>
  </section>
""",
)

# --------------------------------------------------------------------------
# Service detail pages — data-driven
# --------------------------------------------------------------------------
SERVICE_CONTENT = {
    "implementation.html": dict(
        title="Odoo Implementation Services | Canvas Systems",
        desc="End-to-end Odoo ERP implementation across six phases — discovery, configuration, data migration, UAT, training, go-live and hypercare.",
        eyebrow="Implementation",
        h1="Odoo implementation, end to end",
        sub="A full ERP rollout in 10–12 weeks, structured across six phases with a sign-off gate at each one. You always know which phase you're in and what's blocking the next.",
        prose=f"""
        <h2>What an implementation covers</h2>
        <p>An implementation is the whole job: understanding how you work today, configuring Odoo to match, moving your data across, testing it with the people who'll use it, training them, and standing beside you on cutover day.</p>
        <ul class="ticks">
          <li><span class="tick">&#10003;</span><span><strong>Business Process Review.</strong> Workshops with every affected department to document how work actually flows — including the parts that live in someone's head.</span></li>
          <li><span class="tick">&#10003;</span><span><strong>Gap analysis.</strong> Every process mapped to standard Odoo, with the gaps flagged, costed and decided on before development starts.</span></li>
          <li><span class="tick">&#10003;</span><span><strong>Environment setup.</strong> Cloud, private cloud or on-premise, with staging and production separated and backups configured from day one.</span></li>
          <li><span class="tick">&#10003;</span><span><strong>Module configuration.</strong> Products, partners, warehouses, tax codes, chart of accounts, approval rules, user roles and access rights.</span></li>
          <li><span class="tick">&#10003;</span><span><strong>Localization.</strong> Country tax regime, currency, language, and any statutory or e-invoicing formats you're required to file.</span></li>
          <li><span class="tick">&#10003;</span><span><strong>Branded documents.</strong> Invoices, quotations, purchase orders and delivery notes in your identity, in the languages you trade in.</span></li>
          <li><span class="tick">&#10003;</span><span><strong>Data migration.</strong> Customers, suppliers, products and opening balances cleansed, validated, pilot-loaded and signed off.</span></li>
          <li><span class="tick">&#10003;</span><span><strong>Training and hypercare.</strong> Role-based sessions before go-live, then four weeks of dedicated support after it.</span></li>
        </ul>

        <div class="callout">
          <strong>Why the sign-off gates matter</strong>
          The most expensive ERP mistakes are discovered late. A gate at the end of each phase means a misunderstanding about your pricing rules surfaces in week two, not week eleven.
        </div>

        <h3>How we run it</h3>
        <ol class="steps">
          <li><strong>Discovery &amp; requirements (Week 1–2)</strong>Stakeholder kick-off, process workshops, gap analysis. Ends with a Business Requirements Document you sign.</li>
          <li><strong>Configuration &amp; customization (Week 3–6)</strong>Environment build, module configuration to the BRD, localization, and branded templates. Ends with a working system demo.</li>
          <li><strong>Data migration (Week 5–7)</strong>Extraction templates, cleansing, transformation, and a pilot load you review before the final migration.</li>
          <li><strong>User acceptance testing (Week 7–8)</strong>Your team runs real scenarios end to end. Issues logged, fixed and retested until you sign off.</li>
          <li><strong>Training (Week 8–9)</strong>Role-based sessions per department, train-the-trainer for internal champions, and written manuals.</li>
          <li><strong>Go-live &amp; hypercare (Week 10–12)</strong>Final data load, cutover with us alongside your team, then four weeks of hypercare and an optimization review.</li>
        </ol>

        <h3>What we need from you</h3>
        <p>Implementations slip for one of two reasons: data arrives late, or the people who know the process aren't available for the workshops. We'll tell you exactly what's needed and when, but plan for a nominated project owner on your side and a few hours per department during discovery and UAT.</p>
""",
        related=[("customization.html", "Customization"), ("migration.html", "Data migration"),
                 ("training.html", "Training"), ("support.html", "Support &amp; AMC")],
    ),
    "customization.html": dict(
        title="Odoo Customization &amp; Development | Canvas Systems",
        desc="Custom Odoo modules, fields, automated workflows, branded reports and dashboards built to fit processes standard Odoo doesn't cover.",
        eyebrow="Customization",
        h1="Custom Odoo development that survives upgrades",
        sub="Standard Odoo covers most of what most businesses do. For the rest, we build custom modules properly — as separate, upgrade-safe code, not edits to the core.",
        prose="""
        <h2>When customization is the right answer</h2>
        <p>Our default position is to configure before we code. Every custom module is something that has to be maintained, tested and carried forward at every future upgrade. But some processes genuinely are your competitive advantage, and forcing them into a standard workflow destroys value.</p>
        <ul class="ticks">
          <li><span class="tick">&#10003;</span><span><strong>Custom modules.</strong> New objects, screens and business logic for processes Odoo has no concept of.</span></li>
          <li><span class="tick">&#10003;</span><span><strong>Fields and views.</strong> Additional data captured where your team already works, without cluttering screens for everyone else.</span></li>
          <li><span class="tick">&#10003;</span><span><strong>Automated workflows.</strong> Approval chains, escalations, scheduled actions and conditional notifications.</span></li>
          <li><span class="tick">&#10003;</span><span><strong>Pricing and discount logic.</strong> Contract rates, volume breaks and customer-specific rules that standard price lists can't express.</span></li>
          <li><span class="tick">&#10003;</span><span><strong>Reports and dashboards.</strong> Printed documents and management views built to the numbers your managers actually ask for.</span></li>
          <li><span class="tick">&#10003;</span><span><strong>Access rules.</strong> Record-level security so branches, teams or subsidiaries only see what they should.</span></li>
        </ul>

        <div class="callout">
          <strong>How we keep customizations safe</strong>
          Everything is built as a separate module with its own version control, never as a patch to Odoo's core. That is the difference between an upgrade taking a fortnight and an upgrade being impossible.
        </div>

        <h3>Our development approach</h3>
        <ol class="steps">
          <li><strong>Specification</strong>Every requirement written up with the expected behaviour and acceptance criteria, then approved by you before a line is written.</li>
          <li><strong>Estimate and approval</strong>Fixed effort per item so you can decide what's worth building and what can wait for phase two.</li>
          <li><strong>Build on staging</strong>Developed against a copy of your live database, never directly on production.</li>
          <li><strong>Test and review</strong>You test against the acceptance criteria on staging and sign off before anything is deployed.</li>
          <li><strong>Deploy and document</strong>Released to production with the module documented so any competent Odoo developer can maintain it later.</li>
        </ol>

        <h3>A word on scope</h3>
        <p>If a request would be better solved by changing a process than by writing code, we'll say so. That conversation occasionally loses us a few days of billable development, and it has saved clients far more than that in maintenance they never had to carry.</p>
""",
        related=[("implementation.html", "Implementation"), ("integration.html", "Integrations"),
                 ("modules.html", "Odoo modules"), ("support.html", "Support &amp; AMC")],
    ),
    "migration.html": dict(
        title="Odoo Data Migration &amp; Version Upgrades | Canvas Systems",
        desc="Migrate data from legacy systems into Odoo, or upgrade an existing Odoo to a newer version — with pilot loads, reconciliation and rollback plans.",
        eyebrow="Migration &amp; upgrades",
        h1="Move your data — and your version — without losing history",
        sub="Two different jobs that both go wrong the same way: rushed, unreconciled and without a way back. We do both with a pilot load, a reconciliation step, and a tested rollback.",
        prose="""
        <h2>Legacy system migration</h2>
        <p>Getting off spreadsheets or an ageing accounting package is mostly a data problem, not a software problem. Years of inconsistent naming, duplicate customers and part-reconciled balances have to be resolved before they land in a system you'll trust.</p>
        <ul class="ticks">
          <li><span class="tick">&#10003;</span><span><strong>Extraction templates.</strong> Structured sheets for customers, suppliers, products, BOMs, open transactions and opening balances.</span></li>
          <li><span class="tick">&#10003;</span><span><strong>Cleansing and de-duplication.</strong> Merging duplicates, standardizing naming and codes, and fixing broken references before load.</span></li>
          <li><span class="tick">&#10003;</span><span><strong>Transformation and mapping.</strong> Old fields mapped to the Odoo model, with a documented decision for anything that doesn't map cleanly.</span></li>
          <li><span class="tick">&#10003;</span><span><strong>Pilot migration.</strong> A full load into a staging database that you review and sign off before the real one.</span></li>
          <li><span class="tick">&#10003;</span><span><strong>Reconciliation.</strong> Balances, stock quantities and open item lists proved against your old system before we call it done.</span></li>
          <li><span class="tick">&#10003;</span><span><strong>Historical data.</strong> A decision, taken deliberately: how many years of transaction history come across, and what stays archived.</span></li>
        </ul>

        <div class="callout">
          <strong>The rule we don't break</strong>
          Nothing goes live until opening balances and stock quantities reconcile against the source system. A go-live on numbers that don't tie is a month-end crisis with a fixed date.
        </div>

        <h2>Odoo version upgrades</h2>
        <p>Odoo releases a major version each year. Staying several versions behind eventually means missing security fixes, losing access to newer apps, and making every future upgrade harder. But an upgrade with custom modules involved is a project, not a button.</p>
        <ol class="steps">
          <li><strong>Assessment</strong>An inventory of your installed modules, customizations and third-party apps, with a compatibility check against the target version.</li>
          <li><strong>Code migration</strong>Custom modules updated for API changes in the new version, and dead code retired rather than carried forward.</li>
          <li><strong>Database upgrade on staging</strong>A full dress rehearsal on a copy, with the elapsed time measured so the real cutover window is known, not guessed.</li>
          <li><strong>Regression testing</strong>Your critical workflows tested end to end against the upgraded staging copy.</li>
          <li><strong>Cutover with rollback</strong>Scheduled for a quiet window, with a tested rollback plan if anything fails the go/no-go check.</li>
        </ol>

        <h3>Should you upgrade?</h3>
        <p>Not always immediately. If your current version is supported, stable and doing the job, the honest advice is often to plan the upgrade for a quiet period rather than treat it as urgent. We'll give you a straight assessment of the risk of waiting.</p>
""",
        related=[("implementation.html", "Implementation"), ("customization.html", "Customization"),
                 ("support.html", "Support &amp; AMC"), ("pricing.html", "Pricing")],
    ),
    "integration.html": dict(
        title="Odoo Integrations | Canvas Systems",
        desc="Connect Odoo to banks, payment gateways, e-invoicing portals, marketplaces, shipping carriers, POS hardware and any REST or SOAP API.",
        eyebrow="Integrations",
        h1="Odoo connected to everything else you run",
        sub="An ERP that doesn't talk to your bank, your storefront or your regulator's portal just moves the re-keying somewhere else. We build the connections that close those gaps.",
        prose="""
        <h2>What we connect</h2>
        <ul class="ticks">
          <li><span class="tick">&#10003;</span><span><strong>Banking.</strong> Statement imports and bank feeds for automated reconciliation, plus payment file generation in your bank's format.</span></li>
          <li><span class="tick">&#10003;</span><span><strong>Payment gateways.</strong> Card and local payment providers wired into sales orders, the customer portal and eCommerce checkout.</span></li>
          <li><span class="tick">&#10003;</span><span><strong>E-invoicing and tax portals.</strong> Statutory submission formats and clearance flows where your jurisdiction requires them.</span></li>
          <li><span class="tick">&#10003;</span><span><strong>eCommerce and marketplaces.</strong> Storefronts and marketplace channels sharing one catalogue, stock pool and order flow.</span></li>
          <li><span class="tick">&#10003;</span><span><strong>Shipping carriers.</strong> Rate lookup, label generation and tracking updates pushed back to the customer.</span></li>
          <li><span class="tick">&#10003;</span><span><strong>Hardware.</strong> Barcode scanners, label printers, scales, POS terminals and biometric attendance devices.</span></li>
          <li><span class="tick">&#10003;</span><span><strong>Business tools.</strong> Email, calendars, document storage, e-signature, and BI tools reading from the Odoo database.</span></li>
          <li><span class="tick">&#10003;</span><span><strong>Anything with an API.</strong> Odoo exposes XML-RPC and JSON-RPC, so a documented REST or SOAP endpoint on the other side is usually enough.</span></li>
        </ul>

        <div class="callout">
          <strong>The question we ask first</strong>
          Does this need to be real-time, or is a scheduled sync every few minutes genuinely fine? Real-time integrations cost more to build and far more to keep running. Most requirements don't need it.
        </div>

        <h3>How we build integrations</h3>
        <ol class="steps">
          <li><strong>Map the data flow</strong>Which system owns each record, which direction data moves, and what happens on a conflict.</li>
          <li><strong>Agree failure behaviour</strong>What the integration does when the other end is down — queue, retry, alert, or block. Decided up front, not discovered in production.</li>
          <li><strong>Build against a sandbox</strong>Developed and tested against the provider's test environment wherever one exists.</li>
          <li><strong>Log everything</strong>Every exchange logged so a failed sync three weeks ago can still be diagnosed and replayed.</li>
          <li><strong>Monitor after launch</strong>Alerting on repeated failures, so you find out from us rather than from a customer.</li>
        </ol>

        <h3>Before you integrate</h3>
        <p>Sometimes the right answer is to retire the other system rather than connect to it. If a tool exists only because the old ERP couldn't do the job, Odoo may already cover it — and one fewer integration is one fewer thing to break.</p>
""",
        related=[("implementation.html", "Implementation"), ("customization.html", "Customization"),
                 ("modules.html", "Odoo modules"), ("support.html", "Support &amp; AMC")],
    ),
    "training.html": dict(
        title="Odoo Training &amp; User Adoption | Canvas Systems",
        desc="Role-based Odoo training, train-the-trainer sessions, written manuals and adoption support so your team actually uses the system.",
        eyebrow="Training",
        h1="The system only works if people use it",
        sub="Most failed ERP projects are technically fine. They fail because the warehouse kept its spreadsheet, and within six months the data in Odoo stopped being true.",
        prose="""
        <h2>How we train</h2>
        <p>Generic product training doesn't stick. People learn their own job, on their own data, in the system they'll log into on Monday. Every session we run is role-based and uses your configured staging environment, not a demo database.</p>
        <ul class="ticks">
          <li><span class="tick">&#10003;</span><span><strong>Role-based sessions.</strong> Separate tracks for Finance, Sales, Purchasing, Inventory, HR and Management — each covering only what that role does.</span></li>
          <li><span class="tick">&#10003;</span><span><strong>Hands-on practice.</strong> Every attendee works through real scenarios on staging, rather than watching a screen share.</span></li>
          <li><span class="tick">&#10003;</span><span><strong>Train-the-trainer.</strong> Internal champions taken deeper so you have in-house capability after we've gone.</span></li>
          <li><span class="tick">&#10003;</span><span><strong>Management training.</strong> A separate session on dashboards and reporting, so leadership pulls its own numbers instead of asking finance.</span></li>
          <li><span class="tick">&#10003;</span><span><strong>Written manuals.</strong> Quick-reference guides per role, in English and Arabic, kept with your configuration rather than generic Odoo documentation.</span></li>
          <li><span class="tick">&#10003;</span><span><strong>Refresher sessions.</strong> Available after go-live for new hires or when a new module comes online.</span></li>
        </ul>

        <div class="callout">
          <strong>Adoption is a leadership decision</strong>
          The single strongest predictor of adoption is whether management stops accepting the old reports. If the spreadsheet is still accepted at the Monday meeting, the spreadsheet survives — and the ERP data quietly rots.
        </div>

        <h3>When training happens</h3>
        <p>Training sits in Phase 5, after UAT and before go-live. That order is deliberate: training on a system that's still changing wastes everybody's time, and training too long before go-live means it's forgotten by cutover.</p>

        <h3>Signs adoption is slipping</h3>
        <ul class="ticks">
          <li><span class="tick">&#10003;</span><span>Stock adjustments rising month over month — someone is reconciling reality to the system instead of recording it.</span></li>
          <li><span class="tick">&#10003;</span><span>Sales orders created after the delivery has already gone out.</span></li>
          <li><span class="tick">&#10003;</span><span>Exports to Excel for routine reporting that a dashboard should cover.</span></li>
          <li><span class="tick">&#10003;</span><span>One person doing all the data entry for a whole department.</span></li>
        </ul>
        <p>All of these are fixable, and all of them are cheaper to fix in month two than in year two. Our AMC includes a periodic review that looks for exactly these patterns.</p>
""",
        related=[("implementation.html", "Implementation"), ("support.html", "Support &amp; AMC"),
                 ("modules.html", "Odoo modules"), ("about.html", "Our methodology")],
    ),
    "support.html": dict(
        title="Odoo Support &amp; Annual Maintenance Contracts | Canvas Systems",
        desc="Odoo support after go-live: Basic, Standard and Premium AMC tiers with 48-hour, 24-hour and 4-hour response SLAs.",
        eyebrow="Support &amp; AMC",
        h1="Support that doesn't end at handover",
        sub="Every implementation includes four weeks of hypercare. After that, an Annual Maintenance Contract keeps someone accountable for the system your business now runs on.",
        prose="""
        <h2>What support covers</h2>
        <ul class="ticks">
          <li><span class="tick">&#10003;</span><span><strong>Issue resolution.</strong> Bugs, errors and unexpected behaviour investigated and fixed within your response SLA.</span></li>
          <li><span class="tick">&#10003;</span><span><strong>User questions.</strong> The "how do I…" queries that otherwise get answered wrongly by whoever sits nearest.</span></li>
          <li><span class="tick">&#10003;</span><span><strong>Patches and security updates.</strong> Applied and tested rather than left to accumulate.</span></li>
          <li><span class="tick">&#10003;</span><span><strong>Minor enhancements.</strong> Small changes to reports, views and workflows included from the Standard tier upward.</span></li>
          <li><span class="tick">&#10003;</span><span><strong>Version updates.</strong> Managed on your schedule, with regression testing on staging first.</span></li>
          <li><span class="tick">&#10003;</span><span><strong>Health reviews.</strong> Periodic checks on performance, data quality, backup integrity and adoption drift.</span></li>
        </ul>

        <div class="callout">
          <strong>Hypercare comes first</strong>
          The four weeks straight after go-live are when the real edge cases surface — the annual stocktake, the unusual credit note, the month-end close. Hypercare is included in every implementation, at no additional cost, before any AMC begins.
        </div>
""",
        extra=f"""
  <section class="soft">
    <div class="wrap">
      <div class="section-head reveal">
        <div class="eyebrow">AMC tiers</div>
        <h2>Choose your response time</h2>
        <p>Priced annually against the size of your deployment. The right tier depends on how long your business can operate with Odoo down.</p>
      </div>
{AMC_PLANS}
      <p class="terms-note">Response time is the time to a human engaging with your ticket, not to resolution. Resolution targets vary by severity and are agreed in the contract.</p>
    </div>
  </section>
""",
        related=[("implementation.html", "Implementation"), ("training.html", "Training"),
                 ("migration.html", "Version upgrades"), ("pricing.html", "Pricing")],
    ),
}

for fname, meta in SERVICE_CONTENT.items():
    crumb = f'<a href="services.html">Services</a><span>/</span><a href="{fname}">{meta["eyebrow"]}</a>'
    PAGES[fname] = dict(
        title=meta["title"],
        desc=meta["desc"],
        active="service",
        body=f"""{page_hero(crumb, meta["eyebrow"], meta["h1"], meta["sub"])}

  <section>
    <div class="wrap content-grid">
      <div class="prose reveal">{meta["prose"]}</div>
      {sidebar(meta["related"])}
    </div>
  </section>
{meta.get("extra", "")}
{CTA_BANNER}
""",
    )


# --------------------------------------------------------------------------
# Write it all out
# --------------------------------------------------------------------------
def main():
    for fname, page in PAGES.items():
        html = head(page["title"], page["desc"], page["active"],
                    page.get("body_class", "")) + page["body"] + FOOTER
        # collapse accidental triple blank lines
        html = re.sub(r"\n{3,}", "\n\n", html)
        (ROOT / fname).write_text(html, encoding="utf-8")
        print(f"  wrote {fname:22} {len(html):>7,} bytes")
    print(f"\n{len(PAGES)} pages built.")


if __name__ == "__main__":
    main()
