"""
Configuration for Senior Home Care Finder Directory
"""
import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Base Paths
BASE_DIR = Path(__file__).parent
TEMPLATES_DIR = BASE_DIR / "templates"
STATIC_DIR = BASE_DIR / "static"
DATA_DIR = BASE_DIR / "data"
OUTPUT_DIR = BASE_DIR / "dist"

# Site Configuration
SITE_NAME = "Senior Home Care Finder"
SITE_DESCRIPTION = "Find trusted in-home care agencies for your aging loved ones. Compare services, read reviews, and connect with local caregivers."
SITE_URL = os.getenv("SITE_URL", "https://seniorhomecarefinder.com")
SITE_AUTHOR = "Senior Home Care Finder"

# Airtable Configuration
AIRTABLE_API_KEY = os.getenv("AIRTABLE_API_KEY")
AIRTABLE_BASE_ID = os.getenv("AIRTABLE_BASE_ID")
AIRTABLE_TABLE_NAME = os.getenv("AIRTABLE_TABLE_NAME", "Agencies")
AIRTABLE_BLOG_TABLE_NAME = os.getenv("AIRTABLE_BLOG_TABLE_NAME", "Blog Posts")

# US States + DC for state-based pages
US_STATES = [
    {"name": "Alabama", "slug": "alabama", "abbr": "AL"},
    {"name": "Alaska", "slug": "alaska", "abbr": "AK"},
    {"name": "Arizona", "slug": "arizona", "abbr": "AZ"},
    {"name": "Arkansas", "slug": "arkansas", "abbr": "AR"},
    {"name": "California", "slug": "california", "abbr": "CA"},
    {"name": "Colorado", "slug": "colorado", "abbr": "CO"},
    {"name": "Connecticut", "slug": "connecticut", "abbr": "CT"},
    {"name": "Delaware", "slug": "delaware", "abbr": "DE"},
    {"name": "District of Columbia", "slug": "district-of-columbia", "abbr": "DC"},
    {"name": "Florida", "slug": "florida", "abbr": "FL"},
    {"name": "Georgia", "slug": "georgia", "abbr": "GA"},
    {"name": "Hawaii", "slug": "hawaii", "abbr": "HI"},
    {"name": "Idaho", "slug": "idaho", "abbr": "ID"},
    {"name": "Illinois", "slug": "illinois", "abbr": "IL"},
    {"name": "Indiana", "slug": "indiana", "abbr": "IN"},
    {"name": "Iowa", "slug": "iowa", "abbr": "IA"},
    {"name": "Kansas", "slug": "kansas", "abbr": "KS"},
    {"name": "Kentucky", "slug": "kentucky", "abbr": "KY"},
    {"name": "Louisiana", "slug": "louisiana", "abbr": "LA"},
    {"name": "Maine", "slug": "maine", "abbr": "ME"},
    {"name": "Maryland", "slug": "maryland", "abbr": "MD"},
    {"name": "Massachusetts", "slug": "massachusetts", "abbr": "MA"},
    {"name": "Michigan", "slug": "michigan", "abbr": "MI"},
    {"name": "Minnesota", "slug": "minnesota", "abbr": "MN"},
    {"name": "Mississippi", "slug": "mississippi", "abbr": "MS"},
    {"name": "Missouri", "slug": "missouri", "abbr": "MO"},
    {"name": "Montana", "slug": "montana", "abbr": "MT"},
    {"name": "Nebraska", "slug": "nebraska", "abbr": "NE"},
    {"name": "Nevada", "slug": "nevada", "abbr": "NV"},
    {"name": "New Hampshire", "slug": "new-hampshire", "abbr": "NH"},
    {"name": "New Jersey", "slug": "new-jersey", "abbr": "NJ"},
    {"name": "New Mexico", "slug": "new-mexico", "abbr": "NM"},
    {"name": "New York", "slug": "new-york", "abbr": "NY"},
    {"name": "North Carolina", "slug": "north-carolina", "abbr": "NC"},
    {"name": "North Dakota", "slug": "north-dakota", "abbr": "ND"},
    {"name": "Ohio", "slug": "ohio", "abbr": "OH"},
    {"name": "Oklahoma", "slug": "oklahoma", "abbr": "OK"},
    {"name": "Oregon", "slug": "oregon", "abbr": "OR"},
    {"name": "Pennsylvania", "slug": "pennsylvania", "abbr": "PA"},
    {"name": "Rhode Island", "slug": "rhode-island", "abbr": "RI"},
    {"name": "South Carolina", "slug": "south-carolina", "abbr": "SC"},
    {"name": "South Dakota", "slug": "south-dakota", "abbr": "SD"},
    {"name": "Tennessee", "slug": "tennessee", "abbr": "TN"},
    {"name": "Texas", "slug": "texas", "abbr": "TX"},
    {"name": "Utah", "slug": "utah", "abbr": "UT"},
    {"name": "Vermont", "slug": "vermont", "abbr": "VT"},
    {"name": "Virginia", "slug": "virginia", "abbr": "VA"},
    {"name": "Washington", "slug": "washington", "abbr": "WA"},
    {"name": "West Virginia", "slug": "west-virginia", "abbr": "WV"},
    {"name": "Wisconsin", "slug": "wisconsin", "abbr": "WI"},
    {"name": "Wyoming", "slug": "wyoming", "abbr": "WY"},
]

# Service categories for filter pages
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

# Care types (for agency profiles)
CARE_TYPES = [
    "Companion Care",
    "Personal Care",
    "Homemaking",
    "Respite Care",
    "Live-In Care",
    "24-Hour Care",
    "Hospice Support",
    "Alzheimer's/Dementia",
    "Post-Surgery",
    "Veterans Care",
]

# Payment options
PAYMENT_OPTIONS = [
    "Private Pay",
    "Medicare",
    "Medicaid",
    "Long-Term Care Insurance",
    "VA Benefits",
]

# Accreditation options
ACCREDITATIONS = [
    "Medicare Certified",
    "Joint Commission",
    "CHAP",
    "BBB Accredited",
]

# Google Analytics
GA_MEASUREMENT_ID = os.getenv("GA_MEASUREMENT_ID", "")

# SEO Settings
DEFAULT_META_TITLE = f"{SITE_NAME} - Find In-Home Care Agencies Near You"
DEFAULT_META_DESCRIPTION = SITE_DESCRIPTION

# Build Settings
ITEMS_PER_PAGE = 24
FEATURED_COUNT = 6
RECENT_COUNT = 8
