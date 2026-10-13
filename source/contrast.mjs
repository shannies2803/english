// Dark-mode contrast sweep.
//
// Why this exists: for several rounds the page looked right in light mode and the
// structural audits were clean, while in dark mode the MCQ options, every
// comprehension passage, every writing task box, the model-answer boxes, the search
// field, document tables and blockquotes were all near-white text on a hard-coded
// near-white background — contrast 1.16, i.e. invisible. Nothing but a measurement
// catches that. This walks the real rendered page in dark mode and fails on any
// visible text below 4.5:1 against the background actually painted behind it.
import { chromium } from 'playwright';

const PAGE = 'file://' + (process.env.PAGE || new URL('./site/index.html', import.meta.url).pathname);
const MIN = 4.5;          // WCAG AA for body text
const MIN_LARGE = 3.0;    // WCAG AA for >=24px, or >=18.66px bold

const EXE = '/opt/pw-browsers/chromium-1194/chrome-linux/chrome';
const b = await chromium.launch({ executablePath: EXE });

// Every surface a child actually reads, in both profiles.
const STOPS = [
  { profile: 0, view: 'practice', set: 'vtZA',   note: 'visual text · MCQ options' },
  { profile: 0, view: 'practice', set: 'cmpZA',  note: 'comprehension passage' },
  { profile: 0, view: 'practice', set: 'compP3', note: 'picture composition · task box + SVG' },
  { profile: 0, view: 'practice', set: 'sitw4',  note: 'P4 situational writing' },
  { profile: 0, view: 'home',     set: null,     note: 'today (younger)' },
  { profile: 1, view: 'practice', set: 'swE',    note: 'situational writing · model + pacbox' },
  { profile: 1, view: 'practice', set: 'compN',  note: 'full composition' },
  { profile: 1, view: 'practice', set: 'readaloud', note: 'reading aloud · criteria bands' },
  { profile: 1, view: 'papers',   set: null,     note: 'mock papers list' },
  { profile: 1, view: 'library',  set: null,     note: 'read & print documents' },
  { profile: 1, view: 'log',      set: null,     note: 'my mistakes' },
  { profile: 1, view: 'home',     set: null,     note: 'today (older)' },
];

const SWEEP = `(() => {
  // getComputedStyle may hand back rgb()/rgba() (0-255) or color(srgb r g b / a) (0-1).
  // Reading the second form as 0-255 made every value ~0 and invented failures, so parse both.
  const parse = c => {
    const srgb = /^color\\(srgb/.test(c);
    const m = (c.match(/[\\d.]+/g) || ['0','0','0']).map(Number);
    const sc = srgb ? 255 : 1;
    return { r: m[0]*sc, g: m[1]*sc, b: m[2]*sc, a: m.length > 3 ? m[3] : 1 };
  };
  const lum = c => {
    const p = parse(c);
    const f = v => { v /= 255; return v <= 0.03928 ? v/12.92 : Math.pow((v+0.055)/1.055, 2.4); };
    return 0.2126*f(p.r) + 0.7152*f(p.g) + 0.0722*f(p.b);
  };
  const alpha = c => parse(c).a;
  const bad = [];
  for (const e of document.querySelectorAll('body *')) {
    // only elements holding their own visible text
    const own = [...e.childNodes].filter(n => n.nodeType === 3 && n.textContent.trim()).map(n => n.textContent.trim()).join(' ');
    if (!own) continue;
    const r = e.getBoundingClientRect();
    if (!r.width || !r.height) continue;
    const s = getComputedStyle(e);
    if (s.visibility === 'hidden' || s.display === 'none' || Number(s.opacity) < 0.15) continue;
    if (s.webkitTextFillColor === 'rgba(0, 0, 0, 0)') continue;
    if (s.filter && s.filter !== 'none' && /blur/.test(s.filter)) continue;   // deliberately masked answers
    if (s.backgroundImage && s.backgroundImage !== 'none') continue;          // gradient/image: no flat colour to measure
    // Climb to whatever is actually painted behind this text. If that turns out to be a
    // gradient (the boss card), there is no single colour to measure and the walk must not
    // sail past it to the page background — that invented four failures.
    let n = e, bg = s.backgroundColor, guard = 0, gradient = false;
    while (alpha(bg) < 0.9 && n.parentElement && guard++ < 40) {
      n = n.parentElement;
      const ns = getComputedStyle(n);
      if (ns.backgroundImage && ns.backgroundImage !== 'none') { gradient = true; break; }
      bg = ns.backgroundColor;
    }
    if (gradient) continue;
    if (alpha(bg) < 0.9) bg = getComputedStyle(document.body).backgroundColor;
    const L1 = lum(s.color), L2 = lum(bg);
    const ratio = (Math.max(L1,L2) + 0.05) / (Math.min(L1,L2) + 0.05);
    const px = parseFloat(s.fontSize);
    const large = px >= 24 || (px >= 18.66 && Number(s.fontWeight) >= 700);
    const floor = large ? ${MIN_LARGE} : ${MIN};
    if (ratio < floor) bad.push({ sel: e.tagName.toLowerCase() + (e.className && typeof e.className === 'string' ? '.' + e.className.trim().split(/\\s+/).join('.') : ''),
                                  text: own.slice(0, 40), color: s.color, bg, ratio: Number(ratio.toFixed(2)), floor });
  }
  // one row per selector is enough
  const seen = new Set();
  return bad.filter(x => { const k = x.sel + x.ratio; if (seen.has(k)) return false; seen.add(k); return true; });
})()`;

let failures = 0;
for (const theme of ['dark', 'light']) {
  const p = await b.newPage({ viewport: { width: 1100, height: 1400 }, colorScheme: theme });
  // The page asks Google Fonts for its typefaces. This container cannot reach them, and
  // waiting for two dozen such requests to time out stretched the sweep past two minutes.
  await p.route('**', r => (r.request().url().startsWith('file:') ? r.continue() : r.abort()));
  await p.goto(PAGE);
  await p.waitForTimeout(500);
  for (const stop of STOPS) {
    await p.evaluate(() => { try { localStorage.clear(); } catch (e) {} });
    await p.goto(PAGE); await p.waitForTimeout(350);
    await p.evaluate(i => document.querySelectorAll('#pick > *')[i].click(), stop.profile);
    await p.waitForTimeout(300);
    const viewOk = await p.evaluate(v => { const el = document.querySelector(`[data-view="${v}"]`); if (el) { el.click(); return true; } return false; }, stop.view);
    if (!viewOk) { failures++; console.log(`FAIL  ${theme} · ${stop.note} — view "${stop.view}" not present`); continue; }
    await p.waitForTimeout(350);
    if (stop.set) {
      const ok = await p.evaluate(id => { const el = document.querySelector(`#secGrid [data-sec="${id}"]`); if (el) { el.click(); return true; } return false; }, stop.set);
      if (!ok) { failures++; console.log(`FAIL  ${theme} · ${stop.note} — set "${stop.set}" not in this profile's grid`); continue; }
      await p.waitForTimeout(500);
      // reveal the model answer / self-mark panel, where several of the bad surfaces live
      await p.evaluate(() => { const b = [...document.querySelectorAll('#qcard button, #qcard .btn')].find(x => /show|reveal|model|check/i.test(x.textContent)); if (b) b.click(); });
      await p.waitForTimeout(400);
    }
    const bad = await p.evaluate(SWEEP);
    if (bad.length) {
      failures += bad.length;
      console.log(`FAIL  ${theme} · ${stop.note} — ${bad.length} low-contrast element(s)`);
      for (const x of bad.slice(0, 6))
        console.log(`        ${x.ratio} (needs ${x.floor})  ${x.sel.slice(0,44)}  "${x.text}"  ${x.color} on ${x.bg}`);
    } else {
      console.log(`pass  ${theme} · ${stop.note}`);
    }
  }
  await p.close();
}
await b.close();
console.log(failures ? `\nFAIL: ${failures} low-contrast elements` : '\ncontrast: all stops pass in both themes');
