#!/usr/bin/env python3
"""Fixes from the seventh audit — vocabulary sets."""
import json, pathlib
fn = pathlib.Path("content_v7_vocab.json"); d = json.loads(fn.read_text(encoding="utf-8"))
S = {s["letter"]: s for s in d["sets"]}
log = []
def set_q(letter, n, **kw):
    q = next(x for x in S[letter]["questions"] if x["n"] == n)
    q.update(kw)
    if "options" in q and "correct" in q:
        q["m"] = q["options"][q["correct"]]; q["a"] = [q["m"]]
    elif "a" in kw:
        q["m"] = kw["a"][0]
    log.append(f"{letter}#{n}")

# ───────────── VA11 similes & proverbs
set_q("VA11", 8, options=["water", "glass", "crystal", "paper"], correct=2)
set_q("VA11", 31, q="The thief was as slippery as an __________ and slid away through the crowd.")

# ───────────── VA12 homophones: replace the pairs that are not true homophones
set_q("VA12", 16, q="The referee decided the tackle was __________ (fair / fare) and waved play on.",
      a=["fair"], tip="'Fair' means just; a 'fare' is the money you pay for a journey.")
set_q("VA12", 17, q="My grandmother paid the bus __________ (fair / fare) with her card.",
      a=["fare"], tip="A 'fare' is the cost of a journey.")
set_q("VA12", 18, q="From the top of the hill we could see the whole __________ (plane / plain).",
      a=["plain"], tip="A 'plain' is flat land; a 'plane' flies.")
set_q("VA12", 19, q="She took a quick __________ (peak / peek) at the last page.",
      a=["peek"], tip="A 'peek' is a quick look; a 'peak' is the top of a mountain.")
set_q("VA12", 34, q="Our team __________ (one / won) the final by a single goal.",
      a=["won"], tip="'Won' is the past of 'win'; 'one' is the number.")
set_q("VA12", 2, q="Please write your name on the line __________ (their / there / they're) is a space.",
      a=["there"], tip="'There is' points out that something exists.")

# ───────────── VA13 compound words: replace the four that are not compounds
set_q("VA13", 11, q="The part of the day after noon is called the after__________.",
      a=["noon"], tip="'Afternoon' is one word: after + noon.")
set_q("VA13", 21, q="Water that falls from the sky over a year is measured as rain__________.",
      a=["fall"], tip="'Rainfall' is one word.")
set_q("VA13", 24, q="A coat you put on in wet weather is a rain__________.",
      a=["coat"], tip="'Raincoat' is one word.")
set_q("VA13", 30, q="The sill at the bottom of a window is a window__________.",
      a=["sill"], tip="'Windowsill' is one word.")

# ───────────── VA14 feelings & character
set_q("VA14", 1, q="After weeks of practice, Devi was __________ when she heard she had come first, and could not stop grinning.",
      options=["elated", "content", "amused", "nervous"], correct=0)
set_q("VA14", 4, q="The referee's decision went against his team and left the coach __________.",
      options=["seething", "sheepish", "wistful", "delighted"], correct=0)
set_q("VA14", 7, q="He looked __________ at the photograph of his old school.",
      options=["wistfully", "wistful", "wistfulness", "wisely"], correct=0,
      tip="'Wistful' means sadly longing for something past. Because 'looked at' here means 'gazed at', the adverb 'wistfully' is needed.")
set_q("VA14", 15, q="The old lady was __________ to everyone who passed her stall, greeting each one with a smile and a joke.",
      options=["genial", "hostile", "aloof", "surly"], correct=0)
set_q("VA14", 31, options=["nagging", "fleeting", "trivial", "momentary"], correct=0)
set_q("VA14", 32, q="Her __________ laughter filled the corridor, and soon everybody else was laughing too.",
      options=["infectious", "grating", "hollow", "forced"], correct=0)
set_q("VA14", 35, q="She gave a __________ nod, plainly annoyed at being stopped, and walked on.",
      options=["grudging", "generous", "warm", "enthusiastic"], correct=0)

# ───────────── VA15 vivid verbs: fix the cue mismatch and the free items
set_q("VA15", 25, q="Instead of 'shone brightly', write that the trophy __________ under the lights.",
      options=["gleamed", "flickered", "glowed", "glinted"], correct=0,
      tip="'Gleamed' is a steady bright shine off a polished surface.")
set_q("VA15", 27, q="Instead of 'the water moved noisily', write that the water __________ over the rocks.",
      options=["gushed", "trickled", "seeped", "dripped"], correct=0,
      tip="'Gushed' shows fast, noisy flow; the others are all slow and quiet.")
set_q("VA15", 28, options=["erupted", "murmured", "muttered", "groaned"], correct=0)
set_q("VA15", 31, q="Instead of 'walked into something by accident', write that he __________ into the door frame.",
      options=["crashed", "edged", "stepped", "leaned"], correct=0)
set_q("VA15", 35, q="Instead of 'smelt strongly and unpleasantly', write that the bin __________ in the heat.",
      options=["reeked", "wafted", "lingered", "drifted"], correct=0,
      tip="'Reeked' means gave off a powerful bad smell.")
set_q("VA15", 36, q="Instead of 'shook with cold', write that she __________ at the bus stop.",
      options=["shivered", "swayed", "wobbled", "twitched"], correct=0)
set_q("VA15", 37, q="Instead of 'shook with fear', write that his hands __________ as he opened the envelope.",
      options=["trembled", "fidgeted", "drummed", "twisted"], correct=0)
set_q("VA15", 39, q="Instead of 'breathed with difficulty', write that the runner __________ at the finish line.",
      options=["gasped", "sighed", "yawned", "hummed"], correct=0)
set_q("VA15", 40, q="Instead of 'the fire burnt low', write that the fire __________ in the grate.",
      options=["smouldered", "blazed", "crackled", "roared"], correct=0,
      tip="'Smouldered' means burning slowly without flame; the other three are loud or bright.")

# ───────────── VA16 idioms
set_q("VA16", 11, q="Kumar has green fingers; his balcony is full of orchids.",
      tip="'Green fingers' (British and Singapore English) means a talent for gardening.")
set_q("VA16", 36, q="Whether pupils may use their phones during breaks is a grey area in the rules.")
set_q("VA16", 40, q="The video was unknown on Monday; by Friday she had become famous overnight.",
      options=["suddenly", "slowly", "secretly", "easily"], correct=0,
      tip="'Overnight' means very suddenly, in a very short time.")

# ───────────── VA18 precise words
set_q("VA18", 23, q="The cleaner worked with a __________ that left not one corner dusty.")

# ───────────── VA17 vocabulary cloze: fix the one wrong key and widen the open blanks
A = {a["n"]: a for a in S["VA17"]["answers"]}
WIDEN = {
 2: ["repaired", "mended", "fixed"],
 3: ["customers", "clients", "regulars"],
 6: ["cheaper", "easier", "quicker", "simpler"],
 7: ["explained", "replied", "answered", "pointed out"],
 8: ["regular", "loyal", "faithful"],
 10: ["queue", "crowd"],
 11: ["brought", "gave"],
 12: ["trade", "craft", "work", "business"],
 14: ["remember", "miss", "recall"],
 15: ["trade", "corner", "job", "business"],
 17: ["observe", "watch", "study"],
 18: ["avoid", "refuse", "shun"],
 19: ["reason", "answer", "explanation", "cause"],
 20: ["trapped", "stuck"],
 21: ["control", "power", "choice", "a say"],
 23: ["crowded", "full", "packed"],
 24: ["gradually", "slowly", "steadily"],
 25: ["noticed", "watched", "seen", "observed"],
 26: ["claim", "choose", "grab", "want"],
}
for n, acc in WIDEN.items():
    A[n]["a"] = acc; log.append(f"VA17#{n}→{len(acc)}")
# blank 4 had no basis for "patiently" — re-cue the sentence
p = S["VA17"]["passages"][0]
old = "He worked (4)______, threading a needle without once holding it up to the light."
assert old in p["text"], "VA17 blank 4"
p["text"] = p["text"].replace(old,
  "He worked slowly and (4)______, never once losing his temper with a tangled rib.")
A[4]["a"] = ["patiently", "calmly"]
log.append("VA17#4 re-cued")

fn.write_text(json.dumps(d, ensure_ascii=False), encoding="utf-8")
print("vocabulary fixes applied:", len(log))
print("  " + " · ".join(log))
