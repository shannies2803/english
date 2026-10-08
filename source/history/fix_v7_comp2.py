#!/usr/bin/env python3
"""Level fixes: relabel The New Boy to P4, add a genuine P3 passage, extend three short passages."""
import json, pathlib
fn = pathlib.Path("content_v7_comprehension.json"); d = json.loads(fn.read_text(encoding="utf-8"))
P = {p["title"]: p for p in d["passages"]}
def wc(p): return sum(len(x.split()) for x in p["text"])

# ── 1. The New Boy is 363 words with author's-craft questions: that is P4 work, not P3
P["The New Boy"]["level"] = "P4"
P["The New Boy"]["words"] = wc(P["The New Boy"])

# ── 2. extend the three passages that fall short of their level's word count
EXTRA = {
 "The Case Against Bottled Water": [(5,
   "There is a second cost that rarely appears on any label. Producing the plastic for a single "
   "one-litre bottle uses roughly three litres of water, most of it in the factory rather than in "
   "the bottle. A drink sold on the promise of purity therefore costs several times its own volume "
   "before it reaches a shelf.")],
 "The Metronome": [(11,
   "I asked her once, in my fifth year, why she never said anything was good. She thought about it "
   "for long enough that I wished I had not asked. Then she said that there were a great many people "
   "who would tell me I was wonderful, and that they would all be trying to be kind, and that being "
   "kind and being useful were not always the same errand. She said I had one hour a week with "
   "somebody whose only job was to be useful, and that she did not intend to waste it.")],
 "The Letter She Never Sent": [(8,
   "Once, about four years ago, my mother took the box down and put it on the kitchen table, and we "
   "both sat and looked at it for perhaps ten minutes. Then she carried it back to the wardrobe "
   "without either of us saying anything. We have not mentioned that afternoon since, and I am not "
   "sure which of us decided.")],
}
for title, inserts in EXTRA.items():
    p = P[title]
    for at, para in sorted(inserts, reverse=True):
        p["text"].insert(at, para)
    p["words"] = wc(p)

# ── 3. a genuine P3 passage: short sentences, concrete events, mostly literal questions
NEW_P3 = {
 "id": "cmpU", "title": "The Egg in the Drain", "level": "P3", "kind": "Narrative",
 "text": [
  "On Saturday morning, my sister Nadia and I heard a noise outside our flat.",
  "It was a small sound. It went cheep, then stopped, then cheep again.",
  "We looked over the corridor railing. We looked behind the bicycles. We looked under the letter boxes. We could not find it anywhere.",
  "Then Nadia lay down flat on the floor and put her ear against the drain cover.",
  "\"It is in here,\" she said.",
  "The drain cover was a metal grid with narrow slots. Through the slots we could see something small and grey. It was a baby bird. It had fallen through the grid and could not get out again.",
  "I tried to lift the cover. It was far too heavy for me. Nadia tried as well, and then we tried together, and it did not move at all.",
  "\"We need an adult,\" Nadia said.",
  "Our father was asleep, because he had worked at night. Our mother had gone to the market. So we went to the flat next door and knocked.",
  "Uncle Ravi opened the door with a newspaper in his hand. We told him about the bird. He came out in his slippers, looked through the slots, and went back inside without a word.",
  "For a moment I thought he did not care.",
  "Then he came back with a screwdriver and a torch.",
  "It took him five minutes to lift the cover. The bird was frightened and hopped away from his hands. Nadia held her jacket open like a net, and Uncle Ravi guided the bird into it, and then it was out.",
  "We put the bird in a shoebox with an old towel. Uncle Ravi telephoned the bird rescue centre. A lady came in a small white van at four o'clock and took the box away.",
  "She told us the bird was a mynah chick. She said it would be fed every two hours and released when it could fly.",
  "That evening, our father woke up and asked what we had done all day.",
  "Nadia said, \"Nothing much.\"",
  "I did not say anything either. But I have thought about it many times since, and I still remember how heavy that drain cover was, and how light the bird was in the jacket."],
 "questions": [
  {"n": 1, "q": "Where were Nadia and the narrator when they first heard the noise?", "a": "They were at their flat, and the sound came from outside in the corridor.", "marks": 1, "tip": "Look at the first two paragraphs."},
  {"n": 2, "q": "Give two places the children searched before they found the bird.", "a": "Any two of: over the corridor railing; behind the bicycles; under the letter boxes.", "marks": 2, "tip": "Two places are asked for. Any two will do."},
  {"n": 3, "q": "How did Nadia work out where the bird was?", "a": "She lay down flat on the floor and put her ear against the drain cover.", "marks": 1, "tip": "She used her ears, not her eyes."},
  {"n": 4, "q": "Why could the children not rescue the bird by themselves?", "a": "The metal drain cover was far too heavy for them to lift, even when they tried together.", "marks": 2, "tip": "Look at what happened when they both tried."},
  {"n": 5, "q": "Why did they go to Uncle Ravi instead of asking their own parents?", "a": "Their father was asleep after working at night, and their mother had gone to the market.", "marks": 2, "tip": "Both parents are accounted for in the same paragraph."},
  {"n": 6, "q": "Why did the narrator think for a moment that Uncle Ravi did not care?", "a": "Because he looked through the slots and then went back inside without saying anything, so it seemed as though he was ignoring them. In fact he had gone to fetch a screwdriver and a torch.", "marks": 2, "tip": "Say what the narrator thought, and then what was really happening."},
  {"n": 7, "q": "What did Nadia do to help catch the bird?", "a": "She held her jacket open like a net so that Uncle Ravi could guide the bird into it.", "marks": 1, "tip": "Look at the paragraph about lifting the cover."},
  {"n": 8, "q": "What two things did the lady from the rescue centre say would happen to the bird?", "a": "It would be fed every two hours, and it would be released when it was able to fly.", "marks": 2, "tip": "Both facts are in the same short paragraph."},
  {"n": 9, "q": "Which word in the passage means 'thin openings'?", "a": "'Slots'.", "marks": 1, "tip": "It describes the gaps in the drain cover."},
  {"n": 10, "q": "The narrator remembers 'how heavy that drain cover was, and how light the bird was'. Why do you think he remembers those two things together?", "a": "Because they are opposites, and putting them side by side shows how much effort went into saving something so small. It suggests that the size of the trouble was worth it.", "marks": 2, "tip": "Think about why a writer would put a heavy thing and a light thing in the same sentence."},
 ]}
assert "slots" in " ".join(NEW_P3["text"]).lower()
NEW_P3["words"] = wc(NEW_P3)
d["passages"].append(NEW_P3)

fn.write_text(json.dumps(d, ensure_ascii=False), encoding="utf-8")
TARGET = {"P3": (200, 320), "P4": (280, 420), "P5": (380, 520), "P6": (420, 620)}
print(f'{"level":6s}{"words":>7s}  {"fits":5s}  title')
for p in d["passages"]:
    lo, hi = TARGET[p["level"]]; w = wc(p)
    print(f'{p["level"]:6s}{w:7d}  {"yes" if lo <= w <= hi else "NO":5s}  {p["title"]}  '
          f'({len(p["questions"])}q, {sum(q["marks"] for q in p["questions"])} marks)')
