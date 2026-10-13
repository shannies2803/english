#!/usr/bin/env python3
"""Audit the whole question bank and all mock papers. Reports defects by severity."""
import json, pathlib, re, collections

SRC = pathlib.Path(__file__).parent
bank = json.loads((SRC / "bank_full.json").read_text(encoding="utf-8"))
papers = json.loads((SRC / "papers.json").read_text(encoding="utf-8"))

ERR, WARN, NOTE = [], [], []
def err(where, msg):  ERR.append((where, msg))
def warn(where, msg): WARN.append((where, msg))
def note(where, msg): NOTE.append((where, msg))

# ** renders as bold in the app, so it is markup rather than an artefact
MD_ARTEFACT = re.compile(r"(`|^\s*\*\s|\[\]|\|\s*$|\*\*\*)")
# "in fact" is an authoring tell in prose, but it is also a connector this pack teaches,
# so it only counts when it is NOT being quoted as the term under discussion.
META_TIP    = re.compile(r"(No —|(?<!['‘])in fact|accept 'no error'|\?\s*No\b|this line is correct)", re.I)
INSTRUCTION_ANSWER = re.compile(r"^(delete|remove)\b", re.I)

seen_text = collections.defaultdict(list)
total = 0

def check_q(where, q, mode, marks_expected=None):
    global total
    total += 1
    qt = (q.get("q") or "").strip()
    if not qt:
        err(where, "empty question text")
    if MD_ARTEFACT.search(qt):
        warn(where, "markdown artefact in question text")
    if len(qt) > 40:
        seen_text[qt[:120]].append(where)

    # answers
    a = q.get("a")
    if mode != "write":
        if not a or not isinstance(a, list) or not any(str(x).strip() for x in a):
            err(where, "missing or empty accepted answers")
        else:
            for x in a:
                if x is None or not str(x).strip():
                    err(where, "blank entry in accepted answers")
                elif INSTRUCTION_ANSWER.match(str(x)):
                    warn(where, f"accepted answer is an instruction, not text the child would type: {x!r}")
                elif "…" in str(x):
                    warn(where, f"ellipsis left in accepted answer: {x!r}")
        if not (q.get("m") or "").strip():
            err(where, "missing model answer (m)")

    # tips
    tip = q.get("tip") or ""
    if META_TIP.search(tip):
        err(where, f"authoring note left in the tip: {tip[:70]!r}")

    # mcq specifics
    if mode == "mcq":
        opts = q.get("options") or []
        c = q.get("correct")
        if len(opts) != 4:
            err(where, f"{len(opts)} options (expected 4)")
        if not isinstance(c, int) or not (0 <= c < len(opts)):
            err(where, f"correct index out of range: {c}")
        elif q.get("m") and q["m"] != opts[c]:
            err(where, "model answer does not match the keyed option")
        if len(set(o.strip().lower() for o in opts)) != len(opts):
            err(where, "duplicate options")
        blanks = [o for o in opts if not o.strip()]
        if blanks:
            err(where, "blank option")

    if marks_expected is not None and q.get("marks") is None:
        warn(where, "no mark value on a paper question")


# ---------- bank ----------
ids = collections.Counter(s["id"] for s in bank)
for k, v in ids.items():
    if v > 1:
        err(f"bank/{k}", f"duplicate set id ({v} times)")

letters = collections.Counter(s["letter"] for s in bank)
for k, v in letters.items():
    if v > 1:
        warn(f"bank/{k}", f"duplicate set letter ({v} sets share it)")

for s in bank:
    if not s.get("questions"):
        err(f'bank/{s["id"]}', "set has no questions")
    if s.get("mode") not in ("mcq", "auto", "self", "edit", "read", "compose"):
        err(f'bank/{s["id"]}', f'unknown mode {s.get("mode")!r}')
    if not s.get("group"):
        err(f'bank/{s["id"]}', "no practice group assigned")
    ns = [q.get("n") for q in s["questions"]]
    if len(set(ns)) != len(ns):
        warn(f'bank/{s["id"]}', "duplicate question numbers within the set")
    for q in s["questions"]:
        check_q(f'{s["id"]}#{q.get("n")}', q, s["mode"])

# ---------- papers ----------
for p in papers:
    stated = p["totalMarks"]
    summed = sum(sec["marks"] for sec in p["sections"])
    if stated != summed:
        err(f'paper/{p["id"]}', f"totalMarks {stated} but sections sum to {summed}")
    for sec in p["sections"]:
        qs = sec["questions"]
        if sec["mode"] == "write":
            crit = sum(c["max"] for c in qs[0]["criteria"])
            if crit != sec["marks"]:
                err(f'paper/{p["id"]}/{sec["id"]}', f"criteria total {crit} != section marks {sec['marks']}")
        else:
            qm = sum(q.get("marks", 1) for q in qs)
            if qm != sec["marks"]:
                err(f'paper/{p["id"]}/{sec["id"]}',
                    f"question marks sum to {qm} but section is worth {sec['marks']}")
        for q in qs:
            check_q(f'{p["id"]}/{sec["id"]}#{q.get("n")}', q, sec["mode"], marks_expected=True)
        if sec.get("useVisual") and not sec.get("visualHtml"):
            err(f'paper/{p["id"]}/{sec["id"]}', "visual section has no rendered visual")

# ---------- answer-position balance ----------
# A set where the right answer is nearly always in the same slot can be scored
# by pattern-matching rather than reading, which makes it worthless as practice.
def explanation_check(s):
    """A wrong answer with no explanation teaches nothing, so a set of them is a defect.

    Two modes are exempt by design: listening sets, where the read-aloud script IS the
    explanation, and compose sets, which carry a 'why' note and examiner bands instead.
    """
    if s.get("listening") or s["mode"] == "compose":
        return
    qs = s["questions"]
    if len(qs) < 8:
        return
    missing = [q for q in qs if not (q.get("tip") or "").strip()]
    share = len(missing) / len(qs)
    if share > 0.75:
        err(s["letter"], f"{len(missing)} of {len(qs)} questions ({share:.0%}) have no explanation")
    elif share > 0.40:
        warn(s["letter"], f"{len(missing)} of {len(qs)} questions ({share:.0%}) have no explanation")


def position_check(label, qs):
    picks = [q["correct"] for q in qs
             if isinstance(q.get("correct"), int) and q.get("options")]
    if len(picks) < 8:
        return
    c = collections.Counter(picks)
    slot, hits = c.most_common(1)[0]
    share = hits / len(picks)
    if share > 0.45:
        err(label, f"answer-position bias: option {slot+1} is correct "
                   f"{share:.0%} of the time ({hits}/{len(picks)})")
    elif share > 0.38:
        warn(label, f"answer-position leaning towards option {slot+1} ({share:.0%})")

for s in bank:
    position_check(f'bank/{s["id"]}', s["questions"])
    explanation_check(s)
for p in papers:
    for sec in p["sections"]:
        position_check(f'paper/{p["id"]}/{sec["id"]}', sec["questions"])

# ---------- cross-set duplicates ----------
for text, wheres in seen_text.items():
    if len(wheres) > 1:
        sets_involved = {w.split("#")[0] for w in wheres}
        if len(sets_involved) > 1:
            warn("duplicate", f'same question in {", ".join(sorted(sets_involved))}: "{text[:70]}…"')

# ---------- report ----------
print(f"AUDITED  {len(bank)} sets · {total} questions · {len(papers)} papers\n")
for label, items in (("ERRORS", ERR), ("WARNINGS", WARN), ("NOTES", NOTE)):
    print(f"--- {label} ({len(items)}) ---")
    for where, msg in items[:60]:
        print(f"  [{where}] {msg}")
    if len(items) > 60:
        print(f"  … and {len(items)-60} more")
    print()

# ---------- picture panels ----------
# Composition pictures are drawings, so most of what matters about them can only be
# judged by looking. piccheck.py finds the part a machine can: figures that merge,
# shapes off the panel, and figures standing on nothing.
try:
    import piccheck, glob as _glob
    _files = sorted(f for f in _glob.glob(str(SRC / "content_*.json"))
                    if "composition" in f or "writing_oral" in f)
    _tot, _probs = 0, []
    for _f in _files:
        _n, _p = piccheck.check(_f)
        _tot += _n; _probs += _p
    print(f"\n--- PICTURE PANELS ({_tot} checked) ---")
    for _b in _probs:
        print("  [picture] " + _b)
    if not _probs:
        print("  no geometry problems")
except Exception as _e:
    print(f"\n--- PICTURE PANELS --- could not run piccheck: {_e}")
