#!/usr/bin/env python3
"""Third v3 patch: mistakes screen (due dates + stars), export/import, printable worksheets."""
import pathlib, sys

p = pathlib.Path(__file__).parent / "build_site2.py"
s = p.read_text(encoding="utf-8")
before = len(s)

def sub(old, new, label):
    global s
    if old not in s:
        sys.exit(f"PATCH FAILED — anchor not found: {label}")
    s = s.replace(old, new, 1)

# ---------------------------------------------------------------- mistakes view markup
sub("""    <h1 class="viewtitle">My mistakes</h1>
    <p class="viewsub">Every question you got wrong, kept in one place. Redo them in a week.</p>
    <div class="btnrow" style="margin:0 0 18px">
      <button class="btn" id="logPractise">Practise these</button>
      <button class="btn ghost" id="logPrint">Print the list</button>
      <button class="btn ghost" id="logClear">Clear all</button>
    </div>
    <div class="card" id="logList"></div>""",
"""    <h1 class="viewtitle">My mistakes</h1>
    <p class="viewsub" id="logSub">Wrong answers come back on a schedule — after 1 day, then 3, 7 and 21. Get one right four times and it retires.</p>
    <div class="btnrow" style="margin:0 0 18px">
      <button class="btn" id="logDue">Review what's due</button>
      <button class="btn ghost" id="logPractise">Practise all of them</button>
      <button class="btn ghost" id="logStars">Starred questions</button>
      <button class="btn ghost" id="logPrint">Print the list</button>
      <button class="btn ghost" id="logClear">Clear all</button>
    </div>
    <div class="card" id="logList"></div>""", "mistakes markup")

# ---------------------------------------------------------------- mistakes render
sub("""function renderLog(){
  const p=P(), el=document.getElementById('logList');
  document.getElementById('logPractise').disabled=!p.log.length;
  if(!p.log.length){
    el.innerHTML=`<div class="empty"><h3>Nothing here yet.</h3><p>Questions you get wrong are collected here automatically.</p></div>`;
    return;
  }
  el.innerHTML=p.log.map(l=>`<div class="logitem">
    <div class="meta">${esc(l.title)} · ${l.date}</div>""",
"""function renderLog(){
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
  const sorted=[...p.log].sort((a,b)=>(a.due||'').localeCompare(b.due||''));
  el.innerHTML=sorted.map(l=>`<div class="logitem">
    <div class="meta">${esc(l.title)} · ${l.date}
      ${(!l.due||l.due<=t)?'<span class="duepill">DUE NOW</span>'
        :`<span class="duepill zero">back on ${l.due}</span>`}
      <span style="color:var(--muted)"> · review ${(l.box||0)+1} of 4</span></div>""", "mistakes render")

sub("""document.getElementById('logPractise').onclick=()=>startQuiz('__log__');""",
"""document.getElementById('logPractise').onclick=()=>startQuiz('__log__');
document.getElementById('logDue').onclick=()=>startQuiz('__due__');
document.getElementById('logStars').onclick=()=>startQuiz('__stars__');""", "mistakes wiring")

# ---------------------------------------------------------------- export / import + worksheet, in the Today card
sub("""      <div class="card" style="padding:24px">
        <h3 style="margin:0 0 4px;font-size:17px">Overall progress</h3>""",
"""      <div class="card" style="padding:24px">
        <h3 style="margin:0 0 4px;font-size:17px">Overall progress</h3>""", "noop anchor")

sub("""    <h2 style="font-size:20px;margin:0 0 12px">Recommended for you</h2>
    <div class="grid" id="homeGrid"></div>""",
"""    <h2 style="font-size:20px;margin:0 0 12px">Recommended for you</h2>
    <div class="grid" id="homeGrid"></div>
    <div class="card" style="padding:22px;margin-top:22px">
      <h3 style="margin:0 0 4px;font-size:16px">Move progress between devices</h3>
      <p style="color:var(--muted);margin:0 0 14px;font-size:14.5px">Progress is stored in this browser only. Export a backup file here and import it on another device — it merges both learners' records rather than overwriting them.</p>
      <div class="btnrow" style="margin:0">
        <button class="btn ghost sm" id="expBtn">Export progress</button>
        <button class="btn ghost sm" id="impBtn">Import progress</button>
        <input type="file" id="impFile" accept="application/json" style="display:none">
      </div>
    </div>""", "export markup")

sub("""/* ---------- error log ---------- */""",
"""/* ---------- export / import ---------- */
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
        cur.done=Math.max(cur.done||0,ip.done||0);
        cur.right=Math.max(cur.right||0,ip.right||0);
        cur.streak=Math.max(cur.streak||0,ip.streak||0);
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
      alert('Progress merged. Nothing was overwritten.');
    }catch(err){ alert('That file could not be read. It should be a file exported from this app.'); }
  };
  r.readAsText(f);
};

/* ---------- printable worksheets ---------- */
function printWorksheet(setId){
  const s=BANK.find(x=>x.id===setId); if(!s) return;
  const host=document.getElementById('wsHost');
  const line='<span class="wsline"></span>';
  const body=s.questions.map(q=>{
    if(s.mode==='mcq') return `<li>${showBlanks(q.q,q.blank)}<br>${q.options.map((o,i)=>`(${i+1}) ${esc(o)}`).join(' &nbsp; ')}</li>`;
    if(s.mode==='mcq') return '';
    return `<li>${showBlanks(q.q,q.blank)} ${line}</li>`;
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

/* ---------- error log ---------- */""", "export + worksheet")

# worksheet host element
sub("""  <!-- LIBRARY -->""",
"""  <div class="worksheet" id="wsHost"></div>

  <!-- LIBRARY -->""", "worksheet host")

# a print button on every set card's results screen
sub("""      <button class="btn ghost" id="doneBtn">Back to practice</button>""",
"""      ${Q.set.id.indexOf('__')!==0?`<button class="btn ghost" id="wsBtn">Print this set as a worksheet</button>`:''}
      <button class="btn ghost" id="doneBtn">Back to practice</button>""", "worksheet button")

sub("""  document.getElementById('doneBtn').onclick=()=>go(Q.set.id==='__log__'?'log':'practice');""",
"""  const wb=document.getElementById('wsBtn');
  if(wb) wb.onclick=()=>printWorksheet(Q.set.id);
  document.getElementById('doneBtn').onclick=()=>go(Q.set.id==='__log__'?'log':'practice');""", "worksheet wiring")

# search wiring + migrate on boot
sub("""function boot(){ renderHome(); renderSecs(); showDocInit(); go('home'); }""",
"""document.getElementById('setsearch').addEventListener('input',e=>renderSearch(e.target.value));
function boot(){ S.profiles.forEach(migrate); renderHome(); renderSecs(); showDocInit(); go('home'); }""",
"search + migrate wiring")

p.write_text(s, encoding="utf-8")
print(f"patch 3 applied ({before} -> {len(s)} bytes)")
