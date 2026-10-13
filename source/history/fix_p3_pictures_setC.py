"""The corrected panels for compP3c, after looking at the first draft rendered at
the size it actually appears. Kept as a script so the set can be rebuilt."""
import sys, json, pathlib
sys.path.insert(0, "lib")
from p3pics import *

fn = pathlib.Path("content_v11_p3_composition.json")
d = json.loads(fn.read_text(encoding="utf-8")); T = {t["n"]: t for t in d["set"]["tasks"]}

FIX = {
 # 1 · The Broken Vase — pieces were behind the table legs; the ball hung in mid-air
 (1,2): (panel(window(104,22), table(16,66,42), person(112,54,TEAL,arms="up",legs="stand"),
               shards(28,96), ball(66,93), worry(128,40)), None),
 (1,3): (panel(window(108,22), person(40,54,TEAL,arms="hold_low",legs="kneel"),
               shards(72,96), openbox(106,84,34,15), worry(20,44)), None),
 # 2 · The Hungry Stray — figures sat on the bench, props unreadable, cat on the box
 (2,1): (panel(bench(100,72,52), cat(26,88), person(60,48,TEAL,legs="stand"),
               person(90,48,ORANGE,legs="stand"), worry(44,58)), None),
 (2,2): (panel(person(34,50,TEAL,arms="reach_r",legs="kneel"), plate(68,92,24),
               cat(116,88), person(140,50,ORANGE,arms="down",legs="stand"), worry(100,56)),
         "They put some food from their plates on the ground for it"),
 (2,3): (panel(openbox(100,82,36,16), person(34,50,TEAL,arms="carry",legs="walk"),
               bowl(66,92,20), cat(132,70), smile_mark(118,34)),
         "They bring a cardboard box and a bowl of water"),
 (2,4): (panel(wallsign(92,22,46,24), cat_in_box(20,80,44,18),
               person(114,56,PLUM,arms="up",legs="stand"), sparkle(78,46)), None),
 # 3 · The Missing Shoe — speed marks implied motion beside a stationary bench
 (3,2): (panel(bench(96,76,50), person(42,50,TEAL,arms="hold_low",legs="kneel"),
               bag(70,80,c=RED), worry(22,42)), None),
 # 4 · The New Pupil — she sat astride a narrow table; the watchers merged
 (4,1): (panel(table(74,62,52), bench(18,80,46), seated(36,52,PLUM),
               person(104,50,TEAL,legs="stand"), person(138,50,ORANGE,legs="stand")), None),
 (4,2): (panel(table(70,62,48), bench(14,80,42), seated(32,52,PLUM),
               person(100,50,TEAL,arms="out",legs="stand"), person(136,50,ORANGE,legs="stand"),
               quote(118,24)), None),
 (4,3): (panel(person(28,52,PLUM,arms="out",legs="walk"), person(74,52,TEAL,arms="reach_l",legs="stand"),
               person(122,52,ORANGE,arms="out",legs="stand"), ball(52,93)), None),
 # 5 · The Running Tap — she stood out of reach; no spanner; one figure at the wrong scale
 (5,2): (panel(basin(14,70,42), tap(30,52,running=True),
               person(66,52,PLUM,arms="reach_l",legs="stand"), worry(100,44), speed(116,58)), None),
 (5,3): (panel(person(30,52,PLUM,arms="out",legs="run"), speed(8,60),
               person(104,48,NAVY,h=11,tall=32,arms="carry",legs="walk"), spanner(124,78), quote(62,24)), None),
 (5,4): (panel(basin(12,70,40), tap(28,52), wallsign(90,30,48,24),
               person(72,54,PLUM,arms="up",legs="stand"), sparkle(150,52)), None),
 # 6 · The Heavy Bags — no stairs at all in panel three; the tin floated
 (6,1): (panel(lift_doors(14,46), person(96,50,PLUM,h=10,tall=28,arms="hold_low",legs="stand"),
               bag(118,80,c=RED,w=15,h=16), bag(70,80,c=GREEN,w=15,h=16)), None),
 (6,2): (panel(lift_doors(14,46,broken=True), wallsign(60,16,44,22),
               person(118,50,PLUM,h=10,tall=28,arms="down",legs="stand"),
               bag(82,80,c=GREEN,w=15,h=16), bag(98,80,c=RED,w=15,h=16), worry(142,40)), None),
 (6,3): (panel(staircase(84,106,4,11), person(26,54,TEAL,arms="carry",legs="walk"),
               bag(44,82,c=GREEN,w=14,h=15), person(66,48,ORANGE,arms="carry",legs="walk"),
               bag(84,62,c=RED,w=14,h=15), person(126,22,PLUM,h=9,tall=24,arms="down",legs="walk")), None),
 (6,4): (panel(door(12,50), person(58,50,PLUM,h=10,tall=28,arms="reach_r",legs="stand"),
               tin(80,76,22), person(116,54,TEAL,arms="carry",legs="stand"), smile_mark(130,30)), None),
}
for (tn, pi), (svg, cap) in FIX.items():
    T[tn]["pictures"][pi-1]["svg"] = svg
    if cap: T[tn]["pictures"][pi-1]["caption"] = cap
fn.write_text(json.dumps(d, ensure_ascii=False), encoding="utf-8")
print(f"re-applied {len(FIX)} corrected panels to compP3c")
