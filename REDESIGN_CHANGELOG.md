# Redesign Changelog — Senior Home Care Finder

Narrative log of the redesign work on `seniorhomecarefinder.com`. **Most recent milestone at the top.** Each entry captures what shipped, what it changed for users / Google / the business, and what's still open.

The methodology is ported from the `financial-tools-directory` sibling project — disciplined, documented, incremental — but the aesthetic is rethought for a healthcare / elder-care audience.

For the terse one-line-per-decision log, see [`REDESIGN_NOTES.md`](REDESIGN_NOTES.md). For the homepage plan, see [`REDESIGN_PLAN.md`](REDESIGN_PLAN.md). For the AdSense posture (this site is already approved), see [`ADSENSE_PRESUBMISSION_PLAN_SENIOR.md`](ADSENSE_PRESUBMISSION_PLAN_SENIOR.md).

---

## Milestone 5 — Static pages: contact / submit / about / privacy / terms / success (2026-04-20)

**Branch:** `redesign/homepage-healthcare-native` (continuation)
**Commits:** `94146f4` (form-component CSS + contact + submit), `03e8588` (about + privacy + terms + success)
**Templates rewritten:** `contact.html`, `submit.html`, `about.html`, `privacy.html`, `terms.html`, `success.html`
**CSS additions (~320 lines):** `.form-*` field components, `.static-page` shell, `.info-card` sidebar block, `.legal-prose`, `.anti-list`, `.founder-block`, `.success-page` + `.success-page__mark/title/body/actions`

### What changed

- **Six remaining static pages** all migrated off the old Tailwind markup and onto the new tokenized system. Fast-tracked out of the planned M5/M6 split after Kevin flagged the pages were rendering raw (unstyled forms, plain browser buttons, no editorial hierarchy) in the live preview. Once the branch merges, those pages become user-visible — had to be in the same release.
- **Form component suite** (`.form-field`, `.form-label`, `.form-input`, `.form-select`, `.form-textarea`, `.form-section-title`, `.form-note`, `.form-submit`) — first-class tokenized inputs with focus rings on the tokenized `--shadow-focus` (static rgba fallback for Safari < 16.2). Reusable by any future form (the newsletter internals could port to these in a later polish pass).
- **`contact.html`** — editorial page-head, two-column layout with the Netlify contact form on the left and a sidebar of four `info-card`s (response time / before-you-write / agency-route / verification pointer). Subject dropdown rewritten to match the operations that actually exist. Honeypot + `form-name` hidden input preserved. JS success handler updated to navigate to the directory-style `/success/` URL.
- **`submit.html`** — editorial page-head, single-column form broken into labeled sections (`Agency information` / `Contact person`) via `.form-section-title`. `form-note` call-out explains the review process up front. Sidebar reinforces the three load-bearing trust posture lines: what happens next, that listing is free (no paid placements), how families actually find listings (organic search, direct calls, no lead routing). Added a "State license number" optional field that lets agencies volunteer it at submit time, closing a loop with the per-agency "How to verify" checklist.
- **`about.html`** — rewritten copy aligned with the homepage anti-position block: "A directory, built the way we'd want one for a parent." Sections: Why this exists / What you'll find here / What we don't do (anti-list with red-× markers) / Founder story (WWII-veteran photo preserved, wrapped in the new `.founder-block` component) / How listings get added / How the site makes money. All copy at grade-8 readability.
- **`privacy.html`** — rewritten to describe the current stack accurately (Netlify, Airtable, Mailchimp, GA, AdSense, Medicare Care Compare, state licensing boards). Added a "How we source agency listings" section, explicit "We don't sell your personal information" language, data-retention window (14 months for GA per default), and a plain-English `your rights` section.
- **`terms.html`** — rewritten with the load-bearing YMYL clauses explicit: "This site is not a healthcare provider, referral service, or medical-advice site." "Listings are not endorsements." "No paid placement — agencies don't pay to appear or rank higher." Advertising disclosure clarifies ad selection is Google's, not ours.
- **`success.html`** — centered `.success-page` layout with an SVG checkmark (not the raw `&#10003;` entity, which inherited the surrounding font-size and rendered at an unintended ornamental scale) in a secondary-tint circle. Fraunces headline, two CTAs (back home + browse guides). Already noindexed via the M2 STATIC_PAGES fix; rewrite is purely visual/copy.
- **Breadcrumbs + BreadcrumbList JSON-LD** on every static page via the shared macro — no more missing-schema gap on static content.

### Why it helps

- **Entire template tree is now on the new design system.** Every user-facing URL — homepage, every listing template, every static page — renders from the tokenized CSS layer. No more "will look broken until M5/M6" caveat in the plan. Branch is merge-ready.
- **Forms that actually match the site's posture.** Contact and submit forms previously looked like generic Netlify-Forms boilerplate. The tokenized `.form-*` components read as part of the site — consistent focus rings, typography, and spacing with the rest of the surface.
- **YMYL trust posture reinforced in the legal layer.** Privacy and terms now state plainly what the site does and doesn't do: no lead sales, no paid placements, no medical advice, no endorsement of listings. Legal pages matter more on a healthcare directory than on a generic site, both for user trust and for AdSense content review.
- **Founder story preserved.** The WWII-veteran photo and the story behind the site — load-bearing E-E-A-T content — kept verbatim, wrapped in the new `.founder-block` component.
- **Operational submit form.** New "State license number" field, rewritten contact subject dropdown, and "How families find you" sidebar give agency submitters a clearer model of how the directory actually works.

### Known gaps

- **`.pullquote` and `.data-callout`** editorial components not yet added to `custom.css` — sibling ships them as optional authoring tools. Low priority; no current blog post uses them.
- **Newsletter signup in `base.html`** still uses its own inline input styling rather than the new `.form-*` components. Visually fine because it sits on the dark newsletter band, but could port for consistency in a later polish pass.
- **`/success/` vs `/success/index.html`** — contact + submit JS now redirects to `/success/` (the directory form). Netlify's redirect handling picks that up correctly; the Netlify form post-processing uses `/success/index.html` internally. Tested locally with the sample-data build.
- **No per-page CAPTCHA** on forms — relying on Netlify's built-in spam filter + honeypot input. Acceptable for current volume. Revisit if submission spam becomes a problem.

---

## Milestone 4 — Blog templates (index + post) (2026-04-20)

**Branch:** `redesign/homepage-healthcare-native` (continuation)
**Commits:** `ea486d1` (blog.html + post.html rewrite + ~230 lines of new CSS)
**Templates rewritten:** `blog.html`, `post.html`
**CSS additions:** `.filter-pills` / `.filter-pill`, `.post-index` / `.post-row`, `.article` + children, `.disclaimer-box`, `.related-posts` / `.related-post`

### What changed

- **`blog.html`** rewritten as a magazine-style post list. Each row is a tokenized `.post-row` with mono-caps meta (category · date · reading time · author), Fraunces title, and Public Sans excerpt. Featured image renders as a 160×120 right-aligned thumbnail — **only** when present, so posts without images don't get a fallback-icon placeholder that pretends they do. Filter pills (`.filter-pills`) restyled in the token system; URL-hash deep-linking preserved so homepage category chips (`/blog.html#guides`) still land on the right pill.
- **`post.html`** rewritten as an editorial reading experience. Large Fraunces headline (`opsz 96 / SOFT 40`), Public Sans deck pulled from `post.excerpt`, mono-caps meta row. Body runs through the `.prose` block tokenized in M1 — finally closes the hardcoded-hex dark-mode bug that was visible on every blog post. Disclaimer uses the new warn-tinted `.disclaimer-box`. Footer has the tokenized share list (with `|urlencode` on all interpolated fields, picking up the M2-polish URL-encoding fix). Related posts render in a 3-column tokenized card row using `rejectattr + list + slice` (Jinja doesn't support `{% break %}`).
- **Article JSON-LD** now emitted on every post: `headline`, `datePublished`, `author` (Person), `publisher` (Organization with `logo` ImageObject), `mainEntityOfPage`, optional `image` and `description`. Closes the M7b-port gap for editorial content; makes posts eligible for Google News / Discover and for AI-Overview pull candidacy.
- **BreadcrumbList JSON-LD** on both index (Home / Guides) and post (Home / Guides / post title) via the shared `_breadcrumb_schema.html` macro. "Guides" is now the canonical noun across nav, footer, breadcrumb, and page-head — "Resources" wording retired.
- **Reading time** computed in Jinja: `(content | striptags | wordcount) // 225 + 1`, minimum 1. 225 wpm is audience-tuned (slightly slower than the 250 editorial default because this site's readers skew older). Shown on the blog index rows AND on the article itself AND on related-post cards.
- **Four reserved ad slots** across the two templates (`blog-a`, `blog-b`, post-page doesn't carry any yet — intentional, editorial reading experience runs ad-free through the body, with house ads on index and agency/state pages carrying the inventory).
- **CSS additions (~230 lines):** filter pills with active state, magazine-list row, article header + meta + deck + image + body + footer, disclaimer box with amber warn-tint, related-posts band + card.

### Why it helps

- **Reading experience on par with the content.** 25+ original articles at 1,500–2,500 words each is the load-bearing substance of this site's YMYL case to Google. An editorial typographic register — Fraunces headline, Public Sans deck, 66ch prose measure, 1.75 line-height — reads like a trustworthy reference, not a Tailwind-utility block. The finance sibling's M4 found the same: the reading surface is the quality signal.
- **Dark-mode bug finally closed.** The old `.prose` block had hardcoded `#1f2937` / `#2563eb` / `#e5e7eb` / `#4b5563` / `#f9fafb` hex values. With tokenization from M1 already in place, `post.html` now picks up all the design-token colors automatically — zero additional CSS change needed. (We're light-only on this site per the M0 decision, but the token chain is correct for future flexibility.)
- **Article schema = SERP rich features.** `datePublished`, `author`, `publisher.logo` unlock the byline treatment in search results ("By Author · Date"), Google News eligibility, and AI-Overview pull candidacy. The audience specifically Googles for things like "how to choose a home care agency" — AI Overview is already showing up on most of those queries.
- **Scanability of the magazine index.** Mono-caps meta in 12px tabular-figure type, distinct `.post-row__category` in teal, titles in Fraunces at 20–26px depending on viewport. Easy to scan 25 articles without photos, easy to deep-link from the homepage category chips via the hash filter.
- **YMYL disclaimer visually distinct.** Amber warn-tinted left border + mono-caps "Disclaimer" label — reads as "heads-up, not endorsement" without being alarming. Copy rewritten for grade-8 readability (CDC Clear Communication Index target).
- **Reusable article components.** `.article__title` / `.article__deck` / `.article__meta` / `.disclaimer-box` / `.related-posts` port directly to per-service editorial pages if we add them, and to the other four Kevin directory sites.

### Known gaps

- **Blog content doesn't use the optional `.pullquote` or `.data-callout` components** the sibling ships — those are opt-in authoring elements (raw HTML in markdown). If Kevin wants them available here, it's ~30 lines of CSS to port. Deferred.
- **No table of contents / reading-progress bar** on long-form posts. Deferred.
- **Prose image styles are tokenized** in `.prose img` (inherits from the cascade) but no lazy-loading or intrinsic-width defaults are applied to embedded markdown images — whatever the author writes is what renders.
- **Article schema `author.url`** not set — we don't have author bio pages yet. When/if we add a founder bio or team page, circle back to link authors there via schema.

---

## Milestone 3 — Service page (2026-04-20)

**Branch:** `redesign/homepage-healthcare-native` (continuation)
**Commits:** `b8f2940` (service.html rewrite + .service-chip component)
**Templates rewritten:** `service.html`
**CSS additions:** `.service-chip-row`, `.service-chip`

### What changed

- **service.html** rewritten to match the M2 directory-page pattern. Editorial page-head with service icon next to Fraunces service name, description as lede, meta row showing agency + state counts with tabular figures.
- **Breadcrumb nav + BreadcrumbList JSON-LD** via the shared `_breadcrumb_schema.html` macro — two-level (Home / Service). No intermediate `/services.html` hub exists, so routing through one would be a dead link. The homepage `#browse-services` anchor serves as the conceptual hub.
- **Directory shell** reuses the state-page layout: left aside with state-filter list rendered via the existing `.city-list` component (same label + count nav-row pattern as state-page cities), main column with two reserved ad slots (`service-a`, `service-b`) and the agency grid using the shared `_agency_card.html` partial.
- **`service.intro` editorial paragraph** (100+ word per-service copy from `config.py`) preserved in its own section below the grid. This text predates the redesign and is load-bearing SEO — do not regress.
- **New `.service-chip` / `.service-chip-row`** tokenized component for the "Explore other services" row at the bottom of the page. Distinct from `.chip` (smaller metadata pill); chips-as-nav-buttons need more padding and a hover affordance that shifts border + text to primary.
- **Proper empty-state** with routes to homepage + submit form. `service.intro` still renders in the empty state so the page stays substantive even with zero agency matches.

### Why it helps

- **Full listing surface now on the new design system.** Homepage → state → city → service → agency all use the same editorial register, token system, and card component. No remaining listing page on the old Tailwind layer.
- **Service-page SEO strengthened.** BreadcrumbList JSON-LD makes service pages eligible for SERP breadcrumb display. The per-service 100+ word editorial copy now reads in the editorial typographic register instead of a generic Tailwind prose block.
- **State-filter discoverability.** The sticky `.city-list` sidebar with state counts is the same pattern users have already learned from state pages — no new interaction to figure out.

### Known gaps

- `blog.html`, `post.html` — M4. Will port the `.prose` block that landed (tokenized) in M1's CSS so blog posts stop rendering with hardcoded hex colors.
- `about.html`, `contact.html`, `privacy.html`, `terms.html`, `submit.html`, `success.html` — M5/M6. Copy on several of these also needs an editorial pass (the "Add an Agency" submit flow, the "About" founder story, the healthcare-specific disclosure language).
- No `Service` or `MedicalBusiness` schema per-service — BreadcrumbList is the only JSON-LD. Considered but deferred; the 10 service types we have are broad categories, not individual offerings, so `Service` schema would be thin. Revisit if a per-service FAQ or editorial depth warrants it.

---

## Milestone 2 — Directory pages: state / city / agency (2026-04-20)

**Branch:** `redesign/homepage-healthcare-native` (continuation)
**Commits:** `82da513` (shared partial + breadcrumb macro + directory CSS), `e3ef689` (state + city rewrites), `c9d90e5` (agency rewrite + Medicare Care Compare swap), `de9d164` (M7b sitemap + noindex side-fixes)
**Templates rewritten:** `state.html`, `city.html`, `agency.html`, `_agency_card.html`
**New templates:** `_breadcrumb_schema.html` (macro)
**Build:** `build.py` — sitemap truthy-check bug fixed (`is not None`), `success.html` STATIC_PAGES entry gets `noindex=True`, `build_static_pages` threads the flag through to the template.

### What changed

- **Shared `_agency_card.html` partial** rewritten to the tokenized `.agency-card` component and now drives listings on homepage (featured), state, city, and agency detail (related). One partial is the source of truth for listing UX — matches the sibling's single-partial pattern.
- **`_breadcrumb_schema.html` macro** exposes `schema()` (JSON-LD `BreadcrumbList`) and `nav()` (visible breadcrumb markup). Called from state / city / agency; one import per template, three lines per call. No JSON-LD duplication.
- **State page** rewritten: editorial page-head (eyebrow + Fraunces title + lede + meta row with tabular-figure counts), breadcrumb with schema, two-column directory-shell (left aside with state map + city filter, right main with ad slot + agency grid + ad slot), state editorial paragraph preserved verbatim from `config.py`, proper empty-state when no agencies.
- **City page** rewritten: editorial page-head with "back to {state}" link in meta row, breadcrumb with schema, single-column agency grid, two ad slots, short editorial "finding home care in {city}" block with grade-8 voice, proper empty-state routing to state page + submit form.
- **Agency detail page** rewritten: breadcrumb, HomeHealthCareService + BreadcrumbList JSON-LD, large hero with photo + Fraunces name + rating + primary actions, tokenized detail-card sections (About, Services, Payment, Agency details with two-column spec-list + accreditation chips), two ad slots, tokenized sidebar with Contact card + **Medicare Care Compare card (conditional)** + universal "How to verify this agency" guidance + Share card, related agencies band using the shared partial.
- **Weather link → Medicare Care Compare swap.** The old agency sidebar linked to a National Weather Service forecast for the agency's lat/lng — decorative, not a trust signal. Replaced with a Care Compare card that opens `medicare.gov/care-compare` pre-filtered by the agency's zip + URL-encoded name. Shows only when the agency is Medicare-certified (`accreditation` contains "Medicare Certified" or `payment_options` contains "Medicare"); Care Compare only has data for home-health-certified providers, so showing it universally would be misleading.
- **Universal "How to verify this agency" card** on every agency, Medicare-certified or not. Three-step checklist: (1) verify the state license number with the state licensing board — personalized with `agency.licensing` when present; (2) ask for references from current clients; (3) confirm background-check and training procedures. Real trust signal, consistent grade-8 voice.
- **Leaflet state map** now uses CartoDB Positron tiles instead of OSM's default, giving the map a warm-neutral tone that reads with the `#FAF9F6` page background instead of against it. Markers use `--color-primary` (`#1E4D8C`). Popup HTML is now built with an inline `escapeHtml` helper before concatenation — closes the same class of Airtable-injection path the homepage search XSS fix closed in M1 polish.
- **Six reserved ad slots** across the three templates (`state-a`, `state-b`, `city-a`, `city-b`, `agency-a`, `agency-b`), CLS-safe, `<ins>` tags omitted until Kevin picks AdSense slot IDs.
- **M7b side-fixes** landed alongside the template work:
  - `build.py:build_sitemap` uses `is not None` instead of truthy check for `indexed_states`/`indexed_cities` — prevents the noindex-leak bug where an explicitly-empty filter would fall through to "list every state/city." Same fix sibling landed in M7b.
  - `success.html` marked noindex via STATIC_PAGES entry; `build_static_pages` now threads the flag to the template. Already absent from the sitemap URL list, so this is belt-and-suspenders.
- **CSS additions** (~480 lines): `.breadcrumb`, `.page-head` (editorial headline row for listing/detail templates), `.directory-shell` two-column grid with optional sticky aside, `.state-map` wrapper, `.city-list` (state-page city filter), `.detail-shell` agency-detail grid, `.agency-hero` (photo + name + rating + actions), `.spec-list` (two-column `dl`), `.chip--accredited` and `.chip--payment` variants, `.contact-row`, `.detail-card--care-compare`, `.share-list`, `.related-agencies` band, `.empty-state`. Prose block from M1 stays as-is — used by blog in M4.

### Why it helps

- **Pattern continuity end-to-end.** Homepage → state → city → agency all use the same token system, the same editorial register, and the same agency-card component. Navigating between them is visually continuous instead of the bolted-on-feature feeling the old mix of templates had.
- **Trust signals that actually signal.** Medicare Care Compare (where applicable) + state-licensing verification guidance (universal) replace a decorative weather link. YMYL healthcare content lives or dies by trust — replacing "here's the weather in Houston" with "here's how to verify this agency's license" is exactly the substitution audit reviewers look for.
- **SEO hardening.** `BreadcrumbList` JSON-LD on every directory page makes breadcrumbs eligible for SERP display. Sitemap noindex-leak fix prevents 3-agency-or-below state/city pages from showing up in GSC as "submitted URL not selected as canonical" warnings.
- **Accessibility.** Breadcrumb markup uses proper `<nav aria-label>` + `<ol>` + `aria-current="page"`. Agency hero rating stars use `aria-hidden` with a tabular-figure numeric value as the accessible reading.
- **Map on-brand.** CartoDB Positron tiles on the state map integrate visually with the warm off-white palette; the old OSM tiles stood out as a bright-blue rectangle against everything else.
- **Portfolio reuse.** The breadcrumb macro, agency-card partial, and page-head component port to the other three Kevin directory sites (holistic vet, splash pad, dog groomer) with only copy changes.

### Known gaps

- **`service.html`** still uses the old Tailwind markup but now inherits the new `_agency_card.html` partial (via `{% include %}`). The service page shell will look unstyled in production until its own milestone rewrite, but the cards inside it will render correctly.
- **`blog.html`, `post.html`** still Tailwind-styled — M4.
- **`about.html`, `contact.html`, `privacy.html`, `terms.html`, `submit.html`** still Tailwind-styled — M6.
- **Photo aspect-ratio on agency detail hero** set to 4/3 on ≥700px viewports; mobile falls back to the card's own ratio. Some Google Places photos are square and will letterbox inside the container. Acceptable — fallback icon handles missing photos gracefully.
- **No `HomeHealthCareService` schema nested inside `@graph` yet** — the per-agency schema is still top-level alongside the base.html sitewide `@graph`. Nesting is a future polish item; both are individually valid per schema.org.
- **Map tiles loaded from CartoDB over HTTPS.** CartoDB's free tier allows production directory usage per their ToS, but watch for rate-limit headers if the Airtable agency count pushes tile requests up.
- **`service.html` will visually break** on viewport between M2 deploy and M3/M6 rewrite. Acceptable per the plan's staged rollout; homepage and directory pages are the money pages.

---

## Milestone 1 — Homepage + base.html redesign (2026-04-20)

**Branch:** `redesign/homepage-healthcare-native`
**Commits:** `1f43b32` (planning docs), `fb608c3` (fonts), `82b9ead` (CSS), `2f086bd` (base.html), `6506e3e` (index.html)
**Templates rewritten:** `base.html` (full), `index.html` (full)
**Assets:** `static/fonts/` (4 WOFF2 files, 172 KB total), `static/css/custom.css` (171 → ~1400 lines)
**Build:** no `build.py` change required — new template variables (`max_state_count`) computed in-template via the `state_counts.values() | max` filter chain.

### What changed

- **Full visual pivot** from the blue-gradient SaaS hero + Tailwind card grid to an editorial healthcare-native layout aimed at adult children researching care for an aging parent. Audience-first framing, grade-8 reading level on body copy (CDC Clear Communication Index target for healthcare content).
- **Homepage sections top to bottom:** hero (eyebrow + Fraunces display headline + lede + state locator + 3 stats) → Ad Slot A → "How this works" 3-up editorial → Featured agencies (6-up cards with photos when present) → Ad Slot B → Browse by state (51-tile intensity heatmap, per-tile `--intensity` token from count/max) → Browse by service (10 service cards) → Guides & resources (blog category tiles with counts) → Ad Slot C → Editorial "what this is and isn't" anti-position block → FAQ accordion (schema preserved, copy rewritten to grade-8).
- **Typography:** Public Sans (USWDS, OFL) variable + Fraunces (OFL) variable, self-hosted as WOFF2 (latin + latin-ext subsets). Body scales to 18px base. Hero headline uses Fraunces `opsz 96 / SOFT 40` for editorial warmth without looking designerly.
- **Color tokens:** warm off-white bg (`#FAF9F6`) instead of cool gray; text brightened to `#4A5568` for muted (up from gray-500) to pass WCAG AA at small sizes for the 60+ eye cohort; primary deepened to `#1E4D8C`; accent deepened to `#D97706` for gold-leaf warmth. No dark mode — target audience strongly prefers light.
- **Tailwind CDN removed.** The render-blocking `<script src="https://cdn.tailwindcss.com">` + inline config block is gone from `base.html`. Sibling's M9 finding was that this was the single biggest mobile-perf win (~268 KiB unused JS); same applies here.
- **`base.html` fully rewritten** in semantic class names (`site-nav`, `site-nav__dropdown`, `mobile-menu`, `newsletter`, `site-footer`) backed by the design-token layer. All 16 other templates still reference the old Tailwind utility classes and will render unstyled until their own milestones — acceptable per the plan.
- **Universal schema upgrade:** `base.html` now emits an `@graph` JSON-LD block with `WebSite` + `Organization` cross-referenced by `@id`. This is the M7b-style sitewide E-E-A-T signal that was previously missing. `HomeHealthCareService` schema on agency pages stays — it'll be nested inside `@graph` as part of M2.
- **Mobile menu scroll-containment:** `100dvh` + `overscroll-behavior: contain` + body scroll-lock when open. Fixes the same iOS/Android scroll-chain bug the sibling fixed in M9.
- **Inline SVG brand mark** in nav and footer — zero image fetch on critical path; replaces the `&#128106;` family emoji that rendered inconsistently across platforms.
- **Three ad slots** reserved (`home-a` leaderboard, `home-b` and `home-c` in-content) with CLS-safe `min-height`. No `<ins>` tags yet — positions named via `data-slot` attributes so AdSense slot IDs can be dropped in via a separate scoped commit.
- **Font preload** links for Public Sans + Fraunces latin WOFF2 with `crossorigin`.
- **Mailchimp newsletter** retains the existing pattern, gains a hidden `SITE=senior-home-care` input for cross-site audience segmentation (sibling uses same pattern with `smart-investor`).
- **Accessibility:** skip-link, proper `aria-expanded` / `aria-haspopup` / `aria-controls` on nav and FAQ, `aria-label` on nav and footer, visually-hidden labels on search inputs.

### Why it helps

- **Credibility for a healthcare audience.** The finance-native register (data density, monospace numerics) would read as wrong for adult children researching elder care in crisis. The editorial healthcare register (warm paper bg, humanist type, generous leading, plain-English copy) reads as "trusted reference," closer to AARP or NIA than to a lead-gen site.
- **Performance.** Self-hosted fonts = zero third-party requests on the critical path. Tailwind CDN gone. Inline SVG brand mark. Font preloads for the above-fold Public Sans + Fraunces subsets. Expect the same-scale mobile Lighthouse bump the sibling got when it removed Tailwind in M9.
- **Accessibility.** 18px body is the single largest a11y win available for this audience. Contrast raised on muted text. Skip-link. Focus-visible rings tokenized. ARIA attributes on every interactive element.
- **CLS.** Ad slots have reserved heights. Hero stats use tabular figures. SVG icons don't pop in after fonts load.
- **SEO signal stability.** All URLs, canonicals, and OG tags unchanged. `FAQPage` JSON-LD preserved (rewritten to match the grade-8 visible copy). `WebSite` schema upgraded to `@graph` with `Organization` — a net E-E-A-T addition, not a regression. `msvalidate.01` Bing verification meta tag preserved.
- **YMYL trust signal.** Editorial anti-position block ("agencies don't pay to appear," "we don't sell your info," "we're not a medical-advice site") is the same load-bearing trust pattern the sibling uses on its finance site — explicit anti-positioning matters more in YMYL categories than in generic directories.
- **Portfolio reuse.** The component patterns established here (hero locator, stat block, how-it-works 3-up, agency-card row, state-tile intensity heatmap, service-card, guide-card, editorial block, FAQ accordion) will port to `holisticvetdirectory.com`, `splashpadlocator.com`, and `doggroomerlocator.com` with only copy and color-variable changes — same playground-purpose pattern the sibling's M1 established.

### Known gaps

- **All 14 other templates (state, city, agency, service, blog, post, _agency_card, about, contact, privacy, terms, submit, success) still reference the removed Tailwind utility classes** and will look unstyled until M2–M6 rewrite each. This is the expected "temporarily broken" state per the sibling's M1 → M2 cadence.
- **Three ad slots are placeholder-only** — `<div class="ad-slot__inner">Advertisement</div>` with no `<ins class="adsbygoogle">`. Kevin will drop in slot IDs in a separate scoped commit once he's picked positions in AdSense.
- **Site-wide `@graph` schema** is now universal in `base.html`, but per-page schemas on other templates (`HomeHealthCareService` on agency, `Article` on post) are still top-level; they should be merged into the `@graph` when those templates are redesigned in M2 / M4.
- **`BreadcrumbList` schema macro** not shipped this milestone — deferred to M2 where breadcrumbs actually appear (state / city / agency / post).
- **Sitemap truthy-check bug** (`build.py:844, 852`) not fixed in M1 — it's a build-script fix unrelated to homepage rendering. Recommend landing it as a side-milestone fix alongside the `success.html` noindex fix; both are one-line changes and both were M7b work on sibling.
- **Verified locally only against sample data (5 agencies).** Production build will hit Airtable's ~5,690 agencies; template logic uses `{{ total_count }}` and the `state_counts.values() | max` filter chain, both of which scale — but verify by watching Netlify's first post-merge build.
- **No Lighthouse run yet.** Synthetic perf numbers should be captured once the homepage is live on a branch preview; expected to land similarly to sibling's 91/97/100 mobile.

---

## Milestone 0 — Baseline inventory + planning groundwork (2026-04-20)

**No commits** — discovery + documentation.

### What happened

- Loaded the personal `smart-investor-redesign` skill plus its references (stack-conventions, adsense-constraints, finance-native-direction, directory-patterns) — the skill's naming is sibling-specific but the methodology applies verbatim.
- Read sibling-project artifacts in full:
  - `/Users/kevincollins/GitHub/financial-tools-directory/CLAUDE.md` — project instructions.
  - `/Users/kevincollins/GitHub/financial-tools-directory/REDESIGN_CHANGELOG.md` — 9 milestones + side-milestones (Tailwind removal, Mailchimp migration, GSC/Bing verification, fabricated-ratings removal).
  - `/Users/kevincollins/GitHub/financial-tools-directory/ADSENSE_RESUBMISSION_PLAN.md` — lessons-learned (many of which originated on this site and came back to the sibling).
- Inventoried this codebase: 16 templates, `build.py` (1015 lines), `config.py` (state + service editorial), `static/css/custom.css` (171 lines), `static/js/search.js`, `static/images/` (28 cached agency photos).
- **AdSense audit:** grep for `adsbygoogle` / `data-ad-slot` returned zero active slots anywhere — only the loader script in `base.html:64`. `.ad-container { min-height: 90px }` is CSS-defined but unused in any template. Homepage slot positions can be proposed freely.
- **Parity gap vs. sibling:** Tailwind CDN still render-blocking in `<head>`; `.prose` block has hardcoded colors (same dark-mode bug sibling fixed in M4); no `@graph` / Organization / BreadcrumbList / Article schema; `success.html` not noindexed; sitemap truthy-check bug present (same `if indexed_states:` bug sibling fixed in M7b); no self-hosted fonts; no design-token layer.
- **Already best-in-class here** (do not regress): `config.py` US_STATES × 51 with 100+ word unique editorial per state; SERVICES × 10 with 100+ word `intro` paragraphs; `HomeHealthCareService` schema on `agency.html`; noindex logic at `build.py:616`; parallel photo-caching in `build.py:208` + `refresh_photos.py`; Mailchimp + Netlify Forms fallback in `base.html`.
- Produced [`REDESIGN_PLAN.md`](REDESIGN_PLAN.md) — audience/aesthetic framing, typography + color proposal, homepage structure, milestone port/adapt/skip plan, list of what's already doing the right thing vs. what's broken, open questions for Kevin, and the proposed Milestone 1 scope.
- Created [`REDESIGN_NOTES.md`](REDESIGN_NOTES.md) — one-line-per-decision log.

### Why it helped

- Caught the Tailwind-CDN parity gap — same render-blocking issue as sibling, and the single biggest likely mobile-performance win on this site.
- Caught the sitemap truthy-bug parity gap (`build.py:844, 852`) — same noindex-leak bug sibling fixed in M7b; fix is a two-line change.
- Made the ad-slot decision explicit: zero slots active today, so positions are proposable without displacing revenue — flagged for Kevin's approval in the plan rather than assumed.
- Established the audience-first framing that rules out porting the sibling's aesthetic wholesale: data-dense Bloomberg-style UI is actively wrong for adult children researching elder care in crisis.
- Captured the three open questions (font licensing, color retune depth, reading-age target) that Kevin needs to answer before production code begins.

### Known gaps

- Milestone 1 (homepage + base.html) is drafted but not started — awaiting Kevin's approval on the plan.
- Open questions in the plan are not answered; proceeding without answers would bake in defaults that might need to be undone.
- No local build was reproduced in this session; next step before writing code is `python3 build.py` to confirm the current `dist/` output is what production looks like.

---

## How this file is maintained

- **One section per shipped milestone**, most recent at the top.
- Each section: date, branch, commits (short SHAs), scope, what changed, why it helps, known gaps.
- **"Why it helps" stays outcome-focused** — what the user / Google / the business gets. Technical minutiae belong in [`REDESIGN_NOTES.md`](REDESIGN_NOTES.md).
- **Past milestones are immutable.** When a known gap is later closed, note it in the milestone that closed it; do not edit earlier entries.
- When a pattern here later ports back to another Kevin directory site (holisticvetdirectory.com, splashpadlocator.com, doggroomerlocator.com), give that work its own section in the receiving project's changelog and reference this one by commit SHA.
