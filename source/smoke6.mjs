const PAGE = 'file://' + (process.env.PAGE || new URL('./site/index.html', import.meta.url).pathname);
import { chromium } from 'playwright';
const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium-1194/chrome-linux/chrome' });
const p = await b.newPage({ viewport: { width: 1000, height: 1100 } });
const errs=[]; p.on('pageerror',e=>errs.push(e.message));
p.on('console',m=>{if(m.type()==='error'&&!/net::ERR/.test(m.text()))errs.push(m.text());});
await p.goto(PAGE);
await p.waitForTimeout(500);
await p.evaluate(()=>document.querySelectorAll('#pick > *')[0].click());
await p.waitForTimeout(300);
for (const idx of [0,1]) {                       // the two new papers
  await p.evaluate(()=>{document.querySelector('[data-view="papers"]').click();});
  await p.waitForTimeout(250);
  const title = await p.evaluate(i=>document.querySelectorAll('#paperGrid [data-paper]')[i].querySelector('h3').textContent.trim(), idx);
  await p.evaluate(i=>document.querySelectorAll('#paperGrid [data-paper]')[i].click(), idx);
  await p.waitForTimeout(600);
  const st = await p.evaluate(()=>{
    const c=document.getElementById('qcard');
    return { qcount: (document.getElementById('qcount')||{}).textContent,
             timer: (document.getElementById('etime')||{}).textContent,
             first: c? c.innerText.slice(0,150).replace(/\n+/g,' | '):'NO CARD',
             hasInput: !!(c && c.querySelector('input,textarea,.opt')) };
  });
  console.log(`\n${title}`);
  console.log(`  q ${st.qcount} · timer ${st.timer} · input ${st.hasInput}`);
  console.log(`  ${st.first}`);
  // step through 12 questions
  const walked = await p.evaluate(async ()=>{
    let ok=0, blank=0;
    for(let i=0;i<12;i++){
      const c=document.getElementById('qcard'); if(!c) break;
      if((c.innerText||'').trim().length<10) blank++;
      const o=[...c.querySelectorAll('.opt')], inp=c.querySelector('input,textarea');
      if(o.length) o[0].click(); else if(inp){inp.value='x';inp.dispatchEvent(new Event('input',{bubbles:true}));}
      await new Promise(r=>setTimeout(r,25));
      const nx=[...document.querySelectorAll('#qcard button, #v-quiz button')].find(x=>/^next/i.test(x.innerText.trim()));
      if(!nx) break; nx.click(); ok++;
      await new Promise(r=>setTimeout(r,35));
    }
    return {advanced:ok, blank, at:(document.getElementById('qcount')||{}).textContent};
  });
  console.log(`  walked ${walked.advanced} questions, ${walked.blank} blank, now at ${walked.at}`);
  await p.evaluate(()=>{const q=document.getElementById('quitBtn'); if(q) q.click();});
  await p.waitForTimeout(250);
  await p.evaluate(()=>{const y=[...document.querySelectorAll('button')].find(x=>/yes|quit|leave/i.test(x.innerText)); if(y)y.click();});
  await p.waitForTimeout(250);
}
console.log('\nERRORS:', errs.length?errs.slice(0,5):'none');
await b.close();
