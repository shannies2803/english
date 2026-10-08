#!/usr/bin/env python3
"""Write the 587 new explanations back into the source content files."""
import json, pathlib, glob, collections

tips = {}
for line in open("tips/ALL.txt", encoding="utf-8"):
    if not line.strip(): continue
    L, n, t = line.rstrip("\n").split("|", 2)
    tips[(L.strip(), int(n))] = t.strip()

# which source file holds which set letter?
applied, byfile = 0, collections.Counter()
for fn in sorted(glob.glob("content_*.json")):
    d = json.loads(pathlib.Path(fn).read_text(encoding="utf-8"))
    changed = False
    def walk(sets):
        global changed, applied
        for s in sets:
            L = s.get("letter")
            if not L: continue
            for q in s.get("questions", []):
                key = (L, q.get("n"))
                if key in tips and not (q.get("tip") or "").strip():
                    q["tip"] = tips[key]; applied += 1; byfile[fn] += 1; changed = True
    if isinstance(d, dict):
        if "sets" in d: walk(d["sets"])
        for k, v in d.items():
            if isinstance(v, list) and v and isinstance(v[0], dict) and "questions" in v[0]:
                walk(v)
            elif isinstance(v, dict) and "questions" in v:
                walk([v])
    if changed:
        pathlib.Path(fn).write_text(json.dumps(d, ensure_ascii=False), encoding="utf-8")
print(f"applied {applied} explanations to source content files")
for f, n in byfile.most_common(): print(f"  {f:34s} {n:4d}")
print(f"  still unplaced: {len(tips) - applied}")
