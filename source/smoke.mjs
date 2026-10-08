const PAGE = 'file://' + (process.env.PAGE || new URL('./site/index.html', import.meta.url).pathname);
import { chromium } from 'playwright';
const EXE = '/opt/pw-browsers/chromium-1194/chrome-linux/chrome';
const b = await chromium.launch({ executablePath: EXE });
const p = await b.newPage();
const errs = [];
p.on('pageerror', e => errs.push('pageerror: ' + e.message));
p.on('console', m => {
  if (m.type() === 'error' && !/ERR_TUNNEL_CONNECTION_FAILED|net::ERR/.test(m.text()))
    errs.push('console: ' + m.text());
});
await p.goto(PAGE);
await p.waitForTimeout(600);

// choose the older profile (P5–P6)
await p.evaluate(() => document.querySelectorAll('#pick > *')[1].click());
await p.waitForTimeout(400);
const home = await p.evaluate(() => ({
  sets: document.getElementById('stSecs').textContent,
  rank: document.getElementById('xpTxt')?.textContent.trim().slice(0, 40),
  quests: document.querySelectorAll('#questList > *').length,
  suggest: document.querySelectorAll('#suggest > *').length,
  badges: document.getElementById('badgeCount')?.textContent.trim(),
}));
console.log('HOME', JSON.stringify(home));

await p.evaluate(() => document.querySelector('[data-view="practice"]').click());
await p.waitForTimeout(400);
const grid = await p.evaluate(() => ({
  cards: document.querySelectorAll('#secGrid [data-sec]').length,
  groups: [...document.querySelectorAll('#secGrid h3,#secGrid .gh,#secGrid .grouphead')].map(e => e.textContent.trim()),
}));
console.log('PRACTICE GRID', grid.cards, 'cards ·', JSON.stringify(grid.groups));

// open every set, render its first question
const rep = await p.evaluate(async () => {
  const out = { opened: 0, blank: [], badBold: [], noInput: [], samples: [] };
  const ids = [...document.querySelectorAll('#secGrid [data-sec]')].map(e => e.getAttribute('data-sec'));
  for (const id of ids) {
    document.querySelector(`#secGrid [data-sec="${id}"]`).click();
    await new Promise(r => setTimeout(r, 30));
    const card = document.getElementById('qcard');
    const txt = (card ? card.innerText : '').trim();
    if (!txt || txt.length < 8) out.blank.push(id);
    if (txt.includes('**')) out.badBold.push(id);
    const interactive = card && card.querySelector('input, textarea, .opt, [data-opt], button');
    if (!interactive) out.noInput.push(id);
    if (out.samples.length < 4) out.samples.push(id + ' :: ' + txt.slice(0, 80).replace(/\n/g, ' | '));
    out.opened++;
    document.getElementById('quitBtn').click();
    await new Promise(r => setTimeout(r, 20));
  }
  return out;
});
console.log('OPENED', rep.opened, 'sets');
console.log('  blank:', rep.blank.length ? rep.blank : 'none');
console.log('  literal ** rendered:', rep.badBold.length ? rep.badBold : 'none');
console.log('  no input control:', rep.noInput.length ? rep.noInput : 'none');
rep.samples.forEach(s => console.log('  ', s));

// answer one MCQ correctly and one wrongly, to exercise marking + error log
const mark = await p.evaluate(async () => {
  document.querySelector('#secGrid [data-sec="v7VA11"]').click();
  await new Promise(r => setTimeout(r, 60));
  const opts = [...document.querySelectorAll('#qcard .opt, #qcard [data-opt]')];
  const n = opts.length;
  if (n) opts[0].click();
  await new Promise(r => setTimeout(r, 120));
  return { options: n, feedback: document.getElementById('qcard').innerText.slice(-140) };
});
console.log('MARKING', JSON.stringify(mark).slice(0, 320));

// papers and library still render
await p.evaluate(() => { document.getElementById('quitBtn')?.click(); });
await p.waitForTimeout(150);
for (const v of ['papers', 'library', 'log', 'home']) {
  await p.evaluate(vv => document.querySelector(`[data-view="${vv}"]`).click(), v);
  await p.waitForTimeout(250);
  const len = await p.evaluate(vv => (document.getElementById('v-' + vv)?.innerText || '').trim().length, v);
  console.log(`VIEW ${v}: ${len} chars`);
}
const docs = await p.evaluate(() => document.querySelectorAll('#libnav a, #libnav button, #libnav [data-doc]').length);
console.log('library documents:', docs);

console.log('JS ERRORS:', errs.length ? errs.slice(0, 8) : 'none');
await b.close();
process.exit(errs.length || rep.blank.length || rep.badBold.length ? 1 : 0);
