#!/usr/bin/env python3
"""Geometry check for the four-picture composition panels.

Screenshots are the only way to see whether a panel reads, but they are slow to
look at and easy to skim. These are the mistakes that showed up in the first
drafts and that a machine can find on its own:

  * two figures drawn so close that their bodies merge into one shape
  * anything drawn outside the 160x120 panel, or under the ground bar
  * a figure floating above the ground instead of standing on it
  * a panel with nothing in it but background and ground

Run it over any content file holding picture tasks. It does not judge whether a
drawing looks like what the caption says — only a person can do that.
"""
import json, re, sys, pathlib

GROUND_Y, W, H = 100, 160, 120
CIRC = re.compile(r"<circle cx='([-\d.]+)' cy='([-\d.]+)' r='([-\d.]+)' fill='(#[0-9A-Fa-f]{6})'")
RECT = re.compile(r"<rect x='([-\d.]+)' y='([-\d.]+)' width='([-\d.]+)' height='([-\d.]+)'[^>]*fill='(#[0-9A-Fa-f]{6})'")
FIGURE_COLOURS = {"#10786A", "#B4527A", "#E8865C", "#1F3C88"}
WOOD, PALE = "#A88B62", "#CBD5E3"

def check(path):
    data = json.loads(pathlib.Path(path).read_text(encoding="utf-8"))
    sets = []
    for v in data.values():
        sets += (v if isinstance(v, list) else [v])
    problems = []
    panels = 0
    for s in sets:
        for t in s.get("tasks", []):
            for pi, p in enumerate(t.get("pictures", []), 1):
                panels += 1
                svg, where = p["svg"], f'{s.get("id","?")} task {t["n"]} "{t["title"]}" panel {pi}'
                heads = [(float(a), float(b), float(c), d) for a, b, c, d in CIRC.findall(svg)
                         if d in FIGURE_COLOURS and float(c) >= 6]
                rects = [(float(a), float(b), float(c), float(d), e) for a, b, c, d, e in RECT.findall(svg)]
                bodies = [r for r in rects if r[4] in FIGURE_COLOURS and r[3] >= 15]

                if len(svg) < 260:
                    problems.append(f"{where}: almost nothing drawn ({len(svg)} chars)")

                # figures too close together
                for i in range(len(heads)):
                    for j in range(i + 1, len(heads)):
                        x1, y1, r1, _ = heads[i]; x2, y2, r2, _ = heads[j]
                        gap = abs(x1 - x2)
                        if gap < r1 + r2 + 4 and abs(y1 - y2) < 26:
                            problems.append(f"{where}: two figures only {gap:.0f}px apart — they will merge")
                for i in range(len(bodies)):
                    for j in range(i + 1, len(bodies)):
                        ax, ay, aw, ah, _ = bodies[i]; bx, by, bw, bh, _ = bodies[j]
                        if ax < bx + bw and bx < ax + aw and ay < by + bh and by < ay + bh:
                            problems.append(f"{where}: two figure bodies overlap")

                # out of bounds, and figures not standing on the ground
                for x, y, r, _ in heads:
                    if x - r < 0 or x + r > W or y - r < 0:
                        problems.append(f"{where}: a head sits outside the panel at ({x:.0f},{y:.0f})")
                for x, y, w, h, c in rects:
                    if x < -1 or y < -1 or x + w > W + 1 or y + h > H + 1:
                        problems.append(f"{where}: a shape runs off the panel at ({x:.0f},{y:.0f} {w:.0f}x{h:.0f})")
                # A figure need not reach the ground if it is standing or sitting on
                # something: a bench or table top, or a stair tread. Collect every
                # surface in the panel and let a figure land on any of them.
                surfaces = [GROUND_Y] + [y for x, y, w, h, c in rects
                                         if c in (WOOD, PALE) and w >= 8 and h <= 60]
                for x, y, w, h, c in bodies:
                    foot = y + h + 14          # body bottom plus a leg
                    if not any(sy - 10 <= foot <= sy + 16 for sy in surfaces):
                        near = min(surfaces, key=lambda sy: abs(sy - foot))
                        problems.append(f"{where}: a figure's feet land at y={foot:.0f} with no surface "
                                        f"there — nearest is y={near:.0f}")
    return panels, problems

if __name__ == "__main__":
    total, bad = 0, []
    for f in (sys.argv[1:] or ["content_v11_p3_composition.json"]):
        n, probs = check(f)
        total += n; bad += probs
    print(f"CHECKED {total} panels")
    for b in bad:
        print("  " + b)
    print(f"\n{len(bad)} problems")
    sys.exit(1 if bad else 0)
