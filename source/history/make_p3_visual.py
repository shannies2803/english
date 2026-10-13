import json, pathlib

def wrap(title, accent, light, pale, body):
    return (f'<div style="font-family:system-ui,sans-serif;background:#FFF;border:2px solid {accent};'
            f'border-radius:10px;padding:18px 20px;max-width:520px;color:#15171F">'
            f'<div style="background:{accent};color:#fff;margin:-18px -20px 14px;padding:11px 20px;'
            f'border-radius:8px 8px 0 0;font-weight:800;font-size:19px;letter-spacing:.2px">{title}</div>'
            + body + '</div>')

def tbl(light, pale, headers, rows):
    th = "".join(f'<th style="text-align:left;padding:7px 8px;border:1px solid {light};background:{pale}">{h}</th>' for h in headers)
    out = [f'<table style="width:100%;border-collapse:collapse;font-size:13.5px"><tr>{th}</tr>']
    for i, r in enumerate(rows):
        tds = "".join(f'<td style="padding:7px 8px;border:1px solid {light};background:{pale if i%2 else "#FFFFFF"}">{c}</td>' for c in r)
        out.append(f"<tr>{tds}</tr>")
    return "".join(out) + "</table>"

def note(text, accent, pale):
    return (f'<p style="margin:12px 0 0;font-size:12.5px;background:{pale};border-left:4px solid {accent};'
            f'padding:8px 10px;border-radius:0 6px 6px 0">{text}</p>')

V = []

# ── P3 · a class timetable, the commonest P3 stimulus of all
AC, LI, PA = "#2A5CA8", "#C4D7EF", "#EBF2FB"
V.append({"id":"vtZE","level":"P3","title":"Primary 3 Timetable","html": wrap(
  "PRIMARY 3 KINDNESS — TIMETABLE", AC, LI, PA,
  '<p style="margin:0 0 12px;font-size:13.5px">Recess is from <b>9.30 to 10.00 a.m.</b> every day.</p>'
  + tbl(LI, PA, ["Time", "Monday", "Tuesday", "Wednesday"],
      [["8.00 – 9.30", "English", "Mathematics", "English"],
       ["10.00 – 11.00", "Mathematics", "Science", "Mathematics"],
       ["11.00 – 12.00", "Science", "Art", "Mother Tongue"],
       ["12.00 – 1.00", "Physical Education", "Mother Tongue", "Music"]])
  + note("Bring your recorder on the day you have Music. Bring your PE kit on the day you have "
         "Physical Education.", AC, PA)),
 "questions":[
  {"n":1,"q":"What time does recess begin?","options":["8.00 a.m.","9.30 a.m.","10.00 a.m.","11.00 a.m."],"correct":1,
   "tip":"The line above the table gives the recess time."},
  {"n":2,"q":"Which subject do the pupils have first on Tuesday?","options":["English","Mathematics","Science","Art"],"correct":1,
   "tip":"Read down the Tuesday column to the first row."},
  {"n":3,"q":"On which day do the pupils have Art?","options":["Monday","Tuesday","Wednesday","Every day"],"correct":1,
   "tip":"Look across the 11.00 – 12.00 row."},
  {"n":4,"q":"Which subject is taught on all three days?","options":["Science","Art","Mathematics","Music"],"correct":2,
   "tip":"Check each subject against all three columns. Mathematics appears in every one."},
  {"n":5,"q":"On which day must a pupil bring her recorder?","options":["Monday","Tuesday","Wednesday","Every day"],"correct":2,
   "tip":"The box says to bring it on the Music day. Find Music in the table."},
  {"n":6,"q":"How long is the first lesson of each day?","options":["Half an hour","One hour","One and a half hours","Two hours"],"correct":2,
   "tip":"The first row runs from 8.00 to 9.30."},
  {"n":7,"q":"A pupil has forgotten his PE kit. On which day will this be a problem?","options":["Monday","Tuesday","Wednesday","It will not matter"],"correct":0,
   "tip":"Find Physical Education in the table, then read which column it is in."},
  {"n":8,"q":"Which statement is true according to the timetable?","options":["Science is taught every day","Mother Tongue is taught twice","Art is taught before recess","Music is on Monday"],"correct":1,
   "tip":"Check each one. Count how many times Mother Tongue appears."}]})

# ── P3 · a simple pictogram, which P3 papers use as often as a bar chart
AC, LI, PA = "#1E7A4C", "#BEDDC9", "#EAF5EF"
rows = [("Monday", 4), ("Tuesday", 7), ("Wednesday", 3), ("Thursday", 7), ("Friday", 9)]
pic = "".join(
  f'<div style="display:flex;align-items:center;gap:10px;margin:7px 0;font-size:13px">'
  f'<div style="width:86px;flex:0 0 86px;font-weight:600">{d}</div>'
  f'<div style="letter-spacing:3px;font-size:16px;color:{AC}">' + "●" * n + "</div>"
  f'<div style="margin-left:6px;color:#5C6B85">{n}</div></div>'
  for d, n in rows)
V.append({"id":"vtZF","level":"P3","title":"Books Borrowed Last Week","html": wrap(
  "BOOKS BORROWED BY PRIMARY 3 KINDNESS", AC, LI, PA,
  '<p style="margin:0 0 10px;font-size:13.5px">Each <b style="color:'+AC+'">●</b> stands for '
  '<b>one book</b>.</p>' + pic
  + note("The library is closed on Saturday and Sunday. Any book taken out on Friday must be returned "
         "by the following Thursday.", AC, PA)),
 "questions":[
  {"n":1,"q":"How many books does each dot stand for?","options":["One","Two","Five","Ten"],"correct":0,
   "tip":"The line above the chart tells you what one dot means."},
  {"n":2,"q":"On which day were the most books borrowed?","options":["Tuesday","Wednesday","Thursday","Friday"],"correct":3,
   "tip":"Look for the longest row of dots."},
  {"n":3,"q":"How many books were borrowed on Wednesday?","options":["Three","Four","Seven","Nine"],"correct":0,
   "tip":"Count the dots in the Wednesday row, or read the number at the end of it."},
  {"n":4,"q":"On which two days was the same number of books borrowed?","options":["Monday and Wednesday","Tuesday and Thursday","Wednesday and Friday","Monday and Friday"],"correct":1,
   "tip":"Look for two rows with the same number of dots."},
  {"n":5,"q":"How many more books were borrowed on Friday than on Monday?","options":["Three","Four","Five","Nine"],"correct":2,
   "tip":"Take the Monday number away from the Friday number."},
  {"n":6,"q":"How many books were borrowed altogether that week?","options":["Twenty","Twenty-six","Thirty","Thirty-four"],"correct":2,
   "tip":"Add all five numbers: 4, 7, 3, 7 and 9."},
  {"n":7,"q":"A pupil borrows a book on Friday. By which day must she return it?","options":["Monday","Wednesday","Thursday","Friday"],"correct":2,
   "tip":"The box at the bottom gives the rule for books taken out on Friday."},
  {"n":8,"q":"Why does the chart show only five days?","options":["Nobody borrowed books at the weekend","The library is closed at the weekend","The chart ran out of space","Only five days were counted"],"correct":1,
   "tip":"The box at the bottom explains why there is no Saturday or Sunday row."}]})

bad = []
for v in V:
    for q in v["questions"]:
        if len(q["options"]) != 4: bad.append(f'{v["id"]} Q{q["n"]}: {len(q["options"])} options')
        if len(set(q["options"])) != 4: bad.append(f'{v["id"]} Q{q["n"]}: duplicate option')
        if not (0 <= q["correct"] < 4): bad.append(f'{v["id"]} Q{q["n"]}: correct out of range')
        if not q.get("tip"): bad.append(f'{v["id"]} Q{q["n"]}: no explanation')
    ns = [q["n"] for q in v["questions"]]
    assert ns == list(range(1, len(ns)+1))
    import collections
    print(f'{v["level"]} {v["title"][:34]:36s} {len(v["questions"])}q  '
          f'answer positions {dict(sorted(collections.Counter(q["correct"] for q in v["questions"]).items()))}')
# arithmetic in the pictogram questions must actually be right
tot = sum(n for _, n in rows)
assert tot == 30, tot
assert rows[4][1] - rows[0][1] == 5
print("pictogram totals check out: 4+7+3+7+9 =", tot)
for b in bad: print("  ERROR " + b)
print("ERRORS:", len(bad))
pathlib.Path("content_v11_p3_visual.json").write_text(
    json.dumps({"visualTexts": V}, ensure_ascii=False), encoding="utf-8")
