#!/usr/bin/env python3
"""
Senior Home Care Finder - Static Site Generator

Fetches home care agency listings from Airtable and generates a static HTML site.
Falls back to sample data if Airtable is not configured.
"""
import json
import os
import shutil
from datetime import datetime
from pathlib import Path

import markdown as md_lib
from jinja2 import Environment, FileSystemLoader
from markupsafe import Markup
from slugify import slugify

import config


def get_sample_data():
    """Return sample agencies for testing without Airtable."""
    return [
        {
            "name": "Comfort Keepers",
            "slug": "comfort-keepers-houston",
            "description": "Comfort Keepers provides award-winning in-home care for seniors. Our caregivers help with daily activities, companionship, and personal care while promoting independence and dignity.",
            "address": "1234 Main Street, Suite 100",
            "city": "Houston",
            "state": "Texas",
            "state_slug": "texas",
            "city_slug": "houston",
            "zip": "77001",
            "county": "Harris County",
            "phone": "(713) 555-0100",
            "website_url": "https://www.comfortkeepers.com",
            "google_maps_url": "",
            "photo_url": "",
            "hours": "Mon-Fri: 8am-6pm, 24/7 On-Call",
            "services": ["Companion Care", "Personal Care", "Homemaking"],
            "care_types": ["Companion Care", "Personal Care", "Respite Care", "Alzheimer's/Dementia"],
            "payment_options": ["Private Pay", "Long-Term Care Insurance", "VA Benefits"],
            "licensing": "TX-HCS-12345",
            "accreditation": ["BBB Accredited"],
            "languages": ["English", "Spanish"],
            "service_area": "Greater Houston Area, Harris County, Fort Bend County",
            "year_established": 1998,
            "rating": 4.8,
            "review_count": 156,
            "status": "Featured",
            "date_added": "2025-01-01",
            "latitude": 29.7604,
            "longitude": -95.3698,
        },
        {
            "name": "Home Instead Senior Care",
            "slug": "home-instead-austin",
            "description": "Home Instead provides personalized in-home care services to help seniors live safely and comfortably at home. We specialize in Alzheimer's and dementia care.",
            "address": "5678 Congress Ave",
            "city": "Austin",
            "state": "Texas",
            "state_slug": "texas",
            "city_slug": "austin",
            "zip": "78701",
            "county": "Travis County",
            "phone": "(512) 555-0200",
            "website_url": "https://www.homeinstead.com",
            "google_maps_url": "",
            "photo_url": "",
            "hours": "24/7 Care Available",
            "services": ["Alzheimer's & Dementia Care", "Personal Care", "Companion Care"],
            "care_types": ["Alzheimer's/Dementia", "Personal Care", "Live-In Care", "24-Hour Care"],
            "payment_options": ["Private Pay", "Long-Term Care Insurance"],
            "licensing": "TX-HCS-67890",
            "accreditation": ["Joint Commission", "BBB Accredited"],
            "languages": ["English", "Spanish", "Vietnamese"],
            "service_area": "Austin, Round Rock, Cedar Park, Georgetown",
            "year_established": 2001,
            "rating": 4.7,
            "review_count": 203,
            "status": "Featured",
            "date_added": "2025-01-02",
            "latitude": 30.2672,
            "longitude": -97.7431,
        },
        {
            "name": "Visiting Angels",
            "slug": "visiting-angels-chicago",
            "description": "Visiting Angels provides non-medical home care services including personal care, companion care, and respite care. Our caregivers are carefully screened and trained.",
            "address": "789 Michigan Ave",
            "city": "Chicago",
            "state": "Illinois",
            "state_slug": "illinois",
            "city_slug": "chicago",
            "zip": "60601",
            "county": "Cook County",
            "phone": "(312) 555-0300",
            "website_url": "https://www.visitingangels.com",
            "google_maps_url": "",
            "photo_url": "",
            "hours": "Mon-Sun: 8am-8pm",
            "services": ["Personal Care", "Companion Care", "Respite Care"],
            "care_types": ["Personal Care", "Companion Care", "Respite Care", "Post-Surgery"],
            "payment_options": ["Private Pay", "Medicaid", "Long-Term Care Insurance"],
            "licensing": "IL-HCS-11111",
            "accreditation": ["CHAP", "BBB Accredited"],
            "languages": ["English", "Spanish", "Polish"],
            "service_area": "Chicago, Evanston, Oak Park, Skokie",
            "year_established": 2005,
            "rating": 4.6,
            "review_count": 89,
            "status": "Active",
            "date_added": "2025-01-03",
            "latitude": 41.8781,
            "longitude": -87.6298,
        },
        {
            "name": "Right at Home",
            "slug": "right-at-home-dallas",
            "description": "Right at Home offers in-home care and assistance to seniors and adults with disabilities. We help with daily tasks so you can continue living independently.",
            "address": "321 Commerce St",
            "city": "Dallas",
            "state": "Texas",
            "state_slug": "texas",
            "city_slug": "dallas",
            "zip": "75201",
            "county": "Dallas County",
            "phone": "(214) 555-0400",
            "website_url": "https://www.rightathome.net",
            "google_maps_url": "",
            "photo_url": "",
            "hours": "24/7 Care Available",
            "services": ["Personal Care", "Homemaking", "Transportation"],
            "care_types": ["Personal Care", "Homemaking", "Veterans Care"],
            "payment_options": ["Private Pay", "VA Benefits", "Long-Term Care Insurance"],
            "licensing": "TX-HCS-22222",
            "accreditation": ["Medicare Certified"],
            "languages": ["English", "Spanish"],
            "service_area": "Dallas, Plano, Irving, Richardson",
            "year_established": 2008,
            "rating": 4.5,
            "review_count": 67,
            "status": "Active",
            "date_added": "2025-01-04",
            "latitude": 32.7767,
            "longitude": -96.7970,
        },
        {
            "name": "BrightStar Care",
            "slug": "brightstar-care-miami",
            "description": "BrightStar Care provides a full range of home care services from companionship to skilled nursing. Joint Commission accredited for quality assurance.",
            "address": "100 Biscayne Blvd",
            "city": "Miami",
            "state": "Florida",
            "state_slug": "florida",
            "city_slug": "miami",
            "zip": "33132",
            "county": "Miami-Dade County",
            "phone": "(305) 555-0500",
            "website_url": "https://www.brightstarcare.com",
            "google_maps_url": "",
            "photo_url": "",
            "hours": "24/7 Care Available",
            "services": ["Personal Care", "Live-In Care", "Hospice Support"],
            "care_types": ["Personal Care", "Live-In Care", "24-Hour Care", "Hospice Support"],
            "payment_options": ["Private Pay", "Medicare", "Medicaid", "Long-Term Care Insurance"],
            "licensing": "FL-HCS-33333",
            "accreditation": ["Joint Commission", "Medicare Certified"],
            "languages": ["English", "Spanish", "Creole"],
            "service_area": "Miami, Miami Beach, Coral Gables, Hialeah",
            "year_established": 2010,
            "rating": 4.9,
            "review_count": 245,
            "status": "Featured",
            "date_added": "2025-01-05",
            "latitude": 25.7617,
            "longitude": -80.1918,
        },
    ]


def _to_list(val):
    """Convert a value to a list — handles comma-separated strings from Airtable text fields."""
    if isinstance(val, list):
        return val
    if isinstance(val, str) and val.strip():
        return [s.strip() for s in val.split(",") if s.strip()]
    return []


def fetch_from_airtable():
    """Fetch agencies from Airtable API."""
    if not config.AIRTABLE_API_KEY or not config.AIRTABLE_BASE_ID:
        print("Airtable not configured. Using sample data.")
        return None

    try:
        from pyairtable import Api
        import time

        api = Api(config.AIRTABLE_API_KEY, timeout=(30, 60))
        table = api.table(config.AIRTABLE_BASE_ID, config.AIRTABLE_TABLE_NAME)

        # Fetch in pages to avoid gateway timeouts on Netlify
        records = []
        for page in table.iterate(page_size=100):
            records.extend(page)
            print(f"  Fetched {len(records)} records so far...")
            time.sleep(0.2)  # Brief pause to avoid rate limits

        agencies = []
        for record in records:
            fields = record.get("fields", {})

            # Skip drafts
            if fields.get("Status") == "Draft":
                continue

            state_name = fields.get("State", "")
            city_name = fields.get("City", "")
            agency = {
                "name": fields.get("Name", ""),
                "slug": fields.get("Slug") or slugify(fields.get("Name", "") + "-" + city_name),
                "description": fields.get("Description", ""),
                "address": fields.get("Address", ""),
                "city": city_name,
                "state": state_name,
                "state_slug": slugify(state_name),
                "city_slug": slugify(city_name),
                "zip": fields.get("Zip", ""),
                "county": fields.get("County", ""),
                "phone": fields.get("Phone", ""),
                "website_url": fields.get("Website URL", ""),
                "google_maps_url": fields.get("Google Maps URL", ""),
                "photo_url": fields.get("Photo URL", ""),
                "hours": fields.get("Hours", ""),
                "services": _to_list(fields.get("Services", [])),
                "care_types": _to_list(fields.get("Care Types", [])),
                "payment_options": _to_list(fields.get("Payment Options", [])),
                "licensing": fields.get("Licensing", ""),
                "accreditation": _to_list(fields.get("Accreditation", [])),
                "languages": _to_list(fields.get("Languages", [])),
                "service_area": fields.get("Service Area", ""),
                "year_established": fields.get("Year Established", ""),
                "rating": fields.get("Rating", 0),
                "review_count": fields.get("Review Count", 0),
                "status": fields.get("Status", "Active"),
                "date_added": fields.get("Date Added", ""),
                "latitude": fields.get("Latitude", ""),
                "longitude": fields.get("Longitude", ""),
            }
            agencies.append(agency)

        print(f"Fetched {len(agencies)} agencies from Airtable.")
        return agencies

    except Exception as e:
        print(f"Error fetching from Airtable: {e}")
        return None


def get_agencies():
    """Get agencies from Airtable or fall back to sample data."""
    agencies = fetch_from_airtable()
    if agencies is None:
        agencies = get_sample_data()
        print(f"Using {len(agencies)} sample agencies.")
    return agencies


def load_local_blog_posts():
    """Load blog posts from local markdown files in content/blogposts/."""
    blog_dir = config.BASE_DIR / "content" / "blogposts"
    if not blog_dir.exists():
        return []

    posts = []
    for md_file in sorted(blog_dir.glob("*.md")):
        text = md_file.read_text(encoding="utf-8")

        # Parse frontmatter between ``` markers
        meta = {}
        content = text
        if text.startswith("```"):
            parts = text.split("```", 2)
            if len(parts) >= 3:
                # Parse key: value pairs from frontmatter
                for line in parts[1].strip().split("\n"):
                    if ":" in line:
                        key, _, value = line.partition(":")
                        meta[key.strip().lower()] = value.strip()
                content = parts[2].strip()

        status = meta.get("status", "Published")
        if status != "Published":
            continue

        title = meta.get("title", md_file.stem)
        post = {
            "title": title,
            "slug": meta.get("slug", slugify(title)),
            "content": content,
            "excerpt": meta.get("excerpt", ""),
            "author": meta.get("author", "Senior Home Care Finder Staff"),
            "publish_date": meta.get("published date", meta.get("publish date", "")),
            "featured_image": meta.get("featured image", ""),
            "meta_description": meta.get("meta description", ""),
            "status": status,
            "featured": meta.get("featured", "").lower() == "true",
            "category": meta.get("category", ""),
        }
        posts.append(post)

    if posts:
        print(f"Loaded {len(posts)} blog posts from content/blogposts/.")
    return posts


def fetch_blog_posts():
    """Fetch published blog posts from Airtable, merged with local markdown files."""
    # Load local posts first
    local_posts = load_local_blog_posts()
    local_slugs = {p["slug"] for p in local_posts}

    # Then try Airtable
    airtable_posts = []
    if config.AIRTABLE_API_KEY and config.AIRTABLE_BASE_ID:
        try:
            from pyairtable import Api

            api = Api(config.AIRTABLE_API_KEY)
            table = api.table(config.AIRTABLE_BASE_ID, config.AIRTABLE_BLOG_TABLE_NAME)
            records = table.all()

            for record in records:
                fields = record.get("fields", {})

                if fields.get("Status") != "Published":
                    continue

                title = fields.get("Title", "")
                slug = (fields.get("Slug", "") or slugify(title)).strip()

                # Skip if local file already has this slug (local takes priority)
                if slug in local_slugs:
                    continue

                # Handle Featured Image — could be a URL string or Airtable attachment array
                featured_image = fields.get("Featured Image", "")
                if isinstance(featured_image, list) and featured_image:
                    featured_image = featured_image[0].get("url", "")

                post = {
                    "title": title,
                    "slug": slug,
                    "content": fields.get("Content", ""),
                    "excerpt": fields.get("Excerpt", ""),
                    "author": fields.get("Author", "Senior Home Care Finder Staff"),
                    "publish_date": fields.get("Publish Date", ""),
                    "featured_image": featured_image,
                    "meta_description": fields.get("Meta Description", ""),
                    "status": fields.get("Status", "Published"),
                    "featured": fields.get("Featured", False),
                    "category": fields.get("Category", ""),
                }
                airtable_posts.append(post)

            print(f"Fetched {len(airtable_posts)} blog posts from Airtable.")

        except Exception as e:
            print(f"Note: Could not fetch blog posts ({e})")

    all_posts = local_posts + airtable_posts
    all_posts.sort(key=lambda x: x.get("publish_date", ""), reverse=True)
    return all_posts


def setup_output_directory():
    """Create clean output directory."""
    if config.OUTPUT_DIR.exists():
        shutil.rmtree(config.OUTPUT_DIR)

    config.OUTPUT_DIR.mkdir(parents=True)
    (config.OUTPUT_DIR / "state").mkdir()
    (config.OUTPUT_DIR / "agency").mkdir()
    (config.OUTPUT_DIR / "services").mkdir()
    (config.OUTPUT_DIR / "blog").mkdir()

    # Copy static files
    if config.STATIC_DIR.exists():
        shutil.copytree(config.STATIC_DIR, config.OUTPUT_DIR / "static")


def create_jinja_env():
    """Create Jinja2 environment with custom filters."""
    env = Environment(
        loader=FileSystemLoader(config.TEMPLATES_DIR),
        autoescape=True
    )

    def format_date(date_str):
        if not date_str:
            return ""
        try:
            dt = datetime.strptime(str(date_str)[:10], "%Y-%m-%d")
            return dt.strftime("%B ") + str(dt.day) + dt.strftime(", %Y")
        except (ValueError, TypeError):
            return date_str

    def star_rating(rating):
        """Convert numeric rating to star display."""
        if not rating:
            return ""
        full_stars = int(rating)
        half_star = 1 if rating - full_stars >= 0.5 else 0
        empty_stars = 5 - full_stars - half_star
        return "★" * full_stars + "½" * half_star + "☆" * empty_stars

    env.filters["slugify"] = slugify
    env.filters["tojson"] = lambda v: json.dumps(v, ensure_ascii=False)
    env.filters["markdown"] = lambda text: Markup(md_lib.markdown(text or "", extensions=["extra", "nl2br"]))
    env.filters["format_date"] = format_date
    env.filters["star_rating"] = star_rating

    env.globals["site_name"] = config.SITE_NAME
    env.globals["site_url"] = config.SITE_URL
    env.globals["site_description"] = config.SITE_DESCRIPTION
    env.globals["services"] = config.SERVICES
    env.globals["us_states"] = config.US_STATES
    env.globals["current_year"] = datetime.now().year
    env.globals["ga_measurement_id"] = config.GA_MEASUREMENT_ID

    return env


def group_agencies_by_state(agencies):
    """Group agencies by state slug."""
    grouped = {}
    for agency in agencies:
        state_slug = agency.get("state_slug", "")
        if state_slug:
            grouped.setdefault(state_slug, []).append(agency)
    return grouped


def group_agencies_by_city(agencies):
    """Group agencies by state and city."""
    grouped = {}
    for agency in agencies:
        state_slug = agency.get("state_slug", "")
        city_slug = agency.get("city_slug", "")
        if state_slug and city_slug:
            key = (state_slug, city_slug, agency.get("city", ""), agency.get("state", ""))
            grouped.setdefault(key, []).append(agency)
    return grouped


def build_homepage(env, agencies, posts):
    """Build the homepage."""
    template = env.get_template("index.html")

    featured = [a for a in agencies if a.get("status") == "Featured"][:config.FEATURED_COUNT]
    if not featured:
        featured = agencies[:config.FEATURED_COUNT]

    recent = sorted(agencies, key=lambda x: x.get("date_added", ""), reverse=True)[:config.RECENT_COUNT]

    # Group by state for state browse section
    by_state = group_agencies_by_state(agencies)
    state_counts = {s: len(v) for s, v in by_state.items()}

    # Featured post for homepage
    featured_post = next((p for p in posts if p.get("featured")), None)
    recent_posts = [p for p in posts if p is not featured_post][:3]

    html = template.render(
        featured_agencies=featured,
        recent_agencies=recent,
        all_agencies=agencies,
        state_counts=state_counts,
        total_count=len(agencies),
        featured_post=featured_post,
        recent_posts=recent_posts,
        page_title=config.DEFAULT_META_TITLE,
        meta_description=config.DEFAULT_META_DESCRIPTION,
        request_path="/",
    )

    output_path = config.OUTPUT_DIR / "index.html"
    output_path.write_text(html)
    print(f"Built: index.html ({len(agencies)} total agencies)")


MIN_AGENCIES_FOR_INDEX = 3  # Noindex state/city pages below this threshold


def build_state_pages(env, agencies):
    """Build one page per US state."""
    template = env.get_template("state.html")
    grouped = group_agencies_by_state(agencies)

    indexed_states = []
    noindexed_states = []

    for state in config.US_STATES:
        state_agencies = grouped.get(state["slug"], [])
        state_agencies.sort(key=lambda x: x.get("city", ""))

        # Group by city for the state page
        cities = {}
        for agency in state_agencies:
            city = agency.get("city", "Unknown")
            city_slug = agency.get("city_slug", "unknown")
            cities.setdefault((city, city_slug), []).append(agency)

        noindex = len(state_agencies) < MIN_AGENCIES_FOR_INDEX

        if noindex:
            noindexed_states.append(state["name"])
        else:
            indexed_states.append(state["slug"])

        html = template.render(
            state=state,
            agencies=state_agencies,
            cities=cities,
            noindex=noindex,
            page_title=f"Home Care Agencies in {state['name']} - {config.SITE_NAME}",
            meta_description=f"Find {len(state_agencies)} trusted home care agencies in {state['name']}. Compare services, read reviews, and connect with local caregivers.",
            request_path=f"/state/{state['slug']}.html",
        )

        output_path = config.OUTPUT_DIR / "state" / f"{state['slug']}.html"
        output_path.write_text(html)
        print(f"Built: state/{state['slug']}.html ({len(state_agencies)} agencies{' [noindex]' if noindex else ''})")

    if noindexed_states:
        print(f"  Noindexed {len(noindexed_states)} state pages (< {MIN_AGENCIES_FOR_INDEX} agencies)")

    return indexed_states  # Return for sitemap filtering


def build_city_pages(env, agencies):
    """Build one page per city (within state folders)."""
    template = env.get_template("city.html")
    grouped = group_agencies_by_city(agencies)

    indexed_cities = []
    noindex_count = 0

    for (state_slug, city_slug, city_name, state_name), city_agencies in grouped.items():
        city_agencies.sort(key=lambda x: x.get("name", ""))

        # Create state subfolder if needed
        state_folder = config.OUTPUT_DIR / "state" / state_slug
        state_folder.mkdir(parents=True, exist_ok=True)

        # Find state info
        state_info = next((s for s in config.US_STATES if s["slug"] == state_slug), {"name": state_name, "slug": state_slug, "abbr": ""})

        noindex = len(city_agencies) < MIN_AGENCIES_FOR_INDEX

        if noindex:
            noindex_count += 1
        else:
            indexed_cities.append(f"{state_slug}/{city_slug}")

        html = template.render(
            city=city_name,
            city_slug=city_slug,
            state=state_info,
            agencies=city_agencies,
            noindex=noindex,
            page_title=f"Home Care Agencies in {city_name}, {state_info['abbr'] or state_name} - {config.SITE_NAME}",
            meta_description=f"Find {len(city_agencies)} home care agencies in {city_name}, {state_name}. Compare in-home care services, read reviews, and get help for your loved ones.",
            request_path=f"/state/{state_slug}/{city_slug}.html",
        )

        output_path = state_folder / f"{city_slug}.html"
        output_path.write_text(html)
        print(f"Built: state/{state_slug}/{city_slug}.html ({len(city_agencies)} agencies{' [noindex]' if noindex else ''})")

    if noindex_count:
        print(f"  Noindexed {noindex_count} city pages (< {MIN_AGENCIES_FOR_INDEX} agencies)")

    return indexed_cities  # Return for sitemap filtering


def build_agency_pages(env, agencies):
    """Build individual agency detail pages."""
    template = env.get_template("agency.html")

    for agency in agencies:
        # Related agencies: same city or same state
        related = [
            a for a in agencies
            if a["slug"] != agency["slug"] and (
                a.get("city_slug") == agency.get("city_slug") or
                a.get("state_slug") == agency.get("state_slug")
            )
        ][:4]

        # Find state info for breadcrumbs
        state_info = next(
            (s for s in config.US_STATES if s["slug"] == agency.get("state_slug")),
            {"name": agency.get("state", ""), "slug": agency.get("state_slug", ""), "abbr": ""}
        )

        html = template.render(
            agency=agency,
            state=state_info,
            related_agencies=related,
            page_title=f"{agency['name']} - {agency['city']}, {agency['state']} - {config.SITE_NAME}",
            meta_description=agency.get("description", "")[:160] or f"{agency['name']} provides in-home care services in {agency['city']}, {agency['state']}.",
            request_path=f"/agency/{agency['slug']}.html",
        )

        output_path = config.OUTPUT_DIR / "agency" / f"{agency['slug']}.html"
        output_path.write_text(html)
        print(f"Built: agency/{agency['slug']}.html")


def build_service_pages(env, agencies):
    """Build service category filter pages."""
    template = env.get_template("service.html")

    for service in config.SERVICES:
        # Filter agencies that offer this service
        service_agencies = [
            a for a in agencies
            if service["name"] in a.get("services", []) or service["name"] in a.get("care_types", [])
        ]

        # Build state list sorted by count desc for sidebar filter
        state_counts = {}
        for a in service_agencies:
            s = a.get("state", "")
            if s:
                state_counts[s] = state_counts.get(s, 0) + 1
        state_list = sorted(state_counts.items(), key=lambda x: (-x[1], x[0]))

        html = template.render(
            service=service,
            agencies=service_agencies,
            state_list=state_list,
            page_title=f"{service['name']} Services - {config.SITE_NAME}",
            meta_description=service["description"],
            request_path=f"/services/{service['slug']}.html",
        )

        output_path = config.OUTPUT_DIR / "services" / f"{service['slug']}.html"
        output_path.write_text(html)
        print(f"Built: services/{service['slug']}.html ({len(service_agencies)} agencies)")


def build_blog_page(env, posts):
    """Build the blog listing page."""
    template = env.get_template("blog.html")
    html = template.render(
        posts=posts,
        page_title=f"Blog - {config.SITE_NAME}",
        meta_description="Guides, tips, and resources to help you find the right home care for your loved ones.",
        request_path="/blog.html",
    )
    output_path = config.OUTPUT_DIR / "blog.html"
    output_path.write_text(html)
    print(f"Built: blog.html ({len(posts)} posts)")


def build_post_pages(env, posts):
    """Build individual blog post pages."""
    template = env.get_template("post.html")

    for post in posts:
        if not post.get("slug"):
            continue
        html = template.render(
            post=post,
            all_posts=posts,
            page_title=f"{post['title']} - {config.SITE_NAME}",
            meta_description=post.get("meta_description") or post.get("excerpt", "")[:160],
            request_path=f"/blog/{post['slug']}.html",
        )
        output_path = config.OUTPUT_DIR / "blog" / f"{post['slug']}.html"
        output_path.write_text(html)
        print(f"Built: blog/{post['slug']}.html")


def build_search_index(agencies):
    """Generate search-index.json for client-side search."""
    index = [
        {
            "name": a["name"],
            "city": a.get("city", ""),
            "state": a.get("state", ""),
            "slug": a["slug"],
            "services": a.get("services", []),
        }
        for a in agencies if a.get("name") and a.get("slug")
    ]
    output_path = config.OUTPUT_DIR / "search-index.json"
    with open(output_path, "w") as f:
        json.dump(index, f, ensure_ascii=False)
    print(f"Built: search-index.json ({len(index)} agencies)")


def build_sitemap(agencies, posts, indexed_states=None, indexed_cities=None):
    """Generate sitemap.xml — only includes indexable pages."""
    urls = [
        f"{config.SITE_URL}/",
        f"{config.SITE_URL}/blog.html",
        f"{config.SITE_URL}/about.html",
        f"{config.SITE_URL}/contact.html",
        f"{config.SITE_URL}/submit.html",
        f"{config.SITE_URL}/privacy.html",
        f"{config.SITE_URL}/terms.html",
    ]

    # State pages — only indexed ones
    if indexed_states:
        for state_slug in indexed_states:
            urls.append(f"{config.SITE_URL}/state/{state_slug}.html")
    else:
        for state in config.US_STATES:
            urls.append(f"{config.SITE_URL}/state/{state['slug']}.html")

    # City pages — only indexed ones
    if indexed_cities:
        for city_key in indexed_cities:
            urls.append(f"{config.SITE_URL}/state/{city_key}.html")
    else:
        cities_added = set()
        for agency in agencies:
            state_slug = agency.get("state_slug", "")
            city_slug = agency.get("city_slug", "")
            if state_slug and city_slug:
                city_key = f"{state_slug}/{city_slug}"
                if city_key not in cities_added:
                    urls.append(f"{config.SITE_URL}/state/{state_slug}/{city_slug}.html")
                    cities_added.add(city_key)

    # Service pages
    for service in config.SERVICES:
        urls.append(f"{config.SITE_URL}/services/{service['slug']}.html")

    # Agency pages
    for agency in agencies:
        urls.append(f"{config.SITE_URL}/agency/{agency['slug']}.html")

    # Blog posts
    for post in posts:
        if post.get("slug"):
            urls.append(f"{config.SITE_URL}/blog/{post['slug']}.html")

    sitemap = '<?xml version="1.0" encoding="UTF-8"?>\n'
    sitemap += '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    for url in urls:
        sitemap += f"  <url><loc>{url}</loc></url>\n"
    sitemap += "</urlset>"

    output_path = config.OUTPUT_DIR / "sitemap.xml"
    output_path.write_text(sitemap)
    print(f"Built: sitemap.xml ({len(urls)} URLs)")


def build_robots():
    """Generate robots.txt."""
    robots = f"""User-agent: *
Allow: /

Sitemap: {config.SITE_URL}/sitemap.xml
"""
    output_path = config.OUTPUT_DIR / "robots.txt"
    output_path.write_text(robots)
    print("Built: robots.txt")


def copy_ads_txt():
    """Copy ads.txt to output directory."""
    ads_txt_path = Path("ads.txt")
    if ads_txt_path.exists():
        shutil.copy(ads_txt_path, config.OUTPUT_DIR / "ads.txt")
        print("Built: ads.txt")


# Static pages
STATIC_PAGES = [
    {
        "template": "about.html",
        "output": "about.html",
        "title": "About Us",
        "description": "Learn about Senior Home Care Finder and our mission to help families find trusted in-home care.",
    },
    {
        "template": "privacy.html",
        "output": "privacy.html",
        "title": "Privacy Policy",
        "description": "Our privacy policy explains how we collect, use, and protect your information.",
    },
    {
        "template": "contact.html",
        "output": "contact.html",
        "title": "Contact Us",
        "description": "Get in touch with Senior Home Care Finder for questions or to update a listing.",
    },
    {
        "template": "terms.html",
        "output": "terms.html",
        "title": "Terms of Service",
        "description": "Terms and conditions for using Senior Home Care Finder.",
    },
    {
        "template": "success.html",
        "output": "success/index.html",
        "title": "Message Sent",
        "description": "Thank you for contacting us.",
    },
    {
        "template": "submit.html",
        "output": "submit.html",
        "title": "Submit an Agency",
        "description": "Submit a home care agency to be added to our directory.",
    },
]


def build_static_pages(env, agencies=None):
    """Build static informational pages."""
    total_count = len(agencies) if agencies else 0
    for page in STATIC_PAGES:
        template = env.get_template(page["template"])
        html = template.render(
            page_title=f"{page['title']} - {config.SITE_NAME}",
            meta_description=page["description"],
            request_path=f"/{page['output']}",
            total_count=total_count,
        )
        output_path = config.OUTPUT_DIR / page["output"]
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(html)
        print(f"Built: {page['output']}")


def main():
    """Main build process."""
    print(f"\n{'='*50}")
    print(f"Building {config.SITE_NAME}")
    print(f"{'='*50}\n")

    print("Setting up output directory...")
    setup_output_directory()

    print("\nFetching agencies...")
    agencies = get_agencies()

    print("\nFetching blog posts...")
    posts = fetch_blog_posts()

    env = create_jinja_env()

    print("\nBuilding pages...")
    build_homepage(env, agencies, posts)
    indexed_states = build_state_pages(env, agencies)
    indexed_cities = build_city_pages(env, agencies)
    build_agency_pages(env, agencies)
    build_service_pages(env, agencies)
    build_static_pages(env, agencies)
    build_blog_page(env, posts)
    build_post_pages(env, posts)

    print("\nBuilding SEO files...")
    build_sitemap(agencies, posts, indexed_states, indexed_cities)
    build_robots()
    copy_ads_txt()
    build_search_index(agencies)

    print(f"\n{'='*50}")
    print(f"Build complete! Output in: {config.OUTPUT_DIR}")
    print(f"{'='*50}")
    print(f"\nTo preview locally:")
    print(f"  cd {config.OUTPUT_DIR}")
    print(f"  python3 -m http.server 8000")
    print(f"  Open http://localhost:8000")


if __name__ == "__main__":
    main()
