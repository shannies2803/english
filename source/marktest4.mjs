const PAGE = 'file://' + (process.env.PAGE || new URL('./site/index.html', import.meta.url).pathname);
import { chromium } from 'playwright';
const b = await chromium.launch({ executablePath:'/opt/pw-browsers/chromium-1194/chrome-linux/chrome' });
const p = await b.newPage();
await p.goto(PAGE); await p.waitForTimeout(600);
const r = await p.evaluate(() => {
  const MACHINE=new Set(['auto','edit']);
  const out={keysOk:0, keysBad:[], softened:[], crossKey:[]};
  for (const s of BANK) for (const q of s.questions) {
    const mode=q.mode||s.mode; if(!MACHINE.has(mode)) continue;
    const acc=q.a||[]; if(!acc.length) continue;
    // 1. every key still marks 'right'
    for (const a of acc) { if (mark(a,acc,q.q)==='right') out.keysOk++; else out.keysBad.push({set:s.letter,n:q.n,a}); }
    // 2. does the wider tolerance now soften an OFFERED distractor to 'close'?
    for (const m of (q.q||'').matchAll(/\(([^()]*\/[^()]*)\)/g))
      for (const part of m[1].split('/')) {
        const t=part.trim(); if(!t || acc.some(a=>a.toLowerCase()===t.toLowerCase())) continue;
        const v=mark(t,acc,q.q);
        if (v!=='wrong') out.softened.push({set:s.letter,n:q.n,key:acc[0],typed:t,v});
      }
  }
  // 3. within a set, does one question's key get accepted for a different question?
  //    (a sign the tolerance is too loose for very short keys)
  for (const s of BANK) {
    if (!MACHINE.has(s.mode)) continue;
    const qs=s.questions.filter(q=>(q.a||[]).length);
    for (let i=0;i<qs.length && out.crossKey.length<8;i++)
      for (let j=0;j<qs.length;j++) {
        if (i===j) continue;
        const other=qs[j].a[0], mine=qs[i].a;
        if (mine.some(a=>a.toLowerCase()===String(other).toLowerCase())) continue;
        if (mark(other,mine,qs[i].q)==='right') { out.crossKey.push({set:s.letter,q:qs[i].n,from:qs[j].n,typed:other}); break; }
      }
  }
  return out;
});
console.log('keys still accepted:', r.keysOk, '· keys now rejected:', r.keysBad.length, r.keysBad.slice(0,5));
console.log('offered distractors NOT marked plainly wrong:', r.softened.length);
r.softened.slice(0,10).forEach(x=>console.log('   ', JSON.stringify(x)));
console.log("another question's key wrongly accepted:", r.crossKey.length, r.crossKey.slice(0,5));
await b.close();
