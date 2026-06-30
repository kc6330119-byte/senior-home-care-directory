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

# Local data source (post-Airtable migration). When this CSV exists, build.py
# reads agencies from it instead of Airtable — see build.get_agencies().
AGENCIES_CSV = DATA_DIR / "agencies.csv"

# Committed export of the Airtable Blog Posts table. Used as a fallback in
# build.fetch_blog_posts() so the blog still builds if Airtable is removed.
BLOG_POSTS_CSV = DATA_DIR / "blog_posts.csv"

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
    {"name": "Alabama", "slug": "alabama", "abbr": "AL", "description": "Alabama's aging population is growing steadily, particularly in metro areas like Birmingham, Huntsville, and Mobile. The state's warm climate allows many seniors to remain active year-round, and families often seek in-home care to help loved ones age in place while staying connected to their communities. Alabama licenses home health agencies through the Department of Public Health."},
    {"name": "Alaska", "slug": "alaska", "abbr": "AK", "description": "Alaska presents unique challenges for senior care due to its vast geography and rural communities. Many families in Anchorage, Fairbanks, and the Mat-Su Valley rely on in-home caregivers to help seniors navigate long winters and limited access to medical facilities. The state's Medicaid waiver program supports home and community-based care for eligible residents."},
    {"name": "Arizona", "slug": "arizona", "abbr": "AZ", "description": "Arizona is a top retirement destination, with large senior populations in Phoenix, Tucson, Scottsdale, and Sun City. The dry desert climate appeals to many retirees but brings summer heat risks that make companion care and daily check-ins especially important. Arizona's ALTCS Medicaid program provides home care coverage for qualifying seniors."},
    {"name": "Arkansas", "slug": "arkansas", "abbr": "AR", "description": "Arkansas has a significant rural senior population that depends on in-home care to maintain independence. Little Rock, Fayetteville, and Fort Smith are hubs for home care agencies, but many providers also serve surrounding rural communities. The state's ARChoices Medicaid waiver helps eligible seniors receive personal care and homemaking services at home."},
    {"name": "California", "slug": "california", "abbr": "CA", "description": "California has the largest senior population of any U.S. state, with major care needs concentrated in Los Angeles, San Francisco, San Diego, and Sacramento. The state's diverse communities mean many agencies offer multilingual caregivers fluent in Spanish, Mandarin, Tagalog, Vietnamese, and Korean. California licenses home care organizations through the Department of Social Services and offers the In-Home Supportive Services (IHSS) Medicaid program for eligible residents."},
    {"name": "Colorado", "slug": "colorado", "abbr": "CO", "description": "Colorado's growing senior population is concentrated in the Front Range cities of Denver, Colorado Springs, and Fort Collins, though mountain communities face unique accessibility challenges. The state's high altitude and active lifestyle culture mean many seniors prioritize maintaining independence at home. Colorado's Health First Colorado Medicaid program includes home and community-based services waivers."},
    {"name": "Connecticut", "slug": "connecticut", "abbr": "CT", "description": "Connecticut has one of the highest percentages of residents over 65 in the Northeast. Cities like Hartford, New Haven, and Stamford have robust home care networks, and the state's Connecticut Home Care Program for Elders helps seniors who might otherwise need nursing home care remain at home with professional support."},
    {"name": "Delaware", "slug": "delaware", "abbr": "DE", "description": "Delaware's compact size means most home care agencies can serve the entire state, from Wilmington in the north to the beach communities of Sussex County. The state has a rapidly aging population and supports home care through its Diamond State Health Plan Medicaid waiver, helping seniors access personal care and companion services."},
    {"name": "District of Columbia", "slug": "district-of-columbia", "abbr": "DC", "description": "Washington, D.C. has a dense network of home care agencies serving its diverse senior population across all eight wards. The District's Elderly and Persons with Physical Disabilities Waiver provides Medicaid-funded home care for qualifying residents, and the city's extensive public transit system supports caregivers and clients alike."},
    {"name": "Florida", "slug": "florida", "abbr": "FL", "description": "Florida has the second-largest population of adults over 65 in the nation, making it one of the most active markets for in-home senior care. Major metro areas like Miami, Tampa, Orlando, and Jacksonville have hundreds of licensed agencies, and many providers offer bilingual caregivers in Spanish and Creole. Florida's Statewide Medicaid Managed Care Long-Term Care program helps eligible seniors receive home and community-based services as an alternative to nursing facilities."},
    {"name": "Georgia", "slug": "georgia", "abbr": "GA", "description": "Georgia's senior care landscape spans the Atlanta metro area, coastal Savannah, and many rural communities across the state. The state's aging population is growing faster than the national average, increasing demand for in-home personal care and companion services. Georgia's Community Care Services Program and SOURCE waiver provide Medicaid-funded home care options for eligible seniors."},
    {"name": "Hawaii", "slug": "hawaii", "abbr": "HI", "description": "Hawaii's island geography creates distinct home care markets on Oahu, Maui, the Big Island, and Kauai. The state has a strong multigenerational family culture, and many home care agencies offer caregivers who speak Hawaiian, Japanese, Filipino, and other Pacific Island languages. Hawaii's Medicaid waiver programs support home and community-based care for eligible seniors."},
    {"name": "Idaho", "slug": "idaho", "abbr": "ID", "description": "Idaho's senior population is growing rapidly, particularly in Boise, Meridian, and Idaho Falls. Rural communities across the state face home care access challenges, making agencies that serve wider geographic areas especially valuable. The state's Aged and Disabled Medicaid waiver helps qualifying seniors receive in-home personal care and homemaking assistance."},
    {"name": "Illinois", "slug": "illinois", "abbr": "IL", "description": "Illinois has a large and diverse senior population centered in Chicago and its suburbs, with significant needs in downstate communities like Springfield, Peoria, and Rockford. The state's Community Care Program is one of the most comprehensive Medicaid home care programs in the country, helping seniors maintain independence through homemaker, adult day, and emergency home response services."},
    {"name": "Indiana", "slug": "indiana", "abbr": "IN", "description": "Indiana's senior care needs span Indianapolis, Fort Wayne, South Bend, and many rural communities. The state's Aged and Disabled Medicaid waiver provides home and community-based services including personal care, homemaking, and respite care. Indiana families often seek agencies that offer flexible scheduling to supplement care provided by family members."},
    {"name": "Iowa", "slug": "iowa", "abbr": "IA", "description": "Iowa has one of the highest percentages of residents over 65 in the Midwest, with home care demand strongest in Des Moines, Cedar Rapids, and Davenport. The state's rural character means many seniors live far from medical facilities, making in-home care essential for aging in place. Iowa's Medicaid Home and Community-Based Services waiver supports eligible seniors with personal care and homemaking."},
    {"name": "Kansas", "slug": "kansas", "abbr": "KS", "description": "Kansas seniors benefit from a growing network of home care agencies in Wichita, Kansas City, Topeka, and Overland Park. The state's rural western counties face particular challenges with caregiver availability, making agencies that serve wide areas especially important. Kansas's HCBS Frail Elderly waiver provides Medicaid-funded home care services for qualifying residents."},
    {"name": "Kentucky", "slug": "kentucky", "abbr": "KY", "description": "Kentucky's senior population is growing, with home care needs concentrated in Louisville, Lexington, and the Northern Kentucky metro area, as well as Appalachian communities in eastern Kentucky. The state's Medicaid Home and Community-Based waiver programs help eligible seniors receive personal care, homemaking, and companion services as alternatives to institutional care."},
    {"name": "Louisiana", "slug": "louisiana", "abbr": "LA", "description": "Louisiana's senior care needs are concentrated in New Orleans, Baton Rouge, and Shreveport, though rural parishes also have significant aging populations. The state's warm, humid climate requires particular attention to senior safety during summer months and hurricane season. Louisiana's Community Choices Waiver provides Medicaid-funded home care for eligible seniors across the state."},
    {"name": "Maine", "slug": "maine", "abbr": "ME", "description": "Maine has the oldest median age of any U.S. state, making home care services critically important for communities from Portland to Bangor and throughout rural inland areas. Long winters and geographic isolation make in-home caregivers essential for many seniors aging in place. Maine's Medicaid programs include home and community-based waivers covering personal care and homemaking."},
    {"name": "Maryland", "slug": "maryland", "abbr": "MD", "description": "Maryland's senior population is concentrated in the Baltimore metro area, Montgomery and Prince George's counties near Washington D.C., and the Eastern Shore communities. The state's diverse communities are served by agencies offering multilingual caregivers. Maryland's Community First Choice program and other Medicaid waivers help eligible seniors receive home care services."},
    {"name": "Massachusetts", "slug": "massachusetts", "abbr": "MA", "description": "Massachusetts has a well-developed home care infrastructure, particularly in the Boston metro area, Worcester, and Springfield. The state's strong healthcare sector means many agencies employ caregivers with clinical training beyond basic requirements. MassHealth, the state's Medicaid program, offers extensive home and community-based service options for eligible seniors."},
    {"name": "Michigan", "slug": "michigan", "abbr": "MI", "description": "Michigan's senior care needs span the Detroit metro area, Grand Rapids, and communities across both peninsulas. The state's cold winters make in-home care especially important for seniors who face mobility and safety challenges during icy months. Michigan's MI Choice waiver provides Medicaid-funded home care services including personal care, homemaking, and respite care."},
    {"name": "Minnesota", "slug": "minnesota", "abbr": "MN", "description": "Minnesota is recognized for its high-quality senior care standards. Home care agencies in Minneapolis-St. Paul, Rochester, and Duluth serve a growing aging population that values independence. The state's Elderly Waiver and Alternative Care programs provide Medicaid and state-funded home care services for seniors who might otherwise require nursing facility care."},
    {"name": "Mississippi", "slug": "mississippi", "abbr": "MS", "description": "Mississippi's largely rural senior population faces significant home care access challenges outside of Jackson, Gulfport, and Hattiesburg. The state has a growing need for in-home caregivers as families seek alternatives to institutional care. Mississippi's Elderly and Disabled Medicaid waiver helps qualifying seniors receive personal care and homemaking services at home."},
    {"name": "Missouri", "slug": "missouri", "abbr": "MO", "description": "Missouri's home care needs are concentrated in St. Louis, Kansas City, and Springfield, with rural communities across the Ozarks and southern Missouri also seeking in-home support. The state licenses home health agencies through the Department of Health and Senior Services and offers Medicaid waiver programs covering personal care and homemaker services for eligible seniors."},
    {"name": "Montana", "slug": "montana", "abbr": "MT", "description": "Montana's vast distances between communities make in-home care essential for seniors in Billings, Missoula, Great Falls, and across rural areas. The state's aging ranching and farming communities particularly depend on caregivers who understand the challenges of rural living. Montana's Big Sky Waiver provides Medicaid-funded home and community-based services for eligible seniors."},
    {"name": "Nebraska", "slug": "nebraska", "abbr": "NE", "description": "Nebraska's senior population is served by home care agencies centered in Omaha, Lincoln, and Grand Island, with coverage extending to rural western communities. The state's Medicaid Aged and Disabled waiver supports in-home personal care and homemaking services for qualifying seniors, helping them avoid premature moves to nursing facilities."},
    {"name": "Nevada", "slug": "nevada", "abbr": "NV", "description": "Nevada's senior population is growing rapidly, driven by retirees in Las Vegas, Reno, and Henderson. The state's desert climate brings extreme summer heat that makes daily check-ins and companion care critical for senior safety. Nevada's Home and Community-Based waiver provides Medicaid-funded personal care and homemaking services for eligible seniors."},
    {"name": "New Hampshire", "slug": "new-hampshire", "abbr": "NH", "description": "New Hampshire has a growing senior population, particularly in the southern tier near Manchester and Nashua and in the Lakes Region. Long winters and rural geography make in-home care vital for seniors aging in place. The state's Choices for Independence waiver provides Medicaid-funded home care services including personal care, homemaking, and respite."},
    {"name": "New Jersey", "slug": "new-jersey", "abbr": "NJ", "description": "New Jersey's dense population and high cost of living make in-home care a preferred alternative to assisted living for many families across Newark, Jersey City, and the suburbs. The state's diverse communities are served by agencies offering caregivers fluent in Spanish, Portuguese, Hindi, and other languages. NJ FamilyCare Medicaid programs include home and community-based service options."},
    {"name": "New Mexico", "slug": "new-mexico", "abbr": "NM", "description": "New Mexico's senior population includes significant Hispanic and Native American communities with distinct cultural care preferences. Home care agencies in Albuquerque, Santa Fe, and Las Cruces often offer bilingual caregivers. The state's Mi Via and Centennial Care Medicaid waivers provide home and community-based services for eligible seniors across urban and rural areas."},
    {"name": "New York", "slug": "new-york", "abbr": "NY", "description": "New York has one of the largest senior populations in the country, with major care needs in New York City's five boroughs, Long Island, Westchester, and upstate cities like Buffalo, Rochester, and Albany. The state's diverse communities require agencies offering caregivers in dozens of languages. New York's Medicaid program is one of the most comprehensive in the nation, with managed long-term care plans coordinating home care services for eligible seniors."},
    {"name": "North Carolina", "slug": "north-carolina", "abbr": "NC", "description": "North Carolina's growing retirement communities in Charlotte, Raleigh-Durham, and Asheville drive strong demand for in-home senior care. The state's mix of urban and rural communities means agencies must serve diverse geographic areas. North Carolina's Community Alternatives Program for Disabled Adults (CAP/DA) provides Medicaid-funded home care for eligible seniors."},
    {"name": "North Dakota", "slug": "north-dakota", "abbr": "ND", "description": "North Dakota's harsh winters and rural landscape make in-home care essential for seniors in Fargo, Bismarck, and Grand Forks, as well as farming communities across the state. The state's Medicaid HCBS waiver programs support personal care, homemaking, and respite services for qualifying seniors aging in place."},
    {"name": "Ohio", "slug": "ohio", "abbr": "OH", "description": "Ohio has a substantial aging population spread across major metros including Columbus, Cleveland, Cincinnati, and Dayton. The state's PASSPORT Medicaid waiver is one of the longest-running home and community-based care programs in the country, helping eligible seniors receive personal care, homemaking, and other services as alternatives to nursing facility placement."},
    {"name": "Oklahoma", "slug": "oklahoma", "abbr": "OK", "description": "Oklahoma's senior care needs span Oklahoma City, Tulsa, and rural communities across the state. Many families seek home care agencies that understand the cultural diversity of Oklahoma's population, including significant Native American communities. The state's ADvantage Medicaid waiver provides home and community-based services for eligible seniors and adults with disabilities."},
    {"name": "Oregon", "slug": "oregon", "abbr": "OR", "description": "Oregon is known for its progressive approach to senior care, with strong home and community-based services available in Portland, Eugene, Salem, and across rural communities. The state's Medicaid K Plan provides personal care services for eligible seniors, and Oregon has been a national leader in shifting care from institutions to home settings."},
    {"name": "Pennsylvania", "slug": "pennsylvania", "abbr": "PA", "description": "Pennsylvania has one of the largest populations of adults over 65 in the nation, with major care needs in Philadelphia, Pittsburgh, and communities across the Lehigh Valley, Poconos, and central Pennsylvania. The state's aging infrastructure includes a strong network of Area Agencies on Aging that help connect families with home care providers. Pennsylvania's Community HealthChoices Medicaid managed care program coordinates home and community-based services for eligible seniors statewide."},
    {"name": "Rhode Island", "slug": "rhode-island", "abbr": "RI", "description": "Rhode Island's small size means most home care agencies can serve the entire state, from Providence to Newport and Warwick. The state has a high percentage of residents over 65 and supports home care through its Medicaid HCBS waivers, helping seniors receive personal care, homemaking, and companion services as alternatives to institutional care."},
    {"name": "South Carolina", "slug": "south-carolina", "abbr": "SC", "description": "South Carolina's growing retirement communities along the coast in Charleston, Myrtle Beach, and Hilton Head, combined with inland needs in Columbia and Greenville, drive strong demand for in-home senior care. The state's warm climate attracts retirees, and its Community Long-Term Care Medicaid waiver supports home-based services for eligible seniors."},
    {"name": "South Dakota", "slug": "south-dakota", "abbr": "SD", "description": "South Dakota's rural character and extreme winters make in-home care essential for seniors in Sioux Falls, Rapid City, and farming communities statewide. The state's HCBS waiver programs provide Medicaid-funded personal care, homemaking, and respite services for qualifying seniors who wish to remain in their homes rather than move to assisted living or nursing facilities."},
    {"name": "Tennessee", "slug": "tennessee", "abbr": "TN", "description": "Tennessee's senior population is growing across Nashville, Memphis, Knoxville, and Chattanooga. The state's CHOICES Medicaid managed long-term care program helps eligible seniors access home and community-based services including personal care, homemaking, and companion care. Many agencies serve both urban centers and surrounding rural areas."},
    {"name": "Texas", "slug": "texas", "abbr": "TX", "description": "Texas has one of the fastest-growing senior populations in the country, with major home care markets in Houston, Dallas-Fort Worth, San Antonio, and Austin. The state's diverse communities are served by agencies offering caregivers fluent in Spanish, Vietnamese, Chinese, and other languages. Texas's STAR+PLUS Medicaid managed care program coordinates home and community-based services for eligible seniors, and the state's large geographic footprint means many agencies specialize in specific metro areas or regions."},
    {"name": "Utah", "slug": "utah", "abbr": "UT", "description": "Utah's family-oriented culture means many seniors receive care from relatives, but professional home care agencies in Salt Lake City, Provo, and St. George fill critical gaps when family care isn't sufficient. The state's Aging Waiver provides Medicaid-funded home and community-based services for eligible seniors including personal care, homemaking, and respite care."},
    {"name": "Vermont", "slug": "vermont", "abbr": "VT", "description": "Vermont has the second-oldest median age in the nation, creating strong demand for home care in Burlington, Montpelier, and rural communities across the Green Mountains. The state's Choices for Care Medicaid waiver provides home and community-based services for eligible seniors, and Vermont's small-town character means caregivers often form close bonds with their clients."},
    {"name": "Virginia", "slug": "virginia", "abbr": "VA", "description": "Virginia's senior care needs span Northern Virginia's D.C. suburbs, the Hampton Roads metro area, Richmond, and rural communities in the Shenandoah Valley and southwestern Virginia. The state's large veteran population also drives demand for VA-eligible home care agencies. Virginia's Commonwealth Coordinated Care Plus Medicaid program covers home and community-based services for eligible seniors."},
    {"name": "Washington", "slug": "washington", "abbr": "WA", "description": "Washington state's senior population is concentrated in Seattle, Tacoma, Spokane, and the Puget Sound region, with growing retirement communities on the Olympic Peninsula and in central Washington. The state's COPES Medicaid waiver provides comprehensive home and community-based services for eligible seniors, and Washington has been a leader in promoting home care as an alternative to institutional placement."},
    {"name": "West Virginia", "slug": "west-virginia", "abbr": "WV", "description": "West Virginia's mountainous terrain and rural communities create particular challenges for senior care access. Home care agencies in Charleston, Huntington, and Morgantown serve seniors who often live far from medical facilities. The state's Aged and Disabled Medicaid waiver provides personal care and homemaking services for eligible seniors aging in place."},
    {"name": "Wisconsin", "slug": "wisconsin", "abbr": "WI", "description": "Wisconsin's senior care landscape includes major markets in Milwaukee, Madison, and Green Bay, along with many rural communities in the northern part of the state. Long winters make in-home care especially valuable for seniors who face mobility challenges during cold months. Wisconsin's Family Care and IRIS Medicaid programs provide home and community-based services for eligible seniors and adults with disabilities."},
    {"name": "Wyoming", "slug": "wyoming", "abbr": "WY", "description": "Wyoming's small population and vast distances between communities make in-home care essential for seniors in Cheyenne, Casper, and rural areas across the state. The state's Medicaid HCBS waiver programs support personal care and homemaking services for eligible seniors, and many agencies serve large geographic regions to meet the needs of isolated communities."},
]

# Service categories for filter pages
SERVICES = [
    {
        "name": "Companion Services",
        "slug": "companion-care",
        "description": "Companionship, conversation, and social engagement for seniors living at home",
        "icon": "🤝",
        "intro": "Companion care focuses on providing meaningful social interaction and emotional support for seniors who live alone or spend long periods without company. Caregivers engage in conversation, play games, accompany clients on walks or outings, and help prevent the isolation and depression that many older adults experience. This type of care is often the first step families take when a loved one begins showing signs of loneliness, withdrawal, or mild cognitive decline. Companion care does not typically include hands-on personal care like bathing or dressing, but many agencies offer companion and personal care together in a flexible care plan."
    },
    {
        "name": "Personal Care",
        "slug": "personal-care",
        "description": "Assistance with bathing, dressing, grooming, and daily personal hygiene",
        "icon": "🛁",
        "intro": "Personal care services help seniors with the activities of daily living (ADLs) that become difficult due to age, illness, or disability. This includes assistance with bathing, dressing, grooming, oral hygiene, toileting, and mobility support like transferring from bed to wheelchair. Caregivers are trained to provide this intimate assistance while preserving the client's dignity and independence. When considering personal care services, ask agencies about their caregiver training requirements, how they match caregivers to clients, and whether they can accommodate specific needs like catheter care or diabetes management."
    },
    {
        "name": "Homemaking",
        "slug": "homemaking",
        "description": "Light housekeeping, meal prep, laundry, and household management",
        "icon": "🏠",
        "intro": "Homemaking services help seniors maintain a clean, safe, and comfortable living environment when household tasks become physically challenging. Services typically include light housekeeping, vacuuming, dusting, laundry, meal planning and preparation, grocery shopping, and errand running. For many families, homemaking care is an affordable way to ensure a parent or grandparent is eating nutritious meals and living in a well-maintained home. These services can be scheduled for just a few hours per week or combined with personal care for more comprehensive support."
    },
    {
        "name": "Alzheimer's & Dementia Care",
        "slug": "alzheimers-dementia",
        "description": "Specialized care for seniors with Alzheimer's disease or other forms of dementia",
        "icon": "🧠",
        "intro": "Alzheimer's and dementia care requires specialized training that goes beyond standard home care. Caregivers who work with memory care clients learn to manage sundowning behaviors, redirect agitation, create structured daily routines, and maintain a safe home environment that reduces confusion and fall risk. As dementia progresses, care needs evolve from gentle reminders and supervision to full assistance with daily activities. When choosing a dementia care agency, ask about their caregiver certification programs, how they handle behavioral challenges, and whether they offer graduated care plans that adjust as the disease advances."
    },
    {
        "name": "Respite Care",
        "slug": "respite-care",
        "description": "Temporary relief for family caregivers — short-term professional coverage",
        "icon": "🔄",
        "intro": "Respite care provides temporary relief for family members who serve as primary caregivers. Whether you need coverage for a few hours to run errands, a weekend away, or an extended vacation, professional respite caregivers step in to maintain your loved one's routine and comfort. Caregiver burnout is a serious risk for the estimated 53 million Americans who provide unpaid care to family members, and regular respite breaks are essential for sustaining long-term caregiving. Many agencies offer flexible respite scheduling, and some costs may be covered by Medicaid waiver programs or VA benefits."
    },
    {
        "name": "Live-In Care",
        "slug": "live-in-care",
        "description": "Around-the-clock caregivers who live in the senior's home",
        "icon": "🏡",
        "intro": "Live-in care provides a dedicated caregiver who resides in the senior's home, offering continuous support throughout the day and being available overnight for emergencies. This arrangement works well for seniors who need frequent assistance but want to remain in their own home rather than move to an assisted living facility. Live-in caregivers typically work in shifts of several days on and off, alternating with a second caregiver. While more expensive than hourly care, live-in care is significantly less costly than most residential facilities and allows seniors to maintain their familiar surroundings, routines, and community connections."
    },
    {
        "name": "Post-Surgery Care",
        "slug": "post-surgery",
        "description": "Recovery assistance after hospital stays or surgical procedures",
        "icon": "🏥",
        "intro": "Post-surgery care helps seniors recover safely at home after hospital stays, surgical procedures, or acute illness. Caregivers assist with medication reminders, wound care monitoring, mobility support, meal preparation, and transportation to follow-up appointments. Hospital readmissions are a significant risk for older adults — nearly 20% of Medicare patients are readmitted within 30 days — and professional home care during recovery can help prevent complications. Post-surgery care is often short-term, lasting from a few days to several weeks, and can be covered by Medicare or private insurance depending on the circumstances."
    },
    {
        "name": "Veterans Care",
        "slug": "veterans-care",
        "description": "Home care services for veterans, including VA-eligible agencies",
        "icon": "🎖️",
        "intro": "Veterans care agencies specialize in serving former military members and their spouses, often working directly with the Department of Veterans Affairs to coordinate benefits and billing. The VA offers several programs that cover in-home care costs, including the Aid and Attendance pension benefit, the Homemaker/Home Health Aide program, and the Veteran Directed Care program. Many veterans are unaware they qualify for these benefits, which can significantly reduce or eliminate out-of-pocket costs for home care. When searching for a veterans care agency, look for providers experienced with VA enrollment and claims processing."
    },
    {
        "name": "Hospice Support",
        "slug": "hospice-support",
        "description": "Comfort care and end-of-life support for seniors and their families",
        "icon": "💜",
        "intro": "Hospice support services focus on comfort, dignity, and quality of life for seniors facing a terminal illness or end-of-life transition. Non-medical hospice caregivers provide companionship, personal care, light housekeeping, and emotional support that complements the clinical services provided by a hospice medical team. These caregivers also offer respite for family members during an emotionally and physically demanding time. Hospice support at home allows seniors to spend their final months surrounded by familiar people and places, and many families find that this personalized care provides peace and comfort for the entire family."
    },
    {
        "name": "Transportation",
        "slug": "transportation",
        "description": "Rides to medical appointments, errands, and social activities",
        "icon": "🚗",
        "intro": "Transportation services help seniors maintain their independence and social connections by providing reliable rides to medical appointments, pharmacy visits, grocery stores, religious services, and social activities. For many older adults, giving up driving is a major loss of autonomy, and professional transportation services fill that gap safely. Caregivers who provide transportation often assist clients from door to door, helping with getting in and out of vehicles and carrying packages. Some agencies offer transportation as a standalone service, while others include it as part of a broader companion or personal care plan."
    },
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

# AdSense pre-submission noindex policy
# -------------------------------------
# Listings whose NAME contains a residential / institutional venue type
# are not in-home care agencies and should not be indexed. Generated from
# the gitignored `validate_listings.py` after that script's HARD_FAIL list
# was tightened on 2026-05-09.
#
# Re-derive after any new Outscraper batch by name-matching the agencies
# table against the following set (lowercase, word-bounded substring match
# on the Name field):
#
#   senior living, senior community, retirement community, retirement village,
#   retirement home, assisted living, nursing home, skilled nursing facility,
#   rehabilitation center, rehabilitation hospital, rehab center, rehab
#   hospital, memory care, adult day care, adult day services, adult day
#   center, hospice center, hospice facility, hospice house, the bungalows,
#   the cottages, village at, manor at, the gardens at, estates at,
#   walmart home services (retail-store false positives), rescare
#   (residential disability services chain), community living (residential
#   disability services), treatment center, comprehensive treatment,
#   treatment facility (clinics / methadone), behavioral health center,
#   supported living
#
# Notably absent: "hospice home" (matches inside "Hospice Home Health"
# which is a legitimate home-health naming convention); bare "skilled
# nursing" / "adult day" (services some in-home agencies offer); bare
# "walmart" (matches Help-at-Home franchise locations whose name includes
# "Inside [city] Walmart" — those are legitimate home-care agencies, the
# full "walmart home services" phrase is what we want to exclude).
#
# These pages still build (so direct URLs continue to work) but receive
# `<meta name="robots" content="noindex, follow">`, are dropped from the
# sitemap, and are excluded from state / city / service / related-agency
# listings.
AGENCY_NOINDEX_SLUGS = {
    # The list below is the union of (a) all slugs flagged by
    # validate_listings.py LIKELY NOT HOME CARE classification, and (b) one-off
    # additions surfaced by the F3 description-regen review (off-topic listings
    # whose names don't match a global hard-fail pattern: HVAC, lawn care,
    # insurance, security, car dealership, etc.). Re-derive whenever the
    # Airtable data changes meaningfully — script + chain-name list documented
    # in the comment block above.
    "a-step-ahead-learning-center-north-bergen-nj",
    "adorable-senior-living-hillsborough-nc",
    "america-s-top-assisted-living-resources-llc-mesa-az",
    "angelic-care-adult-family-home-sammamish-wa",
    "appleton-community-living-llc-appleton-wi",
    "arh-beckley-homecare-store-beckley-wv",
    "assisted-living-home-care-services-cheshire-ct",
    "assisted-living-home-care-services-westport-ct",
    "avanti-senior-living-at-lafayette-youngsville-la",
    "azura-memory-care-of-oak-creek-oak-creek-wi",
    "baycare-assisted-living-pocomoke-salisbury-pocomoke-city-md",
    "beckley-comprehensive-treatment-center-beaver-wv",
    "bozeman-health-hillcrest-senior-living-birchwood-bozeman-mt",
    "brightstar-senior-living-madison-wi",
    "cardinal-senior-living-at-danville-danville-va",
    "carepartners-adult-day-center-st-albans-city-vt",
    "charter-senior-living-of-fredericksburg-falmouth-va",
    "charter-senior-living-of-hazel-crest-hazel-crest-il",
    "choptank-residential-assisted-living-denton-md",
    "christopher-heights-of-attleboro-attleboro-ma",
    "cmf-security-solutions-beloit-ks",
    "cook-willow-health-center-plymouth-ct",
    "country-place-senior-living-of-fairhope-fairhope-al",
    "country-view-assisted-living-oak-creek-wi",
    "cozy-corner-adult-day-services-dubuque-ia",
    "cuba-manor-inc-cuba-mo",
    "ecumenical-retirement-community-harrisburg-pa",
    "farm-bureau-financial-services-beloit-ks",
    "effingham-healthcare-senior-living-effingham-il",
    "elm-york-assisted-living-east-elmhurst-ny",
    "fair-haven-motors-inc-fair-haven-vt",
    "glowcares-llc-senior-care-services-assisted-living-residential-assisted-living-respite-stays-mechanicsville-va",
    "grande-premium-meats-del-norte-co",
    "guardian-angels-engel-haus-senior-living-albertville-albertville-mn",
    "hamilton-trace-family-first-senior-living-fishers-in",
    "haven-assisted-living-mechanicsville-va",
    "heartland-mechical-heating-cooling-inc-valier-mt",
    "heritage-senior-living-soda-springs-soda-springs-id",
    "heron-pointe-senior-living-monmouth-or",
    "highgate-senior-living-bozeman-bozeman-mt",
    "homestead-assisted-living-of-hiawatha-hiawatha-ks",
    "homestead-senior-living-st-albans-city-vt",
    "insideout-home-inspections-llc-canterbury-nh",
    "jivan-adult-day-health-center-cape-verdean-adult-day-health-center-attleborough-falls-ma",
    "kg-care-homes-assisted-living-laveen-village-az",
    "lakeview-supported-living-services-madison-wi",
    "lantern-crest-senior-living-santee-ca",
    "lewis-insurance-associates-fredericksburg-va",
    "life-pittsburgh-allegheny-center-day-health-center-pittsburgh-pa",
    "lilac-homes-enhanced-assisted-living-memory-care-dilworth-mn",
    "logan-health-assisted-living-shelby-shelby-mt",
    "lucas-adult-family-home-a-sammamish-adult-family-home-sammamish-wa",
    "majestic-care-of-toledo-assisted-living-toledo-oh",
    "manchin-assisted-living-llc-bridgeport-wv",
    "medical-mall-arh-homecare-store-hazard-ky",
    "midway-homes-adult-care-st-paul-mn",
    "miranda-landscape-co-lebanon-me",
    "mountaineer-rv-outdoor-center-llc-jane-lew-wv",
    "mva-health-center-shinnston-shinnston-wv",
    "naturalawn-of-america-north-attleborough-ma",
    "neighborworks-of-western-vermont-west-rutland-vt",
    "newbern-drug-newbern-tn",
    "north-central-insurance-weston-wv",
    "northwest-colorado-health-community-health-center-steamboat-springs-co",
    "oak-park-place-dubuque-dubuque-ia",
    "oak-park-place-oak-creek-oak-creek-wi",
    "park-house-southfield-senior-living-southfield-mi",
    "partnerships-in-community-living-inc-monmouth-or",
    "premier-gentle-care-afh-sammamish-wa",
    "productivity-vermont-bristol-vt",
    "rescare-aiken-sc",
    "rescare-community-living-canton-oh",
    "rescare-community-living-fort-wayne-in",
    "rescare-community-living-kansas-city-ks",
    "rescare-community-living-moraine-oh",
    "rescare-community-living-new-albany-in",
    "rescare-community-living-parkersburg-wv",
    "rescare-family-youth-services-clarksburg-bridgeport-wv",
    "rivercrest-senior-living-new-albany-in",
    "ron-wilson-center-for-effective-living-inc-monmouth-or",
    "rose-senior-living-clinton-township-clinton-township-mi",
    "sammamish-senior-living-afh-sammamish-wa",
    "senior-community-care-of-kentucky-pace-louisville-ky",
    "steelville-senior-living-steelville-mo",
    "stonehill-health-center-dubuque-ia",
    "summer-village-senior-living-auburn-al",
    "sun-vista-care-sammamish-adult-family-home-sammamish-wa",
    "sunrise-of-newton-newton-ma",
    "terrabella-hillsborough-hillsborough-nc",
    "the-brennity-at-fairhope-senior-living-fairhope-al",
    "the-bungalows-at-mayfield-mayfield-ky",
    "the-cortland-howell-howell-mi",
    "the-heritage-assisted-living-adult-day-care-llc-las-cruces-nm",
    "tim-osterbur-country-financial-agent-st-joseph-il",
    "traceway-retirement-community-tupelo-ms",
    "trulieve-weston-dispensary-weston-wv",
    "twin-towers-senior-living-community-cincinnati-oh",
    "tyler-insurance-services-creston-ia",
    "united-refrigeration-inc-clarksburg-wv",
    "unity-homecare-agency-assisted-living-home-care-cecil-county-elkton-md-elkton-md",
    "vibrant-life-senior-living-durand-durand-mi",
    "vibrant-life-senior-living-temperance-temperance-mi",
    "walmart-home-services-alexandria-la",
    "walmart-home-services-auburn-al",
    "walmart-home-services-bemidji-mn",
    "walmart-home-services-bristow-ok",
    "walmart-home-services-cary-nc",
    "walmart-home-services-chicago-il",
    "walmart-home-services-clinton-nc",
    "walmart-home-services-clinton-township-mi",
    "walmart-home-services-creston-ia",
    "walmart-home-services-cuba-mo",
    "walmart-home-services-danville-va",
    "walmart-home-services-dilworth-mn",
    "walmart-home-services-dubuque-ia",
    "walmart-home-services-dyersburg-tn",
    "walmart-home-services-effingham-il",
    "walmart-home-services-fairfield-ia",
    "walmart-home-services-fredericksburg-va",
    "walmart-home-services-grundy-va",
    "walmart-home-services-guthrie-ok",
    "walmart-home-services-hiawatha-ks",
    "walmart-home-services-hillsborough-nc",
    "walmart-home-services-kansas-city-ks",
    "walmart-home-services-kendallville-in",
    "walmart-home-services-killeen-tx",
    "walmart-home-services-kokomo-in",
    "walmart-home-services-leesville-la",
    "walmart-home-services-leland-nc",
    "walmart-home-services-lexington-tn",
    "walmart-home-services-locust-grove-va",
    "walmart-home-services-lowville-ny",
    "walmart-home-services-mattoon-il",
    "walmart-home-services-mayfield-ky",
    "walmart-home-services-mechanicsville-va",
    "walmart-home-services-mesa-az",
    "walmart-home-services-moraine-oh",
    "walmart-home-services-neosho-mo",
    "walmart-home-services-new-roads-la",
    "walmart-home-services-ottawa-ks",
    "walmart-home-services-owensville-mo",
    "walmart-home-services-pineville-la",
    "walmart-home-services-pocomoke-city-md",
    "walmart-home-services-port-allen-la",
    "walmart-home-services-raymore-mo",
    "walmart-home-services-ridgeland-ms",
    "walmart-home-services-roanoke-va",
    "walmart-home-services-rochester-nh",
    "walmart-home-services-santee-ca",
    "walmart-home-services-seminole-tx",
    "walmart-home-services-shelbyville-tn",
    "walmart-home-services-sioux-falls-sd",
    "walmart-home-services-snyder-tx",
    "walmart-home-services-st-albans-city-vt",
    "walmart-home-services-steamboat-springs-co",
    "walmart-home-services-sweetwater-tx",
    "walmart-home-services-taylorville-il",
    "walmart-home-services-tilton-nh",
    "walmart-home-services-tompkinsville-ky",
    "walmart-home-services-tupelo-ms",
    "walmart-home-services-union-city-tn",
    "walmart-home-services-urbana-il",
    "walmart-home-services-wauseon-oh",
    "walmart-home-services-weston-wv",
    "waterford-estates-independent-living-supportive-living-memory-care-hazel-crest-il",
    "wegman-care-center-at-st-ann-s-community-rochester-ny",
    "west-cecil-health-center-wchc-conowingo-conowingo-md",
    "yama-services-adult-assisted-living-mechanicsville-va",
}

# How many city pages stay indexed. The top N cities by agency count keep
# `index, follow` and (in a forthcoming editorial sprint) get hand-written
# 400-600 word editorial. The remaining cities get `noindex, follow` and
# drop from the sitemap. Per AdSense pre-submission Q3.
TOP_INDEXED_CITY_COUNT = 25
