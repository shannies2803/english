const PAGE = 'file://' + (process.env.PAGE || new URL('./site/index.html', import.meta.url).pathname);
import { chromium } from 'playwright';
const b = await chromium.launch({ executablePath:'/opt/pw-browsers/chromium-1194/chrome-linux/chrome' });
const p = await b.newPage();
await p.goto(PAGE); await p.waitForTimeout(600);

const res = await p.evaluate(() => {
  const MACHINE=new Set(['auto','edit']);
  const out={variantRejected:{}, nearMiss:[], checkedV:0};
  const VARIANTS = {
    'capitalised':      a => a.charAt(0).toUpperCase()+a.slice(1),
    'trailing full stop': a => a + '.',
    'in quotes':        a => '"'+a+'"',
    'extra spaces':     a => '  '+a+'  ',
    'trailing comma':   a => a + ',',
  };
  for (const s of BANK) for (const q of s.questions) {
    const mode=q.mode||s.mode; if(!MACHINE.has(mode)) continue;
    const acc=q.a||[]; if(!acc.length) continue;
    const key=acc[0];
    for (const [name,fn] of Object.entries(VARIANTS)) {
      out.checkedV++;
      const v=mark(fn(key),acc,q.q);
      if (v!=='right') {
        (out.variantRejected[name]=out.variantRejected[name]||[]).push({set:s.letter,n:q.n,typed:fn(key),v});
      }
    }
    // a DIFFERENT offered word that lands within Levenshtein 1 of the key gets
    // "So close — check the spelling", which is misleading: it is the wrong word.
    const offered = (q.q||'').match(/\(([^()]*\/[^()]*)\)/);
    if (offered) {
      for (const alt of offered[1].split('/').map(x=>x.trim())) {
        if (!alt || acc.some(a=>a.toLowerCase()===alt.toLowerCase())) continue;
        if (mark(alt,acc,q.q)==='close') out.nearMiss.push({set:s.letter,n:q.n,key,alt,q:(q.q||'').slice(0,72)});
      }
    }
  }
  return out;
});
console.log('variant checks run:', res.checkedV);
for (const [k,v] of Object.entries(res.variantRejected))
  console.log(`  rejected "${k}": ${v.length}`, v.slice(0,3).map(x=>`${x.set}#${x.n} ${JSON.stringify(x.typed)}->${x.v}`).join('  '));
if (!Object.keys(res.variantRejected).length) console.log('  all variants accepted');
console.log(`\nwrong-but-similar offered word marked "close" (misleading): ${res.nearMiss.length}`);
res.nearMiss.slice(0,18).forEach(r=>console.log(`   ${r.set}#${r.n}  key=${JSON.stringify(r.key)} alt=${JSON.stringify(r.alt)}  ${r.q}`));
await b.close();
