# Redesign Changelog — Senior Home Care Finder

Narrative log of the redesign work on `seniorhomecarefinder.com`. **Most recent milestone at the top.** Each entry captures what shipped, what it changed for users / Google / the business, and what's still open.

The methodology is ported from the `financial-tools-directory` sibling project — disciplined, documented, incremental — but the aesthetic is rethought for a healthcare / elder-care audience.

For the terse one-line-per-decision log, see [`REDESIGN_NOTES.md`](REDESIGN_NOTES.md). For the homepage plan, see [`REDESIGN_PLAN.md`](REDESIGN_PLAN.md). For the AdSense posture (this site is already approved), see [`ADSENSE_PRESUBMISSION_PLAN_SENIOR.md`](ADSENSE_PRESUBMISSION_PLAN_SENIOR.md).

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
