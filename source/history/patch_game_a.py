#!/usr/bin/env python3
"""Game layer: XP and ranks, combo multiplier, badges, daily quests, boss battle, head-to-head."""
import pathlib, sys

p = pathlib.Path(__file__).parent / "build_site2.py"
s = p.read_text(encoding="utf-8")
before = len(s)

def sub(old, new, label):
    global s
    if old not in s:
        sys.exit(f"PATCH FAILED — anchor not found: {label}")
    s = s.replace(old, new, 1)

# ------------------------------------------------------------------ styles
sub(""".star{background:none;""",
"""/* ---------- game layer ---------- */
.xpbar{display:flex;align-items:center;gap:10px;margin-top:16px}
.xpbar .bar-track{flex:1;height:10px}
.xpbar .bar-fill{background:linear-gradient(90deg,var(--accent),var(--gold))}
.rank{display:flex;align-items:center;gap:11px}
.rankbadge{width:44px;height:44px;border-radius:12px;display:grid;place-items:center;flex:none;
  font-family:var(--sans);font-weight:800;font-size:16px;color:#fff;
  background:linear-gradient(140deg,var(--accent-deep),var(--accent));box-shadow:0 2px 8px rgba(0,0,0,.14)}
.rankname{font-family:var(--sans);font-weight:800;font-size:19px;letter-spacing:-.01em;line-height:1.1}
.ranksub{font-family:var(--mono);font-size:10.5px;letter-spacing:.09em;text-transform:uppercase;color:var(--muted)}
.combo{position:fixed;right:22px;bottom:22px;z-index:50;background:var(--ink);color:#fff;
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
.badge.got{border-color:var(--gold);background:#FFFBF0}
.quest{display:flex;align-items:center;gap:11px;padding:11px 0;border-bottom:1px solid var(--line)}
.quest:last-child{border-bottom:0}
.quest .tick{width:24px;height:24px;border-radius:50%;border:2px solid var(--line);flex:none;
  display:grid;place-items:center;font-size:13px;color:#fff}
.quest.done .tick{background:var(--ok);border-color:var(--ok)}
.quest .qt{flex:1;font-family:var(--sans);font-size:14.5px}
.quest.done .qt{color:var(--muted);text-decoration:line-through}
.quest .qx{font-family:var(--mono);font-size:11.5px;color:var(--gold);font-weight:600}
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
.boss .btn:disabled{background:#6A5490;color:#C9B6E8}
.lvlup{position:fixed;inset:0;z-index:90;display:grid;place-items:center;background:rgba(18,26,44,.72);padding:20px}
.lvlup .card{max-width:380px;text-align:center;padding:32px 28px}
.lvlup .rankbadge{width:72px;height:72px;font-size:26px;margin:0 auto 16px}
.star{background:none;""", "styles")

# ------------------------------------------------------------------ profile fields
sub("""function migrate(p){ p.stars=p.stars||[]; p.goal=p.goal||120;""",
"""const RANKS=[
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
  p.quest=p.quest&&p.quest.day===today()?p.quest:null;""", "profile fields")

p.write_text(s, encoding="utf-8")
print(f"game patch 1 applied ({before} -> {len(s)} bytes)")
