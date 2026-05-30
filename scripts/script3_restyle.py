"""
Editorial restyle of the 10 Vega-Lite chart specs.
Run once to convert the corporate teal/gold/red charts to a unified
muted-red editorial palette inspired by FT / Bloomberg / NYT graphics.
"""

import json
import os
import re
from pathlib import Path

ROOT = Path(__file__).parent / "vega-lite"

# Editorial palette  ---------------------------------------------------------
INK         = "#14110F"
INK_SOFT    = "#3A3633"
INK_MUTE    = "#7A736D"
INK_FAINT   = "#B8B1AB"
RULE        = "#E5E0D8"
RULE_SOFT   = "#EFEBE3"
BG          = "#F5F0E8"            # warm cream, matches body
ACCENT      = "#B23A2F"            # shuttle red (primary)
ACCENT_DEEP = "#7F2820"            # deepest
ACCENT_MID  = "#D9826E"            # terracotta
ACCENT_SOFT = "#E8B7B0"
ACCENT_WASH = "#F6E6E2"

# Color swap table — replace any of these colours with editorial equivalent.
COLOR_MAP = {
    # teal family → deep red (primary accent)
    "#1E5F74": ACCENT_DEEP,
    "#2B88A1": ACCENT,
    "#1B5366": ACCENT_DEEP,
    "#EAF4F8": ACCENT_WASH,
    "#C8D8E0": INK_FAINT,
    "#C8E6F5": ACCENT_WASH,
    # gold family → terracotta or neutral
    "#F5A623": ACCENT_MID,
    "#FEF6E6": ACCENT_WASH,
    "#C47A00": ACCENT_DEEP,
    # red family → deepen
    "#D94F35": ACCENT,
    "#B03525": ACCENT_DEEP,
    "#E63946": ACCENT,
    "#D9534F": ACCENT,
    # generic neutrals from old design
    "#F7F4EF": BG,
    "#DDD9D2": RULE,
    "#EEEAE4": RULE_SOFT,
    "#1A1A2E": INK,
    "#505060": INK_SOFT,
    "#8A8A9A": INK_MUTE,
    # whites that should now be background
    "white": BG,
    "#FFFFFF": BG,
    "#FFF": BG,
    "#EEEEEE": RULE_SOFT,
    "#EEE": RULE_SOFT,
}

# Editorial font for any inline font directive that survives
EDITORIAL_FONT = "Inter, 'Helvetica Neue', Arial, sans-serif"
EDITORIAL_SERIF = "Fraunces, Georgia, serif"


def deep_swap_colors(obj):
    """Recursively rewrite color strings + drop chart-level titles + tidy fonts."""
    if isinstance(obj, dict):
        new = {}
        for k, v in obj.items():
            # Strip embedded titles — titles now live in the HTML
            if k == "title" and isinstance(v, dict) and "text" in v:
                continue
            # Strip background — page background shows through
            if k == "background":
                new[k] = None
                continue
            # Strip font overrides — global config handles it
            if k == "font":
                new[k] = EDITORIAL_FONT
                continue
            new[k] = deep_swap_colors(v)
        return new
    if isinstance(obj, list):
        return [deep_swap_colors(x) for x in obj]
    if isinstance(obj, str):
        if obj in COLOR_MAP:
            return COLOR_MAP[obj]
        return obj
    return obj


def strip_chart_title_and_clean(spec):
    """Strip the top-level `title` block (we render titles in HTML)."""
    spec.pop("title", None)
    spec.pop("description", None)
    spec["background"] = None
    # Recursive color & font swap
    spec = deep_swap_colors(spec)
    # Compact, minimal padding
    spec.setdefault("padding", 4)
    return spec


# Per-chart custom overrides — applied AFTER the global swap.
def patch_chart1(spec):
    """Body map: keep red intensity gradient but match editorial palette."""
    for layer in spec.get("layer", []):
        enc = layer.get("encoding", {})
        # The color encoding for the muscle dots
        if "color" in enc and isinstance(enc["color"], dict):
            scale = enc["color"].get("scale", {})
            if "range" in scale:
                # Tonal red ramp
                scale["range"] = [ACCENT_WASH, ACCENT_SOFT, ACCENT_MID, ACCENT, ACCENT_DEEP]
            if "scheme" in scale:
                del scale["scheme"]
    return spec


def patch_chart2(spec):
    """Longevity lollipop — three sport categories on tonal scale."""
    new_range = [ACCENT_DEEP, INK_FAINT, ACCENT_MID]  # Racket, Aerobic, Team
    for layer in spec.get("layer", []):
        enc = layer.get("encoding", {})
        for ch in ("color",):
            if ch in enc and isinstance(enc[ch], dict):
                scale = enc[ch].get("scale", {})
                if "range" in scale:
                    scale["range"] = new_range
    return spec


def patch_chart3(spec):
    """Calorie bar — Badminton highlighted, others muted."""
    for layer in spec.get("layer", []):
        enc = layer.get("encoding", {})
        if "color" in enc and isinstance(enc["color"], dict):
            scale = enc["color"].get("scale", {})
            if "range" in scale and len(scale["range"]) == 2:
                scale["range"] = [ACCENT_DEEP, INK_FAINT]
    return spec


def patch_chart4(spec):
    """Choropleth — sequential red ramp."""
    for layer in spec.get("layer", []):
        enc = layer.get("encoding", {})
        if "color" in enc and isinstance(enc["color"], dict):
            scale = enc["color"].get("scale", {})
            if "range" in scale:
                scale["range"] = [ACCENT_WASH, ACCENT_MID, ACCENT, ACCENT_DEEP]
        # State labels should remain readable
    return spec


def patch_chart5(spec):
    """Participation trend — area + line, tonal red."""
    for layer in spec.get("layer", []):
        mark = layer.get("mark", {})
        if isinstance(mark, dict):
            if mark.get("type") == "area":
                mark["color"] = ACCENT
                mark["opacity"] = 0.18
            if mark.get("type") == "line":
                mark["color"] = ACCENT_DEEP
                mark["strokeWidth"] = 2.2
        enc = layer.get("encoding", {})
        if "color" in enc and isinstance(enc["color"], dict):
            scale = enc["color"].get("scale", {})
            if "range" in scale:
                scale["range"] = [ACCENT_DEEP, ACCENT_MID, INK_FAINT][:len(scale["range"])]
    return spec


def patch_chart6(spec):
    """Population pyramid — Male / Female tonal."""
    for layer in spec.get("layer", []):
        enc = layer.get("encoding", {})
        if "color" in enc and isinstance(enc["color"], dict):
            scale = enc["color"].get("scale", {})
            if "range" in scale and len(scale["range"]) >= 2:
                scale["range"] = [ACCENT_DEEP, ACCENT_MID] + scale["range"][2:]
    return spec


def patch_chart7(spec):
    """Melbourne venues — university vs other."""
    for layer in spec.get("layer", []):
        mark = layer.get("mark", {})
        # Background polygon should be pale neutral
        if isinstance(mark, dict) and mark.get("type") == "geoshape":
            mark["fill"] = RULE
            mark["stroke"] = BG
            mark["strokeWidth"] = 0.5
        enc = layer.get("encoding", {})
        if "color" in enc and isinstance(enc["color"], dict):
            scale = enc["color"].get("scale", {})
            if "range" in scale:
                # 2 categories
                if len(scale["range"]) == 2:
                    scale["range"] = [ACCENT_DEEP, INK_FAINT]
                else:
                    scale["range"] = [ACCENT_DEEP, ACCENT, ACCENT_MID, INK_FAINT][:len(scale["range"])]
    return spec


def patch_chart8(spec):
    """Talent pipeline — funnel with deepening reds toward the top."""
    for layer in spec.get("layer", []):
        enc = layer.get("encoding", {})
        if "color" in enc and isinstance(enc["color"], dict):
            scale = enc["color"].get("scale", {})
            if "range" in scale:
                # Replace any range with monotone red ramp
                scale["range"] = [ACCENT_DEEP, ACCENT, ACCENT_MID, ACCENT_SOFT][:max(2, len(scale["range"]))]
            if "scheme" in scale:
                del scale["scheme"]
    return spec


def patch_chart9(spec):
    """World rankings multiline — tonal palette across players."""
    palette = [ACCENT_DEEP, ACCENT, ACCENT_MID, ACCENT_SOFT, INK_FAINT, INK_MUTE]
    for layer in spec.get("layer", []):
        enc = layer.get("encoding", {})
        if "color" in enc and isinstance(enc["color"], dict):
            scale = enc["color"].get("scale", {})
            if "range" in scale:
                scale["range"] = palette[:len(scale["range"])]
            if "scheme" in scale:
                del scale["scheme"]
                scale["range"] = palette
    return spec


def patch_chart10(spec):
    """Tournament bubble — tier categories."""
    palette = [ACCENT_DEEP, ACCENT, ACCENT_MID, INK_FAINT]
    for layer in spec.get("layer", []):
        enc = layer.get("encoding", {})
        if "color" in enc and isinstance(enc["color"], dict):
            scale = enc["color"].get("scale", {})
            if "range" in scale:
                scale["range"] = palette[:len(scale["range"])]
    return spec


PATCHERS = {
    "chart1_muscle_body_map.json": patch_chart1,
    "chart2_longevity_lollipop.json": patch_chart2,
    "chart3_calorie_bar.json": patch_chart3,
    "chart4_choropleth_map.json": patch_chart4,
    "chart5_participation_trend.json": patch_chart5,
    "chart6_population_pyramid.json": patch_chart6,
    "chart7_melbourne_venues_map.json": patch_chart7,
    "chart8_talent_pipeline.json": patch_chart8,
    "chart9_rankings_multiline.json": patch_chart9,
    "chart10_tournament_bubble.json": patch_chart10,
}


def process_one(path: Path):
    raw = path.read_text(encoding="utf-8")
    spec = json.loads(raw)
    spec = strip_chart_title_and_clean(spec)
    patcher = PATCHERS.get(path.name)
    if patcher:
        spec = patcher(spec)
    # Standardise width/height: container width, modest height
    if spec.get("width") not in ("container",):
        if path.name == "chart1_muscle_body_map.json":
            # body map keeps fixed dims
            pass
        elif path.name in ("chart4_choropleth_map.json", "chart7_melbourne_venues_map.json"):
            spec["width"] = "container"
        else:
            spec["width"] = "container"
    if isinstance(spec.get("height"), int) and spec["height"] > 380:
        spec["height"] = 380
    # Remove embedded inline config — global config wins
    if "config" in spec:
        kept = {}
        # Only keep `view.stroke=null` and `legend.orient` overrides
        cfg = spec["config"]
        if isinstance(cfg, dict):
            if "view" in cfg:
                kept["view"] = {"stroke": None}
        spec["config"] = kept
    path.write_text(json.dumps(spec, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"  rewrote  {path.name}")


def main():
    print("Restyling Vega-Lite specs to editorial palette …")
    for f in sorted(ROOT.glob("chart*.json")):
        process_one(f)
    print("Done.")


if __name__ == "__main__":
    main()
