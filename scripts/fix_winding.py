import json

def signed_area(ring):
    area = 0.0
    for i in range(len(ring) - 1):
        area += ring[i][0] * ring[i+1][1] - ring[i+1][0] * ring[i][1]
    area += ring[-1][0] * ring[0][1] - ring[0][0] * ring[-1][1]
    return 0.5 * area

with open('data/aus_states_mainland.geojson') as f:
    data = json.load(f)

for feat in data['features']:
    geom = feat['geometry']
    
    if geom['type'] == 'MultiPolygon':
        for poly in geom['coordinates']:
            ring = poly[0]
            if signed_area(ring) > 0:
                # CCW -> CW
                poly[0] = ring[::-1]
    elif geom['type'] == 'Polygon':
        ring = geom['coordinates'][0]
        if signed_area(ring) > 0:
            geom['coordinates'][0] = ring[::-1]

with open('data/aus_states_mainland.geojson', 'w') as f:
    json.dump(data, f)
