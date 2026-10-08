const PAGE = 'file://' + (process.env.PAGE || new URL('./site/index.html', import.meta.url).pathname);
import { chromium } from 'playwright';
const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium-1194/chrome-linux/chrome' });
const p = await b.newPage({ viewport: { width: 950, height: 1200 } });
const errs=[]; p.on('pageerror',e=>errs.push(e.message));
await p.goto(PAGE);
await p.waitForTimeout(500);
await p.evaluate(()=>document.querySelectorAll('#pick > *')[1].click());
await p.waitForTimeout(300);
const open = async id => { await p.evaluate(()=>document.querySelector('[data-view="practice"]').click());
  await p.waitForTimeout(180);
  await p.evaluate(i=>document.querySelector(`#secGrid [data-sec="${i}"]`).click(), id);
  await p.waitForTimeout(350); };

for (const id of ['sitw2','compP3b','g7GA19','g7GA20','g7GA22']) {
  await open(id);
  const r = await p.evaluate(async () => {
    const card = document.getElementById('qcard');
    const btns = [...card.querySelectorAll('button')].map(x=>x.innerText.trim().split('\n')[0]).filter(Boolean);
    const ta = card.querySelectorAll('textarea').length;
    const before = card.innerText.length;
    // press whatever the primary action is
    const go = [...card.querySelectorAll('button')].find(x=>/check|mark|compare|done|answer/i.test(x.innerText));
    if (ta) { const t=card.querySelector('textarea'); t.value='My attempt.'; t.dispatchEvent(new Event('input',{bubbles:true})); }
    if (go) go.click();
    await new Promise(r=>setTimeout(r,450));
    const after = document.getElementById('qcard').innerText;
    return { btns, textareas: ta, before, after: after.length,
             revealed: /model|band|examiner|what makes it work|why this/i.test(after),
             tail: after.slice(-220).replace(/\n+/g,' | ') };
  });
  console.log(`\n== ${id} ==  buttons: ${JSON.stringify(r.btns)}  textareas: ${r.textareas}`);
  console.log(`   ${r.before} -> ${r.after} chars · model/bands revealed: ${r.revealed}`);
  console.log('   tail:', r.tail.slice(0,200));
}
await open('sitw2');
await p.evaluate(async()=>{const c=document.getElementById('qcard');
  const t=c.querySelector('textarea'); if(t){t.value='Draft.';t.dispatchEvent(new Event('input',{bubbles:true}));}
  const go=[...c.querySelectorAll('button')].find(x=>/check|mark|compare|done/i.test(x.innerText)); if(go)go.click();
  await new Promise(r=>setTimeout(r,500));});
await p.screenshot({path:'shot_sitw2.png', fullPage:true});
console.log('\nERRORS:', errs.length?errs:'none');
await b.close();
