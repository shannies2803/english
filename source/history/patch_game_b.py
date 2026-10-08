#!/usr/bin/env python3
"""Game layer part 2: XP engine, combo, badges, quests, level-up."""
import pathlib, sys

p = pathlib.Path(__file__).parent / "build_site2.py"
s = p.read_text(encoding="utf-8")
before = len(s)

def sub(old, new, label):
    global s
    if old not in s:
        sys.exit(f"PATCH FAILED — anchor not found: {label}")
    s = s.replace(old, new, 1)

ENGINE = r"""
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
  const before=rankOf(p.xp).i;
  p.xp+=xp;
  const after=rankOf(p.xp);
  if(after.i>before) setTimeout(()=>levelUp(after),450);
}
function levelUp(r){
  if(!P().game) return;
  const w=document.createElement('div'); w.className='lvlup';
  w.innerHTML=`<div class="card"><div class="rankbadge">${r.tag}</div>
    <h2 style="margin:0 0 6px;font-size:23px">Rank up</h2>
    <p style="margin:0 0 20px;color:var(--muted)">You are now <strong style="color:var(--ink)">${esc(r.name)}</strong>.</p>
    <button class="btn" id="lvlok">Keep going</button></div>`;
  document.body.appendChild(w);
  w.querySelector('#lvlok').onclick=()=>w.remove();
  w.onclick=e=>{ if(e.target===w) w.remove(); };
}
function grant(id){
  const p=P();
  if(p.badges.includes(id)) return false;
  p.badges.push(id); save();
  const b=BADGES.find(x=>x.id===id); if(!b||!p.game) return true;
  const w=document.createElement('div'); w.className='lvlup';
  w.innerHTML=`<div class="card"><div style="font-size:52px;line-height:1">${b.ic}</div>
    <div class="ranksub" style="margin-top:10px">Badge unlocked</div>
    <h2 style="margin:4px 0 6px;font-size:22px">${esc(b.name)}</h2>
    <p style="margin:0 0 20px;color:var(--muted)">${esc(b.how)}</p>
    <button class="btn" id="bok">Nice</button></div>`;
  document.body.appendChild(w);
  w.querySelector('#bok').onclick=()=>w.remove();
  w.onclick=e=>{ if(e.target===w) w.remove(); };
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
"""
sub("/* ---------- export / import ---------- */", ENGINE + "\n/* ---------- export / import ---------- */", "engine")

# ---------------------------------------------------------------- hook the marking
sub("""  const p=P(); p.done++; if(good) p.right++; bumpWeek(1);""",
"""  const p=P(); p.done++; if(good) p.right++; bumpWeek(1);
  p.dayCount=(p.dayCount||0)+1;
  if(good){
    COMBO++; p.best_combo=Math.max(p.best_combo||0,COMBO);
    p.dayCombo=Math.max(p.dayCombo||0,COMBO);
    const xp=Math.round((Q.drill?20:10)*comboMult());
    award(xp); floatXP(xp);
  } else { COMBO=0; award(4); }
  showCombo();
  if(!(p.groups||[]).includes(Q.set.group||'') && Q.set.group){ p.groups.push(Q.set.group); }""",
"marking hook")

sub("""  touchStreak(); save();
  document.getElementById('checkBtn').classList.add('hide');
  document.getElementById('nextBtn').classList.remove('hide');""",
"""  touchStreak(); checkBadges(); checkQuests(); save();
  document.getElementById('checkBtn').classList.add('hide');
  document.getElementById('nextBtn').classList.remove('hide');""",
"badge hook")

# count retired mistakes for the Repair Crew badges
sub("""      if(existing.box>=BOXES.length){ p.log=p.log.filter(l=>l.key!==key); Q.retired=(Q.retired||0)+1; }""",
"""      if(existing.box>=BOXES.length){ p.log=p.log.filter(l=>l.key!==key);
        Q.retired=(Q.retired||0)+1; p.retired=(p.retired||0)+1; }""",
"retired counter")

# set results: perfect scores, new-set and accuracy quests, drill badge
sub("""  if(Q.set.id!=='__log__'){
    const prev=p.progress[Q.set.id]||{best:0,tries:0};
    p.progress[Q.set.id]={best:Math.max(prev.best,Q.right/n),tries:prev.tries+1};
  }""",
"""  if(Q.set.id!=='__log__'){
    const prev=p.progress[Q.set.id]||{best:0,tries:0};
    if(!prev.tries) p.dayNew=(p.dayNew||0)+1;
    p.progress[Q.set.id]={best:Math.max(prev.best,Q.right/n),tries:prev.tries+1};
    if(Q.right===n) p.perfect=(p.perfect||0)+1;
    if(Q.right/n>=0.8) p.dayGood=(p.dayGood||0)+1;
    if(Q.drillDone) grant('clock');
    if(['compose'].includes(Q.set.mode)) grant('write');
  }
  COMBO=0; showCombo();""",
"finish hook")

sub("""function finish(){
  clearInterval(Q.drillTick); Q.drill=false;""",
"""function finish(){
  clearInterval(Q.drillTick); if(Q.drill){ Q.drillDone=true; } Q.drill=false;""",
"drill done flag")

# set results: award badges and quests, and record paper milestones
sub("""  save();
  document.getElementById('qbar').style.width='100%';
  document.getElementById('qcount').textContent=`${n} / ${n}`;""",
"""  checkBadges(); checkQuests(); save();
  document.getElementById('qbar').style.width='100%';
  document.getElementById('qcount').textContent=`${n} / ${n}`;""",
"finish badge hook")

# mock-paper scores feed the AL badges
sub("""  p.done+=RV.auto.length; p.right+=RV.auto.filter(r=>r.score).length;
  touchStreak(); save();""",
"""  p.done+=RV.auto.length; p.right+=RV.auto.filter(r=>r.score).length;
  if(pc>=85) grant('al1'); if(pc>=75) grant('al2');
  award(Math.round(got*4)); checkBadges(); checkQuests(); touchStreak(); save();""",
"paper badges")

sub("""  p.papers[pp.id]={best:Math.max(prev.best,got),tries:prev.tries+1};
  touchStreak(); save();
  const weakest""",
"""  p.papers[pp.id]={best:Math.max(prev.best,got),tries:prev.tries+1};
  grant('write'); award(Math.round(got*4)); checkBadges(); touchStreak(); save();
  const weakest""",
"writing paper badges")

# weekly goal weeks + paper badges
sub("""  if(!p.week||p.week.start!==weekStart()) p.week={start:weekStart(),count:0};
  const gpc=Math.min(100,Math.round(p.week.count/p.goal*100));""",
"""  if(!p.week||p.week.start!==weekStart()) p.week={start:weekStart(),count:0};
  if(p.week.count>=p.goal && p.week.hit!==p.week.start){
    p.week.hit=p.week.start; p.goalweeks=(p.goalweeks||0)+1; checkBadges(); save();
  }
  const gpc=Math.min(100,Math.round(p.week.count/p.goal*100));""",
"goal weeks")

p.write_text(s, encoding="utf-8")
print(f"game patch 2 applied ({before} -> {len(s)} bytes)")
