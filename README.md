# English Workshop

A Primary 3–6 English practice site for Faye and Philip, following the Singapore
MOE syllabus. The published site is one self-contained HTML file with no
dependencies: open it in a browser and it works, including offline once it has
loaded. Progress is kept in the browser's own storage, per device. That file is
generated from `source/` — see **Editing** below.

| File | What it is | Lives at |
| --- | --- | --- |
| `index.html` | *English·Workshop* — two profiles in one page, P3–P4 and P5–P6 | _set once Netlify is connected_ |

Both children share the page and pick a profile on opening. Each profile keeps
its own progress, error log, XP, badges, text size and theme, so nothing is
mixed up between them.

On *Practice*, a row of subject chips — Oral, Composition & writing,
Comprehension, Visual text & listening, Grammar, Vocabulary — filters the grid
to one subject, with the number of sets shown on each chip. They combine with
the level chips below them. Without that row the grid is a single 12,000px
column, and reaching the oral sets meant scrolling past everything else.

## What is in it

- **185 practice sets, 3,827 questions**, grouped the way the exam is: grammar
  and sentence work (1,777), vocabulary (1,253), comprehension (389), visual
  text and listening (259), writing (70) and oral (79).
- **8 timed mock papers**, 462 questions: **three at Primary 3** (A, B and C —
  same 60 marks and 75 minutes, meant to be sat a few days apart), one at
  Primary 4, three PSLE-format Paper 2s and one PSLE-format Paper 1. The papers
  matching the child's level are listed first.
- **17 printable documents** inside the app under *Read & print*, each set also
  printable as a worksheet with its own answer key.
- **An error log** that collects every question got wrong, groups them by set
  and brings them back on a spaced schedule (1, 3, 7 then 21 days).
- **Every question that can carry an explanation has one**, with these
  exceptions: the four upper-primary listening papers (80 items, where the
  read-aloud script is the explanation), the reading-aloud and planning tasks,
  which carry the model and the examiner's bands instead, and the upper-primary
  oral stimuli, which take the page's own Point–Elaborate–Example–Link advice.
  Both **Primary 3** listening papers have one per item, naming the words in the
  script that settle the answer, so an adult can resolve an argument about it.

## Deploying

Netlify is connected to this repository. Every push to `main` is published
automatically — there is nothing to click. `netlify.toml` holds the settings
(no build command, publish the repository root).

## Editing

Unlike the chess pages, this one is **generated**. Do not edit `index.html` by
hand — the next build would overwrite it. Change the content or the app in
`source/`, rebuild, and commit both.

```bash
cd source
python3 merge_content.py      # assemble the question bank from content_*.json
python3 build_site2.py        # write source/site/index.html
cp site/index.html ../index.html
```

A clean rebuild reproduces the published file byte for byte.

- `source/content_*.json` — the questions, passages, papers and stimuli
- `source/*.md` — the hand-written documents; the rest are generated
- `source/tips/ALL.txt` — every written explanation, one per line as
  `SET|NUMBER|explanation`, applied to the bank at build time
- `source/lib/p3pics.py` — the drawing vocabulary for the Primary 3 composition
  pictures: figures, poses and props in one fixed flat style, so a panel is two
  or three lines and all three sets look like the same book
- `source/history/` — the one-off scripts behind each past correction, kept
  because together they are the record of what was fixed and why

## Checks

`source/` also holds the audits and browser tests. They are not part of the site
and are not needed to deploy it.

```bash
cd source
python3 audit.py              # structural: keys, options, marks, duplicates,
                              # answer-position bias, missing explanations, and
                              # (via piccheck.py) composition-panel geometry
npm install                   # playwright, for the browser tests
./runtests.sh                 # all sixteen browser suites (about four minutes)
```

`audit.py` should report **0 errors**. The 21 remaining warnings are the mock
papers deliberately reusing their visual-text sets, which is by design.
`runtests.sh` should end with **all browser tests pass**; it checks, among other
things, that every one of the 3,198 keyed answers is accepted by the app's own
marking function, that exported progress survives a round trip with nothing
dropped, that no navigation is clipped between 390px and 1280px, and —
`contrast.mjs` — that no text on any of twelve screens falls below WCAG AA
against the colour actually painted behind it, in **both** light and dark mode.

Two things the runner learnt the hard way, both worth keeping:

- A suite that crashes is not a pass. `runtests.sh` used to decide pass/fail by
  grepping output for failure words, so when `node_modules` was missing every
  suite died before opening a browser and the runner cheerfully reported *all
  browser tests pass*. It now requires exit 0, no stack trace, and real output.
- Structural audits cannot see colour. Dark mode was reported clean for several
  rounds while the MCQ options, every comprehension passage, every writing task
  box, the model-answer boxes, the search field and document tables were all
  near-white text on a hard-coded near-white background — a contrast ratio of
  1.16, which is invisible. Only measuring the rendered page found it.

`source/AUDIT_REPORT.md` records eleven rounds of auditing, what each one found,
and — importantly — what is still not covered. Nothing here has been seen by an
MOE teacher.
