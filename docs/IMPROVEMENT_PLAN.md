# The Shuttlecock Effect — Improvement Plan (v2)

**Purpose of this file:** a self-contained brief that another AI (or you) can execute to lift the project from "competent / C–D" to "creative custom-built / HD". Keep the topic (Australian badminton). **Move from 3 sections to 4** (The Body / The Nation / The City / The Competitive Edge) — see §2a. Do **not** rebuild from scratch — re-section, upgrade specific figures, and add coordinated interaction.

Live project: https://dukefens.github.io/FIT2179---Data-Visualisation-Project-2/
Reference exemplar studied: https://deatharder.github.io/afl-viz/

---

## 1. Diagnosis — why it currently reads as "simple"

Three concrete, fixable problems:

1. **Shallow data.** 14 hand-curated CSVs, most 8–31 rows. The AFL exemplar derives ~13 views from one granular match-level dataset (~130 seasons). Depth comes from *one rich source feeding many derived views*, not from many tiny tables. The rubric also explicitly rewards **derived data** for HD.
2. **Almost no interaction.** Only one interactive element exists (the year dropdown on the demographic heatmap). The AFL piece uses a coordinated dashboard (one selection cross-filters 3 sub-views), legend-driven focus, and hover-to-foreground. The rubric requires "an appropriate level of interactive exploration."
3. **Safe idioms only.** Current set = 2 lollipops, 1 body-map, 1 choropleth, 1 area-band line, 1 heatmap, 1 log-bar "funnel", 1 multiline, 1 bubble, 1 scatter-with-trendline. None of the advanced idioms from the unit (network / flow / tree / advanced map) appear. The "Melbourne LGAs" view is a scatter *pretending* to be geography — a wasted map opportunity.

The body-map (Fig 3, `image` + `geoshape`) is the one genuinely custom element — keep and build on that instinct.

---

## 2. Hard constraints the executor MUST respect (from the rubric PDF)

- **Vega-Lite only is marked.** Other libraries (D3, etc.) require prior tutor approval. → Default path for every "impossible-in-VL" idiom is **precompute geometry/layout in Python, emit a small derived CSV/GeoJSON, render with VL primitives** (`rect`, `rule`, `line`, `point`, `arc`, `geoshape`). This is allowed and is explicitly HD-rewarded as "derived data".
- **Minimum 10 visualisations, ≥1 geographic map** with an appropriate projection.
- **Combine data from ≥2 different sources** (already satisfied; keep satisfying per figure).
- **Most recent data available.** Use 2024/2025 releases where they exist.
- **Total downloadable data < a few MB.** Simplify GeoJSON (mapshaper/topojson, ~0.5% on metro boundaries); pre-aggregate; don't ship raw census.
- **Presentation, not exploration.** Interactivity must be tasteful — one coordinated/linked feature per part, not an expert dashboard. Do **not** over-build.
- **Single scrollable page, no horizontal scroll on a small laptop, no section-swapping buttons** (show/hide toggles are fine).
- **Audience = average Australian.** No statistics jargon; introduce any term (e.g. "%MVIC", "Super 500") inline.
- **Plagiarism rule:** idioms must be genuinely custom-built — not someone else's chart with new data.

---

## 2a. Section structure — go from 3 to 4 sections (HD requirement)

The HD band of the **Sketch** criterion reads: *"Four or more clear sections. Headings, text, figures, with detailed, creative and varied charts and maps."* The current project has only **3 parts**, which caps that criterion below HD. The page and the sketch must both show **≥4 clear sections.**

**Cleanest split (no filler needed):** the current Part 2 is overloaded — it carries both national/state geography *and* the Melbourne material (currently stranded as "08 The City" inside Part 3). Separate them:

| New | Section | Scope | Hosts (figures) |
|-----|---------|-------|-----------------|
| Part 1 | **The Body** | Physiology of the sport | Longevity, calories, muscle body-map, kinetic-chain network |
| Part 2 | **The Nation** | Australia-wide geography & demography | State choropleth, **area cartogram**, gender trend, demographic heatmap |
| Part 3 | **The City** *(new section)* | Melbourne — diaspora & courts | **Proportional-symbol map**, **dot-density / hexbin court map**, diaspora–courts correlation |
| Part 4 | **The Competitive Edge** | Elite pathway & results | **Sankey pipeline**, **bump chart**, **adjacency matrix**, tournaments [+ optional network/flow] |

This concentrates the three map idioms in Parts 2–3 (where they earn the most) and gives a clean four-act narrative arc: *one body → one nation → one city → one elite tier.* It also lets the sketch show four visually distinct, map-and-diagram-varied sections.

---

## 3. Strategy — three levers borrowed from the AFL exemplar

1. **Re-source 2–3 figures onto richer, real datasets** so views are *derived*, not typed by hand (Section 4).
2. **Add coordinated interaction** — one linked-highlight or cross-filter per part (Section 6).
3. **Replace 4–5 safe idioms with custom-built advanced idioms** from your list, each justified by the narrative (Sections 5–6). Annotate every one (shaded periods, reference lines, dynasty-style borders) the way AFL does.

---

## 4. Data collected — status as of 2026-05-30

All core datasets collected and saved to `data/`. Sources verified; estimated rows flagged with `estimated=true`.

| # | File | Rows | Status | Source | Feeds |
|---|------|------|--------|--------|-------|
| D1 | `bwf_rankings_deep.csv` | 87 | ✅ Done | BWF/Wikipedia player pages | Bump chart, ranking lines |
| D2 | `australian_open_results.csv` | 15 | ✅ Done | Wikipedia Australian Open results | Tournament bubble, flow map |
| D3 | `ausplay_state_by_year.csv` | 72 | ✅ Done | AusPlay reports (state splits estimated) | Cartogram, choropleth, heatmap |
| D4 | `abs_lga_asian_born_2021.csv` | 17 | ✅ Done | ABS 2021 Census QuickStats (live-fetched) | Proportional-symbol map, correlation |
| D5 | `badminton_victoria_clubs.csv` | 40 | ✅ Done | badmintonvic.com.au clubs page | Proportional-symbol map, hexbin |
| D6 | `melbourne_lga_boundaries.geojson` | 154 KB | ✅ Done | ABS ASGS2021 REST API (geo.abs.gov.au) | All Melbourne maps |
| D7 | `bwf_player_profiles.csv` | 8 | ✅ Done | Wikipedia player infoboxes | Player journey panel, bump chart |

**D7 notes — what is and isn't available publicly for Australian players:**
- ✅ **Height** — confirmed for Mapasa (1.66m), Somerville (1.71m), A.Yu (1.74m), Serasinghe (1.78m), T.Ho (1.55m)
- ✅ **Weight** — confirmed for Mapasa (60kg), Somerville (62kg), Serasinghe (79kg)
- ✅ **Handedness** — confirmed for above 5 players (Mapasa & Serasinghe: Left; others: Right)
- ✅ **Date of birth / birth country** — confirmed for 5 players
- ❌ **Strength, flexibility, speed, agility** — NO public dataset exists for Australian players. These are internal BWF/coaching metrics not published anywhere (checked: BWF profiles, all Kaggle badminton datasets, GitHub repos, academic papers)
- Simon Leung, Wendy Chen, Jack Yu — no Wikipedia pages; profile data unavailable

**Suggested new figure using D1 + D7 — Player Journey Panel:**
An interactive player-selector panel combining:
- Player avatar (initials + colour), bio, height/weight/handedness stat cards
- **Combined line chart**: solid line = confirmed BWF ranking by year; dashed line = estimated years
- Discipline tabs (WD / XD / MD / MS) per player
- Y-axis inverted (rank 1 = top), annotated with career peaks
- This lives in **Part 4 — The Competitive Edge**, alongside the bump chart

Every figure must visibly combine ≥2 of these (e.g. D4 census + D5 courts on one map).

---

## 5. Which complex idioms fit badminton — feasibility map

Legend: **VL** = native Vega-Lite · **VL+PC** = Vega-Lite rendering of Python-precomputed geometry (allowed, HD-rewarded) · **Approval** = genuinely needs D3/Vega + tutor sign-off · **Skip** = no honest narrative fit.

| Idiom | Fit for badminton? | Build path | Where it goes |
|-------|--------------------|-----------|---------------|
| **Sankey** | Yes — the talent pipeline IS a flow with drop-off | VL+PC (precompute node rects + ribbon bands) | Part 3 (replaces funnel) |
| **Alluvial** | Yes — participant flow across age cohorts over years | VL+PC (parallel-sets style) | Part 2 (pairs with heatmap) |
| **Node-Link** | Yes — (a) smash kinetic chain, (b) doubles partnerships | VL+PC (networkx coords → point + rule) | Part 1 **and/or** Part 3 |
| **Adjacency Matrix** | Yes — head-to-head between top players/countries | **VL native** (rect heatmap) | Part 3 |
| **Chord** | Yes — nationalities meeting at the Australian Open | Approval (smooth ribbons) — or VL+PC arc approximation | Part 3 (stretch) |
| **Treemap** | Yes — player base State→LGA→club, or prize-money by grade | VL+PC (squarify → rect + text) | Part 2 or 3 |
| **Dendrogram** | Maybe — cluster states by participation profile | VL+PC (scipy linkage → rule + point) | Part 2 (optional) |
| **Choropleth** | Already have — keep & refine scale | VL native | Part 2 |
| **Proportional Symbol Map** | Yes — Melbourne venues by court count | VL native (geoshape + sized circle) | Part 2 (replaces the fake scatter) |
| **Dot Density Map** | Yes — diaspora population / players as dots | VL native (many points on geoshape) | Part 2 |
| **Bin / Hexbin Map** | Yes — court density across metro Melbourne | square-bin VL native; true hexbin VL+PC | Part 2 (optional 2nd map) |
| **Flow Map** | Yes — international entries flowing into the Australian Open | VL+PC (curved arc paths, width = volume) | Part 3 (stretch) |
| **Area Cartogram** | **Strong** — "VIC = 20% population, 40% of players" anomaly | VL+PC (cartogram geometry → geoshape) | Part 2 (headline idiom) |
| **Isolines / Contour** | Weak — court-density surface is data-thin | VL+PC (scipy contours) | Skip unless time |
| **Colour mapping** | Already used — refine sequential/diverging choices | VL native | Throughout |
| **Shaded relief / Hillshade** | No terrain story | — | Skip |
| **Vector field / Streamlines** | No directional-field story | — | Skip |

**Two clear winners to prioritise:** the **Area Cartogram** (Part 2 headline — makes the central thesis visually undeniable) and the **Sankey** (Part 3 — the funnel literally is one). Both are custom-built + derived = squarely HD.

---

## 6. Figure-by-figure plan (old → new)

### PART ONE — THE BODY
- **Fig 1 Longevity (lollipop)** — keep; add annotation layer (highlight racket-sports bar, reference line for sedentary baseline). Low effort, raises storytelling score.
- **Fig 2 Calories (lollipop)** — keep; merge visually with Fig 1 as a small-multiple pair for layout symmetry.
- **Fig 3 Muscle body-map (image+geoshape)** — keep as the anchor. **Add small-multiples by swing phase** (you already have a `phase` column: Jump / Smash / Landing) so activation *shifts* are visible — this is "combining idioms" on derived data.
- **NEW — Smash kinetic-chain Node-Link.** Nodes = ~15 muscle groups (size = %MVIC from existing EMG CSV), edges = the calf→finger activation sequence. ~15 nodes → layout can be hand-placed in the CSV, no force solver needed. *Interaction:* hovering a muscle on the body-map highlights the same node in the network (linked highlight). This is the Part-1 advanced idiom + the Part-1 interaction in one move.

### PART TWO — THE NATION (Australia-wide geography & demography)
- **Fig 4 State choropleth** — keep projection; refine to a sequential scale; **overlay proportional-symbol circles** (size = total participants) → combined idioms on one map.
- **NEW — Area Cartogram (headline).** Resize each state by participant count, placed beside the geographic choropleth, so "Victoria 20% pop / 40% players" is undeniable. Precompute cartogram polygons in Python, render with `geoshape`. This is the project's signature innovative idiom.
- **Fig 5 Gender area-band line** — keep; strong already. Add the methodology-revision annotation more prominently.
- **Fig 6 Demographic heatmap (has year dropdown)** — keep the dropdown; consider an **Alluvial** companion showing the 18–24 cohort surge as flow across years.

### PART THREE — THE CITY (new section — Melbourne geography)
- **Rebuild "The City" (currently a scatter, old Fig 8) → real Melbourne proportional-symbol map.** Plot LGAs/venues on an actual Greater-Melbourne basemap: circle size = courts, colour = Asian-born % (D4 census + D5 courts). This is the map that anchors the new section.
- **NEW — second city map idiom:** a **dot-density map** (1 dot per N players, showing diaspora concentration) **or** a **square-bin/hexbin court-density map** across metro Melbourne. Two maps in one section justifies it as a standalone act.
- Keep the diaspora–courts **correlation** as a supporting annotated chart (the insight from the old scatter), now clearly framed as analysis *of* the map, not a fake-geography substitute for it.

### PART FOUR — THE COMPETITIVE EDGE (networks & flows)
- **Fig 7 Talent pipeline (log bar) → Sankey.** Grassroots 40k → Club → State → National → International (<20), widths = counts, drop-off = `next_level_pct`. Precompute node rects + ribbon bands in Python, render as `rect` + band marks. Highest-value single upgrade.
- **Fig 9 Rankings (multiline) → Bump chart** (AFL-ladder style) using D1 weekly history, annotating the 2-year top-30 run into Paris 2024. Add hover-to-foreground on a player path (legend/selection highlight). Optionally keep one raw multiline for the actual points.
- **NEW — Head-to-head Adjacency Matrix** (VL-native rect) between top AUS players / rival nations from D2. Cheap, native, adds idiom variety.
- **NEW (pick one) — Doubles-partnership Node-Link** (who partners whom among elite AUS pairs) *or* **Chord of nationalities** at the Australian Open. Node-link is the safer VL+PC build; chord is the stretch/approval option.
- **Fig 10 Tournament bubble** — keep; or upgrade to a **flow map** of international entries into Sydney/Melbourne (D2 entry lists) if time allows. Strengthen the Super 500 upgrade annotation.

---

## 7. Coordinated interaction (one per section — tasteful, not a dashboard)

- **Part 1 (Body):** hover muscle on body-map ↔ highlight node in kinetic-chain network.
- **Part 2 (Nation):** a single state selection that highlights the same region across the choropleth and the cartogram (Vega-Lite `params` + `condition`).
- **Part 3 (City):** hover an LGA to highlight it across the proportional-symbol map and the dot-density/hexbin map.
- **Part 4 (Edge):** hover/click a player to foreground their bump-chart path and adjacency-matrix row.

Implement with Vega-Lite `params` (point/interval selections) and `condition` encodings — no external JS needed. Keep it to highlighting/filtering existing views; do not build free-form exploration tools (rubric: presentation, not exploration).

---

## 8. Recommended final lineup (~13 figures across 4 sections, all VL-renderable)

**Part 1 — The Body**
1. Longevity lollipop (annotated)
2. Calorie lollipop (small-multiple pair with #1)
3. Muscle body-map + per-phase small-multiples
4. **Kinetic-chain node-link** (linked to #3)

**Part 2 — The Nation**
5. State choropleth + proportional-symbol overlay
6. **Area cartogram** (participants) — *headline idiom*
7. Gender area-band line
8. Demographic heatmap (year dropdown) [+ optional alluvial]

**Part 3 — The City**
9. **Melbourne proportional-symbol map** (census × courts) — *the geographic-map requirement*
10. **Dot-density or hexbin court map** (2nd map idiom)
11. Diaspora–courts correlation (annotated supporting chart)

**Part 4 — The Competitive Edge**
12. **Talent-pipeline Sankey**
13. **Rankings bump chart** (+ hover foreground)
14. **Head-to-head adjacency matrix** [+ optional doubles node-link / chord / flow map]

That is **4 clear sections**, 6+ advanced/custom idioms, and 3 genuine maps — hitting the HD bars for the Sketch ("four or more clear sections… varied charts and maps"), Idioms & Complexity ("creative custom-built"), and Layout simultaneously.

---

## 9. Execution order for the implementer (highest value first)

1. **Cartogram** (#6) — biggest narrative payoff, satisfies map requirement strongly. Precompute geometry in Python; render `geoshape`.
2. **Sankey** (#11) — converts the weakest current chart (log funnel) into a custom idiom.
3. **Melbourne proportional-symbol map** (#9) — fixes the fake-geography scatter; combine D4 census + D5 courts.
4. **Kinetic-chain node-link + body-map linked highlight** (#4) — adds Part-1 idiom + interaction together.
5. **Bump chart + adjacency matrix** (#12, #13) — re-source D1/D2, add Part-3 interaction.
6. Annotation/typography/layout polish pass across all figures (shaded periods, reference lines, sight-line alignment, consistent sequential/diverging colour).
7. Stretch: alluvial, chord, flow map, dot-density/hexbin — add only if time.

**Acceptance criteria per figure:** real data from ≥2 sources cited; appropriate marks/channels (no hue for ordered data); at least one informative annotation; loads with total payload < few MB; renders full-width with no horizontal scroll on a 13" laptop; JSON spec committed to the repo and human-readable.

---

## 11. All datasets in use — files and sources

Complete inventory of every data file used or planned in the project, with its primary source URL and licence/access notes.

### New datasets (collected 2026-05-30, in `data/`)

| File | Description | Rows / Size | Source | URL | Licence |
|------|-------------|-------------|--------|-----|---------|
| `bwf_rankings_deep.csv` | Year-end BWF world rankings for 8 Australian players (2013–2024), all disciplines. Unconfirmed years flagged `estimated=true`. | 87 rows | BWF official rankings + Wikipedia player infoboxes | https://bwfbadminton.com/rankings/ · https://en.wikipedia.org | CC BY / public |
| `australian_open_results.csv` | Australian Badminton Open results 2010–2024: grade, host city, prize money, winners per discipline, total entries. 2020–21 cancelled rows included. | 15 rows | Wikipedia — Australian Open (badminton) | https://en.wikipedia.org/wiki/Australian_Open_(badminton) | CC BY-SA |
| `ausplay_state_by_year.csv` | AusPlay estimated badminton participation by state 2016–2024 (participants_thousands, participation_rate_pct). National totals confirmed; state splits population-weighted and flagged `estimated=true`. | 72 rows | Australian Sports Commission — AusPlay participation data | https://www.ausport.gov.au/research-and-innovation/ausplay | Open Government |
| `abs_lga_asian_born_2021.csv` | ABS 2021 Census: total population and Asian-born count/pct for 17 Melbourne LGAs. Counts from QuickStats "top responses" only (undercount); flagged `estimated=true`. | 17 rows | ABS 2021 Census QuickStats | https://abs.gov.au/census/find-census-data/quickstats/2021/ | CC BY 4.0 |
| `badminton_victoria_clubs.csv` | Badminton Victoria affiliated clubs: name, suburb, LGA, lat/long (approx), courts, type. 40 Melbourne-metro clubs. | 40 rows | Badminton Victoria clubs directory | https://badmintonvic.com.au/clubs | Public |
| `melbourne_lga_boundaries.geojson` | Simplified GeoJSON boundaries for 29 Melbourne metro LGAs (point-decimation tolerance 0.002°), field `LGA_NAME_2021`. 154 KB. | 154 KB | ABS ASGS2021 REST API | https://geo.abs.gov.au/arcgis/rest/services/ASGS2021/LGA/MapServer/0/query | CC BY 4.0 |
| `bwf_player_profiles.csv` | Physical profiles for 8 Australian BWF players: DOB, height, weight, handedness, birth country. 5 of 8 confirmed from Wikipedia; 3 have no public page. | 8 rows | Wikipedia player infoboxes | https://en.wikipedia.org/wiki/Setyana_Mapasa (etc.) | CC BY-SA |

### Existing datasets (from earlier project work, in `data/`)

| File | Description | Source |
|------|-------------|--------|
| `longevity_sports.csv` | Life expectancy by sport type | Literature / hand-curated |
| `calorie_burn_activities.csv` | Calories burned per sport per hour | Literature / hand-curated |
| `muscle_activation_smash.csv` | EMG %MVIC by muscle group and swing phase | Academic EMG literature |
| `muscle_regions.geojson` | Body-map polygon regions for muscle overlay | Hand-drawn / custom |
| `ausplay_historical_trends.csv` | National badminton participation trend (earlier, shorter version) | AusPlay reports |
| `ausplay_badminton_demographics.csv` | Participation by age/gender snapshot | AusPlay reports |
| `badminton_participation_by_age_gender.csv` | Age × gender breakdown | AusPlay |
| `badminton_participation_trend.csv` | Year-level national trend | AusPlay |
| `australia_badminton_participation_by_state.csv` | Earlier state-level snapshot | AusPlay |
| `abs_melbourne_lga_demographics.csv` | Earlier LGA demographics (smaller, superseded by `abs_lga_asian_born_2021.csv`) | ABS Census |
| `australian_players_bwf_rankings.csv` | Earlier, shorter rankings table (superseded by `bwf_rankings_deep.csv`) | BWF / hand-curated |
| `bwf_tournaments_australia.csv` | Australian Open tournament history (superseded by `australian_open_results.csv`) | Wikipedia |
| `melbourne_badminton_venues.csv` | Earlier venues list (superseded by `badminton_victoria_clubs.csv`) | Badminton Victoria |
| `melbourne_lga.geojson` | Earlier Melbourne LGA boundaries (superseded by `melbourne_lga_boundaries.geojson`) | ABS |
| `melbourne_lga_courts.csv` | LGA-level court count summary | Derived from venues |
| `aus_states.geojson` / `aus_states_fixed.geojson` / `aus_states_mainland.geojson` | Australian state boundaries | ABS ASGS |
| `states.geojson` | Alternate state boundary file | ABS ASGS |
| `talent_pipeline.csv` | Talent funnel counts (grassroots → elite) | Hand-curated estimates |

### What does NOT exist publicly (confirmed after search)
The following were searched across Kaggle, GitHub, BWF APIs, and academic sources — no usable public dataset exists for these specifically for Australian players:
- Physical performance metrics: strength, flexibility, speed, agility, jump height, endurance
- Match-level win/loss records for Australian players at BWF World Tour events
- Player profile data (height/weight) for Simon Leung, Wendy Chen, Jack Yu (no Wikipedia pages)

---

## 10. Don't forget (submission mechanics)

- **Sketch PDF** must match the *new* layout (4+ clear sections, varied charts) — redo it, on paper, before submitting (digital sketch = 0 on that criterion).
- **500-word writeup:** restate Why/Who/What/How; for **How**, explicitly name the custom-built idioms (cartogram, Sankey, node-link) and that their geometry is *derived in Python and rendered in Vega-Lite* — this is the HD signal the rubric asks for.
- **Acknowledge AI use** and **cite every dataset URL**.
- Keep the existing strong editorial voice; it already scores well on storytelling.

### Technical build notes (Python precompute pattern)
For each non-native idiom: write a small script under `scripts/` that reads raw data, computes layout coordinates, and writes a derived file under `data/` (e.g. `sankey_nodes.csv`, `sankey_links.csv`, `cartogram.geojson`, `kinetic_chain_nodes.csv`/`_edges.csv`). The Vega-Lite spec then just draws primitives from those derived files. Libraries: `squarify` (treemap), `networkx` (node-link layout), `scipy.cluster`/`scipy` (dendrogram/contours), a cartogram routine (e.g. `geopandas` + a Dorling/diffusion cartogram, or precomputed) for #6. This keeps the whole site Vega-Lite and frames the work as derived data — exactly what the HD band rewards.
