#!/usr/bin/env python3
"""Improvements: dark mode, the undefined CSS variables, and the listening script on marking."""
import pathlib, sys
p = pathlib.Path("build_site2.py"); s = p.read_text(encoding="utf-8")
c = [0]
def sub(old, new, label):
    global s
    if s.count(old) == 1:
        s = s.replace(old, new); c[0] += 1; print(f"  {c[0]}. {label}")
    elif new in s:
        c[0] += 1; print(f"  {c[0]}. {label} (already applied)")
    else:
        sys.exit(f"anchor {s.count(old)}x: {label}")

# ── 1 ── --card and --wash were used by earlier additions but never defined
sub("""  --r:14px; --shadow:0 1px 2px rgba(22,35,59,.05),0 10px 30px rgba(22,35,59,.07);
}""",
"""  --card:#FFFFFF; --wash:#F4F6FA;
  --r:14px; --shadow:0 1px 2px rgba(22,35,59,.05),0 10px 30px rgba(22,35,59,.07);
}

/* Dark mode. Follows the device by default; the moon button overrides it per child.
   Every surface colour is a token, so only the tokens change here. */
@media (prefers-color-scheme: dark){
  :root:not([data-theme="light"]){
    --ink:#E6ECF7; --muted:#9AA8BF; --paper:#11161F; --sheet:#1A212D; --line:#2B3442;
    --card:#1A212D; --wash:#212A38;
    --ok:#4ADE9B; --ok-bg:#122C23; --no:#FF8A7E; --no-bg:#301A18;
    --accent:#4FD1BE; --accent-soft:#12312D; --accent-deep:#8FE8DA;
    --gold:#F5C34B;
    --shadow:0 1px 2px rgba(0,0,0,.30),0 10px 30px rgba(0,0,0,.34);
  }
  :root:not([data-theme="light"]) body[data-level="P3"]{ --accent:#B79BFF; --accent-soft:#251A40; --accent-deep:#CDB8FF }
}
:root[data-theme="dark"]{
  --ink:#E6ECF7; --muted:#9AA8BF; --paper:#11161F; --sheet:#1A212D; --line:#2B3442;
  --card:#1A212D; --wash:#212A38;
  --ok:#4ADE9B; --ok-bg:#122C23; --no:#FF8A7E; --no-bg:#301A18;
  --accent:#4FD1BE; --accent-soft:#12312D; --accent-deep:#8FE8DA;
  --gold:#F5C34B;
  --shadow:0 1px 2px rgba(0,0,0,.30),0 10px 30px rgba(0,0,0,.34);
}
:root[data-theme="dark"] body[data-level="P3"]{ --accent:#B79BFF; --accent-soft:#251A40; --accent-deep:#CDB8FF }
@media print{ :root{ --ink:#000; --paper:#fff; --sheet:#fff; --card:#fff; --muted:#333; --line:#999 } }""",
    "--card and --wash defined, and a full dark mode")

# anything that hard-codes white has to follow the theme too
sub(".boss{background:linear-gradient(140deg,#2A1F3D,#4A2C6B);color:#F1EAFB;",
    ".boss{background:linear-gradient(140deg,#2A1F3D,#4A2C6B);color:#F1EAFB;",
    "boss panel already dark in both themes")

# ── 2 ── the theme button, next to the text-size buttons
sub("""      <button class="tsbtn" data-ts="xl">A++</button>
    </span></div>""",
"""      <button class="tsbtn" data-ts="xl">A++</button>
      <button class="tsbtn" id="themeBtn" title="Light or dark">◑</button>
    </span></div>""",
    "Theme button in the top bar")

sub("""document.querySelectorAll('.tsbtn').forEach(b=>b.onclick=()=>{
  const p=P(); p.ts=b.dataset.ts; save();
  document.body.dataset.ts=p.ts;
  document.querySelectorAll('.tsbtn').forEach(x=>x.classList.toggle('on',x===b));
});""",
"""document.querySelectorAll('.tsbtn[data-ts]').forEach(b=>b.onclick=()=>{
  const p=P(); p.ts=b.dataset.ts; save();
  document.body.dataset.ts=p.ts;
  document.querySelectorAll('.tsbtn[data-ts]').forEach(x=>x.classList.toggle('on',x===b));
});
// theme cycles device -> light -> dark and is remembered for this child
function applyTheme(){
  const t=(P()||{}).theme||'auto';
  if(t==='auto') document.documentElement.removeAttribute('data-theme');
  else document.documentElement.dataset.theme=t;
  const b=document.getElementById('themeBtn');
  if(b){ b.textContent = t==='auto'?'◑':(t==='light'?'☀':'☾');
         b.title = t==='auto'?'Following your device — tap for light':(t==='light'?'Light — tap for dark':'Dark — tap to follow your device'); }
}
document.getElementById('themeBtn').onclick=()=>{
  const p=P(); p.theme = p.theme==='auto'||!p.theme ? 'light' : (p.theme==='light'?'dark':'auto');
  save(); applyTheme();
};""",
    "Theme toggle wired and remembered per child")

sub("""  document.body.dataset.ts = p.ts || 'm';""",
"""  document.body.dataset.ts = p.ts || 'm';
  applyTheme();""",
    "Theme applied when a profile loads")

# ── 3 ── listening: after marking, show the line of the script that carried the answer
sub("""    fb.innerHTML = good
      ? `<div class="fbhead">${TICK}${praise}</div>${q.tip?`<div class="tip">${esc(q.tip)}</div>`:''}`
      : `<div class="fbhead">${CROSS}${verdict==='close'?'So close — check the spelling.':'Not quite.'}</div>
         <div>Answer: <span class="model">${esc(q.m||q.a[0])}</span></div>
         ${q.tip?`<div class="tip">${esc(q.tip)}</div>`:''}`;""",
"""    const heard = (Q.set && Q.set.listening && q.script)
      ? `<details class="heard"><summary>What the reader said</summary><div>${
          q.script.split('\\n\\n').map(x=>`<p>${esc(x)}</p>`).join('')}</div></details>` : '';
    fb.innerHTML = good
      ? `<div class="fbhead">${TICK}${praise}</div>${q.tip?`<div class="tip">${esc(q.tip)}</div>`:''}${heard}`
      : `<div class="fbhead">${CROSS}${verdict==='close'?'So close — check the spelling.':'Not quite.'}</div>
         <div>Answer: <span class="model">${esc(q.m||q.a[0])}</span></div>
         ${q.tip?`<div class="tip">${esc(q.tip)}</div>`:''}${heard}`;""",
    "Listening: the script is revealed once the answer is marked")

sub(".weakrow{display:flex;",
""".heard{margin-top:10px;border-top:1px solid var(--line);padding-top:8px}
.heard summary{cursor:pointer;font:600 13.5px/1 var(--sans);color:var(--muted)}
.heard summary:hover{color:var(--ink)}
.heard div{margin-top:8px;font-size:14.5px;line-height:1.6;color:var(--muted)}
.heard p{margin:0 0 8px}
.weakrow{display:flex;""",
    "Styling for the revealed script")
p.write_text(s, encoding="utf-8")
print(f"\n{c[0]} edits applied")
