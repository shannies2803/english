#!/usr/bin/env python3
"""Fixes from the seventh audit — grammar sets."""
import json, pathlib, sys
fn = pathlib.Path("content_v7_grammar.json"); d = json.loads(fn.read_text(encoding="utf-8"))
S = {s["letter"]: s for s in d["sets"]}
def Q(letter, n):
    return next(q for q in S[letter]["questions"] if q["n"] == n)
def A(letter, n):
    return next(a for a in S[letter]["answers"] if a["n"] == n)
log = []
def set_q(letter, n, **kw):
    q = Q(letter, n)
    if "a" in kw and "m" not in kw: kw["m"] = kw["a"][0]
    q.update(kw); log.append(f"{letter}#{n}")

# ───────────── GA13 articles & determiners
set_q("GA13", 27, q="__________ (Neither / None / Both) of the two answers is correct — they contradict each other.",
      a=["Neither"], tip="'Neither' is used for two things and takes a singular verb.")
set_q("GA13", 29, q="I could not decide between the two, so in the end I took __________ (either / neither / both) book.",
      a=["neither"], tip="'Neither' means not one and not the other of the two.")
set_q("GA13", 38, tip="'The Science Centre' is one particular place the reader already knows, so it takes 'the'.")

# ───────────── GA14 conjunctions (P3): remove leaks and lift out the off-level items
set_q("GA14", 10, q="__________ (When / But / Or) the bell rang, everyone stood up.",
      a=["When"], tip="'When' shows the time at which something happened.")
set_q("GA14", 19, q="The soup was too salty, __________ (but / or / because) nobody complained.",
      a=["but"], tip="Two main clauses in contrast are joined by 'but'.")
set_q("GA14", 27, q="Jaya sings well. __________ (However / Because / And), she is shy on stage.",
      a=["However"], tip="'However' starts a new sentence and takes a comma after it.")
set_q("GA14", 28, q="It was crowded. __________ (But / Because / So) we found seats in the end.",
      a=["But"], tip="'But' shows the contrast between the two sentences.")
set_q("GA14", 32, q="Wash your hands __________ (before / because / or) you eat, so that no dirt gets on your food.",
      a=["before"], tip="The clause 'so that no dirt gets on your food' tells you the washing comes first.")
set_q("GA14", 35, q="I like durian __________ (but / because / so) my mother cannot stand it.",
      a=["but"], tip="'But' joins two ideas that disagree.")
set_q("GA14", 36, q="The pupils cheered __________ (when / but / or) the goal was scored.",
      a=["when"], tip="'When' shows that the two things happened at the same moment.")
set_q("GA14", 38, q="__________ (Although / However / Because) she tried very hard, she could not open the jar.",
      a=["Although"], tip="'Although' shows a contrast and comes at the start of the clause.")

# ───────────── GA15 comparatives: make superlative adverbs consistent with item 12
set_q("GA15", 28, q="He arrived __________ of all the guests.",
      options=["latest", "late", "later", "more late"], correct=0,
      a=["latest"], m="latest", tip="A superlative adverb normally has no 'the': 'fastest', 'latest', 'hardest'.")

# ───────────── GA17 conditionals: replace the inverted formal conditional
set_q("GA17", 25, q="__________ (If / Unless / Should) you have any problems, please call me.",
      a=["If"], tip="'If' introduces the condition. (In very formal writing you may also see 'Should you have any problems'.)")

# ───────────── GA18 subject–verb agreement
set_q("GA18", 11, q="There __________ (is / are) a pen and two rulers on the desk.",
      a=["are", "is"], m="are",
      tip="With a compound subject, careful written English uses 'are'. You will also hear 'There is a pen and two rulers', which follows the nearer noun.")
set_q("GA18", 21, q="The committee __________ (is / are) meeting this afternoon.",
      a=["is"], tip="A committee acting as one body takes a singular verb.")
set_q("GA18", 38, q="Most of the pupils __________ (has / have) handed in their forms.",
      a=["have"], tip="'Pupils' is plural, so the fraction word takes a plural verb.")

# ───────────── GA20 synthesis: one wrong tip
set_q("GA20", 31, tip="'Which' after a comma adds extra information about the noun 'library'.")

# ───────────── GA21 spelling: two wrong tips, three stems that fit another keyed word
set_q("GA21", 8, q="The laws of a country are made by its __________.",
      a=["government"], tip="There is an n before the m: govern-ment.")
set_q("GA21", 22, q="My mother and her __________ share an office at work.",
      a=["colleague"], tip="-eague at the end: col-league.")
set_q("GA21", 23, tip="Four vowels in a row after the q: q-u-e-u-e.")
set_q("GA21", 31, q="My uncle studied accounting and now runs his own __________.",
      a=["business"], tip="busi-ness, from 'busy'.")
set_q("GA21", 40, tip="Silent c at the start, and a double s in the middle: sci-ssors.")

# ───────────── GA22 editing: two rule violations, one double error, four leaks
set_q("GA22", 4, q="Passage 14 — My sister said that the food there was gooder than anything at home.",
      a=["better"], tip="The error was “gooder”. The comparative of 'good' is 'better'.")
set_q("GA22", 6, q="Passage 14 — All the stalls had they own speciality.",
      a=["their"], tip="The error was “they”. A possessive is needed before 'own'.")
set_q("GA22", 7, q="Passage 14 — We looked forward to bring the pineapple tarts home to our grandparents.",
      a=["bringing"], tip="The error was “bring”. After 'look forward to' the verb takes the -ing form.")
set_q("GA22", 8, q="Passage 14 — The hotel owner showed us a museum that we would never had found alone.",
      a=["have"], tip="The error was “had”. After 'would' the verb is 'have'.")
set_q("GA22", 21, q="Passage 16 — I have went there every Saturday since January.",
      a=["gone"], tip="The error was “went”. After 'have' the past participle is 'gone'.")
set_q("GA22", 33, q="Passage 17 — Every day she wake up at four o'clock to catch the first bus.",
      a=["wakes"], tip="The error was “wake”. 'She' takes the -s form for a habit.")
set_q("GA22", 35, q="Passage 17 — Since then, our class have kept its own floor tidy.",
      a=["has"], tip="The error was “have”. 'Its' shows the class is being treated as one body, so the verb is 'has'.")

# ───────────── GA23 grammar cloze: widen the accepted answers on the open blanks
WIDEN = {
 4: ["Then", "Suddenly", "Soon"],
 5: ["Within", "After", "In"],
 6: ["were", "had"],
 12: ["could", "would"],
 17: ["one"],                      # re-cued below
 22: ["because", "that"],
 25: ["Everybody", "Everyone"],
 27: ["Now", "Today", "Nowadays"],
 28: ["her", "a", "his"],
 30: ["would", "will", "might"],
}
for n, accepted in WIDEN.items():
    a = A("GA23", n); a["a"] = accepted; log.append(f"GA23#{n} accepts {len(accepted)}")
# blank 17 re-cued in the passage so only "one" works
p = S["GA23"]["passages"][1]
old = "There is (17)______ rule in it, and only one."
assert old in p["text"], "GA23 blank 17 text"
p["text"] = p["text"].replace(old, "There is just (17)______ rule in it, and only one.")
log.append("GA23#17 re-cued")

fn.write_text(json.dumps(d, ensure_ascii=False), encoding="utf-8")
print("grammar fixes applied:", len(log))
print("  " + " · ".join(log))
