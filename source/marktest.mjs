const PAGE = 'file://' + (process.env.PAGE || new URL('./site/index.html', import.meta.url).pathname);
import { chromium } from 'playwright';
const b = await chromium.launch({ executablePath:'/opt/pw-browsers/chromium-1194/chrome-linux/chrome' });
const p = await b.newPage();
const errs=[]; p.on('pageerror',e=>errs.push(e.message));
await p.goto(PAGE);
await p.waitForTimeout(600);

const res = await p.evaluate(() => {
  // Run every keyed answer of every machine-marked question through the app's own marker.
  const out = { checked:0, notRight:[], byMode:{}, close:[], blankKey:[] };
  const MACHINE = new Set(['auto','edit','mcq']);
  for (const s of BANK) {
    for (const q of s.questions) {
      const mode = q.mode || s.mode;
      if (!MACHINE.has(mode)) continue;
      const accepted = q.a || [];
      if (mode === 'mcq') {
        // the option the app will mark right must equal the model answer
        if (q.options && typeof q.correct === 'number') {
          out.checked++;
          if ((q.options[q.correct]||'') !== (q.m||'')) {
            out.notRight.push({set:s.letter, n:q.n, mode, why:'option['+q.correct+'] != model',
                               opt:q.options[q.correct], model:q.m});
          }
        }
        continue;
      }
      if (!accepted.length || !accepted.some(x=>(x||'').trim())) {
        out.blankKey.push({set:s.letter, n:q.n, mode}); continue;
      }
      // every accepted answer must itself be marked 'right'
      for (const a of accepted) {
        out.checked++;
        const v = mark(a, accepted);
        if (v !== 'right') {
          (v==='close' ? out.close : out.notRight).push(
            {set:s.letter, n:q.n, mode, typed:a, verdict:v, accepted});
        }
      }
      out.byMode[mode] = (out.byMode[mode]||0)+1;
    }
  }
  return out;
});
console.log('keyed answers run through mark():', res.checked);
console.log('by mode:', JSON.stringify(res.byMode));
console.log('\nkeyed answer NOT accepted by its own marker:', res.notRight.length);
res.notRight.slice(0,20).forEach(r=>console.log('   ', JSON.stringify(r).slice(0,190)));
console.log('\nkeyed answer marked only "close":', res.close.length);
res.close.slice(0,10).forEach(r=>console.log('   ', JSON.stringify(r).slice(0,170)));
console.log('\nmachine-marked question with a blank key:', res.blankKey.length, res.blankKey.slice(0,8));
console.log('ERRORS:', errs.length?errs:'none');
await b.close();
