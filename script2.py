import json
dx, dy = 100, 15  # ĐỔI 2 SỐ NÀY
with open('data/muscle_regions_backup.geojson') as f: g = json.load(f)
def t(c):
    if isinstance(c[0],(int,float)): return [round(c[0]+dx,2), round(c[1]+dy,2)]
    return [t(s) for s in c]
for feat in g['features']: feat['geometry']['coordinates'] = t(feat['geometry']['coordinates'])
with open('data/muscle_regions.geojson','w') as f: json.dump(g, f)
print(f'Shifted dx={dx}, dy={dy}. Refresh browser.')