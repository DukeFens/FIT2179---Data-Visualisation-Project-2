"""
scripts/build_funnel.py
Precomputes a centred FUNNEL chart for the talent pipeline.

Why a funnel (not a Sankey)?
  A Sankey/alluvial diagram exists to show flows that BRANCH and MERGE
  (multiple sources -> multiple destinations). This dataset is a single
  linear path with attrition: one cohort narrows stage by stage
  (Grassroots -> Club -> State -> National -> Elite, 40,952 -> 20).
  The textbook idiom for sequential-stage attrition / conversion is the
  FUNNEL chart (sales funnels, recruitment pipelines). The key insight is
  the drop-off (advance) rate between consecutive stages.

Scale note: the cohort spans ~2,000:1, which collapses a linear-width
  funnel. Bar width is therefore SQRT-scaled (a standard perceptual
  compromise) and disclosed in the caption. Stage order top->bottom.

Reads:  data/talent_pipeline.csv
Writes: data/funnel_stages.csv   centred trapezoid bands (x,x2 per row)
        data/funnel_labels.csv   advance-rate labels between stages
Run: python3 scripts/build_funnel.py
"""

import csv, math, os

DATA_DIR = os.path.join(os.path.dirname(__file__), '..', 'data')

with open(os.path.join(DATA_DIR, 'talent_pipeline.csv')) as f:
    rows = list(csv.DictReader(f))

# ── Canvas geometry ──────────────────────────────────────────────────────────
W        = 720
CX       = 360          # horizontal centre line
MAX_HALF = 320          # half-width of the widest (top) band
MIN_HALF = 26           # half-width floor so the tiniest tier stays visible
ROW_H    = 76           # vertical spacing between stage centres
TOP_Y    = 40           # y of the first (widest) band centre
BAND_H   = 54           # drawn height of each band

levels = [r['level'] for r in rows]
labels = [r['program'] for r in rows]
counts = [int(r['estimated_players']) for r in rows]
n      = len(rows)
max_c  = counts[0]


def half_width(count):
    return max(MIN_HALF, math.sqrt(count / max_c) * MAX_HALF)


# ── Stage bands ───────────────────────────────────────────────────────────────
stages = []
cys = []
for i in range(n):
    hw = half_width(counts[i])
    cy = TOP_Y + i * ROW_H
    cys.append(cy)
    stages.append({
        'level': levels[i], 'label': labels[i], 'count': counts[i],
        'order': i,
        'next_level_pct': round(counts[i + 1] / counts[i] * 100, 1) if i < n - 1 else '',
        'cy': cy,
        'y':  round(cy - BAND_H / 2, 1),
        'y2': round(cy + BAND_H / 2, 1),
        'x':  round(CX - hw, 1),
        'x2': round(CX + hw, 1),
        'cx': CX,
        'label_y': cy,                       # stage name + count sit on centre line
    })

# ── Advance-rate labels: sit in the gap between consecutive bands ──────────────
gap_labels = []
for i in range(n - 1):
    pct = round(counts[i + 1] / counts[i] * 100, 1)
    gap_labels.append({
        'x': CX,
        'y': round((cys[i] + cys[i + 1]) / 2, 1),
        'advance_pct': pct,
        'label': f"▼ {pct}% advance",
    })

# ── Write ──────────────────────────────────────────────────────────────────────
with open(os.path.join(DATA_DIR, 'funnel_stages.csv'), 'w', newline='') as f:
    w = csv.DictWriter(f, fieldnames=['level', 'label', 'count', 'order',
                                      'next_level_pct', 'cy', 'y', 'y2',
                                      'x', 'x2', 'cx', 'label_y'])
    w.writeheader(); w.writerows(stages)

with open(os.path.join(DATA_DIR, 'funnel_labels.csv'), 'w', newline='') as f:
    w = csv.DictWriter(f, fieldnames=['x', 'y', 'advance_pct', 'label'])
    w.writeheader(); w.writerows(gap_labels)

print(f"✓ funnel_stages.csv ({len(stages)} stages)")
print(f"✓ funnel_labels.csv ({len(gap_labels)} labels)")
for s in stages:
    print(f"  {s['level']:<11} {s['count']:>6}  w={s['x2']-s['x']:.0f}px  next={s['next_level_pct']}%")
