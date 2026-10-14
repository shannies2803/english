import json, pathlib

# ── Editing · four short Primary 3 passages, ten numbered lines each ─────────
# One single-word error per line, and the correction is always one word, because
# that is what the instruction asks for. Mistakes are the ones Primary 3 pupils
# actually make: past tense of irregular verbs, -s on the verb after a singular
# subject, plurals of words ending in -ch/-sh/-y, there/their, and a/an.
PASSAGES = [
 ("Passage A — The Hamster That Got Out", [
  ("Our class hamster is call Pepper.",                                    "called",   "The error was “call”. It needs “is called”, not “is call”."),
  ("He live in a cage beside the window.",                                 "lives",    "The error was “live”. “He” is singular, so the verb takes an -s."),
  ("Last Friday somebody forget to close the little door.",                "forgot",   "The error was “forget”. The past tense of “forget” is “forgot”."),
  ("On Monday morning the cage was empty and we could not find him nowhere.","anywhere","The error was “nowhere”. Two negatives cancel out; use “anywhere” after “not”."),
  ("Mrs Tan told us to look under the cupboardes.",                        "cupboards","The error was “cupboardes”. “Cupboard” just adds -s."),
  ("Suresh find him behind the recycling box.",                            "found",    "The error was “find”. The rest of the story is in the past."),
  ("Pepper had eat a whole packet of sunflower seeds.",                    "eaten",    "The error was “eat”. After “had” we use “eaten”."),
  ("He was to fat to climb back into the cage by himself.",                "too",      "The error was “to”. “Too fat” means more fat than it should be."),
  ("We putted him back and shut the door properly.",                       "put",      "The error was “putted”. The past tense of “put” is “put”."),
  ("Now two pupils check the door every day before they goes home.",       "go",       "The error was “goes”. “They” does not take an -s on the verb."),
 ]),
 ("Passage B — The School Fun Fair", [
  ("Our school hold a fun fair every October.",                            "holds",    "The error was “hold”. “Our school” is singular, so the verb takes an -s."),
  ("Last year it were held on a Saturday morning.",                        "was",      "The error was “were”. “It” takes “was”."),
  ("Each class had they own stall.",                                       "their",    "The error was “they”. “Their” shows that the stalls belonged to them."),
  ("My class sold sandwichs and iced barley water.",                       "sandwiches","The error was “sandwichs”. Words ending in -ch add -es."),
  ("We charged a dollar for a sandwich and fifty cent for a drink.",       "cents",    "The error was “cent”. Fifty is more than one, so the noun is plural."),
  ("A long queue form before we had even finished setting up.",            "formed",   "The error was “form”. The story is in the past."),
  ("By ten o'clock we had sell everything.",                               "sold",     "The error was “sell”. After “had” we use “sold”."),
  ("The money goed to the school's library fund.",                         "went",     "The error was “goed”. The past tense of “go” is “went”."),
  ("Mr Siva said it was a excellent effort.",                              "an",       "The error was “a”. “Excellent” begins with a vowel sound, so it takes “an”."),
  ("This year we are planning a even bigger stall.",                       "an",       "The error was “a”. “Even” begins with a vowel sound."),
 ]),
 ("Passage C — The Thunderstorm", [
  ("The sky turn dark just before we were dismissed.",                     "turned",   "The error was “turn”. The rest of the sentence is in the past."),
  ("Mrs Devi tell us to wait inside the hall.",                            "told",     "The error was “tell”. The past tense of “tell” is “told”."),
  ("There was already more than fifty pupil in there.",                    "pupils",   "The error was “pupil”. Fifty is more than one, so the noun is plural."),
  ("The rain come down so hard that we could not hear the announcement.",  "came",     "The error was “come”. The past tense of “come” is “came”."),
  ("Hui Ling and me sat on the floor near the stage.",                     "I",        "The error was “me”. It is part of the subject: “Hui Ling and I sat”."),
  ("She had bringed an umbrella but it was in her locker.",                "brought",  "The error was “bringed”. The past tense of “bring” is “brought”."),
  ("My shoes was wet right through.",                                      "were",     "The error was “was”. “Shoes” is plural, so it takes “were”."),
  ("After half a hour the rain stopped.",                                  "an",       "The error was “a”. “Hour” begins with a vowel sound because the h is silent."),
  ("The sun came out and the puddles begun to shrink.",                    "began",    "The error was “begun”. Without “had”, the past tense is “began”."),
  ("We walked home slowly, jumping over every puddles on the way.",        "puddle",   "The error was “puddles”. “Every” is followed by a singular noun."),
 ]),
 ("Passage D — Grandmother's Garden", [
  ("My grandmother grow chillies on her corridor.",                        "grows",    "The error was “grow”. “My grandmother” is singular, so the verb takes an -s."),
  ("She have eleven pots altogether.",                                     "has",      "The error was “have”. “She” takes “has”."),
  ("The biggest pot is tallest than me.",                                  "taller",   "The error was “tallest”. Comparing two things takes “taller than”; “tallest” is for three or more."),
  ("Every morning she water them before the sun gets hot.",                "waters",   "The error was “water”. “She” is singular, so the verb takes an -s."),
  ("Last month two of the plant died.",                                    "plants",   "The error was “plant”. “Two of the” is followed by a plural noun."),
  ("She digged them up and put in new soil.",                              "dug",      "The error was “digged”. The past tense of “dig” is “dug”."),
  ("Now there are more leafs than before.",                                "leaves",   "The error was “leafs”. The plural of “leaf” is “leaves”."),
  ("She gives the chillies to our neighbours because she cannot eat them all herself.", "cannot", None),
  ("Yesterday she teached me how to take a cutting.",                      "taught",   "The error was “teached”. The past tense of “teach” is “taught”."),
  ("I am going to try growing one in my room.",                            None, None),
 ]),
]

# the two lines above with no error must be replaced — the instruction promises one per line
PASSAGES[3][1][7] = ("She give the chillies to our neighbours because she cannot eat them all.",
                     "gives", "The error was “give”. “She” is singular, so the verb takes an -s.")
PASSAGES[3][1][9] = ("I am going to try grow one in my own room.",
                     "growing", "The error was “grow”. After “try” we use the -ing form here: “try growing”.")

edit_qs, n = [], 0
for title, lines in PASSAGES:
    for text, ans, tip in lines:
        n += 1
        edit_qs.append({"n": n, "q": f"{title} — {text}", "a": [ans], "m": ans, "tip": tip})

# ── Punctuation · 30 rewriting items at Primary 3 ───────────────────────────
PUNC = [
 ("my birthday is on the 3rd of june", "My birthday is on the 3rd of June",
  "Capital letter at the start, and June is the name of a month."),
 ("where is my reading book", "Where is my reading book?",
  "A question needs a question mark."),
 ("we went to the zoo on tuesday", "We went to the zoo on Tuesday",
  "Days of the week always start with a capital letter."),
 ("i live in singapore with my mother father and sister",
  "I live in Singapore with my mother, father and sister",
  "'I' is always a capital. Singapore is a place name. Commas separate items in a list."),
 ("what a loud noise that was", "What a loud noise that was!",
  "A 'what a…' sentence that shows surprise takes an exclamation mark."),
 ("mrs lim teaches us english and mathematics", "Mrs Lim teaches us English and Mathematics",
  "A person's title and name take capitals, and so do the names of subjects that are languages or proper nouns."),
 ("the cat is sleeping the dog is awake", "The cat is sleeping. The dog is awake.",
  "These are two separate sentences, so they need a full stop between them."),
 ("can you help me carry this box", "Can you help me carry this box?",
  "A question needs a question mark."),
 ("hari said i am ready", "Hari said, \"I am ready.\"",
  "A comma after 'said', then inverted commas round the words that were spoken."),
 ("we bought apples oranges pears and bananas", "We bought apples, oranges, pears and bananas",
  "Commas between the items, but not before the final 'and'."),
 ("dont forget your water bottle", "Don't forget your water bottle",
  "'Don't' is short for 'do not', so it needs an apostrophe."),
 ("the boys bags are in the corridor", "The boys' bags are in the corridor",
  "The bags belong to more than one boy, so the apostrophe goes after the s."),
 ("my sisters name is nadia", "My sister's name is Nadia",
  "One sister owns the name, so the apostrophe comes before the s. Nadia is a name."),
 ("stop shouted the teacher", "\"Stop!\" shouted the teacher",
  "A shout takes an exclamation mark, inside the inverted commas."),
 ("is this your pencil case asked mei", "\"Is this your pencil case?\" asked Mei",
  "The question mark goes inside the inverted commas, and Mei is a name."),
 ("on monday we have pe on friday we have art",
  "On Monday we have PE. On Friday we have Art.",
  "Two sentences, so a full stop between them. Days and subjects take capitals."),
 ("i cant come because im not well", "I can't come because I'm not well",
  "Both 'can't' and 'I'm' are shortened, so both need an apostrophe."),
 ("the river nile is in africa", "The River Nile is in Africa",
  "The names of rivers and continents take capital letters."),
 ("how many brothers do you have", "How many brothers do you have?",
  "A question needs a question mark."),
 ("ravi likes football tennis and swimming", "Ravi likes football, tennis and swimming",
  "Commas between the items in the list, and a capital for Ravi."),
 ("we are going to malaysia in december", "We are going to Malaysia in December",
  "Countries and months take capital letters."),
 ("look out the branch is falling", "Look out! The branch is falling.",
  "A warning takes an exclamation mark, and then a new sentence begins."),
 ("the childrens playground is behind block b", "The children's playground is behind Block B",
  "'Children' is already plural, so the apostrophe comes before the s."),
 ("mother asked have you finished your homework",
  "Mother asked, \"Have you finished your homework?\"",
  "A comma after 'asked', inverted commas round the question, and the question mark inside them."),
 ("that isnt mine said suresh", "\"That isn't mine,\" said Suresh",
  "An apostrophe in 'isn't', a comma before 'said', and a capital for Suresh."),
 ("we visited the science centre the bird park and the museum",
  "We visited the Science Centre, the Bird Park and the Museum",
  "Commas between the items, and capital letters because these are the names of particular places."),
 ("my fathers car is red my uncles car is blue",
  "My father's car is red. My uncle's car is blue.",
  "One father and one uncle, so the apostrophe comes before the s in each. Two sentences, so a full stop between them."),
 ("why is the gate locked asked the boy", "\"Why is the gate locked?\" asked the boy",
  "The question mark belongs inside the inverted commas, because the boy asked the question."),
 ("hurry up well be late", "Hurry up! We'll be late.",
  "An exclamation mark after the order, then a new sentence. 'We'll' is short for 'we will'."),
 ("in january we move to a new classroom", "In January we move to a new classroom",
  "A capital at the start of the sentence and a capital for the month."),
]

# ── Spelling · 40 words Primary 3 pupils get wrong ──────────────────────────
SPELL = [
 ("becuase", "because", "It is be-CAUSE: the cause comes after the be."),
 ("freind", "friend", "Remember: a friend to the end — f-r-i-e-n-d."),
 ("alot", "a lot", "'A lot' is always two words."),
 ("thier", "their", "Their follows the same i-before-e rule as 'friend': t-h-e-i-r."),
 ("wich", "which", "Which begins with wh-, like what, when and where."),
 ("recieve", "receive", "After a c, it is e before i: receive."),
 ("tomorow", "tomorrow", "Tomorrow has one m and two r's."),
 ("beatiful", "beautiful", "Beautiful keeps the whole word 'beauty' at the start: beauti-ful."),
 ("intresting", "interesting", "Say it in four parts: in-ter-est-ing."),
 ("diffrent", "different", "Say it in three parts: dif-fer-ent."),
 ("favourate", "favourite", "It ends -ite, like 'bite': favour-ite."),
 ("libary", "library", "There are two r's: li-brar-y."),
 ("Febuary", "February", "There is an r after the b: Feb-ru-ary."),
 ("excercise", "exercise", "Only one c, and it comes after the x: ex-er-cise."),
 ("resturant", "restaurant", "There is an a after the t: rest-au-rant."),
 ("vegtable", "vegetable", "There is an e in the middle: veg-e-table."),
 ("choclate", "chocolate", "Three parts: choc-o-late."),
 ("brocolli", "broccoli", "Two c's and two l's: broc-co-li."),
 ("surprize", "surprise", "It ends in -ise, and there is an r after the su."),
 ("definately", "definitely", "It has 'finite' in the middle: de-finite-ly."),
 ("seperate", "separate", "There is 'a rat' in the middle: sep-a-rate."),
 ("embarassed", "embarrassed", "Two r's and two s's: em-bar-rassed."),
 ("neccessary", "necessary", "One c and two s's: nec-es-sary."),
 ("begining", "beginning", "Double the n before -ing: be-gin-ning."),
 ("writting", "writing", "One t in writing, two in written."),
 ("stoped", "stopped", "Double the p before -ed: stopped."),
 ("planed", "planned", "Double the n before -ed: planned."),
 ("happend", "happened", "There is an e before the n: happ-ened."),
 ("untill", "until", "Until has only one l at the end."),
 ("allready", "already", "'Already' has one l."),
 ("alright", "all right", "Write it as two words: all right."),
 ("goverment", "government", "There is an n before the m: govern-ment."),
 ("enviroment", "environment", "There is an n before the m: environ-ment."),
 ("quite", "quiet", "Quiet means silent and has two syllables: qui-et. 'Quite' means fairly."),
 ("woudl", "would", "Would rhymes with could and should: w-o-u-l-d."),
 ("becomming", "becoming", "One m in becoming."),
 ("usualy", "usually", "Two l's: usual + ly."),
 ("finaly", "finally", "Two l's: final + ly."),
 ("carefull", "careful", "The suffix -ful has only one l."),
 ("sucessful", "successful", "Two c's and two s's in the middle: suc-cess-ful."),
]

SETS = [
 {"id":"v11GA30","letter":"GA30","level":"P3","mode":"edit",
  "title":"Editing · four Primary 3 passages",
  "instruction":("Each line has one spelling or grammar error. Write the correction — one word only. "
    "This is the Booklet B section worth ten marks, so work line by line and do not rush."),
  "questions":edit_qs},
 {"id":"v11GA31","letter":"GA31","level":"P3","mode":"self",
  "title":"Punctuation · 30 sentences to rewrite",
  "instruction":("Rewrite each line with capital letters and punctuation put right. Write it out in full, "
    "then compare it with the answer and mark yourself."),
  "questions":[{"n":i,"q":f"Rewrite with correct punctuation: {a}","m":b,"tip":t}
               for i,(a,b,t) in enumerate(PUNC,1)]},
 {"id":"v11GA32","letter":"GA32","level":"P3","mode":"auto",
  "title":"Spelling · 40 words to get right",
  "instruction":"Each word below is spelt wrongly. Write it correctly.",
  "questions":[{"n":i,"q":f"Spell this word correctly: {w}","a":[c],"m":c,"tip":t}
               for i,(w,c,t) in enumerate(SPELL,1)]},
]
pathlib.Path("content_v11_p3_grammar.json").write_text(
    json.dumps({"sets":SETS}, ensure_ascii=False), encoding="utf-8")
for s in SETS:
    print(f'{s["letter"]:6s} {s["level"]} {s["mode"]:5s} {s["title"][:44]:46s} {len(s["questions"]):3d} items')
print("TOTAL", sum(len(s["questions"]) for s in SETS), "new P3 questions")
