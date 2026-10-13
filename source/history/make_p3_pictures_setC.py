import sys, json, pathlib
sys.path.insert(0, "lib")
from p3pics import *

T = []   # tasks

# ─────────────────────────────── 1 · The Broken Vase · owning up
T.append({"n":1,"title":"The Broken Vase","theme":"Owning up","pictures":[
 {"caption":"A boy kicks a ball in the living room while his mother is out",
  "svg":panel(window(100,24), table(20,70,40), vase(40,54), person(104,56,TEAL,arms="out",legs="run"), ball(78,92), speed(120,64))},
 {"caption":"The ball hits the vase and it falls and breaks",
  "svg":panel(window(100,24), table(20,70,40), vase(40,86,broken=True), person(106,56,TEAL,arms="up",legs="stand"), ball(58,80), worry(118,44))},
 {"caption":"He sweeps the pieces into a corner and says nothing",
  "svg":panel(window(100,24), person(52,56,TEAL,arms="hold_low",legs="kneel"), vase(96,86,broken=True), box(84,82,26,14), worry(32,46))},
 {"caption":"He tells his mother the truth and she puts a hand on his shoulder",
  "svg":panel(door(16,52), person(62,58,TEAL,arms="down",legs="stand"), person(104,48,PLUM,h=11,tall=32,arms="reach_l",legs="stand"), smile_mark(118,30))},
],
"model":("Last Saturday afternoon my mother went downstairs to buy vegetables. She told me to stay in the flat and "
  "not to play ball indoors.\n\nAs soon as the door closed, I took out my football. I kicked it softly at first, "
  "then harder. On the fourth kick it flew past me and hit the blue vase on the small table. The vase wobbled, "
  "fell and broke into five pieces.\n\nMy heart was beating very fast. The vase had belonged to my grandmother. I "
  "swept the pieces into a corner with my hands and pushed them behind a box, hoping nobody would look there.\n\n"
  "For half an hour I sat on the sofa and pretended to read. I could not read a single page.\n\nWhen my mother came "
  "back, I stood up and told her everything. I said I was sorry and that I would not play ball indoors again. She "
  "was quiet for a moment. Then she put her hand on my shoulder and said that telling the truth was braver than "
  "hiding it.\n\nWe picked up the pieces together. I still feel sad about the vase, but I am glad I did not lie."),
"why":("All four pictures are used in order, and the writer adds what the drawings cannot show: the day, the "
  "instruction not to play indoors, the fourth kick, the five pieces, the grandmother. The hiding in picture three "
  "is given real feeling — sitting on the sofa unable to read a page — instead of 'I was scared'. The ending says "
  "what the mother did and what the writer learnt, without finishing on 'I learnt my lesson'.")})

# ─────────────────────────────── 2 · The Hungry Stray · kindness to animals
T.append({"n":2,"title":"The Hungry Stray","theme":"Kindness to animals","pictures":[
 {"caption":"Two children find a thin cat behind the canteen",
  "svg":panel(bench(100,74,48), cat(44,84), person(96,50,TEAL,legs="stand"), person(126,50,ORANGE,legs="stand"), worry(70,56))},
 {"caption":"They share some food from their plates with it",
  "svg":panel(cat(104,86), person(46,50,TEAL,arms="reach_r",legs="kneel"), person(22,52,ORANGE,arms="carry",legs="stand"), box(76,88,22,10,c=PALE))},
 {"caption":"They bring a cardboard box and a bowl of water",
  "svg":panel(box(96,80,36,18), person(44,50,TEAL,arms="carry",legs="walk"), cat(118,70), basin(20,88,26))},
 {"caption":"The cat sleeps in the box and the children put up a notice",
  "svg":panel(box(26,82,38,18), cat(44,78), person(112,52,PLUM,arms="up",legs="stand"), sign(94,24,42,22), sparkle(70,44))},
],
"model":("We found her on a Tuesday, behind the canteen, where the bins are kept. She was a small brown cat and she "
  "was far too thin. You could see the shape of her bones.\n\nMy friend Devi and I were carrying our plates back. "
  "Without saying anything, we both stopped.\n\nWe put a little rice and two pieces of chicken on the ground. The "
  "cat looked at us for a long time before she came forward. Then she ate everything in less than a minute.\n\nThe "
  "next morning we came to school early. Devi brought a cardboard box from her father's shop and I brought an old "
  "towel and a plastic bowl. We put the box in the shade beside the wall and filled the bowl with water from the "
  "cooler.\n\nBy Friday the cat was sleeping in the box every afternoon. We wrote a notice and taped it to the "
  "wall: PLEASE DO NOT MOVE THE BOX. THERE IS A CAT INSIDE.\n\nShe is not thin any more. Mr Siva says she is the "
  "best mouse-catcher the canteen has ever had."),
"why":("The pictures are followed in order, and every panel is given a detail of its own: the bins, the rice and "
  "two pieces of chicken, the box from the father's shop, the words actually written on the notice. 'You could see "
  "the shape of her bones' shows how thin she was instead of saying 'very thin'. The last two lines show the result "
  "without announcing a moral.")})

# ─────────────────────────────── 3 · The Missing Shoe · problem solving
T.append({"n":3,"title":"The Missing Shoe","theme":"Problem solving","pictures":[
 {"caption":"A boy sits on a bench before PE with only one shoe on",
  "svg":panel(bench(22,76,54), seated(44,46,TEAL), shoe(96,96), worry(72,50))},
 {"caption":"He searches his bag and under the bench but cannot find it",
  "svg":panel(bench(96,76,50), person(42,50,TEAL,arms="hold_low",legs="kneel"), bag(70,80,c=RED), worry(24,42), speed(128,58))},
 {"caption":"A classmate finds the shoe under a bench on the other side",
  "svg":panel(bench(18,74,46), person(100,50,ORANGE,arms="reach_l",legs="kneel"), shoe(30,92), person(136,52,TEAL,legs="stand"), sparkle(72,40))},
 {"caption":"He joins the race and his class cheers",
  "svg":panel(person(40,54,TEAL,arms="out",legs="run"), speed(14,62), person(104,52,ORANGE,arms="up",legs="stand"), person(132,52,PLUM,arms="up",legs="stand"), smile_mark(112,28))},
],
"model":("I have lost many things at school, but never one shoe.\n\nIt was Wednesday, the day we have PE in the "
  "afternoon. I changed on the bench outside the hall as usual. When I reached into my bag for the second shoe, it "
  "was not there. Only the left one was.\n\nI turned the whole bag upside down. I shook out my PE shirt, my water "
  "bottle and a flattened packet of biscuits. I crawled under the bench and found two bottle caps and a lot of "
  "dust. The whistle blew. I was still sitting there with one bare foot.\n\nThen Arun came running from the other "
  "side of the hall, holding my shoe above his head like a prize. Somebody had kicked it under the far bench during "
  "recess.\n\nI put it on in about four seconds and ran to the start line. Mr Lee let me join the second heat.\n\n"
  "I came third out of six, which is my best result this year. The whole class clapped, and I think some of them "
  "were clapping for the shoe."),
"why":("The search in picture two is the heart of the story, so it gets the longest paragraph and real details — the "
  "bottle caps, the dust, the whistle going while he is still sitting there. Arun holding the shoe up like a prize "
  "is one comparison, which is enough. The last line is a small joke rather than a moral, and the writer keeps the "
  "past tense throughout.")})

# ─────────────────────────────── 4 · The New Pupil · friendship
T.append({"n":4,"title":"The New Pupil","theme":"Friendship","pictures":[
 {"caption":"A new girl sits alone at a canteen table during recess",
  "svg":panel(table(18,66,52), seated(40,42,PLUM), person(112,50,TEAL,legs="stand"), person(138,50,ORANGE,legs="stand"))},
 {"caption":"A boy notices her and talks to his friend",
  "svg":panel(table(14,66,44), seated(34,42,PLUM), person(100,50,TEAL,arms="out",legs="stand"), person(132,50,ORANGE,legs="stand"), quote(116,24))},
 {"caption":"They invite her to join their game",
  "svg":panel(person(32,52,PLUM,arms="out",legs="walk"), person(78,52,TEAL,arms="reach_l",legs="stand"), person(120,52,ORANGE,arms="out",legs="stand"), ball(100,92))},
 {"caption":"The three of them walk home together, talking",
  "svg":panel(tree(134,62), person(34,54,PLUM,arms="down",legs="walk"), person(66,54,TEAL,arms="down",legs="walk"), person(98,54,ORANGE,arms="down",legs="walk"), quote(66,24))},
],
"model":("Her name was Hui Shan, and she joined our class on a Monday in the middle of term, which must be the "
  "hardest time to join anything.\n\nAt recess she sat at the end of the long table by herself. She had a packet of "
  "biscuits and she was not eating them. She was reading the noticeboard on the wall, although there was nothing "
  "new on it.\n\nI noticed because I had done the same thing in Primary 1.\n\nI told Arun we should ask her to play "
  "catching with us. He said she might not want to. I said that was all right, but somebody still had to ask.\n\nSo "
  "we walked over and asked. She said yes so quickly that she knocked over her biscuits.\n\nShe turned out to be "
  "the fastest runner of the three of us, which Arun has still not got over.\n\nNow we walk to the bus stop "
  "together every day. She talks the most. It is hard to believe she is the same girl who sat at the end of that "
  "table reading an empty noticeboard."),
"why":("The writer gives a reason for noticing — 'I had done the same thing in Primary 1' — which makes the kindness "
  "believable instead of automatic. The detail of reading a noticeboard with nothing on it does the work of "
  "'she was lonely' without saying it, and the story returns to it in the last line. Hui Shan is given something "
  "of her own: she is the fastest of the three.")})

# ─────────────────────────────── 5 · The Running Tap · responsibility
T.append({"n":5,"title":"The Running Tap","theme":"Responsibility","pictures":[
 {"caption":"A girl finds a tap left running in the empty washroom",
  "svg":panel(basin(18,70,44), tap(34,52,running=True), person(112,52,PLUM,legs="walk"), worry(88,44))},
 {"caption":"She tries to turn it off but the handle is stuck",
  "svg":panel(basin(14,70,42), tap(30,52,running=True), person(90,52,PLUM,arms="reach_l",legs="stand"), worry(122,42), speed(130,62))},
 {"caption":"She runs to tell the cleaner, who brings a spanner",
  "svg":panel(person(32,52,PLUM,arms="out",legs="run"), speed(8,60), person(104,48,NAVY,h=11,tall=32,arms="carry",legs="walk"), quote(60,24))},
 {"caption":"The tap is mended and a new notice goes up",
  "svg":panel(basin(16,70,42), tap(32,52), sign(96,36,46,24), person(118,76,PLUM,h=7,tall=18,arms="up",legs="stand",), sparkle(72,40))},
],
"model":("The second washroom on level three is the one nobody uses, because the window is broken and it is always "
  "cold in there.\n\nI only went in because the other one had a queue.\n\nThe second tap was running hard, straight "
  "down the drain, and from the sound of it, it had been running for some time. There was nobody else in the "
  "washroom.\n\nI tried to turn it off. The handle went round and round without tightening, and the water did not "
  "slow down at all. I tried with both hands and with the edge of my sleeve. Nothing happened except that my "
  "sleeve got wet.\n\nSo I ran. I found Uncle Raj, our cleaner, outside the library with his trolley. He listened, "
  "said \"stuck washer\", and came up with a spanner and a small blue toolbox.\n\nIt took him about two minutes.\n\n"
  "The next week there was a new notice above all the basins: IF A TAP WILL NOT CLOSE, TELL AN ADULT AT ONCE. Uncle "
  "Raj says that if I had walked past, that tap would have run all weekend."),
"why":("The opening explains why she was in an empty washroom, which a marker notices. The failed attempt is shown "
  "with specific actions — both hands, the edge of a sleeve, the wet sleeve — rather than 'I could not turn it "
  "off'. Uncle Raj gets two words of speech and a blue toolbox, which is enough to make him real. The last "
  "sentence gives the point of the story in somebody else's voice instead of the writer's.")})

# ─────────────────────────────── 6 · The Heavy Bags · helping others
T.append({"n":6,"title":"The Heavy Bags","theme":"Helping others","pictures":[
 {"caption":"An old lady waits at the lift with two heavy bags",
  "svg":panel(lift(16,46), person(96,50,PLUM,h=10,tall=28,arms="hold_low",legs="stand"), bag(118,78,c=RED), bag(74,78,c=GREEN))},
 {"caption":"A notice says the lift is not working",
  "svg":panel(lift(16,46), sign(22,16,40,22), person(102,50,PLUM,h=10,tall=28,arms="down",legs="stand"), worry(128,40), bag(78,78,c=GREEN))},
 {"caption":"Two children carry the bags up the stairs for her",
  "svg":panel(person(38,56,TEAL,arms="carry",legs="walk"), bag(56,84,c=GREEN,w=14,h=15), person(92,50,ORANGE,arms="carry",legs="walk"), bag(110,78,c=RED,w=14,h=15), person(136,48,PLUM,h=10,tall=28,arms="down",legs="walk"))},
 {"caption":"At her door she gives them a tin of biscuits",
  "svg":panel(door(14,50), person(60,50,PLUM,h=10,tall=28,arms="reach_r",legs="stand"), box(88,62,24,12,c=GOLD), person(126,54,TEAL,arms="up",legs="stand"), smile_mark(96,34))},
],
"model":("Mrs Goh lives on the eighth floor of our block. She is seventy-nine and she walks with a stick, which "
  "she does not like anybody to mention.\n\nOn Saturday morning my cousin Wei and I came back from the "
  "playground and found her standing in front of the lift with two shopping bags on the floor beside her. One "
  "was full of tins.\n\nThen we saw the notice taped to the lift door: LIFT UNDER REPAIR UNTIL 2 P.M.\n\nIt was "
  "half past ten.\n\nShe said she would wait. We said we would carry the bags up for her, and after she had said "
  "no twice, she said all right.\n\nThe bag of tins was heavier than my school bag with every book in it. We "
  "changed hands at the fourth floor and again at the sixth. Mrs Goh came up slowly behind us, one step at a "
  "time, and told us to stop and rest whenever we liked.\n\nAt her door she went inside and came out with a tin "
  "of pineapple tarts, the good kind in the gold tin.\n\nWe were not expecting anything. But I will not pretend "
  "we were sorry about the tarts."),
"why":("Mrs Goh is made a person in two lines, including something she does not like mentioned — the sort of "
  "detail that lifts content marks. Refusing twice before accepting is true to life. The weight is shown by "
  "comparison with a full school bag, and by changing hands at named floors. The ending is honest and a little "
  "funny instead of 'I felt happy because I had helped somebody'.")})

for t in T:
    assert len(t["pictures"]) == 4, t["title"]
    for p in t["pictures"]:
        assert p["svg"].startswith("<svg viewBox='0 0 160 120'>") and p["svg"].endswith("</svg>")
        assert p["caption"] and len(p["caption"]) < 80
    print(f'{t["n"]} {t["title"][:22]:24s} {t["theme"][:22]:24s} model {len(t["model"].split()):3d} words  '
          f'svg {[len(p["svg"]) for p in t["pictures"]]}')

SET = {"id":"compP3c","letter":"CJ3","level":"P3",
 "title":"Picture composition · 6 more four-picture tasks",
 "instruction":("Four pictures tell a story. Write about 120 to 180 words. Use all four pictures, in order. "
   "Marks: 10 for content, 10 for language. Write yours first, then read the model and the note underneath it."),
 "helper":("1 BEGINNING — who, where, when\n2 PROBLEM — what went wrong (pictures 2 and 3)\n"
   "3 ENDING — how it was solved, and how you felt"),
 "tasks":T}
pathlib.Path("content_v11_p3_composition.json").write_text(
    json.dumps({"set":SET}, ensure_ascii=False), encoding="utf-8")
print("\nwrote content_v11_p3_composition.json ·", sum(len(t["pictures"]) for t in T), "pictures")
