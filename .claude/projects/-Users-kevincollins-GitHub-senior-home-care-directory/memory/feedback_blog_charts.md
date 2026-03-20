---
name: Blog post charts
description: Use Chart.js charts in blog posts where data visualization adds value
type: feedback
---

Add Chart.js charts to blog posts when they contain comparative data, costs, or statistics that benefit from visual presentation.

**Implementation pattern (from holisticvetdirectory.com):**
- Embed `<canvas data-chart='{ ...Chart.js config JSON... }'></canvas>` in the markdown content
- Chart.js loads from CDN: `https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js`
- JS in the template finds all `canvas[data-chart]` elements, parses the JSON config, and initializes charts
- Data is hardcoded in the canvas attribute — no external API needed

**Good candidates for charts:**
- Cost comparisons by region/state
- Benefit amount comparisons (VA, Medicare, Medicaid)
- Survey/statistic visualizations (caregiver burnout rates, etc.)
- Service type popularity/availability

**Why:** Charts add unique visual content that Google values, improve user engagement, and differentiate the site from template-only directories.
**How to apply:** When writing blog posts with comparative data, include Chart.js canvas elements. May need to add chart initialization JS to post.html template.
