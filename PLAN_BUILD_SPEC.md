# Build Spec — Vega-Lite construction details (companion to IMPROVEMENT_PLAN.md)

This file tells the implementer **exactly how to build each figure in Vega-Lite v5**: marks, channel encodings, layers (combined idioms), transforms, and interaction `params`. Read `IMPROVEMENT_PLAN.md` first for the why/structure; this file is the how.

All specs target Vega-Lite v5. Where an idiom needs Python precompute, the script writes a small derived file under `data/` and the spec only renders primitives — keeping the whole site Vega-Lite (HD-rewarded "derived data", no tutor approval needed).

---

## 0. Reusable interaction patterns (use these everywhere)

**A. Dropdown filter** (already used on the heatmap):
```json
"params": [{
  "name": "yearSel",
  "value": 2025,
  "bind": {"input": "select", "options": [2016,2019,2021,2023,2025], "name": "Year: "}
}],
"transform": [{"filter": "datum.year == yearSel"}]
```

**B. Hover-highlight (focus+context)** — fade everything except the hovered category. Channel = opacity (acceptable; never use hue for this):
```json
"params": [{"name": "hov", "select": {"type": "point", "on": "mouseover", "fields": ["club"], "clear": "mouseout"}}],
"encoding": {"opacity": {"condition": {"param": "hov", "value": 1}, "value": 0.15}}
```

**C. Click-to-persist selection / legend filter:**
```json
"params": [{"name": "pick", "select": {"type": "point", "fields": ["state"]}, "bind": "legend"}]
```

**D. Cross-view linking (CRITICAL):** a `param` only reaches views inside the *same* spec. To link two charts, compose them with `"hconcat"`/`"vconcat"` (or `"concat"`) at the top level and declare the shared `param` once at the top. Two separately `vegaEmbed`-ed JSON files **cannot** share a selection. So every "hover here → highlight there" figure below is authored as ONE concatenated spec.

**E. Interval brush** (for the bump chart timeline): `{"name":"brush","select":{"type":"interval","encodings":["x"]}}`.

Keep interaction tasteful (rubric: *presentation, not exploration*) — one linked/filter behaviour per section, no free-form analysis tools.

---

## 0a. RESOLVED — Python environment & dependencies (read first)

Checked the project `.venv`: **`numpy` (2.4.6) and `pandas` (3.0.3) are installed; `shapely`, `scipy`, `geopandas` are NOT.** All precompute below is written to need **only numpy + pandas** — no extra installs. (You *may* `pip install shapely scipy` on the user's Mac if you prefer, but the specs do not require it.)

- **Cartogram (Fig 6):** only 8 states → **do NOT use scipy force simulation.** Use manual anchor placement + optional pure-numpy repel (see Fig 6).
- **Dot-density (Fig 10):** **do NOT use shapely.** Use pure-numpy ray-casting point-in-polygon (see Fig 10).

---

## PART 1 — THE BODY

### Fig 1 — Longevity lollipop (keep + annotate)
- **Idiom:** lollipop (rule + circle) — combined with an annotation layer.
- **Data:** `longevity_sports.csv` (sport, years_gained, category).
- **Layers:**
  1. `rule`: `x` = `years_gained:Q` from 0 to value (`x2` baseline 0), `y` = `sport:N` sorted by years_gained desc.
  2. `circle`: `x`=years_gained, `y`=sport, `size` ~140, `color` = `category:N` (highlight "Racket" in a saturated hue, all else grey via `scale`/`condition`).
  3. `text`: value labels right of each dot (`align:left`, `dx:6`).
  4. **Annotation** `rule`: vertical reference line at the sedentary baseline (0) + a `text` mark calling out "Racket sports: +6 yrs".
- **Channels:** position(x) = magnitude (primary), position(y) = nominal sport, hue = category (categorical → correct).
- **Interaction:** none (it's a hero stat). 

### Fig 2 — Calorie lollipop (small-multiple pair with Fig 1)
- Same lollipop construction on `calorie_burn_activities.csv` (activity, calories_per_hour_70kg, category).
- **Combine:** present Fig 1 + Fig 2 as a `hconcat` so the two share y-axis styling and read as one comparative panel (layout symmetry → Layout criterion).
- Highlight badminton bars in accent hue; grey the rest.

### Fig 3 — Muscle body-map + per-phase small multiples (keep, extend)
- **Idiom:** image basemap + `geoshape`/colored regions (already built) → now **faceted by phase**.
- **Data:** `muscle_activation_smash.csv` (muscle, id, body_region, activation_pct_mvic, **phase**).
- **Build:** keep the SVG body image as a background `image` mark; color muscle regions by `activation_pct_mvic:Q` (sequential single-hue scale, e.g. greens). Add `"facet": {"column": {"field": "phase", "sort": ["Jump","Smash","Landing"]}}` to show how activation migrates through the swing.
- **Channels:** luminance/saturation = activation (ordered → sequential scale, correct), position = anatomy.
- **Interaction:** shared with Fig 4 (below).

### Fig 4 — Smash kinetic-chain Node-Link (NEW) + linked to body-map
- **Idiom:** node-link diagram. **Combined** with Fig 3 in ONE spec for linked highlight.
- **Precompute (Python):** ~15 muscles. Because it's small, hand-place coordinates along the kinetic chain (calf bottom → finger top) OR `networkx.spring_layout`. Emit:
  - `data/kinetic_nodes.csv`: `id, label, x, y, activation_pct_mvic, body_region`
  - `data/kinetic_edges.csv`: `source, target, x, y, x2, y2` (edge endpoints already resolved to node coords, so VL needs no lookup).
- **Spec (single `vconcat`):**
  - Shared param: `{"name":"musc","select":{"type":"point","on":"mouseover","fields":["id"],"clear":"mouseout"}}`.
  - **View A = body map** (Fig 3) with `params:[musc]`; regions get `opacity` condition on `musc`.
  - **View B = network:**
    - Layer 1 `rule`: edges, `x/y/x2/y2` from `kinetic_edges.csv`; `opacity` condition: highlight edges whose source/target match selected node — `{"condition":{"test":"musc.id == datum.source || musc.id == datum.target","value":0.9},"value":0.15}`.
    - Layer 2 `circle`: nodes, `x`/`y`, `size` = `activation_pct_mvic:Q`, `color` = `body_region:N`; `opacity` condition on `musc`.
    - Layer 3 `text`: muscle labels.
- **Channels:** size = activation magnitude, hue = body region, connection = activation sequence. Hover a muscle in either view → both highlight (linked).

---

## PART 2 — THE NATION

### Fig 5 — State choropleth + proportional-symbol overlay (combined idioms, one map)
- **Idioms combined:** choropleth + proportional symbol on the same projection.
- **Data:** D6 states GeoJSON + D3 `australia_badminton_participation_by_state.csv`.
- **Build (layered map):**
  1. `geoshape` basemap from `topojson`/GeoJSON `feature`; `color` = `participation_rate_pct:Q` (sequential blues) via `transform lookup` joining csv on state.
  2. `circle` layer: `longitude`/`latitude` = state centroid (precompute or use `geoCentroid`), `size` = `total_participants_thousands:Q` (proportional symbol; use `scale type:"sqrt"` so AREA encodes value — important, area not radius).
  3. `text`: state codes.
- **Projection:** `{"type":"mercator"}` (already used) or `albers`-style fitted to AU bounds.
- **Channels:** luminance = rate (rate is intensive → choropleth correct); circle area = count (count is extensive → symbol correct). This rate-vs-count split is itself a teaching point — annotate it.
- **Interaction:** shared `pick` param (state) linking to the cartogram (Fig 6) — author Fig 5 + Fig 6 as one `hconcat`.

### Fig 6 — Area Cartogram (NEW, headline) — paired with Fig 5
- **Idiom:** area cartogram (states resized by participant count).
- **Precompute (Python, numpy only — RESOLVED):** build a **Dorling cartogram** without scipy. Step 1: hand-pick 8 anchor coordinates roughly matching Australia's geography (e.g. WA left, QLD top-right, NSW/VIC/TAS down the east, NT top-centre, SA centre, ACT inside NSW) into a dict. Step 2: radius `r = k * sqrt(participants)` (area ∝ value). Step 3 (optional, ~50 iterations of pure-numpy repel): for every overlapping pair, push centres apart by half their overlap each iteration; anchors keep the map legible. Emit `data/cartogram.csv`: `state, x, y, r, total_participants_thousands, participation_rate_pct`. For 8 states, manual placement alone is defensible — the repel loop just polishes overlaps. (If you ever want true distorted *polygons* instead of circles, that needs a diffusion cartogram + geopandas — out of scope; circles are the recommended Dorling form.)
- **Spec:** `circle` mark, `x`/`y` from precomputed coords (`"x":{"field":"x","type":"quantitative","axis":null}`, same for y, both axes hidden). Encode size from the precomputed radius as **area**: `"size":{"field":"area","type":"quantitative","scale":{"type":"identity"}}` where Python also writes `area = pi*r^2` — this guarantees the circle areas exactly match the Dorling sizing (don't let Vega re-scale). `color` = `participation_rate_pct` (diverging scale around the national mean to spotlight the VIC anomaly); `text` labels for state codes.
- **Combine with Fig 5:** side-by-side `hconcat`, shared `pick` selection so clicking VIC highlights it on both the geographic map and the cartogram → the "20% population / 40% players" distortion is the takeaway.
- **This is the geographic-map requirement's most innovative element** — annotate VIC explicitly.

### Fig 7 — Gender area-band line (keep, strengthen annotation)
- **Idiom:** dual line + area band (gap) — already built.
- **Data:** `badminton_participation_trend.csv` (male/female thousands by year).
- **Build:** `area` mark with `y`=male, `y2`=female (the gap band, low-opacity); two `line` marks for each gender; `rule`+`text` annotation at the 2024 methodology revision (dashed). Add a `point` layer on the most recent year with a label.
- **Channels:** position = participants over time; band area = the gender gap (the insight).
- **Interaction:** none needed.

### Fig 8 — Demographic heatmap (keep dropdown) [+ optional alluvial]
- **Idiom:** rect heatmap (matrix), `x`=age_group(ordered), `y`=gender, `color`=percentage:Q with a **fixed** scale `domain` across years (so dropdown comparisons are honest).
- **Data:** `ausplay_badminton_demographics.csv`.
- **Interaction:** Pattern A dropdown (`yearSel`).
- **Optional combine — Alluvial** of cohort flow across years:
  - Precompute `data/alluvial_age.csv`: parallel-sets bands `{year_from, year_to, age_group, x, y, y2}`. Render `area` ribbons (x spans adjacent year columns; y/y2 = band edges) colored by age_group. Shows the 18–24 surge as visible flow.

---

## PART 3 — THE CITY (Melbourne)

### Fig 9 — Melbourne proportional-symbol map (NEW; replaces fake scatter) — the geographic map
- **Idioms combined:** geoshape LGA basemap (choropleth) + proportional symbols.
- **Data:** D6 Greater-Melbourne LGA/SA2 GeoJSON (simplified < few MB) + D4 census `melbourne_lga_courts.csv` (asian_born_pct_2021) + D5 venue courts.
- **Build (layered):**
  1. `geoshape` LGA polygons; `color` = `asian_born_pct_2021:Q` (sequential) via lookup.
  2. `circle` at venue lat/long (`melbourne_badminton_venues.csv`), `size` = `courts:Q` (sqrt scale).
  3. `text` for the top-3 LGAs (Monash, Whitehorse, Greater Dandenong).
- **Projection:** `mercator` fitted to metro bounds (`"fit"` to the GeoJSON extent).
- **Interaction:** shared `lgaHov` param linking to Fig 10 — author Fig 9 + Fig 10 in one `hconcat`/`vconcat`.

### Fig 10 — Dot-density OR hexbin court map (NEW, 2nd city idiom)
- **Dot-density (recommended; numpy only — RESOLVED):** expand each LGA's count into N points (e.g. 1 dot per 200 players) placed *inside* the LGA polygon by **rejection sampling with a pure-numpy ray-casting point-in-polygon test** — no shapely. Algorithm: read the LGA ring coords from the GeoJSON; for each LGA, draw random (lng,lat) inside its bounding box, keep a point if ray-casting says it is inside the ring, repeat until N kept. Ray-casting is ~12 lines (count how many polygon edges a rightward ray from the point crosses; odd = inside). Handle multi-part LGAs by testing each ring. Emit `data/melb_dots.csv`: `lng, lat, lga`. Render `circle` size ~6, opacity ~0.35, colored by `lga`, layered over a faint `geoshape` boundary.
- **Fallback if you want zero geometry code:** grid-sample — lay a fine lat/long grid over each bounding box and keep grid cells whose centre passes the same ray-cast test; coarser but identical dependencies. (Last resort only: jittered cloud around each LGA centroid — loses the true shape.)
- **Hexbin alternative:** precompute hex centroids (`h3` or manual) with court counts; render `point` with `shape` or `square`, `size`/`color` = count.
- **Interaction:** `lgaHov` highlight from Fig 9 dims non-selected LGAs here.

### Fig 11 — Diaspora–courts correlation (keep, reframe as supporting analysis)
- **Idiom:** scatter + regression line (the old "City" chart, now correctly positioned as analysis *of* the maps, not a substitute).
- **Data:** `melbourne_lga_courts.csv`.
- **Build:** `circle` `x`=asian_born_pct_2021, `y`=courts, `size`=population_2021; add `transform: [{"regression":"courts","on":"asian_born_pct_2021"}]` → `line` layer for the trend; `text` labels top LGAs.
- **Channels:** position=correlation, size=population. Annotate the near-linear relationship in plain language (no "R²" jargon — rubric: avoid statistics).

---

## PART 4 — THE COMPETITIVE EDGE

### Fig 12 — Talent-pipeline Sankey (NEW; replaces log-bar funnel)
- **Idiom:** Sankey. **VL render of precomputed ribbons.**
- **Precompute (Python):** from `talent_pipeline.csv` (level, estimated_players, next_level_pct) compute, for each link between consecutive tiers, a filled ribbon. Sample ~20 x-positions between the two tier columns; at each, compute top edge `y` and bottom edge `y2` with a smoothstep so the band curves. Emit `data/sankey_ribbons.csv`: `link_id, source_level, x, y, y2` and `data/sankey_nodes.csv`: `level, x, y, y2, count`.
- **Spec (layered):**
  1. `area` mark (the ribbons): `x:{quantitative,axis:null}`, `y`, `y2`, `detail`=`link_id`, `color`=`source_level:N`, `opacity` ~0.6, `interpolate:"monotone"`.
  2. `rect` (the nodes): tier bars from `sankey_nodes.csv` (`x`,`x2` thin, `y`,`y2`).
  3. `text`: tier name + count ("40,952 → … → <20").
- **Channels:** ribbon width = flow magnitude, x = tier progression. The dramatic narrowing IS the story.
- **Interaction:** hover a tier `rect` → highlight its outgoing ribbon (`param` + opacity condition on `source_level`).

### Fig 13 — Rankings bump chart (NEW; upgrades the multiline) 
- **Idiom:** bump/rank chart (line + point), derived via window transform.
- **Data:** D1 `australian_players_bwf_rankings.csv` (player, year, week, world_ranking).
- **Build:**
  - `transform`: build a continuous date, then `window` rank if needed, but you already have `world_ranking` → use it directly. `y` = `world_ranking:Q` with `scale: {"reverse": true}` (rank 1 at top).
  - Layer 1 `line` (`x`=date, `y`=ranking, `color`=player, `detail`=player).
  - Layer 2 `point` at each observation.
  - Layer 3 annotation: shaded `rect` over the 2022–2024 window + `text` "two years top-30 → Paris 2024".
- **Interaction:** Pattern B hover-highlight on `player` (foreground one path, fade others) — exactly the AFL "hover a club path" behaviour. Optional Pattern E brush on x to read a period.

### Fig 14 — Head-to-head Adjacency Matrix (NEW; VL-native)
- **Idiom:** adjacency matrix (rect heatmap) — **native, no precompute.**
- **Data:** D2 match results between top AUS players / rival nations → aggregate wins.
- **Build:** `rect`, `x`=`player_a:N`, `y`=`player_b:N` (same sort order both axes), `color`=`wins:Q` (sequential); `text` layer with the count. Add a diagonal `rule` to mark self-cells.
- **Channels:** luminance = head-to-head wins (ordered → correct). Compact, high data-ink ratio.
- **Optional swap/add:** doubles-partnership **node-link** (same build pattern as Fig 4, nodes=players, edges=pairings) or a **chord** of Australian-Open nationalities (chord ribbons need precompute or tutor-approved D3 — keep as stretch only).

### (Optional) Fig 15 — Tournament bubble OR flow map
- Keep existing `bwf_tournaments_australia.csv` bubble (size=entries, color=grade, annotate the 2023 Super 500 upgrade), OR upgrade to a **flow map**: precompute curved arcs from each entrant country to Sydney/Melbourne (`data/flows.csv`: `lng,lat` sampled along great-circle arcs, `volume`), render `line`/`trail` with `size`=volume over a world `geoshape`.

---

## Build order & per-figure acceptance checklist

Order (highest value first): **Fig 6 cartogram → Fig 12 Sankey → Fig 9 city map → Fig 4 kinetic node-link → Fig 13 bump + Fig 14 matrix → annotation/typography polish → optional alluvial/flow/chord.**

Each figure is "done" when: (1) draws from ≥2 cited sources where applicable; (2) marks/channels match data type (no hue for ordered, area-not-radius for symbols); (3) has ≥1 informative annotation; (4) its `params`/linking work as specified; (5) JSON is committed, human-readable, and the page payload stays < a few MB; (6) renders full-width with no horizontal scroll on a 13" laptop.

**HD signals this delivers:** combined idioms on single views (Figs 5+6, 9+10, 3+4, choropleth+symbol), genuine interaction (linked highlight Figs 3↔4 / 5↔6 / 9↔10, hover-foreground Fig 13, dropdown Fig 8, Sankey hover Fig 12), and 6+ custom-built/derived idioms (cartogram, Sankey, node-link, dot-density, adjacency matrix, bump).
