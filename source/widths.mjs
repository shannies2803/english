const PAGE = 'file://' + (process.env.PAGE || new URL('./site/index.html', import.meta.url).pathname);
import { chromium } from 'playwright';
const b = await chromium.launch({ executablePath:'/opt/pw-browsers/chromium-1194/chrome-linux/chrome' });
for (const w of [1280, 1000, 820, 600, 390]) {
  const ctx = await b.newContext({viewport:{width:w,height:820}});
  const p = await ctx.newPage();
  await p.goto(PAGE); await p.waitForTimeout(420);
  await p.evaluate(()=>document.querySelectorAll('#pick > *')[1].click()); await p.waitForTimeout(300);
  const r = await p.evaluate(()=>{
    const bar=document.getElementById('topbar');
    const tabs=[...document.querySelectorAll('.tab')];
    const who=document.querySelector('.who');
    const overlap = tabs.some(t=>{ const a=t.getBoundingClientRect(), c=who.getBoundingClientRect();
      return a.right>c.left+1 && a.bottom>c.top+1 && a.top<c.bottom-1; });
    return { barH: Math.round(bar.getBoundingClientRect().height),
             overflowX: document.documentElement.scrollWidth>document.documentElement.clientWidth,
             tabsVisible: tabs.filter(t=>getComputedStyle(t).display!=='none').length,
             tsVisible: getComputedStyle(document.querySelector('.tsbar')).display!=='none',
             overlap };
  });
  console.log(`${String(w).padStart(5)}px  bar ${String(r.barH).padStart(3)}px  tabs ${r.tabsVisible}  sizeBtns ${r.tsVisible}  overlap ${r.overlap}  h-scroll ${r.overflowX}`);
  if (w===390||w===1000) await p.screenshot({path:`shot_w${w}.png`, clip:{x:0,y:0,width:w,height:120}});
  await ctx.close();
}
await b.close();
