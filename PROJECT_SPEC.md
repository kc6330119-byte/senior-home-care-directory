# Senior Home Care Finder — Project Specification

## Project Overview
Building a **national in-home care agency directory** at **seniorhomecarefinder.com**. This site helps adult children find non-medical home care agencies for their aging parents. The audience has extremely high search intent — they're actively looking for help.

This is the third site in a directory factory. The first two (splashpadlocator.com, holisticvetdirectory.com) proved the playbook. This project follows the same architecture with domain-specific adaptations.

**Key differentiator:** Clean, fast, SEO-optimized state/city pages targeting local search gaps that national players (caring.com, aplaceformom.com) don't serve well.

---

## Market Analysis

### Search Volume & Intent
- "home care near me" — millions of monthly searches
- "home care agencies in [city]" — high commercial intent
- Adult children searching for parents — emotionally charged, high-value audience
- Searches spike during family crises (hospital discharge, declining health)

### Competitive Landscape
**National players dominate generic queries:**
- caring.com, aplaceformom.com — lead-gen focused, poor UX
- seniorcare.com — 39,000+ agencies, data-heavy interface
- Gaps at city/local level for clean, fast results

**Our edge:** Same playbook that worked for splash pads — superior local SEO pages with clean UX

### Monetization Opportunity
- **Lead gen:** $20-60 per qualified inquiry
- **Premium listings:** Agencies pay for featured placement
- **AdSense:** High CPMs in senior care vertical
- **Affiliate:** Medical alert systems, home safety products
- **Target:** $5-10K/month revenue within 12 months

---

## Target Keywords (by page type)
| Page Type | Target Keywords | Search Volume |
|-----------|----------------|---------------|
| Homepage | "find home care near me", "senior home care finder" | High |
| State pages | "home care agencies in [state]", "[state] home care services" | Medium-High |
| City pages | "home care in [city]", "[city] home care agencies", "in-home care [city] [state]" | **MONEY KEYWORDS** |
| Agency pages | "[agency name] reviews", "[agency name] [city]" | Long-tail |
| Service pages | "[service type] near me", "companion care services", "alzheimers home care" | Medium |

---

## Service Categories (for filter pages)

```python
SERVICES = [
    {"name": "Companion Care", "slug": "companion-care", "description": "Companionship, conversation, and social engagement for seniors living at home", "icon": "🤝"},
    {"name": "Personal Care", "slug": "personal-care", "description": "Assistance with bathing, dressing, grooming, and daily personal hygiene", "icon": "🛁"},
    {"name": "Homemaking", "slug": "homemaking", "description": "Light housekeeping, meal prep, laundry, and household management", "icon": "🏠"},
    {"name": "Alzheimer's & Dementia Care", "slug": "alzheimers-dementia", "description": "Specialized care for seniors with Alzheimer's disease or other forms of dementia", "icon": "🧠"},
    {"name": "Respite Care", "slug": "respite-care", "description": "Temporary relief for family caregivers — short-term professional coverage", "icon": "🔄"},
    {"name": "Live-In Care", "slug": "live-in-care", "description": "Around-the-clock caregivers who live in the senior's home", "icon": "🏡"},
    {"name": "Post-Surgery Care", "slug": "post-surgery", "description": "Recovery assistance after hospital stays or surgical procedures", "icon": "🏥"},
    {"name": "Veterans Care", "slug": "veterans-care", "description": "Home care services for veterans, including VA-eligible agencies", "icon": "🎖️"},
    {"name": "Hospice Support", "slug": "hospice-support", "description": "Comfort care and end-of-life support for seniors and their families", "icon": "💜"},
    {"name": "Transportation", "slug": "transportation", "description": "Rides to medical appointments, errands, and social activities", "icon": "🚗"},
]
```

---

## Airtable Schema (Complete)

### Base Name: "Senior Home Care Finder"
### Table Name: "Agencies"

| Field Name | Airtable Type | Notes |
|-----------|--------------|-------|
| Name | Single line text | Agency name |
| Slug | Single line text | URL-safe slug (auto-generated if empty) |
| Description | Long text | 2-4 sentences about the agency |
| Address | Single line text | Street address |
| City | Single line text | City name |
| State | Single line text | Full state name (e.g. "Texas", not "TX") |
| Zip | Single line text | ZIP code |
| County | Single line text | County name (useful for rural areas) |
| Phone | Single line text | Primary phone |
| Website URL | URL | Agency website |
| Google Maps URL | URL | Direct Google Maps link |
| Photo URL | URL | Agency photo or logo |
| Hours | Single line text | e.g. "Mon-Fri: 8am-6pm, 24/7 On-Call" |
| Services | Multiple select | See service categories above |
| Care Types | Multiple select | Options: Companion Care, Personal Care, Homemaking, Respite Care, Live-In Care, 24-Hour Care, Hospice Support, Alzheimer's/Dementia, Post-Surgery, Veterans Care |
| Payment Options | Multiple select | Options: Private Pay, Medicare, Medicaid, Long-Term Care Insurance, VA Benefits |
| Licensing | Single line text | State license number if available |
| Accreditation | Multiple select | Options: Medicare Certified, Joint Commission, CHAP, BBB Accredited |
| Languages | Multiple select | Options: English, Spanish, Chinese, Vietnamese, Korean, Tagalog, Other |
| Service Area | Long text | Cities/counties served |
| Year Established | Number | Year agency was founded |
| Rating | Number | 0.0 - 5.0 (Google rating) |
| Review Count | Number | Number of Google reviews |
| Status | Single select | Options: Active, Featured, Draft, Closed |
| Date Added | Date | Auto-set on import |
| Latitude | Number | For future map features |
| Longitude | Number | For future map features |

### Table Name: "Blog Posts"

| Field Name | Airtable Type | Notes |
|-----------|--------------|-------|
| Title | Single line text | Post title |
| Slug | Single line text | URL slug |
| Content | Long text | Markdown content |
| Excerpt | Long text | Short summary for cards |
| Author | Single line text | Default: "Senior Home Care Finder Staff" |
| Publish Date | Date | Publication date |
| Featured Image | URL | Hero image URL |
| Meta Description | Single line text | SEO meta description |
| Status | Single select | Options: Draft, Published |
| Featured | Checkbox | Show on homepage |
| Category | Single select | Options: Guides, Tips, Resources, News |

---

## Data Pipeline

### Outscraper Google Maps Categories
Search queries for Outscraper:
- "Home care agency" (primary)
- "Home health care service"
- "Non-medical home care"
- "Senior home care"
- "In-home care service"
- "Companion care service"
- "Personal care agency"

### Data Volume Estimates
- **Total market:** 40,000–60,000 agencies nationally
- **Launch target:** 5,000 agencies (start with 5-10 major states)
- **Growth target:** 15,000+ agencies within 6 months

### Outscraper Field Mapping → Airtable
| Outscraper Field | Airtable Field |
|-----------------|----------------|
| name | Name |
| full_address | Address |
| city | City |
| state | State |
| postal_code | Zip |
| phone | Phone |
| site | Website URL |
| place_url | Google Maps URL |
| photo | Photo URL |
| working_hours | Hours |
| rating | Rating |
| reviews | Review Count |
| latitude | Latitude |
| longitude | Longitude |

### Data Cleaning Rules
- Normalize state names: "TX" → "Texas", "CA" → "California"
- Remove duplicate agencies (same name + same city)
- Strip agencies with no phone AND no website (likely defunct)
- Default Status = "Active"
- Generate slug from: `slugify(name + "-" + city)`

---

## Design Specification

### Color Scheme
- **Primary:** Warm blue `#2563EB` (trust, healthcare)
- **Secondary:** Soft teal `#0D9488` (calm, caring)
- **Accent:** Warm amber `#F59E0B` (friendly, approachable)
- **Background:** White `#FFFFFF` with light gray sections `#F9FAFB`
- **Text:** Dark gray `#1F2937`

### Design Philosophy
- **Warm and trustworthy** — this audience is stressed and emotional (searching for help for a parent)
- **Clean and scannable** — large text, clear CTAs, easy navigation
- **Mobile-first** — many searches happen on phones during family discussions
- **Fast** — static site, minimal JS, optimized images
- NOT flashy or trendy — professional and reassuring

### Key UI Elements
- **Hero section:** Large search bar ("Find home care agencies in your area"), warm hero image of caregiver with senior
- **State browse grid:** 50 states + DC with agency counts
- **Agency cards:** Name, city/state, services offered, rating stars, phone number
- **Agency detail page:** Full info, services list, payment options, map embed, "Visit Website" and "Call Now" CTAs
- **City pages:** List of agencies in that city with service filters
- **Trust signals:** Accreditation badges, review counts, years established

### Typography
- Headlines: Inter or system sans-serif, bold
- Body: Inter or system sans-serif, regular
- Use Tailwind's default font stack initially

---

## URL Structure (SEO Architecture)

```
/                                    → Homepage
/state/texas.html                    → State listing (all agencies in Texas)
/state/texas/houston.html            → City listing (agencies in Houston, TX) ← **MONEY PAGE**
/agency/comfort-keepers-houston.html → Individual agency page
/services/companion-care.html        → Service category filter
/blog.html                           → Blog listing
/blog/how-to-choose-home-care.html   → Blog post
/about.html                          → About
/contact.html                        → Contact
/submit.html                         → Submit listing
/privacy.html                        → Privacy policy
/terms.html                          → Terms
```

### Key SEO pages (high search intent):
- `/state/{state}.html` → "home care agencies in Texas"
- `/state/{state}/{city}.html` → "home care agencies in Houston TX" ← **THIS IS THE MONEY PAGE**
- `/agency/{slug}.html` → individual agency (long-tail)
- `/services/{service}.html` → "companion care near me", "alzheimers home care"

---

## SEO Strategy

### JSON-LD Schema
Every agency page should include `LocalBusiness` structured data:
```json
{
  "@context": "https://schema.org",
  "@type": "HomeHealthCareService",
  "name": "Agency Name",
  "address": { ... },
  "telephone": "...",
  "url": "...",
  "aggregateRating": { ... }
}
```

### Meta Tags
Every page needs:
- Unique `<title>` tag (under 60 chars)
- Unique `<meta name="description">` (under 160 chars)
- Open Graph tags (og:title, og:description, og:image, og:url)
- Canonical URL

### Content Strategy (Blog Topics for SEO)

Priority blog posts to write:
1. "How to Choose a Home Care Agency: A Complete Guide"
2. "Home Care Costs by State: 2026 Price Guide"
3. "Medicare vs Medicaid: What's Covered for Home Health Care?"
4. "10 Questions to Ask Before Hiring a Home Care Agency"
5. "Types of In-Home Care Services Explained"
6. "When Is It Time to Get Home Care for a Parent?"
7. "How to Pay for Home Care: Insurance, VA Benefits & Financial Options"
8. "Non-Medical vs Medical Home Care: What's the Difference?"
9. "Home Care for Alzheimer's & Dementia: What to Know"
10. "Best Home Care Agencies in [State] — 2026 Guide" (template for each state)

---

## Monetization Strategy

### Phase 1 (Launch - Months 1-3)
- **Google AdSense** — Same publisher account, apply for new domain
- **Ad placements:** Top of page (leaderboard), sidebar on desktop, between listings on mobile
- **Target:** $500-1,000/month from AdSense

### Phase 2 (Growth - Months 4-8)
- **Lead generation:** "Request Info" forms that email agency contact — charge per lead ($20-60)
- **Premium listings:** Agencies pay for featured placement, photos, enhanced profiles
- **Target:** $2,000-4,000/month combined revenue

### Phase 3 (Scale - Months 9-12)
- **Mediavine** — Switch from AdSense once traffic hits 50K sessions/month
- **Direct advertising:** Home care franchises buy state/city sponsorships
- **Affiliate:** Senior care products, medical alert systems, home safety equipment
- **Target:** $5,000-10,000/month total revenue

### Revenue Model Details
- **Lead gen pricing:** $25-40 per qualified form submission
- **Premium listings:** $50-100/month per agency for featured placement
- **Sponsored content:** $500-1,000 per sponsored blog post
- **Directory sponsorship:** $200-500/month for city-level sponsorship

---

## Technical Implementation

### Environment Variables

#### Local (.env)
```
AIRTABLE_API_KEY=your_airtable_api_key
AIRTABLE_BASE_ID=your_base_id
AIRTABLE_TABLE_NAME=Agencies
AIRTABLE_BLOG_TABLE_NAME=Blog Posts
SITE_URL=https://seniorhomecarefinder.com
GA_MEASUREMENT_ID=G-XXXXXXXXXX
```

#### Netlify Dashboard
Set the same variables in: Site settings → Environment variables

### Netlify Configuration

```toml
[build]
  command = "pip install -r requirements.txt && python build.py"
  publish = "dist"

[[redirects]]
  from = "/state/:state"
  to = "/state/:state.html"
  status = 200

[[redirects]]
  from = "/state/:state/:city"
  to = "/state/:state/:city.html"
  status = 200

[[redirects]]
  from = "/agency/:slug"
  to = "/agency/:slug.html"
  status = 200

[[redirects]]
  from = "/services/:service"
  to = "/services/:service.html"
  status = 200

[[redirects]]
  from = "/blog/:slug"
  to = "/blog/:slug.html"
  status = 200

[[headers]]
  for = "/*"
  [headers.values]
    X-Frame-Options = "DENY"
    X-XSS-Protection = "1; mode=block"
    X-Content-Type-Options = "nosniff"
    Referrer-Policy = "strict-origin-when-cross-origin"
```

---

## Launch Checklist

### Phase 1: Build (Weeks 1-2)
- [ ] Create all Python files (build.py, config.py, requirements.txt)
- [ ] Build all Jinja2 templates
- [ ] Set up Airtable base with proper schema
- [ ] Import initial dataset (5 major states)
- [ ] Test build locally

### Phase 2: Deploy (Week 3)
- [ ] Connect GitHub to Netlify
- [ ] Point domain DNS
- [ ] Set environment variables
- [ ] Deploy and test production build
- [ ] Set up GA4 property

### Phase 3: SEO Setup (Week 4)
- [ ] Submit to Google Search Console
- [ ] Submit sitemap
- [ ] Create Google My Business for brand
- [ ] Apply for AdSense on new domain
- [ ] Set up basic blog content (5 initial posts)

### Phase 4: Growth (Months 2-3)
- [ ] Expand to all 50 states
- [ ] Build contact forms for lead generation
- [ ] Add premium listing features
- [ ] Launch content marketing strategy
- [ ] Begin outreach to agencies

---

## Success Metrics

### Traffic Goals
- **Month 1:** 1,000 sessions
- **Month 3:** 5,000 sessions  
- **Month 6:** 15,000 sessions
- **Month 12:** 50,000+ sessions

### Revenue Goals
- **Month 3:** $500/month (AdSense)
- **Month 6:** $2,000/month (AdSense + leads)
- **Month 12:** $5,000-10,000/month (full monetization)

### Content Goals
- **Launch:** 500+ agencies, 5 blog posts
- **Month 3:** 2,000+ agencies, 15 blog posts
- **Month 6:** 5,000+ agencies, 25 blog posts
- **Month 12:** 10,000+ agencies, 50+ blog posts

---

## Risk Assessment

### Technical Risks
- **Low:** Using proven tech stack
- **Mitigation:** Copy successful patterns from splash pad site

### Market Risks
- **Medium:** Competitive space with established players
- **Mitigation:** Focus on local SEO gaps, superior UX

### Business Risks
- **Medium:** Depends on Google traffic
- **Mitigation:** Diversify traffic sources, direct relationships with agencies

### Cost Risks
- **Low:** Minimal hosting costs, profitable at small scale
- **Mitigation:** Start with AdSense, scale monetization gradually

---

## Lessons Learned from Previous Sites

### What Worked (Splash Pad)
- ✅ Static site generator with Airtable backend
- ✅ State-by-state SEO page structure
- ✅ Clean, fast-loading design
- ✅ Netlify hosting + deployment
- ✅ Sample data fallback for development

### What to Improve
- ✅ **Add city-level pages** — the missing piece from splash pad site
- ✅ **Better structured data** — JSON-LD for local business
- ✅ **Enhanced contact forms** — lead generation capability
- ✅ **More service categories** — broader filtering options
- ✅ **Premium listing features** — monetization beyond AdSense

### Technical Lessons
- Always include ads.txt in build output
- Use full state names, not abbreviations
- Netlify Forms need specific attributes
- JS fetch for form submission (not native submit)
- Clear cache and deploy after form changes

---

This specification provides the complete strategic and technical foundation for building the Senior Home Care Finder directory. It combines proven patterns from the successful splash pad site with enhancements specific to the senior care market opportunity.