const PAGE = 'file://' + (process.env.PAGE || new URL('./site/index.html', import.meta.url).pathname);
import { chromium } from 'playwright';
const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium-1194/chrome-linux/chrome' });
const p = await b.newPage({ viewport: { width: 1000, height: 1100 } });
const errs=[]; p.on('pageerror',e=>errs.push(e.message));
p.on('console',m=>{if(m.type()==='error'&&!/net::ERR/.test(m.text()))errs.push(m.text());});
await p.goto(PAGE);
await p.waitForTimeout(500);
await p.evaluate(()=>document.querySelectorAll('#pick > *')[1].click());
await p.waitForTimeout(350);

// text size
const ts = await p.evaluate(async ()=>{
  const before=getComputedStyle(document.body).fontSize;
  const btn=document.getElementById('sizeBtn');
  btn.click(); await new Promise(r=>setTimeout(r,90));   // m -> l
  const mid=getComputedStyle(document.body).fontSize, midLabel=btn.textContent;
  btn.click(); await new Promise(r=>setTimeout(r,90));   // l -> xl
  const after=getComputedStyle(document.body).fontSize;
  const stuck=document.body.dataset.ts, label=btn.textContent;
  btn.click(); await new Promise(r=>setTimeout(r,90));   // back to m
  return {before, mid, midLabel, after, stuck, label, wrapped:document.body.dataset.ts};
});
console.log('text size:', JSON.stringify(ts));

// weak-areas panel with an empty log
console.log('weak panel (no mistakes yet):',
  (await p.evaluate(()=>document.getElementById('weakList').innerText.trim().slice(0,90))));

// generate some real mistakes, then re-check the panel and the grouped log
const made = await p.evaluate(async ()=>{
  const wrongIn = async (setId, n) => {
    document.querySelector('[data-view="practice"]').click();
    await new Promise(r=>setTimeout(r,120));
    document.querySelector(`#secGrid [data-sec="${setId}"]`).click();
    await new Promise(r=>setTimeout(r,200));
    for(let i=0;i<n;i++){
      const card=document.getElementById('qcard'); if(!card) break;
      const opts=[...card.querySelectorAll('.opt')], inp=card.querySelector('input');
      if(opts.length){ const bad=opts.find(o=>!o.classList.contains('sel')); bad.click(); }
      else if(inp){ inp.value='zzzz'; inp.dispatchEvent(new Event('input',{bubbles:true})); }
      await new Promise(r=>setTimeout(r,60));
      const cb=document.getElementById('checkBtn'); if(cb && !cb.classList.contains('hide')) cb.click();
      await new Promise(r=>setTimeout(r,90));
      const nb=document.getElementById('nextBtn'); if(nb && !nb.classList.contains('hide')) nb.click();
      await new Promise(r=>setTimeout(r,60));
    }
    document.getElementById('quitBtn')?.click();
    await new Promise(r=>setTimeout(r,120));
    const y=[...document.querySelectorAll('button')].find(x=>/yes|quit|leave/i.test(x.innerText)); if(y)y.click();
    await new Promise(r=>setTimeout(r,120));
  };
  await wrongIn('vocVA4', 4);
  await wrongIn('vocVA8', 2);
  return (JSON.parse(localStorage.getItem('ew_profiles')||'{}'), true);
});
await p.evaluate(()=>document.querySelector('[data-view="home"]').click());
await p.waitForTimeout(400);
console.log('\nweak panel after mistakes:\n  ' +
  (await p.evaluate(()=>document.getElementById('weakList').innerText.trim().replace(/\n/g,'\n  ').slice(0,400))));
console.log('\nsuggested next:', await p.evaluate(()=>document.getElementById('suggest').innerText.replace(/\n/g,' | ')));
await p.evaluate(()=>document.querySelector('[data-view="log"]').click());
await p.waitForTimeout(400);
console.log('\nmistake log (grouped):\n  ' +
  (await p.evaluate(()=>document.getElementById('logList').innerText.trim().replace(/\n/g,'\n  ').slice(0,420))));
console.log('\njump buttons:', await p.evaluate(()=>document.querySelectorAll('.logjump').length));
console.log('ERRORS:', errs.length?errs.slice(0,4):'none');
await b.close();
