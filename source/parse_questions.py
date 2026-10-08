#!/usr/bin/env python3
"""Parse the practice workbook + answer key into a structured question bank."""
import json, re, pathlib

SRC = pathlib.Path(__file__).parent
PRAC = (SRC / "02_Grammar_Practice.md").read_text(encoding="utf-8")
KEY  = (SRC / "03_Answer_Key.md").read_text(encoding="utf-8")

# section letter -> (title, level, grading mode)
#   auto  = short answer, machine-marked
#   mcq   = multiple choice
#   self  = full-sentence rewrite, child self-marks against the model answer
SECTIONS = {
    "A": ("Nouns",                     "P3", "auto"),
    "B": ("Pronouns",                  "P3", "auto"),
    "C": ("Articles & determiners",    "P3", "auto"),
    "D": ("Subject–verb agreement",    "P3", "auto"),
    "E": ("Tenses",                    "P3", "auto"),
    "F": ("Adjectives & adverbs",      "P3", "auto"),
    "G": ("Prepositions",              "P4", "auto"),
    "H": ("Conjunctions & connectors", "P4", "auto"),
    "I": ("Modal verbs",               "P4", "auto"),
    "J": ("Punctuation",               "P4", "self"),
    "K": ("Active & passive voice",    "P5", "self"),
    "L": ("Reported speech",           "P5", "self"),
    "M": ("Relative clauses",          "P5", "self"),
    "N": ("Question tags",             "P5", "auto"),
    "O": ("Synthesis & transformation","P6", "self"),
}


def split_sections(text):
    """Return {letter: body} for '## SECTION X — ...' blocks."""
    out, cur, buf = {}, None, []
    for line in text.split("\n"):
        m = re.match(r"^##\s+SECTION\s+([A-T])\b", line)
        if m:
            if cur:
                out[cur] = "\n".join(buf)
            cur, buf = m.group(1), []
        elif cur is not None:
            buf.append(line)
    if cur:
        out[cur] = "\n".join(buf)
    return out


P = split_sections(PRAC)
K = split_sections(KEY)

CLEAN_ITALIC = re.compile(r"\*(.+?)\*")
TIP = re.compile(r"💡\s*\*?(.*?)\*?\s*$")


def strip_md(s):
    s = re.sub(r"\*\*(.+?)\*\*", r"\1", s)
    s = re.sub(r"\*(.+?)\*", r"\1", s)
    return s.strip()


def numbered(body):
    """Collect 'N. text' items, joining wrapped lines."""
    items, cur, num = {}, [], None
    for line in body.split("\n"):
        m = re.match(r"^(\d+)\.\s+(.*)$", line.strip())
        if m:
            if num is not None:
                items[num] = " ".join(cur).strip()
            num, cur = int(m.group(1)), [m.group(2)]
        elif num is not None:
            if line.strip() == "" or line.startswith("#") or line.startswith("**"):
                items[num] = " ".join(cur).strip()
                num, cur = None, []
            else:
                cur.append(line.strip())
    if num is not None:
        items[num] = " ".join(cur).strip()
    return items


def parse_answer(raw):
    """Split an answer-key entry into (accepted answers, model answer, tip)."""
    tip = ""
    m = re.search(r"💡\s*(.*)$", raw)
    if m:
        tip = strip_md(m.group(1))
        raw = raw[:m.start()].strip()
    model = strip_md(raw).rstrip(".").strip()

    alts = []
    # "(also accept: x)" / "(accept: x)" / "(also: x)"
    for m in re.finditer(r"\((?:also\s+|or\s*)?(?:accept:?|:)\s*([^)]+)\)", raw, re.I):
        alts += re.split(r"[/,]", m.group(1))
    raw = re.sub(r"\*?\((?:also\s+|or\s*)?(?:accept:?|:)\s*[^)]+\)\*?", "", raw, flags=re.I)
    main = strip_md(raw).rstrip(".").strip()

    # a trailing "(word, word)" lists synonyms, e.g. "horrified (dismayed, upset)"
    m = re.match(r"^(.+?)\s*\(([^()]+)\)$", main)
    # only treat the bracket as synonyms when every part is a short word or two,
    # otherwise it is an explanation and must not become an accepted answer
    if m and not re.search(r"\bthat\b", m.group(2)) and all(
            len(x.strip().split()) <= 2 for x in re.split(r"[/,]", m.group(2))):
        alts += re.split(r"[/,]", m.group(2))
        main = m.group(1).strip()

    cand = ([main] if main else []) + alts
    expanded = []
    for a in cand:
        a = a.strip().rstrip(".")
        if not a:
            continue
        if a.startswith("…") or a.endswith("…"):
            continue          # truncated illustration, not a full answer
        a = re.sub(r"\s*…\s*", " ", a)   # two-blank answer: "was watching … rang"
        if "/" in a and " " not in a.replace("/", ""):
            expanded += [x.strip() for x in a.split("/")]
        else:
            expanded.append(a)
        # inline optional bracket, e.g. "Ali said (that) he was hungry"
        if "(" in a:
            expanded.append(re.sub(r"\s*\([^)]*\)\s*", " ", a).strip())
            expanded.append(a.replace("(", "").replace(")", ""))
    out = [a for a in dict.fromkeys(x for x in expanded if x)]
    return out, (model or (out[0] if out else "")), tip


bank = []

# ---------- Sections A–O ----------
for letter, (title, level, mode) in SECTIONS.items():
    pq, ka = numbered(P[letter]), numbered(K[letter])
    qs = []
    for n in sorted(pq):
        if n not in ka:
            continue
        prompt = strip_md(pq[n])
        answers, model, tip = parse_answer(ka[n])
        if not answers:
            continue
        qs.append({"n": n, "q": prompt, "a": answers, "m": model, "tip": tip})
    bank.append({"id": f"sec{letter}", "letter": letter, "title": title,
                 "level": level, "mode": mode, "questions": qs})

# ---------- Section P: editing ----------
rows_q = re.findall(r"^\|\s*(\d+)\s*\|\s*(.+?)\s*\|\s*_+\s*\|$", P["P"], re.M)
rows_a = re.findall(r"^\|\s*(\d+)\s*\|\s*(.+?)\s*\|\s*(.+?)\s*\|$", K["P"], re.M)
akey = {}
for n, wrong, correct in rows_a:
    if wrong.strip() in ("Wrong", "---"):
        continue
    ans, model, tip = parse_answer(correct)
    akey.setdefault(int(n), []).append({"wrong": strip_md(wrong), "a": ans, "m": model, "tip": tip})
seen = {}
edit_qs = []
for n, line in rows_q:
    n = int(n)
    idx = seen.get(n, 0); seen[n] = idx + 1
    cands = akey.get(n, [])
    if idx < len(cands):
        c = cands[idx]
        edit_qs.append({"n": len(edit_qs) + 1, "q": strip_md(line),
                        "a": c["a"], "m": c["m"],
                        "tip": (f'The error was “{c["wrong"]}”. ' + c["tip"]).strip(),
                        "hint": c["wrong"]})
bank.append({"id": "secP", "letter": "P", "title": "Editing (spelling & grammar)",
             "level": "P5", "mode": "edit", "questions": edit_qs})

# ---------- Sections Q, R, T: cloze ----------
def cloze(section, title, level, blank_re):
    body = P[section]
    ks = numbered(K[section])
    qs = []
    # sentence context for each blank
    for n in sorted(ks):
        answers, model, tip = parse_answer(ks[n])
        if not answers:
            continue
        ctx = ""
        for para in re.split(r"\n\s*\n", body):
            t = para.strip()
            if not t or t.startswith(("#", ">", "|", "*Fill", "*Use")):
                continue
            if re.search(blank_re % n, t):
                ctx = re.sub(r"\s+", " ", strip_md(t)).strip()
                break
        qs.append({"n": n, "q": ctx or f"Blank {n}", "a": answers, "m": model, "tip": tip, "blank": n})
    return {"id": f"sec{section}", "letter": section, "title": title,
            "level": level, "mode": "auto", "questions": qs}

bank.append(cloze("Q", "Grammar cloze", "P5", r"\(%d\)_+"))
bank.append(cloze("R", "Comprehension cloze", "P6", r"\(%d\)_+"))

# ---------- Section S: vocabulary MCQ ----------
mcq_q = []
blocks = re.split(r"\n(?=\d+\.\s)", P["S"])
for b in blocks:
    m = re.match(r"^(\d+)\.\s+(.*?)\n\s*\(1\)\s*(.+?)\s*\(2\)\s*(.+?)\s*\(3\)\s*(.+?)\s*\(4\)\s*(.+?)\s*$", b.strip(), re.S)
    if m:
        mcq_q.append({"n": int(m.group(1)), "q": strip_md(m.group(2)),
                      "options": [strip_md(m.group(i)) for i in (3, 4, 5, 6)]})
ans_rows = re.findall(r"\|\s*(\d+)\s*\|\s*\((\d)\)\s*([a-z]+)\s*\|", K["S"])
amap = {int(n): (int(i), w) for n, i, w in ans_rows}
for q in mcq_q:
    if q["n"] in amap:
        idx, word = amap[q["n"]]
        q["correct"] = idx - 1
        q["a"] = [word]; q["m"] = word
        q["tip"] = ""
mcq_q = [q for q in mcq_q if "correct" in q]
bank.append({"id": "secS", "letter": "S", "title": "Vocabulary (multiple choice)",
             "level": "P4", "mode": "mcq", "questions": mcq_q})

# ---------- Section T: vocabulary cloze with word bank ----------
t = cloze("T", "Vocabulary cloze", "P5", r"\*\*\(%d\)_+\*\*")
t["wordbank"] = ["cautiously", "deafening", "drenched", "gathered",
                 "hesitated", "rummaged", "sheltered", "subsided"]
bank.append(t)

# ---------- report ----------
total = 0
for s in bank:
    n = len(s["questions"])
    total += n
    flag = "  ⚠️" if n == 0 else ""
    print(f'{s["letter"]:>2}  {s["title"][:34]:<34} {s["mode"]:<5} {s["level"]}  {n:>3}{flag}')
print(f"{'':>2}  {'TOTAL':<34} {'':<5} {'':<3} {total:>3}")

(SRC / "questions.json").write_text(json.dumps(bank, ensure_ascii=False), encoding="utf-8")
