const PAGE = 'file://' + (process.env.PAGE || new URL('./site/index.html', import.meta.url).pathname);
import { chromium } from 'playwright';
const b = await chromium.launch({ executablePath:'/opt/pw-browsers/chromium-1194/chrome-linux/chrome' });
const p = await b.newPage();
const errs=[]; p.on('pageerror',e=>errs.push(e.message));
await p.goto(PAGE); await p.waitForTimeout(600);

// ---- spaced repetition: does a mistake come back on the right days? ----
const sr = await p.evaluate(() => {
  const out={boxes:typeof BOXES!=='undefined'?BOXES:null, steps:[]};
  const iso = d => new Date(d).toISOString().slice(0,10);
  const day0 = new Date('2026-01-01T00:00:00Z');
  // walk a single item through every box by simulating correct reviews
  let box = 0, due = iso(day0);
  for (let i=0;i<5;i++){
    const gap = (out.boxes||[])[box];
    const next = gap==null ? null : iso(new Date(Date.parse(due)+gap*864e5));
    out.steps.push({review:i+1, box, dueOn:due, gapDays:gap, nextDue:next});
    if (next==null) break;
    box++; due = next;
  }
  return out;
});
console.log('spaced repetition boxes:', JSON.stringify(sr.boxes));
sr.steps.forEach(s=>console.log(`   review ${s.review}: box ${s.box}, gap ${s.gapDays} days -> next ${s.nextDue ?? 'retired'}`));

// ---- export / import round trip ----
const rt = await p.evaluate(async () => {
  document.querySelectorAll('#pick > *')[1].click();
  await new Promise(r=>setTimeout(r,300));
  // make some state worth preserving
  const p0=P(); p0.done=42; p0.right=37; p0.xp=815; p0.streak=5; p0.ts='l'; p0.theme='dark';
  p0.log=[{title:'Synonyms — closest in meaning', q:{n:1,q:'test q',a:['x'],m:'x'}, given:'y',
           date:'2026-09-30', due:'2026-10-01', box:1}];
  p0.badges=['first','streak3','combo10']; p0.best_combo=14; p0.bosses=2;
  p0.progress={vocVA4:{best:0.8,tried:5}};
  save();
  const before=JSON.parse(JSON.stringify(S));
  // export produces a blob; capture what it would write
  const payload = JSON.stringify(S);
  // wipe, then import that payload through the real import path
  localStorage.clear();
  location.reload();
  return {exportedBytes: payload.length, before:{done:before.profiles[1].done, log:before.profiles[1].log.length,
          xp:before.profiles[1].xp, ts:before.profiles[1].ts, theme:before.profiles[1].theme,
          badges:before.profiles[1].badges.length, combo:before.profiles[1].best_combo,
          bosses:before.profiles[1].bosses}, payload};
});
await p.waitForTimeout(700);
const after = await p.evaluate(async (payload) => {
  // feed the exported JSON through the app's own import handler
  const data = JSON.parse(payload);
  const f = new File([payload], 'backup.json', {type:'application/json'});
  const inp = document.getElementById('impFile');
  const dt = new DataTransfer(); dt.items.add(f); inp.files = dt.files;
  inp.dispatchEvent(new Event('change', {bubbles:true}));
  await new Promise(r=>setTimeout(r,500));
  const pr = S.profiles[1];
  return {done:pr.done, log:(pr.log||[]).length, xp:pr.xp, ts:pr.ts, theme:pr.theme,
          badges:(pr.badges||[]).length, combo:pr.best_combo, bosses:pr.bosses,
          progress:Object.keys(pr.progress||{}).length};
}, rt.payload);
console.log('\nexport/import round trip');
console.log('  before:', JSON.stringify(rt.before));
console.log('  after :', JSON.stringify(after));
const keys=['done','log','xp','ts','theme','badges','combo','bosses'];
const lost=keys.filter(k=>String(after[k])!==String(rt.before[k]));
const ok = lost.length===0;
if(!ok) console.log('  LOST OR CHANGED:', lost.map(k=>`${k} ${rt.before[k]} -> ${after[k]}`).join(', '));
console.log('  ' + (ok ? 'state survived the round trip' : 'STATE LOST OR CHANGED'));
console.log('ERRORS:', errs.length?errs.slice(0,4):'none');
await b.close();
