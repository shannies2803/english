#!/usr/bin/env python3
"""Ten improvements from the eighth audit round."""
import pathlib, sys
p = pathlib.Path("build_site2.py"); s = p.read_text(encoding="utf-8")
n = [0]
def sub(old, new, label):
    global s
    if s.count(old) != 1: sys.exit(f"anchor {s.count(old)}x: {label}")
    s = s.replace(old, new); n[0] += 1; print(f"  {n[0]:2d}. {label}")

# ── 1 ── papers are now level-specific, so show each child the right ones first
sub("""  document.getElementById('paperGrid').innerHTML = PAPERS.map((pp,i)=>{""",
    """  const mineP = PAPERS.filter(x=>paperForMe(x)), restP = PAPERS.filter(x=>!paperForMe(x));
  const card = (pp)=>{
    const i = PAPERS.indexOf(pp);""",
    "Papers split into 'for this child' and the rest")

sub("""      <div class="meta" style="font-size:12.5px">${esc(pp.note)}</div>
    </button>`;
  }).join('') + `<div class="card" style="padding:22px;grid-column:1/-1">""",
    """      <div class="meta" style="font-size:12.5px">${esc(pp.note)}</div>
    </button>`;
  };
  const head = (t,sub)=>`<div class="grouphead" style="grid-column:1/-1"><h2>${t}</h2><p>${sub}</p></div>`;
  document.getElementById('paperGrid').innerHTML =
    (mineP.length ? head('Papers at your level', 'Start here. These match what '+(P().lvl==='P3'?'Primary 3 and 4':'Primary 5 and 6')+' actually sit.') + mineP.map(card).join('') : '')
    + (restP.length ? head('Other papers', 'Aimed at a different level. Have a go if you want a stretch, but do not judge yourself on the score.') + restP.map(card).join('') : '')
    + `<div class="card" style="padding:22px;grid-column:1/-1">""",
    "Paper grid rendered with level headings")

sub("const forMe = s => P().lvl==='P3' ? (s.level==='P3'||s.level==='P4') : true;",
    """const forMe = s => P().lvl==='P3' ? (s.level==='P3'||s.level==='P4') : true;
const paperForMe = pp => { const L=pp.level||'P6';
  return P().lvl==='P3' ? (L==='P3'||L==='P4') : !(L==='P3'||L==='P4'); };""",
    "paperForMe() helper")

# ── 2 ── a level filter on the practice screen: the P5–P6 child has 147 sets to wade through
sub("""<input id="setsearch" type="search" placeholder="Search sets and questions — try &quot;""",
    """<div id="lvlbar" class="lvlbar">
      <button class="lvlchip on" data-lvl="all">All levels</button>
      <button class="lvlchip" data-lvl="P3">P3</button>
      <button class="lvlchip" data-lvl="P4">P4</button>
      <button class="lvlchip" data-lvl="P5">P5</button>
      <button class="lvlchip" data-lvl="P6">P6</button>
    </div>
    <input id="setsearch" type="search" placeholder="Search sets and questions — try &quot;""",
    "Level filter chips added to the practice screen")

sub("#setsearch{width:100%",
    """.lvlbar{display:flex;gap:8px;flex-wrap:wrap;margin:0 0 12px}
.lvlchip{font:600 13px/1 var(--ui);padding:8px 14px;border-radius:999px;border:1.5px solid var(--line);
  background:var(--card);color:var(--muted);cursor:pointer}
.lvlchip.on{background:var(--ink);color:var(--card);border-color:var(--ink)}
#setsearch{width:100%""",
    "Level chip styling")

sub("""function renderSecs(){
  const tq=BANK.reduce((a,s)=>a+s.questions.length,0);""",
    """let LVLFILTER='all';
function renderSecs(){
  const tq=BANK.reduce((a,s)=>a+s.questions.length,0);""",
    "LVLFILTER state")

sub("  const mine=BANK.filter(forMe), rest=BANK.filter(s=>!forMe(s));\n  let html='';",
    """  const lvlOk = s => LVLFILTER==='all' || s.level===LVLFILTER;
  const mine=BANK.filter(s=>forMe(s)&&lvlOk(s)), rest=BANK.filter(s=>!forMe(s)&&lvlOk(s));
  let html='';
  if(LVLFILTER!=='all' && !mine.length && !rest.length)
    html+=`<div class="grouphead"><h2>Nothing at ${LVLFILTER}</h2><p>Try another level.</p></div>`;""",
    "renderSecs honours the level filter")

sub("document.getElementById('setsearch').addEventListener('input',e=>renderSearch(e.target.value))",
    """document.getElementById('setsearch').addEventListener('input',e=>renderSearch(e.target.value));
document.getElementById('lvlbar').addEventListener('click',e=>{
  const b=e.target.closest('[data-lvl]'); if(!b) return;
  LVLFILTER=b.dataset.lvl;
  document.querySelectorAll('.lvlchip').forEach(c=>c.classList.toggle('on',c===b));
  const box=document.getElementById('setsearch');
  if(box.value.trim().length>1) renderSearch(box.value); else renderSecs();
})""",
    "Level filter wired up")

# ── 3 ── the search ignored the level filter, so filtering then searching lost the filter
sub("""  return BANK.filter(s=>{
    if((s.title+' '+s.letter+' '+s.group).toLowerCase().includes(t)) return true;""",
    """  return BANK.filter(s=>{
    if(LVLFILTER!=='all' && s.level!==LVLFILTER) return false;
    if((s.title+' '+s.letter+' '+s.group).toLowerCase().includes(t)) return true;""",
    "Search respects the level filter")

# ── 4 ── group notes were written before listening papers 4, the papers and the oral sets grew
sub("""  'Visual text & listening':'Posters, notices and charts, plus three listening papers an adult reads aloud.',
  'Writing':"Situational writing tasks with full model answers and the examiner's bands.",
  'Oral':'Paper 4 conversation practice. Say your answer out loud first, then type it and compare.'""",
    """  'Visual text & listening':'Posters, notices, timetables and charts, plus four listening papers an adult reads aloud to you.',
  'Writing':"Picture composition, full compositions, situational writing and planning drills — every one with a model answer and the examiner's bands.",
  'Oral':'Paper 4 practice. Reading aloud with what to listen for, and conversation stimuli. Say your answer out loud first, then type it and compare.'""",
    "Group descriptions brought up to date")

p.write_text(s, encoding="utf-8")
print(f"\n{n[0]} edits applied to build_site2.py")
