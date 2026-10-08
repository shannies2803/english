#!/usr/bin/env python3
"""Improvements from the ninth audit round."""
import pathlib, sys
p = pathlib.Path("build_site2.py"); s = p.read_text(encoding="utf-8")
c = [0]
def sub(old, new, label):
    """Idempotent: if the replacement is already in place, count it and move on."""
    global s
    if s.count(old) == 1:
        s = s.replace(old, new); c[0] += 1; print(f"  {c[0]}. {label}")
    elif new in s:
        c[0] += 1; print(f"  {c[0]}. {label} (already applied)")
    else:
        sys.exit(f"anchor {s.count(old)}x and replacement absent: {label}")

# ── A ── a real diagnosis instead of "the first set you haven't finished"
sub("""  const next = mine.find(s=>pct(s)<90) || mine[0];
  document.getElementById('suggest').innerHTML =
    `<p style="font-family:var(--mono);font-size:10.5px;letter-spacing:.1em;text-transform:uppercase;color:var(--muted);margin:0 0 6px">Suggested next</p>
     <strong style="font-family:var(--sans);font-size:16px">Set ${next.letter} · ${esc(next.title)}</strong>`;""",
"""  const diag = diagnose();
  const next = diag.length ? BANK.find(x=>x.id===diag[0].id) : (mine.find(s=>pct(s)<90) || mine[0]);
  document.getElementById('suggest').innerHTML =
    `<p style="font-family:var(--mono);font-size:10.5px;letter-spacing:.1em;text-transform:uppercase;color:var(--muted);margin:0 0 6px">Suggested next</p>
     <strong style="font-family:var(--sans);font-size:16px">Set ${next.letter} · ${esc(next.title)}</strong>
     ${diag.length?`<p style="color:var(--muted);margin:6px 0 0;font-size:14px">${esc(diag[0].why)}</p>`:''}`;
  renderWeak(diag);""",
    "Suggested next now comes from the diagnosis")

sub("function renderHome(){",
"""// Which topics is this child actually getting wrong? Ranked by how many mistakes are
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
function renderHome(){""",
    "diagnose() and the weak-areas panel")

sub("""        <div id="suggest" style="margin-top:20px"></div>""",
"""        <div id="suggest" style="margin-top:20px"></div>
        <div style="margin-top:22px;padding-top:18px;border-top:1px solid var(--line)">
          <p style="font-family:var(--mono);font-size:10.5px;letter-spacing:.1em;text-transform:uppercase;color:var(--muted);margin:0 0 8px">What to work on</p>
          <div id="weakList"></div>
        </div>""",
    "Weak-areas panel added to the Today screen")

sub(".lvlbar{display:flex;gap:8px;flex-wrap:wrap;margin:0 0 12px}",
""".weakrow{display:flex;gap:12px;align-items:flex-start;width:100%;text-align:left;background:none;
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
.tsbar{display:flex;gap:6px;align-items:center;margin-left:auto}
.tsbtn{width:30px;height:30px;border-radius:8px;border:1.5px solid var(--line);background:var(--card);
  color:var(--muted);cursor:pointer;font:700 13px/1 var(--sans)}
.tsbtn.on{background:var(--ink);color:var(--card);border-color:var(--ink)}
body[data-ts="l"]{font-size:17.5px}
body[data-ts="xl"]{font-size:19.5px}
.lvlbar{display:flex;gap:8px;flex-wrap:wrap;margin:0 0 12px}""",
    "styles for the weak list, log grouping and text size")

# ── B ── the mistake log grouped by set, with a way back to that set
sub("""  const sorted=[...p.log].sort((a,b)=>(a.due||'').localeCompare(b.due||''));
  el.innerHTML=sorted.map(l=>`<div class="logitem">""",
"""  const groups={};
  for(const l of p.log){ (groups[l.title]=groups[l.title]||[]).push(l); }
  const order=Object.entries(groups).sort((a,b)=>b[1].length-a[1].length);
  el.innerHTML = order.map(([title,items])=>{
    const set=BANK.find(x=>x.title===title);
    const dueHere=items.filter(l=>!l.due||l.due<=t).length;
    const head=`<div class="logset">${esc(title)}
      <span class="cnt">${items.length} mistake${items.length===1?'':'s'}${dueHere?` · ${dueHere} due`:''}</span>
      ${set?`<button class="logjump" data-sec="${set.id}">Practise this set</button>`:''}</div>`;
    return head + items.sort((a,b)=>(a.due||'').localeCompare(b.due||'')).map(l=>`<div class="logitem">""",
    "Mistake log grouped by set")

sub("""    ${l.q.tip?`<div class="tip" style="font-size:14.5px">${esc(l.q.tip)}</div>`:''}</div>`).join('');
}""",
"""    ${l.q.tip?`<div class="tip" style="font-size:14.5px">${esc(l.q.tip)}</div>`:''}</div>`).join('');
  }).join('');
}""",
    "Mistake log render closed over the new grouping")

# ── C ── text size, for the younger child and for anyone printing
sub("""  document.getElementById('whoLvl').textContent=LEVELS[p.lvl];""",
"""  document.getElementById('whoLvl').textContent=LEVELS[p.lvl];
  document.body.dataset.ts = p.ts || 'm';
  document.querySelectorAll('.tsbtn').forEach(b=>b.classList.toggle('on', b.dataset.ts===(p.ts||'m')));""",
    "Text size applied from the profile")

sub("""<button id="switchBtn">Switch</button></div>""",
"""<button id="switchBtn">Switch</button>
    <span class="tsbar" title="Text size">
      <button class="tsbtn" data-ts="m">A</button>
      <button class="tsbtn" data-ts="l">A+</button>
      <button class="tsbtn" data-ts="xl">A++</button>
    </span></div>""",
    "Text-size buttons in the top bar")

sub("""document.querySelectorAll('.tab').forEach(t=>t.onclick=()=>go(t.dataset.view));""",
"""document.querySelectorAll('.tab').forEach(t=>t.onclick=()=>go(t.dataset.view));
document.querySelectorAll('.tsbtn').forEach(b=>b.onclick=()=>{
  const p=P(); p.ts=b.dataset.ts; save();
  document.body.dataset.ts=p.ts;
  document.querySelectorAll('.tsbtn').forEach(x=>x.classList.toggle('on',x===b));
});""",
    "Text-size buttons wired and remembered per child")

p.write_text(s, encoding="utf-8")
print(f"\n{c[0]} edits applied")
