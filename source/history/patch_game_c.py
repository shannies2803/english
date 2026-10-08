#!/usr/bin/env python3
"""Game layer part 3: rank card, quests, badges wall, head-to-head, Boss Battle, toggle."""
import pathlib, sys

p = pathlib.Path(__file__).parent / "build_site2.py"
s = p.read_text(encoding="utf-8")
before = len(s)

def sub(old, new, label):
    global s
    if old not in s:
        sys.exit(f"PATCH FAILED — anchor not found: {label}")
    s = s.replace(old, new, 1)

# ---------------------------------------------------------------- Today screen markup
sub("""        <div class="goalwrap">""",
"""        <div class="rank gamebit" id="rankCard" style="margin-top:18px"></div>
        <div class="xpbar gamebit"><div class="bar-track"><div class="bar-fill" id="xpBar" style="width:0%"></div></div>
          <span class="ranksub" id="xpTxt"></span></div>
        <div class="goalwrap">""", "rank card")

sub("""    <h2 style="font-size:20px;margin:0 0 12px">Recommended for you</h2>""",
"""    <div class="hero gamebit" style="margin-bottom:22px">
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

    <h2 style="font-size:20px;margin:0 0 12px">Recommended for you</h2>""", "quests + boss + versus")

sub("""    <div class="card" style="padding:22px;margin-top:22px">
      <h3 style="margin:0 0 4px;font-size:16px">Move progress between devices</h3>""",
"""    <div class="card gamebit" style="padding:22px;margin-top:22px">
      <h3 style="margin:0 0 4px;font-size:16px">Badges</h3>
      <p style="color:var(--muted);margin:0 0 14px;font-size:14.5px"><span id="badgeCount"></span></p>
      <div class="badges" id="badgeWall"></div>
    </div>

    <div class="card" style="padding:22px;margin-top:22px">
      <h3 style="margin:0 0 4px;font-size:16px">Move progress between devices</h3>""", "badge wall")

sub("""        <button class="btn ghost sm" id="impBtn">Import progress</button>""",
"""        <button class="btn ghost sm" id="impBtn">Import progress</button>
        <button class="btn ghost sm" id="gameBtn">Turn game mode off</button>""", "game toggle")

# ---------------------------------------------------------------- renderers
RENDER = r"""
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
  document.getElementById('badgeWall').innerHTML=BADGES.map(b=>{
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
function renderBoss(){
  const p=P(), pool=bossPool();
  const ready=pool.length>=15;
  document.getElementById('bossCard').innerHTML=`
    <div class="ranksub" style="color:#C9B6E8">Boss battle</div>
    <h3>15 questions from your weak spots</h3>
    <p>Drawn from what you keep getting wrong. Get <strong style="color:#fff">12 or more</strong> to clear it.
       Cleared ${p.bosses||0} time${(p.bosses||0)===1?'':'s'}.</p>
    <button class="btn" id="bossBtn" ${ready?'':'disabled'}>${ready?'Take it on':'Answer a few more sets first'}</button>`;
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
"""
sub("/* ---------- export / import ---------- */", RENDER + "\n/* ---------- export / import ---------- */", "renderers")

# boss result handling
sub("""  const msg = pc>=90?'Excellent. This one is solid.' : pc>=70?'Good — a few to tidy up.' :""",
"""  if(Q.boss){
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
  const msg = pc>=90?'Excellent. This one is solid.' : pc>=70?'Good — a few to tidy up.' :""",
"boss result")

# track weekly XP for the head-to-head
sub("""function bumpWeek(k){ const p=P(); if(!p.week||p.week.start!==weekStart()) p.week={start:weekStart(),count:0};
  p.week.count+=(k||1); }""",
"""function bumpWeek(k){ const p=P(); if(!p.week||p.week.start!==weekStart()) p.week={start:weekStart(),count:0,xp:0};
  p.week.count+=(k||1); }""", "week xp field")

sub("""function award(xp){
  const p=P();
  const before=rankOf(p.xp).i;
  p.xp+=xp;""",
"""function award(xp){
  const p=P();
  if(!p.week||p.week.start!==weekStart()) p.week={start:weekStart(),count:0,xp:0};
  p.week.xp=(p.week.xp||0)+xp;
  const before=rankOf(p.xp).i;
  p.xp+=xp;""", "award weekly xp")

# wire the toggle and call the renderer
sub("""  document.getElementById('homeGrid').innerHTML""",
"""  renderGame();
  document.getElementById('homeGrid').innerHTML""", "render call")

sub("""document.getElementById('expBtn').onclick=()=>{""",
"""document.getElementById('gameBtn').onclick=()=>{
  const p=P(); p.game=p.game===false; save(); renderHome();
};
document.getElementById('expBtn').onclick=()=>{""", "toggle wiring")

# reset the combo when a run starts
sub("""  Q={set,list,i:0,right:0,missed:[]};
  if(opts&&opts.drill){""",
"""  COMBO=0; showCombo();
  Q={set,list,i:0,right:0,missed:[]};
  if(opts&&opts.drill){""", "combo reset")

p.write_text(s, encoding="utf-8")
print(f"game patch 3 applied ({before} -> {len(s)} bytes)")
