#!/usr/bin/env python3
"""Build v2 of the study site: library + interactive practice + progress, two learner profiles."""
import json, re, html, pathlib
import markdown

SRC = pathlib.Path(__file__).parent
OUT = SRC / "site" / "index.html"
OUT.parent.mkdir(parents=True, exist_ok=True)   # so a fresh clone builds with no manual step

DOCS = [
    ("00_START_HERE_Study_Plan.md",        "Start here",         "Format, plan, routine"),
    ("01_Grammar_Reference.md",            "Grammar rules",      "Every rule, P3 to P6"),
    ("02_Grammar_Practice.md",             "Practice on paper",  "Printable worksheets"),
    ("03_Answer_Key.md",                   "Answer key",         "With explanations"),
    ("04_Vocabulary_Bank.md",              "Vocabulary",         "Words, idioms, phrases"),
    ("05_Composition_Guide.md",            "Composition",        "Continuous writing"),
    ("06_Situational_Writing_and_Oral.md", "Situational & oral", "Paper 1 Part 1, Paper 4"),
    ("07_Comprehension_Guide.md",           "Comprehension",      "Technique + 20 passages"),
    ("08_Writing_Model_Answers.md",         "Writing models",     "Marking rubric + 7 models"),
    ("09_Listening_Scripts.md",             "Listening scripts",  "For the adult reader"),
    ("10_Oral_Practice.md",                 "Oral practice",      "12 passages + 9 stimuli"),
    ("11_Situational_Writing_Models.md",    "Situational models", "20 tasks with model answers"),
    ("12_Picture_Composition_P3_P4.md",     "Picture composition","P3–P4, 12 tasks with models"),
    ("13_More_Grammar_Practice.md",         "More grammar",       "14 new sets + answer key"),
    ("14_More_Vocabulary_Practice.md",      "More vocabulary",    "11 new sets + answer key"),
    ("15_Full_Model_Compositions.md",       "Model compositions", "8 full compositions + bands"),
    ("16_Lower_Primary_Papers.md",          "P3 & P4 papers",     "Two papers with answers"),
]

md = markdown.Markdown(extensions=["tables", "attr_list", "sane_lists", "fenced_code", "toc"])


def slugify(t):
    return re.sub(r"[\s_]+", "-", re.sub(r"[^\w\s-]", "", t.lower()).strip())


def process(path):
    raw = path.read_text(encoding="utf-8")
    lines, title = raw.split("\n"), ""
    for i, ln in enumerate(lines):
        if ln.startswith("# "):
            title = ln[2:].strip()
            lines = lines[:i] + lines[i + 1:]
            break
    raw = "\n".join(lines)
    raw = re.sub(r"^(\s*)-\s\[\s\]\s", r"\1- ☐ ", raw, flags=re.M)

    fixed, prev = [], ""
    for ln in raw.split("\n"):
        if re.match(r"^\s{0,3}([-*+]\s|\d+\.\s)", ln) and prev.strip() and not re.match(r"^\s{0,3}([-*+]\s|\d+\.\s|[#>|])", prev):
            fixed.append("")
        fixed.append(ln); prev = ln
    raw = "\n".join(fixed)

    md.reset()
    body = md.convert(raw)

    sections, prefix = [], slugify(path.stem)
    def anchor(m):
        text = re.sub(r"<[^>]+>", "", m.group(1)).strip()
        sid = f"{prefix}--{slugify(text)}"
        sections.append({"id": sid, "text": text})
        return f'<h2 id="{sid}">{m.group(1)}</h2>'
    body = re.sub(r"<h2[^>]*>(.*?)</h2>", anchor, body, flags=re.S)
    body = body.replace("<table>", '<div class="tablewrap"><table>').replace("</table>", "</table></div>")
    return title, body, sections


docs = []
for fname, label, blurb in DOCS:
    t, b, s = process(SRC / fname)
    docs.append({"label": label, "blurb": blurb, "title": t, "body": b, "sections": s})

search_index = [{"d": i, "id": s["id"], "t": s["text"], "doc": d["label"]}
                for i, d in enumerate(docs) for s in d["sections"]]

nav_items = "\n".join(
    f'''<li><button class="navbtn" data-doc="{i}">
      <span class="navnum">{i:02d}</span>
      <span class="navtext"><strong>{html.escape(d["label"])}</strong><em>{html.escape(d["blurb"])}</em></span>
    </button><ul class="subnav" id="subnav-{i}"></ul></li>'''
    for i, d in enumerate(docs))

panels = "\n".join(
    f'''<article class="doc" id="doc-{i}" data-index="{i}">
      <header class="dochead"><span class="eyebrow">Document {i:02d}</span>
      <h1>{html.escape(d["title"] or d["label"])}</h1></header>{d["body"]}</article>'''
    for i, d in enumerate(docs))

bank = json.loads((SRC / "bank_full.json").read_text(encoding="utf-8"))
papers = json.loads((SRC / "papers.json").read_text(encoding="utf-8"))

T = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>English Workshop — P3 to P6</title>
<meta name="theme-color" content="#16233B">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,400;12..96,600;12..96,800&family=Literata:ital,opsz,wght@0,7..72,400;0,7..72,600;1,7..72,400&family=JetBrains+Mono:wght@400;600&display=swap" rel="stylesheet">
<style>
:root{
  --ink:#16233B; --muted:#5C6B85; --paper:#EEF1F7; --sheet:#FFFFFF; --line:#DCE2EC;
  --ok:#12855F; --ok-bg:#E4F4EC; --no:#D6392C; --no-bg:#FCEAE8;
  --accent:#10786A; --accent-soft:#E4F1EF; --accent-deep:#0B4F46;
  --gold:#F0B429;
  --sans:"Bricolage Grotesque",system-ui,sans-serif;
  --serif:"Literata",Georgia,serif;
  --mono:"JetBrains Mono",ui-monospace,monospace;
  --card:#FFFFFF; --wash:#F4F6FA; --field:#FBFCFE; --gold-bg:#FFF9E8;
  --on-accent:#FFFFFF; --on-ink:#FFFFFF; --gold-text:#8A6100;
  --r:14px; --shadow:0 1px 2px rgba(22,35,59,.05),0 10px 30px rgba(22,35,59,.07);
}

/* Dark mode. Follows the device by default; the moon button overrides it per child.
   Every surface colour is a token, so only the tokens change here. */
@media (prefers-color-scheme: dark){
  :root:not([data-theme="light"]){
    --ink:#E6ECF7; --muted:#9AA8BF; --paper:#11161F; --sheet:#1A212D; --line:#2B3442;
    --card:#1A212D; --wash:#212A38; --field:#141A24; --gold-bg:#2E2512;
    --on-accent:#06201C; --on-ink:#11161F; --gold-text:#F5C34B;
    --ok:#4ADE9B; --ok-bg:#122C23; --no:#FF8A7E; --no-bg:#301A18;
    --accent:#4FD1BE; --accent-soft:#12312D; --accent-deep:#8FE8DA;
    --gold:#F5C34B;
    --shadow:0 1px 2px rgba(0,0,0,.30),0 10px 30px rgba(0,0,0,.34);
  }
  :root:not([data-theme="light"]) body[data-level="P3"]{ --accent:#B79BFF; --accent-soft:#251A40; --accent-deep:#CDB8FF }
}
:root[data-theme="dark"]{
  --ink:#E6ECF7; --muted:#9AA8BF; --paper:#11161F; --sheet:#1A212D; --line:#2B3442;
  --card:#1A212D; --wash:#212A38; --field:#141A24; --gold-bg:#2E2512;
    --on-accent:#06201C; --on-ink:#11161F; --gold-text:#F5C34B;
  --ok:#4ADE9B; --ok-bg:#122C23; --no:#FF8A7E; --no-bg:#301A18;
  --accent:#4FD1BE; --accent-soft:#12312D; --accent-deep:#8FE8DA;
  --gold:#F5C34B;
  --shadow:0 1px 2px rgba(0,0,0,.30),0 10px 30px rgba(0,0,0,.34);
}
:root[data-theme="dark"] body[data-level="P3"]{ --accent:#B79BFF; --accent-soft:#251A40; --accent-deep:#CDB8FF }
@media print{ :root{ --ink:#000; --paper:#fff; --sheet:#fff; --card:#fff; --field:#fff; --gold-bg:#fff; --on-accent:#fff; --on-ink:#fff; --gold-text:#6A4A00; --muted:#333; --line:#999 } }
body[data-level="P3"]{ --accent:#6D3BEB; --accent-soft:#F0EAFF; --accent-deep:#4A22B3; font-size:18.5px }
body[data-level="P5"]{ font-size:17px }
*{box-sizing:border-box}
html{scroll-behavior:smooth}
body{margin:0;background:var(--paper);color:var(--ink);font-family:var(--serif);line-height:1.65;-webkit-font-smoothing:antialiased}
button,input,select{font:inherit;color:inherit}
button{cursor:pointer}
:focus-visible{outline:3px solid var(--accent);outline-offset:2px;border-radius:6px}
@media (prefers-reduced-motion:reduce){*{transition:none!important;animation:none!important;scroll-behavior:auto!important}}
.hide{display:none!important}

/* ============ shell ============ */
#topbar{position:sticky;top:0;z-index:30;background:color-mix(in srgb,var(--paper) 90%,transparent);backdrop-filter:blur(10px);border-bottom:1px solid var(--line)}
.bar{max-width:1120px;margin:0 auto;padding:11px 20px;display:flex;align-items:center;gap:14px}
.logo{font-family:var(--sans);font-weight:800;font-size:17px;letter-spacing:-.02em;white-space:nowrap}
.logo span{color:var(--accent)}
.tabs{display:flex;gap:4px;margin-left:8px;flex:1 1 auto;min-width:0;overflow-x:auto;scrollbar-width:none}
.tabs::-webkit-scrollbar{display:none}
.tab{font-family:var(--sans);font-weight:600;font-size:14.5px;padding:7px 14px;border-radius:100px;border:0;background:none;color:var(--muted);white-space:nowrap}
.tab:hover{color:var(--ink);background:#E3E8F1}
.tab.on{background:var(--ink);color:var(--paper)}
.who{display:flex;align-items:center;gap:8px;flex:0 0 auto;border:1px solid var(--line);background:var(--sheet);border-radius:100px;padding:4px 5px 4px 12px}
.who b{font-family:var(--sans);font-weight:600;font-size:14px}
.who .chip{white-space:nowrap;font-family:var(--mono);font-size:10px;letter-spacing:.06em;background:var(--accent-soft);color:var(--accent-deep);padding:3px 7px;border-radius:100px}
.who button{border:0;background:none;color:var(--muted);font-size:13px;font-family:var(--sans);padding:4px 8px;border-radius:100px}
.who button:hover{background:#EDF0F6;color:var(--ink)}
main{max-width:1120px;margin:0 auto;padding:26px 20px 110px}
@media(max-width:950px){
  .bar{flex-wrap:wrap;padding:9px 14px;gap:8px}
  .logo{font-size:15.5px}
  .who{order:2;margin-left:auto;padding:3px 4px 3px 10px}
  .tabs{order:3;width:100%;margin-left:0;flex:none}
  .tab{font-size:14px;padding:6px 12px}
  main{padding:18px 14px 90px}
  .qcard{padding:22px 20px 20px}
  .hero .card{padding:20px}
  .stats{gap:18px}
}
h1,h2,h3,h4{font-family:var(--sans);letter-spacing:-.018em}
.viewtitle{font-size:clamp(26px,4vw,36px);font-weight:800;margin:0 0 4px}
.viewsub{color:var(--muted);margin:0 0 26px;font-size:16px}

/* ============ cards ============ */
.card{background:var(--sheet);border:1px solid var(--line);border-radius:var(--r);box-shadow:var(--shadow)}
.grid{display:grid;gap:14px;grid-template-columns:repeat(auto-fill,minmax(268px,1fr))}
.sec{padding:18px 18px 16px;text-align:left;border:1px solid var(--line);background:var(--sheet);border-radius:var(--r);box-shadow:var(--shadow);display:flex;flex-direction:column;gap:10px;transition:transform .14s,box-shadow .14s,border-color .14s}
.sec:hover{transform:translateY(-2px);border-color:var(--accent);box-shadow:0 4px 8px rgba(22,35,59,.06),0 16px 34px rgba(22,35,59,.11)}
.sec .row{display:flex;align-items:center;justify-content:space-between;gap:10px}
.sec .letter{font-family:var(--mono);font-size:11px;color:var(--accent-deep);background:var(--accent-soft);padding:3px 8px;border-radius:6px;letter-spacing:.08em}
.sec h3{margin:0;font-size:18px;font-weight:600;line-height:1.25}
.sec .meta{font-family:var(--sans);font-size:13px;color:var(--muted)}
.lvl{font-family:var(--mono);font-size:10px;letter-spacing:.07em;color:var(--muted);border:1px solid var(--line);padding:2px 6px;border-radius:5px}
.bar-track{height:7px;background:var(--wash);border-radius:100px;overflow:hidden;box-shadow:inset 0 0 0 1px var(--line)}
.bar-fill{height:100%;background:var(--accent);border-radius:100px;transition:width .4s}
.bar-fill.gold{background:var(--gold)}
.bar-fill.good{background:var(--ok)}

/* dashboard */
.hero{display:grid;grid-template-columns:1.35fr 1fr;gap:14px;margin-bottom:26px}
@media(max-width:760px){.hero{grid-template-columns:1fr}}
.hero .card{padding:24px}
.hi{font-size:clamp(24px,3.6vw,32px);font-weight:800;margin:0 0 6px}
.stats{display:flex;gap:26px;margin-top:18px;flex-wrap:wrap}
.stat b{display:block;font-family:var(--sans);font-size:28px;font-weight:800;line-height:1}
.stat span{font-family:var(--mono);font-size:10.5px;letter-spacing:.1em;text-transform:uppercase;color:var(--muted)}
.btn{font-family:var(--sans);font-weight:600;font-size:15px;padding:11px 20px;border-radius:100px;border:0;background:var(--accent);color:var(--on-accent)}
.btn:hover{background:var(--accent-deep)}
.btn.ghost{background:var(--sheet);color:var(--ink);border:1px solid var(--line)}
.btn.ghost:hover{background:var(--wash);border-color:var(--muted)}
.btn.sm{font-size:13.5px;padding:8px 15px}
.btn:disabled{opacity:.4;cursor:not-allowed}
.btnrow{display:flex;gap:10px;flex-wrap:wrap;margin-top:20px}

/* ============ quiz ============ */
#quiz{max-width:720px;margin:0 auto}
.qtop{display:flex;align-items:center;gap:14px;margin-bottom:16px}
.qtop .bar-track{flex:1}
.qcount{font-family:var(--mono);font-size:12px;color:var(--muted);white-space:nowrap}
.qcard{padding:30px 30px 26px;position:relative;overflow:hidden}
.qcard::before{content:"";position:absolute;left:0;top:0;bottom:0;width:4px;background:var(--accent)}
.qcard.right::before{background:var(--ok)} .qcard.wrong::before{background:var(--no)}
.passage{background:var(--field);border:1px solid var(--line);border-radius:11px;padding:18px 20px;margin-bottom:20px;max-height:300px;overflow-y:auto;font-size:16px;line-height:1.72}
.passage.open{max-height:none}
.passage h4{margin:0 0 10px;font-size:15px}
.passage p{margin:0 0 11px} .passage p:last-child{margin-bottom:0}
.ptoggle{font-family:var(--sans);font-size:13px;color:var(--accent-deep);background:none;border:0;padding:6px 0;margin-bottom:16px;text-decoration:underline}
/* ---------- game layer ---------- */
.xpbar{display:flex;align-items:center;gap:10px;margin-top:16px}
.xpbar .bar-track{flex:1;height:10px}
.xpbar .bar-fill{background:linear-gradient(90deg,var(--accent),var(--gold))}
.rank{display:flex;align-items:center;gap:11px}
.rankbadge{width:44px;height:44px;border-radius:12px;display:grid;place-items:center;flex:none;
  font-family:var(--sans);font-weight:800;font-size:16px;color:#fff;
  background:linear-gradient(140deg,var(--accent-deep),var(--accent));box-shadow:0 2px 8px rgba(0,0,0,.14)}
.rankname{font-family:var(--sans);font-weight:800;font-size:19px;letter-spacing:-.01em;line-height:1.1}
.ranksub{font-family:var(--mono);font-size:10.5px;letter-spacing:.09em;text-transform:uppercase;color:var(--muted)}
.combo{position:fixed;right:22px;bottom:22px;z-index:50;background:var(--ink);color:var(--on-ink);
  border-radius:14px;padding:11px 16px;font-family:var(--sans);font-weight:800;font-size:15px;
  box-shadow:0 8px 24px rgba(0,0,0,.22);opacity:0;transform:translateY(12px);
  transition:opacity .18s,transform .18s;pointer-events:none}
.combo.on{opacity:1;transform:none}
.combo.hot{background:linear-gradient(140deg,#D6392C,#F0B429)}
.combo small{display:block;font-weight:600;font-size:11px;opacity:.8;letter-spacing:.04em}
.xpfloat{position:fixed;z-index:60;font-family:var(--sans);font-weight:800;font-size:22px;
  color:var(--ok);pointer-events:none;animation:xpup 1s ease-out forwards}
@keyframes xpup{0%{opacity:0;transform:translateY(6px) scale(.9)}
  18%{opacity:1;transform:translateY(-4px) scale(1.06)}
  100%{opacity:0;transform:translateY(-38px) scale(1)}}
.badges{display:grid;grid-template-columns:repeat(auto-fill,minmax(150px,1fr));gap:11px}
.badge{border:1px solid var(--line);border-radius:12px;padding:14px;background:var(--sheet);text-align:center}
.badge .ic{font-size:26px;line-height:1}
.badge b{display:block;font-family:var(--sans);font-size:13.5px;margin-top:7px}
.badge span{display:block;font-size:12px;color:var(--muted);margin-top:3px;line-height:1.4}
.badge.locked{opacity:.42;filter:grayscale(1)}
.badge.got{border-color:var(--gold);background:var(--gold-bg)}
.quest{display:flex;align-items:center;gap:11px;padding:11px 0;border-bottom:1px solid var(--line)}
.quest:last-child{border-bottom:0}
.quest .tick{width:24px;height:24px;border-radius:50%;border:2px solid var(--line);flex:none;
  display:grid;place-items:center;font-size:13px;color:#fff}
.quest.done .tick{background:var(--ok);border-color:var(--ok)}
.quest .qt{flex:1;font-family:var(--sans);font-size:14.5px}
.quest.done .qt{color:var(--muted);text-decoration:line-through}
.quest .qx{font-family:var(--mono);font-size:11.5px;color:var(--gold-text);font-weight:600}
.versus{display:grid;grid-template-columns:1fr auto 1fr;gap:14px;align-items:center;margin-top:14px}
.vs-side{text-align:center}
.vs-side b{display:block;font-family:var(--sans);font-weight:800;font-size:26px;line-height:1}
.vs-side span{font-family:var(--sans);font-size:13px;color:var(--muted)}
.vs-side.lead b{color:var(--ok)}
.vs-mid{font-family:var(--mono);font-size:11px;color:var(--muted);letter-spacing:.1em}
.boss{background:linear-gradient(140deg,#2A1F3D,#4A2C6B);color:#F1EAFB;border-radius:var(--r);padding:22px 24px}
.boss h3{margin:0 0 4px;font-size:19px;color:#fff}
.boss p{margin:0 0 14px;font-size:14.5px;color:#C9B6E8}
.boss .btn{background:var(--gold);color:#3A2B00}
.boss .btn:hover{background:#ffc94d}
.boss .btn:disabled{background:#51376F;color:#E8DEF7}
.toasts{position:fixed;left:50%;top:14px;transform:translateX(-50%);z-index:80;
  display:flex;flex-direction:column;gap:8px;align-items:center;pointer-events:none;width:calc(100% - 28px);max-width:380px}
.toast{display:flex;align-items:center;gap:12px;background:var(--ink);color:var(--on-ink);border-radius:12px;
  padding:11px 16px;box-shadow:0 10px 30px rgba(0,0,0,.24);width:100%;
  opacity:0;transform:translateY(-10px);transition:opacity .22s,transform .22s}
.toast.on{opacity:1;transform:none}
.toast .ic{font-size:24px;line-height:1;flex:none}
.toast.rankup{background:linear-gradient(140deg,var(--accent-deep),var(--accent))}
.toast.rankup .rankbadge{width:34px;height:34px;font-size:12px;border-radius:9px;background:rgba(255,255,255,.18);box-shadow:none}
.toast b{display:block;font-family:var(--sans);font-size:14.5px}
.toast em{display:block;font-style:normal;font-size:12.5px;opacity:.78;margin-top:1px}
.lvlup{position:fixed;inset:0;z-index:90;display:grid;place-items:center;background:rgba(18,26,44,.72);padding:20px}
.lvlup .card{max-width:380px;text-align:center;padding:32px 28px}
.lvlup .rankbadge{width:72px;height:72px;font-size:26px;margin:0 auto 16px}
.star{background:none;border:0;font-size:19px;line-height:1;padding:4px 6px;color:var(--muted);margin-left:auto}
.star.on{color:var(--gold)}
.qlabel{display:flex;align-items:center;gap:8px}
.kbd{font-family:var(--mono);font-size:10.5px;border:1px solid var(--line);border-bottom-width:2px;border-radius:5px;padding:1px 5px;color:var(--muted);background:var(--sheet)}
.drilltimer{font-family:var(--mono);font-size:13px;font-weight:600;background:var(--gold);color:#3A2B00;padding:5px 11px;border-radius:100px}
.drilltimer.low{background:var(--no);color:#fff}
.heard{margin-top:10px;border-top:1px solid var(--line);padding-top:8px}
.heard summary{cursor:pointer;font:600 13.5px/1 var(--sans);color:var(--muted)}
.heard summary:hover{color:var(--ink)}
.heard div{margin-top:8px;font-size:14.5px;line-height:1.6;color:var(--muted)}
.heard p{margin:0 0 8px}
.weakrow{display:flex;gap:12px;align-items:flex-start;width:100%;text-align:left;background:none;
  border:0;border-radius:10px;padding:9px 10px;cursor:pointer;font:inherit;color:inherit}
.weakrow:hover{background:var(--wash)}
.weaknum{flex:0 0 22px;height:22px;border-radius:999px;background:var(--ink);color:var(--card);
  font:700 12px/22px var(--mono);text-align:center;margin-top:2px}
.weakmain{flex:1;font-size:15px;line-height:1.35}
.logset{margin:0 0 10px;font:700 15px/1.3 var(--sans)}
.logset .cnt{font:600 12px/1 var(--mono);color:var(--muted);margin-left:8px}
.logjump{font:600 13px/1 var(--sans);background:none;border:1.5px solid var(--line);border-radius:999px;
  padding:6px 12px;cursor:pointer;color:var(--muted);margin-left:8px}
.logjump:hover{border-color:var(--ink);color:var(--ink)}
.tsbar{display:flex;gap:5px;align-items:center;margin-left:4px}
/* Between about 780 and 1150px the nav and the profile chip compete for the bar.
   Tighten the tabs rather than clipping the last one. */
@media (min-width:951px) and (max-width:1150px){
  .logo{font-size:15px}
  .tabs{margin-left:2px;gap:2px}
  .tab{padding:7px 9px;font-size:13.5px}
  .who{gap:6px;padding:3px 4px 3px 9px;font-size:13.5px}
  .who #switchBtn{font-size:12.5px}
}
.tsbtn{width:30px;height:30px;border-radius:8px;border:1.5px solid var(--line);background:var(--card);
  color:var(--muted);cursor:pointer;font:700 13px/1 var(--sans)}
.tsbtn.on{background:var(--ink);color:var(--card);border-color:var(--ink)}
body[data-ts="l"]{font-size:17.5px}
body[data-ts="xl"]{font-size:19.5px}
.lvlbar{display:flex;gap:8px;flex-wrap:wrap;margin:0 0 12px}
.grpbar{position:sticky;top:var(--barstick,0px);z-index:12;padding:10px 0 2px;margin-bottom:6px;
  background:var(--paper);border-bottom:1px solid var(--line)}
/* On a phone the seven chips wrapped to four rows, and the sticky top bar plus those
   rows took 44% of the screen. Below 760px they become one row you swipe sideways. */
@media (max-width:760px){
  .grpbar{flex-wrap:nowrap;overflow-x:auto;scrollbar-width:none;-webkit-overflow-scrolling:touch;
    padding:9px 0 9px;margin-left:-4px;margin-right:-4px}
  .grpbar::-webkit-scrollbar{display:none}
  .lvlchip.grp{flex:0 0 auto;white-space:nowrap}
  .grpbar>:first-child{margin-left:4px} .grpbar>:last-child{margin-right:4px}
}
.lvlchip.grp{font-size:13.5px;padding:9px 15px}
.lvlchip.grp .n{font-family:var(--mono);font-size:10.5px;opacity:.75;margin-left:6px}
.lvlchip.grp.empty{opacity:.45}
.lvlchip{font:600 13px/1 var(--ui);padding:8px 14px;border-radius:999px;border:1.5px solid var(--line);
  background:var(--card);color:var(--muted);cursor:pointer}
.lvlchip.on{background:var(--ink);color:var(--card);border-color:var(--ink)}
#setsearch{width:100%;max-width:420px;padding:10px 14px;border:1px solid var(--line);border-radius:100px;background:var(--sheet);font-family:var(--sans);font-size:14.5px;margin-bottom:18px}
.duepill{display:inline-block;font-family:var(--mono);font-size:10.5px;letter-spacing:.06em;background:var(--no);color:#fff;padding:2px 8px;border-radius:100px;margin-left:8px}
.duepill.zero{background:var(--ok)}
.goalwrap{margin-top:18px}
.goalwrap .bar-track{height:9px}
.whybox{background:#EEF6F3;border-left:3px solid var(--accent);border-radius:0 8px 8px 0;padding:12px 15px;margin-top:12px;font-size:14.5px}
.pacbox{background:var(--gold-bg);border-left:3px solid var(--gold);border-radius:0 8px 8px 0;padding:11px 14px;margin-bottom:14px;font-size:14px;white-space:pre-wrap}
.worksheet{display:none}
@media print{
  body.printing-ws .worksheet{display:block}
  body.printing-ws main>section,body.printing-ws #topbar{display:none!important}
  .worksheet h1{font-size:18pt;margin:0 0 4pt}
  .worksheet .wsmeta{font-family:var(--mono);font-size:9pt;color:#555;margin-bottom:14pt}
  .worksheet ol{padding-left:20pt}
  .worksheet li{margin-bottom:10pt;break-inside:avoid}
  .worksheet .wsline{border-bottom:1px solid #999;display:inline-block;min-width:150pt;margin-left:6pt}
  .worksheet .wskey{page-break-before:always}
}
.pics{display:grid;grid-template-columns:repeat(3,1fr);gap:10px;margin:16px 0}
.pics.four{grid-template-columns:repeat(4,1fr)}
@media(max-width:700px){.pics.four{grid-template-columns:repeat(2,1fr)}}
.pics figure{margin:0}
.pics svg{width:100%;display:block;border-radius:9px}
.pics figcaption{font-family:var(--sans);font-size:12px;color:var(--muted);margin-top:5px;text-align:center}
@media(max-width:600px){.pics{grid-template-columns:1fr}}
.taskbox{background:var(--field);border:1px solid var(--line);border-radius:11px;padding:16px 18px;margin-bottom:16px;white-space:pre-wrap;font-size:16px;line-height:1.68}
.theme{font-family:var(--sans);font-weight:800;font-size:26px;letter-spacing:-.02em;margin:2px 0 10px}
.wcount{font-family:var(--mono);font-size:12px;color:var(--muted);margin-top:8px}
.crit{margin-top:18px;border-top:1px solid var(--line);padding-top:16px}
.crit h4{margin:0 0 3px;font-size:15.5px}
.crit p{margin:0 0 10px;color:var(--muted);font-size:13.5px}
.bands{display:grid;gap:7px}
.bands button{text-align:left;display:flex;justify-content:space-between;gap:12px;padding:11px 14px;border:1px solid var(--line);border-radius:10px;background:var(--sheet);font-family:var(--sans);font-size:14.2px;line-height:1.45}
.bands button:hover{border-color:var(--accent);background:var(--accent-soft)}
.bands button.on{border-color:var(--accent);background:var(--accent-soft);font-weight:600}
.bands b{font-family:var(--mono);white-space:nowrap}
.timer{font-family:var(--mono);font-size:14px;font-weight:600;background:var(--ink);color:#fff;padding:6px 12px;border-radius:100px;white-space:nowrap}
.timer.low{background:var(--no)}
.secbanner{background:var(--accent-soft);color:var(--accent-deep);border-radius:9px;padding:11px 15px;margin-bottom:18px;font-family:var(--sans);font-size:14px}
.secbanner b{display:block;font-size:15.5px;margin-bottom:2px}
.visual{margin-bottom:20px;overflow-x:auto}
.marksheet{width:100%;border-collapse:collapse;font-size:15px;margin-top:8px}
.marksheet td{padding:8px 10px;border-bottom:1px solid var(--line)}
.marksheet td:last-child{text-align:right;font-family:var(--mono);white-space:nowrap}
.marksheet tr.tot td{font-weight:700;border-top:2px solid var(--ink);border-bottom:0;font-size:16.5px}
.awards{display:flex;gap:8px;flex-wrap:wrap;margin-top:13px}
.awards button{font-family:var(--sans);font-weight:600;font-size:14px;padding:8px 16px;border-radius:100px;border:1px solid var(--line);background:var(--sheet)}
.awards button:hover{border-color:var(--accent);background:var(--accent-soft)}
.marks{font-family:var(--mono);font-size:11px;color:var(--sheet);background:var(--muted);border-radius:5px;padding:2px 7px;margin-left:8px;vertical-align:2px}
.grouphead{grid-column:1/-1;margin:22px 0 2px}
.grouphead:first-child{margin-top:0}
.grouphead h2{font-size:19px;margin:0 0 3px}
.grouphead p{color:var(--muted);margin:0;font-size:14.5px}
.qlabel{font-family:var(--mono);font-size:10.5px;letter-spacing:.12em;text-transform:uppercase;color:var(--muted);margin-bottom:12px}
.qtext{font-size:19px;line-height:1.6;margin:0 0 20px}
.qtext.small{font-size:16.5px;line-height:1.72}
.qtext.pre{white-space:pre-wrap}
.qtext u{text-decoration:none;border-bottom:2.5px dotted var(--accent);padding-bottom:1px}
.blankmark{background:var(--accent-soft);border-radius:4px;padding:0 4px;font-weight:600;color:var(--accent-deep)}
.blankmark.on{background:var(--accent);color:#fff;box-shadow:0 0 0 3px var(--accent-soft)}
.blankmark.dim{opacity:.45}
textarea{width:100%;padding:14px 16px;border:2px solid var(--line);border-radius:11px;background:var(--field);font-family:var(--serif);font-size:17px;line-height:1.6;resize:vertical}
textarea:focus{outline:0;border-color:var(--accent);background:var(--card)}
textarea[readonly]{background:var(--wash);color:var(--muted)}
input[type=text]{width:100%;padding:14px 16px;border:2px solid var(--line);border-radius:11px;background:var(--field);font-family:var(--serif);font-size:18px}
input[type=text]:focus{outline:0;border-color:var(--accent);background:var(--card)}
input[type=text].right{border-color:var(--ok);background:var(--ok-bg)}
input[type=text].wrong{border-color:var(--no);background:var(--no-bg)}
.opts{display:grid;gap:9px}
.opt{display:flex;align-items:center;gap:12px;padding:13px 16px;border:2px solid var(--line);border-radius:11px;background:var(--field);text-align:left;font-family:var(--serif);font-size:17px}
.opt:hover{border-color:var(--accent)}
.opt .k{font-family:var(--mono);font-size:12px;color:var(--muted);border:1px solid var(--line);border-radius:6px;width:24px;height:24px;display:grid;place-items:center;flex:none}
.opt.sel{border-color:var(--accent);background:var(--accent-soft)}
.opt.right{border-color:var(--ok);background:var(--ok-bg)} .opt.right .k{border-color:var(--ok);color:var(--ok)}
.opt.wrong{border-color:var(--no);background:var(--no-bg)} .opt.wrong .k{border-color:var(--no);color:var(--no)}
.wordbank{display:flex;flex-wrap:wrap;gap:7px;margin-bottom:16px}
.wordbank button{font-family:var(--sans);font-size:14px;padding:6px 13px;border-radius:100px;border:1px dashed var(--muted);background:none;color:var(--muted)}
.wordbank button:hover{border-style:solid;border-color:var(--accent);color:var(--accent-deep);background:var(--accent-soft)}
.feedback{margin-top:18px;padding:15px 17px;border-radius:11px;display:none}
.feedback.show{display:block}
.feedback.right{background:var(--ok-bg)} .feedback.wrong{background:var(--no-bg)} .feedback.self{background:var(--wash)}
.fbhead{display:flex;align-items:center;gap:9px;font-family:var(--sans);font-weight:600;font-size:16px;margin-bottom:5px}
.fbhead .mk{width:24px;height:24px;flex:none}
.model{font-weight:600}
.tip{margin-top:7px;font-size:15px;color:var(--muted)}
.selfmark{display:flex;gap:9px;margin-top:13px}
.qfoot{display:flex;gap:10px;margin-top:20px;align-items:center;flex-wrap:wrap}
.hintline{font-family:var(--sans);font-size:13.5px;color:var(--muted)}

/* results */
.result{text-align:center;padding:40px 30px}
.score{font-family:var(--sans);font-weight:800;font-size:64px;line-height:1;letter-spacing:-.03em}
.result p{color:var(--muted);margin:8px 0 0}
.missed{text-align:left;margin-top:26px;border-top:1px solid var(--line);padding-top:20px}
.missed h4{margin:0 0 12px;font-size:15px}
.missed li{margin-bottom:11px;font-size:15.5px}
.missed .yours{color:var(--no)} .missed .theirs{color:var(--ok);font-weight:600}

/* error log */
.logitem{padding:15px 18px;border-bottom:1px solid var(--line)}
.logitem:last-child{border-bottom:0}
.logitem .q{font-size:15.5px}
.logitem .meta{font-family:var(--mono);font-size:10.5px;color:var(--muted);letter-spacing:.06em;text-transform:uppercase;margin-bottom:5px}
.empty{padding:52px 30px;text-align:center;color:var(--muted)}
.empty h3{color:var(--ink);margin:0 0 6px}

/* ============ library ============ */
#libwrap{display:grid;grid-template-columns:272px 1fr;gap:20px;align-items:start}
@media(max-width:900px){#libwrap{grid-template-columns:1fr}}
#libnav{position:sticky;top:74px;max-height:calc(100vh - 96px);overflow-y:auto;padding:12px}
#search{width:100%;padding:10px 13px;border:1px solid var(--line);border-radius:9px;background:var(--field);font-family:var(--sans);font-size:14px;margin-bottom:8px}
#navlist,#results{list-style:none;margin:0;padding:0}
.navbtn{display:flex;gap:10px;width:100%;text-align:left;background:none;border:0;padding:9px 10px;border-radius:9px;align-items:baseline}
.navbtn:hover{background:var(--wash)}
.navbtn.active{background:var(--accent-soft)}
.navnum{font-family:var(--mono);font-size:10.5px;color:var(--muted)}
.navbtn.active .navnum{color:var(--accent-deep)}
.navtext{display:flex;flex-direction:column}
.navtext strong{font-family:var(--sans);font-weight:600;font-size:14.5px}
.navtext em{font-style:normal;font-size:12px;color:var(--muted);font-family:var(--sans)}
.subnav{list-style:none;margin:0 0 6px;padding:0 0 0 34px;display:none}
.subnav.open{display:block}
.subnav a{display:block;padding:4px 0 4px 10px;font-family:var(--sans);font-size:12.8px;color:var(--muted);text-decoration:none;border-left:2px solid var(--line)}
.subnav a:hover{color:var(--accent-deep);border-left-color:var(--accent)}
#results li a{display:block;padding:9px 10px;border-radius:8px;text-decoration:none;font-family:var(--sans);font-size:13.5px}
#results li a:hover{background:var(--wash)}
#results span{display:block;font-family:var(--mono);font-size:10px;color:var(--muted);letter-spacing:.07em;text-transform:uppercase}
.sheet{background:var(--sheet);border:1px solid var(--line);border-radius:var(--r);box-shadow:var(--shadow);position:relative;overflow:hidden}
.sheet::before{content:"";position:absolute;top:0;bottom:0;left:52px;width:1.5px;background:var(--no);opacity:.42}
.doc{display:none;padding:40px 46px 56px 88px}
.doc.active{display:block}
@media(max-width:900px){.sheet::before{left:22px}.doc{padding:26px 20px 40px 42px}}
.dochead{margin-bottom:30px;padding-bottom:18px;border-bottom:1.5px solid var(--ink)}
.eyebrow{font-family:var(--mono);font-size:10.5px;letter-spacing:.14em;text-transform:uppercase;color:var(--no)}
.dochead h1{font-weight:800;font-size:clamp(25px,4vw,36px);line-height:1.1;margin:8px 0 0}
.doc h2{font-weight:800;font-size:22px;margin:46px 0 4px;padding-top:18px;border-top:1px solid var(--line);scroll-margin-top:84px}
.doc h3{font-weight:600;font-size:17px;margin:28px 0 2px;color:var(--accent-deep)}
.doc h4{font-weight:600;font-size:15px;margin:22px 0 0;color:var(--muted)}
.doc p{margin:13px 0} .doc a{color:var(--accent-deep)}
.doc ul,.doc ol{padding-left:22px;margin:13px 0} .doc li{margin:5px 0}
.doc li::marker{color:var(--accent)}
.doc hr{border:0;border-top:1px solid var(--line);margin:34px 0}
.doc hr+h2{border-top:0;padding-top:0;margin-top:24px}
.dochead+hr{display:none}
.doc code{font-family:var(--mono);font-size:.86em;background:var(--wash);padding:2px 5px;border-radius:4px}
.doc pre{background:#132033;color:#DCE6F2;padding:18px 20px;border-radius:9px;overflow-x:auto;font-size:13.5px;line-height:1.6}
.doc pre code{background:none;color:inherit;padding:0}
blockquote{margin:20px 0;padding:13px 18px;background:var(--gold-bg);border-left:3px solid var(--gold);border-radius:0 8px 8px 0}
blockquote p{margin:6px 0} blockquote p:first-child{margin-top:0} blockquote p:last-child{margin-bottom:0}
.tablewrap{overflow-x:auto;margin:18px 0;border:1px solid var(--line);border-radius:9px}
table{border-collapse:collapse;width:100%;font-size:14.6px}
th{background:var(--wash);font-family:var(--sans);font-weight:600;text-align:left;font-size:13px}
th,td{padding:9px 13px;border-bottom:1px solid var(--line);vertical-align:top}
tr:last-child td{border-bottom:0}
/* A stimulus (poster, notice, timetable) is self-contained HTML that brings its own look.
   The document table rules above used to leak into it: a stimulus <th> with no background of
   its own picked up var(--wash), which in dark mode put the stimulus's dark text on a dark
   header. Stop the app's chrome at the edge of .visual. */
.visual table,.visual th,.visual td{background:none;font-family:inherit;font-size:inherit;font-weight:inherit;text-align:inherit;border-bottom:0;padding:0;width:auto}
.masked .doc li,.masked .doc td,.masked .doc blockquote{filter:blur(4.5px);cursor:pointer;user-select:none;transition:filter .16s}
.masked .doc li.shown,.masked .doc td.shown,.masked .doc blockquote.shown{filter:none;background:var(--gold-bg)}
.libtools{display:flex;gap:9px;flex-wrap:wrap;margin-bottom:14px}
.masknote{display:none;font-family:var(--sans);font-size:13.5px;color:var(--no);margin-bottom:12px}
.masked .masknote{display:block}

/* ============ profile picker ============ */
#gate{position:fixed;inset:0;background:linear-gradient(160deg,#16233B,#0B4F46);z-index:90;display:grid;place-items:center;padding:20px}
.gatebox{max-width:520px;width:100%;background:var(--sheet);border-radius:20px;padding:34px}
.gatebox h2{margin:0 0 6px;font-size:26px;font-weight:800}
.gatebox p{margin:0 0 22px;color:var(--muted)}
.pick{display:grid;gap:11px}
.pick button{display:flex;align-items:center;gap:14px;padding:16px 18px;border:2px solid var(--line);border-radius:14px;background:none;text-align:left}
.pick button:hover{border-color:var(--accent)}
.av{width:44px;height:44px;border-radius:12px;display:grid;place-items:center;font-family:var(--sans);font-weight:800;font-size:18px;color:#fff;flex:none}
.pick strong{display:block;font-family:var(--sans);font-size:16.5px}
.pick em{font-style:normal;font-size:13.5px;color:var(--muted);font-family:var(--sans)}

@media print{
  #topbar,.libtools,.masknote,#gate,.tabs,.who{display:none!important}
  main{padding:0;max-width:none}
  #libwrap{display:block} #libnav{display:none}
  .sheet{border:0;box-shadow:none} .sheet::before{display:none} .doc{padding:0}
  .masked .doc li,.masked .doc td,.masked .doc blockquote{filter:none}
  body{font-size:11pt} tr{break-inside:avoid} .doc h2{break-after:avoid}
}
</style>
</head>
<body data-level="P5">

<div id="gate">
  <div class="gatebox">
    <h2>Who's practising today?</h2>
    <p>Each person gets their own progress and mistake list.</p>
    <div class="pick" id="pick"></div>
    <p style="margin:18px 0 0;font-size:13.5px">Tap a name later to rename it or switch.</p>
  </div>
</div>

<header id="topbar"><div class="bar">
  <div class="logo">English<span>·</span>Workshop</div>
  <nav class="tabs">
    <button class="tab on" data-view="home">Today</button>
    <button class="tab" data-view="practice">Practice</button>
    <button class="tab" data-view="papers">Mock papers</button>
    <button class="tab" data-view="library">Read &amp; print</button>
    <button class="tab" data-view="log">My mistakes</button>
  </nav>
  <div class="who"><b id="whoName">—</b><span class="chip" id="whoLvl">P5</span><button id="switchBtn">Switch</button>
    <span class="tsbar">
      <button class="tsbtn" id="sizeBtn" title="Text size">A</button>
      <button class="tsbtn" id="themeBtn" title="Light or dark">◑</button>
    </span></div>
</div></header>

<main>
  <!-- HOME -->
  <section id="v-home">
    <div class="hero">
      <div class="card">
        <h1 class="hi" id="greet">Ready when you are.</h1>
        <p style="color:var(--muted);margin:0" id="greetsub">Pick up where you left off, or start something new.</p>
        <div class="stats">
          <div class="stat"><b id="stStreak">0</b><span>Day streak</span></div>
          <div class="stat"><b id="stDone">0</b><span>Questions done</span></div>
          <div class="stat"><b id="stAcc">—</b><span>Accuracy</span></div>
          <div class="stat"><b id="stSecs">0/20</b><span>Sets tried</span></div>
        </div>
        <div class="rank gamebit" id="rankCard" style="margin-top:18px"></div>
        <div class="xpbar gamebit"><div class="bar-track"><div class="bar-fill" id="xpBar" style="width:0%"></div></div>
          <span class="ranksub" id="xpTxt"></span></div>
        <div class="goalwrap">
          <p style="font-family:var(--mono);font-size:10.5px;letter-spacing:.1em;text-transform:uppercase;color:var(--muted);margin:0 0 6px">
            This week <span id="goalTxt"></span></p>
          <div class="bar-track"><div class="bar-fill" id="goalBar" style="width:0%"></div></div>
        </div>
        <div class="btnrow">
          <button class="btn" id="goNext">Start today's set</button>
          <button class="btn ghost" id="goMistakes">Practise my mistakes</button>
        </div>
      </div>
      <div class="card" style="padding:24px">
        <h3 style="margin:0 0 4px;font-size:17px">Overall progress</h3>
        <p style="color:var(--muted);margin:0 0 16px;font-size:14.5px" id="ovSub">Across every practice set.</p>
        <div class="bar-track" style="height:11px"><div class="bar-fill" id="overall" style="width:0%"></div></div>
        <p style="font-family:var(--mono);font-size:12px;color:var(--muted);margin:10px 0 0"><span id="overallTxt">0%</span> complete</p>
        <div id="suggest" style="margin-top:20px"></div>
        <div style="margin-top:22px;padding-top:18px;border-top:1px solid var(--line)">
          <p style="font-family:var(--mono);font-size:10.5px;letter-spacing:.1em;text-transform:uppercase;color:var(--muted);margin:0 0 8px">What to work on</p>
          <div id="weakList"></div>
        </div>
      </div>
    </div>
    <div class="hero gamebit" style="margin-bottom:22px">
      <div class="card" style="padding:22px">
        <h3 style="margin:0 0 2px;font-size:16px">Today's quests</h3>
        <p style="color:var(--muted);margin:0 0 8px;font-size:14px">Three every day. They reset at midnight.</p>
        <div id="questList"></div>
      </div>
      <div class="card boss" id="bossCard"></div>
    </div>

    <div class="card gamebit" style="padding:22px;margin-bottom:22px">
      <h3 style="margin:0 0 2px;font-size:16px">Head to head</h3>
      <p style="color:var(--muted);margin:0;font-size:14px">Experience earned this week. Resets every Monday.</p>
      <div class="versus" id="versus"></div>
    </div>

    <h2 style="font-size:20px;margin:0 0 12px">Recommended for you</h2>
    <div class="grid" id="homeGrid"></div>
    <div class="card gamebit" style="padding:22px;margin-top:22px">
      <h3 style="margin:0 0 4px;font-size:16px">Badges</h3>
      <p style="color:var(--muted);margin:0 0 14px;font-size:14.5px"><span id="badgeCount"></span></p>
      <div class="badges" id="badgeWall"></div>
    </div>

    <div class="card" style="padding:22px;margin-top:22px">
      <h3 style="margin:0 0 4px;font-size:16px">Move progress between devices</h3>
      <p style="color:var(--muted);margin:0 0 14px;font-size:14.5px">Progress is stored in this browser only. Export a backup file here and import it on another device — it merges both learners' records rather than overwriting them.</p>
      <div class="btnrow" style="margin:0">
        <button class="btn ghost sm" id="expBtn">Export progress</button>
        <button class="btn ghost sm" id="impBtn">Import progress</button>
        <button class="btn ghost sm" id="gameBtn">Turn game mode off</button>
        <input type="file" id="impFile" accept="application/json" style="display:none">
      </div>
    </div>
  </section>

  <!-- PRACTICE -->
  <section id="v-practice" class="hide">
    <h1 class="viewtitle">Practice</h1>
    <p class="viewsub" id="practiceSub">Type your answer, get it marked instantly.</p>
    <div id="grpbar" class="lvlbar grpbar">
      <button class="lvlchip grp on" data-grp="all">Everything</button>
      <button class="lvlchip grp" data-grp="Oral">Oral</button>
      <button class="lvlchip grp" data-grp="Writing">Composition &amp; writing</button>
      <button class="lvlchip grp" data-grp="Comprehension">Comprehension</button>
      <button class="lvlchip grp" data-grp="Visual text &amp; listening">Visual text &amp; listening</button>
      <button class="lvlchip grp" data-grp="Grammar &amp; sentence work">Grammar</button>
      <button class="lvlchip grp" data-grp="Vocabulary">Vocabulary</button>
    </div>
    <div id="lvlbar" class="lvlbar">
      <button class="lvlchip on" data-lvl="all">All levels</button>
      <button class="lvlchip" data-lvl="P3">P3</button>
      <button class="lvlchip" data-lvl="P4">P4</button>
      <button class="lvlchip" data-lvl="P5">P5</button>
      <button class="lvlchip" data-lvl="P6">P6</button>
    </div>
    <input id="setsearch" type="search" placeholder="Search sets and questions — try &quot;tenses&quot; or &quot;passive&quot;…" aria-label="Search practice">
    <div class="grid" id="secGrid"></div>
  </section>

  <!-- QUIZ -->
  <section id="v-quiz" class="hide">
    <div id="quiz">
      <div class="qtop">
        <button class="btn ghost sm" id="quitBtn">← Back</button>
        <div class="bar-track"><div class="bar-fill" id="qbar" style="width:0%"></div></div>
        <div class="qcount" id="qcount">1 / 10</div>
      </div>
      <div class="card qcard" id="qcard"></div>
    </div>
  </section>

  <!-- PAPERS -->
  <section id="v-papers" class="hide">
    <h1 class="viewtitle">Mock papers</h1>
    <p class="viewsub">Full papers under exam conditions. No feedback until you finish, then a complete mark sheet.</p>
    <div class="grid" id="paperGrid"></div>
  </section>

  <!-- LOG -->
  <section id="v-log" class="hide">
    <h1 class="viewtitle">My mistakes</h1>
    <p class="viewsub" id="logSub">Wrong answers come back on a schedule — after 1 day, then 3, 7 and 21. Get one right four times and it retires.</p>
    <div class="btnrow" style="margin:0 0 18px">
      <button class="btn" id="logDue">Review what's due</button>
      <button class="btn ghost" id="logPractise">Practise all of them</button>
      <button class="btn ghost" id="logStars">Starred questions</button>
      <button class="btn ghost" id="logPrint">Print the list</button>
      <button class="btn ghost" id="logClear">Clear all</button>
    </div>
    <div class="card" id="logList"></div>
  </section>

  <div class="worksheet" id="wsHost"></div>

  <!-- LIBRARY -->
  <section id="v-library" class="hide">
    <div class="libtools">
      <button class="btn ghost sm" id="maskbtn" aria-pressed="false">Hide answers</button>
      <button class="btn ghost sm" id="printbtn">Print this document</button>
    </div>
    <p class="masknote">Answers are hidden. Tap any line to reveal just that one.</p>
    <div id="libwrap">
      <aside class="card" id="libnav">
        <input id="search" type="search" placeholder="Search all sections…" aria-label="Search sections">
        <ul id="navlist">%%NAV%%</ul>
        <ul id="results" hidden></ul>
      </aside>
      <div class="sheet">%%PANELS%%</div>
    </div>
  </section>
</main>

<script>
const BANK = %%QUESTIONS%%;
const PAPERS = %%PAPERS%%;
const INDEX = %%INDEX%%;

/* ---------- storage that degrades gracefully ---------- */
const Store = (()=>{
  let ok=true; try{ localStorage.setItem('_t','1'); localStorage.removeItem('_t'); }catch(e){ ok=false; }
  const mem={};
  return {
    get(k){ try{ return ok?localStorage.getItem(k):mem[k]; }catch(e){ return mem[k]; } },
    set(k,v){ try{ ok?localStorage.setItem(k,v):(mem[k]=v); }catch(e){ mem[k]=v; } },
    persistent: ok
  };
})();

const AVATARS=[{bg:'#6D3BEB',lvl:'P3'},{bg:'#10786A',lvl:'P5'}];
const blank=(name,lvl)=>({name,lvl,progress:{},log:[],stars:[],streak:0,last:'',done:0,right:0,
                          goal:120,week:{start:weekStart(),count:0}});
function weekStart(){ const d=new Date(); const n=(d.getDay()+6)%7; d.setDate(d.getDate()-n);
  return d.toISOString().slice(0,10); }
function bumpWeek(k){ const p=P(); if(!p.week||p.week.start!==weekStart()) p.week={start:weekStart(),count:0,xp:0};
  p.week.count+=(k||1); }
// spaced repetition: a missed item comes back after 1, 3, 7 then 21 days
const BOXES=[1,3,7,21];
function addDays(n){ const d=new Date(); d.setDate(d.getDate()+n); return d.toISOString().slice(0,10); }
function dueCount(){ const t=today(); return (P().log||[]).filter(l=>!l.due||l.due<=t).length; }
const RANKS=[
  [0,'Rookie','R'],[300,'Word Scout','WS'],[800,'Sentence Builder','SB'],
  [1600,'Grammar Cadet','GC'],[2800,'Clause Captain','CC'],[4400,'Vocab Voyager','VV'],
  [6400,'Comprehension Codebreaker','CK'],[9000,'Syntax Specialist','SS'],
  [12000,'Paper Slayer','PS'],[16000,'Language Marshal','LM'],
  [21000,'Grand Editor','GE'],[27000,'Wordsmith Supreme','WSU']];
function rankOf(xp){ let r=RANKS[0],i=0;
  RANKS.forEach((x,n)=>{ if(xp>=x[0]){ r=x; i=n; } });
  const next=RANKS[i+1]||null;
  return {i,name:r[1],tag:r[2],floor:r[0],next:next?next[0]:null,nextName:next?next[1]:null}; }

const BADGES=[
  {id:'first',  ic:'🎯', name:'First Blood',      how:'Answer your first question'},
  {id:'c10',    ic:'🔥', name:'Ten in a Row',     how:'Get 10 correct without a miss'},
  {id:'c25',    ic:'⚡', name:'Twenty-five Strong',how:'Get 25 correct without a miss'},
  {id:'q100',   ic:'💯', name:'Century',          how:'Answer 100 questions'},
  {id:'q500',   ic:'📚', name:'Five Hundred',     how:'Answer 500 questions'},
  {id:'q1000',  ic:'🏔️', name:'Thousand Club',    how:'Answer 1000 questions'},
  {id:'d3',     ic:'📅', name:'Three-day Streak', how:'Practise 3 days running'},
  {id:'d7',     ic:'🗓️', name:'Week Warrior',     how:'Practise 7 days running'},
  {id:'d30',    ic:'🏅', name:'Month of Mondays', how:'Practise 30 days running'},
  {id:'perf',   ic:'✨', name:'Flawless',         how:'Score 100% on any set'},
  {id:'perf5',  ic:'🌟', name:'Five Flawless',    how:'Score 100% on five sets'},
  {id:'goal',   ic:'🎽', name:'Goal Getter',      how:'Hit your weekly goal'},
  {id:'goal4',  ic:'🚀', name:'Four Weeks Running',how:'Hit your weekly goal 4 times'},
  {id:'fix10',  ic:'🔧', name:'Repair Crew',      how:'Retire 10 mistakes for good'},
  {id:'fix50',  ic:'🛠️', name:'Master Mechanic',  how:'Retire 50 mistakes for good'},
  {id:'due0',   ic:'🧹', name:'Clean Slate',      how:'Clear every due review in one day'},
  {id:'paper',  ic:'📄', name:'Paper Survivor',   how:'Finish a full mock paper'},
  {id:'paper3', ic:'🎖️', name:'Three Papers Down',how:'Finish three mock papers'},
  {id:'al2',    ic:'🥈', name:'AL2 Range',        how:'Score 75% or more on a mock paper'},
  {id:'al1',    ic:'🥇', name:'AL1 Range',        how:'Score 85% or more on a mock paper'},
  {id:'boss',   ic:'👑', name:'Boss Beaten',      how:'Clear a Boss Battle'},
  {id:'boss5',  ic:'💎', name:'Five Bosses',      how:'Clear five Boss Battles'},
  {id:'clock',  ic:'⏱️', name:'Beat the Clock',   how:'Finish a Beat the Clock run'},
  {id:'write',  ic:'✍️', name:'Writer',           how:'Complete a writing or oral task'},
  {id:'allgrp', ic:'🧭', name:'Explorer',         how:'Try a set from every group'},
  {id:'night',  ic:'🌙', name:'Night Owl',        how:'Practise after 9 p.m.'},
  {id:'early',  ic:'🌅', name:'Early Bird',       how:'Practise before 7 a.m.'},
];
function migrate(p){ p.stars=p.stars||[]; p.goal=p.goal||120;
  p.xp=p.xp||0; p.badges=p.badges||[]; p.best_combo=p.best_combo||0;
  p.perfect=p.perfect||0; p.retired=p.retired||0; p.bosses=p.bosses||0;
  p.goalweeks=p.goalweeks||0; p.groups=p.groups||[]; p.game=p.game!==false;
  p.quest=p.quest&&p.quest.day===today()?p.quest:null;
  p.week=p.week&&p.week.start?p.week:{start:weekStart(),count:0};
  (p.log||[]).forEach(l=>{ if(l.box===undefined){l.box=0;} if(!l.due){l.due=l.date||today();} }); }
let S = JSON.parse(Store.get('ew_state')||'null') || {
  cur:null, profiles:[blank('Younger','P3'), blank('Older','P5')]
};
const save=()=>Store.set('ew_state',JSON.stringify(S));
const P=()=>S.profiles[S.cur];
const starKey=q=>(q._sec||'')+'#'+q.n;
function isStarred(q){ return (P().stars||[]).some(x=>x.key===starKey(q)); }
function toggleStar(q){
  const p=P(), k=starKey(q), i=p.stars.findIndex(x=>x.key===k);
  if(i>=0) p.stars.splice(i,1);
  else p.stars.push({key:k,sec:q._sec,title:q._secTitle,mode:q.mode,options:q.options,correct:q.correct,
                     q:{n:q.n,q:q.q,a:q.a,m:q.m,tip:q.tip,blank:q.blank,marks:q.marks}});
  save(); return i<0;
}
const today=()=>new Date().toISOString().slice(0,10);

/* ---------- text marking ---------- */
const norm = s => (s||'').toLowerCase()
  .replace(/[\u2018\u2019]/g,"'").replace(/[\u201C\u201D]/g,'"')
  .replace(/[.,;:!?"“”]/g,' ').replace(/\s*…\s*/g,' ')
  .replace(/\s+/g,' ').trim();
// Damerau-Levenshtein: counts a transposition as ONE edit, not two.
// Swapping two letters is the commonest English spelling slip there is
// (recieve, thier, freind, beleive), and plain Levenshtein scores those 2,
// so a child who made one typing error was told they were simply wrong.
function lev(a,b){
  const m=a.length,n=b.length; if(Math.abs(m-n)>2) return 9;
  const d=Array.from({length:m+1},(_,i)=>[i,...Array(n).fill(0)]);
  for(let j=0;j<=n;j++) d[0][j]=j;
  for(let i=1;i<=m;i++) for(let j=1;j<=n;j++){
    d[i][j]=Math.min(d[i-1][j]+1,d[i][j-1]+1,d[i-1][j-1]+(a[i-1]===b[j-1]?0:1));
    if(i>1 && j>1 && a[i-1]===b[j-2] && a[i-2]===b[j-1])
      d[i][j]=Math.min(d[i][j], d[i-2][j-2]+1);
  }
  return d[m][n];
}
// Words the question itself offers as alternatives, e.g. "(affect / effect)".
// Choosing one of these is the wrong WORD, not a misspelling, so the spelling
// tolerance below must not soften it to "so close".
function offeredAlternatives(qtext){
  const out=[];
  for(const m of (qtext||'').matchAll(/\(([^()]*\/[^()]*)\)/g))
    for(const part of m[1].split('/')) { const t=part.trim(); if(t && t.split(/\s+/).length<=3) out.push(norm(t)); }
  return out;
}
function mark(user,accepted,qtext){
  const u=norm(user); if(!u) return 'blank';
  for(const a of accepted) if(u===norm(a)) return 'right';
  const acc=accepted.map(norm);
  const distractor = offeredAlternatives(qtext).some(o=>o===u && !acc.includes(o));
  if(distractor) return 'wrong';
  for(const a of accepted){ const n=norm(a); if(n.length>4 && lev(u,n)<=1) return 'close'; }
  return 'wrong';
}
const TICK=`<svg class="mk" viewBox="0 0 24 24" fill="none" stroke="#12855F" stroke-width="3.2" stroke-linecap="round" stroke-linejoin="round"><path d="M4 13l5.2 5.5L20 5"/></svg>`;
const CROSS=`<svg class="mk" viewBox="0 0 24 24" fill="none" stroke="#D6392C" stroke-width="3.2" stroke-linecap="round"><path d="M5 5l14 14M19 5L5 19"/></svg>`;
const esc = s => (s||'').replace(/[&<>]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;'}[c]));
const bold = s => s.replace(/\*\*([^*]+)\*\*/g,'<strong>$1</strong>');
function showBlanks(t,focus){
  let out=bold(esc(t));
  out=out.replace(/\((\d+)\)_{3,}/g,(m,n)=>
    `<span class="blankmark ${+n===focus?'on':(focus?'dim':'')}">&nbsp;${n}&nbsp;</span>`);
  out=out.replace(/_{3,}/g,'<span class="blankmark">&nbsp;?&nbsp;</span>');
  return out;
}

/* ---------- profile gate ---------- */
function renderPick(){
  document.getElementById('pick').innerHTML = S.profiles.map((p,i)=>
    `<button data-p="${i}"><span class="av" style="background:${AVATARS[i].bg}">${esc(p.name[0]||'?')}</span>
      <span><strong>${esc(p.name)}</strong><em>${p.lvl==='P3'?'Primary 3–4':'Primary 5–6'} · ${p.done} questions done</em></span></button>`).join('');
}
document.getElementById('pick').addEventListener('click',e=>{
  const b=e.target.closest('button[data-p]'); if(!b) return;
  S.cur=+b.dataset.p; touchStreak(); save(); document.getElementById('gate').classList.add('hide'); boot();
});
document.getElementById('switchBtn').onclick=()=>{
  const n=prompt('Rename this learner (or press Cancel to just switch):',P().name);
  if(n && n.trim()){ P().name=n.trim(); save(); boot(); return; }
  renderPick(); document.getElementById('gate').classList.remove('hide');
};
function touchStreak(){
  const p=P(), t=today();
  if(p.last===t) return;
  const y=new Date(Date.now()-864e5).toISOString().slice(0,10);
  p.streak = (p.last===y) ? p.streak+1 : 1;
  p.last=t;
}

/* ---------- views ---------- */
const views=['home','practice','quiz','papers','log','library'];
function go(v){
  views.forEach(x=>document.getElementById('v-'+x).classList.toggle('hide',x!==v));
  document.querySelectorAll('.tab').forEach(t=>t.classList.toggle('on',t.dataset.view===v));
  window.scrollTo({top:0});
  if(v==='home') renderHome();
  if(v==='practice') renderSecs();
  if(v==='log') renderLog();
  if(v==='papers') renderPapers();
}
document.querySelectorAll('.tab').forEach(t=>t.onclick=()=>go(t.dataset.view));
const TSIZES=['m','l','xl'], TSLABEL={m:'A',l:'A+',xl:'A++'};
function applySize(){
  const t=(P()||{}).ts||'m';
  document.body.dataset.ts=t;
  const b=document.getElementById('sizeBtn');
  if(b){ b.textContent=TSLABEL[t]; b.classList.toggle('on',t!=='m');
         b.title='Text size: '+TSLABEL[t]+' \u2014 tap to change'; }
}
document.getElementById('sizeBtn').onclick=()=>{
  const p=P(); p.ts=TSIZES[(TSIZES.indexOf(p.ts||'m')+1)%TSIZES.length]; save(); applySize();
};
// theme cycles device -> light -> dark and is remembered for this child
function applyTheme(){
  const t=(P()||{}).theme||'auto';
  if(t==='auto') document.documentElement.removeAttribute('data-theme');
  else document.documentElement.dataset.theme=t;
  const b=document.getElementById('themeBtn');
  if(b){ b.textContent = t==='auto'?'◑':(t==='light'?'☀':'☾');
         b.title = t==='auto'?'Following your device — tap for light':(t==='light'?'Light — tap for dark':'Dark — tap to follow your device'); }
}
document.getElementById('themeBtn').onclick=()=>{
  const p=P(); p.theme = p.theme==='auto'||!p.theme ? 'light' : (p.theme==='light'?'dark':'auto');
  save(); applyTheme();
};

const LEVELS={P3:'P3–P4',P4:'P3–P4',P5:'P5–P6',P6:'P5–P6'};
const forMe = s => P().lvl==='P3' ? (s.level==='P3'||s.level==='P4') : true;
const paperForMe = pp => { const L=pp.level||'P6';
  return P().lvl==='P3' ? (L==='P3'||L==='P4') : !(L==='P3'||L==='P4'); };
const pct = s => { const pr=P().progress[s.id]; return pr? Math.round(pr.best*100):0; };

function secCard(s){
  const pr=P().progress[s.id], p=pct(s);
  const cls = p>=90?'good':(p>0?'gold':'');
  return `<button class="sec" data-sec="${s.id}">
    <div class="row"><span class="letter">SET ${s.letter}</span><span class="lvl">${LEVELS[s.level]}</span></div>
    <h3>${esc(s.title)}</h3>
    <div class="meta">${s.questions.length} questions${pr?` · best ${p}%`:''}</div>
    ${s.alsoIn?`<div class="meta" style="color:var(--no);font-size:12.5px">Also used in ${esc(s.alsoIn)} — do this one well before sitting that paper</div>`:''}
    <div class="bar-track"><div class="bar-fill ${cls}" style="width:${p}%"></div></div>
  </button>`;
}
const GROUPNOTE={
  'Grammar & sentence work':'Rules, cloze, editing and synthesis — the bulk of Paper 2.',
  'Vocabulary':'Word choice in context, the way Booklet A tests it.',
  'Comprehension':'Full passages with model answers. The largest single component of the paper.',
  'Visual text & listening':'Posters, notices, timetables and charts, plus four listening papers an adult reads aloud to you.',
  'Writing':"Picture composition, full compositions, situational writing and planning drills — every one with a model answer and the examiner's bands.",
  'Oral':'Paper 4 practice. Reading aloud with what to listen for, and conversation stimuli. Say your answer out loud first, then type it and compare.'
};
function matchSets(term){
  const t=term.trim().toLowerCase();
  if(t.length<2) return null;
  return BANK.filter(s=>{
    if(LVLFILTER!=='all' && s.level!==LVLFILTER) return false;
    if(GRPFILTER!=='all' && s.group!==GRPFILTER) return false;
    if((s.title+' '+s.letter+' '+s.group).toLowerCase().includes(t)) return true;
    return s.questions.some(q=>((q.q||'')+' '+(q.m||'')).toLowerCase().includes(t));
  });
}
let LVLFILTER='all';
let GRPFILTER='all';
function renderSecs(){
  const tq=BANK.reduce((a,s)=>a+s.questions.length,0);
  document.getElementById('practiceSub').textContent=
    `${tq} questions across ${BANK.length} sets. Type your answer, get it marked instantly.`;
  const lvlOk = s => (LVLFILTER==='all' || s.level===LVLFILTER)
                  && (GRPFILTER==='all' || s.group===GRPFILTER);
  const mine=BANK.filter(s=>forMe(s)&&lvlOk(s)), rest=BANK.filter(s=>!forMe(s)&&lvlOk(s));
  let html='';
  if(!mine.length && !rest.length)
    html+=`<div class="grouphead"><h2>Nothing here yet</h2><p>${
      GRPFILTER==='all' ? `No sets at ${LVLFILTER}. Try another level.`
                        : `No ${GRPFILTER.toLowerCase()} sets at ${LVLFILTER==='all'?'this level':LVLFILTER}. Try another level, or another subject.`
    }</p></div>`;
  for(const g of Object.keys(GROUPNOTE)){
    const inG=mine.filter(s=>s.group===g); if(!inG.length) continue;
    const qn=inG.reduce((a,s)=>a+s.questions.length,0);
    html+=`<div class="grouphead"><h2>${g}</h2><p>${GROUPNOTE[g]} · ${inG.length} set${inG.length===1?'':'s'}, ${qn} questions</p></div>`+inG.map(secCard).join('');
  }
  if(rest.length){
    html+=`<div class="grouphead"><h2>Coming later</h2><p>Aimed at Primary 5 and 6. Have a go if you're curious.</p></div>`+rest.map(secCard).join('');
  }
  document.getElementById('secGrid').innerHTML=html;
}
function renderSearch(term){
  const hits=matchSets(term);
  if(hits===null){ renderSecs(); return; }
  const el=document.getElementById('secGrid');
  el.innerHTML = hits.length
    ? `<div class="grouphead"><h2>${hits.length} set${hits.length===1?'':'s'} match “${esc(term)}”</h2>
        <p>Clear the box to see everything again.</p></div>` + hits.map(secCard).join('')
    : `<div class="grouphead"><h2>Nothing matches “${esc(term)}”</h2><p>Try a shorter word.</p></div>`;
}
// Which topics is this child actually getting wrong? Ranked by how many mistakes are
// logged against a set, then by how far its best score is from full marks.
function diagnose(){
  const p=P(), tally={};
  for(const l of (p.log||[])){
    const s=BANK.find(x=>x.questions.some(q=>q.n===l.q.n && (q.q||'')===(l.q.q||'')))
          || BANK.find(x=>x.title===l.title);
    if(!s || !forMe(s)) continue;
    (tally[s.id] = tally[s.id] || {id:s.id, letter:s.letter, title:s.title, group:s.group, wrong:0}).wrong++;
  }
  const rows=Object.values(tally);
  for(const r of rows){
    const best=pct(BANK.find(x=>x.id===r.id));
    r.score=r.wrong*10 + (100-best)/10;
    r.why = r.wrong===1 ? '1 mistake logged here.' : `${r.wrong} mistakes logged here.`;
  }
  rows.sort((a,b)=>b.score-a.score);
  return rows.slice(0,5);
}
function renderWeak(diag){
  const host=document.getElementById('weakList'); if(!host) return;
  if(!diag.length){
    host.innerHTML=`<p style="color:var(--muted);margin:0;font-size:14.5px">Nothing to report yet. Once you have got a few questions wrong, the topics you find hardest will be listed here.</p>`;
    return;
  }
  const byGroup={};
  for(const d of diag) byGroup[d.group]=(byGroup[d.group]||0)+d.wrong;
  const worstGroup=Object.entries(byGroup).sort((a,b)=>b[1]-a[1])[0];
  host.innerHTML =
    `<p style="color:var(--muted);margin:0 0 10px;font-size:14.5px">Most of your mistakes are in <strong style="color:var(--ink)">${esc(worstGroup[0])}</strong>. These five sets come first.</p>`
    + diag.map((d,i)=>`<button class="weakrow" data-sec="${d.id}">
        <span class="weaknum">${i+1}</span>
        <span class="weakmain"><strong>Set ${d.letter} · ${esc(d.title)}</strong><br>
          <span style="color:var(--muted);font-size:13.5px">${esc(d.why)} Best ${pct(BANK.find(x=>x.id===d.id))}%.</span></span>
      </button>`).join('');
}
function renderHome(){
  const p=P();
  document.getElementById('whoName').textContent=p.name;
  document.getElementById('whoLvl').textContent=LEVELS[p.lvl];
  applySize();
  applyTheme();
  document.body.dataset.level=p.lvl;
  const h=new Date().getHours();
  document.getElementById('greet').textContent =
    `${h<12?'Good morning':h<18?'Good afternoon':'Good evening'}, ${p.name}.`;
  document.getElementById('stStreak').textContent=p.streak;
  document.getElementById('stDone').textContent=p.done;
  document.getElementById('stAcc').textContent=p.done?Math.round(p.right/p.done*100)+'%':'—';
  const tried=Object.keys(p.progress).length;
  document.getElementById('stSecs').textContent=tried+'/'+BANK.length;
  const mine=BANK.filter(forMe);
  const ov=Math.round(mine.reduce((a,s)=>a+pct(s),0)/mine.length);
  document.getElementById('overall').style.width=ov+'%';
  document.getElementById('overallTxt').textContent=ov+'%';
  if(!p.week||p.week.start!==weekStart()) p.week={start:weekStart(),count:0};
  if(p.week.count>=p.goal && p.week.hit!==p.week.start){
    p.week.hit=p.week.start; p.goalweeks=(p.goalweeks||0)+1; checkBadges(); save();
  }
  const gpc=Math.min(100,Math.round(p.week.count/p.goal*100));
  document.getElementById('goalBar').style.width=gpc+'%';
  document.getElementById('goalBar').className='bar-fill'+(gpc>=100?' good':'');
  document.getElementById('goalTxt').textContent=`${p.week.count} of ${p.goal} questions`;
  const due=dueCount();
  document.getElementById('goMistakes').disabled = due===0;
  document.getElementById('goMistakes').textContent =
    due ? `Review ${due} due question${due===1?'':'s'}` :
    (p.log.length? 'Nothing due today' : 'No mistakes saved yet');
  const diag = diagnose();
  const next = diag.length ? BANK.find(x=>x.id===diag[0].id) : (mine.find(s=>pct(s)<90) || mine[0]);
  document.getElementById('suggest').innerHTML =
    `<p style="font-family:var(--mono);font-size:10.5px;letter-spacing:.1em;text-transform:uppercase;color:var(--muted);margin:0 0 6px">Suggested next</p>
     <strong style="font-family:var(--sans);font-size:16px">Set ${next.letter} · ${esc(next.title)}</strong>
     ${diag.length?`<p style="color:var(--muted);margin:6px 0 0;font-size:14px">${esc(diag[0].why)}</p>`:''}`;
  renderWeak(diag);
  document.getElementById('goNext').onclick=()=>startQuiz(next.id);
  renderGame();
  document.getElementById('homeGrid').innerHTML = mine.filter(s=>pct(s)<90).slice(0,6).map(secCard).join('')
    || `<div class="card" style="padding:26px;grid-column:1/-1"><h3 style="margin:0 0 4px">Every set is above 90%.</h3>
        <p style="color:var(--muted);margin:0">Go back over your mistakes, or move up a level in Practice.</p></div>`;
}
document.body.addEventListener('click',e=>{
  const b=e.target.closest('[data-sec]'); if(b) startQuiz(b.dataset.sec);
});
document.getElementById('goMistakes').onclick=()=>startQuiz('__due__');
document.getElementById('logPractise').onclick=()=>startQuiz('__log__');
document.getElementById('logDue').onclick=()=>startQuiz('__due__');
document.getElementById('logStars').onclick=()=>startQuiz('__stars__');

/* ---------- quiz engine ---------- */
let Q=null;
function paintDrill(){
  const el=document.getElementById('qcount'); if(!el||!Q.drill) return;
  const left=Math.max(0,Math.ceil((Q.drillEnds-Date.now())/1000));
  el.innerHTML=`<span class="drilltimer ${left<=15?'low':''}">${left}s</span>
                <span style="margin-left:8px">${Q.i+1}/${Q.list.length}</span>`;
  if(left<=0){ clearInterval(Q.drillTick); Q.drill=false; finish(); }
}
function startQuiz(id, opts){
  let set,list;
  if(id==='__log__'||id==='__due__'){
    const t=today();
    const src=(P().log||[]).filter(l=>id==='__log__'||!l.due||l.due<=t);
    if(!src.length) return;
    list=src.map(l=>({...l.q,_sec:l.sec,_secTitle:l.title,mode:l.mode,options:l.options,correct:l.correct,wordbank:l.wordbank}));
    set={id:'__log__',letter:'★',title:id==='__due__'?'Due for review':'Your saved mistakes',mode:'mixed'};
  } else if(id==='__stars__'){
    const src=P().stars||[];
    if(!src.length) return;
    list=src.map(l=>({...l.q,_sec:l.sec,_secTitle:l.title,mode:l.mode,options:l.options,correct:l.correct}));
    set={id:'__stars__',letter:'★',title:'Starred questions',mode:'mixed'};
  } else {
    set=BANK.find(s=>s.id===id);
    list=set.questions.map(q=>({...q,mode:q.mode||set.mode,options:q.options,correct:q.correct,wordbank:set.wordbank,_sec:set.id,_secTitle:set.title}));
  }
  COMBO=0; showCombo();
  Q={set,list,i:0,right:0,missed:[]};
  if(opts&&opts.drill){
    Q.drill=true; Q.drillEnds=Date.now()+list.length*15000;
    clearInterval(Q.drillTick); Q.drillTick=setInterval(paintDrill,250);
  }
  go('quiz'); renderQ();
}
document.getElementById('quitBtn').onclick=()=>go(Q&&Q.set.id==='__log__'?'log':'practice');

function renderQ(){
  const q=Q.list[Q.i], n=Q.list.length;
  document.getElementById('qbar').style.width=(Q.i/n*100)+'%';
  document.getElementById('qcount').textContent=`${Q.i+1} / ${n}`;
  const mode=q.mode;
  const label = Q.set.id==='__log__' ? `Set ${q._secTitle}` : `Set ${Q.set.letter} · ${Q.set.title}`;
  let input='';
  if(mode==='mcq'){
    input=`<div class="opts">`+q.options.map((o,i)=>
      `<button class="opt" data-opt="${i}"><span class="k">${i+1}</span>${esc(o)}</button>`).join('')+`</div>`;
  } else if(mode==='compose'){
    input=`<textarea id="ans" rows="${q.pictures?18:14}" placeholder="${q.pictures?'Write your story here. About 120 to 180 words.':'Write your email or report here…'}" autocapitalize="sentences"></textarea>
           <div class="wcount" id="wc">0 words</div>`;
  } else if(mode==='self'||mode==='read'){
    input=`<textarea id="ans" rows="${mode==='read'?(q.marks>2?5:3):2}" placeholder="${mode==='read'?'Write your full answer…':'Write your sentence…'}" autocapitalize="sentences"></textarea>`;
  } else {
    input=(q.wordbank?`<div class="wordbank">`+q.wordbank.map(w=>`<button data-word="${esc(w)}">${esc(w)}</button>`).join('')+`</div>`:'')
      +`<input type="text" id="ans" placeholder="Your answer…" autocomplete="off" autocorrect="off" spellcheck="false">`;
  }
  const long = (q.q||'').length>150;
  document.getElementById('qcard').className='card qcard';
  const vis = (Q.set.visual||q._visual) ? `<div class="visual">${Q.set.visual||q._visual}</div>` : '';
  const scr = (Q.set.listening && q.script) ? `<button class="ptoggle" id="stog">Show the reader's script (adult only)</button><div class="passage hide" id="scriptbox">${q.script.split('\n\n').map(x=>`<p>${esc(x)}</p>`).join('')}</div>` : '';
  const psg = Q.set.passage ? `<div class="passage" id="psg"><h4>${esc(Q.set.title.replace('Comprehension · ',''))}</h4>${Q.set.passage.map(x=>`<p>${esc(x)}</p>`).join('')}</div><button class="ptoggle" id="ptog">Expand the passage</button>` : '';
  document.getElementById('qcard').innerHTML=`
    ${Q.banner||(Q.set.instruction?`<div class="secbanner"><b>${esc(Q.set.title)}</b>${esc(Q.set.instruction)}</div>`:'')}
    ${vis}${scr}${psg}
    <div class="qlabel">${esc(label)}${q.marks?`<span class="marks">${q.marks} mark${q.marks>1?'s':''}</span>`:''}
      <button class="star ${isStarred(q)?'on':''}" id="starBtn" title="Star this question (S)" aria-label="Star this question">${isStarred(q)?'★':'☆'}</button></div>
    <p class="qtext ${long?'small':''} ${mode==='compose'?'pre':''}">${showBlanks(q.q,q.blank)}</p>
    ${q.blank?`<p class="hintline" style="margin:-8px 0 14px">Fill blank <strong>${q.blank}</strong>.</p>`:''}
    ${q.pictures?`<div class="pics four">${q.pictures.map((pic,pi)=>
        `<figure>${pic.svg}<figcaption><b>${pi+1}.</b> ${esc(pic.caption)}</figcaption></figure>`).join('')}</div>`:''}
    ${q.pac?`<div class="pacbox"><strong>Before you write:</strong> ${esc(q.pac)}</div>`:''}
    ${input}
    ${mode==='self'?'<p class="hintline" style="margin-top:9px">Write it out, then check it against the model answer.</p>':''}
    ${mode==='read'&&Q.set.oral?`<p class="hintline" style="margin-top:9px">Say it out loud first, then type roughly what you said. ${q.tip ? esc(q.tip) : 'Aim for four to six sentences: Point, Elaborate, Example, Link.'}</p>`:''}
    ${mode==='read'&&!Q.set.oral?`<p class="hintline" style="margin-top:9px">Answer in full sentences. ${q.marks>1?q.marks+' marks means '+q.marks+' separate points.':'One mark — keep it short.'}</p>`:''}
    ${/…/.test(q.m||'')?'<p class="hintline" style="margin-top:9px">Two blanks here — separate your answers with a comma.</p>':''}
    <div class="feedback" id="fb"></div>
    <div class="qfoot"><button class="btn" id="checkBtn">Check</button>
      <button class="btn ghost hide" id="nextBtn">${Q.i+1===n?'See my score':'Next question'}</button></div>`;
  const ta0=document.getElementById('ans');
  if(mode==='compose'&&ta0){
    const cnt=()=>{const w=ta0.value.trim()?ta0.value.trim().split(/\s+/).length:0;
      document.getElementById('wc').textContent=w+' word'+(w===1?'':'s');};
    ta0.addEventListener('input',cnt); cnt();
  }
  const sb=document.getElementById('starBtn');
  if(sb) sb.onclick=()=>{ const on=toggleStar(q); sb.classList.toggle('on',on); sb.textContent=on?'★':'☆'; };
  const stog=document.getElementById('stog');
  if(stog) stog.onclick=()=>{ const b=document.getElementById('scriptbox'); b.classList.toggle('hide');
    stog.textContent=b.classList.contains('hide')?"Show the reader's script (adult only)":"Hide the script"; };
  const ptog=document.getElementById('ptog');
  if(ptog) ptog.onclick=()=>{ const b=document.getElementById('psg'); b.classList.toggle('open');
    ptog.textContent=b.classList.contains('open')?'Collapse the passage':'Expand the passage'; };
  const ans=document.getElementById('ans');
  if(ans){ ans.focus(); ans.addEventListener('keydown',e=>{
    if(e.key==='Enter' && ans.tagName==='INPUT'){ e.preventDefault(); document.getElementById('checkBtn').click(); }
    if(e.key==='Enter' && (e.metaKey||e.ctrlKey)){ e.preventDefault(); document.getElementById('checkBtn').click(); }
  }); }
  document.querySelectorAll('.wordbank button').forEach(b=>b.onclick=()=>{ ans.value=b.dataset.word; ans.focus(); });
  let sel=null;
  document.querySelectorAll('.opt').forEach(b=>b.onclick=()=>{
    if(b.closest('.opts').dataset.locked) return;
    document.querySelectorAll('.opt').forEach(x=>x.classList.remove('sel'));
    b.classList.add('sel'); sel=+b.dataset.opt;
  });
  if(!(Q&&Q.exam)) document.getElementById('checkBtn').onclick=()=>check(q,sel);
  document.getElementById('nextBtn').onclick=()=>{
    Q.i++; if(Q.i>=Q.list.length) finish(); else renderQ();
  };
  Q.pickOption=i=>{ const b=document.querySelector(`.opt[data-opt="${i}"]`); if(b) b.click(); };
  if(Q.drill) paintDrill();
}
// keyboard: 1-4 choose an option, Enter checks then advances, S stars
document.addEventListener('keydown',e=>{
  if(document.getElementById('v-quiz').classList.contains('hide')) return;
  const inField = /^(INPUT|TEXTAREA)$/.test((e.target.tagName||''));
  if(!inField && /^[1-4]$/.test(e.key) && Q && Q.pickOption){ e.preventDefault(); Q.pickOption(+e.key-1); return; }
  if(!inField && (e.key==='s'||e.key==='S')){ const b=document.getElementById('starBtn'); if(b){ e.preventDefault(); b.click(); } return; }
  if(e.key==='Enter' && !inField){
    const nb=document.getElementById('nextBtn'), cb=document.getElementById('checkBtn');
    if(nb && !nb.classList.contains('hide')){ e.preventDefault(); nb.click(); }
    else if(cb && !cb.classList.contains('hide')){ e.preventDefault(); cb.click(); }
  }
});
function check(q,sel){
  const fb=document.getElementById('fb'), card=document.getElementById('qcard');
  const mode=q.mode;
  let verdict;
  if(mode==='mcq'){
    if(sel===null) return;
    document.querySelector('.opts').dataset.locked='1';
    document.querySelectorAll('.opt').forEach((b,i)=>{
      if(i===q.correct) b.classList.add('right');
      else if(i===sel) b.classList.add('wrong');
      b.classList.remove('sel');
    });
    verdict = sel===q.correct?'right':'wrong';
    finishCheck(q,verdict,q.options[sel]);
  } else {
    const el=document.getElementById('ans'), val=el.value;
    if(!val.trim()) return;
    el.readOnly=true;
    if(mode==='compose'){
      const crit=Q.set.criteria||[];
      el.readOnly=true;
      fb.className='feedback self show';
      fb.innerHTML=`<div class="fbhead">Model answer <span class="marks">${esc(q.kind||'')}</span></div>
        <div class="taskbox" style="margin-top:8px">${esc(q.m)}</div>
        ${q.why?`<div class="whybox"><strong>Why it scores:</strong> ${esc(q.why)}</div>`:''}
        ${crit.map((c,ci)=>`<div class="crit"><h4>${esc(c.name)} — out of ${c.max}</h4>
          <p>Compare yours with the model, then pick the band that fits.</p>
          <div class="bands" data-c="${ci}">${c.bands.map(bd=>
            `<button data-marks="${bd.marks}"><span>${esc(bd.label)}</span><b>${bd.marks}</b></button>`).join('')}</div></div>`).join('')}`;
      document.getElementById('checkBtn').classList.add('hide');
      const scores={};
      fb.querySelectorAll('.bands').forEach(g=>g.addEventListener('click',ev=>{
        const bb=ev.target.closest('button[data-marks]'); if(!bb) return;
        g.querySelectorAll('button').forEach(x=>x.classList.remove('on'));
        bb.classList.add('on'); scores[g.dataset.c]=+bb.dataset.marks;
        if(Object.keys(scores).length===crit.length){
          const got=Object.values(scores).reduce((a,b2)=>a+b2,0);
          const max=crit.reduce((a,c)=>a+c.max,0);
          finishCheck(q, got/max>=0.6?'right':'wrong', val, true);
          fb.insertAdjacentHTML('beforeend',
            `<p style="margin-top:14px;font-family:var(--sans);font-weight:600">You scored ${got} out of ${max}.</p>`);
        }
      }));
      return;
    }
    if(mode==='self'||mode==='read'){
      const guess=mark(val,q.a,q.q);
      fb.className='feedback self show';
      fb.innerHTML=`<div class="fbhead">Model answer</div><div class="model">${esc(q.m)}</div>
        ${q.tip?`<div class="tip">${esc(q.tip)}</div>`:''}
        <div class="selfmark"><button class="btn sm" data-self="1">${TICK.replace('class="mk"','style="width:16px;height:16px;vertical-align:-3px;stroke:#fff"')} I got it right</button>
        <button class="btn ghost sm" data-self="0">Not quite</button></div>`;
      document.getElementById('checkBtn').classList.add('hide');
      fb.querySelectorAll('[data-self]').forEach(b=>b.onclick=()=>{
        fb.querySelector('.selfmark').remove();
        finishCheck(q, b.dataset.self==='1'?'right':'wrong', val, true);
      });
      return;
    }
    const r=mark(val,q.a,q.q);
    el.classList.add(r==='right'?'right':'wrong');
    verdict = r==='right'?'right':(r==='close'?'close':'wrong');
    finishCheck(q,verdict,val);
  }
}
function finishCheck(q,verdict,given,quiet){
  const fb=document.getElementById('fb'), card=document.getElementById('qcard');
  const good = verdict==='right';
  card.classList.add(good?'right':'wrong');
  if(!quiet){
    fb.className='feedback show '+(good?'right':'wrong');
    const praise=['Correct.','Nicely done.','That\u2019s right.','Spot on.'][Math.floor(Math.random()*4)];
    const heard = (Q.set && Q.set.listening && q.script)
      ? `<details class="heard"><summary>What the reader said</summary><div>${
          q.script.split('\n\n').map(x=>`<p>${esc(x)}</p>`).join('')}</div></details>` : '';
    fb.innerHTML = good
      ? `<div class="fbhead">${TICK}${praise}</div>${q.tip?`<div class="tip">${esc(q.tip)}</div>`:''}${heard}`
      : `<div class="fbhead">${CROSS}${verdict==='close'?'So close — check the spelling.':'Not quite.'}</div>
         <div>Answer: <span class="model">${esc(q.m||q.a[0])}</span></div>
         ${q.tip?`<div class="tip">${esc(q.tip)}</div>`:''}${heard}`;
  }
  const p=P(); p.done++; if(good) p.right++; bumpWeek(1);
  p.dayCount=(p.dayCount||0)+1;
  if(good){
    COMBO++; p.best_combo=Math.max(p.best_combo||0,COMBO);
    p.dayCombo=Math.max(p.dayCombo||0,COMBO);
    const xp=Math.round((Q.drill?20:10)*comboMult());
    award(xp); floatXP(xp);
  } else { COMBO=0; award(4); }
  showCombo();
  if(!(p.groups||[]).includes(Q.set.group||'') && Q.set.group){ p.groups.push(Q.set.group); }
  const key=(q._sec||'')+'#'+q.n;
  const existing=p.log.find(l=>l.key===key);
  if(good){
    Q.right++;
    if(existing){                       // promote it up the review ladder
      existing.box=Math.min((existing.box||0)+1,BOXES.length);
      if(existing.box>=BOXES.length){ p.log=p.log.filter(l=>l.key!==key);
        Q.retired=(Q.retired||0)+1; p.retired=(p.retired||0)+1; }
      else existing.due=addDays(BOXES[existing.box]);
    }
  } else {
    Q.missed.push({q,given});
    if(existing){ existing.box=0; existing.due=addDays(BOXES[0]); existing.given=given; existing.date=today(); }
    else p.log.push({key,sec:q._sec,title:q._secTitle,mode:q.mode,options:q.options,correct:q.correct,
                     q:{n:q.n,q:q.q,a:q.a,m:q.m,tip:q.tip,blank:q.blank},given,date:today(),
                     box:0,due:addDays(BOXES[0])});
  }
  touchStreak(); checkBadges(); checkQuests(); save();
  document.getElementById('checkBtn').classList.add('hide');
  document.getElementById('nextBtn').classList.remove('hide');
  document.getElementById('nextBtn').focus();
}
function finish(){
  clearInterval(Q.drillTick); if(Q.drill){ Q.drillDone=true; } Q.drill=false;
  const n=Q.list.length, pc=Math.round(Q.right/n*100), p=P();
  if(Q.set.id!=='__log__'){
    const prev=p.progress[Q.set.id]||{best:0,tries:0};
    if(!prev.tries) p.dayNew=(p.dayNew||0)+1;
    p.progress[Q.set.id]={best:Math.max(prev.best,Q.right/n),tries:prev.tries+1};
    if(Q.right===n) p.perfect=(p.perfect||0)+1;
    if(Q.right/n>=0.8) p.dayGood=(p.dayGood||0)+1;
    if(Q.drillDone) grant('clock');
    if(['compose'].includes(Q.set.mode)) grant('write');
  }
  COMBO=0; showCombo();
  checkBadges(); checkQuests(); save();
  document.getElementById('qbar').style.width='100%';
  document.getElementById('qcount').textContent=`${n} / ${n}`;
  if(Q.boss){
    const cleared=Q.right>=12;
    if(cleared){ p.bosses=(p.bosses||0)+1; award(400); checkBadges(); save(); }
    document.getElementById('qcard').className='card qcard';
    document.getElementById('qcard').innerHTML=`<div class="result">
      <div style="font-size:54px;line-height:1">${cleared?'👑':'💀'}</div>
      <div class="score" style="color:${cleared?'var(--ok)':'var(--no)'};font-size:44px;margin-top:8px">${Q.right} / 15</div>
      <p><strong>${cleared?'Boss cleared.':'Not this time.'}</strong> ${cleared?'+400 experience.':'You need 12. Practise your weak sets and come back.'}</p>
      ${Q.missed.length?`<div class="missed"><h4>Went wrong (${Q.missed.length})</h4><ul>`+
        Q.missed.map(m=>`<li>${showBlanks(m.q.q,m.q.blank).slice(0,180)}<br>
          <span class="yours">You wrote: ${esc(m.given)}</span> · <span class="theirs">${esc(m.q.m||m.q.a[0])}</span></li>`).join('')+
        `</ul></div>`:''}
      <div class="btnrow" style="justify-content:center">
        <button class="btn" id="bossAgain">Try another</button>
        <button class="btn ghost" id="bossDone">Back to Today</button></div></div>`;
    document.getElementById('bossAgain').onclick=startBoss;
    document.getElementById('bossDone').onclick=()=>go('home');
    return;
  }
  const msg = pc>=90?'Excellent. This one is solid.' : pc>=70?'Good — a few to tidy up.' :
              pc>=50?'Getting there. Read the rule again, then retry.' : 'Read the rule again, then have another go — this one just needs practice.';
  document.getElementById('qcard').className='card qcard';
  document.getElementById('qcard').innerHTML=`<div class="result">
    <div class="score" style="color:${pc>=70?'var(--ok)':'var(--no)'}">${pc}%</div>
    <p><strong>${Q.right} out of ${n}</strong> — ${msg}</p>
    ${Q.missed.length?`<div class="missed"><h4>Saved to your mistakes (${Q.missed.length})</h4><ul>`+
      Q.missed.map(m=>`<li>${showBlanks(m.q.q,m.q.blank).slice(0,220)}<br>
        <span class="yours">You wrote: ${esc(m.given)}</span> · <span class="theirs">${esc(m.q.m||m.q.a[0])}</span></li>`).join('')+
      `</ul></div>`:''}
    <div class="btnrow" style="justify-content:center">
      ${Q.missed.length?`<button class="btn" id="retryMissed">Retry the ${Q.missed.length} I missed</button>`:''}
      <button class="btn ghost" id="againBtn">Do the whole set again</button>
      ${Q.set.id.indexOf('__')!==0?`<button class="btn ghost" id="drillBtn">Beat the clock (15s a question)</button>`:''}
      ${Q.set.id.indexOf('__')!==0?`<button class="btn ghost" id="wsBtn">Print this set as a worksheet</button>`:''}
      <button class="btn ghost" id="doneBtn">Back to practice</button>
    </div></div>`;
  const rm=document.getElementById('retryMissed');
  if(rm) rm.onclick=()=>{ const list=Q.missed.map(m=>m.q); Q={set:Q.set,list,i:0,right:0,missed:[]}; renderQ(); };
  const db=document.getElementById('drillBtn');
  if(db) db.onclick=()=>startQuiz(Q.set.id,{drill:true});
  document.getElementById('againBtn').onclick=()=>startQuiz(Q.set.id);
  const wb=document.getElementById('wsBtn');
  if(wb) wb.onclick=()=>printWorksheet(Q.set.id);
  document.getElementById('doneBtn').onclick=()=>go(Q.set.id==='__log__'?'log':'practice');
}


/* ---------- mock papers ---------- */
function renderPapers(){
  const p=P();
  const mineP = PAPERS.filter(x=>paperForMe(x)), restP = PAPERS.filter(x=>!paperForMe(x));
  const card = (pp)=>{
    const i = PAPERS.indexOf(pp);
    const rec=(p.papers||{})[pp.id];
    return `<button class="sec" data-paper="${i}" style="grid-column:span 2">
      <div class="row"><span class="letter">${pp.type==='writing'?'PAPER 1':'PAPER 2'}</span><span class="lvl">${pp.minutes} MIN · ${pp.totalMarks} MARKS</span></div>
      <h3>${esc(pp.title)}</h3>
      <div class="meta">${pp.type==='writing'?'2 parts · situational + composition':pp.sections.length+' sections · '+pp.sections.reduce((a,s)=>a+s.questions.length,0)+' questions'}${rec?` · best ${rec.best}/${pp.totalMarks}`:''}</div>
      <div class="bar-track"><div class="bar-fill ${rec&&rec.best/pp.totalMarks>=.75?'good':'gold'}" style="width:${rec?Math.round(rec.best/pp.totalMarks*100):0}%"></div></div>
      <div class="meta" style="font-size:12.5px">${esc(pp.note)}</div>
    </button>`;
  };
  const head = (t,sub)=>`<div class="grouphead" style="grid-column:1/-1"><h2>${t}</h2><p>${sub}</p></div>`;
  document.getElementById('paperGrid').innerHTML =
    (mineP.length ? head('Papers at your level', 'Start here. These match what '+(P().lvl==='P3'?'Primary 3 and 4':'Primary 5 and 6')+' actually sit.') + mineP.map(card).join('') : '')
    + (restP.length ? head('Other papers', 'Aimed at a different level. Have a go if you want a stretch, but do not judge yourself on the score.') + restP.map(card).join('') : '')
    + `<div class="card" style="padding:22px;grid-column:1/-1">
      <h3 style="margin:0 0 6px;font-size:16px">Before you start</h3>
      <p style="color:var(--muted);margin:0;font-size:14.5px">Sit somewhere quiet with paper for rough work. The timer runs from the moment you begin and does not pause. There is no feedback during the paper — you will get a full mark sheet at the end, and written answers are marked against the model answers one at a time.</p></div>`;
}
document.body.addEventListener('click',e=>{
  const b=e.target.closest('[data-paper]'); if(b) startPaper(+b.dataset.paper);
});

let timerId=null;
function startPaper(i){
  const pp=PAPERS[i];
  const list=[];
  pp.sections.forEach(sec=>sec.questions.forEach((q,idx)=>list.push({
    ...q, mode:q.mode||sec.mode, _visual:sec.visualHtml, _secId:sec.id, _secName:sec.name, _mins:sec.minutes,
    _instruction:sec.instruction, _first:idx===0, _passage:sec.passage,
    _secTitle:sec.name, _sec:pp.id+':'+sec.id
  })));
  Q={set:{id:pp.id,letter:'P',title:pp.title},list,i:0,right:0,missed:[],
     exam:true,paper:pp,answers:new Array(list.length).fill(null),
     ends:Date.now()+pp.minutes*60000};
  go('quiz'); tick();
  if(pp.type==='writing') renderWriteQ(); else renderExamQ();
}
function clockLeft(){ return (Q&&Q.exam)?Math.max(0,Q.ends-Date.now()):0; }
function clockText(){
  const left=clockLeft(), m=Math.floor(left/60000), sec=Math.floor(left%60000/1000);
  return `${m}:${String(sec).padStart(2,'0')}`;
}
// the markup a freshly rendered question uses, so the clock never flashes a placeholder
function clockHTML(){
  return `<span class="timer${clockLeft()<600000?' low':''}" id="etime">${clockText()}</span>`;
}
function tick(){
  clearInterval(timerId);
  const beat=()=>{
    if(!Q||!Q.exam){clearInterval(timerId);return;}
    const t=document.getElementById('etime');
    if(t){ t.textContent=clockText(); t.classList.toggle('low',clockLeft()<600000); }
    if(clockLeft()<=0){ clearInterval(timerId); reviewExam(); }
  };
  timerId=setInterval(beat,1000);
  beat();
}
function renderExamQ(){
  const q=Q.list[Q.i], n=Q.list.length;
  Q.banner = q._first ? `<div class="secbanner"><b>${esc(q._secName)}</b>${esc(q._instruction||'')}</div>` : '';
  Q.set.visual=null; Q.set.passage=q._passage&&Array.isArray(q._passage)?q._passage:(q._passage?[q._passage]:null);
  Q.set.title=q._secName;
  renderQ();
  document.getElementById('qbar').style.width=(Q.i/n*100)+'%';
  document.getElementById('qcount').innerHTML=
    `${clockHTML()} <span style="margin-left:8px">${Q.i+1}/${n}</span>`;
  // exam mode: no marking, just record and move on
  const chk=document.getElementById('checkBtn');
  chk.textContent = Q.i+1===n ? 'Finish and mark' : 'Next';
  chk.onclick=()=>{
    const el=document.getElementById('ans');
    const sel=document.querySelector('.opt.sel');
    Q.answers[Q.i]= el ? el.value : (sel? +sel.dataset.opt : null);
    Q.i++;
    if(Q.i>=n){ clearInterval(timerId); reviewExam(); } else renderExamQ();
  };
  const back=document.getElementById('quitBtn');
  back.textContent='← Leave paper';
  back.onclick=()=>{ if(confirm('Leave the paper? Your answers will be lost.')){ clearInterval(timerId); go('papers'); } };
}


/* ---------- writing paper ---------- */
function renderWriteQ(){
  const q=Q.list[Q.i], n=Q.list.length;
  Q.banner=`<div class="secbanner"><b>${esc(q._secName)}</b>${esc(q._instruction||'')}</div>`;
  const pics = q.pictures ? `<div class="pics">${q.pictures.map(p=>`<figure>${p.svg}<figcaption>${esc(p.caption)}</figcaption></figure>`).join('')}</div>` : '';
  const theme = q.theme ? `<div class="theme">Theme: ${esc(q.theme)}</div>` : '';
  document.getElementById('qcard').className='card qcard';
  document.getElementById('qcard').innerHTML=`
    ${Q.banner}
    ${theme}
    ${q.q?`<div class="taskbox">${esc(q.q)}</div>`:''}
    ${pics}
    <p class="hintline" style="margin:0 0 12px">${esc(q.planNote||'')}</p>
    <textarea id="ans" rows="16" placeholder="Write here. Plan first — you have ${q._mins} minutes for this part."></textarea>
    <div class="wcount" id="wc">0 words</div>
    <div class="qfoot"><button class="btn" id="checkBtn">${Q.i+1===n?'Finish and mark':'Next part'}</button></div>`;
  const ta=document.getElementById('ans');
  if(Q.answers[Q.i]) ta.value=Q.answers[Q.i];
  const count=()=>{ const w=ta.value.trim()?ta.value.trim().split(/\s+/).length:0;
    document.getElementById('wc').textContent=w+' word'+(w===1?'':'s'); };
  ta.addEventListener('input',count); count(); ta.focus();
  document.getElementById('qbar').style.width=(Q.i/n*100)+'%';
  document.getElementById('qcount').innerHTML=`${clockHTML()} <span style="margin-left:8px">Part ${Q.i+1}/${n}</span>`;
  document.getElementById('checkBtn').onclick=()=>{
    Q.answers[Q.i]=ta.value; Q.i++;
    if(Q.i>=n){ clearInterval(timerId); reviewWriting(); } else renderWriteQ();
  };
  const back=document.getElementById('quitBtn');
  back.textContent='← Leave paper';
  back.onclick=()=>{ if(confirm('Leave the paper? Your writing will be lost.')){ clearInterval(timerId); go('papers'); } };
}
let WV=null;
function reviewWriting(){
  WV={items:Q.list.map((q,i)=>({q,given:Q.answers[i]||'',scores:{}})),wi:0};
  markWriting();
}
function markWriting(){
  if(WV.wi>=WV.items.length){ writingSheet(); return; }
  const it=WV.items[WV.wi], q=it.q;
  document.getElementById('qbar').style.width='100%';
  document.getElementById('qcount').textContent=`Marking part ${WV.wi+1} / ${WV.items.length}`;
  const words=it.given.trim()?it.given.trim().split(/\s+/).length:0;
  document.getElementById('qcard').className='card qcard';
  document.getElementById('qcard').innerHTML=`
    <div class="secbanner"><b>Mark ${esc(q._secName)}</b>Read your own writing back, then pick the band that honestly describes it.</div>
    <div class="feedback show self" style="margin-top:0">
      <div class="fbhead">What you wrote <span class="marks">${words} words</span></div>
      <div style="white-space:pre-wrap">${esc(it.given||'(left blank)')}</div>
    </div>
    ${q.m?`<details style="margin-top:14px"><summary style="cursor:pointer;font-family:var(--sans);font-size:14px;color:var(--accent-deep)">Show a model answer</summary>
      <div class="taskbox" style="margin-top:10px">${esc(q.m)}</div></details>`:''}
    ${q.criteria.map((c,ci)=>`<div class="crit"><h4>${esc(c.name)} — out of ${c.max}</h4>
      <p>Pick the description that fits best.</p>
      <div class="bands" data-c="${ci}">${c.bands.map(bd=>
        `<button data-marks="${bd.marks}"><span>${esc(bd.label)}</span><b>${bd.marks}</b></button>`).join('')}</div></div>`).join('')}
    <div class="qfoot"><button class="btn" id="wNext" disabled>Next</button></div>`;
  document.querySelectorAll('.bands').forEach(g=>g.addEventListener('click',e=>{
    const b=e.target.closest('button[data-marks]'); if(!b) return;
    g.querySelectorAll('button').forEach(x=>x.classList.remove('on'));
    b.classList.add('on'); it.scores[g.dataset.c]=+b.dataset.marks;
    document.getElementById('wNext').disabled = Object.keys(it.scores).length < q.criteria.length;
  }));
  document.getElementById('wNext').onclick=()=>{ WV.wi++; markWriting(); };
}
function writingSheet(){
  const pp=Q.paper, p=P();
  const rows=[]; let got=0;
  WV.items.forEach(it=>{
    it.q.criteria.forEach((c,ci)=>{
      const m=it.scores[ci]||0; got+=m;
      rows.push(`<tr><td>${esc(it.q._secName)} · ${esc(c.name)}</td><td>${m} / ${c.max}</td></tr>`);
    });
  });
  const pc=Math.round(got/pp.totalMarks*100);
  p.papers=p.papers||{};
  const prev=p.papers[pp.id]||{best:0,tries:0};
  p.papers[pp.id]={best:Math.max(prev.best,got),tries:prev.tries+1};
  grant('write'); award(Math.round(got*4)); checkBadges(); touchStreak(); save();
  const weakest = WV.items.flatMap(it=>it.q.criteria.map((c,ci)=>({n:it.q._secName+' · '+c.name,r:(it.scores[ci]||0)/c.max})))
    .sort((a,b)=>a.r-b.r)[0];
  document.getElementById('qcount').textContent='Complete';
  document.getElementById('qcard').innerHTML=`<div class="result" style="text-align:left">
    <div style="text-align:center">
      <div class="score" style="color:${pc>=65?'var(--ok)':'var(--no)'}">${got}<span style="font-size:28px;color:var(--muted)">/${pp.totalMarks}</span></div>
      <p><strong>${pc}%</strong></p></div>
    <table class="marksheet">${rows.join('')}
      <tr class="tot"><td>Total</td><td>${got} / ${pp.totalMarks}</td></tr></table>
    <p style="color:var(--muted);font-size:13.5px;margin-top:14px">Each band awards the middle of its range, so a strong paper lands around 51 rather than 55. An examiner may go a mark either side.</p>
    <p style="color:var(--muted);font-size:14.5px;margin-top:12px">Weakest area: <strong style="color:var(--ink)">${esc(weakest.n)}</strong>. Work on that one thing this week — not all four.</p>
    <div class="btnrow" style="justify-content:center">
      <button class="btn" id="pDone">Back to papers</button>
      <button class="btn ghost" id="pPrint">Print this</button></div></div>`;
  document.getElementById('pDone').onclick=()=>go('papers');
  document.getElementById('pPrint').onclick=()=>window.print();
}

/* ---------- marking ---------- */
let RV=null;
function reviewExam(){
  const auto=[], manual=[];
  Q.list.forEach((q,i)=>{
    const given=Q.answers[i];
    if(q.mode==='mcq'){
      auto.push({q,given,score:(given===q.correct)?1:0,max:1});
    } else if(q.mode==='auto'||q.mode==='edit'){
      auto.push({q,given,score:mark(given||'',q.a,q.q)==='right'?1:0,max:1});
    } else {
      manual.push({q,given,max:q.marks||1,score:null});
    }
  });
  RV={auto,manual,mi:0};
  if(manual.length) markNext(); else showMarksheet();
}
function markNext(){
  if(RV.mi>=RV.manual.length){ showMarksheet(); return; }
  const it=RV.manual[RV.mi], q=it.q;
  document.getElementById('qbar').style.width='100%';
  document.getElementById('qcount').textContent=`Marking ${RV.mi+1} / ${RV.manual.length}`;
  const psg = Array.isArray(q._passage) ? `<div class="passage" id="psg">${q._passage.map(x=>`<p>${esc(x)}</p>`).join('')}</div><button class="ptoggle" id="ptog">Expand the passage</button>` : '';
  const btns=[]; for(let m=it.max;m>=0;m--) btns.push(`<button data-award="${m}">${m} mark${m===1?'':'s'}</button>`);
  document.getElementById('qcard').className='card qcard';
  document.getElementById('qcard').innerHTML=`
    <div class="secbanner"><b>Mark your own answer</b>Compare with the model, then award the marks you honestly earned.</div>
    ${psg}
    <div class="qlabel">${esc(q._secName)}<span class="marks">${it.max} mark${it.max>1?'s':''}</span></div>
    <p class="qtext ${(q.q||'').length>150?'small':''}">${showBlanks(q.q,q.blank)}</p>
    <div class="feedback show self" style="margin-top:0">
      <div class="fbhead">Your answer</div>
      <div>${esc(it.given||'(left blank)')}</div>
      <div class="fbhead" style="margin-top:14px">Model answer</div>
      <div class="model">${esc(q.m)}</div>
      ${it.max>1?`<div class="tip">${it.max} marks means ${it.max} separate points. Award one mark per point you actually made.</div>`:''}
    </div>
    <div class="awards">${btns.join('')}</div>`;
  const pt=document.getElementById('ptog');
  if(pt) pt.onclick=()=>{ const b=document.getElementById('psg'); b.classList.toggle('open');
    pt.textContent=b.classList.contains('open')?'Collapse the passage':'Expand the passage'; };
  document.querySelectorAll('[data-award]').forEach(b=>b.onclick=()=>{
    it.score=+b.dataset.award; RV.mi++; markNext();
  });
}
function showMarksheet(){
  const pp=Q.paper, p=P();
  const bySec={};
  [...RV.auto,...RV.manual].forEach(r=>{
    const id=r.q._secId; bySec[id]=bySec[id]||{name:r.q._secName,got:0,max:0};
    bySec[id].got+=(r.score||0); bySec[id].max+=r.max;
  });
  const got=Object.values(bySec).reduce((a,s)=>a+s.got,0);
  const pc=Math.round(got/pp.totalMarks*100);
  const band = pc>=85?'AL1 range':pc>=75?'AL2 range':pc>=65?'AL3 range':pc>=55?'AL4 range':pc>=45?'AL5 range':'Below AL5';
  const wrong=RV.auto.filter(r=>!r.score);
  wrong.forEach(r=>{
    const key=r.q._sec+'#'+r.q.n;
    if(!p.log.some(l=>l.key===key))
      p.log.push({key,sec:r.q._sec,title:r.q._secName,mode:r.q.mode,options:r.q.options,correct:r.q.correct,
        q:{n:r.q.n,q:r.q.q,a:r.q.a,m:r.q.m,tip:r.q.tip,blank:r.q.blank},
        given:(r.q.mode==='mcq'? (r.q.options[r.given]||'(blank)') : (r.given||'(blank)')),date:today()});
  });
  p.papers=p.papers||{};
  const prev=p.papers[pp.id]||{best:0,tries:0};
  p.papers[pp.id]={best:Math.max(prev.best,got),tries:prev.tries+1};
  p.done+=RV.auto.length; p.right+=RV.auto.filter(r=>r.score).length;
  if(pc>=85) grant('al1'); if(pc>=75) grant('al2');
  award(Math.round(got*4)); checkBadges(); checkQuests(); touchStreak(); save();
  document.getElementById('qcount').textContent='Complete';
  document.getElementById('qcard').className='card qcard';
  document.getElementById('qcard').innerHTML=`<div class="result" style="text-align:left">
    <div style="text-align:center">
      <div class="score" style="color:${pc>=65?'var(--ok)':'var(--no)'}">${got}<span style="font-size:28px;color:var(--muted)">/${pp.totalMarks}</span></div>
      <p><strong>${pc}%</strong> — ${band}</p>
    </div>
    <table class="marksheet">
      ${Object.values(bySec).map(s=>`<tr><td>${esc(s.name)}</td><td>${s.got} / ${s.max}</td></tr>`).join('')}
      <tr class="tot"><td>Total</td><td>${got} / ${pp.totalMarks}</td></tr>
    </table>
    <p style="color:var(--muted);font-size:14.5px;margin-top:18px">${wrong.length} objective question${wrong.length===1?' has':'s have'} been added to My mistakes. The weakest section above is where the next week of practice should go.</p>
    <div class="btnrow" style="justify-content:center">
      <button class="btn" id="pDone">Back to papers</button>
      <button class="btn ghost" id="pPrint">Print the mark sheet</button>
    </div></div>`;
  document.getElementById('pDone').onclick=()=>go('papers');
  document.getElementById('pPrint').onclick=()=>window.print();
}


/* ---------- XP, combo, badges ---------- */
let COMBO=0;
function comboBox(){
  let el=document.getElementById('combobox');
  if(!el){ el=document.createElement('div'); el.id='combobox'; el.className='combo';
           document.body.appendChild(el); }
  return el;
}
function showCombo(){
  const el=comboBox();
  if(COMBO<3){ el.classList.remove('on'); return; }
  el.classList.add('on');
  el.classList.toggle('hot', COMBO>=10);
  el.innerHTML=`${COMBO} in a row<small>${comboMult().toFixed(1)}× experience</small>`;
}
const comboMult=()=>COMBO>=20?2:COMBO>=10?1.5:COMBO>=5?1.25:1;
function floatXP(n){
  if(!P().game) return;
  const host=document.getElementById('checkBtn')||document.body;
  const r=host.getBoundingClientRect();
  const d=document.createElement('div');
  d.className='xpfloat'; d.textContent='+'+n+' XP';
  d.style.left=(r.left+r.width/2)+'px'; d.style.top=(r.top-6)+'px';
  document.body.appendChild(d); setTimeout(()=>d.remove(),1000);
}
function award(xp){
  const p=P();
  if(!p.week||p.week.start!==weekStart()) p.week={start:weekStart(),count:0,xp:0};
  p.week.xp=(p.week.xp||0)+xp;
  const before=rankOf(p.xp).i;
  p.xp+=xp;
  const after=rankOf(p.xp);
  if(after.i>before) setTimeout(()=>levelUp(after),450);
}
function levelUp(r){
  if(!P().game) return;
  const t=document.createElement('div'); t.className='toast rankup';
  t.innerHTML=`<span class="rankbadge">${r.tag}</span>
    <span><b>Rank up — ${esc(r.name)}</b><em>Keep going.</em></span>`;
  toastHost().appendChild(t);
  requestAnimationFrame(()=>t.classList.add('on'));
  setTimeout(()=>{ t.classList.remove('on'); setTimeout(()=>t.remove(),260); },4200);
}
function toastHost(){
  let el=document.getElementById('toasts');
  if(!el){ el=document.createElement('div'); el.id='toasts'; el.className='toasts';
           document.body.appendChild(el); }
  return el;
}
function grant(id){
  const p=P();
  if(p.badges.includes(id)) return false;
  p.badges.push(id); save();
  const b=BADGES.find(x=>x.id===id); if(!b||!p.game) return true;
  const t=document.createElement('div'); t.className='toast';
  t.innerHTML=`<span class="ic">${b.ic}</span><span><b>${esc(b.name)}</b><em>${esc(b.how)}</em></span>`;
  toastHost().appendChild(t);
  requestAnimationFrame(()=>t.classList.add('on'));
  setTimeout(()=>{ t.classList.remove('on'); setTimeout(()=>t.remove(),260); },3600);
  return true;
}
function checkBadges(){
  const p=P(), h=new Date().getHours();
  if(p.done>=1) grant('first');
  if(p.done>=100) grant('q100');
  if(p.done>=500) grant('q500');
  if(p.done>=1000) grant('q1000');
  if(p.best_combo>=10) grant('c10');
  if(p.best_combo>=25) grant('c25');
  if(p.streak>=3) grant('d3');
  if(p.streak>=7) grant('d7');
  if(p.streak>=30) grant('d30');
  if(p.perfect>=1) grant('perf');
  if(p.perfect>=5) grant('perf5');
  if(p.retired>=10) grant('fix10');
  if(p.retired>=50) grant('fix50');
  if(p.bosses>=1) grant('boss');
  if(p.bosses>=5) grant('boss5');
  if(p.goalweeks>=1) grant('goal');
  if(p.goalweeks>=4) grant('goal4');
  if((p.groups||[]).length>=6) grant('allgrp');
  if(h>=21) grant('night');
  if(h<7) grant('early');
  const tries=Object.values(p.papers||{}).reduce((a,x)=>a+(x.tries||0),0);
  if(tries>=1) grant('paper');
  if(tries>=3) grant('paper3');
}

/* ---------- daily quests ---------- */
const QUESTS=[
  {id:'q20', t:'Answer 20 questions',           x:60,  hit:p=>p.dayCount>=20},
  {id:'q40', t:'Answer 40 questions',           x:120, hit:p=>p.dayCount>=40},
  {id:'due', t:'Clear every due review',        x:100, hit:()=>dueCount()===0},
  {id:'c8',  t:'Get 8 correct in a row',        x:80,  hit:p=>(p.dayCombo||0)>=8},
  {id:'newset',t:'Try a set you have not done', x:70,  hit:p=>(p.dayNew||0)>=1},
  {id:'acc',  t:'Finish a set at 80% or better',x:90,  hit:p=>(p.dayGood||0)>=1},
];
function todayQuests(){
  const p=P();
  if(!p.quest){
    const seed=[...today()].reduce((a,c)=>a+c.charCodeAt(0),0);
    const pool=QUESTS.map((q,i)=>({q,k:(seed*(i+7))%97}));
    pool.sort((a,b)=>a.k-b.k);
    p.quest={day:today(),ids:pool.slice(0,3).map(x=>x.q.id),claimed:[]};
    p.dayCount=0; p.dayCombo=0; p.dayNew=0; p.dayGood=0;
    save();
  }
  return p.quest.ids.map(id=>QUESTS.find(q=>q.id===id)).filter(Boolean);
}
function checkQuests(){
  const p=P();
  todayQuests().forEach(q=>{
    if(!p.quest.claimed.includes(q.id) && q.hit(p)){
      p.quest.claimed.push(q.id); award(q.x); save();
    }
  });
}


/* ---------- game screens ---------- */
function renderGame(){
  const p=P(), on=p.game!==false;
  document.querySelectorAll('.gamebit').forEach(el=>el.classList.toggle('hide',!on));
  document.getElementById('gameBtn').textContent = on?'Turn game mode off':'Turn game mode on';
  if(!on) return;

  const r=rankOf(p.xp);
  document.getElementById('rankCard').innerHTML=
    `<div class="rankbadge">${r.tag}</div><div>
       <div class="rankname">${esc(r.name)}</div>
       <div class="ranksub">${p.xp.toLocaleString()} experience</div></div>`;
  const span=r.next? (p.xp-r.floor)/(r.next-r.floor) : 1;
  document.getElementById('xpBar').style.width=Math.round(span*100)+'%';
  document.getElementById('xpTxt').textContent =
    r.next ? `${(r.next-p.xp).toLocaleString()} to ${r.nextName}` : 'Top rank reached';

  const qs=todayQuests();
  document.getElementById('questList').innerHTML=qs.map(q=>{
    const done=p.quest.claimed.includes(q.id);
    return `<div class="quest ${done?'done':''}"><span class="tick">${done?'✓':''}</span>
      <span class="qt">${esc(q.t)}</span><span class="qx">+${q.x} XP</span></div>`;
  }).join('');

  const got=p.badges.length;
  document.getElementById('badgeCount').textContent=`${got} of ${BADGES.length} unlocked.`;
  const ordered=[...BADGES].sort((x,y)=>
    (p.badges.includes(y.id)?1:0)-(p.badges.includes(x.id)?1:0));
  document.getElementById('badgeWall').innerHTML=ordered.map(b=>{
    const has=p.badges.includes(b.id);
    return `<div class="badge ${has?'got':'locked'}"><div class="ic">${b.ic}</div>
      <b>${esc(b.name)}</b><span>${esc(b.how)}</span></div>`;
  }).join('');

  const wk=pr=>(!pr.week||pr.week.start!==weekStart())?0:(pr.week.xp||0);
  const a=S.profiles[0], b=S.profiles[1];
  const av=wk(a), bv=wk(b);
  document.getElementById('versus').innerHTML=
    `<div class="vs-side ${av>=bv&&av>0?'lead':''}"><b>${av}</b><span>${esc(a.name)}</span></div>
     <div class="vs-mid">VS</div>
     <div class="vs-side ${bv>=av&&bv>0?'lead':''}"><b>${bv}</b><span>${esc(b.name)}</span></div>`;

  renderBoss();
}

/* ---------- Boss Battle ---------- */
function weakSets(){
  const p=P();
  return BANK.filter(forMe).map(s=>{
    const pr=p.progress[s.id];
    return {s, score: pr? pr.best : -1};
  }).filter(x=>x.score<0.9).sort((a,b)=>a.score-b.score).map(x=>x.s);
}
function bossPool(){
  const p=P(), out=[];
  // anything due for review comes first, then questions from the weakest sets
  (p.log||[]).forEach(l=>out.push({...l.q,_sec:l.sec,_secTitle:l.title,mode:l.mode,
                                   options:l.options,correct:l.correct}));
  weakSets().forEach(s=>s.questions.forEach(q=>out.push({...q,mode:q.mode||s.mode,
    options:q.options,correct:q.correct,wordbank:s.wordbank,_sec:s.id,_secTitle:s.title})));
  // no writing or oral in a boss battle — it must be markable
  return out.filter(q=>['mcq','auto','edit'].includes(q.mode));
}
function bossReady(){
  const p=P();
  const tried=Object.keys(p.progress||{}).length;
  return (p.log||[]).length>=5 || tried>=3;
}
function renderBoss(){
  const p=P(), pool=bossPool();
  const ready=bossReady() && pool.length>=15;
  document.getElementById('bossCard').innerHTML=`
    <div class="ranksub" style="color:#C9B6E8">Boss battle</div>
    <h3>15 questions from your weak spots</h3>
    <p>Drawn from what you keep getting wrong. Get <strong style="color:#fff">12 or more</strong> to clear it.
       Cleared ${p.bosses||0} time${(p.bosses||0)===1?'':'s'}.</p>
    <button class="btn" id="bossBtn" ${ready?'':'disabled'}>${ready?'Take it on':'Finish three sets to unlock'}</button>`;
  const bb=document.getElementById('bossBtn');
  if(bb&&ready) bb.onclick=startBoss;
}
function startBoss(){
  const pool=bossPool();
  const pick=[]; const used=new Set();
  while(pick.length<15 && used.size<pool.length){
    const i=Math.floor(Math.random()*pool.length);
    if(used.has(i)) continue;
    used.add(i); pick.push(pool[i]);
  }
  Q={set:{id:'__boss__',letter:'👑',title:'Boss battle',mode:'mixed'},
     list:pick,i:0,right:0,missed:[],boss:true};
  go('quiz'); renderQ();
}

/* ---------- export / import ---------- */
document.getElementById('gameBtn').onclick=()=>{
  const p=P(); p.game=p.game===false; save(); renderHome();
};
document.getElementById('expBtn').onclick=()=>{
  const blob=new Blob([JSON.stringify(S,null,1)],{type:'application/json'});
  const a=document.createElement('a');
  a.href=URL.createObjectURL(blob);
  a.download=`english-workshop-progress-${today()}.json`;
  a.click(); URL.revokeObjectURL(a.href);
};
document.getElementById('impBtn').onclick=()=>document.getElementById('impFile').click();
document.getElementById('impFile').onchange=e=>{
  const f=e.target.files[0]; if(!f) return;
  const r=new FileReader();
  r.onload=()=>{
    try{
      const inc=JSON.parse(r.result);
      if(!inc||!Array.isArray(inc.profiles)) throw 0;
      inc.profiles.forEach((ip,i)=>{
        const cur=S.profiles[i]; if(!cur) { S.profiles[i]=ip; return; }
        // Lifetime counters take the higher of the two. Max rather than sum, so that
        // importing the same backup twice cannot inflate anything.
        for(const k of ['done','right','streak','xp','best_combo','perfect','bosses','goalweeks'])
          cur[k]=Math.max(cur[k]||0,ip[k]||0);
        // 'retired' is a count in older saves and a list in newer ones
        if(Array.isArray(cur.retired)||Array.isArray(ip.retired)){
          const a=Array.isArray(cur.retired)?cur.retired:[], b=Array.isArray(ip.retired)?ip.retired:[];
          cur.retired=[...new Set([...a,...b])];
        } else cur.retired=Math.max(cur.retired||0,ip.retired||0);
        // badges and completed groups are sets: union them, never lose one
        cur.badges=[...new Set([...(cur.badges||[]),...(ip.badges||[])])];
        cur.groups=[...new Set([...(cur.groups||[]),...(ip.groups||[])])];
        // this child's settings come across only when this device has no history of
        // its own, so importing a backup never silently changes a device in use
        const untouched=!(cur.done>0);
        for(const k of ['ts','theme','goal','name','lvl'])
          if(ip[k]!==undefined && (untouched || cur[k]===undefined)) cur[k]=ip[k];
        if(ip.week && (!cur.week || (ip.week.count||0)>(cur.week.count||0))) cur.week=ip.week;
        Object.keys(ip.progress||{}).forEach(k=>{
          const a=cur.progress[k]||{best:0,tries:0}, b=ip.progress[k];
          cur.progress[k]={best:Math.max(a.best,b.best),tries:(a.tries||0)+(b.tries||0)};
        });
        Object.keys(ip.papers||{}).forEach(k=>{
          cur.papers=cur.papers||{};
          const a=cur.papers[k]||{best:0,tries:0}, b=ip.papers[k];
          cur.papers[k]={best:Math.max(a.best,b.best),tries:(a.tries||0)+(b.tries||0)};
        });
        (ip.log||[]).forEach(l=>{ if(!cur.log.some(x=>x.key===l.key)) cur.log.push(l); });
        (ip.stars||[]).forEach(l=>{ cur.stars=cur.stars||[]; if(!cur.stars.some(x=>x.key===l.key)) cur.stars.push(l); });
      });
      S.profiles.forEach(migrate); save(); boot();
      const sum=S.profiles.map(x=>`${x.name}: ${x.done} questions, ${x.xp} XP, ${(x.badges||[]).length} badges, ${(x.log||[]).length} saved mistakes`).join('\n');
      alert('Progress merged. Nothing was overwritten.\n\n'+sum);
    }catch(err){ alert('That file could not be read. It should be a file exported from this app.'); }
  };
  r.readAsText(f);
};

/* ---------- printable worksheets ---------- */
function printWorksheet(setId){
  const s=BANK.find(x=>x.id===setId); if(!s) return;
  const host=document.getElementById('wsHost');
  const line='<span class="wsline"></span>';
  const plain=t=>bold(esc(t||'')).replace(/\((\d+)\)_{3,}/g,(m,n)=>`(${n})${line}`).replace(/_{3,}/g,line);
  const body=s.questions.map(q=>{
    if(s.mode==='mcq')
      return `<li>${plain(q.q)}<br>${q.options.map((o,i)=>`(${i+1}) ${esc(o)}`).join(' &nbsp; ')}</li>`;
    const hasBlank=/_{3,}/.test(q.q||'');
    return `<li>${plain(q.q)}${hasBlank?'':' '+line}</li>`;
  }).join('');
  const key=s.questions.map(q=>`<li>${esc(s.mode==='mcq'?`(${(q.correct??0)+1}) ${q.m}`:(q.m||q.a[0]))}</li>`).join('');
  host.innerHTML=`<h1>${esc(s.title)}</h1>
    <div class="wsmeta">${s.questions.length} questions · ${LEVELS[s.level]} · Name: ____________________  Date: __________</div>
    <ol>${body}</ol>
    <div class="wskey"><h1>Answer key — ${esc(s.title)}</h1><ol>${key}</ol></div>`;
  document.body.classList.add('printing-ws');
  window.print();
  setTimeout(()=>document.body.classList.remove('printing-ws'),400);
}

/* ---------- error log ---------- */
function renderLog(){
  const p=P(), el=document.getElementById('logList'), t=today();
  const due=dueCount();
  document.getElementById('logPractise').disabled=!p.log.length;
  document.getElementById('logDue').disabled=!due;
  document.getElementById('logDue').textContent = due?`Review what's due (${due})`:'Nothing due today';
  const st=document.getElementById('logStars');
  st.disabled=!(p.stars||[]).length;
  st.textContent=(p.stars||[]).length?`Starred questions (${p.stars.length})`:'No starred questions';
  if(!p.log.length){
    el.innerHTML=`<div class="empty"><h3>Nothing here yet.</h3><p>Questions you get wrong are collected here automatically.</p></div>`;
    return;
  }
  const groups={};
  for(const l of p.log){ (groups[l.title]=groups[l.title]||[]).push(l); }
  const order=Object.entries(groups).sort((a,b)=>b[1].length-a[1].length);
  el.innerHTML = order.map(([title,items])=>{
    const set=BANK.find(x=>x.title===title);
    const dueHere=items.filter(l=>!l.due||l.due<=t).length;
    const head=`<div class="logset">${esc(title)}
      <span class="cnt">${items.length} mistake${items.length===1?'':'s'}${dueHere?` · ${dueHere} due`:''}</span>
      ${set?`<button class="logjump" data-sec="${set.id}">Practise this set</button>`:''}</div>`;
    return head + items.sort((a,b)=>(a.due||'').localeCompare(b.due||'')).map(l=>`<div class="logitem">
    <div class="meta">${esc(l.title)} · ${l.date}
      ${(!l.due||l.due<=t)?'<span class="duepill">DUE NOW</span>'
        :`<span class="duepill zero">back on ${l.due}</span>`}
      <span style="color:var(--muted)"> · review ${(l.box||0)+1} of 4</span></div>
    <div class="q">${showBlanks(l.q.q,l.q.blank)}</div>
    <div style="margin-top:5px;font-size:15px"><span class="yours" style="color:var(--no)">You wrote: ${esc(l.given)}</span>
      · <span class="theirs" style="color:var(--ok);font-weight:600">${esc(l.q.m||l.q.a[0])}</span></div>
    ${l.q.tip?`<div class="tip" style="font-size:14.5px">${esc(l.q.tip)}</div>`:''}</div>`).join('');
  }).join('');
}
document.getElementById('logPrint').onclick=()=>window.print();
document.getElementById('logClear').onclick=()=>{ if(confirm('Clear every saved mistake for '+P().name+'?')){ P().log=[]; save(); renderLog(); } };

/* ---------- library ---------- */
const docsEl=[...document.querySelectorAll('.doc')], navBtns=[...document.querySelectorAll('.navbtn')];
function buildSub(i){
  const ul=document.getElementById('subnav-'+i); if(ul.dataset.b) return;
  ul.innerHTML=[...docsEl[i].querySelectorAll('h2')].map(h=>`<li><a href="#${h.id}" data-doc="${i}">${h.textContent}</a></li>`).join('');
  ul.dataset.b='1';
}
function showDoc(i,anchor){
  go('library');
  docsEl.forEach((d,n)=>d.classList.toggle('active',n===i));
  navBtns.forEach((b,n)=>b.classList.toggle('active',n===i));
  document.querySelectorAll('.subnav').forEach((s,n)=>s.classList.toggle('open',n===i));
  buildSub(i); setMask(i===3);
  if(anchor){ const el=document.getElementById(anchor); if(el){ el.scrollIntoView(); return; } }
  window.scrollTo({top:0});
}
navBtns.forEach((b,i)=>b.onclick=()=>showDoc(i));
document.addEventListener('click',e=>{
  const a=e.target.closest('.subnav a, #results a'); if(!a) return;
  e.preventDefault(); showDoc(+a.dataset.doc,a.getAttribute('href').slice(1));
  search.value=''; results.hidden=true; navlist.hidden=false;
});
function setMask(on){
  document.body.classList.toggle('masked',on);
  const b=document.getElementById('maskbtn');
  b.setAttribute('aria-pressed',on); b.textContent=on?'Show answers':'Hide answers';
  if(!on) document.querySelectorAll('.shown').forEach(e=>e.classList.remove('shown'));
}
document.getElementById('maskbtn').onclick=()=>setMask(!document.body.classList.contains('masked'));
document.getElementById('printbtn').onclick=()=>window.print();
document.querySelector('.sheet').addEventListener('click',e=>{
  if(!document.body.classList.contains('masked')) return;
  const t=e.target.closest('li, td, blockquote'); if(t) t.classList.add('shown');
});
const search=document.getElementById('search'), results=document.getElementById('results'), navlist=document.getElementById('navlist');
search.addEventListener('input',()=>{
  const q=search.value.trim().toLowerCase();
  if(q.length<2){ results.hidden=true; navlist.hidden=false; return; }
  navlist.hidden=true; results.hidden=false;
  const hits=INDEX.filter(x=>x.t.toLowerCase().includes(q)).slice(0,25);
  results.innerHTML=hits.length?hits.map(h=>`<li><a href="#${h.id}" data-doc="${h.d}"><span>${h.doc}</span>${h.t}</a></li>`).join('')
    :'<li style="padding:14px;color:var(--muted);font-family:var(--sans);font-size:13.5px">Nothing matches that.</li>';
});

/* ---------- boot ---------- */
document.getElementById('setsearch').addEventListener('input',e=>renderSearch(e.target.value));
function reRender(){
  const box=document.getElementById('setsearch');
  if(box.value.trim().length>1) renderSearch(box.value); else renderSecs();
}
document.getElementById('lvlbar').addEventListener('click',e=>{
  const b=e.target.closest('[data-lvl]'); if(!b) return;
  LVLFILTER=b.dataset.lvl;
  document.querySelectorAll('#lvlbar .lvlchip').forEach(c=>c.classList.toggle('on',c===b));
  countGroups(); reRender();
});
document.getElementById('grpbar').addEventListener('click',e=>{
  const b=e.target.closest('[data-grp]'); if(!b) return;
  GRPFILTER=b.dataset.grp;
  document.querySelectorAll('#grpbar .lvlchip').forEach(c=>c.classList.toggle('on',c===b));
  reRender();
  window.scrollTo({top:0,behavior:'smooth'});
});
// how many sets sit behind each subject chip, for the level currently chosen
function stickOffset(){
  const t=document.getElementById('topbar');
  document.documentElement.style.setProperty('--barstick',(t?t.offsetHeight:0)+'px');
}
addEventListener('resize',stickOffset);
function countGroups(){
  for(const c of document.querySelectorAll('#grpbar [data-grp]')){
    const g=c.dataset.grp;
    const n=BANK.filter(s=>(LVLFILTER==='all'||s.level===LVLFILTER)&&(g==='all'||s.group===g)).length;
    let tag=c.querySelector('.n');
    if(!tag){ tag=document.createElement('span'); tag.className='n'; c.appendChild(tag); }
    tag.textContent=n;
    c.classList.toggle('empty',n===0);
  }
}
function boot(){ S.profiles.forEach(migrate); renderHome(); countGroups(); stickOffset(); renderSecs(); showDocInit(); go('home'); }
function showDocInit(){ docsEl.forEach((d,n)=>d.classList.toggle('active',n===0)); navBtns[0].classList.add('active'); buildSub(0); }
if(S.cur===null || S.cur===undefined){ renderPick(); }
else { document.getElementById('gate').classList.add('hide'); touchStreak(); save(); boot(); }
</script>
</body>
</html>
"""

out = (T.replace("%%NAV%%", nav_items)
        .replace("%%PANELS%%", panels)
        .replace("%%INDEX%%", json.dumps(search_index, ensure_ascii=False))
        .replace("%%QUESTIONS%%", json.dumps(bank, ensure_ascii=False))
        .replace("%%PAPERS%%", json.dumps(papers, ensure_ascii=False)))
OUT.write_text(out, encoding="utf-8")
print(f"wrote {OUT} ({len(out)/1024:.0f} KB) · {sum(len(s['questions']) for s in bank)} questions")
