import json

with open('data/aus_states.geojson') as f:
    data = json.load(f)

def ring_centroid(ring):
    cx = sum(p[0] for p in ring) / len(ring)
    cy = sum(p[1] for p in ring) / len(ring)
    return cx, cy

def in_bounds(cx, cy, lon_min=108, lon_max=156, lat_min=-46, lat_max=-9):
    return lon_min <= cx <= lon_max and lat_min <= cy <= lat_max

filtered = []
for feat in data['features']:
    geom = feat['geometry']
    if geom['type'] == 'MultiPolygon':
        kept = []
        for poly in geom['coordinates']:
            outer_ring = poly[0]
            cx, cy = ring_centroid(outer_ring)
            if in_bounds(cx, cy):
                # KEEP ONLY THE OUTER RING (Remove holes)
                kept.append([outer_ring])
        if kept:
            f2 = dict(feat)
            f2['geometry'] = {**geom, 'coordinates': kept}
            filtered.append(f2)
    elif geom['type'] == 'Polygon':
        outer_ring = geom['coordinates'][0]
        cx, cy = ring_centroid(outer_ring)
        if in_bounds(cx, cy):
            # KEEP ONLY THE OUTER RING (Remove holes)
            f2 = dict(feat)
            f2['geometry'] = {**geom, 'coordinates': [outer_ring]}
            filtered.append(f2)

data['features'] = filtered

with open('data/aus_states_mainland.geojson', 'w') as f:
    json.dump(data, f)
