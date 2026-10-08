#!/usr/bin/env python3
"""Fixes from the eighth audit — the v8 grammar and vocabulary sets."""
import json, pathlib
log = []

# ─────────────────────────────────────── grammar
fn = pathlib.Path("content_v8_grammar.json"); d = json.loads(fn.read_text(encoding="utf-8"))
S = {s["letter"]: s for s in d["sets"]}
def setq(letter, n, **kw):
    q = next(x for x in S[letter]["questions"] if x["n"] == n)
    q.update(kw)
    if "options" in q and "correct" in q: q["m"] = q["options"][q["correct"]]; q["a"] = [q["m"]]
    elif "a" in kw: q["m"] = kw["a"][0]
    log.append(f"{letter}#{n}")

# GA24 — two stems were not actually non-standard, and two tips taught the wrong thing
setq("GA24", 16, q="Everyday speech: *Kindly take note the deadline.*",
     options=["Please note the deadline.", "Kindly take note the deadline.",
              "Please kindly take note the deadline.", "Please take note the deadline."], correct=0,
     tip="'Take note' needs 'of'; the standard written form is simply 'Please note'.")
setq("GA24", 39, q="Everyday speech: *Next time onwards I will remember.*",
     options=["In future I will remember.", "Next time onwards I will remember.",
              "From next time onwards I will remember.", "Next time onward I will remember."], correct=0,
     tip="'Next time onwards' is not standard; use 'in future' or 'from now on'.")
setq("GA24", 21, tip="The verb needs the past tense: 'scolded'. ('Just now' for a moment ago is acceptable; "
                     "what is non-standard is using it for any earlier time.)")
setq("GA24", 9, options=["My mobile phone has stopped working.", "My handphone spoil already.",
                         "My handphone is spoil.", "My handphone already spoiled."], correct=0,
     tip="'Spoil' for a device becomes 'break' or 'stop working'; 'handphone' is 'mobile phone' in formal writing.")

# GA25 — three items accepted only one of two defensible verbs; one tip was false
setq("GA25", 14, q="We sat and __________ (watched / saw) the whole match on television last night.",
     a=["watched"], tip="'Watch' means to follow something over time; 'see' is a single act of noticing.")
setq("GA25", 17, q="The noise from upstairs __________ (disturbed / troubled) my sleep all night.",
     a=["disturbed"], tip="'Disturb somebody's sleep' is the set phrase.")
setq("GA25", 18, q="He __________ (spent / used) all his pocket money on a comic yesterday.",
     a=["spent"], tip="You spend money ON something. 'Spend' is the verb for paying money out.")
setq("GA25", 35, q="He __________ (kicked / knocked) the ball hard with his right foot and it hit the fence.",
     a=["kicked"], tip="A ball struck with the foot is kicked.")

# GA26 — one item printed "just" twice; two accepted only the perfect where both forms work
setq("GA26", 11, q="They __________ (just left / have just left) the building.",
     a=["have just left"], tip="'Just' for something a moment ago takes the present perfect.")
setq("GA26", 9, q="He __________ (lost / has lost) his keys and has not found them yet.",
     a=["has lost"], tip="'Not yet' means the search is still going on, so use the present perfect.")
setq("GA26", 21, q="She __________ (broke / has broken) her leg and is still in plaster.",
     a=["has broken"], tip="'Is still in plaster' shows the result continues, so use the present perfect.")
fn.write_text(json.dumps(d, ensure_ascii=False), encoding="utf-8")

# ─────────────────────────────────────── vocabulary
fn = pathlib.Path("content_v8_vocab.json"); d = json.loads(fn.read_text(encoding="utf-8"))
S = {s["letter"]: s for s in d["sets"]}

# VA19 (P3) — two items had no discriminator; one word was above level
setq("VA19", 16, q="We waited at the bus __________ outside our block for ten minutes, but only taxis went past.",
     options=["stop", "station", "park", "shelter"], correct=0,
     tip="A bus picks up passengers at a bus stop; a bus station is where many routes begin.")
setq("VA19", 37, q="We washed our __________ before we ate.",
     options=["hands", "hand", "handed", "hanged"], correct=0, tip="'Our hands' takes the plural.")
setq("VA19", 17, q="The soup needs more salt because it tastes of __________.",
     options=["nothing", "everything", "anything", "something"], correct=0,
     tip="'Tastes of nothing' means it has no taste at all.")

# VA20 (P4) — one wrong key, four items with no clue, three free items
setq("VA20", 8, q="The soup was __________; we finished it, but nobody asked for more.",
     options=["tasty", "delicious", "superb", "mouth-watering"], correct=0,
     tip="'Tasty' is moderate praise; the other three all claim far more than 'nobody asked for more'.")
setq("VA20", 6, q="I was __________ by the noise from the flat above, though I soon got used to it.",
     options=["annoyed", "enraged", "devastated", "horrified"], correct=0,
     tip="'Soon got used to it' shows the feeling was mild.")
setq("VA20", 7, q="The referee was __________ when the player spat at him, and sent him off at once.",
     options=["enraged", "annoyed", "irritated", "cross"], correct=0,
     tip="Spitting at a person and an instant sending-off point to the strongest word.")
setq("VA20", 11, q="The path was __________ in places, but never so sharp that we had to use our hands.",
     options=["sloping", "steep", "sheer", "vertical"], correct=0,
     tip="'Never so sharp that we needed our hands' rules out the three stronger words.")
setq("VA20", 12, q="He gave the door a __________ push and it swung open without a sound.",
     options=["gentle", "violent", "savage", "furious"], correct=0,
     tip="'Without a sound' shows the push was soft.")
setq("VA20", 15, q="The old bridge was so __________ that two planks gave way as we crossed.",
     options=["rickety", "unsteady", "wobbly", "creaky"], correct=0,
     tip="All four describe a poor bridge, but only 'rickety' carries the sense of falling apart.")
setq("VA20", 16, q="He is __________ of his sister's exam results and tells everyone how hard she worked.",
     options=["proud", "jealous", "envious", "resentful"], correct=0,
     tip="Telling everyone how hard she worked shows pleasure at her success, not envy.")
setq("VA20", 25, q="The crowd was __________ when the goal was disallowed, but nobody left their seat.",
     options=["annoyed", "furious", "enraged", "incensed"], correct=0,
     tip="'Nobody left their seat' shows the anger stopped short of the three stronger words.")
setq("VA20", 33, q="The shop was __________; one customer stood at the counter and nobody else.",
     options=["quiet", "deserted", "empty", "abandoned"], correct=0,
     tip="One customer means it was not deserted or empty — only quiet.")
setq("VA20", 34, q="The train was __________; we had to stand but there was room to turn round.",
     options=["full", "packed", "crammed", "jammed"], correct=0,
     tip="'Room to turn round' rules out the three stronger words.")
setq("VA20", 37, q="The old photograph had __________ a little, though the faces were still clear.",
     options=["faded", "vanished", "disappeared", "dissolved"], correct=0,
     tip="'Still clear' shows only slight loss of colour.")
setq("VA20", 40, q="Her voice was __________ with excitement, though she was trying hard to sound calm.",
     options=["trembling", "steady", "flat", "level"], correct=0,
     tip="'Trying hard to sound calm' shows she was not succeeding.")

# VA21 (P5) — four connectors had a second natural answer; one item was P1 work
setq("VA21", 10, q="We had planned to work in the library, but it was shut. __________ (Instead / Moreover / Therefore), we worked in the canteen.",
     a=["Instead"], tip="'Instead' introduces what was done in place of the original plan.")
setq("VA21", 14, q="We have settled the costs and the timetable. __________ (Finally / Firstly / Meanwhile), I would like to thank the volunteers.",
     a=["Finally"], tip="Two points have already been made, so this is the last one.")
setq("VA21", 15, q="The road will be resurfaced from June until August. __________ (In the meantime / Consequently / Similarly), buses will use Jalan Bahru.",
     a=["In the meantime"], tip="'In the meantime' means during that period.")
setq("VA21", 19, q="The shop sells bread and cakes __________ (but / and / or) no longer bakes biscuits.",
     a=["but"], tip="The second idea contradicts what you would expect from the first.")
setq("VA21", 24, q="I have three things to tell you. __________ (To begin with / Finally / Meanwhile), let me explain why the trip was cancelled.",
     a=["To begin with"], tip="Three points are promised, so this is the first of them.")
fn.write_text(json.dumps(d, ensure_ascii=False), encoding="utf-8")
print(f"{len(log)} items fixed:  " + " · ".join(log))
