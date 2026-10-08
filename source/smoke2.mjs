const PAGE = 'file://' + (process.env.PAGE || new URL('./site/index.html', import.meta.url).pathname);
import { chromium } from 'playwright';
const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium-1194/chrome-linux/chrome' });
const p = await b.newPage({ viewport: { width: 900, height: 1100 } });
const errs = [];
p.on('pageerror', e => errs.push('pageerror: ' + e.message));
p.on('console', m => { if (m.type()==='error' && !/net::ERR/.test(m.text())) errs.push('console: '+m.text()); });
await p.goto(PAGE);
await p.waitForTimeout(500);
await p.evaluate(() => document.querySelectorAll('#pick > *')[1].click());
await p.waitForTimeout(300);
const openSet = async id => {
  await p.evaluate(() => document.querySelector('[data-view="practice"]').click());
  await p.waitForTimeout(200);
  await p.evaluate(i => document.querySelector(`#secGrid [data-sec="${i}"]`).click(), id);
  await p.waitForTimeout(350);
};

// 1 — MCQ marking: right answer then wrong answer
await openSet('v7VA11');
const r1 = await p.evaluate(async () => {
  const q = window.__q || null;
  const btns = [...document.querySelectorAll('#qcard .opt')];
  const texts = btns.map(x => x.innerText.trim().split('\n').pop());
  const right = texts.findIndex(t => t === 'log');
  btns[right].click();
  await new Promise(r => setTimeout(r, 400));
  return { clicked: 'log', after: document.getElementById('qcard').innerText.slice(0, 260) };
});
console.log('--- MCQ correct ---'); console.log(r1.after.replace(/\n+/g, ' | ').slice(0, 240));

const r2 = await p.evaluate(async () => {
  const nb = [...document.querySelectorAll('#qcard button')].find(x => /next/i.test(x.innerText));
  if (nb) nb.click();
  await new Promise(r => setTimeout(r, 350));
  const btns = [...document.querySelectorAll('#qcard .opt')];
  btns[0].click();
  await new Promise(r => setTimeout(r, 400));
  return document.getElementById('qcard').innerText.slice(0, 300);
});
console.log('--- MCQ second answer ---'); console.log(r2.replace(/\n+/g, ' | ').slice(0, 260));

// 2 — typed answer marking on a new auto set
await openSet('g7GA16');
const r3 = await p.evaluate(async () => {
  const inp = document.querySelector('#qcard input');
  inp.value = 'singing';
  inp.dispatchEvent(new Event('input', { bubbles: true }));
  const chk = [...document.querySelectorAll('#qcard button')].find(x => /check/i.test(x.innerText));
  chk.click();
  await new Promise(r => setTimeout(r, 400));
  return document.getElementById('qcard').innerText.slice(0, 300);
});
console.log('--- typed answer (correct: singing) ---'); console.log(r3.replace(/\n+/g, ' | ').slice(0, 250));

// 3 — new picture composition renders its four SVG panels
await openSet('compP3b');
const r4 = await p.evaluate(() => ({
  svgs: document.querySelectorAll('#qcard svg').length,
  captions: [...document.querySelectorAll('#qcard figcaption, #qcard .cap, #qcard .piccap')].map(e => e.innerText.trim()).slice(0, 4),
  text: document.getElementById('qcard').innerText.slice(0, 200),
}));
console.log('--- P3 composition set CJ2 ---', JSON.stringify(r4).slice(0, 420));
await p.screenshot({ path: 'shot_compP3b.png', fullPage: false });

// 4 — new visual text renders its table/chart
await openSet('vtI');
const r5 = await p.evaluate(() => ({
  svgs: document.querySelectorAll('#qcard svg, .visual svg').length,
  tables: document.querySelectorAll('#qcard table, .visual table').length,
  chars: document.getElementById('qcard').innerText.length,
}));
console.log('--- visual text vtI ---', JSON.stringify(r5));
await p.screenshot({ path: 'shot_vtI.png' });

// 5 — new cloze set shows the whole passage
await openSet('v7VA17');
const r6 = await p.evaluate(() => document.getElementById('qcard').innerText.slice(0, 340));
console.log('--- vocab cloze VA17 ---'); console.log(r6.replace(/\n+/g, ' | ').slice(0, 300));

// 6 — new oral stimulus renders its card
await openSet('sbcI');
const r7 = await p.evaluate(() => ({
  svgs: document.querySelectorAll('#qcard svg').length,
  chars: document.getElementById('qcard').innerText.length,
}));
console.log('--- oral sbcI ---', JSON.stringify(r7));
await p.screenshot({ path: 'shot_sbcI.png' });

// 7 — situational writing set 2 shows task, bands and model on reveal
await openSet('sitw2');
const r8 = await p.evaluate(async () => {
  const before = document.getElementById('qcard').innerText.length;
  const rv = [...document.querySelectorAll('#qcard button')].find(x => /model|show|reveal/i.test(x.innerText));
  if (rv) rv.click();
  await new Promise(r => setTimeout(r, 350));
  return { before, after: document.getElementById('qcard').innerText.length,
           btn: rv ? rv.innerText.trim() : null };
});
console.log('--- situational SW2 ---', JSON.stringify(r8));

console.log('ERRORS:', errs.length ? errs : 'none');
await b.close();
