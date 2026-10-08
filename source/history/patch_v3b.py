#!/usr/bin/env python3
"""Second v3 patch: drill timer, compose mode, goal tracker, export/import, worksheets, mistakes UI."""
import pathlib, sys

p = pathlib.Path(__file__).parent / "build_site2.py"
s = p.read_text(encoding="utf-8")
before = len(s)

def sub(old, new, label):
    global s
    if old not in s:
        sys.exit(f"PATCH FAILED — anchor not found: {label}")
    s = s.replace(old, new, 1)

# ---------------------------------------------------------------- compose mode input
sub("""  } else if(mode==='self'||mode==='read'){""",
"""  } else if(mode==='compose'){
    input=`<textarea id="ans" rows="14" placeholder="Write your email or report here…" autocapitalize="sentences"></textarea>
           <div class="wcount" id="wc">0 words</div>`;
  } else if(mode==='self'||mode==='read'){""", "compose input")

sub("""    ${q.blank?`<p class="hintline" style="margin:-8px 0 14px">Fill blank <strong>${q.blank}</strong>.</p>`:''}""",
"""    ${q.blank?`<p class="hintline" style="margin:-8px 0 14px">Fill blank <strong>${q.blank}</strong>.</p>`:''}
    ${q.pac?`<div class="pacbox"><strong>Before you write:</strong> ${esc(q.pac)}</div>`:''}""",
"pac box")

sub("""  const sb=document.getElementById('starBtn');""",
"""  const ta0=document.getElementById('ans');
  if(mode==='compose'&&ta0){
    const cnt=()=>{const w=ta0.value.trim()?ta0.value.trim().split(/\\s+/).length:0;
      document.getElementById('wc').textContent=w+' word'+(w===1?'':'s');};
    ta0.addEventListener('input',cnt); cnt();
  }
  const sb=document.getElementById('starBtn');""", "compose word count")

# ---------------------------------------------------------------- compose marking
sub("""    if(mode==='self'||mode==='read'){""",
"""    if(mode==='compose'){
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
    if(mode==='self'||mode==='read'){""", "compose marking")

# ---------------------------------------------------------------- drill timer
sub("""function startQuiz(id){""",
"""function paintDrill(){
  const el=document.getElementById('qcount'); if(!el||!Q.drill) return;
  const left=Math.max(0,Math.ceil((Q.drillEnds-Date.now())/1000));
  el.innerHTML=`<span class="drilltimer ${left<=15?'low':''}">${left}s</span>
                <span style="margin-left:8px">${Q.i+1}/${Q.list.length}</span>`;
  if(left<=0){ clearInterval(Q.drillTick); Q.drill=false; finish(); }
}
function startQuiz(id, opts){""", "drill paint")

sub("""  Q={set,list,i:0,right:0,missed:[]};
  go('quiz'); renderQ();""",
"""  Q={set,list,i:0,right:0,missed:[]};
  if(opts&&opts.drill){
    Q.drill=true; Q.drillEnds=Date.now()+list.length*15000;
    clearInterval(Q.drillTick); Q.drillTick=setInterval(paintDrill,250);
  }
  go('quiz'); renderQ();""", "drill start")

sub("""function finish(){
  const n=Q.list.length, pc=Math.round(Q.right/n*100), p=P();""",
"""function finish(){
  clearInterval(Q.drillTick); Q.drill=false;
  const n=Q.list.length, pc=Math.round(Q.right/n*100), p=P();""", "drill stop")

# offer the drill on the results screen and add a per-set drill launcher
sub("""      <button class="btn ghost" id="againBtn">Do the whole set again</button>""",
"""      <button class="btn ghost" id="againBtn">Do the whole set again</button>
      ${Q.set.id.indexOf('__')!==0?`<button class="btn ghost" id="drillBtn">Beat the clock (15s a question)</button>`:''}""",
"drill button")

sub("""  document.getElementById('againBtn').onclick=()=>startQuiz(Q.set.id);""",
"""  const db=document.getElementById('drillBtn');
  if(db) db.onclick=()=>startQuiz(Q.set.id,{drill:true});
  document.getElementById('againBtn').onclick=()=>startQuiz(Q.set.id);""", "drill wiring")

# ---------------------------------------------------------------- weekly goal on Today
sub("""        <div class="btnrow">
          <button class="btn" id="goNext">Start today's set</button>""",
"""        <div class="goalwrap">
          <p style="font-family:var(--mono);font-size:10.5px;letter-spacing:.1em;text-transform:uppercase;color:var(--muted);margin:0 0 6px">
            This week <span id="goalTxt"></span></p>
          <div class="bar-track"><div class="bar-fill" id="goalBar" style="width:0%"></div></div>
        </div>
        <div class="btnrow">
          <button class="btn" id="goNext">Start today's set</button>""", "goal markup")

sub("""  document.getElementById('goMistakes').disabled = p.log.length===0;
  document.getElementById('goMistakes').textContent =
    p.log.length? `Practise my mistakes (${p.log.length})` : 'No mistakes saved yet';""",
"""  if(!p.week||p.week.start!==weekStart()) p.week={start:weekStart(),count:0};
  const gpc=Math.min(100,Math.round(p.week.count/p.goal*100));
  document.getElementById('goalBar').style.width=gpc+'%';
  document.getElementById('goalBar').className='bar-fill'+(gpc>=100?' good':'');
  document.getElementById('goalTxt').textContent=`${p.week.count} of ${p.goal} questions`;
  const due=dueCount();
  document.getElementById('goMistakes').disabled = due===0;
  document.getElementById('goMistakes').textContent =
    due ? `Review ${due} due question${due===1?'':'s'}` :
    (p.log.length? 'Nothing due today' : 'No mistakes saved yet');""", "goal render")

sub("""document.getElementById('goMistakes').onclick=()=>startQuiz('__log__');""",
"""document.getElementById('goMistakes').onclick=()=>startQuiz('__due__');""", "due launcher")

p.write_text(s, encoding="utf-8")
print(f"patch 2 applied ({before} -> {len(s)} bytes)")
