import sys, json, pathlib
sys.path.insert(0, "lib")
from p3pics import *

fn = pathlib.Path("content_v7_writing_oral.json")
d = json.loads(fn.read_text(encoding="utf-8")); T = {t["n"]: t for t in d["compositionP3b"]["tasks"]}

PICS = {
 # B1 · The Skipping Rope
 (1,1): panel(rope(50,44), person(44,54,PLUM,arms="up",legs="run"), worry(72,46),
              person(110,52,TEAL,arms="down",legs="stand"), person(138,52,ORANGE,arms="down",legs="stand")),
 (1,2): panel(door(126,50), rope(46,42), person(42,52,PLUM,arms="up",legs="stand"),
              window(84,22,30,22), speed(14,60)),
 (1,3): panel(rope(96,70), seated(44,52,PLUM), bench(18,80,46), worry(74,50), tear(36,56)),
 (1,4): panel(rope(44,40), person(38,52,PLUM,arms="up",legs="run"), certificate(96,54),
              person(126,50,NAVY,h=10,tall=26,arms="reach_l",legs="stand"), sparkle(74,36)),
 # B2 · The Lost Little Boy
 (2,1): panel(stall(10,22,40,RED), stall(58,22,40,GOLD), stall(106,22,44,GREEN),
              person(80,58,ORANGE,h=8,tall=22,arms="down",legs="stand"), tear(72,62), worry(104,56), ground=FLOOR),
 (2,2): panel(person(44,58,ORANGE,h=8,tall=22,arms="down",legs="stand"),
              person(100,52,PLUM,arms="reach_l",legs="kneel"), quote(72,24), tear(36,62), ground=FLOOR),
 (2,3): panel(person(42,48,NAVY,h=9,tall=24,arms="up",legs="stand"), counter(14,64,56,label="INFORMATION"),
              person(98,52,PLUM,arms="down",legs="stand"), person(128,58,ORANGE,h=8,tall=22,arms="down",legs="stand"),
              speed(74,40), ground=FLOOR),
 (2,4): panel(person(46,46,PLUM,h=11,tall=32,arms="reach_r",legs="walk"),
              person(90,58,ORANGE,h=8,tall=22,arms="up",legs="stand"), smile_mark(20,30),
              person(134,52,PLUM,arms="down",legs="stand"), sparkle(116,40), ground=FLOOR),
 # B3 · The Shared Umbrella
 (3,1): panel(rain(14,14,6,132), umbrella(44,38,34), person(44,58,PLUM,arms="up",legs="stand"), door(126,50)),
 (3,2): panel(rain(14,14,6,132), umbrella(38,38,32), person(38,58,PLUM,arms="up",legs="stand"),
              person(112,56,TEAL,arms="down",legs="stand"), worry(90,48), door(128,50)),
 (3,3): panel(rain(14,12,6,132), umbrella(70,36,42), person(56,58,PLUM,arms="up",legs="walk"),
              person(88,58,TEAL,arms="down",legs="walk")),
 (3,4): panel(bench(14,78,52), seated(36,50,PLUM), seated(70,50,TEAL),
              bowl(104,88,20), smile_mark(120,34), sparkle(136,50)),
 # B4 · The Class Plant
 (4,1): panel(table(96,66,50), pot(120,60), person(40,52,TEAL,arms="reach_r",legs="stand"),
              wateringcan(66,58), person(138,46,PLUM,h=11,tall=32,arms="down",legs="stand")),
 (4,2): panel(table(14,66,48), pot(38,60), window(100,24,34,26), wateringcan(66,86), worry(126,58)),
 (4,3): panel(table(14,66,48), pot(38,60,droop=True), person(102,52,TEAL,arms="up",legs="stand"),
              worry(74,44), window(124,24,28,22)),
 (4,4): panel(table(14,66,48), pot(38,60,flower=True), person(102,52,TEAL,arms="reach_l",legs="stand"),
              wateringcan(74,58), sparkle(132,40), smile_mark(118,30)),
 # B5 · Grandmother's Birthday Cake
 (5,1): panel(table(60,68,56), bench(12,82,42), seated(32,54,TEAL), coins(74,62,3),
              person(130,54,ORANGE,arms="down",legs="stand")),
 (5,2): panel(table(14,66,54), cake(26,54,26), card(62,52), person(100,52,TEAL,arms="reach_l",legs="stand"),
              person(134,52,ORANGE,arms="down",legs="stand")),
 (5,3): panel(table(14,66,52), cake(24,54,26,lopsided=True), person(90,52,TEAL,arms="up",legs="stand"),
              person(126,52,ORANGE,arms="up",legs="stand"), worry(66,44)),
 (5,4): panel(table(14,66,52), cake(24,52,26,candles=3), person(94,46,PLUM,h=11,tall=32,arms="out",legs="stand"),
              person(132,54,TEAL,h=8,tall=22,arms="up",legs="stand"), smile_mark(72,30), sparkle(60,42)),
 # B6 · The Last Leg
 (6,1): panel(lane(90,3), person(38,54,PLUM,arms="reach_r",legs="run"), baton(60,62),
              person(106,54,ORANGE,arms="out",legs="run"), speed(12,60)),
 (6,2): panel(lane(90,3), person(34,54,PLUM,arms="out",legs="run"), fallen(94,80,ORANGE),
              speed(10,60), worry(66,46)),
 (6,3): panel(lane(90,3), person(42,52,PLUM,arms="reach_r",legs="kneel"), fallen(78,86,ORANGE),
              person(130,54,TEAL,arms="down",legs="stand"), sparkle(112,40)),
 (6,4): panel(person(40,46,NAVY,h=11,tall=32,arms="reach_r",legs="stand"), certificate(74,52),
              person(112,54,PLUM,arms="up",legs="stand"), person(140,54,ORANGE,arms="up",legs="stand"),
              smile_mark(96,26), sparkle(22,36)),
}
for (tn, pi), svg in PICS.items():
    T[tn]["pictures"][pi-1]["svg"] = svg
fn.write_text(json.dumps(d, ensure_ascii=False), encoding="utf-8")
print(f"redrew {len(PICS)} panels in compP3b")
