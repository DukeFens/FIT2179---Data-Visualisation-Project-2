# Improvement Plan — The Shuttlecock Effect

Topic: Australian badminton. Reference design language: https://deatharder.github.io/afl-viz/ (adopt the *approach*, keep our **green** theme). Keep the existing project — re-section, clean, and upgrade; do not rebuild from scratch.

---

## A. Narrative — 4 sections (assignment needs ≥4)

1. **THE BODY** — why badminton is worth playing (health, energy, anatomy of a smash).
2. **THE NATION** — participation across Australia (states, growth, demographics, talent pipeline).
3. **THE CITY** — badminton in Greater Melbourne (where courts and players are).
4. **THE COMPETITIVE EDGE** — Australia on the world stage (rankings, Australian Open, tournaments).

## B. Chart inventory — data → idiom → section → status

Every chart must justify its idiom by the data type (see §1). Status: **DONE** (already meets the rules) / **TODO** (still needs the cleanup pass) / **TODO+FILTER** (clean + add interaction). Nothing below is "done" except where marked.

**First: DELETE the node-link chart entirely** — `vis-kinetic` (`chart_kinetic_chain`, `kinetic_chain_nodes/edges.csv`). Over-complex, no added insight; the body-shape SVG already tells the smash story. Remove its section, loader entry, and spec.

| # | Section | Chart (id) | Data file(s) | Idiom | Status |
|---|---------|-----------|--------------|-------|--------|
| 1 | Body | vis-health (`chart2_longevity_lollipop`) | `longevity_sports.csv` | Lollipop (custom) | TODO |
| 2 | Body | vis-calories (`chart3_calorie_bar`) | `calorie_burn_activities.csv` | Horizontal bar | TODO |
| 3 | Body | vis-muscles (`chart1_muscle_body_map`) | `muscle_regions.geojson`, `muscle_activation_smash.csv` | **Custom body-shape choropleth (SVG)** | TODO (keep idiom, recolour/clean) |
| 4 | Nation | vis-states (`chart4_choropleth_map`) | `aus_states_mainland.geojson`, `cartogram_dorling.csv` | **Choropleth map** (geo requirement) | TODO |
| 5 | Nation | vis-cartogram (`chart_cartogram`) | `cartogram_dorling.csv` | **Dorling cartogram (custom)** | TODO |
| 6 | Nation | vis-growth (`chart4_longitudinal_growth`) | `ausplay_state_by_year.csv` | Multi-line trend | TODO+FILTER (state selector) |
| 7 | Nation | vis-demo (`chart5_demographic_heatmap`) | `badminton_participation_by_age_gender.csv` | Heatmap | TODO |
| 8 | Nation | vis-sankey (`chart_funnel_pipeline`) | `talent_pipeline.csv` | **Horizontal bar, log scale** | DONE (replaced wrong Sankey idiom) |
| 9 | City | vis-melb-map (`chart_city_paired`) | `melb_dots.csv`, `melbourne_lga_boundaries.geojson` | **Dot-density map (custom)** | TODO |
| 10 | City | vis-melb (`chart_city_correlation`) | `melbourne_lga_merged.csv` (`abs_lga_asian_born_2021.csv`) | Scatter + reference line | TODO |
| 11 | Edge | vis-bump (`chart_bump_rankings`) | `australian_players_bwf_rankings.csv` | **Bump chart (custom)** | TODO+FILTER (highlight player) |
| 12 | Edge | vis-adjacency (`chart_adjacency_matrix`) | `aus_open_wins_matrix.csv` / `adjacency_nations.csv` | **Adjacency matrix** | TODO |
| 13 | Edge | vis-tournaments (`chart8_tournament_density`) | `bwf_tournaments_australia.csv` | Density / bubble timeline | TODO |

→ **13 charts after deleting the node-link** — above the ≥10 requirement, with 6 custom/derived idioms (body SVG, Dorling cartogram, dot-density map, log pipeline, bump, adjacency matrix). Only #8 is done; the other 12 still need the cleanup pass.

**Spare data not yet used** (mine for a stronger chart only if it adds insight, never for filler): `bwf_rankings_deep.csv`, `bwf_player_profiles.csv`, `australian_open_results.csv`, `badminton_victoria_clubs.csv`, `ausplay_badminton_demographics.csv`.

## C. Coordinated interaction — at least one "Explore" dashboard

Build **one** dashboard where a single control filters several simple views at once (afl-viz "Explore the data yourself" model). Best candidate: **a state/year selector driving the growth line + demographic heatmap + state participation together.** "Combined" = multiple coordinated views updating from one control — NOT charts merged on top of each other.

## D. Assignment requirements checklist

- [x] ≥4 sections (§A)
- [x] ≥1 geographic map (choropleth #4; also dot-density #9, cartogram #5)
- [x] ≥10 visualisations (13)
- [x] Custom / derived idioms (6 listed in §B)
- [ ] Coordinated interaction (§C — to build)
- [ ] AI-use acknowledgement in About (§8)

---

## 1. Encoding rules (must follow — this is a visualisation assignment)

Bertin / Mackinlay effectiveness ranking, not personal taste:
- **Nominal/categorical → HUE** (and shape, position). Only true categories get different hues.
- **Ordinal/quantitative → LUMINANCE, LENGTH, POSITION, SIZE.** Never multiple hues for ordered data.
- **Magnitude accuracy:** position > length > angle > area > luminance/saturation > hue.
- **One dominant hue (green)**; sequential green ramp for ordered/quantitative; ≤1 muted secondary accent per chart. No rainbow.
- **Honest scales:** disclose log/√ in caption; zero-baseline for bar length.

## 2. Figure-naming convention (keep SHORT)

- **Caption = one short sentence + `Source: …`.** A method note is one short clause, not a paragraph. Small-multiples share one caption (`Figures 4 to 6 ·`).
- **Title on-canvas = two short lines:** bold title + plain grey subtitle (no scale jargon/ranges crammed in).
- **Section headers:** ALL-CAPS, short, left-aligned.
- Separator is the middle dot `·`; captions italic, muted grey; number every figure.

## 3. Annotation rules (overlap = lost marks)

- Minimal and **direct** — label the line/region/point itself instead of a legend where possible.
- One idea per annotation; move repeated detail to tooltip.
- Fixed, non-colliding placement; verify in-browser that no text overlaps before "done".
- Callout = thin leader line + bold number + small grey sub-line, in empty space.

## 4. Colour system (green)

- Cream bg `#F3F6F0`; ink `#172821`; muted grey `#506158`.
- Sequential green ramp: `#5BAE7C → #3F9A66 → #2C8454 → #1E6B41 → #13502F`.
- Sequential legend = one gradient bar, 3–4 ticks max.

## 5. Fine details from afl-viz

- **Direct labelling:** name only the "story" points/lines; label reference lines in place (`Even win/loss line`, dashed `Median: 22`).
- **Lollipop:** thin stem + value **inside** the dot.
- **Heatmap:** leave empty cells blank (don't fill zeros); dark border to flag special cells; short in-chart note.
- **Era/region:** shaded band with inline italic label (`Peak: 1975 to 1990`); per-panel mini-stats.
- **Scatter:** size + colour double-encode; one italic helper sentence under the title.
- **Interaction:** dropdown **and** click-legend-to-filter; one dropdown drives multiple sub-views.
- **Typography:** comma-formatted numbers; dark ink only for emphasis; minimal/no gridlines; no card borders; generous whitespace; alternating text/chart layout.
- **About:** short, honest AI-use acknowledgement paragraph.

## 6. Workflow (per chart)

Pick idiom by data type → encoding rules (§1) → green system (§4) → two-line title + `Figure N ·` short caption (§2) → minimal direct annotation (§3) → reload localhost & screenshot → confirm no overlap → mark done.
