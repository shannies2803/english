import json, pathlib

# A Primary 3 listening paper. The MOE shape at this level is short spoken texts —
# an announcement, a message, a short conversation — each followed by one question,
# then one or two longer texts carrying several questions. Fourteen marks.
#
# Every script is written to be READ ALOUD, so the answer is never in a word the
# child would have to see spelt: it is in a number, a name, a time or an action.
# Each item also carries an explanation naming the words in the script that decide it,
# because the adult reading it needs to be able to settle an argument afterwards.

SHORT = [
 ("Good morning, Primary 3. A reminder about Thursday's trip to the Science Centre. "
  "Bring your water bottle, a cap and your packed lunch. You do not need to bring money, "
  "because the school has already paid for everything, including the ice cream.",
  "What do pupils NOT need to bring on the trip?",
  ["A cap", "Money", "A packed lunch", "A water bottle"], 1,
  "The script lists a bottle, a cap and lunch, then says 'You do not need to bring money'."),

 ("This is a message for Hari from his mother. Hari, I will be twenty minutes late. "
  "Please wait inside the library, not at the gate, because it is raining. Do not walk home by yourself.",
  "Where must Hari wait?",
  ["At the gate", "Inside the library", "At home", "At the bus stop"], 1,
  "She says 'wait inside the library, not at the gate'."),

 ("Attention, shoppers. The lift in this building is being repaired this morning. "
  "Please use the escalator at the far end, beside the bakery. The lift will be working again after lunch.",
  "Why must shoppers use the escalator?",
  ["The escalator is faster", "The lift is being repaired", "The bakery is closed",
   "The lift is too full"], 1,
  "'The lift in this building is being repaired this morning' is the reason given."),

 ("Nadia, could you help me for a minute? I need six chairs carried into the hall, "
  "not the classroom. Take them two at a time so you do not drop any.",
  "How many chairs does the teacher need?",
  ["Two", "Four", "Six", "Twelve"], 2,
  "'I need six chairs carried into the hall'. Two at a time is how to carry them, not how many."),

 ("The swimming lesson on Friday has been moved. It will now start at half past two "
  "instead of three o'clock, and it will finish at the usual time. Please be changed and ready by twenty past two.",
  "What time will the swimming lesson now start?",
  ["Twenty past two", "Half past two", "Three o'clock", "The usual time"], 1,
  "'It will now start at half past two instead of three o'clock'. Twenty past two is when to be ready."),

 ("Boys and girls, the field is closed today because the grass was cut this morning "
  "and it is still wet. You may play in the covered court or in the hall. Nobody is to go onto the field, "
  "not even to fetch a ball.",
  "Why is the field closed?",
  ["It is raining", "The grass was cut and is still wet", "A match is being played",
   "It is being repaired"], 1,
  "'The grass was cut this morning and it is still wet' is the reason."),

 ("Mei Qi, your art project is due on Wednesday, not Tuesday. You still need to finish "
  "the painting and write the title on the back. The glue is in the cupboard if you need it.",
  "What must Mei Qi still do?",
  ["Only finish the painting", "Only write the title",
   "Finish the painting and write the title", "Buy some glue"], 2,
  "Two things are named: 'finish the painting and write the title on the back'."),

 ("This is the two o'clock announcement. Will the owner of a blue bicycle with a "
  "broken bell please come to the general office. It has been left outside the gate since Monday.",
  "What is wrong with the bicycle?",
  ["It has a flat tyre", "It has a broken bell", "It has no lock", "It is the wrong colour"], 1,
  "'A blue bicycle with a broken bell'."),
]

PASS_A = ("Listen carefully. This is about our class library corner.\n\n"
 "From next week the corner will be open every day at recess, not only on Fridays.\n\n"
 "You may borrow one book at a time. Write your name and the date on the yellow card, "
 "not in the book itself.\n\n"
 "Books must come back within one week. If you need longer, come and ask me — I will almost always say yes. "
 "What I do not want is a book that disappears for a month.\n\n"
 "Please do not eat while you are reading. Last term two books came back with oil on them, and we had to "
 "throw one away.\n\n"
 "There is a box of new books arriving on Tuesday. Twelve of them are about animals, which several of you "
 "have been asking for.")
QA = [
 ("When will the library corner be open?",
  ["Only on Fridays", "Every day at recess", "After school", "On Tuesdays"], 1,
  "'Open every day at recess, not only on Fridays'."),
 ("Where must a pupil write his name?",
  ["In the book", "On the yellow card", "On the box", "On the noticeboard"], 1,
  "'Write your name and the date on the yellow card, not in the book itself'."),
 ("How long may a book be kept?",
  ["One day", "One week", "One month", "A whole term"], 1,
  "'Books must come back within one week.' A month is what the teacher says she does not want."),
 ("What happened to the two books last term?",
  ["They were lost", "They came back with oil on them", "They were never borrowed",
   "They were taken home for a month"], 1,
  "'Two books came back with oil on them, and we had to throw one away'."),
 ("How many of the new books are about animals?",
  ["Two", "Twelve", "Twenty", "It does not say"], 1,
  "'Twelve of them are about animals'."),
]

PASS_B = ("Now listen to this short talk about keeping a fish tank.\n\n"
 "A fish tank is not hard work, but it does need the same small jobs done every week.\n\n"
 "Feed your fish once a day, and only as much as they can finish in two minutes. Too much food is the "
 "commonest mistake. The food that is left over sinks, rots, and makes the water cloudy.\n\n"
 "Change about a quarter of the water each week. Never all of it at once — that would take away the good "
 "bacteria the fish need.\n\n"
 "Keep the tank out of direct sunlight, or you will be scraping green algae off the glass every few days.\n\n"
 "And if a fish starts swimming on its side, or stops eating, move it into a separate container straight away "
 "and tell an adult. A sick fish can make the others sick too.")
QB = [
 ("How often should the fish be fed?",
  ["Twice a day", "Once a day", "Every two minutes", "Once a week"], 1,
  "'Feed your fish once a day.' Two minutes is how long they should take to finish it."),
 ("What is the commonest mistake?",
  ["Changing too much water", "Giving too much food", "Keeping the tank too dark",
   "Feeding them too late"], 1,
  "'Too much food is the commonest mistake'."),
 ("How much of the water should be changed each week?",
  ["All of it", "About half", "About a quarter", "None of it"], 2,
  "'Change about a quarter of the water each week.'"),
 ("Why should the whole tank of water NOT be changed at once?",
  ["It takes too long", "It would take away the good bacteria", "The fish would escape",
   "The water would be too cold"], 1,
  "'Never all of it at once — that would take away the good bacteria the fish need'."),
 ("What should you do first if a fish stops eating?",
  ["Change all the water", "Give it more food", "Move it into a separate container",
   "Put the tank in the sun"], 2,
  "'Move it into a separate container straight away and tell an adult' — moving it comes first."),
]

items, n = [], 0
for script, q, o, c, tip in SHORT:
    n += 1
    items.append({"n": n, "script": script, "q": q, "options": o, "correct": c, "tip": tip})
for i, (q, o, c, tip) in enumerate(QA):
    n += 1
    it = {"n": n, "q": q, "options": o, "correct": c, "passage": "A", "tip": tip}
    if i == 0: it["script"] = PASS_A
    items.append(it)
for i, (q, o, c, tip) in enumerate(QB):
    n += 1
    it = {"n": n, "q": q, "options": o, "correct": c, "passage": "B", "tip": tip}
    if i == 0: it["script"] = PASS_B
    items.append(it)

spec = {"title": "Listening Comprehension · Practice Paper 6 (Primary 3)",
 "level": "P3",
 "instructions": ("An adult reads each text aloud TWICE at a normal pace, with a short pause between the two "
   "readings. Let the child read the question and the four options first. Do not show the child the script.\n\n"
   "Items 1 to 8 are short texts with one question each. Items 9 to 13 all belong to one longer text, and "
   "items 14 to 18 to another — read each of those once, pause, read it again, then let the child answer all "
   "five questions. Written for Primary 3 only: 18 marks."),
 "items": items}

pathlib.Path("content_v11_p3_listening.json").write_text(
    json.dumps({"listening6": spec}, ensure_ascii=False), encoding="utf-8")

print(f'{spec["title"]}  ·  {len(items)} items')
print(f'  short texts: {len(SHORT)}   passage A: {len(QA)}   passage B: {len(QB)}')
import collections
print("  answer positions before spreading:",
      dict(sorted(collections.Counter(i["correct"] for i in items).items())))
for i in items:
    assert len(i["options"]) == 4 and len(set(i["options"])) == 4, i["n"]
    assert 0 <= i["correct"] < 4
    assert i.get("tip")
print("  every item: 4 distinct options, one keyed answer, one explanation")
