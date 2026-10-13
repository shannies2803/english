#!/usr/bin/env python3
"""Merge the parsed workbook bank with the new drill and comprehension content."""
import json, pathlib, re

SRC = pathlib.Path(__file__).parent
bank = json.loads((SRC / "questions.json").read_text(encoding="utf-8"))
drills = json.loads((SRC / "content_drills.json").read_text(encoding="utf-8"))
v3drills = json.loads((SRC / "content_v3_drills.json").read_text(encoding="utf-8"))
v4young = json.loads((SRC / "content_v4_younger.json").read_text(encoding="utf-8"))
v4vocab = json.loads((SRC / "content_v4_vocab.json").read_text(encoding="utf-8"))
v6vocab = json.loads((SRC / "content_v6_vocab.json").read_text(encoding="utf-8"))
v6gram = json.loads((SRC / "content_v6_grammar.json").read_text(encoding="utf-8"))
v7gram = json.loads((SRC / "content_v7_grammar.json").read_text(encoding="utf-8"))
v7vocab = json.loads((SRC / "content_v7_vocab.json").read_text(encoding="utf-8"))
v7comp = json.loads((SRC / "content_v7_comprehension.json").read_text(encoding="utf-8"))
v8gram = json.loads((SRC / "content_v8_grammar.json").read_text(encoding="utf-8"))
v8vocab = json.loads((SRC / "content_v8_vocab.json").read_text(encoding="utf-8"))
v9comp = json.loads((SRC / "content_v9_comprehension.json").read_text(encoding="utf-8"))
v9vl = json.loads((SRC / "content_v9_visual_listening.json").read_text(encoding="utf-8"))
v10comp = json.loads((SRC / "content_v10_comprehension.json").read_text(encoding="utf-8"))
v10vis = json.loads((SRC / "content_v10_visual.json").read_text(encoding="utf-8"))
v10oral = json.loads((SRC / "content_v10_oral.json").read_text(encoding="utf-8"))
v10wr = json.loads((SRC / "content_v10_writing.json").read_text(encoding="utf-8"))
v11or = json.loads((SRC / "content_v11_p3_oral.json").read_text(encoding="utf-8"))
drills["sets"] += (v3drills["sets"] + v4young["sets"] + v4vocab["sets"]
                   + v6vocab["sets"] + v6gram["sets"]
                   + v7gram["sets"] + v7vocab["sets"]
                   + v8gram["sets"] + v8vocab["sets"])
comp = json.loads((SRC / "content_comprehension.json").read_text(encoding="utf-8"))

# multi-passage cloze sets carry their blanks in a separate answers list
MULTI_PASSAGE = {"secY", "secZE", "secZF", "graGA11", "g7GA23", "v7VA17", "clzA"}

drills["sets"] += v7comp["clozeSets"]

# ---------- drills ----------
for s in drills["sets"]:
    if s["id"] in MULTI_PASSAGE:               # expand cloze passages into questions
        qs = []
        amap = {a["n"]: a for a in s["answers"]}
        for p in s["passages"]:
            for n in range(p["from"], p["to"] + 1):
                a = amap[n]
                qs.append({"n": n, "q": p["text"], "a": a["a"], "m": a["a"][0],
                           "tip": a.get("tip", ""), "blank": n})
        s = {k: v for k, v in s.items() if k not in ("passages", "answers")}
        s["questions"] = qs
    else:
        s["questions"] = [q for q in s["questions"] if not q.get("skip")]
        for q in s["questions"]:
            if s["mode"] == "mcq":
                q["a"] = [q["options"][q["correct"]]]
                q["m"] = q["options"][q["correct"]]
            elif "a" not in q:
                q["a"] = [q.get("m", "")]
            q.setdefault("m", q["a"][0])
    bank.append(s)

# ---------- comprehension ----------
extra2 = json.loads((SRC / "content_extra2.json").read_text(encoding="utf-8"))
v3comp = json.loads((SRC / "content_v3_comprehension.json").read_text(encoding="utf-8"))
comp["passages"] += (extra2["passages"] + v3comp["passages"] + v4young["passages"]
                     + v7comp["passages"] + v9comp["passages"] + v10comp["passages"])
for ci, p in enumerate(comp["passages"], 1):
    bank.append({
        "id": p["id"], "letter": f"C{ci}", "title": f'Comprehension · {p["title"]}',
        "level": p["level"], "mode": "read", "kind": p["kind"],
        "passage": p["text"],
        "questions": [{"n": q["n"], "q": q["q"], "a": [q["a"]], "m": q["a"],
                       "tip": q.get("tip", ""), "marks": q["marks"]} for q in p["questions"]]
    })

# ---------- visual text + listening ----------
vl = json.loads((SRC / "content_visual_listening.json").read_text(encoding="utf-8"))
for vi, v in enumerate(vl["visualTexts"], 1):
    for q in v["questions"]:
        q["a"] = [q["options"][q["correct"]]]
        q["m"] = q["options"][q["correct"]]
    bank.append({"id": v["id"], "letter": f"V{vi}", "title": f'Visual text · {v["title"]}',
                 "level": v["level"], "mode": "mcq", "visual": v["html"],
                 "questions": v["questions"]})

lis = vl["listening"]
scripts = {}
lq = []
for it in lis["items"]:
    if it.get("script"):
        scripts[it.get("passage") or it["n"]] = it["script"]
    q = {"n": it["n"], "q": it["q"], "options": it["options"], "correct": it["correct"],
         "a": [it["options"][it["correct"]]], "m": it["options"][it["correct"]],
         "script": it.get("script") or scripts.get(it.get("passage"), ""), "tip": ""}
    lq.append(q)
bank.append({"id": "listen1", "letter": "L1", "title": lis["title"], "level": "P5",
             "mode": "mcq", "listening": True, "instruction": lis["instructions"],
             "questions": lq})

def build_listening(spec, sid, letter):
    scripts, qs = {}, []
    for it in spec["items"]:
        if it.get("script"):
            scripts[it.get("passage") or it["n"]] = it["script"]
        qs.append({"n": it["n"], "q": it["q"], "options": it["options"], "correct": it["correct"],
                   "a": [it["options"][it["correct"]]], "m": it["options"][it["correct"]],
                   "script": it.get("script") or scripts.get(it.get("passage"), ""), "tip": ""})
    bank.append({"id": sid, "letter": letter, "title": spec["title"], "level": "P6",
                 "mode": "mcq", "listening": True, "instruction": spec["instructions"],
                 "questions": qs})

lis2 = json.loads((SRC / "content_extra2.json").read_text(encoding="utf-8"))["listening2"]
build_listening(lis2, "listen2", "L2")
lis3 = v3comp["listening3"]
build_listening(lis3, "listen3", "L3")
v7vl = json.loads((SRC / "content_v7_visual_listening.json").read_text(encoding="utf-8"))
lis4 = v7vl["listening4"]
build_listening(lis4, "listen4", "L4")
lis5 = v9vl["listening5"]
build_listening(lis5, "listen5", "L5")
for vi, vv in enumerate(v9vl["visualTexts"], 12):
    for q in vv["questions"]:
        q["a"] = [q["options"][q["correct"]]]; q["m"] = q["a"][0]; q.setdefault("tip", "")
    bank.append({"id": vv["id"], "letter": f"V{vi}", "title": f'Visual text · {vv["title"]}',
                 "level": vv["level"], "mode": "mcq", "visual": vv["html"],
                 "questions": vv["questions"]})
for vi, vv in enumerate(v7vl["visualTexts"], 8):
    for q in vv["questions"]:
        q["a"] = [q["options"][q["correct"]]]; q["m"] = q["a"][0]; q.setdefault("tip", "")
    bank.append({"id": vv["id"], "letter": f"V{vi}", "title": f'Visual text · {vv["title"]}',
                 "level": vv["level"], "mode": "mcq", "visual": vv["html"],
                 "questions": vv["questions"]})
for vi, vv in enumerate(v10vis["visualTexts"], 14):
    for q in vv["questions"]:
        q["a"] = [q["options"][q["correct"]]]; q["m"] = q["a"][0]; q.setdefault("tip", "")
    bank.append({"id": vv["id"], "letter": f"V{vi}", "title": f'Visual text · {vv["title"]}',
                 "level": vv["level"], "mode": "mcq", "visual": vv["html"],
                 "questions": vv["questions"]})

# two further visual texts, practice-only
for vi, vv in enumerate(v3comp["visualTexts"], 6):
    for q in vv["questions"]:
        q["a"] = [q["options"][q["correct"]]]; q["m"] = q["a"][0]; q.setdefault("tip", "")
    bank.append({"id": vv["id"], "letter": f"V{vi}", "title": f'Visual text · {vv["title"]}',
                 "level": vv["level"], "mode": "mcq", "visual": vv["html"],
                 "questions": vv["questions"]})

# ---------- mock paper ----------
paper = json.loads((SRC / "content_paper2.json").read_text(encoding="utf-8"))
vmap = {x["id"]: x for x in vl["visualTexts"]}
for sec in paper["sections"]:
    if sec.get("useVisual"):
        v = vmap[sec["visual"]]
        sec["visualHtml"] = v["html"]
        sec["questions"] = [dict(q) for q in v["questions"]]
    if sec["mode"] == "mcq":
        for q in sec["questions"]:
            q["a"] = [q["options"][q["correct"]]]
            q["m"] = q["options"][q["correct"]]
            q.setdefault("marks", 1)
    elif sec["mode"] in ("auto",):
        sec["questions"] = [{"n": a["n"], "q": sec["passage"], "a": a["a"], "m": a["a"][0],
                             "tip": a.get("tip", ""), "blank": a["n"], "marks": 1}
                            for a in sec["answers"]]
        sec.pop("answers", None)
    else:
        for q in sec["questions"]:
            q.setdefault("marks", 1)
            if "a" not in q:
                q["a"] = [q.get("m") or q.get("a")]
            elif isinstance(q["a"], str):
                q["m"] = q["a"]; q["a"] = [q["m"]]

# ---------- second paper + its visual text ----------
p2b = json.loads((SRC / "content_paper2b.json").read_text(encoding="utf-8"))
v = p2b["visualText"]
for q in v["questions"]:
    q["a"] = [q["options"][q["correct"]]]; q["m"] = q["a"][0]; q.setdefault("tip", "")
bank.append({"id": v["id"], "letter": "V4", "title": f'Visual text · {v["title"]}',
             "level": v["level"], "mode": "mcq", "visual": v["html"], "questions": v["questions"]})
vmap[v["id"]] = v

def prep(paper):
    for sec in paper["sections"]:
        if sec.get("useVisual"):
            sec["visualHtml"] = vmap[sec["visual"]]["html"]
            sec["questions"] = [dict(q) for q in vmap[sec["visual"]]["questions"]]
        if sec["mode"] == "mcq":
            for q in sec["questions"]:
                q["a"] = [q["options"][q["correct"]]]; q["m"] = q["a"][0]; q.setdefault("marks", 1)
        elif sec["mode"] == "auto":
            sec["questions"] = [{"n": a["n"], "q": sec["passage"], "a": a["a"], "m": a["a"][0],
                                 "tip": a.get("tip", ""), "blank": a["n"], "marks": 1}
                                for a in sec["answers"]]
            sec.pop("answers", None)
        elif sec["mode"] == "write":
            sec["questions"] = [{"n": 1, "q": sec.get("task", ""),
                                 "m": sec.get("model", ""), "a": [sec.get("model", "")],
                                 "marks": sec["marks"], "criteria": sec["criteria"],
                                 "pictures": sec.get("pictures"), "planNote": sec.get("planNote"),
                                 "theme": sec.get("theme")}]
        else:
            for q in sec["questions"]:
                q.setdefault("marks", 1)
                if "a" not in q:
                    q["a"] = [q.get("m")]
                elif isinstance(q["a"], str):
                    q["m"] = q["a"]; q["a"] = [q["m"]]
    return paper

prep(p2b["paper"])

p2c = json.loads((SRC / "content_paper2c.json").read_text(encoding="utf-8"))
v5 = p2c["visualText"]
for q in v5["questions"]:
    q["a"] = [q["options"][q["correct"]]]; q["m"] = q["a"][0]; q.setdefault("tip", "")
bank.append({"id": v5["id"], "letter": "V5", "title": f'Visual text · {v5["title"]}',
             "level": v5["level"], "mode": "mcq", "visual": v5["html"], "questions": v5["questions"]})
vmap[v5["id"]] = v5
prep(p2c["paper"])

# ---------- paper 1 (writing) and oral ----------
po = json.loads((SRC / "content_paper1_oral.json").read_text(encoding="utf-8"))
prep(po["paper1"])

p2d = json.loads((SRC / "content_paper2d.json").read_text(encoding="utf-8"))
p2e = json.loads((SRC / "content_paper2e.json").read_text(encoding="utf-8"))
p2f = json.loads((SRC / "content_paper2f.json").read_text(encoding="utf-8"))
p2g = json.loads((SRC / "content_paper2g.json").read_text(encoding="utf-8"))
for _p in (p2d["paper"], p2e["paper"], p2f["paper"], p2g["paper"]):
    prep(_p)
# the three PSLE-format papers and the writing paper are upper primary
for _p in (paper, p2b["paper"], p2c["paper"], po["paper1"]):
    _p.setdefault("level", "P6")

oral = po["oral"]
v3wo = json.loads((SRC / "content_v3_writing_oral.json").read_text(encoding="utf-8"))
v4wr = json.loads((SRC / "content_v4_writing.json").read_text(encoding="utf-8"))
v7wo = json.loads((SRC / "content_v7_writing_oral.json").read_text(encoding="utf-8"))
v8wo = json.loads((SRC / "content_v8_writing_oral.json").read_text(encoding="utf-8"))
v8wr = json.loads((SRC / "content_v8_writing.json").read_text(encoding="utf-8"))
oral["conversation"] += (v3wo["oral"] + v7wo["oral2"] + v8wo["oral3"]
                         + v10oral["oral4"] + v11or["oral5"])
oral["readAloud"] += (v4wr["readAloud"] + v7wo["readAloud2"] + v8wo["readAloud3"]
                      + v10oral["readAloud4"])

# reading aloud, practised in the app: say it, then mark yourself
bank.append({
    "id": "readaloud", "letter": "RA", "title": f'Reading aloud · {len(oral["readAloud"])} passages', "level": "P3",
    "mode": "compose", "oral": True,
    "instruction": "Read the passage out loud to an adult, then mark yourself against what the notes say to listen for.",
    "criteria": [
        {"name": "Fluency and pace", "max": 5, "bands": [
            {"label": "5 · Smooth throughout, well judged pace, no stumbles", "marks": 5},
            {"label": "4 · Mostly smooth, one or two stumbles", "marks": 4},
            {"label": "2–3 · Several stumbles, or rushed", "marks": 3},
            {"label": "0–1 · Halting, words guessed", "marks": 1}]},
        {"name": "Pronunciation and expression", "max": 5, "bands": [
            {"label": "5 · Clear final consonants, stress and feeling match the meaning", "marks": 5},
            {"label": "4 · Clear, with a little expression", "marks": 4},
            {"label": "2–3 · Some words mispronounced, flat delivery", "marks": 3},
            {"label": "0–1 · Hard to follow", "marks": 1}]}
    ],
    "questions": [{"n": i, "q": r["text"],
                   "m": "Listen for:\n• " + "\n• ".join(r["notes"]),
                   "a": [r["text"]], "marks": 10, "kind": f'Reading aloud · {r["level"]} and above',
                   "pac": "Read it silently once for meaning. Mark your pauses. Circle any hard words and say them twice. Then read it aloud."}
                  for i, r in enumerate(oral["readAloud"], 1)]
})

# composition planning, six minutes a plan
cp = v4wr["composition"]
bank.append({
    "id": cp["id"], "letter": "CP", "title": cp["title"], "level": cp["level"],
    "mode": "compose", "criteria": cp["criteria"], "instruction": cp["instruction"],
    "questions": [{"n": t["n"], "q": f'Theme: {t["theme"]}\n\n{t["prompt"]}',
                   "m": t["model"], "a": [t["model"]], "marks": 10,
                   "kind": f'Plan only · {t["theme"]}',
                   "pac": "Six minutes. Six boxes: theme, setting, characters, problem, climax, resolution. Notes, not sentences."}
                  for t in cp["tasks"]]
})

# P3–P4 picture composition: four pictures, write the story
p3c = json.loads((SRC / "content_v5_p3_composition.json").read_text(encoding="utf-8"))["set"]
bank.append({
    "id": p3c["id"], "letter": "CJ", "title": p3c["title"], "level": p3c["level"],
    "mode": "compose", "criteria": p3c["criteria"], "instruction": p3c["instruction"],
    "questions": [{"n": t["n"], "q": t["title"], "m": t["model"], "a": [t["model"]],
                   "marks": 20, "kind": f'Picture composition · {t["theme"]}',
                   "pac": p3c["helper"], "why": t["why"],
                   "pictures": t["pictures"]}
                  for t in p3c["tasks"]]
})

p3e = json.loads((SRC / "content_v11_p3_composition.json").read_text(encoding="utf-8"))["set"]
bank.append({
    "id": p3e["id"], "letter": p3e["letter"], "title": p3e["title"], "level": p3e["level"],
    "mode": "compose", "criteria": p3c["criteria"], "instruction": p3e["instruction"],
    "questions": [{"n": t["n"], "q": t["title"], "m": t["model"], "a": [t["model"]],
                   "marks": 20, "kind": f'Picture composition · {t["theme"]}',
                   "pac": p3e["helper"], "why": t["why"],
                   "pictures": t["pictures"]}
                  for t in p3e["tasks"]]
})

p3d = v7wo["compositionP3b"]
bank.append({
    "id": p3d["id"], "letter": p3d["letter"], "title": p3d["title"], "level": p3d["level"],
    "mode": "compose", "criteria": p3c["criteria"], "instruction": p3d["instruction"],
    "questions": [{"n": t["n"], "q": t["title"], "m": t["model"], "a": [t["model"]],
                   "marks": 20, "kind": f'Picture composition · {t["theme"]}',
                   "pac": p3d["helper"], "why": t["why"],
                   "pictures": t["pictures"]}
                  for t in p3d["tasks"]]
})

# ---------- printable P3–P4 composition document ----------
PC = ["# Picture Composition — Primary 3 and 4", "",
      "At Primary 3 and 4, composition is a **four-picture series**. The pictures tell a story in order, "
      "and the child writes it out in about 120 to 180 words. It is marked out of 20: **10 for content, "
      "10 for language**.", "",
      "This is a different exam from the Primary 5–6 one. There is no theme to interpret and no choice of "
      "pictures — all four must be used, in order. The skill being tested is telling a clear story in correct "
      "past tense, not inventing a plot.", "",
      "---", "", "## What the marks are for", "",
      "| Content — 10 | | Language — 10 | |", "|---|---|---|---|"]
for i in range(5):
    a = p3c["criteria"][0]["bands"][i]; b3 = p3c["criteria"][1]["bands"][i]
    PC.append(f'| {a["label"]} | {a["marks"]} | {b3["label"]} | {b3["marks"]} |')
PC += ["", "### The three things that lift a P3 composition", "",
       "1. **Add what the pictures cannot show.** The day, the weather, a name, why the child was there, "
       "what they were thinking. A story that only describes the four drawings stays in the middle band.",
       "2. **Stay in the past tense.** This is where most language marks are lost at this level. "
       "*I saw, I ran, she smiled* — not *I see, I run, she smiles*.",
       "3. **End with a feeling and a reason.** \"I was happy\" earns little. \"I was happy, but not because "
       "of the chocolates\" earns a great deal more.", "",
       "### Before writing — three boxes, two minutes", "", "```", p3c["helper"], "```", "",
       "---", "", "## The twelve tasks", "",
       "*Write your own story first. Then read the model and the note underneath it.*", ""]
for t in p3c["tasks"] + [dict(x, n=x["n"] + len(p3c["tasks"])) for x in p3d["tasks"]]:
    PC += [f'### {t["n"]}. {t["title"]}  ·  *{t["theme"]}*', "",
           "**The four pictures**", ""]
    for pi, pic in enumerate(t["pictures"], 1):
        PC.append(f'{pi}. {pic["caption"]}')
    PC += ["", "**Model composition**", "", "> " + t["model"].replace("\n\n", "\n>\n> "), "",
           f'**What makes it work:** {t["why"]}', "", "---", ""]
PC += ["## A note for parents", "",
       "Mark one thing at a time. A Primary 3 child told to fix their tense, add more detail, vary their "
       "sentences and improve their ending will change nothing. Pick the single weakest of the two scales, "
       "say what to do about it in one sentence, and let everything else go until next week."]
(SRC / "12_Picture_Composition_P3_P4.md").write_text("\n".join(PC), encoding="utf-8")

for oi, c in enumerate(oral["conversation"], 1):
    bank.append({"id": c["id"], "letter": f"O{oi}", "title": f'Oral · {c["title"]}',
                 "level": c["level"], "mode": "read", "oral": True, "visual": c["stimulus"],
                 "questions": [{"n": q["n"], "q": q["q"], "a": [q["model"]], "m": q["model"],
                                # left empty on purpose when the question has no tip of its own:
                                # the page then prints its own upper-primary advice, and setting
                                # it here as well printed the same instruction twice
                                "tip": q.get("tip", ""),
                                "marks": 5} for q in c["questions"]]})

# ---------- situational writing practice set ----------
sw = v3wo["situational"]
bank.append({
    "id": sw["id"], "letter": "SW", "title": sw["title"], "level": sw["level"],
    "mode": "compose", "criteria": sw["criteria"],
    "questions": [{"n": t["n"], "q": t["task"], "m": t["model"], "a": [t["model"]],
                   "kind": t["kind"], "pac": t["pac"], "why": t["why"], "marks": 15}
                  for t in sw["tasks"]]
})

sw2 = v7wo["situational2"]
bank.append({
    "id": sw2["id"], "letter": sw2["letter"], "title": sw2["title"], "level": sw2["level"],
    "mode": "compose", "criteria": sw["criteria"],
    "questions": [{"n": t["n"], "q": t["task"], "m": t["model"], "a": [t["model"]],
                   "kind": t["kind"], "pac": t["pac"], "why": t["why"], "marks": 15}
                  for t in sw2["tasks"]]
})

sw4 = v8wo["situational4"]
bank.append({
    "id": sw4["id"], "letter": sw4["letter"], "title": sw4["title"], "level": sw4["level"],
    "mode": "compose", "criteria": sw4["criteria"],
    "questions": [{"n": t["n"], "q": t["task"], "m": t["model"], "a": [t["model"]],
                   "kind": t["kind"], "pac": t["pac"], "why": t["why"], "marks": 10}
                  for t in sw4["tasks"]]
})

sw5 = v10wr["situational5"]
bank.append({
    "id": sw5["id"], "letter": sw5["letter"], "title": sw5["title"], "level": sw5["level"],
    "mode": "compose", "criteria": sw5["criteria"], "instruction": sw5["instruction"],
    "questions": [{"n": t["n"], "q": t["task"], "m": t["model"], "a": [t["model"]],
                   "kind": t["kind"], "pac": t["pac"], "why": t["why"], "marks": 15}
                  for t in sw5["tasks"]]
})

cm = v8wr["composition2"]
bank.append({
    "id": cm["id"], "letter": cm["letter"], "title": cm["title"], "level": cm["level"],
    "mode": "compose", "criteria": cm["criteria"], "instruction": cm["instruction"],
    "questions": [{"n": t["n"], "q": f'Theme: {t["theme"]}\n\n{t["prompt"]}',
                   "m": t["model"], "a": [t["model"]], "marks": 40,
                   "kind": f'Full composition · {t["theme"]}',
                   "pac": "Plan for six minutes, then write for forty. " + t["plan"],
                   "why": t["why"] + (
                       "\n\n**A shorter Primary 5 version of the same story:**\n\n" + t["p5model"]
                       if t.get("p5model") else "")}
                  for t in cm["tasks"]]
})

cn = v10wr["composition3"]
bank.append({
    "id": cn["id"], "letter": cn["letter"], "title": cn["title"], "level": cn["level"],
    "mode": "compose", "criteria": cn["criteria"], "instruction": cn["instruction"],
    "questions": [{"n": t["n"], "q": f'Theme: {t["theme"]}\n\n{t["prompt"]}',
                   "m": t["model"], "a": [t["model"]], "marks": 40,
                   "kind": f'Full composition · {t["theme"]}',
                   "pac": "Plan for six minutes, then write for forty. " + t["plan"],
                   "why": t["why"] + (
                       "\n\n**A shorter Primary 5 version of the same story:**\n\n" + t["p5model"]
                       if t.get("p5model") else "")}
                  for t in cn["tasks"]]
})

# ---------- printable situational writing document ----------
SW = ["# Situational Writing — Twenty Tasks with Model Answers", "",
      "Paper 1 Part 1 is worth **15 marks**: 9 for task fulfilment and 6 for language and organisation. "
      "Task fulfilment is worth more, which means covering every bullet point matters more than elegant writing.", "",
      "Work through one task a week. Write your own answer first, cover the model, then compare.", "",
      "---", "", "## The marking bands", "",
      "| Task fulfilment | | Language and organisation | |", "|---|---|---|---|"]
for i in range(5):
    a = sw["criteria"][0]["bands"][i]; b2 = sw["criteria"][1]["bands"][i]
    SW.append(f'| {a["label"]} | {a["marks"]} | {b2["label"]} | {b2["marks"]} |')
SW += ["", "---", ""]
_allsw = (sw["tasks"] + [dict(x, n=x["n"] + len(sw["tasks"])) for x in sw2["tasks"]]
          + [dict(x, n=x["n"] + len(sw["tasks"]) + len(sw2["tasks"])) for x in sw4["tasks"]])
for t in _allsw:
    SW += [f'## Task {t["n"]} · {t["kind"]}', "",
           "**The task**", "", t["task"].replace("\n", "\n"), "",
           f'> **Before you write:** {t["pac"]}', "",
           "**Model answer**", "", "```", t["model"], "```", "",
           f'**Why it scores:** {t["why"]}', "", "---", ""]
SW += ["## The five most common ways marks are lost", "",
       "1. **A bullet point missed entirely.** Tick them off on the question paper as you write.",
       "2. **A bullet point mentioned but not developed.** Each point needs one supporting detail, not a bare sentence.",
       "3. **Tone drifting.** \"Dear Sir or Madam\" followed by \"Hey, so anyway\" loses language marks immediately.",
       "4. **A vague request.** \"Please do something about it\" earns less than \"Please repair the zip or exchange the bag\".",
       "5. **Inventing facts that contradict the question.** If the question says two weeks ago, do not write last month."]
(SRC / "11_Situational_Writing_Models.md").write_text("\n".join(SW), encoding="utf-8")

# ---------- printable oral document ----------
OD = ["# Oral Practice — Paper 4 (30 marks)", "",
      "Reading Aloud is worth 10 marks and Stimulus-based Conversation 20. Both are practised out loud. "
      "Reading silently will not prepare a child for either.", "",
      "---", "", "## Part 1 — Reading Aloud", "",
      "**How to use these:** give the child five minutes with the passage. They should read it silently once for meaning, "
      "mark the pauses, circle difficult words, and underline the words to stress. Then they read it aloud to you. "
      "Read the notes yourself first — they list what to listen for.", ""]
for i, r in enumerate(oral["readAloud"], 1):
    OD += [f'### Passage {i}  ·  *{r["level"]} and above*', "", "> " + r["text"], "",
           "**Listen for:**", ""] + [f'- {n}' for n in r["notes"]] + [""]
OD += ["---", "", "## Part 2 — Stimulus-based Conversation", "",
       "Three questions follow each stimulus. The child looks at the stimulus for a short while, then answers aloud. "
       "Model answers are given — they are one good version, not the only one. What matters is the **shape**: "
       "Point, Elaborate, Example, Link.", "",
       "> **The single most common mistake** is a one-sentence answer. Four to six sentences is the target for every question.", ""]
for c in oral["conversation"]:
    OD += [f'### {c["title"]}  ·  *{c["level"]} and above*', "",
           "*(The stimulus for this topic is shown in the app under Practice. A description is given below so the "
           "conversation can also be done from this document.)*", ""]
    OD += ["**Stimulus summary:** " + re.sub(r"<[^>]+>", " ", c["stimulus"]).replace("&middot;", "·").replace("&ldquo;", "“").replace("&rdquo;", "”").replace("&nbsp;", " "), ""]
    for q in c["questions"]:
        OD += [f'**Q{q["n"]}. {q["q"]}**', "", "> " + q["model"], ""]
OD += ["---", "", "## Marking Reading Aloud at home", "",
       "| Out of 10 | What it sounds like |", "|---|---|",
       "| 9–10 | Fluent throughout, clear final consonants, expression matches the meaning, well-judged pace |",
       "| 7–8 | Mostly fluent, one or two stumbles, some expression |",
       "| 5–6 | Several stumbles or mispronunciations, flat delivery, rushed |",
       "| 3–4 | Frequent hesitation, words guessed, little sense of the meaning |",
       "| 1–2 | Very halting |", "",
       "## Marking the Conversation at home", "",
       "| Out of 20 | What it sounds like |", "|---|---|",
       "| 17–20 | Every answer developed over several sentences with a personal example, clear opinions, natural delivery, good eye contact |",
       "| 13–16 | Answers developed but one is short, or examples are general rather than personal |",
       "| 9–12 | Answers of one or two sentences, opinions stated but not explained |",
       "| 5–8 | Very short answers, long pauses, needs prompting |",
       "| 1–4 | Barely responds |", "",
       "> Score the child honestly, tell them the one thing to change, and do the same stimulus again a week later. "
       "The improvement between attempt one and attempt two is usually larger than anything a term of lessons produces."]
(SRC / "10_Oral_Practice.md").write_text("\n".join(OD), encoding="utf-8")

# ---------- printable listening scripts ----------
LS = ["# Listening Comprehension — Reader's Script", "",
      "**For the adult reading aloud. Do not show this document to the child.**", "",
      lis["instructions"], "",
      "Read each text twice, at a normal pace, pausing for about five seconds between the two readings. "
      "The child should read the question and the four options *before* you begin. Answers are at the end.", "",
      "---", ""]
seen = set()
for it in lis["items"]:
    if it.get("passage") and it["passage"] in seen:
        continue
    if it.get("passage"):
        seen.add(it["passage"])
        LS += [f'## Passage {it["passage"]} — for questions {it["n"]}–{it["n"]+4}', ""]
    else:
        LS += [f'## Question {it["n"]}', ""]
    for para in it["script"].split("\n\n"):
        LS += ["> " + para.strip(), ">"]
    LS += ["", "---", ""]
LS += ["## Answers", "", "| Q | Ans | | Q | Ans |", "|---|---|---|---|---|"]
half = len(lis["items"]) // 2
for i in range(half):
    a = lis["items"][i]; b = lis["items"][i + half]
    LS.append(f'| {a["n"]} | ({a["correct"]+1}) | | {b["n"]} | ({b["correct"]+1}) |')
def script_doc(spec, heading):
    out = [f"# {heading}", "",
           "**For the adult reading aloud. Do not show this document to the child.**", "",
           spec["instructions"], "",
           "Read each text twice, at a normal pace, pausing for about five seconds between the two readings. "
           "The child should read the question and the four options *before* you begin. Answers are at the end.", "",
           "---", ""]
    seen2 = set()
    for it in spec["items"]:
        if it.get("passage") and it["passage"] in seen2:
            continue
        if it.get("passage"):
            seen2.add(it["passage"])
            out += [f'## Passage {it["passage"]} — for questions {it["n"]}–{it["n"]+4}', ""]
        else:
            out += [f'## Question {it["n"]}', ""]
        for para in it["script"].split("\n\n"):
            out += ["> " + para.strip(), ">"]
        out += ["", "---", ""]
    out += ["## Answers", "", "| Q | Ans | | Q | Ans |", "|---|---|---|---|---|"]
    h = len(spec["items"]) // 2
    for i in range(h):
        a = spec["items"][i]; b2 = spec["items"][i + h]
        out.append(f'| {a["n"]} | ({a["correct"]+1}) | | {b2["n"]} | ({b2["correct"]+1}) |')
    return "\n".join(out)

LS = LS[:0] + [script_doc(lis, "Listening Comprehension — Reader's Script, Paper 1"), "",
               "\n\n" + script_doc(lis2, "Listening Comprehension — Reader's Script, Paper 2"), "",
               "\n\n" + script_doc(lis3, "Listening Comprehension — Reader's Script, Paper 3"), "",
               "\n\n" + script_doc(lis4, "Listening Comprehension — Reader's Script, Paper 4"), "",
               "\n\n" + script_doc(lis5, "Listening Comprehension — Reader's Script, Paper 5 (Primary 3–4)")]
(SRC / "09_Listening_Scripts.md").write_text("\n".join(LS), encoding="utf-8")


# ---------- printable document: the eight full model compositions ----------
CD = ["# Continuous Writing — Eight Full Model Compositions", "",
      "Paper 1 Part 2 is worth **40 marks**: 20 for content and 20 for language. This is the single "
      "largest block of marks in the whole examination.", "",
      "Use these the hard way. Set a timer for 46 minutes — six to plan, forty to write — and write the "
      "whole composition before you read the model. Reading the model first is comfortable and teaches "
      "you nothing.", "", "---", "", "## The marking bands", "",
      "| Content — 20 | | Language — 20 | |", "|---|---|---|---|"]
for i in range(5):
    a = cm["criteria"][0]["bands"][i]; b4 = cm["criteria"][1]["bands"][i]
    CD.append(f'| {a["label"]} | {a["marks"]} | {b4["label"]} | {b4["marks"]} |')
CD += ["", "> **A word of warning about these models.** They are deliberately plain. They work by "
       "structure, specific detail and honest feeling rather than by rich description. A Singapore "
       "marking scheme also rewards vivid vocabulary, varied sentence openings and figurative language, "
       "so do not read these as permission to write flatly. Take the shape from them, and bring your own "
       "colour to it.", "", "---", ""]
for t in cm["tasks"]:
    CD += [f'## {t["n"]}. {t["theme"]}', "", "**The task**", "", t["prompt"], "",
           f'> **A plan that would work:** {t["plan"]}', "",
           "**Model composition** (" + str(len(t["model"].split())) + " words)", "",
           "> " + t["model"].replace("\n\n", "\n>\n> "), "",
           f'**Why it scores:** {t["why"]}', ""]
    if t.get("p5model"):
        CD += ["**The same story at Primary 5 length** (" + str(len(t["p5model"].split())) + " words)", "",
               "> " + t["p5model"].replace("\n\n", "\n>\n> "), ""]
    CD += ["---", ""]
(SRC / "15_Full_Model_Compositions.md").write_text("\n".join(CD), encoding="utf-8")

# ---------- printable document: the two lower-primary papers ----------
def paper_doc(pp, heading, intro):
    D = [f"# {heading}", "", intro, "",
         f'**{pp["totalMarks"]} marks · {pp["minutes"]} minutes.** Sit it in one go, with a timer, and do not '
         "look anything up. Mark it afterwards against the answers at the end.", "", "---", ""]
    K = ["", "---", "", "# Answers", ""]
    for sec in pp["sections"]:
        D += [f'## {sec["name"]}  ·  {sec["marks"]} marks', ""]
        if sec.get("instruction"): D += [f'*{sec["instruction"]}*', ""]
        K += [f'### {sec["name"]}', ""]
        if sec.get("visualHtml") or sec.get("visual"):
            D += ["> *(The poster or notice for this section is in the website version. "
                  "Open it on screen for this part.)*", ""]
        if sec.get("passage"):
            txt = sec["passage"]
            D += [txt if isinstance(txt, str) else "\n\n".join(txt), ""]
        if sec["mode"] == "auto" and sec.get("answers"):
            K += ["  ·  ".join(f'**{a["n"]}** {a["a"][0]}' for a in sec["answers"]), ""]
        for q in sec.get("questions", []):
            if q.get("options"):
                D.append(f'{q["n"]}. {q["q"]}')
                D.append("   " + "   ".join(f'({i+1}) {o}' for i, o in enumerate(q["options"])))
                D.append("")
            else:
                mk = f' *({q["marks"]}m)*' if q.get("marks") else ""
                D += [f'{q["n"]}. {q["q"]}{mk}', ""]
        if sec["mode"] == "mcq":
            K += ["  ·  ".join(f'**{q["n"]}** ({q["correct"]+1})' for q in sec["questions"]), ""]
        elif sec["mode"] in ("edit", "read", "self"):
            for q in sec["questions"]:
                ans = q.get("a") if isinstance(q.get("a"), str) else (q.get("m") or (q.get("a") or [""])[0])
                K.append(f'- **{q["n"]}** {ans}')
            K.append("")
        D += ["---", ""]
    return "\n".join(D + K)

(SRC / "16_Lower_Primary_Papers.md").write_text(
    paper_doc(p2d["paper"], "Primary 3 Practice Paper",
              "A Primary 3 school-examination paper. This is not a PSLE paper: it is shorter, there is no "
              "synthesis section, and the comprehension is mostly about finding information in the passage.")
    + "\n\n\\newpage\n\n"
    + paper_doc(p2e["paper"], "Primary 4 Practice Paper",
                "A Primary 4 school-examination paper. Longer than the Primary 3 one, with a vocabulary cloze "
                "and a short synthesis section added."),
    encoding="utf-8")
print("15_Full_Model_Compositions.md and 16_Lower_Primary_Papers.md written")

# ---------- printable document for the new grammar & vocabulary sets ----------
def practice_doc(title, intro, setlist, outfile):
    """Write a question paper plus a separate answer key for a list of drill sets."""
    Q = [f"# {title}", "", intro, "",
         "Work one section at a time. Write your answers on paper, then mark yourself "
         "against the answer key at the end. Anything you get wrong goes on your error "
         "log and comes back in a week.", "", "---", ""]
    K = ["", "---", "", "# Answer Key", ""]
    for s_ in setlist:
        head = f'{s_["letter"]} · {s_["title"]}  ·  {s_["level"]}'
        Q += [f'## {head}', ""]
        if s_.get("instruction"):
            _ins = (s_["instruction"].replace("Type it in the box", "Write your answer")
                    .replace("in the box", "on your paper")
                    .replace("Type the", "Write the").replace("Type your", "Write your")
                    .replace("Type it", "Write it").replace(" type ", " write "))
            Q += [f'*{_ins}*', ""]
        K += [f'### {head}', ""]
        if s_["id"] in MULTI_PASSAGE:
            for pp in s_["passages"]:
                Q += [pp["text"], ""]
            amap = {a["n"]: a for a in s_["answers"]}
            row = []
            for n in sorted(amap):
                row.append(f'**{n}** {amap[n]["a"][0]}')
            K += ["  ·  ".join(row), ""]
        elif s_["mode"] == "mcq":
            for q in s_["questions"]:
                Q.append(f'{q["n"]}. {q["q"]}')
                Q.append("   " + "   ".join(f'({i+1}) {o}' for i, o in enumerate(q["options"])))
                Q.append("")
            K += ["  ·  ".join(f'**{q["n"]}** ({q["correct"]+1})' for q in s_["questions"]), ""]
            for q in s_["questions"]:
                if q.get("tip"):
                    K.append(f'- **{q["n"]}** {q["options"][q["correct"]]} — {q["tip"]}')
            K.append("")
        else:
            for q in s_["questions"]:
                Q += [f'{q["n"]}. {q["q"]}', ""]
            for q in s_["questions"]:
                tip = f' — {q["tip"]}' if q.get("tip") else ""
                K.append(f'- **{q["n"]}** {q["m"]}{tip}')
            K.append("")
        Q += ["---", ""]
    (SRC / outfile).write_text("\n".join(Q + K), encoding="utf-8")
    return sum(len(x.get("questions", x.get("answers", []))) for x in setlist)

_v7sets = {x["id"]: x for x in (v7gram["sets"] + v7vocab["sets"] + v8gram["sets"] + v8vocab["sets"])}
_n13 = practice_doc(
    "More Grammar Practice — 14 New Sets",
    "Eleven further grammar sets covering the areas that the earlier practice book treats "
    "only briefly: articles and determiners, conjunctions, comparatives, verb patterns, "
    "conditionals, harder subject–verb agreement, punctuating speech, synthesis and "
    "transformation, spelling, editing and grammar cloze.",
    [_v7sets[x["id"]] for x in v7gram["sets"] + v8gram["sets"]],
    "13_More_Grammar_Practice.md")
_n14 = practice_doc(
    "More Vocabulary Practice — 11 New Sets",
    "Eight further vocabulary sets: similes and proverbs, homophones, compound words, "
    "words for describing feelings and character, vivid verbs for composition, a third set "
    "of idioms, a vocabulary cloze and the precise words that lift a Primary 6 answer.",
    [_v7sets[x["id"]] for x in v7vocab["sets"] + v8vocab["sets"]],
    "14_More_Vocabulary_Practice.md")
print(f"13_More_Grammar_Practice.md  ({_n13} questions)")
print(f"14_More_Vocabulary_Practice.md  ({_n14} questions)")

# ---------- grouping for the practice screen ----------
GROUPS = {
    "Grammar & sentence work": list("ABCDEFGHIJKLMNOPQUVW")
                               + ["Z1", "Z2", "Z4", "Z5", "Y1", "Y2", "Y3", "Y4", "Y5", "Y6", "Y7"]
                               + [f"GA{i}" for i in range(1, 30)],
    "Vocabulary": list("STX") + ["Z3", "Y8", "W1", "W2", "W3", "W4"]
                  + [f"VA{i}" for i in range(1, 25)],
    "Comprehension": ["R", "Y", "Z6", "Z7"] + [f"C{i}" for i in range(1, 41)],
    "Visual text & listening": [f"V{i}" for i in range(1, 22)] + ["L1", "L2", "L3", "L4", "L5"],
    "Writing": ["SW", "SW2", "SW4", "SW5", "CP", "CM", "CN", "CJ", "CJ2", "CJ3"],
    "Oral": [f"O{i}" for i in range(1, 26)] + ["RA"],
}
for s in bank:
    for g, letters in GROUPS.items():
        if s["letter"] in letters:
            s["group"] = g
            break
    s.setdefault("group", "Grammar & sentence work")

ORDER = ["Grammar & sentence work", "Vocabulary", "Comprehension",
         "Visual text & listening", "Writing", "Oral"]
# ---------- spread the correct answer evenly across the four positions ----------
# Written questions tend to put the right answer in the same slot every time, which lets a
# child score highly by always clicking the same option. Shuffle deterministically so the
# order is stable across rebuilds (saved progress stores an index).
import hashlib, random as _rnd

PINNED = ("none of", "all of", "all four", "neither", "nothing", "it does not say",
          "there is none", "both of", "either of", "no change")

def _spread(sid, qs):
    """Place the correct option at a balanced target slot, then shuffle the rest around it."""
    idxs = [i for i, q in enumerate(qs) if q.get("options") and "correct" in q]
    if not idxs:
        return
    seq = [i % 4 for i in range(len(idxs))]          # even spread of target positions
    _rnd.Random(int(hashlib.md5(sid.encode()).hexdigest()[:8], 16)).shuffle(seq)
    for pos, qi in zip(seq, idxs):
        q = qs[qi]
        opts = q["options"]
        # keep "none of the above"-style options where the author put them
        movable = [i for i, o in enumerate(opts)
                   if not o.strip().lower().startswith(PINNED)]
        if len(movable) < 2 or q["correct"] not in movable:
            continue
        target = movable[pos % len(movable)]
        correct_opt = opts[q["correct"]]
        others = [opts[i] for i in movable if i != q["correct"]]
        _rnd.Random(int(hashlib.md5(f'{sid}#{q["n"]}'.encode()).hexdigest()[:8], 16)).shuffle(others)
        new = list(opts)
        new[target] = correct_opt
        it = iter(others)
        for slot in movable:
            if slot != target:
                new[slot] = next(it)
        q["options"] = new
        q["correct"] = target
        if q.get("m"):
            q["m"] = new[target]
            q["a"] = [q["m"]]

for _s in bank:
    _spread(_s["id"], _s["questions"])
for _p in (paper, p2b["paper"], p2c["paper"], po["paper1"],
           p2d["paper"], p2e["paper"], p2f["paper"], p2g["paper"]):
    for _sec in _p["sections"]:
        if _sec["mode"] == "mcq":
            _spread(_p["id"] + _sec["id"], _sec["questions"])
(SRC / "papers.json").write_text(
    json.dumps([p2d["paper"], p2f["paper"], p2g["paper"], p2e["paper"],
                paper, p2b["paper"], p2c["paper"], po["paper1"]],
               ensure_ascii=False), encoding="utf-8")

# --- explanations written separately, applied to the assembled bank ---
# Doing this here rather than in the source files means a tip lands whatever shape
# its set is stored in (questions, cloze answers, or a visual text inside a paper).
_tipfile = SRC / "tips" / "ALL.txt"
if _tipfile.exists():
    _tips, _hit = {}, 0
    for _line in _tipfile.read_text(encoding="utf-8").splitlines():
        if not _line.strip():
            continue
        _L, _n, _t = _line.split("|", 2)
        _tips[(_L.strip(), int(_n))] = _t.strip()
    for _s in bank:
        for _q in _s["questions"]:
            _k = (_s["letter"], _q.get("n"))
            if _k in _tips and not (_q.get("tip") or "").strip():
                _q["tip"] = _tips[_k]
                _hit += 1
    print(f"applied {_hit} explanations from tips/ALL.txt")

bank.sort(key=lambda s: (ORDER.index(s["group"]), s["id"]))

# --- late corrections applied to the assembled bank ---
NO_ARTICLE = ["x", "none", "no article", "no preposition", "-", "\u2014"]
for s_ in bank:
    for q in s_["questions"]:
        if isinstance(q.get("a"), list) and q["a"] and q["a"][0].startswith("X"):
            q["a"] = ["X"] + NO_ARTICLE
            q["m"] = "X"
        # accept the corrected fragment as well as the full rewritten sentence
        if q.get("m", "").startswith("We discussed the problem"):
            q["a"] = ["We discussed the problem", "discussed the problem",
                      "We discussed the problem.", "discussed"]

# full-sentence rewrites sitting inside otherwise auto-marked sets must be self-marked
SENTENCE_ITEMS = {"secG": [120], "secH": [123, 124]}
for s_ in bank:
    for n in SENTENCE_ITEMS.get(s_["id"], []):
        for q in s_["questions"]:
            if q["n"] == n:
                q["mode"] = "self"

PAPER_VISUALS = {"vtA": "Mock Paper 2A", "vtD": "Mock Paper 2B", "vtE": "Mock Paper 2C"}
for s_ in bank:
    if s_["id"] in PAPER_VISUALS:
        s_["alsoIn"] = PAPER_VISUALS[s_["id"]]

(SRC / "bank_full.json").write_text(json.dumps(bank, ensure_ascii=False), encoding="utf-8")

# ---------- generate the comprehension guide document ----------
L = ["# Comprehension Guide — Paper 2 Open-Ended (20 marks)",
     "",
     "Comprehension is the largest single component of Paper 2 Booklet B, and the one where marks are most often lost to **technique** rather than understanding. Most children understand the passage perfectly well and still lose six or seven marks, because they answer the question they expected instead of the question that was asked.",
     "",
     "This guide has two parts: the eight question types and how each one must be answered, then four full passages with model answers.",
     "",
     "---", "",
     "## Part 1 — The Eight Question Types", ""]

for i, l in enumerate(comp["lessons"], 1):
    L += [f'### {i}. {l["title"]}  ·  *{l["marks"]}*', "",
          l["rule"], "",
          f'> **Question:** {l["example"]["q"]}', ">",
          f'> ❌ **Weak:** {l["example"]["weak"]}', ">",
          f'> ✅ **Strong:** {l["example"]["strong"]}', ">",
          f'> *{l["example"]["note"]}*', ""]

L += ["---", "",
      "## How to work through a comprehension passage", "",
      "1. **Read the questions first.** Two minutes spent here saves ten later — you read the passage knowing what to look for.",
      "2. **Read the passage once, without stopping.** Do not annotate yet. Get the whole shape of it.",
      "3. **Read again with a pencil.** Underline anything that answers a question, and write the question number in the margin beside it.",
      "4. **Check the marks.** One mark means one point. Three marks means three separate points. Never write a paragraph for a one-mark question, and never write one sentence for a three-mark question.",
      "5. **Answer in full sentences**, unless the question asks for a single word.",
      "6. **Re-read your answer against the question.** The commonest error in the whole paper is answering a related question rather than the one printed.",
      "",
      "### The lifting trap", "",
      "Lifting means copying a phrase straight from the passage. It is allowed for some questions and fatal for others:",
      "",
      "| Question says | Lifting |",
      "|---|---|",
      "| \"Give evidence\" / \"Quote\" | ✅ Expected — copy exactly |",
      "| Nothing about wording | ⚠️ Allowed, but adapt so it reads as an answer |",
      "| \"In your own words\" | ❌ Zero marks if you lift the key words |",
      "",
      "---", "",
      "## Part 2 — Practice Passages", "",
      "*Model answers follow each passage. Cover them, write your own answers first, then compare.*", ""]

for p in comp["passages"]:
    total = sum(q["marks"] for q in p["questions"])
    L += ["---", "",
          f'## {p["title"]}', "",
          f'*{p["kind"]} · about {p["words"]} words · {len(p["questions"])} questions · {total} marks · suggested for {p["level"]} and above*', ""]
    for para in p["text"]:
        L += [para, ""]
    L += ["### Questions", ""]
    for q in p["questions"]:
        L.append(f'**{q["n"]}.** {q["q"]}' + ("" if "(" in q["q"] else f' *({q["marks"]}m)*"'.replace('"', '')))
        L.append("")
    L += ["### Model answers", ""]
    for q in p["questions"]:
        L += [f'**{q["n"]}.** {q["a"]}  `[{q["marks"]}m]`', ""]
        if q.get("tip"):
            L += [f'> {q["tip"]}', ""]

(SRC / "07_Comprehension_Guide.md").write_text("\n".join(L), encoding="utf-8")

tot = sum(len(s["questions"]) for s in bank)
print(f"{len(bank)} sets · {tot} questions")
for s in bank[-9:]:
    print(f'  {s["id"]:<8} {s["title"][:44]:<44} {s["mode"]:<5} {len(s["questions"]):>3}')
