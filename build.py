#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TravelDore static site generator (v2).
Builds every HTML page from shared partials so the whole site stays
visually and structurally consistent. Run: python3 build.py
"""
import os, re, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "tools"))
from generate_images import make_plate

ROOT = os.path.dirname(os.path.abspath(__file__))

# ---------------------------------------------------------------------------
# Icon system — small, consistent line-icon set (24x24, stroke=currentColor)
# Replaces emoji for a cleaner, professional, classic look.
# ---------------------------------------------------------------------------
_ICON_PATHS = {
    "compass":  '<circle cx="12" cy="12" r="9"/><path d="M14.5 9.5 12.8 14a1 1 0 0 1-1.3 1.3L7 12l4.3-2.5a1 1 0 0 1 1.2 0z"/>',
    "map":      '<path d="M9 4 4 6v14l5-2 6 2 5-2V4l-5 2-6-2Z"/><path d="M9 4v14M15 6v14"/>',
    "gem":      '<path d="M6 3h12l3 5-9 13L3 8Z"/><path d="M3 8h18M9 3l3 5 3-5M9 21 8 8m7 13 1-13"/>',
    "refresh":  '<path d="M4 12a8 8 0 0 1 14-5.3L20 8"/><path d="M20 4v4h-4"/><path d="M20 12a8 8 0 0 1-14 5.3L4 16"/><path d="M4 20v-4h4"/>',
    "search":   '<circle cx="11" cy="11" r="7"/><path d="m20 20-3.5-3.5"/>',
    "handshake":'<path d="M8 12 3 9v6l5 3"/><path d="m16 12 5-3v6l-5 3"/><path d="M8 12h3l2 2 2-2h1"/><path d="M8 12 5 9l3-2 3 2"/><path d="M16 12l3-3-3-2-3 2"/>',
    "plane":    '<path d="M10.5 20 12 15l-6.5-1L4 16l1.5-6L3 8l1-3 8 2.5L18 3l2 2-4.5 6.5L18 20l-3-1.5-2 2.5-1-3.5-1.5 2Z"/>',
    "calendar": '<rect x="3.5" y="5" width="17" height="16" rx="1.5"/><path d="M8 3v4M16 3v4M3.5 10h17"/>',
    "family":   '<circle cx="8" cy="7" r="2.5"/><circle cx="16" cy="7" r="2.5"/><path d="M3 20v-2a5 5 0 0 1 5-5h0a5 5 0 0 1 5 5v2"/><path d="M13 13.5a5 5 0 0 1 8 4v2.5"/>',
    "heart":    '<path d="M12 20.5 4.7 13.3a5 5 0 0 1 7.3-6.8 5 5 0 0 1 7.3 6.8Z"/>',
    "globe":    '<circle cx="12" cy="12" r="9"/><path d="M3 12h18M12 3a14 14 0 0 1 0 18M12 3a14 14 0 0 0 0 18"/>',
    "users":    '<circle cx="9" cy="8" r="3"/><path d="M3 20a6 6 0 0 1 12 0"/><circle cx="17" cy="9" r="2.5"/><path d="M14.5 20a5 5 0 0 1 6.5-4.7"/>',
    "sparkle":  '<path d="M12 3v4M12 17v4M3 12h4M17 12h4M6 6l2.5 2.5M15.5 15.5 18 18M18 6l-2.5 2.5M8.5 15.5 6 18"/>',
    "home":     '<path d="M4 11 12 4l8 7"/><path d="M6 10v10h12V10"/><path d="M10 20v-6h4v6"/>',
    "car":      '<path d="M4 16V11l2-5h12l2 5v5"/><path d="M4 16h16M6 16v2M18 16v2"/><circle cx="7.5" cy="16" r="1.3"/><circle cx="16.5" cy="16" r="1.3"/>',
    "palm":     '<path d="M12 22V11"/><path d="M12 11c-2-4-6-5-9-3 2 3 5 4 9 3Z"/><path d="M12 11c2-4 6-5 9-3-2 3-5 4-9 3Z"/><path d="M12 11c0-4 1-7 3-9-3 0-5 3-3 9Z"/>',
    "mountain": '<path d="M3 19 9 8l4 6.5L15 11l6 8Z"/>',
    "leaf":     '<path d="M5 19c8 1 13-4 14-14-9 0-14 5-14 14Z"/><path d="M5 19c2-5 5-8 9-10"/>',
    "yoga":     '<circle cx="12" cy="5" r="1.8"/><path d="M12 8v6M6 20l6-6 6 6M8 12h8"/>',
    "sunrise":  '<path d="M12 4v3M4.2 15h15.6M6 9.5 8 11M18 9.5 16 11"/><path d="M6 15a6 6 0 0 1 12 0"/><path d="M3 19h18"/>',
    "wifi-off": '<path d="M2 8.5a16 16 0 0 1 4.6-2.7M21.5 8.5a16 16 0 0 0-6-3.2M6 12a10 10 0 0 1 4-2M18 12a10 10 0 0 0-3.4-1.9M9 15.5a5 5 0 0 1 6 0M12 19v.01M3 3l18 18"/>',
    "baby":     '<circle cx="12" cy="7" r="3"/><path d="M8 13c0 4 2 7 4 7s4-3 4-7"/><path d="M9 10c-2 0-3 1.5-2 3M15 10c2 0 3 1.5 2 3"/>',
    "briefcase":'<rect x="3" y="8" width="18" height="12" rx="1.5"/><path d="M8 8V6a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"/><path d="M3 13h18"/>',
    "boot":     '<path d="M8 3v8l-4 4v3a1 1 0 0 0 1 1h13a1 1 0 0 0 1-1c0-2-1-3-3-3.5L12 13V3Z"/><path d="M8 6h4"/>',
    "tent":     '<path d="M3 20 12 5l9 15"/><path d="M8.5 20 12 12l3.5 8"/><path d="M3 20h18"/>',
    "lion":     '<circle cx="12" cy="12" r="4"/><path d="M12 3v3M12 18v3M4 6l2 2M18 6l-2 2M4 18l2-2M18 18l-2-2M3 12h3M18 12h3"/>',
    "wine":     '<path d="M7 3h10l-1 8a4 4 0 0 1-8 0Z"/><path d="M12 13v6M8 21h8"/>',
    "hut":      '<path d="M4 20V11L12 5l8 6v9"/><path d="M9 20v-6h6v6"/>',
    "festival": '<path d="M4 21 8 9l4 12M12 21l4-16 4 16"/><circle cx="8" cy="6" r="1.3"/><circle cx="16" cy="4" r="1.3"/>',
    "masks":    '<circle cx="8.5" cy="10" r="5"/><circle cx="15.5" cy="12" r="5"/><path d="M6.5 9.5h1M10 9.5h1M13.5 12h1M17 12h1"/>',
    "train":    '<rect x="5" y="4" width="14" height="13" rx="3"/><path d="M5 12h14M8 21l-2-4M18 21l2-4"/><circle cx="9" cy="14.5" r="1"/><circle cx="15" cy="14.5" r="1"/>',
    "ship":     '<path d="M5 12V5h5V3h4v2h5v7"/><path d="M3 12h18l-2.5 7a2 2 0 0 1-1.9 1.4H7.4A2 2 0 0 1 5.5 19Z"/>',
    "ticket":   '<path d="M4 8a2 2 0 0 1 2-2h12a2 2 0 0 1 2 2v2a2 2 0 0 0 0 4v2a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2v-2a2 2 0 0 0 0-4Z"/><path d="M10 6v12" stroke-dasharray="2 2"/>',
    "moon":     '<path d="M20 14.5A8.5 8.5 0 1 1 9.5 4a7 7 0 0 0 10.5 10.5Z"/>',
    "camera":   '<rect x="3" y="7" width="18" height="13" rx="2"/><path d="M8 7 9.5 4h5L16 7"/><circle cx="12" cy="13.5" r="3.5"/>',
    "video":    '<rect x="3" y="6" width="12" height="12" rx="1.5"/><path d="m15 10 6-3v10l-6-3Z"/>',
    "graduate": '<path d="M2 9 12 4l10 5-10 5Z"/><path d="M6 11.5V16c0 1.7 2.7 3 6 3s6-1.3 6-3v-4.5"/><path d="M22 9v6"/>',
    "landmark": '<path d="M3 21h18M4 21V10M20 21V10M2 10l10-6 10 6M7 10v7M12 10v7M17 10v7"/>',
    "tool":     '<path d="M14.5 3.5a4 4 0 0 0-5 5L3 15l2 2 6.5-6.5a4 4 0 0 0 5-5Z"/>',
    "villa":    '<path d="M3 11 12 4l9 7"/><path d="M5 10v10h14V10"/><path d="M9 20v-5h6v5"/><path d="M9 13h6"/>',
    "island":   '<path d="M3 19c3-2 15-2 18 0"/><path d="M12 3v9"/><path d="M12 3c-2 2-2 4 0 6"/><circle cx="12" cy="14" r="3"/>',
    "concierge":'<circle cx="12" cy="7" r="3.2"/><path d="M5 20c0-4 3-6 7-6s7 2 7 6"/><path d="M9 4.5 12 2l3 2.5"/>',
    "location": '<path d="M12 21s7-6.5 7-12a7 7 0 0 0-14 0c0 5.5 7 12 7 12Z"/><circle cx="12" cy="9" r="2.5"/>',
    "mail":     '<rect x="3" y="5" width="18" height="14" rx="2"/><path d="m4 6.5 8 6.5 8-6.5"/>',
    "clock":    '<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3.5 2"/>',
    "chat":     '<path d="M4 5h16v11H8l-4 4Z"/>',
    "arrow":    '<path d="M5 12h14M13 6l6 6-6 6"/>',
    "check":    '<path d="M5 13l4 4L19 7"/>',
    "instagram":'<rect x="3" y="3" width="18" height="18" rx="5"/><circle cx="12" cy="12" r="4"/><circle cx="17.2" cy="6.8" r="1"/>',
    "facebook": '<path d="M14 21v-7h3l.5-4H14V8c0-1.2.4-2 2.2-2H18V2.2C17.6 2.1 16.3 2 14.9 2 11.8 2 10 3.9 10 7.3V10H7v4h3v7Z"/>',
    "whatsapp": '<path d="M12 3a9 9 0 0 0-7.8 13.4L3 21l4.7-1.2A9 9 0 1 0 12 3Z"/><path d="M8.5 8.6c.2-.5.4-.5.7-.5h.5c.2 0 .4 0 .6.5.2.5.7 1.7.7 1.8.1.1.1.3 0 .4-.1.2-.1.3-.3.5-.1.2-.3.3-.4.5-.1.1-.3.3-.1.6.2.3.8 1.3 1.7 2.1 1.2 1 2.1 1.4 2.4 1.5.3.1.5.1.6-.1.2-.2.7-.8.9-1.1.2-.3.4-.2.6-.1.2.1 1.5.7 1.8.8.3.2.5.2.5.4 0 .2 0 1-.4 1.5-.4.6-1.8 1.1-2.5 1.1-.6 0-1.6-.1-3.4-1.2-2.6-1.6-4.2-4.5-4.4-4.7-.1-.2-1-1.3-1-2.5 0-1.2.6-1.8.8-2Z" fill="currentColor" stroke="none"/>',
}

def icon(name, size="1em"):
    body = _ICON_PATHS.get(name, _ICON_PATHS["sparkle"])
    return f'<svg class="icon" style="width:{size};height:{size};" viewBox="0 0 24 24">{body}</svg>'

# ---------------------------------------------------------------------------
# Local placeholder photography (self-contained, no external network calls)
# ---------------------------------------------------------------------------
def img(seed, w=1600, h=1000, label="TravelDore", small=""):
    fname = make_plate(seed, w, h, label=label, small=small)
    return f"__IMGPATH__/{fname}"  # resolved to correct relative path per page depth

def rel(path, depth):
    return ("../" * depth) + path

def resolve_images(html, depth):
    """Replace placeholder image path markers with the correct relative path for this page depth."""
    return html.replace("__IMGPATH__/", rel("images/", depth))

print("Setup complete: icons + image system ready.")

# ---------------------------------------------------------------------------
# Shared partials
# ---------------------------------------------------------------------------

def head(title, desc, depth, extra_css=""):
    css = rel("css/style.css", depth)
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title} | TravelDore</title>
<meta name="description" content="{desc}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="stylesheet" href="{css}">
{extra_css}
</head>
<body>
<div id="loader"><div class="loader-mark">Travel<em>Dore</em></div><div class="loader-bar"></div></div>
<div id="scroll-progress"></div>
<div id="cursor-glow"></div>
"""

def navbar(depth):
    home = rel("index.html", depth)
    exp = rel("experiences/index.html", depth)
    gal = rel("gallery.html", depth)
    abo = rel("about.html", depth)
    testi = rel("index.html#testimonials", depth)
    book = rel("index.html#booking", depth)
    plan = rel("plan-my-journey.html", depth)
    con = rel("contact.html", depth)
    links = f"""
      <a href="{home}">Home</a>
      <a href="{exp}">Experiences</a>
      <a href="{gal}">Gallery</a>
      <a href="{abo}">About</a>
      <a href="{testi}">Testimonials</a>
      <a href="{book}">Booking</a>
      <a href="{con}">Contact</a>"""
    return f"""
<header id="site-header">
  <div class="container navbar">
    <a href="{home}" class="brand">Travel<em>Dore</em></a>
    <nav class="nav-links">{links}
    </nav>
    <a href="{plan}" class="btn btn-primary btn-sm nav-cta">Plan My Journey</a>
    <button class="nav-toggle" id="nav-toggle" aria-label="Open menu"><span></span><span></span><span></span></button>
  </div>
</header>
<div class="mobile-panel" id="mobile-panel">
  <button class="mobile-close" id="mobile-close" aria-label="Close menu">&times;</button>{links}
  <a href="{plan}" class="btn btn-primary" style="margin-top:22px;">Plan My Journey</a>
</div>
"""

def whatsapp():
    return f"""
<div id="wa-float" aria-label="Chat on WhatsApp">{icon('whatsapp','28px')}</div>
<div id="wa-box">
  <div class="wa-head">
    <div><strong>TravelDore Concierge</strong><div style="font-size:.7rem;opacity:.85;">Typically replies within an hour</div></div>
    <button id="wa-close" style="color:#fff;font-size:1.1rem;">&times;</button>
  </div>
  <div class="wa-body">
    <div class="wa-bubble">Namaste! Curious about a curated journey? Message us directly on WhatsApp and let's start planning.</div>
    <a class="wa-btn" href="https://wa.me/917046001515" target="_blank" rel="noopener">Start Chat</a>
  </div>
</div>
"""

def footer(depth):
    home = rel("index.html", depth)
    exp = rel("experiences/index.html", depth)
    gal = rel("gallery.html", depth)
    abo = rel("about.html", depth)
    con = rel("contact.html", depth)
    plan = rel("plan-my-journey.html", depth)
    e = lambda slug: rel(f"experiences/{slug}.html", depth)
    return f"""
<footer id="site-footer">
  <div class="container">
    <div class="footer-grid">
      <div class="footer-brand">
        <a href="{home}" class="brand">Travel<em>Dore</em></a>
        <p>An Art Of Exploration. Curated journeys designed to inspire, connect, and transform &mdash; crafted around you, not a standard itinerary.</p>
        <div class="footer-social">
          <a href="https://instagram.com" target="_blank" rel="noopener" aria-label="Instagram">{icon('instagram')}</a>
          <a href="https://facebook.com" target="_blank" rel="noopener" aria-label="Facebook">{icon('facebook')}</a>
          <a href="https://wa.me/917046001515" target="_blank" rel="noopener" aria-label="WhatsApp">{icon('whatsapp')}</a>
        </div>
      </div>
      <div class="footer-col">
        <h4>Explore</h4>
        <ul>
          <li><a href="{home}">Home</a></li>
          <li><a href="{exp}">Experiences</a></li>
          <li><a href="{gal}">Gallery</a></li>
          <li><a href="{abo}">About Us</a></li>
          <li><a href="{con}">Contact</a></li>
        </ul>
      </div>
      <div class="footer-col">
        <h4>Experiences</h4>
        <ul>
          <li><a href="{e('leisure-escapes')}">Leisure Escapes</a></li>
          <li><a href="{e('wellness-journeys')}">Wellness Journeys</a></li>
          <li><a href="{e('adventure-nature')}">Adventure &amp; Nature</a></li>
          <li><a href="{e('signature-experiences')}">Signature Experiences</a></li>
          <li><a href="{e('corporate-experiences')}">Corporate Experiences</a></li>
          <li><a href="{e('learning-purpose')}">Learning &amp; Purpose</a></li>
          <li><a href="{e('luxury-collection')}">Luxury Collection</a></li>
        </ul>
      </div>
      <div class="footer-col">
        <h4>Get In Touch</h4>
        <ul class="footer-contact">
          <li>{icon('whatsapp')}&nbsp; +91 70460 01515</li>
          <li>{icon('mail')}&nbsp; inquiry@traveldore.com</li>
          <li>{icon('clock')}&nbsp; 10 AM &ndash; 7 PM, Mon &ndash; Sat</li>
        </ul>
        <a href="{plan}" class="btn btn-outline btn-sm" style="border-color:rgba(255,255,255,.3);">Plan My Journey</a>
      </div>
    </div>
    <div class="footer-bottom">
      <span>&copy; 2026 TravelDore. All rights reserved.</span>
      <span>Founded by Vidhi Modi &mdash; Crafted with wanderlust.</span>
    </div>
  </div>
</footer>
"""

def scripts(depth):
    js = rel("js/main.js", depth)
    return f'<script src="{js}"></script>\n</body>\n</html>'

def page(title, desc, depth, body, extra_css=""):
    html = head(title, desc, depth, extra_css) + navbar(depth) + body + whatsapp() + footer(depth) + scripts(depth)
    return resolve_images(html, depth)

def write(path, content):
    full = os.path.join(ROOT, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "w", encoding="utf-8") as f:
        f.write(content)
    print("wrote", path)

# ---------------------------------------------------------------------------
# Shared content data
# ---------------------------------------------------------------------------

EXPERIENCES = [
    dict(slug="leisure-escapes", title="Leisure Escapes", ic="palm",
         tag="Weekend escapes to family holidays", seed="leisure-hero"),
    dict(slug="wellness-journeys", title="Wellness Journeys", ic="leaf",
         tag="Retreats for mind, body & soul", seed="wellness-hero"),
    dict(slug="adventure-nature", title="Adventure & Nature", ic="mountain",
         tag="For those who chase the wild", seed="adventure-hero"),
    dict(slug="signature-experiences", title="Signature Experiences", ic="sparkle",
         tag="Stories instead of sightseeing", seed="signature-hero"),
    dict(slug="corporate-experiences", title="Corporate Experiences", ic="briefcase",
         tag="Teams that grow together", seed="corporate-hero"),
    dict(slug="learning-purpose", title="Learning & Purpose", ic="graduate",
         tag="Journeys that change who you become", seed="learning-hero"),
    dict(slug="luxury-collection", title="Luxury Collection", ic="gem",
         tag="Exclusivity, privacy, extraordinary", seed="luxury-hero"),
]

WHY_CARDS = [
    ("concierge", "Personalized Concierge", "A dedicated travel concierge shapes every detail around you, from first inquiry to the moment you're home."),
    ("map", "Curated Experiences", "No fixed packages, no copy-paste itineraries — every journey is designed around your interests and pace."),
    ("gem", "Luxury Planning", "Handpicked stays, private transfers, and exceptional service woven into every stage of the journey."),
    ("refresh", "Flexible Itineraries", "Travel at your own rhythm. Every plan bends around you, never the other way around."),
    ("search", "Hidden Gems", "We go beyond the guidebooks to the places, people, and moments most travelers never discover."),
    ("handshake", "Authentic Local Connections", "Real conversations, real communities, real culture — travel that leaves something behind."),
]

STATS = [
    ("50+", "Journeys Curated"),
    ("99%", "Client Satisfaction"),
    ("24/7", "Travel Concierge"),
]

TESTIMONIALS = [
    ("TravelDore didn't just plan our honeymoon — they designed an experience we still talk about a year later. Every detail felt personal.", "Ananya & Rohan", "Couple Escape, Bali"),
    ("Our leadership offsite finally felt different. Beautiful venue, seamless logistics, and space to actually think.", "Karan Mehta", "Corporate Retreat, Rishikesh"),
    ("I've traveled solo before, but this was the first trip where I felt both free and completely taken care of.", "Simran Kaur", "Solo Trip, Vietnam"),
    ("The wellness retreat was exactly what I needed — no itinerary stress, just stillness, yoga, and the mountains.", "Devika Shah", "Wellness Retreat, Himachal"),
    ("From the first WhatsApp message to the last sunset, everything was effortless. This is how travel should feel.", "The Kapoor Family", "Family Holiday, Maldives"),
]

BOOKING_STEPS = [
    ("Discover", "Share your travel dreams through a short inquiry."),
    ("Talk to Concierge", "A dedicated expert understands your style & pace."),
    ("Customize", "Your itinerary is shaped around your preferences."),
    ("Book", "Confirm your journey with complete transparency."),
    ("Travel", "Experience it — seamless, effortless, immersive."),
    ("Share Memories", "Return home and tell us your story."),
]

GALLERY_ITEMS = [
    ("g1", "luxury", "Boutique villa terrace"),
    ("g2", "nature", "Himalayan sunrise trail"),
    ("g3", "food", "Street food trail, Vietnam"),
    ("g4", "culture", "Festival of colors"),
    ("g5", "adventure", "Sea kayaking at dawn"),
    ("g6", "people", "Local artisan at work"),
    ("g7", "luxury", "Private plunge pool"),
    ("g8", "nature", "Mountain lake reflection"),
    ("g9", "culture", "Heritage courtyard"),
    ("g10", "adventure", "Cliffside trekking"),
    ("g11", "food", "Candlelit dinner by the sea"),
    ("g12", "people", "Conversations on the road"),
    ("g13", "luxury", "Cabin above the clouds"),
    ("g14", "nature", "Island cove at low tide"),
    ("g15", "culture", "Lantern-lit old town"),
    ("g16", "adventure", "White-water rafting"),
]

def purpose_chips():
    return "".join(
        f'<button type="button" class="purpose-chip{" active" if i==0 else ""}" data-value="{e["title"]}">{icon(e["ic"])} {e["title"]}</button>'
        for i, e in enumerate(EXPERIENCES)
    )

# ---------------------------------------------------------------------------
# Reusable section builders
# ---------------------------------------------------------------------------

def ornament():
    return '<div class="ornament"><span class="diamond"></span></div>'

def stats_band():
    items = "".join(f'<div class="stat"><div class="stat-num">{n}</div><div class="stat-label">{l}</div></div>' for n, l in STATS)
    return f'<section class="stats-band"><div class="container stats-grid">{items}</div></section>'

def why_section():
    cards = "".join(f'''
      <div class="why-card">
        <div class="why-icon">{icon(ic)}</div>
        <h3>{title}</h3>
        <p>{copy}</p>
      </div>''' for ic, title, copy in WHY_CARDS)
    return f'''
<section class="section" id="why">
  <div class="container">
    <div class="section-head reveal">
      <div class="eyebrow" style="justify-content:center;">Why TravelDore</div>
      <h2>Extraordinary journeys don't happen by chance.</h2>
      <p>Anyone can book flights and hotels. We curate experiences that feel personal, effortless, and unforgettable — designed around you, not a standard itinerary.</p>
    </div>
    <div class="why-grid stagger">{cards}
    </div>
  </div>
</section>'''

def experiences_section(depth):
    cards = ""
    for i, e in enumerate(EXPERIENCES):
        href = rel(f"experiences/{e['slug']}.html", depth)
        cards += f'''
      <a href="{href}" class="exp-card reveal-scale">
        <img src="{img(e['seed'],900,1100,e['title'])}" alt="{e['title']}" loading="lazy">
        <div class="exp-card-veil"></div>
        <div class="exp-card-content">
          <span class="exp-card-num">{icon(e['ic'])} 0{i+1}</span>
          <h3>{e['title']}</h3>
          <div class="exp-card-arrow">{icon('arrow')}</div>
        </div>
      </a>'''
    return f'''
<section class="section bg-lilac" id="experiences">
  <div class="container">
    <div class="section-head reveal">
      <div class="eyebrow" style="justify-content:center;">Explore Experiences</div>
      <h2>Seven ways to explore the world</h2>
      <p>From weekend escapes to legendary train journeys — every path is curated, never generic.</p>
    </div>
    <div class="exp-grid">{cards}
    </div>
  </div>
</section>'''

def gallery_section(depth, limit=None, show_filters=True):
    gal = rel("gallery.html", depth)
    items = GALLERY_ITEMS if limit is None else GALLERY_ITEMS[:limit]
    cards = ""
    heights = [520, 400, 460, 620, 380, 500, 440, 560]
    for i, (gid, cat, label) in enumerate(items):
        h = heights[i % len(heights)]
        cards += f'''
      <div class="masonry-item reveal" data-category="{cat}">
        <img src="{img(gid,700,h,label)}" alt="{label}" loading="lazy">
        <div class="masonry-veil"><span>{label}</span></div>
      </div>'''
    filters = ""
    if show_filters:
        cats = ["all", "luxury", "culture", "nature", "adventure", "people", "food"]
        filters = '<div class="gallery-filters">' + "".join(
            f'<button class="filter-btn{" active" if c=="all" else ""}" data-filter="{c}">{c.capitalize()}</button>' for c in cats
        ) + '</div>'
    cta = "" if limit is None else f'<div class="center mt-lg"><a href="{gal}" class="btn btn-ghost">View Full Gallery</a></div>'
    return f'''
<section class="section" id="gallery">
  <div class="container">
    <div class="section-head reveal">
      <div class="eyebrow" style="justify-content:center;">Gallery</div>
      <h2>Moments, not just destinations</h2>
      <p>A Pinterest-style journey through luxury, culture, nature, and the everyday beauty of travel.</p>
    </div>
    {filters}
    <div class="masonry">{cards}
    </div>
    {cta}
  </div>
</section>
<div id="lightbox"><button class="lb-close">&times;</button><img id="lb-img" src="" alt="Gallery preview"></div>'''

def testimonials_section():
    slides = "".join(f'''
      <div class="testi-slide">
        <div class="testi-card">
          <div class="testi-quote">&ldquo;</div>
          <div class="testi-stars">&#9733;&#9733;&#9733;&#9733;&#9733;</div>
          <p class="testi-text">{quote}</p>
          <div class="testi-name">{name}</div>
          <div class="testi-role">{role}</div>
        </div>
      </div>''' for quote, name, role in TESTIMONIALS)
    return f'''
<section class="section bg-lilac" id="testimonials">
  <div class="container">
    <div class="section-head reveal">
      <div class="eyebrow" style="justify-content:center;">Testimonials</div>
      <h2>Stories from our travelers</h2>
    </div>
    <div class="testi-wrap reveal">
      <div class="testi-track"><div class="testi-slides" id="testi-slides">{slides}
      </div></div>
      <div class="testi-nav">
        <button class="testi-arrow" id="testi-prev" aria-label="Previous">{icon('arrow')}</button>
        <button class="testi-arrow" id="testi-next" aria-label="Next" style="transform:scaleX(-1);">{icon('arrow')}</button>
      </div>
      <div class="testi-dots" id="testi-dots"></div>
    </div>
  </div>
</section>'''

def booking_section():
    steps = "".join(f'''
      <div class="tl-step">
        <div class="tl-num">{i+1}</div>
        <h4>{t}</h4>
        <p>{d}</p>
      </div>''' for i, (t, d) in enumerate(BOOKING_STEPS))
    return f'''
<section class="section" id="booking">
  <div class="container">
    <div class="section-head reveal">
      <div class="eyebrow" style="justify-content:center;">Booking Process</div>
      <h2>From first inquiry to lasting memory</h2>
      <p>A simple, guided path — because planning a journey should feel as good as taking one.</p>
    </div>
    <div class="timeline stagger">{steps}
    </div>
  </div>
</section>'''

def inquiry_section(depth):
    chips = purpose_chips()
    return f'''
<section class="section" id="plan">
  <div class="container">
    <div class="form-panel reveal-scale">
      <div class="section-head align-left" style="margin-bottom:38px;max-width:640px;">
        <div class="eyebrow" style="color:var(--gold-soft);">Plan My Journey</div>
        <h2 style="color:#fff;">Tell us what you're dreaming of</h2>
        <p style="color:rgba(255,255,255,.75);">Share a few details and your dedicated concierge will reach out within 24 hours.</p>
      </div>
      <form id="inquiry-form">
        <div class="form-grid">
          <div class="field"><label for="name">Name</label><input type="text" id="name" name="name" placeholder="Your full name" required></div>
          <div class="field"><label for="email">Email</label><input type="email" id="email" name="email" placeholder="you@email.com" required></div>
          <div class="field"><label for="phone">Phone</label><input type="tel" id="phone" name="phone" placeholder="+91 00000 00000" required></div>
          <div class="field"><label for="city">City</label><input type="text" id="city" name="city" placeholder="Where you're travelling from" required></div>
        </div>
        <div class="field" style="margin-top:24px;">
          <label>Travel Purpose</label>
          <div class="purpose-scroll">{chips}</div>
          <input type="hidden" id="purpose-value" name="purpose" value="{EXPERIENCES[0]['title']}">
        </div>
        <div class="form-grid full" style="margin-top:24px;">
          <div class="field"><label for="msg">What's in your mind? (optional)</label><textarea id="msg" name="message" rows="4" placeholder="Tell us a little about the journey you're imagining..."></textarea></div>
        </div>
        <div class="form-submit"><button type="submit" class="btn btn-primary">Submit Inquiry</button>
          <p class="form-note">We typically respond within 24 hours, Monday to Saturday.</p>
        </div>
      </form>
      <div class="form-success" id="form-success">
        <div class="tick">{icon('check')}</div>
        <h3 style="color:#fff;font-family:var(--font-display);font-size:1.7rem;">Thank you!</h3>
        <p>Your inquiry has been received. Our concierge team will reach out shortly — or message us on WhatsApp for an instant reply.</p>
      </div>
    </div>
  </div>
</section>'''

def instagram_section():
    seeds = ["ig1","ig2","ig3","ig4","ig5","ig6"]
    items = "".join(f'''
      <a href="https://instagram.com" target="_blank" rel="noopener" class="insta-item reveal">
        <img src="{img(s,500,500,'@traveldore')}" alt="TravelDore on Instagram" loading="lazy">
        <div class="insta-veil">{icon('instagram','1.3rem')}</div>
      </a>''' for s in seeds)
    return f'''
<section class="section bg-lilac">
  <div class="container">
    <div class="section-head reveal">
      <div class="eyebrow" style="justify-content:center;">@traveldore</div>
      <h2>Follow the journey</h2>
    </div>
    <div class="insta-grid">{items}
    </div>
  </div>
</section>'''

def cta_band(depth, title, subtitle, btn_text="Plan My Journey", seed="cta-band"):
    plan = rel("plan-my-journey.html", depth)
    return f'''
<section class="section">
  <div class="container">
    <div class="cta-band reveal-scale">
      <div class="hero-media"><img src="{img(seed,1600,700,title)}" alt=""></div>
      <div class="cta-band-content">
        <h2>{title}</h2>
        <p>{subtitle}</p>
        <a href="{plan}" class="btn btn-primary">{btn_text}</a>
      </div>
    </div>
  </div>
</section>'''

# ---------------------------------------------------------------------------
# Experience page content (from TravelDore master content doc)
# Each category tuple: (icon_key, title, lede, bullets[5])
# ---------------------------------------------------------------------------

EXPERIENCE_CONTENT = {
"leisure-escapes": dict(
    heading="Leisure Escapes", seed="leisure-hero",
    intro="Travel isn't about ticking destinations off a list. It's about collecting moments you'll never want to forget. Whether you're escaping the everyday, celebrating life's milestones, or simply chasing a change of scenery, our Leisure Escapes are thoughtfully curated to match your travel style — effortless, immersive, and filled with experiences that stay with you long after you've returned home.",
    categories=[
        ("calendar","Weekend Escapes","Sometimes, all you need is two days to reset.",
         ["Quick getaways that feel like a complete escape","Hidden gems just a drive or short flight away","Perfect for spontaneous plans and last-minute adventures","Slow mornings, scenic sunsets, and zero Monday blues","Handpicked stays with unforgettable experiences"]),
        ("plane","Leisure Travel","Travel simply because your soul needs it.",
         ["Personalized vacations designed around your interests","A perfect balance of relaxation, exploration, and local culture","Discover destinations beyond the usual tourist trail","Travel at your pace — no rushing, no compromises","Every itinerary crafted with care, not copied from a brochure"]),
        ("family","Family Holidays","Because the best family stories begin on the road.",
         ["Experiences every generation can enjoy together","Kid-friendly adventures without compromising on luxury","Create traditions that become lifelong memories","Safe, seamless, and thoughtfully planned family journeys","Less planning, more quality time"]),
        ("heart","Couple Escapes","For anniversaries, proposals, honeymoons — or just because.",
         ["Romantic stays with breathtaking views","Private experiences designed for meaningful moments","Candlelit dinners, hidden beaches, and unforgettable sunsets","Luxury escapes where every detail feels personal","Celebrate love beyond ordinary vacations"]),
        ("globe","Solo Trips","The greatest journey is often the one you take with yourself.",
         ["Travel confidently with curated solo-friendly experiences","Meet like-minded travelers along the way","Discover new places — and a new version of yourself","Safe, flexible, and empowering adventures","Freedom to explore exactly how you want"]),
        ("users","Group Tours","Great destinations become unforgettable with great company.",
         ["Small, curated groups — not crowded bus tours","Shared adventures with people who love to explore","Authentic local experiences beyond sightseeing","Perfect balance of planned activities and free time","Come as strangers, leave with lifelong friendships"]),
        ("sparkle","Luxury Holidays","Travel where every detail feels exceptional.",
         ["Handpicked luxury hotels and boutique stays","Private experiences crafted around your preferences","Exclusive dining, unique experiences, and premium comfort","Personalized concierge service from start to finish","Luxury that's defined by experiences, not extravagance"]),
        ("home","Luxury Staycations","You don't have to travel far to escape beautifully.",
         ["Discover extraordinary stays closer to home","Boutique resorts, heritage properties, and hidden retreats","Perfect for quick celebrations or peaceful weekends","Indulge without the hassle of long-distance travel","Relax, recharge, and reconnect"]),
        ("car","Road Trips","Because the journey should be as memorable as the destination.",
         ["Scenic routes you'll want to drive again and again","Charming cafés, hidden viewpoints, and local discoveries","Flexible itineraries with room for spontaneous detours","Curated playlists, pit stops, and unforgettable landscapes","Every mile becomes part of the adventure"]),
        ("palm","Island Escapes","Trade notifications for ocean waves.",
         ["Crystal-clear waters, quiet beaches, and endless horizons","Relaxation meets unforgettable island adventures","Sunset cruises, snorkeling, and hidden coves","Handpicked island stays for every travel style","Slow down, breathe deeply, and let the sea set the pace"]),
        ("mountain","Mountain Escapes","Find peace where the air is crisp and the views never end.",
         ["Cozy cabins, luxury lodges, and scenic mountain retreats","Sunrise hikes and evenings by the fire","Nature, adventure, and complete tranquility","Escape the noise and reconnect with what matters","Every mountain has a story waiting to be discovered"]),
        ("globe","International Tours","Explore the world beyond postcards.",
         ["Curated international journeys designed around experiences, not checklists","Discover iconic landmarks alongside hidden local gems","Seamless planning — from visas to unforgettable moments","Immerse yourself in cultures, cuisines, and stories that inspire","Travel confidently, knowing every detail is taken care of"]),
    ],
    closing="More than a vacation. More than a destination. At TravelDore, every Leisure Escape is thoughtfully curated to help you slow down, reconnect, celebrate, and return with stories worth telling — not just photos worth posting."
),

"wellness-journeys": dict(
    heading="Wellness Journeys", seed="wellness-hero",
    intro="Sometimes the best destination isn't a place — it's a better version of yourself. In a world that rarely slows down, Wellness Journeys are an invitation to pause, breathe, and reconnect. Every experience is thoughtfully designed to nourish your mind, body, and soul, because true luxury is returning home feeling lighter than when you left.",
    categories=[
        ("leaf","Wellness Retreats","Step away from the chaos and into complete calm.",
         ["Slow down in destinations designed for rest and renewal","Reconnect with yourself through immersive wellness experiences","Nourish your body, mind, and soul with mindful living","Thoughtfully curated stays where every detail encourages balance","Return home feeling refreshed — not like you need another vacation"]),
        ("yoga","Yoga Retreats","Find your balance — on and off the mat.",
         ["Practice yoga in breathtaking locations that inspire stillness","Suitable for beginners, seasoned practitioners, and everyone in between","Blend mindful movement with meaningful travel experiences","Sunrise sessions, nature walks, and moments of complete presence","A journey that strengthens both your body and your perspective"]),
        ("sunrise","Meditation Retreats","Disconnect from distractions. Reconnect with yourself.",
         ["Escape the constant noise of everyday life","Discover the power of silence, mindfulness, and intentional living","Peaceful environments that encourage clarity and self-reflection","Guided experiences designed to help you slow your thoughts and calm your mind","Leave with a quieter mind and a fuller heart"]),
        ("wifi-off","Digital Detox Retreats","Because life feels different when you're fully present.",
         ["Trade screen time for sunrise views and meaningful conversations","Unplug from notifications and reconnect with the world around you","Experience the freedom of being truly offline","Replace endless scrolling with unforgettable moments","A reminder that the best connections don't need Wi-Fi"]),
        ("baby","Babymoon","Celebrate the beautiful journey before your greatest adventure begins.",
         ["Peaceful escapes designed for expecting parents","Relaxing stays where comfort, wellness, and care come first","Gentle experiences created to help you unwind together","Celebrate this once-in-a-lifetime chapter before welcoming your little one","Create beautiful memories before life changes in the most wonderful way"]),
        ("briefcase","Employee Wellness","Healthy teams create stronger organizations.",
         ["Curated wellness experiences that help employees recharge and reconnect","Encourage better work-life balance beyond the office walls","Mindfulness sessions, wellness activities, and meaningful team experiences","Reduce burnout while strengthening morale and collaboration","Because investing in your people is the best investment a company can make"]),
    ],
    closing="Wellness isn't about escaping life — it's about returning to it with more energy, clarity, and purpose. At TravelDore, every Wellness Journey is carefully curated to help you slow down, recharge, and reconnect with what truly matters."
),

"adventure-nature": dict(
    heading="Adventure & Nature", seed="adventure-hero",
    intro="The best stories begin where your comfort zone ends. Adventure isn't about how far you travel — it's about how deeply you experience the world. From misty mountains and untamed forests to open roads and untouched islands, every journey is designed for those who seek more than sightseeing.",
    categories=[
        ("boot","Adventure Tours","For those who believe ordinary was never an option.",
         ["Go beyond the guidebooks and into unforgettable adventures","Experience destinations through thrilling, immersive activities","Discover hidden trails, breathtaking landscapes, and authentic local experiences","Every itinerary balances excitement with comfort and safety","Because the best memories are made outside your comfort zone"]),
        ("tent","Camping","Sleep under a sky full of stars, not city lights.",
         ["Wake up to birdsong instead of alarm clocks","Camp in handpicked locations surrounded by nature's beauty","Evenings around a campfire, stories that last a lifetime","Disconnect from routines and reconnect with the outdoors","Experience simplicity in its most beautiful form"]),
        ("lion","Wildlife Expeditions","Witness nature exactly as it was meant to be.",
         ["Explore some of the world's most incredible wildlife habitats","Observe magnificent animals in their natural environment","Guided experiences that respect nature and promote responsible tourism","Every safari and expedition is a chance to discover something extraordinary","Because some encounters can never be captured — they're simply unforgettable"]),
        ("mountain","Mountain Escapes","Find freedom where the air is fresher and the views stretch forever.",
         ["Escape to majestic peaks, peaceful valleys, and breathtaking landscapes","Perfect for adventure seekers and slow travelers alike","Discover scenic hikes, hidden villages, and unforgettable viewpoints","Cozy stays that combine comfort with spectacular surroundings","Every mountain reminds us how beautifully small we are"]),
        ("car","Road Trips","The destination is just one chapter of the journey.",
         ["Cruise along scenic routes filled with unexpected discoveries","Stop wherever curiosity leads — from hidden cafés to panoramic viewpoints","Flexible itineraries with the freedom to explore at your own pace","Every turn reveals a new story waiting to unfold","Because the open road has a way of making you feel limitless"]),
        ("palm","Island Escapes","Where every wave invites you to slow down.",
         ["Discover pristine beaches, turquoise waters, and hidden island treasures","Balance adventure with moments of complete relaxation","Snorkel vibrant reefs, chase sunsets, and embrace island life","Handpicked stays that let you wake up to the sound of the sea","Leave behind the noise and find your own slice of paradise"]),
    ],
    closing="Adventure isn't measured by distance — it's measured by the moments that take your breath away. At TravelDore, every Adventure & Nature experience is thoughtfully curated to awaken your curiosity and reconnect you with the beauty of the world."
),

"signature-experiences": dict(
    heading="Signature Experiences", seed="signature-hero",
    intro="Some journeys can't be searched. They have to be curated. This is where TravelDore truly comes alive — designed for curious travelers who seek stories instead of sightseeing, moments instead of milestones, and memories that can't be booked with a simple click.",
    categories=[
        ("wine","Food Trails","Taste a destination the way locals do.",
         ["Follow the flavors that define a region — not just the restaurants everyone knows","Meet local chefs, family kitchens, and hidden culinary gems","Discover stories behind every spice, recipe, and tradition","From bustling street food to unforgettable fine dining experiences","Because every destination tells its story through its food"]),
        ("hut","Hidden India","Discover the India that guidebooks often overlook.",
         ["Venture beyond famous landmarks into places rich with untold stories","Explore forgotten villages, secret viewpoints, and hidden cultural treasures","Meet artisans, local communities, and traditions passed down for generations","Experience India's incredible diversity through authentic local connections","Travel deeper, not just farther"]),
        ("festival","Festival Experiences","Celebrate the world the way locals do.",
         ["Witness traditions that transform destinations into unforgettable celebrations","Immerse yourself in music, colors, rituals, and centuries-old customs","Experience festivals beyond the crowds with thoughtfully curated access","Celebrate moments that bring communities together","Every festival is more than an event — it's a story waiting to be lived"]),
        ("masks","Cultural Experiences","Travel beyond attractions and into authentic human connections.",
         ["Experience traditions, art, music, and local ways of life firsthand","Meet the people who make every destination unique","Participate in meaningful experiences instead of simply observing them","Discover the soul of a place through its culture","Because the best souvenirs are the stories you bring home"]),
        ("train","Luxury Train Journeys","Rediscover the romance of slow travel.",
         ["Journey through breathtaking landscapes in timeless elegance","Experience world-class hospitality while the scenery unfolds outside your window","Every stop reveals a new destination, every mile a new memory","Where the journey itself becomes the highlight","Travel in comfort, style, and old-world charm"]),
        ("ship","Luxury Cruises","Let the ocean become your pathway to extraordinary experiences.",
         ["Wake up to a new destination without ever unpacking twice","Indulge in exceptional dining, entertainment, and world-class service","Explore iconic ports alongside hidden coastal gems","Relax, unwind, and let every horizon inspire you","Luxury isn't just where you stay — it's how you travel"]),
        ("ticket","Event Tourism","Travel because some moments deserve to be experienced live.",
         ["From global sporting events to iconic concerts and exclusive exhibitions","Build your journey around experiences you'll remember forever","Seamlessly combine premium travel with unforgettable events","Enjoy carefully planned itineraries that make every moment effortless","Because some memories are worth crossing borders for"]),
        ("moon","Nightlife Tourism","Discover a destination after the sun goes down.",
         ["Experience vibrant nightlife beyond the typical tourist spots","Hidden cocktail bars, rooftop lounges, live music, and local entertainment","Explore cities through their evening culture and energy","Curated nights designed for unforgettable conversations and experiences","Every city tells a different story after dark"]),
        ("camera","Photography Tours","For those who chase moments worth capturing.",
         ["Visit destinations through the eyes of a storyteller","Discover sunrise viewpoints, hidden alleys, and breathtaking landscapes","Learn tips from experienced photographers while exploring","Perfect for beginners, hobbyists, and professionals alike","Capture more than photos — capture emotions"]),
        ("globe","Photography Expeditions","Go beyond the postcard and into the extraordinary.",
         ["Multi-day journeys designed around light, landscapes, and once-in-a-lifetime moments","Access remote locations few photographers ever experience","Chase wildlife, dramatic scenery, and authentic cultural encounters","Travel with fellow creators who share your passion for storytelling","Because the world's greatest shots are rarely found on the easiest paths"]),
    ],
    closing="Not every experience can be booked. Some have to be discovered. At TravelDore, our Signature Experiences are the heart of who we are — built around stories, emotions, and extraordinary moments most travelers never get to experience."
),

"corporate-experiences": dict(
    heading="Corporate Experiences", seed="corporate-hero",
    intro="Great teams aren't built in boardrooms — they're built through shared experiences. At TravelDore, we design corporate experiences that inspire collaboration, strengthen leadership, celebrate achievements, and create meaningful connections beyond the workplace.",
    categories=[
        ("handshake","Corporate Retreats","Step away from the office to think bigger.",
         ["Escape the everyday and create space for fresh ideas","Blend strategy, collaboration, and relaxation into one seamless experience","Strengthen team relationships in inspiring destinations","Carefully curated retreats designed around your business goals","Because the best breakthroughs often happen outside the meeting room"]),
        ("briefcase","Leadership Retreats","Inspire leaders to think beyond the next quarter.",
         ["Exclusive retreats designed for founders, executives, and leadership teams","Encourage strategic thinking in environments that spark creativity","Balance productive sessions with meaningful downtime","Build stronger leadership through shared experiences","Create the space where vision becomes action"]),
        ("globe","Annual Offsites","Turn your annual gathering into an experience everyone looks forward to.",
         ["Move beyond hotel conference rooms and predictable agendas","Combine business objectives with memorable experiences","Celebrate milestones, align teams, and strengthen company culture","Seamlessly planned from logistics to leisure","Because great companies deserve unforgettable gatherings"]),
        ("users","Team Building","Build stronger teams through shared adventures.",
         ["Replace ordinary activities with meaningful experiences that bring people closer","Foster trust, collaboration, and communication in natural settings","Fun, engaging activities designed to strengthen real workplace relationships","Create memories that continue long after the trip ends","Stronger teams begin with stronger connections"]),
        ("sparkle","Reward Trips","Celebrate success with experiences worth earning.",
         ["Recognize achievements with unforgettable travel experiences","Luxury getaways designed to motivate and inspire","Reward your top performers with something they'll truly remember","Personalized itineraries that reflect your company's appreciation","Because exceptional work deserves exceptional rewards"]),
        ("compass","Workations","Where productivity meets inspiration.",
         ["Trade office walls for inspiring destinations","Blend focused work with meaningful travel experiences","Premium stays with reliable workspaces and exceptional comfort","Encourage creativity, collaboration, and work-life balance","Because sometimes a change of scenery changes everything"]),
        ("ticket","Conference Planning","Professional events, seamlessly delivered.",
         ["End-to-end planning for conferences, summits, and corporate gatherings","Venue selection, accommodation, logistics, and guest experiences — all managed with precision","Create events that feel polished, engaging, and memorable","Focus on your attendees while we handle every detail","From planning to execution, we've got it covered"]),
        ("leaf","Employee Wellness","Invest in your people — the results will speak for themselves.",
         ["Wellness-focused experiences designed to reduce burnout and improve wellbeing","Mindfulness, nature, movement, and meaningful team connections","Help employees return refreshed, motivated, and re-energized","Encourage healthier work-life balance through thoughtfully curated journeys","Because thriving people build thriving organizations"]),
    ],
    closing="More than business travel. A catalyst for stronger teams. Our Corporate Experiences are thoughtfully curated to help businesses inspire their people and create moments that leave a lasting impact — long after everyone returns to the office."
),

"learning-purpose": dict(
    heading="Learning & Purpose", seed="learning-hero",
    intro="The most meaningful journeys don't just change where you've been — they change who you become. At TravelDore, our Learning & Purpose experiences are designed for curious minds, compassionate hearts, and lifelong learners.",
    categories=[
        ("graduate","Kids Educational Travel","Because the world's greatest classroom has no walls.",
         ["Turn curiosity into unforgettable real-world learning experiences","Explore history, science, wildlife, culture, and innovation beyond textbooks","Interactive journeys designed to inspire young minds","Safe, engaging, and age-appropriate experiences for every learner","Because some lessons are best learned through exploration"]),
        ("heart","Volunteer Experiences","Travel with purpose. Leave a positive impact.",
         ["Become part of meaningful community and conservation initiatives","Connect with local people through authentic, responsible experiences","Give back while gaining a deeper understanding of the places you visit","Create memories that matter — not just for you, but for others too","Because the best journeys leave something behind, not just footprints"]),
        ("video","Creator Trips","Designed for storytellers, dreamers, and creative minds.",
         ["Explore extraordinary destinations with fellow creators","Discover breathtaking locations perfect for photography, filmmaking, and content creation","Curated experiences that inspire fresh ideas and authentic storytelling","Collaborate, learn, and create in environments that spark creativity","Because every great creator deserves unforgettable stories to tell"]),
        ("graduate","Student Expeditions","Learning becomes unforgettable when it's experienced firsthand. (Coming Soon)",
         ["Educational journeys designed to broaden perspectives beyond the classroom","Explore destinations that inspire curiosity, leadership, and global awareness","Interactive experiences that combine travel with hands-on learning","Build confidence, independence, and lifelong friendships","Because education should be as exciting as discovery itself"]),
        ("landmark","Heritage Learning","Every monument has a story. Every culture has a lesson. (Coming Soon)",
         ["Step into history through immersive cultural experiences","Discover ancient traditions, architecture, and local heritage","Learn from historians, artisans, and communities preserving timeless legacies","Understand the stories that shaped civilizations","Because appreciating the past helps us understand the present"]),
        ("tool","Skill-Based Travel","Return with more than souvenirs — return with new skills. (Coming Soon)",
         ["Learn from local experts through immersive workshops and experiences","Explore culinary arts, photography, craftsmanship, wellness, and more","Combine travel with personal and professional growth","Every destination becomes an opportunity to learn something new","Because the best investment you can make is in yourself"]),
        ("graduate","University Tours","Helping students explore possibilities beyond borders. (Coming Soon)",
         ["Visit world-renowned universities and inspiring academic campuses","Gain insights into international education and student life","Meet experts, attend information sessions, and explore future opportunities","Designed for students and families planning global education journeys","Because every great future begins with informed choices"]),
    ],
    closing="Travel isn't just about seeing the world — it's about growing through it. Our Learning & Purpose experiences are designed to leave you richer in perspective, not just in passport stamps."
),

"luxury-collection": dict(
    heading="The Luxury Collection", seed="luxury-hero",
    intro="Luxury isn't about spending more — it's about experiencing more. At TravelDore, luxury is deeply personal: waking up to breathtaking views, enjoying experiences crafted exclusively for you, and knowing every detail has been thoughtfully taken care of.",
    categories=[
        ("sparkle","Luxury Holidays","Travel where every detail is thoughtfully crafted.",
         ["Handpicked destinations paired with exceptional stays and unforgettable experiences","Private transfers, premium accommodations, and personalized itineraries","Indulge in authentic experiences that go beyond traditional luxury","Travel at your own pace with every moment tailored to your preferences","Because true luxury is having every detail taken care of before you even think about it"]),
        ("ship","Luxury Cruises","Discover the world from a different horizon.",
         ["Sail through iconic coastlines and hidden destinations in complete comfort","World-class hospitality, fine dining, and breathtaking ocean views","Wake up to a new destination without ever repacking your suitcase","Curated shore experiences that make every stop unforgettable","Let every sunrise over the sea become part of your story"]),
        ("train","Luxury Train Journeys","Experience the timeless elegance of slow travel.",
         ["Journey through spectacular landscapes aboard some of the world's most iconic luxury trains","Elegant cabins, exceptional service, and unforgettable dining experiences","Watch breathtaking scenery unfold from the comfort of your private suite","Rediscover the romance of travel where the journey is just as extraordinary as the destination","Because some adventures are meant to be savored, not rushed"]),
        ("home","Luxury Staycations","Escape without going far.",
         ["Discover extraordinary retreats just a short journey from home","Boutique resorts, heritage palaces, and secluded hideaways","Perfect for celebrations, anniversaries, or simply pressing pause","Experience five-star comfort without the stress of long-distance travel","Sometimes the most luxurious getaway is the one that's closest to you"]),
        ("villa","Private Villas","Your own sanctuary, your own pace.",
         ["Stay in exclusive villas where privacy meets unparalleled comfort","Perfect for families, couples, celebrations, or intimate group escapes","Enjoy private pools, personalized services, and breathtaking surroundings","Create unforgettable moments in spaces designed just for you","Because luxury is having a place that feels entirely your own"]),
        ("island","Private Islands","The ultimate escape, reserved for a select few. (Coming Soon)",
         ["Experience unmatched privacy surrounded by crystal-clear waters","Curated island retreats designed for complete exclusivity","Personalized experiences tailored entirely around you","Luxury redefined through serenity, space, and extraordinary service","Because sometimes paradise should belong only to you"]),
        ("concierge","Bespoke Concierge","Travel designed around you — not the other way around. (Coming Soon)",
         ["Every itinerary begins with understanding your dreams, not selling a package","From exclusive reservations to once-in-a-lifetime experiences, every detail is personalized","Private guides, luxury transportation, hidden experiences, and seamless planning","Dedicated support before, during, and after your journey","Because no two travelers — and no two journeys — should ever be the same"]),
    ],
    closing="Luxury isn't measured by stars — it's measured by how a journey makes you feel. Every detail is thoughtfully curated so you can simply arrive, unwind, and experience the extraordinary."
),
}

# ---------------------------------------------------------------------------
# Page: HOME
# ---------------------------------------------------------------------------
def build_home():
    depth = 0
    hero = f'''
<section class="hero">
  <div class="hero-media"><img src="{img('hero-main',1920,1200,'An Art Of Exploration','TravelDore')}" alt="Cinematic travel landscape"></div>
  <div class="container hero-content">
    <span class="hero-eyebrow">TravelDore</span>
    <h1>An <em>Art</em> Of Exploration</h1>
    <p>Curated journeys designed to inspire, connect, and transform.</p>
    <div class="hero-actions">
      <a href="#experiences" class="btn btn-primary">Explore Experiences</a>
      <a href="plan-my-journey.html" class="btn btn-outline">Plan My Journey</a>
    </div>
  </div>
  <div class="hero-scroll"><span>Scroll</span><div class="dot"></div></div>
</section>'''

    about = f'''
<section class="section" id="about">
  <div class="container about-grid">
    <div class="framed reveal-scale">
      <div class="media-inner"><img src="{img('about-founder',900,1100,'TravelDore')}" alt="TravelDore curated experience"></div>
      <div class="about-badge"><div class="num">50+</div><div class="lbl">Journeys Curated</div></div>
    </div>
    <div class="about-copy reveal">
      <div class="eyebrow">About TravelDore</div>
      <h2>Experience the Extraordinary.</h2>
      <p class="lede">Beyond itineraries. Beyond checklists. Beyond expectations.</p>
      <p>At TravelDore, we believe travel is more than reaching a destination — it's about discovering experiences that stay with you forever. We're not a traditional travel agency focused on selling fixed packages. Instead, we curate meaningful journeys designed around your interests, your pace, and the moments you want to create.</p>
      <p>Whether it's a hidden café tucked away in Europe, a wellness retreat in the mountains, a corporate offsite that inspires new ideas, or a food trail through India's vibrant streets — every experience is thoughtfully crafted to feel personal, authentic, and unforgettable.</p>
      <a href="about.html" class="btn btn-dark">Meet The Founder</a>
    </div>
  </div>
</section>'''

    body = (hero + stats_band() + about + why_section() + experiences_section(depth)
            + gallery_section(depth, limit=8, show_filters=False) + testimonials_section()
            + booking_section() + inquiry_section(depth) + instagram_section())
    write("index.html", page("Home", "TravelDore — An Art Of Exploration. Curated luxury journeys designed to inspire, connect, and transform.", depth, body))

# ---------------------------------------------------------------------------
# Page: EXPERIENCES INDEX
# ---------------------------------------------------------------------------
def build_experiences_index():
    depth = 0
    hero = f'''
<section class="page-hero">
  <div class="hero-media"><img src="{img('experiences-index',1920,1000,'Experiences')}" alt="Explore Experiences"></div>
  <div class="container page-hero-content">
    <div class="breadcrumb"><a href="index.html">Home</a> / Experiences</div>
    <h1>Explore Experiences</h1>
    <p>Seven distinct paths into the world, each shaped around a different kind of traveler. Choose the one that speaks to you today — or blend a few into a journey that's entirely your own.</p>
  </div>
</section>'''
    body = hero + experiences_section(depth) + cta_band(depth,
        "Not sure where to begin?",
        "Tell us what you're dreaming of and let our concierge team shape the perfect journey.",
        seed="experiences-cta")
    write("experiences/index.html", page("Experiences", "Explore TravelDore's seven curated experience categories — from Leisure Escapes to the Luxury Collection.", depth, body))

# ---------------------------------------------------------------------------
# Page: Individual experience pages
# ---------------------------------------------------------------------------
def build_experience_page(e):
    depth = 1
    data = EXPERIENCE_CONTENT[e["slug"]]

    exp_nav = "".join(
        f'<a href="{other["slug"]}.html" class="{"active" if other["slug"]==e["slug"] else ""}">{icon(other["ic"])} {other["title"]}</a>'
        for other in EXPERIENCES
    )

    hero = f'''
<section class="page-hero">
  <div class="hero-media"><img src="{img(data['seed'],1920,1000,data['heading'])}" alt="{data['heading']}"></div>
  <div class="container page-hero-content">
    <div class="breadcrumb"><a href="../index.html">Home</a> / <a href="index.html">Experiences</a> / {data['heading']}</div>
    <h1>{data['heading']}</h1>
    <p>{e['tag']}</p>
  </div>
</section>'''

    cards = ""
    for ic, title, lede, bullets in data["categories"]:
        seed = re.sub(r'[^a-z0-9]+', '-', title.lower())
        li = "".join(f"<li>{b}</li>" for b in bullets)
        cards += f'''
      <div class="category-card reveal">
        <div class="category-media"><img src="{img(e['slug']+'-'+seed,700,700,title)}" alt="{title}" loading="lazy"></div>
        <div class="category-body">
          <span class="icon-wrap">{icon(ic)}</span>
          <h3>{title}</h3>
          <span class="category-tag">{lede}</span>
          <ul>{li}</ul>
        </div>
      </div>'''

    closing_parts = data['closing'].split('. ')
    closing_head = closing_parts[0] + ('.' if not closing_parts[0].endswith('.') else '')
    closing_rest = '. '.join(closing_parts[1:])

    body = hero + f'''
<section class="section">
  <div class="container">
    <div class="exp-nav">{exp_nav}</div>
    <div class="section-head align-left" style="margin-bottom:56px;">
      <p style="font-size:1.08rem;color:var(--ink-soft);font-weight:300;max-width:820px;">{data['intro']}</p>
    </div>
    <div class="category-grid stagger">{cards}
    </div>
    <div class="closing-band reveal">
      <h3>{closing_head}</h3>
      <p>{closing_rest}</p>
    </div>
  </div>
</section>
''' + cta_band(depth, "Ready to design your journey?", "Talk to a TravelDore concierge and start turning this into your next trip.", seed=e['slug']+"-cta")

    write(f"experiences/{e['slug']}.html", page(data['heading'], f"{data['heading']} — {e['tag']} | TravelDore curated journeys.", depth, body))

# ---------------------------------------------------------------------------
# Page: ABOUT
# ---------------------------------------------------------------------------
def build_about():
    depth = 0
    hero = f'''
<section class="page-hero">
  <div class="hero-media"><img src="{img('about-hero',1920,1000,'About TravelDore')}" alt="About TravelDore"></div>
  <div class="container page-hero-content">
    <div class="breadcrumb"><a href="index.html">Home</a> / About</div>
    <h1>Experience the Extraordinary.</h1>
    <p>Beyond itineraries. Beyond checklists. Beyond expectations.</p>
  </div>
</section>'''

    intro = f'''
<section class="section">
  <div class="container about-grid">
    <div class="framed reveal-scale">
      <div class="media-inner"><img src="{img('about-story',900,1100,'Our Story')}" alt="TravelDore story"></div>
    </div>
    <div class="about-copy reveal">
      <div class="eyebrow">Our Story</div>
      <h2>We don't just plan where you go.</h2>
      <p>At TravelDore, we believe travel is more than reaching a destination — it's about discovering experiences that stay with you forever. We're not a traditional travel agency focused on selling fixed packages. Instead, we curate meaningful journeys designed around your interests, your pace, and the moments you want to create.</p>
      <p>Whether it's a hidden caf&eacute; tucked away in Europe, a wellness retreat in the mountains, a corporate offsite that inspires new ideas, or a food trail through India's vibrant streets, every experience is thoughtfully crafted to feel personal, authentic, and unforgettable.</p>
      <p class="lede">We create stories you'll tell for years to come.</p>
    </div>
  </div>
</section>'''

    founder = f'''
<section class="section bg-lilac">
  <div class="container founder-wrap">
    <div class="framed reveal-scale">
      <div class="media-inner"><img src="{img('founder-portrait',800,1000,'Vidhi Modi')}" alt="Vidhi Modi, Founder of TravelDore"></div>
    </div>
    <div class="reveal">
      <div class="eyebrow">Meet The Founder</div>
      <h2 style="font-size:clamp(1.8rem,3.5vw,2.6rem);margin-bottom:20px;">Vidhi Modi</h2>
      <p>TravelDore was founded by Vidhi Modi with a simple vision — to redefine the way people experience travel. After years in the corporate world, Vidhi realized that the most memorable moments weren't found in meeting rooms, but in the journeys that brought new perspectives, meaningful connections, and unforgettable stories.</p>
      <p>That vision became TravelDore: a brand built around curated experiences, purposeful travel, and authentic exploration.</p>
      <div class="founder-quote">&ldquo;What kind of experience are you looking for?&rdquo;</div>
      <p>Because we believe the best trips aren't measured by the places you visit — but by how they make you feel.</p>
    </div>
  </div>
</section>'''

    why = why_section()

    closing = f'''
<section class="section">
  <div class="container">
    <div class="closing-band reveal" style="text-align:left;display:grid;grid-template-columns:1fr auto;gap:30px;align-items:center;">
      <div>
        <h3>With TravelDore, you don't just visit destinations. You experience them.</h3>
        <p>Anyone can book flights and hotels. We go a step further by curating experiences that feel personal, effortless, and unforgettable — from hidden gems and immersive cultural experiences to luxury escapes, wellness retreats, and corporate travel.</p>
      </div>
      <a href="plan-my-journey.html" class="btn btn-primary">Plan My Journey</a>
    </div>
  </div>
</section>'''

    body = hero + intro + founder + why + closing
    write("about.html", page("About Us", "The story of TravelDore and founder Vidhi Modi — curated, purposeful, authentic travel experiences.", depth, body))

# ---------------------------------------------------------------------------
# Page: GALLERY
# ---------------------------------------------------------------------------
def build_gallery():
    depth = 0
    hero = f'''
<section class="page-hero">
  <div class="hero-media"><img src="{img('gallery-hero',1920,1000,'Gallery')}" alt="TravelDore Gallery"></div>
  <div class="container page-hero-content">
    <div class="breadcrumb"><a href="index.html">Home</a> / Gallery</div>
    <h1>Gallery</h1>
    <p>A Pinterest-style journey through luxury stays, cultural moments, wild landscapes, and the everyday beauty travel reveals.</p>
  </div>
</section>'''
    body = hero + gallery_section(depth, limit=None, show_filters=True) + cta_band(depth, "Seen enough to get inspired?", "Let's turn this inspiration into your next curated journey.", seed="gallery-cta")
    write("gallery.html", page("Gallery", "Browse the TravelDore gallery — luxury, culture, nature, adventure, people and food from curated journeys.", depth, body))

# ---------------------------------------------------------------------------
# Page: CONTACT
# ---------------------------------------------------------------------------
def build_contact():
    depth = 0
    hero = f'''
<section class="page-hero">
  <div class="hero-media"><img src="{img('contact-hero',1920,1000,'Contact Us')}" alt="Contact TravelDore"></div>
  <div class="container page-hero-content">
    <div class="breadcrumb"><a href="index.html">Home</a> / Contact</div>
    <h1>Let's Start Planning</h1>
    <p>Reach out and a TravelDore concierge will get back to you within 24 hours.</p>
  </div>
</section>'''

    info = f'''
<section class="section">
  <div class="container contact-grid">
    <div class="reveal">
      <div class="eyebrow">Get In Touch</div>
      <h2 style="font-size:clamp(1.8rem,3.5vw,2.6rem);margin-bottom:30px;">We'd love to hear from you</h2>
      <div class="contact-card">
        <div class="contact-icon">{icon('whatsapp')}</div>
        <div><h4>WhatsApp</h4><p><a href="https://wa.me/917046001515" target="_blank" rel="noopener">+91 70460 01515</a></p></div>
      </div>
      <div class="contact-card">
        <div class="contact-icon">{icon('mail')}</div>
        <div><h4>Email</h4><p><a href="mailto:inquiry@traveldore.com">inquiry@traveldore.com</a></p></div>
      </div>
      <div class="contact-card">
        <div class="contact-icon">{icon('clock')}</div>
        <div><h4>Business Hours</h4><p>10 AM &ndash; 7 PM, Monday to Saturday</p></div>
      </div>
      <div class="contact-card">
        <div class="contact-icon">{icon('camera')}</div>
        <div><h4>Follow Along</h4><p><a href="https://instagram.com" target="_blank" rel="noopener">Instagram</a> &nbsp;&middot;&nbsp; <a href="https://facebook.com" target="_blank" rel="noopener">Facebook</a></p></div>
      </div>
    </div>
    <div class="map-embed reveal-scale">
      <iframe src="https://www.google.com/maps?q=Ahmedabad,Gujarat,India&output=embed" allowfullscreen="" loading="lazy" title="TravelDore location map"></iframe>
    </div>
  </div>
</section>'''

    body = hero + info + inquiry_section(depth)
    write("contact.html", page("Contact", "Get in touch with TravelDore via WhatsApp, email, or our inquiry form. We reply within 24 hours.", depth, body))

# ---------------------------------------------------------------------------
# Page: PLAN MY JOURNEY
# ---------------------------------------------------------------------------
def build_plan_journey():
    depth = 0
    hero = f'''
<section class="page-hero">
  <div class="hero-media"><img src="{img('plan-hero',1920,1000,'Plan My Journey')}" alt="Plan My Journey"></div>
  <div class="container page-hero-content">
    <div class="breadcrumb"><a href="index.html">Home</a> / Plan My Journey</div>
    <h1>Plan My Journey</h1>
    <p>Every extraordinary trip starts with a conversation. Tell us what you're dreaming of, and let's design it together.</p>
  </div>
</section>'''
    body = hero + booking_section() + inquiry_section(depth)
    write("plan-my-journey.html", page("Plan My Journey", "Start planning your curated TravelDore journey — share your travel purpose and preferences with our concierge.", depth, body))

# ---------------------------------------------------------------------------
# Build all
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    build_home()
    build_experiences_index()
    for e in EXPERIENCES:
        build_experience_page(e)
    build_about()
    build_gallery()
    build_contact()
    build_plan_journey()
    print("\\nAll pages built successfully.")
