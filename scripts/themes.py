#!/usr/bin/env python3
"""Export the graphic themes of Pipe Maze 3D as colour swatches for the website.

    scripts/themes.py [path/to/pipe_maze_3d]

Reads every theme ScriptableObject (Assets/App/Assets/Themes/ScriptableObjects/**/*.asset), follows
the background / pipe / player / flag material references and writes src/data/themes.json:
[{ "name", "family", "background": [colorA, colorB], "pipe", "player", "flag" }, ...]
"""
import glob
import json
import os
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
SITE = HERE.parent
PROJECT = Path(sys.argv[1]) if len(sys.argv) > 1 else Path.home() / "ghq/github.com/aureliendrouet/pipe_maze_3d"
THEMES = PROJECT / "Assets/App/Assets/Themes"
OUT = SITE / "src/data/themes.json"

ORDER = ["Default", "Elemental", "Food", "Game", "NextGen", "Paper", "Retro"]


def hex_color(text, key):
    m = re.search(r"- %s: \{r: ([\d.e-]+), g: ([\d.e-]+), b: ([\d.e-]+)" % re.escape(key), text)
    if not m:
        return None
    return "#%02x%02x%02x" % tuple(min(255, int(round(float(v) * 255))) for v in m.groups())


guid_to_material = {}
for meta in glob.glob(str(THEMES / "Materials/**/*.mat.meta"), recursive=True):
    guid = re.search(r"guid: (\w+)", open(meta).read()).group(1)
    guid_to_material[guid] = meta[:-5]

themes = []
for asset in glob.glob(str(THEMES / "ScriptableObjects/**/*.asset"), recursive=True):
    text = open(asset).read()
    rel = os.path.relpath(asset, THEMES / "ScriptableObjects")
    family = os.path.dirname(rel) or "Default"
    name = Path(asset).stem  # the `id` field is not unique (M-Io says P-Man), the file name is
    mats = {}
    for key in ("background", "pipe", "player", "flag"):
        ref = re.search(key + r": \{fileID: \d+, guid: (\w+)", text)
        mats[key] = open(guid_to_material[ref.group(1)]).read() if ref and ref.group(1) in guid_to_material else ""
    bg = mats["background"]
    themes.append({
        "name": name,
        "family": family,
        "background": [hex_color(bg, "_ColorA") or hex_color(bg, "_Color"), hex_color(bg, "_ColorB") or hex_color(bg, "_Color")],
        "pipe": hex_color(mats["pipe"], "_Color"),
        "player": hex_color(mats["player"], "_Color"),
        "flag": hex_color(mats["flag"], "_Color"),
    })

themes.sort(key=lambda t: (ORDER.index(t["family"]) if t["family"] in ORDER else 99, t["name"]))
OUT.parent.mkdir(parents=True, exist_ok=True)
OUT.write_text(json.dumps(themes, indent=2) + "\n")
print(f"{len(themes)} themes -> {OUT.relative_to(SITE)}")
