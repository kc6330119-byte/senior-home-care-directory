# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

A **national in-home care agency directory** at seniorhomecarefinder.com. Static site built with Python/Jinja2, data from Airtable, hosted on Netlify. Third site in a directory factory following the splash-pad-directory pattern.

**Key SEO target:** City-level pages (`/state/texas/houston.html`) for "home care in [city]" searches.

## Build Commands

```bash
# Setup
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env  # Then add Airtable keys

# Build (uses sample data without .env)
python3 build.py

# Preview locally
cd dist && python3 -m http.server 8000
```

**Netlify build command:** `pip install -r requirements.txt && python build.py`

## Architecture

### Static Site Generator Pattern
- `build.py` — Single-file generator that fetches from Airtable and renders Jinja2 templates to `dist/`
- `config.py` — Site config, US states list, service categories
- `templates/` — Jinja2 templates (base.html is the layout)
- `dist/` — Generated output (gitignored)

### Key Build Functions (model after splash-pad-directory/build.py)
1. `fetch_from_airtable()` / `get_sample_data()` — Data layer with fallback
2. `build_homepage()`, `build_state_pages()`, `build_city_pages()`, `build_agency_pages()`
3. `build_service_pages()` — Filter pages by care type
4. `build_sitemap()`, `build_robots()`, `build_search_index()`

### Critical Addition vs Splash Pad Site
**City-level pages** are required. URL structure: `/state/{state}/{city}.html`

## Airtable Field Names (exact names required)

**Agencies table:** Name, Slug, Description, Address, City, State (full name, not abbreviation), Zip, County, Phone, Website URL, Google Maps URL, Photo URL, Hours, Services, Care Types, Payment Options, Licensing, Accreditation, Languages, Service Area, Year Established, Rating, Review Count, Status, Date Added, Latitude, Longitude

**Blog Posts table:** Title, Slug, Content, Excerpt, Author, Publish Date, Featured Image, Meta Description, Status, Featured, Category

## URL Structure

```
/                                    → Homepage
/state/texas.html                    → State listing
/state/texas/houston.html            → City listing (money page)
/agency/comfort-keepers-houston.html → Agency detail
/services/companion-care.html        → Service filter
/blog/{slug}.html                    → Blog posts
```

## Design Requirements

- **Palette** (tokenized in `static/css/custom.css`):
  - `--color-primary: #1E4D8C` (deep trustworthy blue)
  - `--color-secondary: #0F766E` (institutional teal)
  - `--color-accent: #D97706` (gold-leaf amber)
  - `--color-bg: #FAF9F6` (warm off-white)
  - `--color-text: #1A2332` (deep navy-black)
- **Fonts:** self-hosted variable WOFF2 — Public Sans (body) + Fraunces (display serif). See `static/fonts/`.
- **No Tailwind.** Semantic tokenized CSS only. Base font size is 18px for accessibility (audience skews older — adult children 50–65 researching care for a parent 75+).
- **Mobile-first, editorial healthcare aesthetic.** Not finance-dense, not SaaS-gradient. See `REDESIGN_PLAN.md` for the audience framing.
- **Body copy targets grade-8 reading level** (CDC Clear Communication Index standard for healthcare content).
- **Schema:** `@graph` with `WebSite` + `Organization` sitewide (in `base.html`); `HomeHealthCareService` on agency detail; `Article` on blog posts; `BreadcrumbList` via the `_breadcrumb_schema.html` macro on state / city / agency / blog / post pages.
- **Three ad slots** on most high-traffic templates, named via `data-slot` attributes (e.g. `home-a`, `state-a`, `agency-a`). CLS-safe `min-height` already in CSS.
- **Redesign history:** see `REDESIGN_CHANGELOG.md` (narrative) and `REDESIGN_NOTES.md` (one-line decision log).

## Environment Variables

```
AIRTABLE_API_KEY=
AIRTABLE_BASE_ID=
AIRTABLE_TABLE_NAME=Agencies
AIRTABLE_BLOG_TABLE_NAME=Blog Posts
SITE_URL=https://seniorhomecarefinder.com
GA_MEASUREMENT_ID=G-XXXXXXXXXX
```

## Key Constraints

- State names must be full names ("Texas" not "TX") for consistent slugification
- `ads.txt` must be copied to `dist/` root (AdSense publisher: `ca-pub-9265762311868507`)
- Netlify Forms require `data-netlify="true"` and `name="contact"` attributes
- Use JS fetch for form submission (not native submit) to avoid redirect issues
- Never commit `.env` files

## Reference Project

Previous site to reference for patterns: `/Users/kevincollins/GitHub/splash-pad-directory/`
- `build.py` — Static site generator structure
- `config.py` — States/categories pattern
- `templates/base.html` — Nav, footer, AdSense slots, Analytics
