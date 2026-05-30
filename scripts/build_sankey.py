"""
scripts/build_sankey.py
Precomputes Sankey node rectangles + ribbon bands for the talent pipeline.
Reads:  data/talent_pipeline.csv
Writes: data/sankey_nodes.csv, data/sankey_links.csv
Run:    python3 scripts/build_sankey.py
"""

import csv, json, os

# ── Load source data ──────────────────────────────────────────────────────────
DATA_DIR = os.path.join(os.path.dirname(__file__), '..', 'data')

with open(os.path.join(DATA_DIR, 'talent_pipeline.csv')) as f:
    rows = list(csv.DictReader(f))

# Expected columns: stage, count, next_level_pct, label
# e.g. Grassroots, 40000, 12, "40,000 recreational players"

CHART_W = 700   # Vega-Lite container width (approx)
CHART_H = 320
NODE_W  = 28    # width of each Sankey node rectangle
GAP     = 0     # gap between stages (% of total height reserved for gaps)

stages = rows  # already ordered in the CSV

# ── Compute cumulative flow ───────────────────────────────────────────────────
counts = [float(r['count']) for r in stages]
max_count = counts[0]

# x positions: evenly spaced across the chart width
n = len(stages)
xs = [NODE_W/2 + i * (CHART_W - NODE_W) / (n - 1) for i in range(n)]

# y positions: node height proportional to count; centred vertically
def node_height(count, scale=CHART_H * 0.85):
    return max(4, count / max_count * scale)

nodes = []
for i, (row, x, count) in enumerate(zip(stages, xs, counts)):
    h = node_height(count)
    y_mid = CHART_H / 2
    nodes.append({
        'stage_index': i,
        'stage':       row['stage'],
        'label':       row.get('label', row['stage']),
        'count':       int(count),
        'x':           round(x, 1),
        'y':           round(y_mid - h/2, 1),
        'x2':          round(x + NODE_W, 1),
        'y2':          round(y_mid + h/2, 1),
        'height':      round(h, 1),
    })

# ── Compute ribbon bands (one per consecutive stage pair) ────────────────────
links = []
for i in range(len(nodes) - 1):
    src = nodes[i]
    dst = nodes[i+1]
    # ribbon spans from right edge of source to left edge of destination
    # y-extent determined by the smaller of the two nodes (flow = exit count)
    flow_count = dst['count']
    flow_frac  = flow_count / max_count
    band_h     = flow_frac * (CHART_H * 0.85)
    y_mid      = CHART_H / 2
    links.append({
        'link_index':  i,
        'source':      src['stage'],
        'target':      dst['stage'],
        'flow_count':  flow_count,
        'x':           src['x2'],           # right edge of source node
        'x2':          dst['x'],            # left edge of target node
        'y':           round(y_mid - band_h/2, 1),
        'y2':          round(y_mid + band_h/2, 1),
    })

# ── Write outputs ─────────────────────────────────────────────────────────────
nodes_path = os.path.join(DATA_DIR, 'sankey_nodes.csv')
links_path = os.path.join(DATA_DIR, 'sankey_links.csv')

with open(nodes_path, 'w', newline='') as f:
    w = csv.DictWriter(f, fieldnames=nodes[0].keys())
    w.writeheader(); w.writerows(nodes)

with open(links_path, 'w', newline='') as f:
    w = csv.DictWriter(f, fieldnames=links[0].keys())
    w.writeheader(); w.writerows(links)

print(f"✓ sankey_nodes.csv  ({len(nodes)} nodes)")
print(f"✓ sankey_links.csv  ({len(links)} links)")
