// The subject chips on the Practice screen.
//
// Why this exists: the practice grid is 168 sets in one column, about 12,000px tall.
// Finding the oral or composition sets meant scrolling past everything else. The chips
// filter the grid to one subject; this checks they still do, that they combine with the
// level chips, that the counts on them are true, and that the sticky row sits under the
// top bar rather than behind it at every width.
import { chromium } from 'playwright';

const PAGE = 'file://' + (process.env.PAGE || new URL('./site/index.html', import.meta.url).pathname);
const EXE = '/opt/pw-browsers/chromium-1194/chrome-linux/chrome';
const b = await chromium.launch({ executablePath: EXE });
let fail = 0;
const check = (ok, msg) => { if (!ok) { fail++; console.log('FAIL  ' + msg); } else console.log('ok    ' + msg); };

const open = async (w, h, profile) => {
  const p = await b.newPage({ viewport: { width: w, height: h } });
  await p.route('**', r => (r.request().url().startsWith('file:') ? r.continue() : r.abort()));
  p.on('pageerror', e => { fail++; console.log('FAIL  pageerror: ' + e.message); });
  await p.goto(PAGE); await p.waitForTimeout(450);
  await p.evaluate(i => document.querySelectorAll('#pick > *')[i].click(), profile);
  await p.waitForTimeout(250);
  await p.evaluate(() => document.querySelector('[data-view="practice"]').click());
  await p.waitForTimeout(350);
  return p;
};

const pick = async (p, grp) => { await p.evaluate(g => document.querySelector(`#grpbar [data-grp="${g}"]`).click(), grp); await p.waitForTimeout(300); };
const lvl  = async (p, l)   => { await p.evaluate(x => document.querySelector(`#lvlbar [data-lvl="${x}"]`).click(), x => x, l).catch(()=>{}); };

for (const profile of [0, 1]) {
  const p = await open(1100, 900, profile);
  const label = profile === 0 ? 'younger' : 'older';

  // every subject in the bank has a chip, and no chip names a subject that is not there
  const r = await p.evaluate(() => ({
    chips: [...document.querySelectorAll('#grpbar [data-grp]')].map(c => c.dataset.grp),
    groups: [...new Set(BANK.map(s => s.group))],
    total: BANK.length,
  }));
  check(r.chips[0] === 'all', `${label}: first chip shows everything`);
  for (const g of r.groups) check(r.chips.includes(g), `${label}: chip for "${g}"`);
  for (const c of r.chips.slice(1)) check(r.groups.includes(c), `${label}: chip "${c}" matches a real group`);

  // each chip's count is the number of sets it actually shows
  for (const g of r.chips) {
    await pick(p, g);
    const got = await p.evaluate(gg => ({
      shown: document.querySelectorAll('#secGrid [data-sec]').length,
      onChip: Number(document.querySelector(`#grpbar [data-grp="${gg}"] .n`).textContent),
      wrongGroup: [...document.querySelectorAll('#secGrid [data-sec]')]
        .map(e => BANK.find(s => s.id === e.getAttribute('data-sec')))
        .filter(s => gg !== 'all' && s && s.group !== gg).length,
    }), g);
    check(got.shown === got.onChip, `${label}: "${g}" chip says ${got.onChip}, grid shows ${got.shown}`);
    check(got.wrongGroup === 0, `${label}: "${g}" shows nothing from another subject`);
  }

  // the filter must shorten the page, which is the whole point
  await pick(p, 'all');
  const tall = await p.evaluate(() => document.documentElement.scrollHeight);
  await pick(p, 'Writing');
  const short = await p.evaluate(() => document.documentElement.scrollHeight);
  check(short < tall / 3, `${label}: Writing is ${short}px against ${tall}px for everything`);

  // subject and level combine, and an empty combination explains itself
  await p.evaluate(() => document.querySelector('#lvlbar [data-lvl="P3"]').click());
  await p.waitForTimeout(300);
  const combo = await p.evaluate(() => ({
    shown: [...document.querySelectorAll('#secGrid [data-sec]')].map(e => BANK.find(s => s.id === e.getAttribute('data-sec'))),
    chipCounts: [...document.querySelectorAll('#grpbar [data-grp]')].map(c => Number(c.querySelector('.n').textContent)),
    emptyNote: document.querySelector('#secGrid .grouphead p')?.textContent || '',
  }));
  check(combo.shown.every(s => s && s.group === 'Writing' && s.level === 'P3'),
        `${label}: Writing + P3 shows only P3 writing sets`);
  check(combo.shown.length > 0 || /writing/i.test(combo.emptyNote),
        `${label}: an empty combination says which subject and level it meant`);
  check(combo.chipCounts[0] >= Math.max(...combo.chipCounts.slice(1)),
        `${label}: chip counts follow the chosen level`);

  // clearing both brings everything back
  await p.evaluate(() => document.querySelector('#lvlbar [data-lvl="all"]').click());
  await pick(p, 'all');
  const back = await p.evaluate(() => document.querySelectorAll('#secGrid [data-sec]').length);
  check(back === r.total, `${label}: clearing both filters restores all ${r.total} sets`);

  // search still works while a subject is chosen, and respects it
  await pick(p, 'Oral');
  await p.evaluate(() => { const b = document.getElementById('setsearch'); b.value = 'school'; b.dispatchEvent(new Event('input')); });
  await p.waitForTimeout(300);
  const searched = await p.evaluate(() => [...document.querySelectorAll('#secGrid [data-sec]')]
    .map(e => BANK.find(s => s.id === e.getAttribute('data-sec'))).filter(s => s && s.group !== 'Oral').length);
  check(searched === 0, `${label}: searching inside a subject stays inside it`);
  await p.close();
}

// the sticky row must sit under the top bar, not behind it, at every width
for (const w of [390, 600, 768, 950, 1100, 1280]) {
  const p = await open(w, 800, 0);
  await p.evaluate(() => window.scrollTo(0, 2500));
  await p.waitForTimeout(350);
  const r = await p.evaluate(() => {
    const tb = document.getElementById('topbar').getBoundingClientRect();
    const gb = document.getElementById('grpbar').getBoundingClientRect();
    return { overlap: gb.top < tb.bottom - 1, visible: gb.bottom > 0 && gb.top < innerHeight,
             chrome: Math.round(gb.bottom), share: gb.bottom / innerHeight };
  });
  check(!r.overlap, `${w}px: subject row is not hidden behind the top bar`);
  check(r.visible, `${w}px: subject row stays on screen while scrolling`);
  check(r.share < 0.33, `${w}px: fixed chrome is ${r.chrome}px, ${Math.round(r.share*100)}% of the screen`);
  await p.close();
}

await b.close();
console.log(fail ? `\nFAIL: ${fail} problems with the subject filter` : '\nsubject filter: all checks pass');
