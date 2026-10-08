const PAGE = 'file://' + (process.env.PAGE || new URL('./site/index.html', import.meta.url).pathname);
import { chromium } from 'playwright';
const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium-1194/chrome-linux/chrome' });
const errs = [];
async function run(profileIdx, label) {
  const p = await b.newPage({ viewport: { width: 1000, height: 1000 } });
  p.on('pageerror', e => errs.push(`${label} pageerror: ` + e.message));
  p.on('console', m => { if (m.type()==='error' && !/net::ERR/.test(m.text())) errs.push(`${label} console: `+m.text()); });
  await p.goto(PAGE);
  await p.waitForTimeout(500);
  await p.evaluate(i => document.querySelectorAll('#pick > *')[i].click(), profileIdx);
  await p.waitForTimeout(350);
  await p.evaluate(() => document.querySelector('[data-view="practice"]').click());
  await p.waitForTimeout(300);
  const all = await p.evaluate(() => document.querySelectorAll('#secGrid [data-sec]').length);
  const byLvl = {};
  for (const L of ['P3','P4','P5','P6']) {
    await p.evaluate(l => document.querySelector(`.lvlchip[data-lvl="${l}"]`).click(), L);
    await p.waitForTimeout(160);
    byLvl[L] = await p.evaluate(() => document.querySelectorAll('#secGrid [data-sec]').length);
  }
  // filter + search together
  await p.evaluate(() => document.querySelector('.lvlchip[data-lvl="P3"]').click());
  await p.waitForTimeout(120);
  const combo = await p.evaluate(async () => {
    const box = document.getElementById('setsearch');
    box.value = 'vocabulary'; box.dispatchEvent(new Event('input', { bubbles: true }));
    await new Promise(r => setTimeout(r, 200));
    const cards = [...document.querySelectorAll('#secGrid [data-sec]')];
    return { n: cards.length, allP3: cards.every(c => (c.innerText.match(/P3–P4/))) };
  });
  await p.evaluate(() => { const b=document.getElementById('setsearch'); b.value=''; b.dispatchEvent(new Event('input',{bubbles:true}));
                           document.querySelector('.lvlchip[data-lvl="all"]').click(); });
  await p.waitForTimeout(150);
  await p.evaluate(() => document.querySelector('[data-view="papers"]').click());
  await p.waitForTimeout(350);
  const papers = await p.evaluate(() => ({
    heads: [...document.querySelectorAll('#paperGrid .grouphead h2')].map(e=>e.textContent.trim()),
    cards: [...document.querySelectorAll('#paperGrid [data-paper]')].map(e=>e.querySelector('h3').textContent.trim().slice(0,44)),
  }));
  console.log(`\n== ${label} ==`);
  console.log(`  practice: ${all} sets visible · by level ${JSON.stringify(byLvl)}`);
  console.log(`  filter+search: ${combo.n} hits, all at this level: ${combo.allP3}`);
  console.log(`  papers: ${JSON.stringify(papers.heads)}`);
  papers.cards.forEach(c => console.log('     ', c));
  await p.close();
}
await run(0, 'Younger (P3–P4)');
await run(1, 'Older (P5–P6)');
console.log('\nJS ERRORS:', errs.length ? errs : 'none');
await b.close();
