#!/usr/bin/env python3
"""Clean Melbourne LGA GeoJSON and build centroid lookup CSV."""

import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GEO_PATH = ROOT / "data" / "melbourne_lga_boundaries.geojson"
MERGED_PATH = ROOT / "data" / "melbourne_lga_merged.csv"
CENTROID_PATH = ROOT / "data" / "melbourne_lga_centroids.csv"


def ring_centroid(ring):
    xs = [p[0] for p in ring]
    ys = [p[1] for p in ring]
    return sum(xs) / len(xs), sum(ys) / len(ys)


def valid_ring(ring):
    return isinstance(ring, list) and len(ring) >= 4


def clean_geometry(geom):
    gtype = geom["type"]
    if gtype == "Polygon":
        rings = [ring for ring in geom["coordinates"] if valid_ring(ring)]
        if not rings:
            return None
        return {"type": "Polygon", "coordinates": rings}
    if gtype == "MultiPolygon":
        polys = []
        for poly in geom["coordinates"]:
            if not poly:
                continue
            outer = poly[0]
            if valid_ring(outer):
                polys.append([outer])
        if not polys:
            return None
        if len(polys) == 1:
            return {"type": "Polygon", "coordinates": polys[0]}
        return {"type": "MultiPolygon", "coordinates": polys}
    return None


def main():
    with open(GEO_PATH, encoding="utf-8") as f:
        data = json.load(f)

    merged = {}
    with open(MERGED_PATH, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            merged[row["lga"]] = row

    cleaned = []
    centroids = []
    for feat in data["features"]:
        geom = clean_geometry(feat["geometry"])
        if geom is None:
            continue
        lga = feat["properties"]["LGA_NAME_2021"]
        cleaned.append(
            {
                "type": "Feature",
                "properties": feat["properties"],
                "geometry": geom,
            }
        )
        if geom["type"] == "Polygon":
            lon, lat = ring_centroid(geom["coordinates"][0])
        else:
            lon, lat = ring_centroid(geom["coordinates"][0][0])
        row = merged.get(lga, {})
        centroids.append(
            {
                "lga": lga,
                "lon": round(lon, 5),
                "lat": round(lat, 5),
                "courts": int(float(row["courts"])) if row.get("courts") else 0,
                "asian_born_pct": float(row["asian_born_pct"]) if row.get("asian_born_pct") else 0.0,
            }
        )

    out = {"type": "FeatureCollection", "features": cleaned}
    with open(GEO_PATH, "w", encoding="utf-8") as f:
        json.dump(out, f)

    with open(CENTROID_PATH, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(
            f, fieldnames=["lga", "lon", "lat", "courts", "asian_born_pct"]
        )
        writer.writeheader()
        writer.writerows(centroids)

    print(f"Cleaned {len(cleaned)} LGA features → {GEO_PATH.name}")
    print(f"Wrote {len(centroids)} centroids → {CENTROID_PATH.name}")


if __name__ == "__main__":
    main()
