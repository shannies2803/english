const PAGE = 'file://' + (process.env.PAGE || new URL('./site/index.html', import.meta.url).pathname);
import { chromium } from 'playwright';
const b = await chromium.launch({ executablePath:'/opt/pw-browsers/chromium-1194/chrome-linux/chrome' });
for (const w of [1280,1100,1000,900,820]) {
  const ctx = await b.newContext({viewport:{width:w,height:700}});
  const p = await ctx.newPage();
  await p.goto(PAGE); await p.waitForTimeout(380);
  await p.evaluate(()=>document.querySelectorAll('#pick > *')[1].click()); await p.waitForTimeout(260);
  const r = await p.evaluate(()=>{
    const nav=document.querySelector('.tabs');
    const clipped=[...nav.querySelectorAll('.tab')].filter(t=>
      t.getBoundingClientRect().right > nav.getBoundingClientRect().right+0.5).map(t=>t.textContent.trim());
    return {clipped, barH:Math.round(document.getElementById('topbar').getBoundingClientRect().height)};
  });
  console.log(`${String(w).padStart(5)}px  bar ${r.barH}px  clipped tabs: ${r.clipped.length?r.clipped.join(', '):'none'}`);
  await ctx.close();
}
await b.close();
