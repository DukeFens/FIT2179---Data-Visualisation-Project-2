import json

with open('data/aus_states_mainland.geojson') as f:
    data = json.load(f)

for feat in data['features']:
    geom = feat['geometry']
    print(f"{feat['properties']['STATE_NAME']}: {geom['type']}")
    if geom['type'] == 'MultiPolygon':
        print(f"  First poly depth: {len(geom['coordinates'][0])}")
        print(f"  First ring length: {len(geom['coordinates'][0][0])}")
        print(f"  First pt: {geom['coordinates'][0][0][0]}")
    elif geom['type'] == 'Polygon':
        print(f"  Depth: {len(geom['coordinates'])}")
        print(f"  First ring length: {len(geom['coordinates'][0])}")
        print(f"  First pt: {geom['coordinates'][0][0]}")
