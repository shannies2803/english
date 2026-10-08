#!/usr/bin/env python3
"""Fixes from the seventh audit — comprehension."""
import json, pathlib, re
fn = pathlib.Path("content_v7_comprehension.json"); d = json.loads(fn.read_text(encoding="utf-8"))
P = {p["title"]: p for p in d["passages"]}
log = []
def q(title, n): return next(x for x in P[title]["questions"] if x["n"] == n)

# ── 1. the marks are already a field; stop repeating them in the question text
n = 0
for p in d["passages"]:
    for x in p["questions"]:
        new = re.sub(r"\s*\(\d+m\)\s*$", "", x["q"])
        if new != x["q"]: x["q"] = new; n += 1
log.append(f"stripped duplicated mark labels from {n} questions")

# ── 2. The Wrong Trophy Q1 — model contradicted the passage's own resolution
q("The Wrong Trophy", 1)["a"] = ("It bore the name MEI LING TAN, not her own name MEI LING TANG. "
    "The plate on her trophy was in fact the other girl's name plate.")
q("The Wrong Trophy", 6)["tip"] = ("Look at what each girl does once the mistake is discovered, not at "
    "what either of them says.")
log.append("Wrong Trophy Q1 model corrected, Q6 tip filled")

# ── 3. Bottled Water Q8 — the model claimed something the passage never says
x = q("The Case Against Bottled Water", 8)
x["a"] = x["a"].replace(" or government action", "")
log.append("Bottled Water Q8: removed unsupported 'government action'")

# ── 4. two-mark questions whose models listed more points than the marks allow
x = q("The New Boy", 5)
x["a"] = "Any two of: he had moved from Chennai six weeks earlier; he had an older sister already at secondary school; he could name every bone in the human hand."
x["tip"] = "Two facts are asked for. Any two of the three will do."
x = q("Why Some Animals Play Dead", 6)
x["a"] = "Any two of: it cannot feed while it lies still; it cannot escape if a second attacker arrives; it cannot protect its young; it is useless against a predator that hunts by smell."
x["tip"] = "Two disadvantages are asked for. Any two will do."
log.append("New Boy Q5 and Play Dead Q6 keyed as 'any two of'")

# ── 5. The Metronome Q8 tip misquoted the passage
q("The Metronome", 8)["tip"] = ("The last point is about the force of 'I have not been able to make myself "
    "stop' — far stronger than simply saying he still does it.")
log.append("Metronome Q8 tip corrected")

# ── 6. mark schemes invented a narrator's gender the passages never state
for title, subs in {
  "The New Boy": [("he ", "the narrator "), (" his ", " the narrator's ")],
  "The Metronome": [("he ", "the narrator "), (" his ", " the narrator's ")],
}.items():
    for x in P[title]["questions"]:
        for a, b in subs:
            x["a"] = x["a"].replace(" " + a, " " + b)
log.append("narrator pronouns neutralised in two mark schemes")

# ── 7. one vocabulary-in-context question per passage (only 1 in 48 before)
VOCAB = {
 "The New Boy": (9, 1, "Which word in the passage tells you that Arjun spoke very quietly?",
   "'Mumbled'.", "Look for the verb describing how he said his name."),
 "The Wrong Trophy": (9, 1, "Which word in the passage means 'put off until later'?",
   "'Postponed'.", "It describes what happened to the prize-giving."),
 "The Metronome": (9, 1, "Which word in the passage means 'strange or unusual in an amusing way'?",
   "'Eccentric'.", "It is used to describe the teacher."),
 "The Letter She Never Sent": (9, 1, "Which word in the passage means 'a thing kept because of the memories attached to it'?",
   "'Keepsake'.", "Look in the paragraph about the drawer."),
 "The Case Against Bottled Water": (9, 1, "Which word in the passage means 'able to be broken down naturally'?",
   "'Biodegradable'.", "Look in the paragraph about what happens to the plastic."),
 "Why Some Animals Play Dead": (9, 1, "Which word in the passage means 'happening without being decided'?",
   "'Involuntary'.", "Look in the paragraph explaining that the animal does not choose to do it."),
}
added = []
for title, (n, marks, text, ans, tip) in VOCAB.items():
    body = " ".join(P[title]["text"]).lower()
    word = ans.strip("'.").lower()
    if word in body:
        P[title]["questions"].append({"n": n, "q": text, "a": ans, "marks": marks, "tip": tip})
        added.append(f"{title[:22]}→{word}")
    else:
        added.append(f"SKIP {title[:22]} ({word} not in passage)")
log.append("vocabulary-in-context: " + "; ".join(added))

fn.write_text(json.dumps(d, ensure_ascii=False), encoding="utf-8")
print("\n".join("  " + l for l in log))
