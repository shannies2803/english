#!/usr/bin/env python3
"""Import dropped XP, badges and preferences on the floor. Merge everything."""
import pathlib, sys
p = pathlib.Path("build_site2.py"); s = p.read_text(encoding="utf-8")
old = """        cur.done=Math.max(cur.done||0,ip.done||0);
        cur.right=Math.max(cur.right||0,ip.right||0);
        cur.streak=Math.max(cur.streak||0,ip.streak||0);"""
new = """        // Lifetime counters take the higher of the two. Max rather than sum, so that
        // importing the same backup twice cannot inflate anything.
        for(const k of ['done','right','streak','xp','best_combo','perfect','bosses','goalweeks'])
          cur[k]=Math.max(cur[k]||0,ip[k]||0);
        // 'retired' is a count in older saves and a list in newer ones
        if(Array.isArray(cur.retired)||Array.isArray(ip.retired)){
          const a=Array.isArray(cur.retired)?cur.retired:[], b=Array.isArray(ip.retired)?ip.retired:[];
          cur.retired=[...new Set([...a,...b])];
        } else cur.retired=Math.max(cur.retired||0,ip.retired||0);
        // badges and completed groups are sets: union them, never lose one
        cur.badges=[...new Set([...(cur.badges||[]),...(ip.badges||[])])];
        cur.groups=[...new Set([...(cur.groups||[]),...(ip.groups||[])])];
        // this child's settings come across only when this device has no history of
        // its own, so importing a backup never silently changes a device in use
        const untouched=!(cur.done>0);
        for(const k of ['ts','theme','goal','name','lvl'])
          if(ip[k]!==undefined && (untouched || cur[k]===undefined)) cur[k]=ip[k];
        if(ip.week && (!cur.week || (ip.week.count||0)>(cur.week.count||0))) cur.week=ip.week;"""
assert s.count(old) == 1
s = s.replace(old, new)

# say what actually came across, instead of a bare "merged"
old2 = """      S.profiles.forEach(migrate); save(); boot();
      alert('Progress merged. Nothing was overwritten.');"""
new2 = """      S.profiles.forEach(migrate); save(); boot();
      const sum=S.profiles.map(x=>`${x.name}: ${x.done} questions, ${x.xp} XP, ${(x.badges||[]).length} badges, ${(x.log||[]).length} saved mistakes`).join('\\n');
      alert('Progress merged. Nothing was overwritten.\\n\\n'+sum);"""
assert s.count(old2) == 1
s = s.replace(old2, new2)
p.write_text(s, encoding="utf-8")
print("import now merges every field, and reports what came across")
