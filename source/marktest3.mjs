const PAGE = 'file://' + (process.env.PAGE || new URL('./site/index.html', import.meta.url).pathname);
import { chromium } from 'playwright';
const b = await chromium.launch({ executablePath:'/opt/pw-browsers/chromium-1194/chrome-linux/chrome' });
const p = await b.newPage();
await p.goto(PAGE); await p.waitForTimeout(600);
const r = await p.evaluate(() => {
  const cases = [
    // [typed, accepted, question text, expected verdict, note]
    ['affect', ['affect'], 'The rain did not __________ (affect / effect) our plans.', 'right', 'the right word'],
    ['effect', ['affect'], 'The rain did not __________ (affect / effect) our plans.', 'wrong', 'wrong word, not a typo'],
    ['affct',  ['affect'], 'The rain did not __________ (affect / effect) our plans.', 'close', 'a real misspelling still forgiven'],
    ['recieve',['receive'], 'Did you __________ my message?',                          'close', 'classic misspelling forgiven'],
    ['recieved',['receive'],'Did you __________ my message?',                          'wrong', 'two edits away'],
    ['Has',    ['has'],    'The list of names __________ (has / have) been posted.',    'right', 'capitalisation ignored'],
    ['has.',   ['has'],    'The list of names __________ (has / have) been posted.',    'right', 'trailing stop ignored'],
    ['have',   ['has'],    'The list of names __________ (has / have) been posted.',    'wrong', 'the other offered word'],
    ['',       ['has'],    'x __________ (has / have) y',                               'blank', 'empty stays blank'],
    ['were',   ['was','were'], 'There __________ (is / are) a pen and two rulers.',      'right', 'second accepted answer'],
    ['thier',  ['their'],  'They collected __________ bags.',                           'close', 'transposition forgiven'],
    ['freind', ['friend'], 'He is my best __________.',                                 'close', 'transposition forgiven'],
    ['beleive',['believe'],'I __________ she is telling the truth.',                    'close', 'transposition forgiven'],
    ['there',  ['their'],  'They collected __________ bags.',                           'wrong', 'different word, 2 edits'],
    ['quiet',  ['quite'],  'It was __________ difficult.',                              'close', 'transposition, no distractor list'],
    ['were',   ['was'],    'The committee __________ (was / were) meeting.',            'wrong', 'offered distractor stays wrong'],
  ];
  return cases.map(([t,a,q,exp,note]) => {
    const got = mark(t,a,q);
    return {typed:t, expected:exp, got, pass:got===exp, note};
  });
});
let bad=0;
for (const c of r) { if(!c.pass) bad++;
  console.log(`  ${c.pass?'ok  ':'FAIL'} ${JSON.stringify(c.typed).padEnd(11)} -> ${c.got.padEnd(6)} (expected ${c.expected})  ${c.note}`); }
console.log(bad? `\n${bad} FAILED` : '\nall marking cases pass');
await b.close();
process.exit(bad?1:0);
