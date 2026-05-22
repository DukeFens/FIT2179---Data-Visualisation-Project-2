# FIT2179 Data Visualisation 2 — Revised Project Plan
## "The Shuttlecock Effect: A Data-Driven Analysis of Badminton in Australia"

**Deadline:** Friday 29 May 2026, 11:55 PM  
**Tool:** Vega-Lite (MANDATORY — not Plotly or D3)  
**Deliverable:** Single scrollable GitHub Pages web page  
**Minimum:** 10 visualisations, at least 1 geographic map, substantial variety of idioms

---

## ⚠️ CRITICAL CHANGES FROM ORIGINAL PLAN

| Issue | Original Plan | Revised Plan |
|-------|--------------|--------------|
| Technology | Python + Plotly/D3 | **Vega-Lite only** (as required) |
| Chart 1 | Radar Chart | **Dot Plot / Heatmap** (Radar needs workaround in Vega-Lite) |
| Chart 8 | Sankey Diagram | **Isotype/Grid Chart** (Sankey NOT in Vega-Lite) |
| Historical data | 2016–2026 AusPlay | **Split: 2023–2025 (new AusPlay) + BA Annual Reports** |

---

## DIAGRAM PLAN — 10 CONFIRMED VISUALISATIONS

### PART 1: THE HUMAN BODY (Health & Science)

---

### Chart 1: "Smash Power — Which Muscles Fire the Most?"
- **Idiom:** Horizontal Bar Chart (with colour gradient by activation level)
- **Vega-Lite marks:** `bar` + colour encoding by value + text labels
- **Data file:** `data/muscle_activation_smash.csv`
- **Data source:** Frontiers in Sports, 2025 — "Muscle synergy analysis during badminton forehand overhead smash" (PMC12170632). EMG %MVIC values for 15 muscles.
- **Variables shown:** Muscle name (Y), % MVIC activation (X), body region (colour)
- **Why this idiom:** Clean, readable for a general audience. Sorted bar chart makes it immediately clear which muscles are most activated. Grouped by body region adds context.
- **Interactivity:** Tooltip showing exact muscle activation %, body region, movement phase
- **Data status:** ✅ CSV created (`data/muscle_activation_smash.csv`)
- **Note:** Values extracted from Table 1 of the 2025 PMC study. Cite: Frontiers in Sports and Active Living, doi: 10.3389/fspor.2025.1596670

---

### Chart 2: "Play Badminton, Live Longer"
- **Idiom:** Lollipop Chart (Cleveland dot plot variant)
- **Vega-Lite marks:** `layer` with `rule` (the stem) + `point` (the dot) + text annotation
- **Data file:** `data/longevity_sports.csv`
- **Data source:** Copenhagen City Heart Study (Schnohr et al., 2018, Mayo Clinic Proceedings). Followed 8,577 participants over 25 years.
- **Variables shown:** Sport name (Y axis), Years of life added vs sedentary (X axis), Sport category (colour)
- **Why this idiom:** Lollipop reduces visual clutter vs standard bar. The standout position of tennis/badminton tells the story instantly.
- **Interactivity:** Hover tooltip showing exact years gained + mortality reduction %
- **Data status:** ✅ CSV created (`data/longevity_sports.csv`)
- **Key insight:** Badminton adds 6.2 years vs running's 3.2 years — a story worth telling!

---

### Chart 3: "Badminton vs. Your Day — Calorie Comparison"
- **Idiom:** Grouped/Stacked Bar Chart
- **Vega-Lite marks:** `bar` with `stack` and `color` encoding
- **Data file:** `data/calorie_burn_activities.csv`
- **Data source:** Compendium of Physical Activities (Ainsworth et al., 2011). METs are a standardised, publicly available measure.
- **Variables shown:** Activity (X), Calories/hour for 70kg person (Y), Intensity category (colour)
- **Why this idiom:** Side-by-side comparison of total calories and the Social vs Competitive split for badminton makes the point viscerally clear.
- **Interactivity:** Hover for exact calorie counts, toggle between body weights (60/70/80 kg)
- **Data status:** ✅ CSV created (`data/calorie_burn_activities.csv`)

---

### PART 2: BADMINTON ACROSS AUSTRALIA (Macro Landscape)

---

### Chart 4: "Where Does Australia Play?" (MANDATORY MAP)
- **Idiom:** Choropleth Map (Australia, State level)
- **Vega-Lite marks:** `geoshape` + colour encoding by participation rate
- **Data file:** `data/australia_badminton_participation_by_state.csv` + Australian states TopoJSON
- **Data sources:**
  1. **AusPlay 2025** (Australian Sports Commission, 30 April 2026 release). Download: [National Data Tables](https://ascwrstorageprod001.ausport.gov.au/assets/i-4rhlW5CGAKD9UEzlZAGA.xlsx) and [By Sport Data Tables](https://ascwrstorageprod001.ausport.gov.au/assets/SgW4532FOd0g6i29E4jJWg.xlsx)
  2. **Badminton Australia Annual Report 2023/24**
- **TopoJSON:** Use `https://cdn.jsdelivr.net/npm/vega-datasets@2/data/au-states.topojson` or `world-110m.json` filtered to Australia
- **Variables shown:** State (geoshape), participation rate % (colour gradient — lighter = lower)
- **Why this idiom:** The most intuitive way to show geographic variation. Viewers immediately see Victoria as the badminton hub.
- **Interactivity:** Click/hover to show state name, participation rate, total players, number of registered clubs
- **Data status:** ✅ CSV created (preliminary numbers); **Confirm exact rates from AusPlay Excel files once downloaded**
- **⚠️ ACTION REQUIRED:** Download the AusPlay "By Sport Data Tables" xlsx and find badminton participation by state to get official numbers

---

### Chart 5: "A Sport on the Rise"
- **Idiom:** Stacked Area Chart
- **Vega-Lite marks:** `area` with `stack` = `true`, multiple series (Male/Female)
- **Data file:** `data/badminton_participation_trend.csv`
- **Data sources:**
  1. **AusPlay 2024 & 2025** (Jan-Dec 2024: ~237K male, ~170.5K female; Jan-Dec 2025: ~245K male, ~178K female)
  2. **AusPlay 2015-2023 archive** (old methodology — shown as a separate panel with a dotted break to indicate methodology change)
  3. **Badminton Australia Annual Reports 2019-2024** (www.badminton.org.au/policies-reports/)
- **⚠️ IMPORTANT NOTE:** AusPlay changed from phone to online methodology in July 2023. The time series has a break. Clearly annotate this break on the chart with a vertical dashed line and label.
- **Why this idiom:** Shows accumulated volume and the male/female gap over time. The COVID dip (2020-21) adds interesting storytelling.
- **Interactivity:** Hover to show year-specific Male/Female split
- **Data status:** ✅ CSV created (preliminary — confirm with actual AusPlay downloads)

---

### Chart 6: "Gen Z Is Taking Over the Courts"
- **Idiom:** Population Pyramid (Diverging Bar Chart)
- **Vega-Lite marks:** `bar` — male bars extend LEFT (negative values), female bars RIGHT (positive values)
- **Data file:** `data/badminton_participation_by_age_gender.csv`
- **Data sources:**
  1. **AusPlay 2025 "By Sport" Data Tables** (has age + gender breakdown for badminton)
  2. **AusPlay Badminton Power BI Report**: https://app.powerbi.com/view?r=eyJrIjoiNmEyMjEyOWItMGE4MS00NWVhLTk2MzItMTA2OWY4N2UyYWIwIiwidCI6IjhkMmUwZjRjLTU1ZjItNGNiMS04ZWU3LWRhNWRkM2ZmMzYwMCJ9
- **Variables shown:** Age group (Y), Male participants (left bars), Female participants (right bars)
- **Why this idiom:** Instantly shows the "bulge" at 18-24 (university age), proving the Gen Z/student claim.
- **Interactivity:** Hover shows exact participant counts and % of total for each age/gender group
- **Data status:** ✅ CSV created (preliminary); **confirm from AusPlay By Sport Excel once downloaded**

---

### Chart 7: "Find Your Court in Melbourne"
- **Idiom:** Point Map (Proportional Symbol Map)
- **Vega-Lite marks:** `point` mark overlaid on a Melbourne suburb base map
- **Data file:** `data/melbourne_badminton_venues.csv`
- **Data sources:**
  1. **OpenStreetMap** (overpass-turbo.eu — query: `node[sport=badminton](around:50000,-37.8136,144.9631)`)
  2. **Badminton Victoria club directory** (badmintonvic.org.au)
- **Variables shown:** Venue location (lat/lon → position), Number of courts (point size), Venue type (colour)
- **Special feature:** Highlight university-adjacent venues (Monash Clayton, Monash Caulfield, RMIT, UniMelb) with a different symbol/colour
- **Why this idiom:** Instantly shows concentration around inner suburbs and near campuses. Actionable info for students!
- **Interactivity:** Click a dot to see venue name, courts, type, and whether near a university
- **Base map:** Use `https://cdn.jsdelivr.net/npm/vega-datasets@2/data/world-110m.json` or OpenStreetMap tile layer via `image` mark
- **Data status:** ✅ CSV created (16 venues manually compiled from known Melbourne venues)

---

### PART 3: ELITE PERFORMANCE

---

### Chart 8: "From School Yard to the World Stage — The Talent Funnel"
- **Idiom:** Custom Isotype / Grid Rectangle Chart (creative, HD-worthy)
- **Vega-Lite marks:** `rect` marks arranged in a funnel-like grid + text annotations
- **Alternative:** Layered bar chart with explicit counts and percentage labels
- **Data file:** `data/talent_pipeline.csv`
- **Data sources:**
  1. **Badminton Australia Annual Report 2023/24** — 40,952 Sporting Schools participants, 327 sessions
  2. **Badminton Australia website** — Junior Falcons (10 players at World Juniors 2023), Senior Falcons (~20 active)
  3. **BWF event entry lists** for Australian players
- **Why replace Sankey:** Sankey diagrams are NOT natively in Vega-Lite (require d3-sankey plugin, which needs tutor approval). This isotype grid approach is more creative, achievable in Vega-Lite, and more readable for a general audience.
- **What it shows:** Grassroots (40,952) → Club (~18,000) → State (~1,200) → Junior Falcons (45) → Senior Falcons (20)
- **Interactivity:** Hover each level to see details, attrition rate, what programs exist at each level
- **Data status:** ✅ CSV created

---

### Chart 9: "Climbing the World Rankings — Australia's Top Players"
- **Idiom:** Multi-line Chart (with ranked Y-axis, inverted — lower rank = higher on screen)
- **Vega-Lite marks:** `line` + `point` marks, multiple series per player
- **Data file:** `data/australian_players_bwf_rankings.csv`
- **Data sources:**
  1. **BWF Historical Rankings** (corporate.bwfbadminton.com/players/historical-rankings/ — provides Excel downloads per year)
  2. **Kaggle: BWF World Rankings dataset** (kaggle.com/datasets/kabhishm/badminton-world-federation-bwf-rankings)
  3. **GitHub: raywan/bwf-data** (github.com/raywan/bwf-data — CSV format, scraped from BWF)
- **Players tracked:** Tiffany Ho (WS), Setyana Mapasa (WD), Angela Yu (WD), Gronya Sommerville (XD), Ken Choo (XD)
- **Time period:** 2022–2025 (6-monthly snapshots)
- **Why this idiom:** Multiple lines allow trajectory comparison. Inverted Y-axis (rank 1 at top) is natural and intuitive.
- **Interactivity:** Hover to see exact ranking and tournament points at each data point. Click a line to highlight that player.
- **Data status:** ✅ CSV created (preliminary); **⚠️ ACTION REQUIRED:** Download official BWF rankings Excel to verify/replace with exact ranking numbers
- **BWF Download:** https://corporate.bwfbadminton.com/players/historical-rankings/

---

### Chart 10: "Australia's Badminton Tournaments — Prestige vs Prize"
- **Idiom:** Bubble Chart (scatter plot with sized points)
- **Vega-Lite marks:** `point` with size channel, shape or colour channel for tournament category
- **Data file:** `data/bwf_tournaments_australia.csv`
- **Data sources:**
  1. **BWF World Tour official results** (bwfbadminton.com/tournament-results/)
  2. **Kaggle: Badminton BWF World Tour** (kaggle.com/datasets/sanderp/badminton-bwf-world-tour)
  3. **Wikipedia: Australian Badminton Open articles** (for historical prize money)
- **Variables shown:** Prize Money USD (X axis), BWF Points for winner (Y axis), Total entries (bubble size), Tournament grade (colour)
- **Why this idiom:** Three variables simultaneously — shows how Australia's Open sits in the global tournament landscape.
- **Interactivity:** Hover bubble to see tournament name, year, grade, prize money, entries
- **Data status:** ✅ CSV created

---

## DATA SOURCES SUMMARY

| Chart | Primary Source | Secondary Source | Status |
|-------|---------------|-----------------|--------|
| 1. Muscle Activation | PMC12170632 (Frontiers Sports, 2025) | — | ✅ CSV ready |
| 2. Longevity | Copenhagen City Heart Study (Mayo Clinic Proc, 2018) | British J Sports Med | ✅ CSV ready |
| 3. Calories | Ainsworth Compendium of Physical Activities (2011) | — | ✅ CSV ready |
| 4. Choropleth Map | AusPlay 2025 (ASC) | Badminton Australia Annual Report 2024 | ⚠️ Need xlsx download |
| 5. Area Chart | AusPlay 2024–2025 | AusPlay 2015-2023 archive | ⚠️ Need xlsx download |
| 6. Population Pyramid | AusPlay 2025 By Sport | AusPlay Power BI Badminton report | ⚠️ Need xlsx download |
| 7. Melbourne Map | OpenStreetMap / Overpass API | Badminton Victoria directory | ✅ CSV ready (verify) |
| 8. Talent Funnel | Badminton Australia Annual Report 2024 | BWF junior results | ✅ CSV ready |
| 9. Rankings (Multi-line) | BWF Historical Rankings | Kaggle BWF Rankings | ⚠️ Need BWF xlsx |
| 10. Bubble Chart | BWF World Tour results | Kaggle BWF World Tour dataset | ✅ CSV ready |

---

## ⚠️ ACTIONS YOU NEED TO TAKE TO GET REAL DATA

### Priority 1 — AusPlay Excel Downloads (MOST IMPORTANT)
These links are time-limited SAS tokens (expire 13 May 2026 19:26 UTC) — **download immediately!**

1. **National Data Tables (2025):**
   `https://ascwrstorageprod001.ausport.gov.au/assets/i-4rhlW5CGAKD9UEzlZAGA.xlsx`
   → Find "Badminton" rows → extract participation by state, age, gender

2. **By Sport Data Tables (2025):**
   `https://ascwrstorageprod001.ausport.gov.au/assets/SgW4532FOd0g6i29E4jJWg.xlsx`
   → This has dedicated sport-by-sport breakdown including Badminton

3. **VIC Data Tables (2025):**
   `https://ascwrstorageprod001.ausport.gov.au/assets/LX5zMNc31kIZKdo6XJnEkQ.xlsx`

4. **Badminton Power BI Report (interactive):**
   https://app.powerbi.com/view?r=eyJrIjoiNmEyMjEyOWItMGE4MS00NWVhLTk2MzItMTA2OWY4N2UyYWIwIiwidCI6IjhkMmUwZjRjLTU1ZjItNGNiMS04ZWU3LWRhNWRkM2ZmMzYwMCJ9

### Priority 2 — BWF Rankings
5. Download from: https://corporate.bwfbadminton.com/players/historical-rankings/
   → Select each year (2022, 2023, 2024, 2025) → Download Excel → Filter for AUS players

### Priority 3 — Melbourne Venues (Verify)
6. Run the Overpass API query at https://overpass-turbo.eu/:
   ```
   [out:json];
   (
     node[sport=badminton](around:50000,-37.8136,144.9631);
     way[sport=badminton](around:50000,-37.8136,144.9631);
   );
   out body;
   ```
   Export as GeoJSON/CSV → update `melbourne_badminton_venues.csv`

### Priority 4 — Kaggle Datasets (for Charts 9 & 10)
7. kaggle.com/datasets/kabhishm/badminton-world-federation-bwf-rankings (free download)
8. kaggle.com/datasets/sanderp/badminton-bwf-world-tour (for tournament prize money data)

---

## TECHNICAL IMPLEMENTATION NOTES

### Technology Stack
- **Charts:** Vega-Lite v5 (embed via CDN: `https://cdn.jsdelivr.net/npm/vega-lite@5`)
- **Web page:** HTML + CSS (Pure.css or custom)
- **Data files:** CSV/JSON (hosted in same GitHub repo, kept under a few MB)
- **Maps:** TopoJSON for Australia states + OpenStreetMap for Melbourne venues

### Vega-Lite Feasibility by Chart Type
| Idiom | Vega-Lite Support | Notes |
|-------|------------------|-------|
| Bar / Horizontal Bar | ✅ Native | Chart 1, 3 |
| Lollipop (rule + point layer) | ✅ Native | Chart 2 |
| Stacked Area | ✅ Native | Chart 5 |
| Diverging Bar (Population Pyramid) | ✅ Native | Chart 6 |
| Choropleth Map (geoshape) | ✅ Native | Chart 4 |
| Point Map | ✅ Native | Chart 7 |
| Multi-line Chart | ✅ Native | Chart 9 |
| Bubble Chart (scatter + size) | ✅ Native | Chart 10 |
| Isotype/Grid Chart | ✅ With `rect` marks | Chart 8 |
| **Sankey** | ❌ NOT native | Replaced with Chart 8 |
| **Radar/Spider** | ❌ NOT native | Replaced with Chart 1 |

### GitHub Pages Structure
```
/index.html          ← Single scrollable page
/css/style.css       ← Styling
/data/               ← All CSV/JSON data files
/vega-lite/          ← All Vega-Lite JSON spec files (one per chart)
/images/             ← Any images used
/sketch.pdf          ← Required paper sketch
```

### Interactivity Features (Vega-Lite)
- Tooltips on all charts: `"tooltip": true` or custom tooltip specs
- Selection highlighting: `"selection"` for click-to-highlight
- Zoom/pan on maps: `"zoom": true`
- Linked views: Use shared `selection` across related charts (e.g., state selection on map highlighting bar chart)

### Colour Palette
Consistent palette across all charts:
- Primary: `#1E5F74` (deep teal — badminton court colour)
- Accent: `#FFB830` (gold — Australian sporting gold)
- Female: `#E8A0BF` (pink-rose)
- Male: `#7EB8D4` (light blue)
- Neutral: `#F5F5F0` (background)

---

## STORY STRUCTURE (Narrative Flow)

**Hero statement:** "Badminton is quietly becoming Australia's most accessible, health-boosting, and fastest-growing indoor sport."

**Part 1 — The Science** (Charts 1-3)
> Hook: "Why does your body love badminton? The data says everything."
- Show muscles activated (Chart 1) → It's a full-body workout
- Show life expectancy gains (Chart 2) → Science backs the longevity benefit
- Show calorie comparison (Chart 3) → More effective than most workouts

**Part 2 — The Nation** (Charts 4-7)
> Transition: "Half a million Australians already know this. Here's where they play."
- National map (Chart 4) → Victoria leads, NSW follows
- Growth over time (Chart 5) → Steady rise, Gen Z fuelling it
- Age demographics (Chart 6) → University students are the core
- Melbourne venues (Chart 7) → Courts near every campus

**Part 3 — The Elite** (Charts 8-10)
> Escalation: "From school yards to the world stage — Australia's badminton ecosystem."
- Talent pipeline (Chart 8) → How Australians reach the top
- World rankings (Chart 9) → Australia's rising international stars
- Tournament ecosystem (Chart 10) → Australia hosts world-class events

**Closing statement:** "Whether you're at Monash, RMIT, or Melbourne Uni — a court is waiting. The data proves it's worth your time."

---

## MARKING CRITERIA ALIGNMENT

| Criterion | How We Meet It |
|-----------|---------------|
| At least 1 map | Chart 4 (Choropleth) + Chart 7 (Point Map) = 2 maps |
| 10+ visualisations | 10 confirmed charts (diverse idioms) |
| Substantial idiom variety | Bar, Lollipop, Stacked Area, Diverging Bar, Choropleth, Point Map, Multi-line, Bubble, Grid/Isotype = 9 different idioms |
| Real-world data from 2 sources | AusPlay (ASC) + BWF + Badminton Australia + Academic papers |
| Data from 2 different sources (required) | AusPlay + Badminton Australia Annual Reports (minimum) |
| Custom/creative visualisation (for HD) | Chart 8 (Isotype grid) + Chart 2 (annotated lollipop) |
| Interactivity | Tooltips on all charts, selection on map + bar charts |
| Storytelling | 3-part narrative with concise text panels |
| Vega-Lite only | All 10 charts implementable in Vega-Lite |
| GitHub Pages | Single URL, all JSON specs in repo |
| Audience (Australians) | All data is Australia-focused, jargon-free language |

---

*Plan last updated: 16 May 2026*  
*Author: Duke Phan — FIT2179 Data Visualisation 2, Monash University*
