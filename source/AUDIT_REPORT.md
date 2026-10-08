# Audit Report — P3–P6 English Workshop

**First audit:** 14 August 2026 · **Re-audited eleven times since, most recently:** 29 September 2026
**Scope:** 154 practice sets · 3,794 individual items (3437 in Practice + 357 inside the mock papers) · 6 mock papers · 17 documents · 1 website

---

## 1. What was checked

### Automated (`audit.py`, re-runnable)
| Check | Applies to |
|---|---|
| Every question has text, accepted answers and a model answer | all 892 items |
| MCQ: exactly 4 options, correct index in range, no duplicate or blank options | 208 MCQ items |
| MCQ: model answer matches the keyed option | 208 items |
| No authoring notes or markdown artefacts left in question text or tips | all items |
| No accepted answer that is an instruction rather than something a child would type | all items |
| No ellipsis or empty string left inside an accepted answer | all items |
| Paper `totalMarks` equals the sum of its sections | 4 papers |
| Each section's marks equal the sum of its question marks | 32 sections |
| Writing-paper criteria totals equal the section marks | 2 sections |
| Duplicate set IDs, duplicate question numbers, unassigned practice groups | all 43 sets |
| Identical question text appearing in more than one set | all items |

### Live, in a real browser (Chromium, headless) — `./runtests.sh` runs all of these
| Check | Result |
|---|---|
| Every keyed answer accepted by the marking function (3,198) | pass |
| Every plausible typing variant accepted (7,500 checks) | pass |
| Offered distractors marked plainly wrong, not "so close" | pass |
| Transposition misspellings forgiven with a hint | pass |
| Export/import round trip preserves every field | pass |
| Spaced-repetition boxes 1/3/7/21, retire after four | pass |
| No clipped navigation or overlap, 390px to 1280px | pass |
| Light and dark themes, both profiles | pass |

### Earlier browser checks
| Check | Result |
|---|---|
| Every one of the 99 sets opens from Practice and marks its first question correctly | pass |
| Five full sets walked question-by-question, every keyed answer submitted | pass, 0 rejections |
| All 4 mock papers completed with keyed answers | 95/95, 95/95, 95/95, 51/55 |
| JavaScript errors across every view and every set | none |
| Print stylesheet strips navigation | pass |
| Mobile (390 px) renders all four practice groups | pass |
| All 13 documents load in Read & print | pass |

---

## 2. Defects found and fixed

### Errors — 2 found, 2 fixed

**1. Authoring note left inside a live question.** `Mock Paper 2C, Editing, line 12` carried the tip *"The error is the missing comparative? No — the error is 'louder' should be..."* — a note to myself that would have been shown to a child. The underlying item was also weak, since "clapped louder" is acceptable in speech. Replaced with a clean tense error (*I clap* → *clapped*).

**2. Blank question text.** `Mock Paper 1, Part 2` rendered the composition task with no task statement — the theme and pictures appeared, but the instruction did not. A task statement was added.

### Warnings — 28 found, 21 resolved, 7 accepted by design

**Answers that were instructions, not answers (4 items).** Four editing lines used the *although… but* redundancy error, where the correct response is to delete a word. The stored answer was `delete "but"` — a child typing `but` would have been marked wrong, and typing `delete but` is not something anyone would do. PSLE editing asks for a replacement word, not a deletion, so all four lines were rewritten as substitution errors. The although/but rule is still taught in Grammar Reference §9.2 and drilled in Practice Set H, where it is self-marked and the format fits.

**An explanation leaking into the accepted answers (1 item).** The parser treated a bracketed note as a list of synonyms, so `Set C #35` accepted the string *"no article before meals"* as a correct answer. The parser now only treats a trailing bracket as synonyms when every part is one or two words.

**Full-sentence rewrites inside auto-marked sets (3 items).** `Set G #120` and `Set H #123–124` asked the child to rewrite a whole sentence but were being machine-marked, which punishes a valid alternative phrasing. These three now self-mark against the model, while the rest of their sets continue to auto-mark.

**"No article needed" answers (3 items).** These expected the literal letter `X`. They now also accept *none*, *no article*, *no preposition* and a dash.

**An ambiguous vocabulary item (1 item).** *"He was ______ of his younger sister's musical talent"* accepted only *envious*, but *supportive*, *unaware* and *dismissive* all fit the sentence as written. The stem was extended so only one answer works.

**Visual texts shared between Practice and the mock papers (21 warnings, accepted).** Three visual texts appear both as practice sets and inside a mock paper's Booklet A. This is deliberate — they are good practice — but a child who drills them the week before sitting that paper gets an inflated score. Rather than remove them, each affected practice card now carries a red line: *"Also used in Mock Paper 2A — do this one well before sitting that paper."*

### Also fixed during the audit

- **Listening sets had no visible instructions.** A child opening a listening paper in Practice saw questions with no explanation of how they work. Set-level instructions now render as a banner on every question.
- **Mock Paper 1 appeared to be unachievable.** A perfect run scored 51/55 because each band button awards the middle of its range. The bands now show their ranges (*17–20 · Clearly on theme…*) and the mark sheet explains that band marks are midpoints.

---

## 2b. Second audit — 28 September 2026 (v3 expansion)

The bank grew from 43 sets to 60 and from 892 items to 1,206. The audit was re-run in full.

**Errors — 1 found, 1 fixed.** The new situational-writing set uses a marking mode (`compose`) that the audit script did not recognise, so it was flagged as an unknown mode. The checker was extended rather than the content changed.

**Build failure caught before shipping — 1.** A group label containing an apostrophe was written with a doubled backslash inside a Python raw string, which emitted invalid JavaScript and silently prevented the whole app from starting. The browser smoke test caught it immediately; a structural audit alone would not have. This is the argument for testing the built page rather than only the data.

**Two rendering defects caught in the browser.** Bullet points in the new situational tasks were collapsing onto a single line, and the printable worksheets rendered blanks as a stray "? ?". Both fixed.

**Re-verified after the expansion:** all 60 sets open and mark their first question correctly; zero JavaScript errors across every view; the audit reports 0 errors and the same 21 by-design warnings about visual texts shared with the mock papers.

---

## 2c. Third audit — 28 September 2026 (v4 expansion)

The bank grew from 60 sets to 76 and from 1,206 items to 1,585.

**What this round was actually for.** The audit script was extended to report the question count available to each learner profile, and it surfaced a real imbalance: the Primary 3–4 profile could reach only **194** questions while the Primary 5–6 profile could reach 773. Nearly everything added since the first version had been pitched at the older child. Eight easier sets and two P3/P4 comprehension passages were written to correct this. The younger profile now reaches **453** questions.

**Errors — 0.**

**Warnings — 1 new, fixed.** A new Primary 4 adjectives question was word-for-word identical to an existing one in Set F ("She is the ___ (tall) of the two sisters"). Rewritten.

**Also closed this round:** four vocabulary banks in document 04 — idioms, phrasal verbs, confusing word pairs and collocations — had been reference lists with no practice attached to them. They now have 150 questions between them. Reading aloud and composition planning were likewise document-only; both are now practisable in the app with self-marking bands.

**Re-verified:** all 76 sets open and mark their first question correctly; zero JavaScript errors; 0 structural errors and the same 21 by-design warnings about visual texts shared with the mock papers.

---

## 2d. Fourth audit — 28 September 2026 (P3–P4 composition)

**A coverage gap, reported by the user rather than found by the audit.** Primary 3 and 4 also sit a composition paper, and nothing here covered it. The two writing sets that existed were both Primary 5–6 formats: situational writing, and planning for a themed three-picture composition. The P3–P4 paper is a different exam — a **four-picture series**, all four compulsory and in order, marked out of 20 rather than 40.

This is worth recording because it is the kind of gap a structural audit cannot find. Every check passed; the content was simply not there. Coverage against the syllabus has to be checked by a person against the syllabus, not by a script against the data.

**Added:** a six-task picture composition set with drawn four-panel sequences, a model composition and a marking note for each, P3–P4 bands (Content 10, Language 10), and document 12 as the printable version.

**One defect fixed during the round:** the practice group heading read "1 sets, 6 questions".

**Re-verified:** 77 sets, all opening and marking correctly; 0 errors; 0 JavaScript errors; the same 21 by-design warnings.

---

## 2e. Fifth audit — 29 September 2026 (vocabulary and grammar expansion)

A large volume round: 22 new sets, 866 new questions. Grammar went from 710 to **1146** and Vocabulary from 293 to **723**. The bank is now 99 sets and 2218 practice questions.

**Errors — 0.**

**Real defects found and fixed — 11.**

*A rendering bug the audit had been suppressing.* Question text uses `**bold**` markup, and the app was escaping it, so a synonym question displayed literally as `Which word is closest in meaning to **enormous**?`. The audit had a rule for this but exempted sentence-rewriting sets, which is where the markup mostly sat — so it had been shipping visibly broken since the second version, in every synthesis set. Fixed at render time by converting `**…**` to real bold, in both the app and the printable worksheets, and the audit's exemption was removed so it cannot hide again.

*Nine duplicated questions.* The new sets repeated nine questions word-for-word from existing sets — two grammar, seven vocabulary. All nine were rewritten rather than deleted. At this volume, the cross-set duplicate check has become the single most useful thing the audit does.

*One instruction-style answer.* A new editing line again used the *although … but* redundancy, where the correct response is to delete a word rather than replace one, which the marker cannot accept. Rewritten as a substitution error — the same mistake caught in the first audit, which suggests the pattern is worth a dedicated check.

**Re-verified:** 99 sets, every one opening and marking its first question correctly; 0 JavaScript errors; 0 structural errors; the same 21 by-design warnings about visual texts shared with the mock papers.

---

## 2f. Sixth audit — 29 September 2026 (answer-position bias)

**The most serious defect found in any round so far, and the audit script found it.**

A new check measured how often the correct answer sits in the same slot within each multiple-choice set. **23 of the 24 MCQ sets were biased**, several severely:

| Set | Correct answer position | Share |
|---|---|---|
| Antonyms | option 2 | **100%** |
| Phrasal verbs (set 2) | option 1 | **100%** |
| Synonyms | option 2 | 98% |
| Vocabulary · harder words | option 2 | 96% |
| Vocabulary · MCQ set 4 | option 2 | 94% |

A child could have scored 96% on the vocabulary set by clicking the second option every time without reading a single question. The sets were not merely easier than intended — they were teaching pattern-matching instead of English, which is worse than no practice at all.

This happens because a person writing questions naturally puts the right answer in a habitual slot. It is invisible question by question and obvious only in aggregate, which is exactly what a script is for and a human reader is not.

**The fix.** The merge step now places each correct answer at a balanced target slot — a round-robin across the four positions, deterministically shuffled per set, with the other options redistributed around it. Options such as "None of the above" stay where the author put them. The shuffle is seeded from the set and question id so it is stable across rebuilds, which matters because saved progress stores an option index.

Result: the overall distribution is now 201 / 197 / 191 / 188 across the four positions, and no set exceeds 38%. The mock papers are balanced too.

**The check is now permanent.** Anything above 45% is a hard error; above 38% is a warning. New content cannot reintroduce this.

**Also this round:** a game layer was added (experience, ranks, combo multiplier, 27 badges, daily quests, a Boss Battle drawn from weak areas, and a head-to-head between the two learners). It can be switched off per learner. Badge and rank-up notifications were built as modals first and rewritten as toasts, because a dialog that interrupts a run mid-set is worse than no celebration at all.

**Re-verified:** 99 sets, all marking correctly; 0 errors; 0 JavaScript errors; game mode verified both on and off, on desktop and at phone width.

---

## 2g. Seventh audit — 29 September 2026 (v7 content expansion)

This round added 36 sets and 871 questions: six comprehension passages, two comprehension
cloze passages, four visual texts, a fourth listening paper, eleven grammar sets, eight
vocabulary sets, six situational writing tasks, six picture compositions, three oral stimuli
and four reading-aloud passages.

**Errors — 0.** The structural audit passed on the first full run after the merge.

**Warnings — 3 real, all fixed.** Three new questions duplicated wording already in the bank:
two subject–verb agreement items (*Mathematics is my favourite subject*, *Either of the two
routes is acceptable*) and one homophone item (*Honesty is an important principle*). All three
were rewritten rather than deleted, so the set counts are unchanged. The remaining 21 warnings
are the mock papers deliberately reusing their visual-text sets, which is by design.

**Two content defects caught by eye, not by the audit:**

- **Six vocabulary items did not belong in their set.** The compound-words set contained items
  whose answers were not compounds at all (*pedestrian*, *bicycle*, *lunch*), each with a tip
  that admitted as much. A set that teaches the wrong thing is worse than a shorter set, so all
  six were replaced with genuine compounds.
- **One abstract-noun item had two defensible answers.** *There was no ____ in his voice* offered
  both *hesitation* and *hesitancy*, and the tip conceded that either would do. Rewritten with
  three clearly wrong distractors.

**One presentation defect fixed after looking at the rendered page.** The six new picture
compositions were first drawn in a different visual style from the existing set — figures with
skin-tone heads rather than the flat single-colour silhouettes used everywhere else — and two
panels were unreadable without their captions. All 24 panels were redrawn in the house style and
one panel (*she sits down, discouraged*) was drawn again a second time. This is the third round
in which a defect was visible only in a screenshot and invisible to both the structural audit and
the browser smoke test, which is the argument for looking at the thing as well as testing it.

**Answer-position bias re-checked.** Across the 35 multiple-choice sets large enough to measure,
the correct answer now falls in option 1/2/3/4 in 273/270/262/262 questions. The most biased
single set sits at 38%, against a 25% ideal and a 45% failure threshold. No set is guessable.

**Browser smoke test.** All 135 sets opened, rendered a first question, and presented a working
input control; no blank cards, no literal `**` in rendered text, no JavaScript errors across
every view. Marking was exercised on a multiple-choice set, a typed-answer set, an editing set,
two self-marked sets and both compose sets; the model answer and examiner bands revealed
correctly in each.

---

## 2h. Eighth audit — 29 September 2026 (v8 expansion, and a review by other readers)

This round differed from the seven before it. Instead of only running the structural audit, each block of
new material was given to a separate reader who had not written it, with instructions to look for wrong
keys, ambiguous items, level mismatches and design faults. That produced about 120 findings on the v7
content and about 50 on the v8 content — far more than the script had ever found, and of a kind the script
cannot find.

**What the script caught that a reader would not.** Three duplicated questions across 3,700 items, and the
answer-position check: the v8 vocabulary sets were written with the correct answer first every single time
(130 items out of 130). The build pipeline's `_spread()` step redistributed them to 34/33/31/32 before they
reached the app, which is exactly what that step exists for. A reader looking at the source files flagged
this as a serious defect; it was already handled.

**What the readers caught that the script could not.**

- **Ambiguous items — by far the largest category, about 60 in all.** Sentences where a second option was
  equally defensible, so a child would be marked wrong for right English: *"Wash your hands ____ you eat"*
  accepts both *before* and *after*; *"We ____ the match on television"* accepts both *watched* and *saw*;
  *"The library was shut. ____ we worked in the canteen"* accepts both *Instead* and *Therefore*. Each was
  fixed either by adding a clause that settles the answer or by widening the accepted-answer list.
- **Items that did not belong in their own set.** Four "compound words" that were not compounds, five
  "homophone" pairs that were only near-homophones (*accept/except*, *affect/effect*, *whistle/wrestle*),
  and two items in a Singapore-usage set whose supposedly wrong version — *"Take note of the deadline"*,
  *"Next time I will remember"* — is in fact perfectly good English. That last pair mattered most: a set
  teaching a child to *correct* correct English is worse than no set at all.
- **A visual-text question with no correct answer.** The Primary 3 paper asked which pupil was on duty three
  times in the week. Recomputing the roster showed four pupils tied on two duties and nobody on three. The
  roster was changed so exactly one answer is right.
- **Two editing lines that broke the format's own rule.** Every editing line must contain one error fixable
  by substituting one word. One line had no error at all; one had two (a transposition *and* a missing
  *-ed*); one keyed a two-word answer.
- **Level mismatches.** A Primary 3 comprehension passage running 363 words with two author's-craft
  questions — Primary 5 work; it was relabelled P4 and a genuine 316-word P3 passage written to replace it.
  Six Primary 4 situational models running at Primary 6 length, with no word target stated. Two oral
  stimuli labelled P3 whose model answers converted percentages to fractions.
- **Factual and internal errors in the writing models.** A model composition that said the corridor was
  empty two sentences after saying nobody in it had turned round. A Singapore primary pupil doing "the
  geography project" — a secondary subject here; it is Social Studies at primary. Two reading-aloud notes
  that described the wrong sentence ("the third sentence has three parts" — it has two; the fifth has three).
- **A gap no single item revealed.** Across 48 comprehension questions only one was vocabulary-in-context,
  and all six passages ended with the same kind of question. Twelve vocabulary-in-context questions were
  added, each verified by script to use a word that genuinely appears in its passage.

**One criticism accepted rather than fixed.** A reader observed that the eight model compositions share a
single adult, understated voice, and that they deliberately avoid the vivid description and figurative
language a Singapore marking scheme also rewards. That is true. Rather than rewrite them, the printable
document now opens with a warning saying exactly this, and telling the child to take the structure from
them and bring their own colour.

**Two new mock papers.** Until this round every paper was PSLE format, so the younger child had nothing to
sit. A Primary 3 paper (60 marks, 75 minutes) and a Primary 4 paper (75 marks, 90 minutes) were written in
the shape a school examination actually takes at those levels, and both were reviewed the same way.

**Ten improvements to the app**, all arising from the audit rather than from new content: papers are now
grouped into "papers at your level" and "other papers" for each child; a level filter was added to the
practice screen, since one child now faces 147 sets; the search respects that filter; the group
descriptions were rewritten to match what the groups now contain; and the examination clock, which reset to
`--:--` on every question and only recovered on the next tick, now renders its live value directly.

**Browser smoke test.** All 147 sets opened and rendered a working first question; both new papers were
walked question by question with their timers running; no blank cards, no literal `**`, no JavaScript
errors in any view under either profile.

---

## 2i. Ninth audit — 29 September 2026 (explanations)

This round was not about adding questions. It measured something nobody had measured before, and the
answer was bad.

**1,329 of 3,372 questions — 39 per cent — had no explanation at all.** A child who got one of them
wrong saw the right answer and nothing else. Worse, those questions then went into the error log and came
back a week later under spaced repetition, so the child met a question they still had no way of reasoning
about. The vocabulary group was the worst at 55 per cent, and eleven sets of forty or fifty questions had
not a single explanation between them.

**738 explanations were written**, covering idioms, phrasal verbs, synonyms, antonyms, the four large
vocabulary multiple-choice sets, word forms, connectors, two cloze sets, every visual text, and nine
further sets the new audit rule flagged. Missing explanations are now **576 of 3437, 17%**.
Of what remains, 80 are listening items where the read-aloud script is the explanation and 65 are writing
tasks that carry a "why it scores" note and examiner bands instead.

**Each one was checked before it was allowed in.** A script verified that every explanation pointed at a
question that exists, that it was not overwriting an existing one, that it stayed under thirty words, that
it never named an option number, and that it engaged with either the keyed answer or the question stem. A
random sample was then read by hand against its question. The checker's own false positives were
instructive: it flagged 92 explanations as "not mentioning the answer", and almost all of them were
glossing the *question* word instead, which is the more useful thing to explain.

**A new audit rule stops this returning.** `explanation_check` fails any set where more than three
quarters of the questions carry no explanation, and warns above two fifths. Listening sets and writing
sets are exempt by design, for the reasons above. The rule immediately failed nine sets, which were then
written; it currently warns on forty more, which is an honest statement of work still to do rather than a
clean bill of health.

**Six further improvements to the app**, all following from what the audit showed:

1. **A real diagnosis.** "Suggested next" used to be the first set below 90 per cent. It now ranks the
   child's actual logged mistakes by set, and the Today screen carries a *What to work on* panel naming
   the five weakest sets, the group most mistakes fall in, and how many mistakes sit in each.
2. **The mistake log is grouped by set** instead of being one long flat list, with a count against each
   and a button that takes the child straight into that set.
3. **Text size** can be set to A, A+ or A++ and is remembered per child, which matters when one profile is
   a Primary 3 pupil and the other is Primary 6.
4. **Papers at your level** are listed first for each child, and the level filter on the practice screen
   now also constrains search.
5. **The examination clock** no longer blanks to `--:--` on every question.
6. **Explanations now appear in the error log**, which is where a child meets their mistakes a second
   time and where an explanation does the most work.

**New content in the thinnest places, not the easiest ones.** The level matrix showed Primary 3
comprehension at 18 questions and Primary 3 and 4 visual text at 8 each, against 762 for Primary 5
grammar. Added: four comprehension passages (P3, P4 and two P5), two visual texts at P3 and P4, and a
fifth listening paper written at Primary 3–4 level, since all four existing listening papers are P5–P6.

---

## 2j. Tenth audit — 30 September 2026 (finishing the explanations, and dark mode)

The previous round left an honest loose end: forty sets still sat above the audit's warning threshold for
missing explanations, and the report said so rather than claiming a clean bill of health. This round
closed it.

**416 further explanations were written**, covering every remaining set: active and passive voice,
reported speech, relative clauses, punctuation, fragments and run-ons, synthesis and transformation, the
Primary 3 and 4 grammar drills, prepositions, collocations, prefixes and suffixes, easily confused words,
and the remaining cloze blanks. The position now:

| | before this work began | now |
|---|---|---|
| Questions with no explanation | 1,329 of 3,372 (39%) | 160 of 3437 (5%) |
| Grammar & sentence work | 454 missing (27%) | 0 |
| Vocabulary | 638 missing (55%) | 0 |
| Comprehension | 38 missing (13%) | 0 |
| **Questions that should have one and do not** | — | **0** |

The 160 that remain are all exempt by design and were each checked to carry their substitute: 95
listening items, where the read-aloud script is the explanation and every one of the 95 has its script,
and 65 writing tasks, which carry a "why it scores" note and the examiner's bands instead. The audit now
reports zero errors and zero explanation warnings.

**Dark mode.** The app had none. Every surface colour was already a token, so the change was to redefine
the tokens under `prefers-color-scheme: dark`, with a button that cycles *follow your device → light →
dark* and remembers the choice per child. Two defects showed up only in a screenshot, not in any test:
the top bar had hard-coded the light background colour and went nearly invisible, and the progress-bar
tracks had hard-coded a pale grey that rendered as solid white bars on a dark card. Both were
hard-coded values that should have been tokens.

**A bug of my own making, found the same way.** Two CSS variables used by the previous round's additions,
`--card` and `--wash`, had never been defined, so those styles had been silently falling back. Defining
them was part of the same change.

**And a regression I introduced and then fixed.** The three text-size buttons plus the new theme button
pushed two navigation items off the top bar between 820 and 1280 pixels — "My mistakes" disappeared
entirely at 1000px. A width sweep caught it. The size control is now a single button cycling A / A+ / A++,
the navigation wraps to its own row below 950px instead of clipping, and a width sweep from 390 to 1280
pixels now shows no clipped tab and no overlap at any width. That sweep is now part of the test suite.

**Listening answers can be checked.** A listening question is marked after an adult has read the script
aloud twice. The child could not see what had been said, so a wrong answer taught nothing. Marking a
listening question now reveals a *What the reader said* panel containing that item's script.

---

## 2k. Eleventh audit — 30 September 2026 (the marking engine, and saved progress)

Every round so far had checked the *content*. This one checked the two pieces of machinery the content
runs on, neither of which had ever been tested at scale: the function that decides whether a typed answer
is right, and the code that moves a child's progress between devices. Both were wrong.

**The marking engine now has a test suite.** Three tests were written and all of them run in a browser
against the built page, using the app's own functions rather than a copy:

1. *Every keyed answer must be accepted by its own marker.* 3,198 keyed answers across every
   machine-marked question. All passed — if this had failed, a child typing the correct answer would have
   been told they were wrong.
2. *Every plausible variant must be accepted.* 7,500 checks: capitalised, with a trailing full stop, in
   quotation marks, with stray spaces, with a trailing comma. All passed.
3. *Sixteen hand-written edge cases*, each asserting an exact verdict.

**Defect found: 31 questions called a wrong word a spelling mistake.** The marker forgave answers within
one edit of the key and said *"So close — check the spelling."* But in items like `(affect / effect)`,
`(advice / advise)` and `(rises / raises)`, the other offered word is one edit away and is the entire
point of the question. A child choosing the wrong word was told they had spelt the right one badly. The
marker now reads the alternatives the question itself offers and marks any of them plainly wrong.

**Defect found: the commonest spelling slip in English was not forgiven.** The tolerance used plain
Levenshtein distance, which scores a transposition as two edits — so `recieve`, `thier`, `freind` and
`beleive` were all marked simply wrong, with no hint. The distance is now Damerau–Levenshtein, which
counts a swap as one edit. Re-checked afterwards: no keyed answer stopped being accepted, no offered
distractor became forgiven, and no question's key is accepted for a different question in the same set.

**Defect found: exported progress lost half of itself on import.** The merge handled seven fields and
silently dropped the rest. A parent restoring a backup on a new device would have lost the child's **XP
and therefore their rank, every badge they had earned, their best combo, their boss-battle clears, and
both their text-size and theme settings**. The merge now carries every field, with a rule per kind:
lifetime counters take the higher of the two so importing the same backup twice cannot inflate anything;
badges and completed groups are unioned so none is ever lost; and a child's settings are adopted only
when the receiving device has no history of its own, so restoring a backup cannot silently change a
device already in use. The confirmation now lists what actually came across rather than saying "merged".

**The spaced-repetition schedule was checked** by walking an item through all four boxes: 1, 3, 7 then 21
days, retiring after the fourth pass. Correct.

**A test runner.** All fourteen browser tests now run from one command, `runtests.sh`. Writing it found a
fifteenth bug — in the runner itself, where a case-insensitive grep made the string "clipped tabs: none"
match a pattern looking for a clipped tab name.

---

## 3. Known limitations

These are honest constraints, not bugs.

**Self-marking is only as honest as the child.** Sentence rewrites, comprehension answers, composition, situational writing and oral cannot be machine-marked. Roughly a third of all items rely on the child or parent comparing against a model. This is also true of any assessment book with an answer key at the back.

**Comprehension model answers are one good version, not the only one.** A child whose wording differs but whose meaning matches deserves the mark. The marking screens say so, but a parent marking strictly will under-score.

**Progress does not sync between devices automatically.** It lives in that browser's storage. There is now an export and import pair on the Today screen that moves a backup file between devices, and importing merges rather than overwrites — but it is a manual step, and clearing browser data without exporting first still loses everything.

**Spelling tolerance is deliberately narrow.** A one-character slip returns *"So close — check the spelling"* and is counted wrong. In an exam it would be wrong, so this is correct, but it will occasionally annoy.

**Several rounds of review have been done by readers who did not write the material, which is the closest thing here to a second opinion.** Those reviews found defects the scripts could not — ambiguous items above all. They are not a substitute for a teacher.

**Nothing here has been vetted by an MOE teacher.** The content follows the published syllabus structure and paper format, and the audit above verifies internal consistency. It does not verify pedagogical judgement. If your child's teacher says something here is wrong, believe the teacher.

---

## 4. Coverage against the exam

| Component | Marks | Practice items | Full papers | Guide |
|---|---|---|---|---|
| P1 Situational Writing | 15 | 26 prompts + 23 models | 1 | Doc 06, 08, 11 |
| P1 Continuous Writing | 40 | 45 prompts + 16 models + 10 planning drills | 1 | Doc 05, 08, 15 |
| P3–P4 Picture Composition | 20 | 12 tasks with models and bands | — | Doc 12 |
| P2 Grammar MCQ | 10 | 220 | 5 | Doc 01, 13 |
| P2 Vocabulary MCQ + cloze | 10 | 1153 | 5 | Doc 04, 14 |
| P2 Visual Text | 8 | 98 across 13 texts | 5 | — |
| P2 Grammar Cloze | 10 | 90 | 5 | Doc 01, 13 |
| P2 Editing | 12 | 145 | 5 | Doc 01, 13 |
| P2 Comprehension Cloze | 15 | 105 | 3 | Doc 07 |
| P2 Synthesis | 10 | 285 | 4 | Doc 01 §18, 13 |
| P2 Comprehension | 20 | 218 across 25 passages | 5 | Doc 07 |
| P3 Listening | 20 | 95 across 5 papers | 5 | Doc 09 |
| P4 Reading Aloud | 10 | 15 passages, self-marked in app | — | Doc 10 |
| P4 Conversation | 20 | 36 with model answers | — | Doc 10 |

Every component of every paper is covered by a technique guide and a practice bank. Six full timed papers:
one at Primary 3, one at Primary 4, three PSLE-format Paper 2s and one PSLE-format Paper 1.

---

## 5. How to re-run this audit

Inside the pack:

```
python3 parse_questions.py     # rebuild the bank from the markdown workbook + answer key
python3 merge_content.py       # merge the authored JSON content and papers
python3 audit.py               # structural audit — should report 0 errors
python3 build_site2.py         # compile the single-file website
```

If you edit any content, run all four in that order. `audit.py` will catch a broken answer key before it reaches a child.
