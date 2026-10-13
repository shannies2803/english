import json, pathlib

P = []

# ───────────────────────────── P3 narrative · The Shortcut
P.append({"id":"cmpZE","title":"The Shortcut","level":"P3","kind":"Narrative","text":[
 "There are two ways from my block to the school gate.",
 "The long way goes round the carpark, past the provision shop and up the ramp. It takes eleven minutes. I know, because I have counted.",
 "The short way goes through a gap in the hedge, across a strip of grass and over a low wall. It takes four.",
 "My mother has told me twice not to use it. She says the wall is higher on the other side than it looks.",
 "On Tuesday I woke up late.",
 "I ran down the stairs with my shoes in my hand and one sock on. The lift was busy. By the time I reached the hedge it was twenty-five past seven, and assembly begins at half past.",
 "I went through the gap.",
 "The grass was wet, which I had not expected, and my socks were soaked before I had taken five steps. At the wall I put one hand down, swung my legs over, and landed badly.",
 "My knee hit the concrete first. My water bottle rolled under a parked car.",
 "I sat on the ground for a moment. Nothing was broken, but my knee was bleeding and my shorts were torn along the edge.",
 "Then I had to crawl under the car for my bottle, which took three minutes.",
 "I walked into assembly at twenty to eight, late anyway, with a bleeding knee and one wet sock.",
 "Mrs Devi did not ask what had happened. She looked at my knee, then at my shorts, and said only, \"The long way is eleven minutes.\"",
 "I use the long way now. It is eleven minutes, and I leave at twenty past seven."],
 "questions":[
 {"n":1,"q":"How long does each of the two ways to school take?","a":"The long way takes eleven minutes and the short way takes four.","marks":2,
  "tip":"Both times are given, in two different paragraphs."},
 {"n":2,"q":"Give two things the writer passes on the long way.","a":"Any two of: the carpark; the provision shop; the ramp.","marks":2,
  "tip":"Three things are listed in one sentence. Two of them will do."},
 {"n":3,"q":"Why had the writer's mother told him not to use the short way?","a":"She said the wall is higher on the other side than it looks.","marks":1,
  "tip":"Her reason is given in the same sentence as the warning."},
 {"n":4,"q":"How do we know the writer was in a hurry on Tuesday morning?","a":"He ran down the stairs carrying his shoes with only one sock on, because he had woken up late and the lift was busy.","marks":2,
  "tip":"Look at what he is carrying and what he is wearing, not just at the word 'ran'."},
 {"n":5,"q":"What had the writer not expected about the grass?","a":"That it would be wet. His socks were soaked within five steps.","marks":1,
  "tip":"One short clause says it directly."},
 {"n":6,"q":"Give two things that went wrong when the writer landed.","a":"Any two of: his knee hit the concrete and began to bleed; his shorts were torn along the edge; his water bottle rolled under a parked car.","marks":2,
  "tip":"Three things went wrong across two paragraphs."},
 {"n":7,"q":"Was the short way faster for the writer that morning? Explain your answer.","a":"No. He reached assembly at twenty to eight, ten minutes after it began, so he was late anyway — and he had lost three minutes crawling under the car for his bottle.","marks":2,
  "tip":"Compare the time he arrived with the time assembly starts. The point of the story is in that comparison."},
 {"n":8,"q":"Which word in the passage means 'completely wet'?","a":"'Soaked'.","marks":1,
  "tip":"Look in the paragraph about the grass."},
 {"n":9,"q":"Mrs Devi said only, \"The long way is eleven minutes.\" Why do you think she said nothing else?","a":"She could see from his knee and his torn shorts exactly what he had done, so there was no need to ask or to scold him. Repeating the time was enough to make the point, and letting him work it out himself was stronger than telling him off.","marks":2,
  "tip":"Think about what she had already worked out before she spoke, and why she chose those words."},
 {"n":10,"q":"How has the writer's behaviour changed since Tuesday?","a":"He now uses the long way and leaves ten minutes earlier, at twenty past seven.","marks":2,
  "tip":"The last sentence gives two changes, not one."}]})

# ───────────────────────────── P3 narrative · The Jar of Buttons
P.append({"id":"cmpZF","title":"The Jar of Buttons","level":"P3","kind":"Narrative","text":[
 "My grandmother keeps a glass jar of buttons on the shelf above her sewing machine.",
 "There must be two hundred of them. Most are white or brown and perfectly ordinary. A few are not.",
 "When I was small she let me pour them onto the floor and sort them into piles: round ones, square ones, the ones with four holes, the ones with two.",
 "I always kept three buttons apart from the rest.",
 "The first is wooden and almost black, and larger than a fifty-cent coin. The second is bright red glass. The third has a tiny silver anchor on it.",
 "Last month I asked her where the three had come from.",
 "She put down her sewing. The wooden one, she said, came off her father's coat. He wore that coat for twenty-two years and the button is the only part of it left.",
 "The red glass one came from a dress she wore to her own wedding. There were nine on the dress. Eight are still on it, in a box under her bed. This one came off on the day and was never sewn back.",
 "The silver anchor came from a sailor's jacket that somebody left on a bus in 1971. Nobody claimed it, so the bus company gave it away, and my grandmother cut off the buttons before she used the cloth for a cushion.",
 "\"Every button in this jar came off something,\" she said. \"Most of them I cannot remember. Those three I can.\"",
 "She has said I may have the jar one day.",
 "I will not sort them into piles any more. But I will keep those three apart."],
 "questions":[
 {"n":1,"q":"Where does the grandmother keep the buttons?","a":"In a glass jar on the shelf above her sewing machine.","marks":1,
  "tip":"The first sentence says both the container and the place."},
 {"n":2,"q":"How did the writer play with the buttons when she was small?","a":"She poured them onto the floor and sorted them into piles — round ones, square ones, ones with four holes and ones with two.","marks":2,
  "tip":"Two parts: what she did with them, and how she grouped them."},
 {"n":3,"q":"Describe the three buttons the writer always kept apart.","a":"One is wooden and almost black, larger than a fifty-cent coin. One is bright red glass. One has a tiny silver anchor on it.","marks":2,
  "tip":"Each one is described in a separate sentence."},
 {"n":4,"q":"What is special about the wooden button?","a":"It came off her great-grandfather's coat, which he wore for twenty-two years, and it is the only part of that coat still left.","marks":2,
  "tip":"Two facts: where it came from, and why it matters now."},
 {"n":5,"q":"How many buttons were on the wedding dress, and where are the others now?","a":"There were nine. Eight are still on the dress, which is in a box under the grandmother's bed.","marks":2,
  "tip":"Both numbers are in the same paragraph."},
 {"n":6,"q":"Explain how the silver anchor button came to be in the jar.","a":"A sailor's jacket was left on a bus in 1971 and nobody claimed it, so the bus company gave it away. The grandmother cut the buttons off before using the cloth to make a cushion.","marks":2,
  "tip":"There are three steps: left behind, given away, then cut off. All three are needed."},
 {"n":7,"q":"Which word in the passage means 'said that something belonged to them'?","a":"'Claimed'.","marks":1,
  "tip":"Look in the paragraph about the jacket on the bus."},
 {"n":8,"q":"What does the grandmother mean when she says, \"Every button in this jar came off something\"?","a":"Every button once belonged to a real piece of clothing that somebody wore, so each one has a story behind it — even though she can no longer remember most of them.","marks":2,
  "tip":"Her next sentence explains the part of her meaning that matters most."},
 {"n":9,"q":"Why do you think the writer will no longer sort the buttons into piles?","a":"When she was small the buttons were only shapes to be grouped. Now she knows they came off real clothes belonging to real people, so sorting them by shape would miss the thing that makes them worth keeping.","marks":2,
  "tip":"Compare what she thought the buttons were then with what she knows now."},
 {"n":10,"q":"Give one piece of evidence that the grandmother trusts the writer with something important.","a":"She has said the writer may have the jar one day. She also put down her sewing to answer the question properly, rather than answering while she worked.","marks":1,
  "tip":"One is enough, but look for actions rather than feelings."}]})

# ───────────────────────────── P3 non-narrative · Why Cats' Eyes Shine
P.append({"id":"cmpZG","title":"Why Cats' Eyes Shine in the Dark","level":"P3","kind":"Non-narrative","text":[
 "Point a torch at a cat at night and its eyes shine back at you, green or gold.",
 "Point the same torch at a person and nothing happens.",
 "The difference is a layer behind the cat's eye called the tapetum. It works like a tiny mirror.",
 "Light goes into the eye. Some of it is used straight away. The rest would be wasted, but the mirror bounces it back through the eye a second time, so the cat gets two chances to use the same light.",
 "This is why a cat can see on a night when we can see almost nothing. A cat needs only about one sixth as much light as a person does.",
 "The mirror is not perfect, and that is the price. The bounced light scatters a little, so a cat's picture of the world is slightly blurred. A cat cannot read the small print on a tin of its own food, and it would not be able to even if it wanted to.",
 "Cats also see fewer colours than we do. Red looks dull and greyish to them. What a cat is very good at is spotting something that moves.",
 "Many animals have this mirror: dogs, cows, horses, deer and crocodiles. Human beings do not, and neither do most birds that hunt by day.",
 "The colour you see in the shine depends on the animal. Most cats shine green. Dogs are often yellow or orange. A cat with blue eyes may shine red instead, because it has very little of the colouring that normally covers the mirror.",
 "There is one more thing worth knowing. The shine is not the cat looking at you. It is your own torchlight coming back."],
 "questions":[
 {"n":1,"q":"What is the layer behind a cat's eye called?","a":"The tapetum.","marks":1,
  "tip":"It is named in the third paragraph."},
 {"n":2,"q":"In your own words, explain how the tapetum helps a cat.","a":"It works like a mirror. Light that would have been wasted is bounced back through the eye a second time, so the cat can use the same light twice.","marks":2,
  "tip":"Explain it without copying the paragraph word for word."},
 {"n":3,"q":"How much light does a cat need compared with a person?","a":"About one sixth as much.","marks":1,
  "tip":"One figure is given."},
 {"n":4,"q":"The passage says the mirror 'is not perfect'. Give one disadvantage of having it.","a":"The bounced light scatters a little, so the cat's picture of the world is slightly blurred and it cannot see fine detail such as small print.","marks":2,
  "tip":"The paragraph calls this 'the price'. Say what is lost, not just that something is lost."},
 {"n":5,"q":"Give two things a cat's eyesight is NOT good at.","a":"Any two of: seeing fine detail or small print, because its picture is slightly blurred; seeing colours, especially red, which looks dull and greyish.","marks":2,
  "tip":"Two weaknesses are described in two paragraphs. The thing cats ARE good at is in the same paragraph as the second one."},
 {"n":6,"q":"Give two animals, apart from cats, that have this mirror.","a":"Any two of: dogs; cows; horses; deer; crocodiles.","marks":2,
  "tip":"Five are listed in one sentence."},
 {"n":7,"q":"Why might a cat with blue eyes shine red instead of green?","a":"Because it has very little of the colouring that usually covers the mirror.","marks":2,
  "tip":"The reason is given in the same sentence, after the word 'because'."},
 {"n":8,"q":"Which word in the passage means 'spread out in different directions'?","a":"'Scatters'.","marks":1,
  "tip":"Look in the paragraph about the price of having the mirror."},
 {"n":9,"q":"Why does the writer say that the shine 'is not the cat looking at you'?","a":"People think the cat's eyes are producing the light. In fact the eyes are only reflecting the torchlight that was shone at them, so without a torch there would be no shine at all.","marks":2,
  "tip":"The last sentence says where the light actually comes from."},
 {"n":10,"q":"Why do you think the writer begins by telling the reader to point a torch at a cat and then at a person?","a":"It asks the reader to picture something they can test for themselves, and the difference between the two is exactly what the rest of the passage explains.","marks":1,
  "tip":"Think about what the two sentences set up for the paragraphs that follow."}]})

ok = True
for p in P:
    body = " ".join(p["text"]); p["words"] = len(body.split())
    marks = sum(q["marks"] for q in p["questions"])
    for q in p["questions"]:
        if "Which word in the passage" in q["q"]:
            w = q["a"].strip().strip("'.").lower()
            if w not in body.lower(): print(f"  !! {p['title']}: '{w}' not in passage"); ok = False
        if not q.get("tip"): print("  !! no tip", p["title"], q["n"]); ok = False
    ns = [q["n"] for q in p["questions"]]
    assert ns == list(range(1, len(ns)+1))
    print(f'{p["level"]} {p["kind"][:13]:14s} {p["title"][:34]:36s} {p["words"]:4d} words  {len(p["questions"])}q  {marks:2d} marks')
assert len({p["title"] for p in P}) == len(P)
print("vocabulary words all present in their passages:", ok)
pathlib.Path("content_v11_p3_comprehension.json").write_text(
    json.dumps({"passages": P}, ensure_ascii=False), encoding="utf-8")
print("TOTAL new questions:", sum(len(p["questions"]) for p in P))
