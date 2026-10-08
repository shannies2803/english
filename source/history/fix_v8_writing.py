#!/usr/bin/env python3
"""Fixes from the eighth audit — compositions, situational writing and oral."""
import json, pathlib
log = []

# ─────────────────── the eight full compositions
fn = pathlib.Path("content_v8_writing.json"); d = json.loads(fn.read_text(encoding="utf-8"))
T = {t["n"]: t for t in d["composition2"]["tasks"]}

# 1 — Comp 1 contradicted itself and ran over its own word limit
T[1]["model"] = T[1]["model"].replace(
    "so quietly that nobody in the corridor had even turned round",
    "so quietly that nobody came running")
T[1]["model"] = T[1]["model"].replace(
    "I had been in the school office twice before, both times to collect something. The third time was different.\n\n"
    "It started with a football, a science corridor and a window that had been cracked, not smashed, so quietly "
    "that nobody came running. I stood with the ball still in my hands and waited for somebody to shout. Nobody "
    "did. The corridor stayed empty. After about ten seconds I walked away.\n\n",
    "I had been in the school office twice before, both times to collect something. The third time was different.\n\n"
    "It began with a football and a window that cracked, rather than smashed, so quietly that nobody came running. "
    "I stood with the ball in my hands and waited for somebody to shout. Nobody did. After about ten seconds I "
    "walked away.\n\n")
log.append(f"Comp 1: contradiction removed, now {len(T[1]['model'].split())} words")

# 2 — Geography is a secondary subject in Singapore; primary pupils do Social Studies
T[2]["model"] = T[2]["model"].replace("the geography project", "the Social Studies project")
# 3 — the phone was never actually in the scene, unlike every other model's picture object
T[2]["model"] = T[2]["model"].replace(
    "\"It's one message,\" she said. \"Just say yes.\"",
    "She held out her phone with the message already typed. All I had to do was press send from my own.\n\n"
    "\"It's one message,\" she said. \"Just say yes.\"")
log.append("Comp 2: Social Studies; the phone now appears in the scene")

# 4 — Comp 7: the brother had been visiting the cat during the 'perfect' first two days
T[7]["why"] = T[7]["why"].replace(
    "The structure is excellent: two easy days, then the slip,",
    "The structure is excellent: two days that only looked easy — note that he had already been visiting the "
    "cat for three days — then the slip,")
log.append("Comp 7: the 'why' note now accounts for the three days")

# 5 — Comp 3's advice would cost marks on a prompt phrased 'a time when YOU...'
T[3]["why"] += (" One caution: this works because the prompt does not say \"you\". Check the wording of your own "
                "prompt first — if it asks about you, you must be at the centre of the story.")
log.append("Comp 3: caveat added about prompts phrased 'a time when you…'")

# 6 — every model was P6 length, so a P5 pupil had nothing at their own target
for n in (4, 5):
    t = T[n]
    t["p5model"] = None
T[4]["p5model"] = (
 "The drinks auntie at our hawker centre is Mdm Chong, and she has never got my order wrong in four years.\n\n"
 "Last November I went down for lunch on the day my mother's wallet had been stolen. I had two dollars and "
 "forty cents. The chicken rice was three dollars.\n\n"
 "I stood there for about four seconds. It felt much longer, and I could hear the queue behind me.\n\n"
 "Then a hand came past my shoulder and put a coin on the counter. Mdm Chong had left her own stall to do it.\n\n"
 "I tried to pay her back the next day. She refused twice, and the second time she was annoyed, so I stopped "
 "trying.\n\nWhat I do instead is buy my drink from her every single day, even when her queue is the longer one. "
 "I have done that for ten months. I do not think she has noticed, and that is not really the point.")
T[5]["p5model"] = (
 "The box was under the bed in the spare room, and it was full of old school reports.\n\n"
 "They were my father's, from Primary 1 to Secondary 4, held together with a rubber band that snapped when I "
 "touched it.\n\nMy father is an engineer. He checks his work twice. He has told me more than once that "
 "carelessness is a choice.\n\nIn Primary 4 he was ranked thirty-first out of thirty-eight.\n\n"
 "His teacher had written: *Kumar is a bright boy who has decided that he is not.*\n\n"
 "Underneath, in different ink, somebody had added the date 1987 and the words *she did*.\n\n"
 "I put everything back exactly as I had found it and have never mentioned it. But when he tells me off about "
 "carelessness now, I listen differently. He is not repeating a rule. He is passing on something that happened "
 "to him.")
d["composition2"]["instruction"] += (
 " Two of the tasks also carry a shorter Primary 5 model, to show how the same story is told in about 170 words.")
log.append(f"Comps 4 and 5: P5-length models added "
           f"({len(T[4]['p5model'].split())} and {len(T[5]['p5model'].split())} words)")
fn.write_text(json.dumps(d, ensure_ascii=False), encoding="utf-8")

# ─────────────────── P4 situational writing and the oral stimuli
fn = pathlib.Path("content_v8_writing_oral.json"); d = json.loads(fn.read_text(encoding="utf-8"))
SW = d["situational4"]
# 7 — no word target, and two models ran to P6 length
SW["instruction"] = ("Write about 60 to 80 words. Cover all three points, each with one supporting detail. "
                     "Marks: 6 for task fulfilment, 4 for language and format.")
for t in SW["tasks"]:
    t["task"] += "\n\nWrite about 60 to 80 words."
T4 = {t["n"]: t for t in SW["tasks"]}
T4[4]["model"] = (
 "To: ah_gong@email.com\nSubject: Come to my Sports Day!\n\nDear Ah Gong,\n\n"
 "Our school Sports Day is on Saturday 12 July, from 8 a.m. to 12 noon, on the school field.\n\n"
 "I am running in the 100 metres at about 9.15, and I am in the class relay, which is the last event.\n\n"
 "You can take bus 156 from your block and get off at the fourth stop, right outside our gate. If you would "
 "rather not, my father can fetch you at half past seven.\n\nPlease come!\n\nLove,\nSarah")
T4[6]["model"] = (
 "To: jia_wei@email.com\nSubject: Our trip to the wetland reserve\n\nHi Jia Wei,\n\n"
 "You missed a good one. Last Thursday our level went to the wetland reserve at Sungei Buloh.\n\n"
 "The best part was the mudskippers. One hopped onto a root a metre from the boardwalk and sat staring at us.\n\n"
 "The thing that went wrong was our worksheet. Faizal put it on the railing for one second and the wind took it "
 "into the water, so we redid it from memory on the bus.\n\nHow is your new school?\n\nYour friend,\nDinesh")
log.append(f"P4 situational: word target added; tasks 4 and 6 cut to "
           f"{len(T4[4]['model'].split())} and {len(T4[6]['model'].split())} words")

# 8 — two oral stimuli were labelled P3 but demanded percentage reasoning
for c in d["oral3"]:
    if c["id"] in ("sbcK", "sbcL"): c["level"] = "P4"
log.append("oral sbcK and sbcL relabelled P4 to match their demand")

# 9 — two read-aloud notes described the wrong sentence
RA = {r["id"]: r for r in d["readAloud3"]}
RA["ra13"]["notes"][1] = ("Pause at the commas in the fifth sentence (“He eats cabbage on Thursdays…”). "
                          "It has three parts.")
RA["ra14"]["notes"][2] = "Final consonants: recorded, imitating, worked, mark, machine."
log.append("read-aloud notes ra13 and ra14 corrected against their passages")
fn.write_text(json.dumps(d, ensure_ascii=False), encoding="utf-8")
print("\n".join("  " + l for l in log))
