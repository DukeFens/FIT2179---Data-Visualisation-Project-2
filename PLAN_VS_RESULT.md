# Plan vs. Final Result — Reconciliation

Comparison of the **recommended final lineup** (IMPROVEMENT_PLAN.md §8) against what is
actually wired into `index.html` and rendering. Verified by: headless Vega compile/render
harness (`scripts/validate.js`, all 14 specs ✅) + Chrome DevTools network/console
(all spec + data requests returned HTTP 200, zero JS errors).

## Status legend
- ✅ **Match** — built, wired, renders, matches plan intent.
- ⚠️ **Partial** — built and rendering, but a planned enhancement is missing or simplified.
- ➕ **Bonus** — present beyond the plan.

---

## Part 1 — The Body

| # | Plan item | Wired spec | Status | Notes |
|---|-----------|-----------|--------|-------|
| 1 | Longevity lollipop (annotated) | `chart2_longevity_lollipop.json` | ✅ | Renders. |
| 2 | Calorie lollipop (pair with #1) | `chart3_calorie_bar.json` | ⚠️ | Built as a **horizontal bar** (badminton highlighted), not a lollipop. Functionally equivalent; cosmetic deviation. |
| 3 | Muscle body-map **+ per-phase small-multiples** | `chart1_muscle_body_map.json` | ⚠️ | Single body-map renders. The **per-phase (Jump/Smash/Landing) small-multiples** are NOT in the wired spec. A faceted + kinetic-linked version exists unused at `chart_body_paired.json`. |
| 4 | Kinetic-chain node-link **(linked to #3)** | `chart_kinetic_chain.json` | ⚠️ | Node-link renders with hover. The **linked highlight body-map ↔ network** is not active in the wired standalone (cross-spec selection isn't possible across two separate embeds). The linked version lives in `chart_body_paired.json`. |

## Part 2 — The Nation

| # | Plan item | Wired spec | Status | Notes |
|---|-----------|-----------|--------|-------|
| 5 | State choropleth + proportional-symbol overlay | `chart4_choropleth_map.json` | ✅ | Choropleth (players/million) + sqrt-scaled circles. Join fixed (full state name → abbreviation). |
| 6 | Area cartogram (headline idiom) | `chart_cartogram.json` | ✅ | Dorling circles sized by participants, coloured by players/million. |
| 7 | Gender area-band line | `chart4_longitudinal_growth.json` | ✅ | Renders. |
| 8 | Demographic heatmap (year dropdown) | `chart5_demographic_heatmap.json` | ✅ | Interactive dropdown present. |

> Plan's optional **choropleth ↔ cartogram linked highlight** exists unused at `chart_nation_paired.json`; wired versions are standalone (not cross-linked).

## Part 3 — The City

| # | Plan item | Wired spec | Status | Notes |
|---|-----------|-----------|--------|-------|
| 9 | Melbourne proportional-symbol map (census × courts) | `chart_city_paired.json` (top panel) | ✅ | Real Greater-Melbourne basemap, Asian-born % choropleth + court circles. |
| 10 | Dot-density / hexbin court map (2nd map idiom) | `chart_city_paired.json` (bottom panel) | ✅ | Dot-density map, **linked-highlight to the top panel** (shared `lgaHov` selection). This is the one fully-realised linked combined idiom. |
| 11 | Diaspora–courts correlation (annotated) | `chart_city_correlation.json` | ✅ | Scatter with trend, r ≈ 0.81. |

## Part 4 — The Competitive Edge

| # | Plan item | Wired spec | Status | Notes |
|---|-----------|-----------|--------|-------|
| 12 | Talent-pipeline Sankey | `chart_sankey_pipeline.json` | ✅ | Precomputed node rects + ribbon bands (derived data in Python). *Was appearing as a "tiny bar" only because the whole section was stuck at opacity 0 — see fix below.* |
| 13 | Rankings bump chart (+ hover foreground) | `chart_bump_rankings.json` | ✅ | Hover-to-foreground on player path (`playerHov`). Olympic top-30 zone + Paris 2024 band annotated. |
| 14 | Head-to-head adjacency matrix | `chart_adjacency_matrix.json` | ✅ | Native `rect` heat-matrix. |
| ➕ | (Tournament view — old Fig 10 upgrade) | `chart8_tournament_density.json` | ➕ | Bonus 14th figure; bubble/density of Australian BWF events. |

---

## Headline scorecard

- **4 sections** (Body / Nation / City / Competitive Edge) — ✅ matches HD structure requirement.
- **≥1 geographic map** — ✅ three genuine maps (state choropleth, cartogram, Melbourne basemap + dot-density).
- **≥10 visualisations** — ✅ 14 figures wired.
- **Custom / derived-data idioms** — ✅ Sankey, cartogram, node-link, dot-density, adjacency matrix all built from Python-precomputed geometry rendered in pure Vega-Lite.
- **Coordinated interaction** — ⚠️ delivered in City (linked map↔dots), bump hover, heatmap dropdown, kinetic hover. The **Body** and **Nation** linked-highlight combos were built (`chart_body_paired`, `chart_nation_paired`) but are **not wired** — the standalone versions are used instead.

## Bug found & fixed during review

1. **Whole page stuck invisible (the "nothing updated / messy" symptom).** 27 of 28 `.reveal`
   sections sat at `opacity: 0`. The `<body>` is the scroll container (`overflow-y:auto`),
   which made the viewport-rooted `IntersectionObserver` never fire, so sections below the
   first screen never received the `.visible` class. **Fix:** replaced the observer with a
   plain scroll listener (reveals within 92% of viewport) plus a 2.5 s safety net that
   force-reveals everything — nothing can stay hidden now.
2. **Sankey "tiny bar".** Not a data bug — the ribbons (opacity 0.25) were being multiplied
   by the section's ~0.1 opacity, leaving only the solid Grassroots node rect visible. Fixed
   automatically by (1).
3. (From earlier pass) 4× duplicate-signal runtime errors, a broken state-name join, and
   6 dangling 404 spec references — all resolved.

## Outstanding decisions for you

- **Wire the linked Body & Nation combos?** To make Parts 1–2 match the plan's
  linked-highlight intent, repoint `#vis-muscles → chart_body_paired` and
  `#vis-states → chart_nation_paired` (each merges two panels into one figure, so the
  separate kinetic/cartogram sections would be folded in). This strengthens the HD
  "combined idioms" score but changes the figure count/numbering.
- **Calorie chart:** convert the bar to a true lollipop to mirror Fig 1, if exact pairing matters.
- **Muscle map:** add the Jump/Smash/Landing per-phase small-multiples.
