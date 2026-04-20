# Senior Home Care Finder — Redesign Plan (Milestone 0)

**Date:** 2026-04-20
**Scope:** Redesign the homepage first, then extend established patterns to directory / agency / blog / static pages, matching the disciplined incremental methodology used on the `financial-tools-directory` sibling project.
**Intent:** Port the sibling's *infrastructure* (design tokens, semantic CSS, self-hosted fonts, SEO hardening, performance budget) while rethinking the *aesthetic* from scratch for a healthcare / elder-care audience.

---

## Audience & visual direction: "Trusted neighbor," not Silicon Valley product

| Dimension | Finance-native (sibling) | Healthcare-native (this site) |
|---|---|---|
| Primary user | Pre-retiree researching advisors | Adult child (50–65) researching care for a parent (75+) |
| Emotional state | Skeptical, analytical | Overwhelmed, often in crisis (post-hospital, post-fall) |
| YMYL category | Finance | Healthcare + elder care — arguably higher-stakes |
| Info density | Bloomberg-dense is a feature | Density is **stress-inducing** — reject it |
| Type scale | Compact, numeric-heavy | Generous — 18px body minimum, readable by a 75-year-old |
| Color semantics | Green/red/amber for up/down/warn | Warm / calm / trustworthy; avoid alarming red |
| Dark mode | First-class | Not a priority — older eyes generally prefer light-on-dark-text |

**Reference companies studied (to borrow from, not imitate):**
- **A Place for Mom** — warmth, photography, conversational; but too lead-gen heavy.
- **Honor** — modern without being cold; clear typography; illustrations over stock photography.
- **AARP** — authoritative, accessible, slightly old-fashioned in a way that reads as "been here for decades, knows what they're doing."
- **NHS UK (digital.nhs.uk)** — plain-English ethos; high contrast; the gold standard for healthcare clarity.
- **National Institute on Aging (nia.nih.gov)** — teal/blue institutional trust, large type, patient voice.

**Anti-patterns to avoid:**
- Stock photos of smiling-grandparent-with-caregiver (indistinguishable from ten other directories).
- Coral/pink "senior living" palettes (reads as assisted-living-marketing, not advisor-to-families).
- Urgency language ("Get help NOW!") — this audience is already scared.
- Tiny grey-on-grey secondary text (WCAG problem, especially for the end-user cohort).
- Bloomberg-style data density — the numbers here are emotional (cost, hours, distance), not analytical.

---

## Proposed typography system

**Body sans-serif:** **Public Sans** (variable WOFF2, self-hosted).
- Why: Designed by USWDS specifically for government/health accessibility. Open-licensed. High legibility at 18px body. Carries institutional trust without feeling corporate.
- Alternative: Inter — equally legible but more "startup."

**Editorial display serif:** **Fraunces** (variable, already in sibling font inventory — portable).
- Why: Humanist warmth, SOFT axis lets us dial down "designerly" and up "approachable." Works for agency names and editorial headlines without feeling Silicon-Valley.
- Alternative: Source Serif 4, Lora.

**Monospace:** **not load-bearing here.** The sibling's Geist Mono is tied to tabular figures for finance; our numerics are phone numbers, ZIP codes, ratings — Public Sans tabular features handle this fine.

**Base scale:**
- `--font-size-base: 1.125rem` (18px) — up from sibling's 16px default. This is the single most impactful a11y change for the audience.
- `--line-height-prose: 1.75` — prose reads like a magazine article, not a UI tooltip.
- Measure: 66ch for long-form prose; 58ch for hero copy.

---

## Proposed color direction

**Keep the broad palette from CLAUDE.md** (blue primary, teal secondary, amber accent) but **retune** for healthcare + accessibility:

| Token | Current (Tailwind-driven) | Proposed | Rationale |
|---|---|---|---|
| `--color-bg` | `bg-gray-50` (#F9FAFB) | `#FAF9F6` (warm off-white) | Slightly warm paper tone, reads as "magazine" not "app." |
| `--color-surface` | white | white | — |
| `--color-text` | gray-900 | `#1A2332` (deep navy-black) | More contrast than gray-900 on warm bg; AAA on white. |
| `--color-text-muted` | gray-500 (#6B7280) | `#4A5568` | **Brighten** muted text — gray-500 fails WCAG AA at small sizes for 60+ eyes. |
| `--color-primary` | #2563EB (blue-600) | `#1E4D8C` (deeper blue) | Calmer, less "SaaS product." |
| `--color-secondary` | #0D9488 (teal-600) | `#0F766E` (teal-700) | Slightly deeper teal — reads as "healthcare institutional." |
| `--color-accent` | #F59E0B (amber-500) | `#D97706` (amber-600) | Deeper amber for CTAs; gold-leaf warmth over highlighter-yellow. |
| `--color-border` | gray-200 | `#E5E0D8` | Warm neutral border, not cool gray. |
| `--color-success` | — | `#0F766E` | Re-use secondary; not using semantic red/green the way finance does. |
| `--color-warn` | — | `#B45309` | Used sparingly — disclaimers, "medicare does not cover" callouts. |

**No semantic green/red/amber layer.** The finance site uses these for up/down/warn. Here, `success` = secondary, `warn` = accent. We don't have financial gain/loss to color-code.

---

## Proposed homepage structure

Adapted from sibling Milestone 1 (14 sections); this site needs ~8 simpler sections.

```
┌──────────────────────────────────────────────────────────────┐
│ Site nav (tokenized — port from sibling M9 rewrite)          │
├──────────────────────────────────────────────────────────────┤
│ Hero                                                         │
│  • Editorial headline (Fraunces) — not "find trusted care"   │
│    but something like "Home care starts with knowing the     │
│    questions to ask."                                        │
│  • State locator (select → go to /state/[slug].html)         │
│  • 3 trust signals: listings count · states covered · years  │
├──────────────────────────────────────────────────────────────┤
│ Ad slot A (leaderboard, min-height 100, CLS-safe)            │
├──────────────────────────────────────────────────────────────┤
│ "How this directory works" — 3-up editorial                  │
│  (Browse by state · Browse by service · Read the guides)     │
│  Replaces the "Verified agencies / Real reviews" trust bar — │
│  that reads as generic; this reads as orientation.           │
├──────────────────────────────────────────────────────────────┤
│ Featured agencies (3 cards, type-first rows like sibling M2) │
│  — no photos required, services as chips, phone + city visible│
├──────────────────────────────────────────────────────────────┤
│ Ad slot B (in-content, min-height 250)                       │
├──────────────────────────────────────────────────────────────┤
│ Browse by state — grid with per-state agency counts          │
│  (intensity shading like sibling state heatmap, but subtler) │
├──────────────────────────────────────────────────────────────┤
│ Browse by service — 10 cards (already have 10 SERVICES)      │
├──────────────────────────────────────────────────────────────┤
│ Guides & resources — blog category tiles, post counts        │
├──────────────────────────────────────────────────────────────┤
│ Ad slot C (before FAQ, min-height 250)                       │
├──────────────────────────────────────────────────────────────┤
│ Editorial block — "What we don't do" anti-position           │
│  ("We don't sell leads. Agencies don't pay to be listed."    │
│   — this site's version of the sibling's "no paid placements"│
│   editorial block, load-bearing for YMYL trust)              │
├──────────────────────────────────────────────────────────────┤
│ FAQ accordion (schema preserved, styling tokenized)          │
├──────────────────────────────────────────────────────────────┤
│ Newsletter (Mailchimp — already wired, restyle only)         │
├──────────────────────────────────────────────────────────────┤
│ Footer (tokenized, port from sibling M9 semantic rewrite)    │
└──────────────────────────────────────────────────────────────┘
```

**Three ad slots** (A / B / C) reserved, CLS-safe, none in place today (zero active slots per grep). Slot placement is approvable now since nothing exists to disturb.

---

## Milestone plan — which sibling milestones port wholesale vs. need adaptation

### Port wholesale (no aesthetic rethink)
- **M7b — SEO hardening**
  - `@graph` WebSite + Organization in `base.html`.
  - BreadcrumbList JSON-LD macro (`_breadcrumb_schema.html`), called from state / city / agency / blog / post templates.
  - Article schema on `post.html`.
  - Descriptive alt text audit on agency logos / photos.
  - Keep `HomeHealthCareService` schema on `agency.html` (already in place) — just nest inside `@graph`.
  - `success.html` → noindex (one-line fix in `build_static_pages`).
  - Sitemap truthy bug → `is not None` check in `build.py:844` and `:852`.
- **M9 — Tailwind removal + mobile performance**
  - Remove `<script src="https://cdn.tailwindcss.com">` from `base.html:68`.
  - Delete inline `tailwind.config` block.
  - Rewrite nav / footer / newsletter / mobile menu in tokenized semantic CSS — exactly as sibling did.
  - `#mobile-menu` scroll-containment with `100dvh` + `overscroll-behavior: contain`.
- **Side-milestone — Mailchimp newsletter**
  - Already implemented here. Verify honeypot + SITE hidden-input are present (`SITE` tag should read `senior-home-care`, not the sibling's value).
- **Side-milestone — GSC verification helper**
  - `copy_verification_files()` helper in `build.py` for the Google/Bing token files and any future additions. Bing meta tag already in place (added this morning in commit 3603bbf). Google file-upload verification to verify next.

### Port with aesthetic rethink
- **M1 — Homepage** (described above).
- **M2 — Directory pages** (state / city / agency)
  - "Type-first list row" for agency listings, but **less dense than sibling** — include photo when present (finance advisor listings had no photos; home care agencies often do and photos are load-bearing for trust).
  - Keep Leaflet map on state pages; swap OSM → CartoDB Positron for consistent warm-tone map styling (Dark Matter not needed — no dark mode here).
  - Agency detail `HomeHealthCareService` schema stays; add BreadcrumbList alongside.
  - **Replace Weather link** (`agency.html:267-277`) with a Medicare **Care Compare** link for agencies that have Medicare certification — this is the healthcare equivalent of the sibling site's weather→BrokerCheck swap. Medicare.gov/care-compare is the authoritative public registry.
- **M4 — Blog**
  - Magazine-index listing (no photo cards required).
  - Tokenize `.prose` colors (custom.css:98, 106, 126, 134 — same bug sibling fixed).
  - Fraunces headlines + Public Sans body; reading-time meta.
  - Disclaimer box (medical/financial/legal — already in `post.html`, just restyle).
- **M6 — Static pages + copy pivot**
  - About / contact / privacy / terms rewrite.
  - Add "What we don't do" anti-positioning (healthcare version: no paid placements, no lead sales, not a medical-advice site).
  - Founder bio when Kevin's ready.

### Skip
- **M3 — Compare feature.** Portable to this site ("compare 3 agencies side-by-side") but not in the initial scope. Revisit as milestone 3+ once homepage + directory pages + blog are validated.
- **M5 — Tools hub.** Not applicable — no tools section here.
- **M7 / M8 — Calculators.** Not applicable in current form. Long-term, a "what does home care cost?" calculator would fit, but out of scope.

---

## What's already doing the right thing in this codebase

Parts of this site predate the sibling project's best patterns; others match or exceed the sibling's state. **Do not regress these:**

1. **`config.py` US_STATES** — all 51 states already have unique 100+ word editorial descriptions. Keep verbatim; sibling's state copy was modeled on this.
2. **`config.py` SERVICES** — 10 service categories each with a 100+ word `intro` paragraph. Keep verbatim. Sibling has nothing equivalent at this depth.
3. **`HomeHealthCareService` JSON-LD on `agency.html`** — correct schema type, already emitting AggregateRating conditionally, PostalAddress, etc. Nest inside `@graph`, don't rewrite.
4. **Noindex logic** (`build.py:616` — `MIN_AGENCIES_FOR_INDEX = 3`) — already in place; this is the pattern sibling copied here.
5. **Local markdown blog loader** (`build.py:374`) — loads posts with ``` frontmatter from `content/blogposts/`, merges with Airtable. Sibling has an equivalent but ours runs in `ThreadPoolExecutor` for images, which is faster.
6. **Image caching / photo refresh** (`build.py:208` + `refresh_photos.py`) — thread pool, Airtable-clears-on-broken-URL. Sibling doesn't have equivalent agency-photo churn pressure.
7. **Mailchimp + Netlify Forms fallback** in base.html (`base.html:237-261`) — already correct, newer than sibling's pattern.
8. **Bing + (pending) Google verification meta tag** already wired into base.html (added this morning).
9. **ads.txt** present at project root with correct publisher ID, copied to `dist/` on build.

## What's broken or missing (parity with sibling)

1. **Tailwind CDN still in `<head>`** — render-blocking, ~268 KiB unused JS.
2. **`.prose` block has hardcoded colors** — `custom.css:98, 106, 126, 134` — no dark mode is OK here, but tokenization lets component CSS reuse the same values.
3. **No Organization / `@graph` schema** — only WebSite.
4. **No BreadcrumbList schema anywhere** — breadcrumb markup exists, JSON-LD doesn't.
5. **No Article schema on `post.html`.**
6. **`success.html` lacks noindex.**
7. **Sitemap truthy bug** (`build.py:844, 852`) — `if indexed_states:` treats empty list as "caller didn't filter." Fix: `is not None`.
8. **No self-hosted fonts** — relies on system-font stack via Tailwind defaults.
9. **`custom.css` is 171 lines total** — no design tokens, no component layer.
10. **`goToState()` inline handler in `index.html`** — fine, but replace with a proper form submit for progressive enhancement.

---

## Working agreements (from `smart-investor-redesign` skill + Kevin's brief)

- Work on branch (`redesign/homepage-healthcare-native` for M1).
- Small scoped commits with intent-describing messages.
- `REDESIGN_NOTES.md` — one-line decision log, updated continuously.
- `REDESIGN_CHANGELOG.md` — narrative release notes, appended per milestone.
- **Ask before:**
  - Adding dependencies.
  - Changing URLs / slugs / canonicals.
  - Moving AdSense slots (there are none active, but the slot positions agreed in this plan become load-bearing once populated).
  - Touching the build pipeline.
  - Deploying to production.
- Site is **already AdSense-approved** — the bar for changes is "don't break what works."

---

## Open questions for Kevin

1. **Font licensing:** Public Sans is OFL — no issue. Fraunces is OFL — no issue. Both self-hostable. **Approve?**
2. **Color retune:** keep the blue/teal/amber family, but deeper/warmer per the table above. **Approve?** Or lean further from "institutional" toward "magazine" (e.g., warmer cream bg + burgundy accent)?
3. **Photos:** home care agencies often have real Google-Places photos (already cached in `static/images/`). Unlike the sibling's finance site, we should keep them prominently in listings. **Confirm that's the direction?**
4. **Weather link on agency detail** — replace with Medicare Care Compare? Or keep both?
5. **Reading age:** target body copy readability at ~grade 8 (typical healthcare standard) or lower? Affects hero copy voice directly.
6. **Milestone 1 scope:** homepage only, or homepage + base.html (since the Tailwind removal has to be near-simultaneous with tokenization)? Recommend: homepage + base.html as a single M1, matching how the sibling did it.

---

## Proposed first implementation milestone (for approval, not execution)

**Milestone 1 — Homepage + base.html redesign**
1. Create branch `redesign/homepage-healthcare-native`.
2. Self-host Public Sans + Fraunces as variable WOFF2 in `static/fonts/`.
3. Author `static/css/custom.css` design-token layer + homepage component styles.
4. Rewrite `base.html` (no Tailwind CDN, tokenized nav/footer/newsletter, schema @graph, font preloads, SVG favicon update if wanted).
5. Rewrite `templates/index.html` section-by-section per the structure above.
6. Reserve the three ad slots with CLS-safe `min-height`; `data-slot="home-a|home-b|home-c"` attributes.
7. Verify local build produces valid output for all 16 templates (most will temporarily render with broken styles until their own milestones land — acceptable).
8. Land as 3–4 scoped commits on the branch; Kevin reviews before merge.

**Not in M1:** state / city / agency / blog / post / about / contact / privacy / terms / service — all follow in M2–M6, matching the sibling's milestone cadence.

---

**Status: awaiting approval. No production code has been written.**
