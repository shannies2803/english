import json, pathlib

# ── Set 1 · 50 everyday-word MCQ items at Primary 3 ─────────────────────────
# (sentence, four options, index of the answer, explanation)
MCQ = [
 ("The old gate was so __________ that it fell off when I pushed it.", ["sturdy","rusty","shiny","heavy"], 1,
  "'Rusty' metal is weak and crumbling, which is why the gate fell off."),
 ("Grandfather walked slowly because he was __________ after the long journey.", ["weary","cheerful","curious","polite"], 0,
  "'Weary' means very tired."),
 ("The kitten was too __________ to come out from under the sofa.", ["noisy","timid","hungry","clever"], 1,
  "'Timid' means easily frightened, which explains why it stayed hidden."),
 ("Mother told us to speak in a __________ so that we would not wake the baby.", ["shout","whisper","song","laugh"], 1,
  "A 'whisper' is speaking very softly."),
 ("The floor was __________ after the mopping, so we walked carefully.", ["dusty","damp","dry","warm"], 1,
  "'Damp' means slightly wet, which is how a freshly mopped floor feels."),
 ("Ravi __________ down the corridor so that nobody would hear him.", ["tiptoed","stamped","marched","galloped"], 0,
  "To 'tiptoe' is to walk on your toes, very quietly."),
 ("The glue made my fingers __________.", ["sticky","smooth","clean","cold"], 0,
  "'Sticky' things hold on to your skin, which glue does."),
 ("We could not swim at that end because the water was too __________.", ["shallow","salty","clear","blue"], 0,
  "'Shallow' water is not deep, so there is no room to swim."),
 ("The wind was so __________ that it bent the young trees.", ["gentle","fierce","warm","quiet"], 1,
  "'Fierce' means very strong and wild."),
 ("Siti was __________ about what was inside the parcel.", ["curious","angry","sleepy","sorry"], 0,
  "'Curious' means wanting to know something."),
 ("Please __________ the towel neatly before you put it away.", ["tear","fold","throw","squeeze"], 1,
  "To 'fold' something is to bend it over so it lies flat and neat."),
 ("The branch __________ in half when the boy sat on it.", ["snapped","stretched","floated","melted"], 0,
  "To 'snap' is to break suddenly with a sharp sound."),
 ("I had to __________ the lemon hard to get any juice out.", ["squeeze","stroke","shake","wipe"], 0,
  "To 'squeeze' is to press something tightly."),
 ("My little brother __________ across the floor before he could walk.", ["crawled","skipped","jumped","ran"], 0,
  "Babies 'crawl' on their hands and knees."),
 ("The sky grew __________ and we knew the rain was coming.", ["gloomy","golden","bright","clear"], 0,
  "'Gloomy' means dark and dull."),
 ("Uncle Lim is very __________ with children who ask many questions.", ["patient","sudden","sour","narrow"], 0,
  "A 'patient' person does not get annoyed by waiting or by questions."),
 ("The boy was __________ and refused to apologise.", ["stubborn","generous","grateful","careful"], 0,
  "A 'stubborn' person will not change his mind."),
 ("Leaves were __________ all over the playground after the storm.", ["scattered","stacked","folded","buried"], 0,
  "'Scattered' means spread about untidily."),
 ("I felt __________ before I went up to read in front of the school.", ["nervous","bored","proud","hungry"], 0,
  "'Nervous' means worried and a little afraid."),
 ("The cat __________ out in the sun and closed its eyes.", ["stretched","shrank","hurried","shivered"], 0,
  "To 'stretch' is to make your body longer and looser."),
 ("Nobody wanted to sit on the __________ chair in the corner.", ["new","wobbly","soft","tall"], 1,
  "A 'wobbly' chair is not steady, so it is not safe to sit on."),
 ("The boys had to __________ the heavy box across the floor.", ["drag","lift","toss","spin"], 0,
  "To 'drag' is to pull something along the ground because it is too heavy to carry."),
 ("Please do not __________ your classmates in the queue.", ["shove","greet","follow","count"], 0,
  "To 'shove' is to push roughly."),
 ("We were __________ with mud after the obstacle course.", ["covered","divided","measured","folded"], 0,
  "'Covered with' mud means mud was all over us."),
 ("The puppy __________ when it heard the thunder.", ["trembled","yawned","smiled","barked"], 0,
  "To 'tremble' is to shake because you are afraid or cold."),
 ("The girls __________ behind their hands at the teacher's joke.", ["giggled","sobbed","shouted","sighed"], 0,
  "To 'giggle' is to laugh in a small, quiet way."),
 ("Arun __________ his answer so softly that nobody heard it.", ["mumbled","announced","sang","spelt"], 0,
  "To 'mumble' is to speak unclearly and too quietly."),
 ("Mother __________ when she saw the state of my room.", ["sighed","clapped","giggled","cheered"], 0,
  "To 'sigh' is to let out a long breath, often when you are tired or disappointed."),
 ("The path up the hill was narrow and __________.", ["crooked","straight","wide","flat"], 0,
  "'Crooked' means bent and not straight."),
 ("We kept a __________ key under the flowerpot.", ["spare","single","heavy","golden"], 0,
  "A 'spare' key is an extra one, kept in case it is needed."),
 ("The tiny lamp __________ in the dark corridor.", ["glowed","exploded","melted","vanished"], 0,
  "To 'glow' is to give out a soft, steady light."),
 ("The candle flame __________ whenever the fan turned.", ["flickered","froze","grew","sank"], 0,
  "To 'flicker' is to burn unsteadily, going bright and dim."),
 ("By four o'clock the writing on the board had almost __________.", ["faded","shone","risen","multiplied"], 0,
  "To 'fade' is to become fainter and harder to see."),
 ("The temple was __________ — it was built hundreds of years ago.", ["ancient","modern","noisy","narrow"], 0,
  "'Ancient' means very old."),
 ("An __________ crowd waited outside the stadium.", ["enormous","invisible","obedient","edible"], 0,
  "'Enormous' means very big."),
 ("Please keep your desk __________ so that you can find things.", ["tidy","wet","loud","empty"], 0,
  "'Tidy' means neat and in order."),
 ("Mei Qi felt __________ on her first day, before she made any friends.", ["lonely","jealous","proud","brave"], 0,
  "'Lonely' means unhappy because you are alone."),
 ("Hari was __________ when his brother won the prize he had wanted.", ["jealous","delighted","relieved","amused"], 0,
  "'Jealous' means unhappy because somebody else has what you want."),
 ("It is __________ to say 'please' and 'thank you'.", ["polite","rude","silly","secret"], 0,
  "'Polite' behaviour shows good manners."),
 ("The old man __________ about the noise from the flat above.", ["grumbled","giggled","whistled","agreed"], 0,
  "To 'grumble' is to complain in a low, unhappy voice."),
 ("The girls __________ all the way home about the school trip.", ["chattered","mourned","whispered","argued"], 0,
  "To 'chatter' is to talk quickly and happily for a long time."),
 ("Father __________ so loudly last night that I could hear him through the wall.", ["snored","sneezed","sang","read"], 0,
  "To 'snore' is to breathe noisily while you are asleep."),
 ("I __________ to the shop because there was no hurry.", ["strolled","dashed","sprinted","leapt"], 0,
  "To 'stroll' is to walk slowly and in a relaxed way."),
 ("Ben __________ for the bus and only just caught it.", ["dashed","strolled","wandered","limped"], 0,
  "To 'dash' is to run very fast for a short distance."),
 ("After twisting his ankle, Rahim __________ off the field.", ["limped","skipped","marched","charged"], 0,
  "To 'limp' is to walk unevenly because one leg hurts."),
 ("We __________ through the market with no particular plan.", ["wandered","raced","queued","climbed"], 0,
  "To 'wander' is to walk about without aiming for anywhere."),
 ("The fisherman __________ the net into the sea.", ["tossed","folded","buried","measured"], 0,
  "To 'toss' is to throw something lightly."),
 ("Please __________ the rope — I cannot hold it any longer.", ["release","tighten","knot","coil"], 0,
  "To 'release' something is to let go of it."),
 ("A thin layer of frost made the glass __________.", ["blurred","clean","warm","heavy"], 0,
  "'Blurred' means not clear, so you cannot see through it properly."),
 ("The dew on the grass __________ in the morning sun.", ["sparkled","shrank","wilted","sank"], 0,
  "To 'sparkle' is to shine with many small flashes of light."),
]

# ── Set 2 · vocabulary cloze, two short Primary 3 passages ──────────────────
PA = ("Passage A — The School Fish Tank\n\n"
 "The fish tank stands beside the library door, and every Primary 3 class takes a (1)______ at looking after it.\n\n"
 "Last term it was our job. Mrs Devi showed us how much food to give: one small (2)______ each morning, and no "
 "more, because the leftover food makes the water (3)______.\n\n"
 "On Tuesday we noticed that one of the orange fish was swimming on its side. We told Mrs Devi at once, and she "
 "said we had done the right thing to (4)______ it so quickly.\n\n"
 "She moved it into a smaller tank of its own. Three days later it was (5)______ again, and we put it back with "
 "the others.")
PB = ("Passage B — The Rainy Morning\n\n"
 "The rain started before six o'clock and did not stop. By the time I reached the bus stop my shoes were "
 "(6)______ through.\n\n"
 "There was already a long (7)______ of people waiting, and no shelter at all for the last ten of us.\n\n"
 "Then a lady in a yellow raincoat (8)______ her umbrella over the smallest children so that they would stay "
 "dry. Nobody had asked her to.\n\n"
 "When the bus finally came, everybody climbed on (9)______ and nobody pushed.\n\n"
 "I was fifteen minutes late for school, but Mr Siva said he would (10)______ me, because half the class was "
 "late as well.")
CLOZE = [
 (1, ["turn"], "Each class 'takes a turn' — they do it one after another."),
 (2, ["pinch","spoonful","scoop"], "A very small amount of fish food is a 'pinch' — or a 'spoonful' or 'scoop'."),
 (3, ["dirty","cloudy","foul","murky"], "Leftover food rots, so the water becomes 'dirty' or 'cloudy'."),
 (4, ["notice","report","spot"], "They told her quickly, so what they did quickly was 'notice' or 'report' it."),
 (5, ["well","healthy","better"], "The fish recovered, so it was 'well' or 'healthy' again."),
 (6, ["soaked","wet","drenched"], "The rain went right through them, so they were 'soaked' through."),
 (7, ["queue","line","row"], "People waiting one behind another form a 'queue'."),
 (8, ["held","stretched","put"], "She 'held' her umbrella over them — the past tense is needed."),
 (9, ["calmly","quietly","patiently","orderly"], "'Nobody pushed' tells you they boarded 'calmly' or 'quietly'."),
 (10, ["excuse","forgive","pardon"], "He would let it pass, so he would 'excuse' or 'forgive' her."),
]

# ── Set 3 · opposites, 40 items ─────────────────────────────────────────────
OPP = [
 ("ancient","modern",["modern","elderly","historic","ruined"]),
 ("enormous","tiny",["tiny","wide","heavy","empty"]),
 ("shallow","deep",["deep","narrow","clear","still"]),
 ("damp","dry",["dry","cold","clean","soft"]),
 ("fierce","gentle",["gentle","loud","quick","proud"]),
 ("crooked","straight",["straight","short","thin","smooth"]),
 ("tidy","messy",["messy","small","empty","dark"]),
 ("weary","energetic",["energetic","hungry","cheerful","patient"]),
 ("timid","bold",["bold","kind","quiet","honest"]),
 ("stubborn","obedient",["obedient","cheerful","truthful","generous"]),
 ("polite","rude",["rude","shy","loud","late"]),
 ("gloomy","bright",["bright","narrow","heavy","noisy"]),
 ("lonely","sociable",["sociable","wealthy","tidy","brave"]),
 ("sticky","slippery",["slippery","thick","sour","heavy"]),
 ("sturdy","flimsy",["flimsy","narrow","hollow","plain"]),
 ("patient","impatient",["impatient","careless","selfish","boastful"]),
 ("spare","only",["only","broken","golden","hidden"]),
 ("whisper","shout",["shout","listen","mutter","answer"]),
 ("release","grip",["grip","throw","drop","lift"]),
 ("gather","scatter",["scatter","collect","stack","count"]),
 ("fade","brighten",["brighten","shrink","harden","spread"]),
 ("stretch","shrink",["shrink","fold","twist","bend"]),
 ("dash","stroll",["stroll","chase","jump","climb"]),
 ("praise","scold",["scold","thank","greet","teach"]),
 ("accept","refuse",["refuse","receive","collect","choose"]),
 ("arrive","depart",["depart","enter","return","wait"]),
 ("borrow","lend",["lend","buy","keep","return"]),
 ("remember","forget",["forget","repeat","learn","write"]),
 ("hide","reveal",["reveal","cover","bury","lock"]),
 ("increase","reduce",["reduce","repeat","measure","divide"]),
 ("rough","smooth",["smooth","dry","cold","firm"]),
 ("feeble","strong",["strong","tall","wealthy","willing"]),
 ("permit","forbid",["forbid","request","ignore","report"]),
 ("faint","loud",["loud","high","short","sweet"]),
 ("scarce","plentiful",["plentiful","costly","useful","fresh"]),
 ("humble","boastful",["boastful","clever","wealthy","quiet"]),
 ("expand","contract",["contract","float","burn","harden"]),
 ("ascend","descend",["descend","hurry","pause","circle"]),
 ("praiseworthy","shameful",["shameful","ordinary","costly","doubtful"]),
 ("victory","defeat",["defeat","contest","reward","struggle"]),
]

SETS = []
SETS.append({"id":"v11VA25","letter":"VA25","level":"P3","mode":"mcq",
 "title":"Vocabulary · everyday words (set 4)",
 "instruction":"Choose the word that fits the sentence best.",
 "questions":[{"n":i,"q":q,"options":o,"correct":c,"tip":t}
              for i,(q,o,c,t) in enumerate(MCQ,1)]})
SETS.append({"id":"v11VA26","letter":"VA26","level":"P3","mode":"auto",
 "title":"Vocabulary cloze · two short passages",
 "instruction":"Fill each blank with one suitable word. More than one word may fit; the mark scheme lists the ones that are accepted.",
 "passages":[{"from":1,"to":5,"text":PA},{"from":6,"to":10,"text":PB}],
 "answers":[{"n":n,"a":a,"tip":t} for n,a,t in CLOZE]})
SETS.append({"id":"v11VA27","letter":"VA27","level":"P3","mode":"mcq",
 "title":"Opposites · 40 items",
 "instruction":"Choose the word that is most nearly OPPOSITE in meaning to the word in bold.",
 "questions":[{"n":i,"q":f"Choose the opposite of **{w}**.","options":o,
               "correct":o.index(ans),
               "tip":f"'{ans.capitalize()}' is the opposite of '{w}'."}
              for i,(w,ans,o) in enumerate(OPP,1)]})

pathlib.Path("content_v11_p3_vocab.json").write_text(
    json.dumps({"sets":SETS}, ensure_ascii=False), encoding="utf-8")
for s in SETS:
    n = len(s.get("questions", s.get("answers", [])))
    print(f'{s["letter"]:6s} {s["level"]} {s["mode"]:5s} {s["title"][:44]:46s} {n:3d} items')
print("TOTAL", sum(len(s.get("questions", s.get("answers", []))) for s in SETS), "new P3 vocabulary questions")
