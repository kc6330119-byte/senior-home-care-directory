# SHCF AdSense Pre-Submission Audit (2026-05-08)

**Status:** Audit + plan only. No code changes. Awaiting Kevin's go-ahead before any remediation.

**Inputs verified against:** live `seniorhomecarefinder.com`, current `templates/`, current `build.py`, current `config.py`, current `validate_listings.py`, current `enrich_descriptions.py`, live `sitemap.xml` (6,171 URLs), 29-URL evenly-sampled live agency-page scan, fresh inspection of off-topic-pattern slugs.

**Reference patterns:** HVD post-rejection diagnosis (video-7-script.md), DGL pre-submission audit (2026-04-29), SPL audit + Batch 1/2 remediation (2026-05-06), AdSense playbook YMYL gates.

**Pre-submission plan already in repo:** `ADSENSE_PRESUBMISSION_PLAN_SENIOR.md` (created 2026-03-19). Many items marked DONE. This audit grades how those completed items are holding up against current scrutiny standards (HVD/SPL post-rejection bar) and surfaces what was missed or regressed.

---

## Phase 1 — Verification of handoff claims

| # | Claim (paraphrased) | Status | YMYL severity |
|---|---|---|---|
| 1 | "How to verify this agency" templated block on every agency page | **Confirmed (100% of sample)** | Critical |
| 2 | `aggregateRating` schema with no on-page review collection + display without source attribution | **Confirmed (~86% schema, ~93% body)** | Critical |
| 3 | Newsletter form posts to `doggroomerlocator` Mailchimp on every page | **Confirmed** | High (trust) |
| 4 | OG image + `/favicon.ico` return 404 | **Confirmed** | Low |
| 5 | Terms language disclaims editorial value (YMYL framing) | **Confirmed** | Medium |
| 6 | Templated Medicare Care Compare paragraph on Medicare-certified agency pages | **Confirmed but smaller-scope than feared** | Medium |
| 7 | No agency-level quality gate; `validate_listings.py` not part of build | **Confirmed (and worse: gate has a config bug)** | Critical |
| 8 | Sitemap composition upside-down (directory >> editorial) | **Confirmed (99.3% / 0.7%)** | High |

### 1. "How to verify this agency" block

**Evidence:** `templates/agency.html:237-248` renders the block in the right sidebar of every agency detail page. Three-line ordered list, with one line varying (license number text vs. "ask for the license number"). Sample of 29 evenly-spaced agency pages from the live sitemap: **29 / 29 (100%)** render the block.

Position is sidebar (slightly less of an AdSense red flag than main-column boilerplate), but with 5,690 agency URLs in the sitemap and 100% coverage, this is the HVD "About Our Specialties" pattern at 5,690 pages. 1,000 pages got HVD rejected for templated content; 5,690 is far past that threshold.

**Severity: Critical.**

### 2. `aggregateRating` schema + display

**Schema-level evidence:** `templates/agency.html:31-37` emits the JSON-LD `AggregateRating` block populated from `agency.rating` and `agency.review_count`. Source is Google Maps (third-party). 25 of 29 sampled pages emit the schema (~86%); extrapolated to ~4,900 of 5,690 indexable agency pages.

**Display-level evidence:** `templates/agency.html:83-91` renders `★★★★★ 4.5 (47 reviews)` in the hero with **no source attribution**. SPL had the same pattern on 2,126 pages and stripped it on 2026-05-06 to avoid manual-action exposure. Sampled body shows the rating in 27 of 29 pages (~93%).

**Compounding finding:** `enrich_descriptions.py:142-146` includes a rating sentence pool with explicit Google attribution: *"With a {rating}-star Google rating from {count} reviews, {name} is well-regarded by families in the area."* 21 of 29 sampled pages contain "Google rating" wording in the description body. So the body sometimes attributes the source — but the *hero display* and the *JSON-LD `AggregateRating`* still misrepresent it as the publisher's first-party rating.

**Severity: Critical.** Two separate manual-action surfaces (schema + hero) plus a body inconsistency.

**Recommendation:** Option A from handoff (remove rating display + schema entirely). YMYL standards are stricter than SPL's recreational profile, and the Brennity case below shows the rating data quality is actively harmful when paired with mis-classified listings.

### 3. Newsletter form

**Evidence:** `config.py:194-201` hardcodes `https://doggroomerlocator.us12.list-manage.com/subscribe/post?...` as the Mailchimp action URL. List ID differs from SPL's, but the *domain* is identical: a senior-care site posting newsletter signups to `doggroomerlocator`. Form is rendered on every page via `templates/base.html:191-219`.

The pattern is the same trust signal break that contributed to SPL's rejection environment. Kevin's previous directive (SPL): full removal of form, env vars, JS, related CSS, and any Privacy Policy mention.

**Severity: High** (trust signal, not a direct policy violation).

### 4. OG image + favicon 404

**Evidence:** `curl -sI https://seniorhomecarefinder.com/static/images/og-image.png` returns `HTTP 404`. Same for `/favicon.ico`. `templates/base.html:17` references the OG image as `https://res.cloudinary.com/dnmrgvjdm/image/upload/.../SeniorGuide_ybruqy.png` (Cloudinary fallback) — so social previews actually work, but only because of the Cloudinary URL, not the broken `/static/images/og-image.png` path. The `<link rel="icon" type="image/svg+xml">` data-URI at `base.html:98` covers browser tabs, but the legacy `/favicon.ico` request still 404s.

Cosmetic but trivially fixable.

**Severity: Low.**

### 5. Terms language

**Evidence:** `templates/terms.html:41` reads: *"we do not verify the credentials, licensing status, caregiver training, or quality of services of listed agencies on an ongoing basis. Every agency page includes a 'How to verify this agency' checklist; please use it before engaging any agency."*

For a YMYL site, this is the wrong framing. Compare to HVD's editorial-standards rewrite, which replaced the disclaimer-only stance with a positive description of what HVD *does* (license verification against state boards, AHVMA/IVAS cross-reference, update cadence). The current SHCF copy reads to a reviewer as "this is a scraped list with no editorial value-add."

**Severity: Medium** for first-time-submission YMYL bar.

### 6. Templated Care Compare paragraph

**Evidence:** `templates/agency.html:230-234` renders inside `{% if is_medicare_certified and agency.zip %}`. Per-page text:

> *"Medicare publishes quality ratings, patient-experience data, and complaint history for Medicare-certified agencies. Look up {{ agency.name }} on Care Compare to see the official record."*

Only the `{{ agency.name }}` substitution varies. Same templated-on-N-pages pattern as #1, but **scoped to Medicare-certified agencies only.**

**Scale:** 0 of 29 sampled pages contained the block in my scan. Medicare-certified agencies are a minority (gated by `'Medicare Certified' in (agency.accreditation or [])` OR `'Medicare' in (agency.payment_options or [])`). I could not get a precise count without an Airtable query, but the absence in a 29-URL sample suggests <500 pages, possibly <200.

**Severity: Medium.** Same pattern as #1, smaller surface area.

### 7. No agency-level quality gate (and the gate that exists has a config bug)

**Evidence — gate is missing from build:** `build.py` has `MIN_AGENCIES_FOR_INDEX = 3` (line 627) for state and city pages, but **no equivalent quality threshold for agency detail pages**. Every agency in the data feed is indexed regardless of description quality, category relevance, or AI-artifact presence. `is_thin_agency` does not exist. There is no equivalent to SPL's post-Batch-2 `evaluate_pad`.

**Evidence — validation script ran once at submission, not at build:** `validate_listings.py` exists. `ADSENSE_PRESUBMISSION_PLAN_SENIOR.md` reports it ran 2026-03-20 and removed 117 records. But the script is not invoked from `build.py`; it's a one-off Airtable cleanup. Anything added since 2026-03-20 (or anything that slipped through) is unguarded.

**Critical: the script's positive-keyword list contains residential-facility terms.** `validate_listings.py:46-48`:

```python
POSITIVE_KEYWORDS = [
    ...
    "assisted living", "adult day", "skilled nursing",
    "private duty", "non-medical", "nonmedical",
]
```

These four are **residential / institutional** terms, not in-home care. A senior-living facility containing "assisted living" in its name or description scores +2 positive (cumulative — caps at +4). Combined with any other positive match, that overrides the MEDIUM_NEGATIVE bucket (which contains "nursing home", "medical center", "hospital" at +2 each). The scoring math in `score_record` (lines 100-159) means a senior-living facility with a templated AI description containing "assisted living" + "personal care" + "elderly" easily scores `pos=4-6, neg=2`, which classifies as **LIKELY HOME CARE**.

**Verified concrete example:** `https://seniorhomecarefinder.com/agency/the-brennity-at-fairhope-senior-living-fairhope-al.html` is live and indexed. Its description (templated by `enrich_descriptions.py`) reads:

> *"The Brennity at Fairhope Senior Living brings experienced, compassionate caregivers to seniors throughout Fairhope and the surrounding Alabama communities. Their care team offers services including live-in care."*

That sentence is fabricated. The Brennity at Fairhope is a residential senior-living community, not an in-home care agency. The AI-generated templated description presents it as one, complete with a 4.8-star Google `aggregateRating`. This is the SPL "Galaxy Theatres Riverbank IMAX is a water play destination" pattern, transposed to YMYL healthcare.

**Slug-based scope estimate** (lower bound — only catches what the slug encodes):
- 26 `senior-living`
- 19 `assisted-living`
- 24 `rehabilitation` / `-rehab-`
- 64 `nursing` (mixed: some are "nursing home", some legitimately use "nursing" in home-care branding — needs manual sort)
- 5 `adult-day`
- 3 `memory-care`
- 2 `retirement-community`
- 1 `hospital`

**Floor: ~80 confirmed off-topic by slug alone (1.4%). Ceiling unknown — requires either a category-relevance pass or a venue-type whitelist applied to the dataset.**

The Brennity proves the pattern: an off-topic listing got a templated AI description that fabricates it as in-home care, then got an `aggregateRating` schema, then passed validation. A reviewer hitting two of these in five clicks fails the YMYL standard.

**Severity: Critical.**

### 8. Sitemap composition

**Evidence (live `sitemap.xml`):**

| Type | Count | % of total |
|---|---|---|
| Agency detail | 5,690 | 92.2% |
| City | 388 | 6.3% |
| State | 50 | 0.8% |
| Blog post | 26 | 0.4% |
| Service | 10 | 0.2% |
| Static (home, about, contact, privacy, terms, submit, blog index) | 7 | 0.1% |
| **Total** | **6,171** | 100% |

**Directory : Editorial ratio = 99.3% / 0.7%.** Identical shape to DGL's pre-rejection footprint (99.3%) and slightly worse than HVD's at rejection (98%).

If service pages are counted as editorial (they have substantive `intro` paragraphs in `config.py`), the ratio improves marginally to 99.1% / 0.9%. Still upside-down.

The blog content itself is strong — 26 posts, 25 of which are 2,200-3,000 words each, totaling ~67,000 words. Above the AdSense playbook 50,000-word target. **The problem is not blog volume; the problem is the directory-page count drowning the blog ratio.**

**Severity: High.** This alone is a rejection signal independent of content quality.

---

## Phase 2 — Findings the handoff didn't anticipate

### A. The agency descriptions are templated at scale (HVD pattern, 5x size)

This is the biggest finding of the audit.

**Evidence:** `enrich_descriptions.py` is a deterministic template generator. The script comment cites "2,592+ possible description combinations." But the *structural skeleton* is identical on every page:

1. Opening sentence (1 of 6 variations) — always `name + city + state` shape
2. Service intro phrase (1 of 4 variations) + care-type list
3. Payment sentence (1 of 3 variations)
4. Optional language sentence (1 of 3 variations)
5. Optional rating sentence (1 of 3 variations) — including the "{rating}-star Google rating" fragment
6. Optional hours sentence (1 of 3 variations)
7. Closing sentence (1 of 4 variations)

`ADSENSE_PRESUBMISSION_PLAN_SENIOR.md` reports the enrichment script processed **4,815 records on 2026-03-20**. That's **85% of the 5,690 indexable agency pages.**

**29-URL evenly-sampled scan from live `sitemap.xml`:**

| Templated phrase | Pages matched | % of sample |
|---|---|---|
| "How to verify this agency" | 29 / 29 | **100%** |
| "Their care team offers services including" | 18 / 29 | 62% |
| "Families can pay through" | 20 / 29 | 69% |
| "Reach out to ... discuss care options" | 21 / 29 | 72% |
| "brings experienced, compassionate caregivers" | 12 / 29 | 41% |
| `aggregateRating` schema present | 25 / 29 | 86% |
| "Google rating" body wording | 21 / 29 | 72% |

Five specific live meta-description samples confirm the rotation:

- `all-ways-caring-homecare-bethel-ak.html`: *"Serving the Bethel area, All Ways Caring HomeCare offers compassionate in-home care tailored to each client's needs..."*
- `right-at-home-iowa-city-ia.html`: *"Right at Home provides professional in-home care services to seniors and families in Iowa City, Iowa. Their care team offers services including hands-on assista[nce]..."*
- `the-brennity-at-fairhope-senior-living-fairhope-al.html`: *"The Brennity at Fairhope Senior Living brings experienced, compassionate caregivers to seniors throughout Fairhope and the surrounding Alabama communities..."*

Three of five share the same structural template with city/state/services swapped in. The fourth (`golden-care-la-mesa-ca`) has a non-templated description (Outscraper-sourced) — but that one mis-cites Carlsbad and San Diego County for an agency listed in La Mesa, an unrelated data-quality issue.

**This is the HVD "About Our Specialties" pattern at 5,690 pages instead of 1,000.** Google's templated-content detector picks up structural similarity even when individual nouns vary. The 6 × 4 × 3 × 3 × 3 × 4 × 3 = 7,776 theoretical combinations are spread across 5,690 pages — many duplicates inevitable.

**Severity: Critical.** This is the single biggest pre-submission risk and was **introduced by the remediation pass**, not pre-existing. The 2026-03-19/20 fix that "diversified descriptions" to address the templated-content concern produced templated content at scale.

### B. City pages have a doorway-pattern boilerplate (HVD pattern, 1.9x size)

**Evidence:** `templates/city.html:60-67` renders an identical wrapper paragraph below the agency cards on every indexed city page:

```
Home care in {{ city }} covers a range of services — companion care,
personal care, memory care, hospice support, and more. Each agency below
lists the services they offer and the payment options they accept, so
you can narrow your search quickly.

Before calling, write down a short list of what you need help with
(bathing, meals, driving to appointments, overnight coverage) and the
hours per week you're estimating. Most agencies offer a free in-home
assessment before care starts.
```

**388 indexed city pages emit this same paragraph.** Only the city name varies. Plus a templated lede at lines 24-31 (`{{ count }} in-home care agencies serving {{ city }}, {{ state.abbr }}. Compare services, payment options, and accreditation side-by-side`).

This is **identical to HVD's 207 city-page doorway pattern, scaled 1.9x.** HVD's diagnosis (2026-04-27): *"Just a 50-word templated intro and the same vet cards that appear on the state page above them. That's the textbook definition of what Google calls a doorway page."*

Same shape here: ~80-word templated wrapper + agency cards that already appear on the parent state page.

**Severity: Critical.** Same pattern, same root cause as HVD's rejection.

### C. Hero rating display has no source attribution (compounds finding #2)

**Evidence:** `templates/agency.html:83-91`:

```html
<div class="agency-hero__rating">
    <span class="agency-hero__rating-stars">{{ agency.rating | star_rating }}</span>
    <span class="agency-hero__rating-value">{{ agency.rating }}</span>
    {% if agency.review_count %}
    <span>({{ agency.review_count }} review{{ 's' if ... }})</span>
    {% endif %}
</div>
```

No "Google rating" label. The description body sometimes mentions Google (via `enrich_descriptions.py`'s rotated rating sentence), but the *hero* — which is the first thing a reviewer sees on every agency page — presents the rating as if it's first-party. Schema-display attribution mismatch with itself.

**Severity:** rolls up under finding #2.

### D. `validate_listings.py` is the wrong script for this site

Already covered in finding #7. The configuration in `POSITIVE_KEYWORDS` includes residential-facility terms ("assisted living", "adult day", "skilled nursing") that should be in `MEDIUM_NEGATIVE` for an in-home-care directory. This is what let The Brennity through.

**Severity:** rolls up under finding #7.

### E. Care Types vs Services drift in `enrich_descriptions.py`

**Evidence:** `enrich_descriptions.py:226` reads `Care Types` from Airtable. `ADSENSE_PRESUBMISSION_PLAN_SENIOR.md` Action 14 reports Care Types was consolidated into Services on 2026-03-19. If `Care Types` is now empty in Airtable, the enrichment script silently produces shorter descriptions (skips the care-type sentence) — which would make some listings even more thinly templated.

**Severity: Low** — adjacent data hygiene issue, only matters if enrichment is re-run.

### F. AI-refusal phrase scan inconclusive

Background scan of 200 random agency pages was killed before completing (no signal in partial output). My 29-URL hand-sample showed zero AI-refusal phrases, which is consistent with the build pipeline (descriptions go through `clean_description()` in `auto_descriptions.py:49-55`, which strips `nan`-only lines but does not check for refusal phrases). The Outscraper enrichment for non-home-care categories was never AI-generated for off-topic listings post-submission, so refusal phrases aren't expected here.

**Severity: Low** until proven otherwise. Recommend a full-corpus grep before submission. SPL had 4 such pages slip through; SHCF could have them too.

### G. No anti-positioning / editorial-standards page

**Evidence:** No `editorial-standards.html`, no equivalent on `about.html`, no positive YMYL framing anywhere. The only mention of editorial process is the `terms.html:41` disclaimer.

For a YMYL first submission with no rejection history, the absence of editorial standards is the framing AdSense reviewers will read as "scraped list."

**Severity: Medium.**

### H. `download_agency_images()` writes to repo at build time (deferred from prior session)

Already known. Not an AdSense rejection risk. Noted for completeness.

---

## Phase 3 — Fix plan ranked by AdSense impact

YMYL standards apply throughout. The primary failure mode is templated content at scale (findings #1, A, B). Secondary is mis-classified off-topic listings (#7). Tertiary is trust/cosmetic (#3, #4, #5, G).

| # | Fix | Findings addressed | Impact | Effort | Verdict |
|---|---|---|---|---|---|
| F1 | **Strip `aggregateRating` schema + remove rating from hero display** | #2, C | Critical | Small (template + JSON-LD edits) | **Ship freely** — same playbook as SPL Batch 1 |
| F2 | **Remove the "How to verify this agency" templated block from `agency.html`. Replace with one sentence linking to a single new editorial article at `/guides/how-to-verify-a-home-care-agency.html`** (1,500-2,000 words, YMYL-grade, written by Kevin, with state-by-state licensing-board lookup table) | #1 | Critical | Medium (1 new article + template edit) | **Ship with editorial article** — directly addresses the HVD pattern |
| F3 | **Replace `enrich_descriptions.py`-generated descriptions on indexable agency pages.** Three sub-paths: (a) for agencies with original Outscraper descriptions of useful length, restore the original; (b) for thin-only agencies, noindex them; (c) for any remaining, regenerate with Claude Haiku using a one-shot prompt that varies *structure* not just nouns, with an artifact-phrase blacklist. Cost estimate: ~$20 if path (c) covers ~5,000 records. | A | Critical | Large (new pipeline + Airtable rewrite) | **Critical to discuss before shipping** — open question 1 below |
| F4 | **Noindex city pages by default; convert to a state-grouped hub page approach OR remove the templated wrapper paragraph and add per-city editorial (top 50 cities by listing count)** | B | Critical | Large (template rewrite + 50-city editorial pass) | **Ship with editorial pass for top cities; noindex the long tail** |
| F5 | **Tighten `validate_listings.py`:** move `assisted living`, `adult day`, `skilled nursing`, `senior living`, `nursing home`, `rehabilitation`, `memory care`, `retirement community`, `hospice facility`, `assisted living facility` to a NAME-based hard-fail list. Re-run on full Airtable. Add a venue-type whitelist (in-home care, home health, personal care, companion care, respite, dementia care, hospice support, etc.). Flag everything else for manual review. | #7, D | Critical | Medium (script edits + full re-validation) | **Ship before F3 path (c)** so you don't AI-enrich off-topic listings again |
| F6 | **Remove newsletter form entirely** — template, env vars, JS, related CSS, Privacy Policy mention if any. Same scope as SPL Batch 1 F6. | #3 | High (trust) | Small | **Ship freely** |
| F7 | **Add real `og-image.png` (1200×630, brand-consistent) + real `/favicon.ico`.** Same recipe SPL used (PIL generators committed under `scripts/`). | #4 | Low | Small | **Ship freely** |
| F8 | **Rewrite Terms anti-positioning section with positive YMYL framing.** Replace "we do not verify" with a description of what SHCF *does*: cross-references Medicare Care Compare for Medicare-certified agencies, captures licensing numbers from Outscraper / state databases, links directly to state licensing boards on every detail page, retires listings flagged by users. Frame factually. | #5 | Medium | Small (copy edit) | **Ship freely** |
| F9 | **Add `/about/editorial-standards.html`** describing data sources, update cadence, anti-positioning ("we are not medical professionals"), what reviewers can expect from listing quality. Same template SI used post-resubmission. | G | Medium | Medium (1 new page) | **Ship with F8** |
| F10 | **Strip the templated Care Compare wrapper from `agency.html:230-234`.** Replace with a one-line link to a new short editorial article `/guides/how-to-use-medicare-care-compare.html`. | #6 | Medium | Small | **Ship freely** |
| F11 | **Full-corpus AI-artifact phrase scan** across `dist/agency/*.html` after F3 lands. Confirm zero matches before submission. | F | Low (precaution) | Small | **Ship as gate, not as edit** |
| F12 | **Sitemap regeneration** — falls out of F4 (city noindex), F5 (off-topic noindex), and F3 (thin noindex). Should drop from 6,171 to ~5,000-5,400 URLs depending on how aggressively F3 path (b) is applied. | #8 | High | None (derived) | Safe, derived |

### Resubmission gate snapshot

| Gate | Current state |
|---|---|
| Zero AI-refusal phrases on indexed URLs | ⚠️ unverified (no full-corpus scan yet) |
| Zero confirmed off-topic listings indexed | ❌ ~80 confirmed by slug, ceiling unknown |
| Sitemap reduced to verified, on-topic URLs only | ❌ 6,171 URLs, validation not part of build |
| `is_thin_agency` checks description quality, not just length | ❌ does not exist |
| Description templating eliminated or reduced to tolerable scale | ❌ ~85% of agencies use the template |
| City pages have unique editorial OR are noindexed | ❌ identical wrapper on 388 indexed pages |
| Newsletter form fully removed | ❌ DGL Mailchimp form live on every page |
| OG image + favicon return 200 | ❌ both 404 |
| `aggregateRating` schema removed (or backed by on-page reviews) | ❌ ~4,900 pages emit it |
| Templated detail-page blocks removed (verify, Care Compare) | ❌ both still rendered |
| Editorial standards page exists | ❌ |
| Terms framing is positive-YMYL not disclaimer-only | ❌ |
| About / Contact / Submit / Privacy / Terms accessible | ✅ |
| `ads.txt` valid | ✅ |
| Blog ratio ≥ 25 posts at 1,500+ words each | ✅ 25 posts, 2,200-3,000 words each, ~67,000 total |
| State pages have unique editorial | ✅ `config.US_STATES` has unique 3-4 sentence state descriptions |
| Service pages have unique editorial | ✅ `config.SERVICES` `intro` paragraphs are substantive |

**Pass count: 4 / 17.** Worse than SPL pre-Batch-1 (2 / 12) on a normalized basis.

---

## Phase 4 — Open questions for Kevin

### 1. Description-template scope (F3) — the single biggest call

The `enrich_descriptions.py`-generated descriptions on ~4,815 records are the single biggest rejection risk. Three paths, in order of cost / risk / quality:

**(a) Restore Outscraper originals where they exist + noindex everything else.** Cheapest. Sitemap drops to ~3,000 URLs. Risk: many Outscraper descriptions are themselves thin (that's why enrichment ran), and "everything else" would be a large fraction of the directory.

**(b) Re-AI-generate with a structurally-varied prompt (Claude Haiku, ~$20).** Spends ~$20 to write per-listing descriptions that don't share a template skeleton. Open prompt-design question: how do we ensure structural variation across 5,000 records? Probably need a per-record prompt seed mixing the agency's unique facts.

**(c) Hybrid: noindex everything that isn't already factually-rich (license number + multiple services + coverage area), use option (b) for the trimmed remainder.** Smallest indexed footprint, highest per-page quality.

**My recommendation: (c).** Aligns with the AdSense playbook's "smaller and stronger" principle. Sitemap likely lands at ~3,500-4,000 URLs of indexable agencies, all with non-templated descriptions. **Confirm before any pipeline work begins.**

### 2. Rating display — Option A or Option B (handoff question)

Handoff recommends Option A (remove rating display + schema entirely). I agree given (a) the data quality on senior-care agency Google ratings is uncertain — many ratings are based on <10 reviews skewed by either family praise or a single complaint, and (b) YMYL bar is stricter than SPL's recreational profile.

**Confirm: strip rating + `aggregateRating` schema entirely (Option A)?**

### 3. City page treatment (F4)

Two sub-paths:

**(a) Mass-noindex cities + rebuild the IA so navigation goes state → agency directly.** Drops ~388 URLs. Removes the doorway pattern in one move.

**(b) Hand-write per-city editorial for top 50 by listing count + noindex the long tail.** Preserves the IA but adds substantial work (50 × 300-word editorial blurbs = ~15,000 words of original content).

DGL's pre-rejection city pattern got noindexed wholesale in their planned remediation. SHCF has the advantage that city is already a legitimate user-search intent for home care ("home care in Houston"). **Recommend (b) for the top 50, (a) for the rest.** Confirm scope.

### 4. Off-topic listing noindex order (F5 + F3)

`validate_listings.py` config bug must be fixed BEFORE any new AI enrichment runs. If F3 path (c) ships first with the existing positive-keyword list, we'll regenerate templated descriptions for senior-living facilities again. **Confirm: F5 (validation tightening) lands and re-runs against full Airtable before F3 starts.**

### 5. Editorial scope vs. submission urgency

The combined fix list is meaningfully larger than SPL's. F2 (editorial article on verifying an agency), F4(b) (50 city editorial blurbs), F8 + F9 (Terms rewrite + editorial-standards page), F3 path (c) (description regeneration), and F10 (Care Compare article) total roughly **20,000-25,000 words of new editorial + a description-regeneration pipeline**. At the playbook timeline (3-week minimum GSC recrawl after fixes), submission is **realistically 4-5 weeks out from when remediation begins.**

Acceptable timeline, or is there pressure to submit sooner? If sooner: F1 + F5 + F6 + F7 + F8 + city-noindex (mass) + agency-noindex on validation-flagged listings is a **minimum-viable submission**, but at the cost of a smaller indexed footprint and a higher chance the templated description pattern (untreated) is the rejection reason.

### 6. Branded-query traffic guardrail

Per the DGL/SPL playbook, before any noindex pass we cross-reference GSC traffic so the noindex doesn't nick currently-clicking pages. SHCF has only 2 lifetime Google clicks (handoff context). The guardrail isn't load-bearing this round. **Confirm: treat noindex passes as pure-positive; no protected-URL list needed.**

### 7. AI-refusal phrase scan (F11)

Should I run a full-corpus grep on `dist/agency/*.html` against the 16-pattern blacklist used in SPL Batch 2 (`PAD_ARTIFACT_PATTERNS`) before any work begins, or after F3 / F5 land? Doing it now gives us a baseline; doing it after gives a clean gate-pass signal. **Recommend: now (15-min job), then again after F3/F5 as a gate.**

---

## Surprises (not in handoff)

1. **The biggest rejection risk is the remediation that already happened, not the rejected status quo.** `ADSENSE_PRESUBMISSION_PLAN_SENIOR.md` reports 4,815 descriptions enriched on 2026-03-20 to address the templated-content concern. The enrichment script produces templated content at 5,690-page scale — **the HVD "About Our Specialties" pattern, by another route.** This is the single biggest finding, and the handoff didn't anticipate it because the handoff focused on the templated-block patterns (HVD-style FAQ, verify-block, Care Compare) and not the description-generation pipeline itself. The blocks are real problems; the descriptions are a 5x bigger problem.

2. **`validate_listings.py` actively classifies senior-living facilities as positive matches.** Lines 47-48 list "assisted living", "adult day", "skilled nursing" as POSITIVE_KEYWORDS. That's the configuration error that let The Brennity at Fairhope — a residential senior-living community — into the directory with a fabricated home-care description and a Google `aggregateRating`. Anyone reviewing the script for a different niche would have caught this; it didn't surface during the original 2026-03-20 validation run because the run used this same buggy config.

3. **City pages are a textbook HVD doorway pattern at 1.9x scale (388 vs 207).** This was not flagged in the handoff. The `templates/city.html:60-67` boilerplate is identical to HVD's diagnosed problem, just with a different domain.

4. **Blog content quality is excellent and the playbook target is met.** 25 posts × 2,200-3,000 words = ~67,000 words. Above the 50,000-56,000 SI/SHCF reference targets. **The blog is not the problem and shouldn't be touched.** Every other site in the portfolio at this stage was *short* on blog content; SHCF is *long*. The fix list focuses entirely on the directory side.

5. **No geo-block, no AI-refusal phrases in initial sample, no FAQ-on-detail-page block.** Three classes of issue that bit other portfolio sites are absent here. SHCF's structural surface is *cleaner* than SPL's pre-rejection state — which is why the templated-description finding lands so hard. There's no other big drain to compete with it for blame.

---

## Honest assessment

**Top three pre-submission risks (ranked):**
1. Templated descriptions on 4,815 of 5,690 agency pages (Phase 2A). This is the HVD pattern at 5x scale and was introduced by the existing remediation pass.
2. The 99.3% / 0.7% directory-to-editorial ratio, driven by 5,690 indexable agency URLs and 388 templated-wrapper city pages (#8 + Phase 2B).
3. `aggregateRating` schema spam on ~4,900 pages with no on-page reviews (#2). Manual-action risk independent of AdSense.

**Honest call vs HVD/SPL:** SHCF is **further from ready than SPL was post-Batch 2**, but the underlying issues are more *structurally fixable* than HVD's. The blog content is strong, the static pages are accessible, the design is mature, the schema is otherwise well-structured. The fix list is large but mechanical: tighten the validation script, regenerate descriptions on a smaller indexed footprint, kill the templated city wrapper, strip the rating schema, ship the editorial articles. None of it requires a redesign.

**Estimated remediation timeline:** 7-10 days of engineering + 3-week GSC recrawl + 1-4 week AdSense review = **submission ~4-6 weeks out from go-ahead.** Faster (~3-4 weeks) if Kevin elects the minimum-viable path in question 5.

**Single biggest surprise:** the templated-description finding (Phase 2A). Specifically the discovery that the 2026-03-19 "diversification" remediation produced templated content at scale via a deterministic hash-keyed sentence-pool generator. The handoff focused on the visible HVD-shaped blocks (verify, Care Compare) but the descriptions themselves — the largest text on every detail page — share the same structural skeleton across thousands of pages. That's the AdSense reviewer's first read on every detail page and the strongest signal of programmatic content the site emits.

---

## Next step

Awaiting Kevin's response to the open questions above (especially Q1 description-template scope, Q2 rating Option A vs B, Q3 city page treatment, Q5 editorial-vs-urgency tradeoff). No code changes until at least Q1 and Q5 are decided, since those frame the scope of every subsequent fix.
