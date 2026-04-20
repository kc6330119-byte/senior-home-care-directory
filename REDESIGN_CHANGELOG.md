# Redesign Changelog — Senior Home Care Finder

Narrative log of the redesign work on `seniorhomecarefinder.com`. **Most recent milestone at the top.** Each entry captures what shipped, what it changed for users / Google / the business, and what's still open.

The methodology is ported from the `financial-tools-directory` sibling project — disciplined, documented, incremental — but the aesthetic is rethought for a healthcare / elder-care audience.

For the terse one-line-per-decision log, see [`REDESIGN_NOTES.md`](REDESIGN_NOTES.md). For the homepage plan, see [`REDESIGN_PLAN.md`](REDESIGN_PLAN.md). For the AdSense posture (this site is already approved), see [`ADSENSE_PRESUBMISSION_PLAN_SENIOR.md`](ADSENSE_PRESUBMISSION_PLAN_SENIOR.md).

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
