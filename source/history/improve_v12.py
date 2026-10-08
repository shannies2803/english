#!/usr/bin/env python3
"""The 'so close' spelling tolerance must not fire on a deliberate distractor."""
import pathlib, sys
p = pathlib.Path("build_site2.py"); s = p.read_text(encoding="utf-8")
c=[0]
def sub(old,new,label):
    global s
    if s.count(old)==1: s=s.replace(old,new); c[0]+=1; print(f"  {c[0]}. {label}")
    elif new in s: c[0]+=1; print(f"  {c[0]}. {label} (already)")
    else: sys.exit(f"anchor {s.count(old)}x: {label}")

sub("""function mark(user,accepted){
  const u=norm(user); if(!u) return 'blank';
  for(const a of accepted) if(u===norm(a)) return 'right';
  for(const a of accepted){ const n=norm(a); if(n.length>4 && lev(u,n)<=1) return 'close'; }
  return 'wrong';
}""",
"""// Words the question itself offers as alternatives, e.g. "(affect / effect)".
// Choosing one of these is the wrong WORD, not a misspelling, so the spelling
// tolerance below must not soften it to "so close".
function offeredAlternatives(qtext){
  const out=[];
  for(const m of (qtext||'').matchAll(/\\(([^()]*\\/[^()]*)\\)/g))
    for(const part of m[1].split('/')) { const t=part.trim(); if(t && t.split(/\\s+/).length<=3) out.push(norm(t)); }
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
}""",
    "mark() no longer calls a deliberate distractor a near-miss")

sub("      const guess=mark(val,q.a);", "      const guess=mark(val,q.a,q.q);", "self/read call site")
sub("    const r=mark(val,q.a);", "    const r=mark(val,q.a,q.q);", "auto/edit call site")
sub("score:mark(given||'',q.a)==='right'?1:0", "score:mark(given||'',q.a,q.q)==='right'?1:0", "paper marking call site")
p.write_text(s, encoding="utf-8")
print(f"\n{c[0]} edits")
