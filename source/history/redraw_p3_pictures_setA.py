import sys, json, pathlib
sys.path.insert(0, "lib")
from p3pics import *

fn = pathlib.Path("content_v5_p3_composition.json")
d = json.loads(fn.read_text(encoding="utf-8")); T = {t["n"]: t for t in d["set"]["tasks"]}

PICS = {
 # A1 · The Wallet on the Bench
 (1,1): panel(bench(14,74,54), wallet(30,64), person(110,52,TEAL,arms="out",legs="walk"), sparkle(76,46)),
 (1,2): panel(bench(12,74,50), wallet(26,64), person(96,52,TEAL,arms="out",legs="stand"), worry(126,42), worry(66,46)),
 (1,3): panel(counter(94,66,58,label="SHOP"), person(40,52,TEAL,arms="reach_r",legs="stand"),
              wallet(72,56), person(124,46,NAVY,h=10,tall=26,arms="reach_l",legs="stand")),
 (1,4): panel(person(44,52,TEAL,arms="down",legs="stand"), person(96,48,PLUM,h=10,tall=28,arms="reach_l",legs="stand"),
              wallet(70,60), smile_mark(110,26), sparkle(126,44)),
 # A2 · The Fallen Groceries
 (2,1): panel(person(44,48,NAVY,h=10,tall=28,arms="hold_low",legs="walk"), bag(64,78,c=GREEN,w=16,h=17),
              worry(22,40), tree(128,62)),
 (2,2): panel(person(40,48,NAVY,h=10,tall=28,arms="out",legs="stand"), tornbag(62,80),
              fruit(92,93,3), worry(18,38), speed(118,62)),
 (2,3): panel(person(34,48,NAVY,h=10,tall=28,arms="hold_low",legs="stand"),
              person(92,52,PLUM,arms="reach_l",legs="kneel"), fruit(116,93,3), tornbag(62,80)),
 (2,4): panel(door(14,50), person(54,48,NAVY,h=10,tall=28,arms="reach_r",legs="stand"),
              person(104,52,PLUM,arms="carry",legs="walk"), bag(122,80,c=GREEN,w=15,h=16), smile_mark(76,28)),
 # A3 · The Kite in the Tree
 (3,1): panel(kite(118,34,RED), person(34,54,TEAL,arms="up",legs="run"), person(66,54,ORANGE,arms="up",legs="stand"),
              speed(10,62)),
 (3,2): panel(tree(112,56), kite(112,40,RED,tail=False), person(34,54,TEAL,arms="up",legs="stand"),
              person(64,54,ORANGE,arms="up",legs="stand"), worry(84,44)),
 (3,3): panel(tree(126,56), kite(126,40,RED,tail=False), person(30,54,TEAL,arms="out",legs="stand"),
              person(78,48,NAVY,h=10,tall=28,arms="up",legs="stand"), quote(54,24)),
 (3,4): panel(kite(120,30,RED), person(36,54,TEAL,arms="up",legs="run"), person(68,54,ORANGE,arms="up",legs="stand"),
              smile_mark(94,34), sparkle(16,44)),
 # A4 · Caught in the Rain
 (4,1): panel(person(44,54,TEAL,arms="down",legs="walk"), tree(128,62),
              *[f"<circle cx='{x}' cy='22' r='9' fill='{PALE}'/>" for x in (30,44,58)]),
 (4,2): panel(rain(16,16,6,130), person(52,56,TEAL,arms="up",legs="run"), worry(80,46), speed(118,62)),
 (4,3): panel(rain(16,14,6,130), umbrella(66,38,36), person(52,56,PLUM,arms="up",legs="stand"),
              person(84,56,TEAL,arms="down",legs="stand")),
 (4,4): panel(door(130,50), umbrella(56,34,34), person(44,54,PLUM,arms="down",legs="walk"),
              person(72,54,TEAL,arms="down",legs="walk"), smile_mark(96,26)),
 # A5 · The Spilt Paint
 (5,1): panel(easel(100,36), table(14,70,46), paintpot(26,56,RED), paintpot(44,56,GOLD),
              person(72,52,TEAL,arms="reach_l",legs="stand"), person(132,52,ORANGE,arms="down",legs="stand")),
 (5,2): panel(easel(104,36), table(14,70,46), paintpot(30,88,RED,spilt=True),
              person(70,52,TEAL,arms="up",legs="stand"), worry(94,44), paintpot(46,56,GOLD)),
 (5,3): panel(person(40,52,TEAL,arms="down",legs="stand"), person(96,46,PLUM,h=11,tall=32,arms="reach_l",legs="stand"),
              paintpot(20,88,RED,spilt=True), quote(68,24)),
 (5,4): panel(paintpot(96,88,RED,spilt=True), person(40,52,TEAL,arms="hold_low",legs="kneel"),
              person(118,46,PLUM,h=11,tall=32,arms="hold_low",legs="kneel"), sparkle(76,44)),
 # A6 · The Injured Bird
 (6,1): panel(tree(128,58), bird(46,92), person(96,52,PLUM,arms="out",legs="stand"), worry(70,48)),
 (6,2): panel(openbox(96,82,34,15), bird(110,76), person(44,52,PLUM,arms="reach_r",legs="kneel"), sparkle(74,44)),
 (6,3): panel(door(124,50), person(44,46,NAVY,h=11,tall=32,arms="carry",legs="walk"),
              openbox(64,70,30,14), person(100,54,PLUM,h=8,tall=22,arms="down",legs="walk")),
 (6,4): panel(tree(24,58), bird(104,30,flying=True), person(68,52,PLUM,arms="up",legs="stand"),
              smile_mark(40,34), sparkle(136,42)),
}
for (tn, pi), svg in PICS.items():
    T[tn]["pictures"][pi-1]["svg"] = svg
fn.write_text(json.dumps(d, ensure_ascii=False), encoding="utf-8")
print(f"redrew {len(PICS)} panels in compP3a")
