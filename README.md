# TravelDore Website — Code Package (v2)

A complete, static, mobile-first multi-page website built to the TravelDore
brand brief — classic luxury-travel-house aesthetic, Cormorant Garamond +
Poppins, the lavender/plum/gold palette, framed photography, and refined
motion.

## How to view it
Double-click `index.html` to open it in any browser — no build step, no
server, no dependencies.

## What changed in this version
- **Fixed alignment issues.** The previous build linked to an external
  image CDN (picsum.photos) that isn't reachable from every network —
  every failed image collapsed its container and threw grids out of
  alignment. This version generates its **own branded placeholder
  photography locally** (`images/` folder, `tools/generate_images.py`)
  so the site never depends on outside services and never shows a broken
  layout, online or offline.
- **Grid bugs fixed.** The experiences grid no longer uses uneven
  row-spans; category cards, the contact grid, and the form grid all
  have proper breakpoints so nothing overlaps or squishes on tablet.
- **Classic redesign.** Swapped the floating glass "SaaS" navbar for a
  full-width bar with a gold underline on hover; buttons are now
  rounded-rectangle (boutique-hotel style) instead of full pills;
  photography is presented in a gold-lined picture-frame treatment;
  sections are separated with a thin gold ornamental divider; card
  icons are a custom-drawn line-icon set (no emoji) for a more
  premium, professional feel.
- Verified with real screenshots at desktop (1440px) and mobile (390px)
  widths before delivery.

## Structure
```
index.html                     Home
about.html                     About + Founder (Vidhi Modi) + Why TravelDore
gallery.html                   Pinterest-style masonry gallery with filters
contact.html                   Contact details + map + inquiry form
plan-my-journey.html           Booking timeline + inquiry form
experiences/index.html         Experiences hub (7 categories)
experiences/*.html             The 7 experience pages (full content)
css/style.css                  Design system: tokens, layout, components, animation
js/main.js                     Loader, scroll progress, nav, carousel, filters, forms, WhatsApp box
images/                        Generated branded placeholder photography
tools/generate_images.py       Placeholder-photo generator (PIL, no network needed)
build.py                       Site generator — edit content here, then `python3 build.py` to rebuild every page
```

## Images
All photography is elegant generated placeholder plates (deep plum to
lavender gradients, gold frame, section label) so the site is fully
self-contained and never breaks. Before launch, replace files in
`images/` with real TravelDore photography of the same filenames, or
point the `<img src>` tags at your CDN.

## Before launch
- Swap placeholder photography for real brand photography/video
- Connect the inquiry form to email/CRM (currently front-end demo only)
- Update Instagram/Facebook links
- Set exact map coordinates in `contact.html` if you want a precise pin
