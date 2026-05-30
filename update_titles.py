import json
import os

updates = {
    "chart2_health_matrix.json": {
        "text": "Life-expectancy gains vs. sedentary peers",
        "subtitle": "The social dimension of racket sports appears to drive the outsized longevity benefit."
    },
    "chart3_calorie_bar.json": {
        "text": "Energy expenditure per hour",
        "subtitle": "Based on a 70-kg adult."
    },
    "chart1_muscle_body_map.json": {
        "text": "Muscle activation intensity during a forehand smash",
        "subtitle": "Darker green = higher activation (% MVIC)."
    },
    "chart4_longitudinal_growth.json": {
        "text": "National adult participation by gender, 2016–2025",
        "subtitle": "Area band = gap between male and female participation; dashed line = 2024 methodology revision."
    },
    "chart5_demographic_heatmap.json": {
        "text": "Participation by age group and gender",
        "subtitle": "The young-adult skew is consistent across years but intensifying."
    },
    "chart_city_paired.json": {
        "text": "Badminton courts by Greater Melbourne LGA",
        "subtitle": "Circle size = number of courts; shade = Asian-born residents (%)."
    },
    "chart10_melbourne_venues.json": {
        "text": "Asian-born population vs. badminton courts by LGA",
        "subtitle": "Dot size = LGA population; trend line shows positive correlation."
    },
    "chart6_talent_pipeline.json": {
        "text": "Talent pipeline drop-off across competitive tiers",
        "subtitle": "Logarithmic scale showing the narrowing path to elite representation."
    },
    "chart_adjacency_matrix.json": {
        "text": "Australian Open titles by nation, 2010–2024",
        "subtitle": "Use the dropdown to filter by discipline."
    },
    "chart9_elite_rankings.json": {
        "text": "BWF world ranking trajectories, 2022–2025",
        "subtitle": "Lower values = higher rankings; highlights top Australian players."
    },
    "chart8_tournament_density.json": {
        "text": "Australian-hosted BWF events, 2016–2025",
        "subtitle": "Bubble size = total entries; colour = tournament grade."
    }
}

title_template = {
    "anchor": "start",
    "fontSize": 13,
    "subtitleFontSize": 10,
    "color": "#172821",
    "subtitleColor": "#506158",
    "offset": 8
}

for filename, title_data in updates.items():
    filepath = os.path.join("vega-lite", filename)
    if os.path.exists(filepath):
        with open(filepath, "r") as f:
            data = json.load(f)
        
        # Merge the new title data into the template
        new_title = title_template.copy()
        new_title["text"] = title_data["text"]
        new_title["subtitle"] = title_data["subtitle"]
        
        # In chart1_muscle_body_map.json, it might be an hconcat or vconcat. Let's check root first.
        # Most of them are single view, so putting title at root is fine.
        data["title"] = new_title
        
        with open(filepath, "w") as f:
            json.dump(data, f, indent=2)
            
print("Done updating titles.")
