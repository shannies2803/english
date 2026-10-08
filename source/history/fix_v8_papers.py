#!/usr/bin/env python3
"""Fixes from the eighth audit — the two new mock papers."""
import json, pathlib, re
log = []

# ─────────────────────────────── Primary 3 paper
fn = pathlib.Path("content_paper2d.json"); d = json.loads(fn.read_text(encoding="utf-8"))
S = {s["id"]: s for s in d["paper"]["sections"]}
def q(sid, n): return next(x for x in S[sid]["questions"] if x["n"] == n)

# 1 — A3 Q2 asked which pupil is on duty three times; NOBODY was. Give Gopal the Friday slot.
S["A3"]["visual"] = S["A3"]["visual"].replace(
    "<td style=\"padding:7px 8px;border:1px solid #BBD6C6\">Nadia, Ken</td>",
    "<td style=\"padding:7px 8px;border:1px solid #BBD6C6\">Nadia, Gopal</td>")
assert "Nadia, Gopal" in S["A3"]["visual"]
log.append("P3 A3: Friday pair changed to Nadia, Gopal so Q2 has exactly one answer")

# 2 — B1 blank 1 keyed 'by' but the sentence already had the article: "by the bus"
S["B1"]["passage"] = S["B1"]["passage"].replace(
    "at eight o'clock (1)______ the bus", "at eight o'clock (1)______ bus")
A = {a["n"]: a for a in S["B1"]["answers"]}
assert "(1)______ bus," in S["B1"]["passage"] or "(1)______ bus" in S["B1"]["passage"]
# 3 — widen the two blanks with a second natural answer
A[2]["a"] = ["before", "after", "when", "as"]
A[7]["a"] = ["but", "though", "yet"]
log.append("P3 B1: blank 1 article removed; blanks 2 and 7 widened")

# 4 — Q10 was a 3-mark symbolic-inference item, which is P5/P6 work in a P3 paper.
#     Recast as a 2-mark inference and move the spare mark to Q7, which needed two points.
x = q("B3", 10)
x["q"] = "What does the grandfather hope will happen next April, and how do we know?"
x["a"] = ("He hopes there will be another crop of mangoes to pick and share. We know because he keeps the "
          "bottle on the bamboo pole all year round, ready, even in the months when there is nothing to pick.")
x["marks"] = 2
x = q("B3", 7)
x["q"] = "What did Mrs Rahim do with her mangoes, and what did she tell the family when she came?"
x["a"] = ("She made mango chutney from them and brought a jar of it to the family. She told them she had not "
          "spoken to anybody on their floor for two years.")
x["marks"] = 2
# Q9 asked the same thing as the new half of Q7, so replace it with a retrieval item
x = q("B3", 9)
x["q"] = "Which word in the passage means 'go bad'?"
x["a"] = "'Spoil'."
x["marks"] = 1
x["tip"] = "Look in the paragraph about the mangoes that fell onto the grass."
q("B3", 8)["q"] = "How do we know the neighbours were grateful? Give one piece of evidence."
q("B3", 8)["a"] = ("Either: somebody left a tin of biscuits outside their door the next morning; or Mrs Rahim "
                   "brought them a jar of mango chutney a week later.")
q("B3", 8)["marks"] = 1
tot = sum(x["marks"] for x in S["B3"]["questions"])
S["B3"]["marks"] = tot
d["paper"]["totalMarks"] = sum(s["marks"] for s in d["paper"]["sections"])
d["paper"]["minutes"] = 75
log.append(f"P3 B3: Q7/Q8/Q9/Q10 rebalanced; section now {tot} marks, paper {d['paper']['totalMarks']}, 75 min")
fn.write_text(json.dumps(d, ensure_ascii=False), encoding="utf-8")

# ─────────────────────────────── Primary 4 paper
fn = pathlib.Path("content_paper2e.json"); d = json.loads(fn.read_text(encoding="utf-8"))
S = {s["id"]: s for s in d["paper"]["sections"]}

# 5 — editing line 4 carried TWO errors (transposition and a missing -ed)
x = q("B2", 4)
x["q"] = "The bundles are then wieghed on a scale borrowed from the canteen."
log.append("P4 B2 line 4: now a single spelling error (wieghed → weighed)")

# 6 — 'volcanos' is a listed variant, so that line arguably had no error
x = q("B2", 9)
x["q"] = "My favourite is a book about heros who explored the Arctic."
x["a"] = ["heroes"]; x["m"] = "heroes"
x["tip"] = "The error was “heros”. The plural is 'heroes'."
# 7 — 'Our class have been collecting' is acceptable British usage, so the line had no clear error
x = q("B2", 1)
x["q"] = "Our class collect old newspapers since April."
x["a"] = ["has"]; x["m"] = "has"
x["tip"] = "The error was “collect”. 'Since April' needs the present perfect: 'has been collecting' — write 'has'."
# that fix is muddled; make it a clean single-word substitution instead
x["q"] = "Our class has been collecting old newspaper since April."
x["a"] = ["newspapers"]; x["m"] = "newspapers"
x["tip"] = "The error was “newspaper”. More than one is collected, so the plural is needed."
# 8 — five of twelve lines tested subject-verb agreement; broaden the sampling
x = q("B2", 12)
x["q"] = "Mrs Ong says that bottles are worth more then paper."
x["a"] = ["than"]; x["m"] = "than"
x["tip"] = "The error was “then”. After a comparative use 'than'."
x = q("B2", 6)
x["q"] = "Mrs Ong was very pleased of the result."
x["a"] = ["with"]; x["m"] = "with"
x["tip"] = "The error was “of”. The phrase is 'pleased with'."
log.append("P4 B2: lines 1, 6, 9, 12 rewritten to broaden the rules sampled")

# 9 — cloze blank 8 also accepted 'only', which reverses the meaning
S["B1"]["passage"] = S["B1"]["passage"].replace(
    "He (8)______ complained once.", "He (8)______ complained at all.")
A = {a["n"]: a for a in S["B1"]["answers"]}
A[8]["tip"] = "'He never complained at all' — the negative is needed before the verb."
A[3]["a"] = ["but", "yet"]
A[10]["a"] = ["like", "as"]
log.append("P4 B1: blank 8 reworded; blanks 3 and 10 widened")

# 10 — synthesis Q2 needed both tense backshift and an adverbial shift: P5/P6 work
x = q("B3", 2)
x["q"] = "\"I am bringing the tickets,\" said Priya. **(that)**"
x["m"] = "Priya said that she was bringing the tickets"
log.append("P4 B3 Q2: simplified to a single backshift")

# 11 — comprehension Q9 asked a P6 craft question
x = q("B4", 9)
x["q"] = "What does the last sentence tell us about how the narrator and Mr Pillai know each other?"
x["a"] = ("They have exchanged two written notes over three years, but the narrator has never heard Mr Pillai "
          "speak. It shows that they have got to know each other without a single spoken word.")
log.append("P4 B4 Q9: recast as content inference rather than craft evaluation")

# 12 — the passage was 277 words and abstract; make it longer and more concrete
p = S["B4"]["passage"]
insert_after = "The second time, I stayed for two hours.\n\n"
extra = ("What changed was a girl of about six at the shelf by the window. She had found a book about sharks "
         "and was holding it open with both arms because it was too big for her hands. She did not say "
         "anything. She simply turned it round and showed it to me, and I nodded, and she went back to "
         "reading. The whole exchange took four seconds and I have remembered it for three years.\n\n")
assert insert_after in p
S["B4"]["passage"] = p.replace(insert_after, insert_after + extra)
log.append(f"P4 B4: passage extended to {len(S['B4']['passage'].split())} words")
d["paper"]["totalMarks"] = sum(s["marks"] for s in d["paper"]["sections"])
fn.write_text(json.dumps(d, ensure_ascii=False), encoding="utf-8")

print("\n".join("  " + l for l in log))
for f in ("content_paper2d.json", "content_paper2e.json"):
    p = json.load(open(f))["paper"]
    print(f'\n{p["title"]}  {p["totalMarks"]} marks  {p["minutes"]} min')
    for s in p["sections"]:
        n = len(s.get("questions", s.get("answers", [])))
        chk = (sum(x.get("marks", 1) for x in s["questions"]) if s["mode"] in ("read", "self")
               else n)
        print(f'   {s["id"]:3s} {s["mode"]:5s} {s["marks"]:3d} marks  ({chk} from questions)'
              + ("  <-- MISMATCH" if chk != s["marks"] else ""))
