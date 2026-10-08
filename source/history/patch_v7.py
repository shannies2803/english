#!/usr/bin/env python3
"""Wire all v7 content into the merge script."""
import pathlib, sys
p = pathlib.Path("merge_content.py"); src = p.read_text(encoding="utf-8")

def sub(old, new, label):
    global src
    if src.count(old) != 1:
        sys.exit(f"anchor not found ({src.count(old)}x): {label}")
    src = src.replace(old, new)
    print("  ok:", label)

# 1 ── load the new drill files
sub('v6gram = json.loads((SRC / "content_v6_grammar.json").read_text(encoding="utf-8"))\n'
    'drills["sets"] += (v3drills["sets"] + v4young["sets"] + v4vocab["sets"]\n'
    '                   + v6vocab["sets"] + v6gram["sets"])',
    'v6gram = json.loads((SRC / "content_v6_grammar.json").read_text(encoding="utf-8"))\n'
    'v7gram = json.loads((SRC / "content_v7_grammar.json").read_text(encoding="utf-8"))\n'
    'v7vocab = json.loads((SRC / "content_v7_vocab.json").read_text(encoding="utf-8"))\n'
    'drills["sets"] += (v3drills["sets"] + v4young["sets"] + v4vocab["sets"]\n'
    '                   + v6vocab["sets"] + v6gram["sets"]\n'
    '                   + v7gram["sets"] + v7vocab["sets"])',
    "load v7 grammar + vocab")

# 2 ── new cloze sets are multi-passage
sub('MULTI_PASSAGE = {"secY", "secZE", "secZF", "graGA11"}',
    'MULTI_PASSAGE = {"secY", "secZE", "secZF", "graGA11", "g7GA23", "v7VA17", "clzA"}',
    "MULTI_PASSAGE")

# 3 ── comprehension: add the v7 passages and the new cloze set
sub('v3comp = json.loads((SRC / "content_v3_comprehension.json").read_text(encoding="utf-8"))\n'
    'comp["passages"] += extra2["passages"] + v3comp["passages"] + v4young["passages"]',
    'v3comp = json.loads((SRC / "content_v3_comprehension.json").read_text(encoding="utf-8"))\n'
    'v7comp = json.loads((SRC / "content_v7_comprehension.json").read_text(encoding="utf-8"))\n'
    'comp["passages"] += (extra2["passages"] + v3comp["passages"] + v4young["passages"]\n'
    '                     + v7comp["passages"])',
    "load v7 comprehension passages")

# 4 ── the two-passage comprehension cloze joins the drill bank
sub('# ---------- drills ----------',
    'drills["sets"] += v7comp["clozeSets"]\n\n'
    '# ---------- drills ----------',
    "v7 comprehension cloze into drills")

# 5 ── four more visual texts + listening paper 4
sub('lis3 = v3comp["listening3"]\n'
    'build_listening(lis3, "listen3", "L3")',
    'lis3 = v3comp["listening3"]\n'
    'build_listening(lis3, "listen3", "L3")\n'
    'v7vl = json.loads((SRC / "content_v7_visual_listening.json").read_text(encoding="utf-8"))\n'
    'lis4 = v7vl["listening4"]\n'
    'build_listening(lis4, "listen4", "L4")\n'
    'for vi, vv in enumerate(v7vl["visualTexts"], 8):\n'
    '    for q in vv["questions"]:\n'
    '        q["a"] = [q["options"][q["correct"]]]; q["m"] = q["a"][0]; q.setdefault("tip", "")\n'
    '    bank.append({"id": vv["id"], "letter": f"V{vi}", "title": f\'Visual text · {vv["title"]}\',\n'
    '                 "level": vv["level"], "mode": "mcq", "visual": vv["html"],\n'
    '                 "questions": vv["questions"]})',
    "listening paper 4 + visual texts V8–V11")

# 6 ── writing and oral: second situational set, second P3 composition set,
#      three more stimuli, four more read-aloud passages
sub('oral["conversation"] += v3wo["oral"]\n'
    'oral["readAloud"] += v4wr["readAloud"]',
    'v7wo = json.loads((SRC / "content_v7_writing_oral.json").read_text(encoding="utf-8"))\n'
    'oral["conversation"] += v3wo["oral"] + v7wo["oral2"]\n'
    'oral["readAloud"] += v4wr["readAloud"] + v7wo["readAloud2"]',
    "load v7 writing/oral")

sub('    "id": "readaloud", "letter": "RA", "title": "Reading aloud · 8 passages", "level": "P4",',
    '    "id": "readaloud", "letter": "RA", "title": "Reading aloud · 12 passages", "level": "P4",',
    "read-aloud title")

# second P3 picture-composition set, built the same way as the first
sub('# ---------- printable P3–P4 composition document ----------',
    'p3d = v7wo["compositionP3b"]\n'
    'bank.append({\n'
    '    "id": p3d["id"], "letter": p3d["letter"], "title": p3d["title"], "level": p3d["level"],\n'
    '    "mode": "compose", "criteria": p3c["criteria"], "instruction": p3d["instruction"],\n'
    '    "questions": [{"n": t["n"], "q": t["title"], "m": t["model"], "a": [t["model"]],\n'
    '                   "marks": 20, "kind": f\'Picture composition · {t["theme"]}\',\n'
    '                   "pac": p3d["helper"], "why": t["why"],\n'
    '                   "pictures": t["pictures"]}\n'
    '                  for t in p3d["tasks"]]\n'
    '})\n\n'
    '# ---------- printable P3–P4 composition document ----------',
    "second P3 composition set (CJ2)")

# second situational writing set
sub('# ---------- printable situational writing document ----------',
    'sw2 = v7wo["situational2"]\n'
    'bank.append({\n'
    '    "id": sw2["id"], "letter": sw2["letter"], "title": sw2["title"], "level": sw2["level"],\n'
    '    "mode": "compose", "criteria": sw["criteria"],\n'
    '    "questions": [{"n": t["n"], "q": t["task"], "m": t["model"], "a": [t["model"]],\n'
    '                   "kind": t["kind"], "pac": t["pac"], "why": t["why"], "marks": 15}\n'
    '                  for t in sw2["tasks"]]\n'
    '})\n\n'
    '# ---------- printable situational writing document ----------',
    "second situational set (SW2)")

# 7 ── listening script document gains paper 4
sub('               "\\n\\n" + script_doc(lis3, "Listening Comprehension — Reader\'s Script, Paper 3")]',
    '               "\\n\\n" + script_doc(lis3, "Listening Comprehension — Reader\'s Script, Paper 3"), "",\n'
    '               "\\n\\n" + script_doc(lis4, "Listening Comprehension — Reader\'s Script, Paper 4")]',
    "listening script doc paper 4")

# 8 ── groups
sub('                               + [f"GA{i}" for i in range(1, 13)],',
    '                               + [f"GA{i}" for i in range(1, 24)],',
    "grammar group GA1–GA23")
sub('                  + [f"VA{i}" for i in range(1, 11)],',
    '                  + [f"VA{i}" for i in range(1, 19)],',
    "vocabulary group VA1–VA18")
sub('    "Comprehension": ["R", "Y", "Z6"] + [f"C{i}" for i in range(1, 15)],',
    '    "Comprehension": ["R", "Y", "Z6", "Z7"] + [f"C{i}" for i in range(1, 21)],',
    "comprehension group C1–C20 + Z7")
sub('    "Visual text & listening": [f"V{i}" for i in range(1, 8)] + ["L1", "L2", "L3"],',
    '    "Visual text & listening": [f"V{i}" for i in range(1, 12)] + ["L1", "L2", "L3", "L4"],',
    "visual/listening group V1–V11 + L4")
sub('    "Writing": ["SW", "CP", "CJ"],',
    '    "Writing": ["SW", "SW2", "CP", "CJ", "CJ2"],',
    "writing group")
sub('    "Oral": [f"O{i}" for i in range(1, 7)] + ["RA"],',
    '    "Oral": [f"O{i}" for i in range(1, 10)] + ["RA"],',
    "oral group O1–O9")

p.write_text(src, encoding="utf-8")
print("merge_content.py patched")
