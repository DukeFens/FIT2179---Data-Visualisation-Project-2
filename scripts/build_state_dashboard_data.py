#!/usr/bin/env python3
"""Build enriched state dashboard CSV for Figure 4 interactive map + charts."""

import csv
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"

STATES = {
    "NSW": ("New South Wales", 8.4),
    "VIC": ("Victoria", 6.7),
    "QLD": ("Queensland", 5.5),
    "WA": ("Western Australia", 2.9),
    "SA": ("South Australia", 1.8),
    "ACT": ("Australian Capital Territory", 0.46),
    "TAS": ("Tasmania", 0.57),
    "NT": ("Northern Territory", 0.25),
}

PERIOD_FOR_YEAR = {
    **{y: "Pre-COVID (2016–19)" for y in range(2016, 2020)},
    **{y: "COVID era (2020–21)" for y in (2020, 2021)},
    **{y: "Recovery (2022–24)" for y in range(2022, 2025)},
    2025: "Recovery (2022–24)",
}


def rate_pct(participants_k: float, pop_m: float) -> float:
    return round(participants_k / (pop_m * 10), 2)


def load_rows():
    rows = []
    with open(DATA / "ausplay_state_by_year.csv", newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            code = row["state"]
            name, pop = STATES[code]
            participants = float(row["participants_thousands"])
            rows.append(
                {
                    "year": int(row["year"]),
                    "state_code": code,
                    "state_name": name,
                    "participants_thousands": participants,
                    "participation_rate_pct": rate_pct(participants, pop),
                    "population_millions": pop,
                    "estimated": row["estimated"],
                }
            )

    with open(DATA / "australia_badminton_participation_by_state.csv", newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            code = row["state_code"]
            name, pop = STATES[code]
            participants = float(row["total_participants_thousands"])
            rows.append(
                {
                    "year": int(row["year"]),
                    "state_code": code,
                    "state_name": name,
                    "participants_thousands": participants,
                    "participation_rate_pct": float(row["participation_rate_pct"]),
                    "population_millions": pop,
                    "registered_clubs": int(row["registered_clubs"]),
                    "players_per_thousand": round(participants / pop, 1),
                    "estimated": "False",
                }
            )
    return rows


def add_derived(rows):
    by_year = defaultdict(list)
    for row in rows:
        by_year[row["year"]].append(row)

    national_avg = {}
    for year, year_rows in by_year.items():
        total_p = sum(r["participants_thousands"] for r in year_rows)
        total_pop = sum(r["population_millions"] for r in year_rows)
        national_avg[year] = round(total_p / (total_pop * 10), 2)

    for year, year_rows in by_year.items():
        ranked = sorted(
            year_rows,
            key=lambda r: r["participation_rate_pct"],
            reverse=True,
        )
        rank_map = {r["state_code"]: i + 1 for i, r in enumerate(ranked)}
        for row in year_rows:
            row["rank"] = rank_map[row["state_code"]]
            row["national_avg_rate_pct"] = national_avg[year]
            row["period"] = PERIOD_FOR_YEAR[row["year"]]
            if "players_per_thousand" not in row:
                row["players_per_thousand"] = round(
                    row["participants_thousands"] / row["population_millions"], 1
                )
            if "registered_clubs" not in row:
                row["registered_clubs"] = ""
    return rows


def write_dashboard(rows):
    fieldnames = [
        "year",
        "state_code",
        "state_name",
        "participants_thousands",
        "participation_rate_pct",
        "rank",
        "period",
        "population_millions",
        "players_per_thousand",
        "registered_clubs",
        "national_avg_rate_pct",
        "estimated",
    ]
    rows.sort(key=lambda r: (r["year"], r["state_code"]))
    out = DATA / "ausplay_state_dashboard.csv"
    with open(out, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    print(f"Wrote {len(rows)} rows → {out}")


def write_map_centroids():
    """Map overlay circles — replaces standalone cartogram (Fig 5)."""
    centroids = [
        ("NSW", "New South Wales", 146.5, -32.0),
        ("VIC", "Victoria", 143.8, -36.8),
        ("QLD", "Queensland", 143.5, -22.5),
        ("WA", "Western Australia", 121.5, -26.0),
        ("SA", "South Australia", 135.5, -30.0),
        ("TAS", "Tasmania", 146.5, -42.5),
        ("ACT", "Australian Capital Territory", 149.0, -35.5),
        ("NT", "Northern Territory", 133.5, -19.5),
    ]
    latest = {}
    with open(DATA / "australia_badminton_participation_by_state.csv", newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            latest[row["state_code"]] = row

    out = DATA / "state_map_overlay.csv"
    with open(out, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=[
                "state_code",
                "state_name",
                "lon",
                "lat",
                "participants_thousands",
                "participation_rate_pct",
                "players_per_thousand",
                "registered_clubs",
            ],
        )
        writer.writeheader()
        for code, name, lon, lat in centroids:
            row = latest[code]
            pop = STATES[code][1]
            participants = float(row["total_participants_thousands"])
            writer.writerow(
                {
                    "state_code": code,
                    "state_name": name,
                    "lon": lon,
                    "lat": lat,
                    "participants_thousands": participants,
                    "participation_rate_pct": float(row["participation_rate_pct"]),
                    "players_per_thousand": round(participants / pop, 1),
                    "registered_clubs": int(row["registered_clubs"]),
                }
            )
    print(f"Wrote map overlay → {out}")


if __name__ == "__main__":
    write_dashboard(add_derived(load_rows()))
    write_map_centroids()
