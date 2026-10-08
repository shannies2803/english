const PAGE = 'file://' + (process.env.PAGE || new URL('./site/index.html', import.meta.url).pathname);
import { chromium } from 'playwright';
const EXE='/opt/pw-browsers/chromium-1194/chrome-linux/chrome';
const b = await chromium.launch({ executablePath: EXE });
const errs=[];
async function shot(scheme, file){
  const ctx = await b.newContext({ viewport:{width:1000,height:1000}, colorScheme: scheme });
  const p = await ctx.newPage();
  p.on('pageerror',e=>errs.push(scheme+': '+e.message));
  p.on('console',m=>{if(m.type()==='error'&&!/net::ERR/.test(m.text()))errs.push(scheme+': '+m.text());});
  await p.goto(PAGE);
  await p.waitForTimeout(500);
  await p.evaluate(()=>document.querySelectorAll('#pick > *')[1].click());
  await p.waitForTimeout(350);
  const col = await p.evaluate(()=>({
    bg:getComputedStyle(document.body).backgroundColor,
    fg:getComputedStyle(document.body).color,
    card:getComputedStyle(document.querySelector('.card')||document.body).backgroundColor,
    theme:document.documentElement.dataset.theme||'(device)',
  }));
  console.log(`${scheme.padEnd(5)} ${JSON.stringify(col)}`);
  await p.screenshot({path:file});
  await ctx.close();
}
await shot('light','shot_light.png');
await shot('dark','shot_dark.png');

// the toggle, and the listening script reveal
const ctx = await b.newContext({ viewport:{width:1000,height:1000}, colorScheme:'light' });
const p = await ctx.newPage();
p.on('pageerror',e=>errs.push(e.message));
await p.goto(PAGE); await p.waitForTimeout(500);
await p.evaluate(()=>document.querySelectorAll('#pick > *')[1].click()); await p.waitForTimeout(300);
const cycle=[];
for(let i=0;i<4;i++){
  cycle.push(await p.evaluate(()=>({t:document.documentElement.dataset.theme||'auto',
                                    bg:getComputedStyle(document.body).backgroundColor})));
  await p.evaluate(()=>document.getElementById('themeBtn').click());
  await p.waitForTimeout(120);
}
console.log('theme cycle:', JSON.stringify(cycle));

// listening set: answer one, confirm the script appears
const lis = await p.evaluate(async ()=>{
  document.querySelector('[data-view="practice"]').click();
  await new Promise(r=>setTimeout(r,200));
  document.querySelector('#secGrid [data-sec="listen5"]').click();
  await new Promise(r=>setTimeout(r,350));
  const before = !!document.querySelector('#fb .heard');
  document.querySelectorAll('.opt')[0].click();
  await new Promise(r=>setTimeout(r,80));
  document.getElementById('checkBtn').click();
  await new Promise(r=>setTimeout(r,250));
  const d=document.querySelector('#fb .heard');
  if(d) d.open=true;
  await new Promise(r=>setTimeout(r,80));
  return { before, after: !!d, summary: d? d.querySelector('summary').textContent : null,
           text: d? d.querySelector('div').innerText.slice(0,90) : null };
});
console.log('listening script reveal:', JSON.stringify(lis));
await p.screenshot({path:'shot_listen.png'});
console.log('ERRORS:', errs.length?errs.slice(0,5):'none');
await b.close();
