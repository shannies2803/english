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

## What is in it

- **168 practice sets, 3,535 questions**, grouped the way the exam is: grammar
  and sentence work (1,667), vocabulary (1,153), comprehension (359), visual
  text and listening (225), writing (64) and oral (67).
- **6 timed mock papers**, 357 questions: one at Primary 3, one at Primary 4,
  three PSLE-format Paper 2s and one PSLE-format Paper 1. The papers matching
  the child's level are listed first.
- **17 printable documents** inside the app under *Read & print*, each set also
  printable as a worksheet with its own answer key.
- **An error log** that collects every question got wrong, groups them by set
  and brings them back on a spaced schedule (1, 3, 7 then 21 days).
- **Every question that can carry an explanation has one.** The 124 that do not
  are listening items, where the read-aloud script is the explanation, and
  reading-aloud and planning tasks, which carry the model and the examiner's
  bands instead.

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
- `source/history/` — the one-off scripts behind each past correction, kept
  because together they are the record of what was fixed and why

## Checks

`source/` also holds the audits and browser tests. They are not part of the site
and are not needed to deploy it.

```bash
cd source
python3 audit.py              # structural: keys, options, marks, duplicates,
                              # answer-position bias, missing explanations
npm install                   # playwright, for the browser tests
./runtests.sh                 # all fifteen browser suites (about three minutes)
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
