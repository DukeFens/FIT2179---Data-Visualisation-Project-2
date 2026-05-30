import json

def signed_area(ring):
    area = 0.0
    for i in range(len(ring) - 1):
        area += ring[i][0] * ring[i+1][1] - ring[i+1][0] * ring[i][1]
    # Add the last segment connecting back to the first
    area += ring[-1][0] * ring[0][1] - ring[0][0] * ring[-1][1]
    return 0.5 * area

with open('data/aus_states_mainland.geojson') as f:
    data = json.load(f)

for feat in data['features']:
    geom = feat['geometry']
    state = feat['properties']['STATE_NAME']
    
    if geom['type'] == 'MultiPolygon':
        areas = [signed_area(poly[0]) for poly in geom['coordinates']]
        cw = sum(1 for a in areas if a < 0)
        ccw = sum(1 for a in areas if a > 0)
        print(f"{state}: {len(areas)} polys -> {cw} CW, {ccw} CCW")
    elif geom['type'] == 'Polygon':
        a = signed_area(geom['coordinates'][0])
        print(f"{state}: 1 poly -> {'CW' if a < 0 else 'CCW'} (area {a})")
