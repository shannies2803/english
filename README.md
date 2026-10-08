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

- **154 practice sets, 3,437 questions**, grouped the way the exam is: grammar
  and sentence work (1,667), vocabulary (1,153), comprehension (323), visual
  text and listening (193), writing (50) and oral (51).
- **6 timed mock papers**, 357 questions: one at Primary 3, one at Primary 4,
  three PSLE-format Paper 2s and one PSLE-format Paper 1. The papers matching
  the child's level are listed first.
- **17 printable documents** inside the app under *Read & print*, each set also
  printable as a worksheet with its own answer key.
- **An error log** that collects every question got wrong, groups them by set
  and brings them back on a spaced schedule (1, 3, 7 then 21 days).
- **Every question that can carry an explanation has one.** The 160 that do not
  are listening items, where the read-aloud script is the explanation, and
  writing tasks, which carry a "why it scores" note and the examiner's bands.

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
./runtests.sh                 # all fourteen browser suites
```

`audit.py` should report **0 errors**. The 21 remaining warnings are the mock
papers deliberately reusing their visual-text sets, which is by design.
`runtests.sh` should end with **all browser tests pass**; it checks, among other
things, that every one of the 3,198 keyed answers is accepted by the app's own
marking function, that exported progress survives a round trip with nothing
dropped, and that no navigation is clipped between 390px and 1280px.

`source/AUDIT_REPORT.md` records eleven rounds of auditing, what each one found,
and — importantly — what is still not covered. Nothing here has been seen by an
MOE teacher.
