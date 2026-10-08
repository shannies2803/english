#!/usr/bin/env python3
"""Apply the v3 app improvements to build_site2.py."""
import pathlib, re, sys

p = pathlib.Path(__file__).parent / "build_site2.py"
s = p.read_text(encoding="utf-8")
before = len(s)

def sub(old, new, label):
    global s
    if old not in s:
        sys.exit(f"PATCH FAILED — anchor not found: {label}")
    s = s.replace(old, new, 1)

# ---------------------------------------------------------------- styles
sub(""".pics{display:grid;""",
""".star{background:none;border:0;font-size:19px;line-height:1;padding:4px 6px;color:#C8D0DE;margin-left:auto}
.star.on{color:var(--gold)}
.qlabel{display:flex;align-items:center;gap:8px}
.kbd{font-family:var(--mono);font-size:10.5px;border:1px solid var(--line);border-bottom-width:2px;border-radius:5px;padding:1px 5px;color:var(--muted);background:var(--sheet)}
.drilltimer{font-family:var(--mono);font-size:13px;font-weight:600;background:var(--gold);color:#3A2B00;padding:5px 11px;border-radius:100px}
.drilltimer.low{background:var(--no);color:#fff}
#setsearch{width:100%;max-width:420px;padding:10px 14px;border:1px solid var(--line);border-radius:100px;background:var(--sheet);font-family:var(--sans);font-size:14.5px;margin-bottom:18px}
.duepill{display:inline-block;font-family:var(--mono);font-size:10.5px;letter-spacing:.06em;background:var(--no);color:#fff;padding:2px 8px;border-radius:100px;margin-left:8px}
.duepill.zero{background:var(--ok)}
.goalwrap{margin-top:18px}
.goalwrap .bar-track{height:9px}
.whybox{background:#EEF6F3;border-left:3px solid var(--accent);border-radius:0 8px 8px 0;padding:12px 15px;margin-top:12px;font-size:14.5px}
.pacbox{background:#FFF9E8;border-left:3px solid var(--gold);border-radius:0 8px 8px 0;padding:11px 14px;margin-bottom:14px;font-size:14px}
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
.pics{display:grid;""", "styles")

# ---------------------------------------------------------------- profile shape
sub("""const blank=(name,lvl)=>({name,lvl,progress:{},log:[],streak:0,last:'',done:0,right:0});""",
"""const blank=(name,lvl)=>({name,lvl,progress:{},log:[],stars:[],streak:0,last:'',done:0,right:0,
                          goal:120,week:{start:weekStart(),count:0}});
function weekStart(){ const d=new Date(); const n=(d.getDay()+6)%7; d.setDate(d.getDate()-n);
  return d.toISOString().slice(0,10); }
function bumpWeek(k){ const p=P(); if(!p.week||p.week.start!==weekStart()) p.week={start:weekStart(),count:0};
  p.week.count+=(k||1); }
// spaced repetition: a missed item comes back after 1, 3, 7 then 21 days
const BOXES=[1,3,7,21];
function addDays(n){ const d=new Date(); d.setDate(d.getDate()+n); return d.toISOString().slice(0,10); }
function dueCount(){ const t=today(); return (P().log||[]).filter(l=>!l.due||l.due<=t).length; }
function migrate(p){ p.stars=p.stars||[]; p.goal=p.goal||120;
  p.week=p.week&&p.week.start?p.week:{start:weekStart(),count:0};
  (p.log||[]).forEach(l=>{ if(l.box===undefined){l.box=0;} if(!l.due){l.due=l.date||today();} }); }""",
"profile shape")

sub("""const P=()=>S.profiles[S.cur];""",
"""const P=()=>S.profiles[S.cur];
const starKey=q=>(q._sec||'')+'#'+q.n;
function isStarred(q){ return (P().stars||[]).some(x=>x.key===starKey(q)); }
function toggleStar(q){
  const p=P(), k=starKey(q), i=p.stars.findIndex(x=>x.key===k);
  if(i>=0) p.stars.splice(i,1);
  else p.stars.push({key:k,sec:q._sec,title:q._secTitle,mode:q.mode,options:q.options,correct:q.correct,
                     q:{n:q.n,q:q.q,a:q.a,m:q.m,tip:q.tip,blank:q.blank,marks:q.marks}});
  save(); return i<0;
}""", "star helpers")

# ---------------------------------------------------------------- practice search
sub("""    <div class="grid" id="secGrid"></div>
  </section>

  <!-- QUIZ -->""",
"""    <input id="setsearch" type="search" placeholder="Search sets and questions — try &quot;tenses&quot; or &quot;apostrophe&quot;…" aria-label="Search practice">
    <div class="grid" id="secGrid"></div>
  </section>

  <!-- QUIZ -->""", "search box")

sub("""function renderSecs(){
  const tq=BANK.reduce((a,s)=>a+s.questions.length,0);""",
"""function matchSets(term){
  const t=term.trim().toLowerCase();
  if(t.length<2) return null;
  return BANK.filter(s=>{
    if((s.title+' '+s.letter+' '+s.group).toLowerCase().includes(t)) return true;
    return s.questions.some(q=>((q.q||'')+' '+(q.m||'')).toLowerCase().includes(t));
  });
}
function renderSecs(){
  const tq=BANK.reduce((a,s)=>a+s.questions.length,0);""", "matchSets")

sub("""  document.getElementById('secGrid').innerHTML=html;
}""",
"""  document.getElementById('secGrid').innerHTML=html;
}
function renderSearch(term){
  const hits=matchSets(term);
  if(hits===null){ renderSecs(); return; }
  const el=document.getElementById('secGrid');
  el.innerHTML = hits.length
    ? `<div class="grouphead"><h2>${hits.length} set${hits.length===1?'':'s'} match “${esc(term)}”</h2>
        <p>Clear the box to see everything again.</p></div>` + hits.map(secCard).join('')
    : `<div class="grouphead"><h2>Nothing matches “${esc(term)}”</h2><p>Try a shorter word.</p></div>`;
}""", "renderSearch")

# ---------------------------------------------------------------- star + shortcuts + drill timer in renderQ
sub("""    <div class="qlabel">${esc(label)}${q.marks?`<span class="marks">${q.marks} mark${q.marks>1?'s':''}</span>`:''}</div>""",
"""    <div class="qlabel">${esc(label)}${q.marks?`<span class="marks">${q.marks} mark${q.marks>1?'s':''}</span>`:''}
      <button class="star ${isStarred(q)?'on':''}" id="starBtn" title="Star this question (S)" aria-label="Star this question">${isStarred(q)?'★':'☆'}</button></div>""",
"star button")

sub("""  const stog=document.getElementById('stog');
  if(stog) stog.onclick=""",
"""  const sb=document.getElementById('starBtn');
  if(sb) sb.onclick=()=>{ const on=toggleStar(q); sb.classList.toggle('on',on); sb.textContent=on?'★':'☆'; };
  const stog=document.getElementById('stog');
  if(stog) stog.onclick=""", "star wiring")

sub("""  if(!(Q&&Q.exam)) document.getElementById('checkBtn').onclick=()=>check(q,sel);
  document.getElementById('nextBtn').onclick=()=>{
    Q.i++; if(Q.i>=Q.list.length) finish(); else renderQ();
  };
}""",
"""  if(!(Q&&Q.exam)) document.getElementById('checkBtn').onclick=()=>check(q,sel);
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
});""", "keyboard + option picker")

# ---------------------------------------------------------------- spaced repetition on marking
sub("""  const p=P(); p.done++; if(good) p.right++;
  if(good) Q.right++; else {
    Q.missed.push({q,given});
    const key=(q._sec||'')+'#'+q.n;
    if(!p.log.some(l=>l.key===key))
      p.log.push({key,sec:q._sec,title:q._secTitle,mode:q.mode,options:q.options,correct:q.correct,
                  q:{n:q.n,q:q.q,a:q.a,m:q.m,tip:q.tip},given,date:today()});
  }""",
"""  const p=P(); p.done++; if(good) p.right++; bumpWeek(1);
  const key=(q._sec||'')+'#'+q.n;
  const existing=p.log.find(l=>l.key===key);
  if(good){
    Q.right++;
    if(existing){                       // promote it up the review ladder
      existing.box=Math.min((existing.box||0)+1,BOXES.length);
      if(existing.box>=BOXES.length){ p.log=p.log.filter(l=>l.key!==key); Q.retired=(Q.retired||0)+1; }
      else existing.due=addDays(BOXES[existing.box]);
    }
  } else {
    Q.missed.push({q,given});
    if(existing){ existing.box=0; existing.due=addDays(BOXES[0]); existing.given=given; existing.date=today(); }
    else p.log.push({key,sec:q._sec,title:q._secTitle,mode:q.mode,options:q.options,correct:q.correct,
                     q:{n:q.n,q:q.q,a:q.a,m:q.m,tip:q.tip,blank:q.blank},given,date:today(),
                     box:0,due:addDays(BOXES[0])});
  }""", "spaced repetition")

# the mistakes replay must no longer wipe the whole log
sub("""  } else {
    p.log = p.log.filter(l=>Q.missed.some(m=>(m.q._sec||'')+'#'+m.q.n===l.key));
  }""",
"""  }""", "log replay")

# ---------------------------------------------------------------- mistakes queue honours due dates
sub("""  if(id==='__log__'){
    if(!P().log.length) return;
    list=P().log.map(l=>({...l.q,_sec:l.sec,_secTitle:l.title,mode:l.mode,options:l.options,correct:l.correct,wordbank:l.wordbank}));
    set={id:'__log__',letter:'★',title:'Your saved mistakes',mode:'mixed'};
  } else {""",
"""  if(id==='__log__'||id==='__due__'){
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
  } else {""", "due queue")

p.write_text(s, encoding="utf-8")
print(f"patched build_site2.py  ({before} -> {len(s)} bytes)")
