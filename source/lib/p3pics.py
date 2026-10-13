"""Flat-silhouette picture panels for Primary 3 composition tasks.

The style is fixed by the two sets already in the bank: a 160x120 panel with a
pale background and a ground bar, figures built from a circle head, a rounded
rectangle body and stroked limbs in one solid colour each, and a small set of
marks for motion and feeling. No faces, no skin tones — the earlier attempt at
drawing heads with skin tones had to be redrawn, because it sat beside these
and looked like a different book.
"""

BG, BG2 = "#F1F4F9", "#D7E0EC"
GROUND, FLOOR = "#C6CEDC", "#E0D6C4"
TEAL, PLUM, ORANGE, NAVY = "#10786A", "#B4527A", "#E8865C", "#1F3C88"
GOLD, RED, GREEN, WOOD, STEEL = "#E0A800", "#D6392C", "#4C9F70", "#A88B62", "#8FA5C0"
MARK, SPEECH, PALE = "#8894AA", "#5C6B85", "#CBD5E3"


def panel(*parts, bg=BG, ground=GROUND, gy=100):
    """A finished panel. Pass the drawing parts in back-to-front order."""
    body = "".join(parts)
    g = (f"<rect x='4' y='{gy}' width='152' height='6' rx='3' fill='{ground}'/>" if ground else "")
    return (f"<svg viewBox='0 0 160 120'><rect width='160' height='120' rx='8' fill='{bg}'/>{g}{body}</svg>")


def person(x, y, c, h=9, tall=26, arms="down", legs="stand", lean=0):
    """A figure standing on the ground, head centre at (x, y).

    arms: down | out | up | reach_r | reach_l | carry | hold_low
    legs: stand | walk | run | kneel | sit
    """
    bw = h * 2 - 2
    bx, by = x - bw / 2, y + h + 1
    p = [f"<circle cx='{x + lean}' cy='{y}' r='{h}' fill='{c}'/>",
         f"<rect x='{bx}' y='{by}' width='{bw}' height='{tall}' rx='{bw/2.3:.1f}' fill='{c}'/>"]
    sy = by + 4
    aw = max(4.4, h * 0.55)
    A = {
        "down":     [f"M{bx} {sy}L{bx-5} {sy+11}", f"M{bx+bw} {sy}L{bx+bw+5} {sy+11}"],
        "out":      [f"M{bx} {sy}L{bx-11} {sy+3}", f"M{bx+bw} {sy}L{bx+bw+11} {sy+3}"],
        "up":       [f"M{bx} {sy}L{bx-8} {sy-11}", f"M{bx+bw} {sy}L{bx+bw+8} {sy-11}"],
        "reach_r":  [f"M{bx} {sy}L{bx-5} {sy+10}", f"M{bx+bw} {sy}L{bx+bw+13} {sy-5}"],
        "reach_l":  [f"M{bx} {sy}L{bx-13} {sy-5}", f"M{bx+bw} {sy}L{bx+bw+5} {sy+10}"],
        "carry":    [f"M{bx} {sy}L{bx-4} {sy+13}", f"M{bx+bw} {sy}L{bx+bw+4} {sy+13}"],
        "hold_low": [f"M{bx} {sy}L{bx-2} {sy+14}", f"M{bx+bw} {sy}L{bx+bw+2} {sy+14}"],
    }[arms]
    for d in A:
        p.append(f"<path d='{d}' stroke='{c}' stroke-width='{aw:.1f}' stroke-linecap='round' fill='none'/>")
    ky, lw = by + tall - 2, max(5, h * 0.62)
    L = {
        "stand": [f"M{x-4} {ky}L{x-5} {ky+12}", f"M{x+4} {ky}L{x+5} {ky+12}"],
        "walk":  [f"M{x-3} {ky}L{x-9} {ky+12}", f"M{x+3} {ky}L{x+8} {ky+11}"],
        "run":   [f"M{x-3} {ky}L{x-13} {ky+9}", f"M{x+3} {ky}L{x+11} {ky+12}"],
        # a folded thigh along the ground with the shin dropping from its end reads as
        # kneeling; a single diagonal read as a lunge, or as the figure falling over
        "kneel": [f"M{x-2} {ky}L{x-14} {ky+2}", f"M{x-14} {ky+2}L{x-14} {ky+8}",
                  f"M{x+3} {ky}L{x+5} {ky+8}"],
        "sit":   [f"M{x-3} {ky}L{x+9} {ky}", f"M{x+8} {ky}L{x+9} {ky+11}"],
    }[legs]
    for d in L:
        p.append(f"<path d='{d}' stroke='{c}' stroke-width='{lw:.1f}' stroke-linecap='round' fill='none'/>")
    return "".join(p)


def seated(x, y, c, h=9):
    """A figure sitting on a bench or step at (x, y) head centre."""
    bw = h * 2 - 2
    return (f"<circle cx='{x}' cy='{y}' r='{h}' fill='{c}'/>"
            f"<rect x='{x-bw/2}' y='{y+h+1}' width='{bw}' height='18' rx='{bw/2.3:.1f}' fill='{c}'/>"
            f"<path d='M{x-2} {y+h+18}L{x+13} {y+h+19}' stroke='{c}' stroke-width='6' stroke-linecap='round'/>"
            f"<path d='M{x+11} {y+h+19}L{x+12} {y+h+30}' stroke='{c}' stroke-width='6' stroke-linecap='round'/>"
            f"<path d='M{x+bw/2} {y+h+6}L{x+bw/2+9} {y+h+13}' stroke='{c}' stroke-width='5' stroke-linecap='round'/>")


# ── small marks, used sparingly
def worry(x, y):      return f"<path d='M{x} {y}q-6 6-3 12M{x+5} {y}q6 6 3 12' stroke='{MARK}' stroke-width='2.4' fill='none' stroke-linecap='round'/>"
def speed(x, y):      return f"<path d='M{x} {y}h11M{x+2} {y+6}h9M{x+4} {y+12}h7' stroke='{MARK}' stroke-width='2.2' stroke-linecap='round'/>"
def sparkle(x, y):    return f"<path d='M{x} {y-6}l2 5 5 1-4 3 1 6-4-3-5 3 1-6-4-3 5-1z' fill='{GOLD}'/>"
def quote(x, y):      return f"<text x='{x}' y='{y}' font-size='16' text-anchor='middle' fill='{SPEECH}' font-family='system-ui'>&#8220;&#8221;</text>"
def tear(x, y):       return f"<circle cx='{x}' cy='{y}' r='2' fill='#5AA9E6'/><circle cx='{x+5}' cy='{y+4}' r='1.6' fill='#5AA9E6'/>"
def smile_mark(x, y): return f"<path d='M{x} {y}q6-7 12 0' stroke='{GOLD}' stroke-width='3' fill='none' stroke-linecap='round'/>"

# ── props
def bench(x, y, w=46):  return f"<rect x='{x}' y='{y}' width='{w}' height='5' rx='2.5' fill='{WOOD}'/><rect x='{x+4}' y='{y+5}' width='4' height='12' fill='{WOOD}'/><rect x='{x+w-8}' y='{y+5}' width='4' height='12' fill='{WOOD}'/>"
def table(x, y, w=52):  return f"<rect x='{x}' y='{y}' width='{w}' height='5' rx='2' fill='{WOOD}'/><rect x='{x+3}' y='{y+5}' width='4' height='{98-y}' fill='{WOOD}'/><rect x='{x+w-7}' y='{y+5}' width='4' height='{98-y}' fill='{WOOD}'/>"
def door(x, y, w=30, h=46, c=PALE): return f"<rect x='{x}' y='{y}' width='{w}' height='{h}' rx='3' fill='{c}'/><circle cx='{x+w-6}' cy='{y+h/2}' r='2.2' fill='{SPEECH}'/>"
def window(x, y, w=34, h=26): return f"<rect x='{x}' y='{y}' width='{w}' height='{h}' rx='3' fill='#EAF1FB' stroke='{PALE}' stroke-width='2.4'/><path d='M{x+w/2} {y}v{h}M{x} {y+h/2}h{w}' stroke='{PALE}' stroke-width='2'/>"
def vase(x, y, c=RED, broken=False):
    if broken:
        return (f"<path d='M{x-9} {y+10}l5-4 3 5z' fill='{c}'/><path d='M{x+2} {y+11}l6-5 2 5z' fill='{c}'/>"
                f"<path d='M{x-2} {y+6}l4-4 3 4z' fill='{c}' opacity='.8'/>")
    return (f"<path d='M{x-6} {y}q-4 10 0 16h12q4-6 0-16z' fill='{c}'/>"
            f"<rect x='{x-4}' y='{y-4}' width='8' height='5' rx='2' fill='{c}'/>")
def ball(x, y, r=7, c=GOLD): return f"<circle cx='{x}' cy='{y}' r='{r}' fill='{c}'/>"
def bag(x, y, c=GREEN, w=16, h=18): return f"<rect x='{x}' y='{y}' width='{w}' height='{h}' rx='2' fill='{c}'/><path d='M{x+3} {y}q{w/2-3} -8 {w-6} 0' stroke='{c}' stroke-width='2.4' fill='none'/>"
def cat(x, y, c="#8C7350"):
    return (f"<ellipse cx='{x}' cy='{y}' rx='12' ry='7' fill='{c}'/>"
            f"<circle cx='{x-11}' cy='{y-5}' r='5.5' fill='{c}'/>"
            f"<path d='M{x-15} {y-9}l1-4 3 3zM{x-8} {y-10}l2-4 2 4z' fill='{c}'/>"
            f"<path d='M{x+11} {y-2}q7-3 5-10' stroke='{c}' stroke-width='3' fill='none' stroke-linecap='round'/>"
            f"<path d='M{x-6} {y+6}v4M{x+4} {y+6}v4' stroke='{c}' stroke-width='3' stroke-linecap='round'/>")
def box(x, y, w=30, h=16, c=WOOD): return f"<rect x='{x}' y='{y}' width='{w}' height='{h}' rx='2' fill='{c}'/><path d='M{x} {y+5}h{w}' stroke='#FFFFFF' stroke-width='1.6' opacity='.5'/>"
def tap(x, y, running=False):
    w = f"<path d='M{x+10} {y+8}v{26}' stroke='#5AA9E6' stroke-width='4' stroke-linecap='round'/>" if running else ""
    return (f"<path d='M{x} {y}h8v8' stroke='{STEEL}' stroke-width='4' fill='none' stroke-linejoin='round'/>"
            f"<rect x='{x-4}' y='{y-5}' width='8' height='5' rx='2' fill='{STEEL}'/>" + w)
def basin(x, y, w=40): return f"<path d='M{x} {y}h{w}v7a9 9 0 0 1-9 9h-{w-18}a9 9 0 0 1-9-9z' fill='{PALE}'/>"
def shoe(x, y, c=NAVY): return f"<path d='M{x} {y}h13q5 0 6 5h-19z' fill='{c}'/>"
def lift(x, y, w=36, h=48, lit=False):
    c = GOLD if lit else PALE
    return (f"<rect x='{x}' y='{y}' width='{w}' height='{h}' rx='3' fill='{PALE}'/>"
            f"<path d='M{x+w/2} {y}v{h}' stroke='#FFFFFF' stroke-width='2'/>"
            f"<rect x='{x+w/2-7}' y='{y-9}' width='14' height='7' rx='2' fill='{c}'/>")
def stairs(x, y, n=4, s=9):
    return "".join(f"<rect x='{x+i*s}' y='{y+ (n-1-i)*-0 + i*0}' width='{s}' height='{(i+1)*s}' fill='{PALE}' transform='translate(0,{-(i+1)*s+ (n)*s})'/>" for i in range(n))
def sign(x, y, w=40, h=22, c="#FFFFFF"):
    return (f"<rect x='{x}' y='{y}' width='{w}' height='{h}' rx='3' fill='{c}' stroke='{PALE}' stroke-width='2'/>"
            f"<path d='M{x+5} {y+7}h{w-10}M{x+5} {y+13}h{w-16}' stroke='{SPEECH}' stroke-width='2' stroke-linecap='round'/>")
def tree(x, y):
    return (f"<rect x='{x-3}' y='{y}' width='6' height='26' fill='#8B6B3D'/>"
            f"<circle cx='{x}' cy='{y-8}' r='17' fill='{GREEN}'/><circle cx='{x-13}' cy='{y}' r='11' fill='{GREEN}'/>"
            f"<circle cx='{x+13}' cy='{y-1}' r='11' fill='{GREEN}'/>")


# ── props added after looking at the first drafts at the size they render
def plate(x, y, w=22, food=True):
    """A plate seen in profile on a surface, with a little food on it."""
    f = f"<path d='M{x+5} {y-3}q{w/2-5} -5 {w-10} 0z' fill='{ORANGE}'/>" if food else ""
    return (f"<path d='M{x} {y}h{w}q-2 6-8 6h-{w-16}q-6 0-8-6z' fill='#FFFFFF' stroke='{PALE}' stroke-width='1.6'/>" + f)

def bowl(x, y, w=20, water=True):
    wv = f"<path d='M{x+3} {y+3}h{w-6}' stroke='#5AA9E6' stroke-width='3' stroke-linecap='round'/>" if water else ""
    return (f"<path d='M{x} {y}h{w}v3a8 8 0 0 1-8 8h-{w-16}a8 8 0 0 1-8-8z' fill='{PALE}'/>" + wv)

def openbox(x, y, w=34, h=17, c=WOOD):
    """A box with its near wall lower, so something can be seen sitting inside it."""
    return (f"<path d='M{x} {y}h{w}v{h}h-{w}z' fill='{c}'/>"
            f"<path d='M{x-3} {y+4}h{w+6}v{h-4}h-{w+6}z' fill='{c}' opacity='.85'/>"
            f"<path d='M{x-3} {y+4}h{w+6}' stroke='#FFFFFF' stroke-width='1.6' opacity='.55'/>")

def shards(x, y, c=RED):
    """Broken pieces lying on the ground."""
    return (f"<path d='M{x} {y}l5-6 3 6z' fill='{c}'/>"
            f"<path d='M{x+10} {y}l6-5 2 5z' fill='{c}'/>"
            f"<path d='M{x+20} {y}l4-4 3 4z' fill='{c}' opacity='.85'/>"
            f"<path d='M{x+5} {y+1}h22' stroke='{c}' stroke-width='1.4' opacity='.45'/>")

def spanner(x, y, c=STEEL):
    return (f"<path d='M{x} {y}l16 10' stroke='{c}' stroke-width='4' stroke-linecap='round'/>"
            f"<path d='M{x-6} {y-6}a5.5 5.5 0 1 0 7 7l-3-3 1-3-4 2z' fill='{c}'/>")

def staircase(x, y, steps=4, s=11):
    """A flight of stairs rising to the right, resting on the ground at y."""
    out = []
    for i in range(steps):
        h = (i + 1) * s
        out.append(f"<rect x='{x + i*s}' y='{y - h}' width='{s}' height='{h}' fill='{PALE}'/>")
        out.append(f"<path d='M{x + i*s} {y - h}h{s}' stroke='#FFFFFF' stroke-width='1.8'/>")
    return "".join(out)

def lift_doors(x, y, w=34, h=50, broken=False):
    lamp = RED if broken else GOLD
    return (f"<rect x='{x}' y='{y}' width='{w}' height='{h}' rx='2' fill='{PALE}'/>"
            f"<path d='M{x+w/2} {y}v{h}' stroke='#FFFFFF' stroke-width='2.4'/>"
            f"<rect x='{x+w+4}' y='{y+10}' width='7' height='14' rx='3' fill='{STEEL}'/>"
            f"<circle cx='{x+w+7.5}' cy='{y+17}' r='2.2' fill='{lamp}'/>")

def tin(x, y, w=22, c=GOLD):
    return (f"<rect x='{x}' y='{y}' width='{w}' height='11' rx='2' fill='{c}'/>"
            f"<rect x='{x-2}' y='{y-3}' width='{w+4}' height='4' rx='2' fill='{c}'/>"
            f"<path d='M{x+4} {y+5}h{w-8}' stroke='#FFFFFF' stroke-width='1.6' opacity='.6'/>")

def wallsign(x, y, w=44, h=24):
    """A notice fixed flat to a wall — not a speech bubble floating in the air."""
    return (f"<rect x='{x}' y='{y}' width='{w}' height='{h}' rx='2' fill='#FFFFFF' stroke='{STEEL}' stroke-width='2'/>"
            f"<path d='M{x+5} {y+8}h{w-10}M{x+5} {y+14}h{w-17}' stroke='{SPEECH}' stroke-width='2' stroke-linecap='round'/>"
            f"<circle cx='{x+3}' cy='{y+3}' r='1.6' fill='{STEEL}'/><circle cx='{x+w-3}' cy='{y+3}' r='1.6' fill='{STEEL}'/>")


# ── further props, for redrawing the first two composition sets
def wallet(x, y, c="#8B6B3D"):
    return (f"<rect x='{x}' y='{y}' width='18' height='12' rx='2' fill='{c}'/>"
            f"<path d='M{x} {y+5}h18' stroke='#FFFFFF' stroke-width='1.4' opacity='.55'/>"
            f"<rect x='{x+11}' y='{y+3}' width='5' height='4' rx='1' fill='{GOLD}'/>")

def counter(x, y, w=56, label=None):
    t = (f"<text x='{x+5}' y='{y+13}' font-family='system-ui' font-size='8' fill='{SPEECH}'>{label}</text>"
         if label else "")
    return (f"<rect x='{x}' y='{y}' width='{w}' height='{100-y}' rx='2' fill='{PALE}'/>"
            f"<rect x='{x-2}' y='{y-4}' width='{w+4}' height='5' rx='2' fill='{STEEL}'/>" + t)

def kite(x, y, c=RED, tail=True):
    t = (f"<path d='M{x} {y+13}q5 7 -1 12q-6 5 0 11' stroke='{c}' stroke-width='1.8' fill='none'/>" if tail else "")
    return (f"<path d='M{x} {y-12}l10 12-10 13-10-13z' fill='{c}'/>"
            f"<path d='M{x-10} {y} h20M{x} {y-12}v25' stroke='#FFFFFF' stroke-width='1.2' opacity='.6'/>" + t)

def umbrella(x, y, w=34, c="#7C4DB5", up=True):
    if not up:
        return f"<path d='M{x} {y}l16 26' stroke='{c}' stroke-width='3.4' stroke-linecap='round'/>"
    return (f"<path d='M{x-w/2} {y}a{w/2} {w/2.6} 0 0 1 {w} 0z' fill='{c}'/>"
            f"<path d='M{x} {y}v22' stroke='{c}' stroke-width='2.6' stroke-linecap='round'/>"
            f"<path d='M{x} {y+22}q5 0 5-5' stroke='{c}' stroke-width='2.4' fill='none' stroke-linecap='round'/>")

def rain(x, y, n=5, w=40):
    return "".join(f"<path d='M{x + i*(w/n)} {y}l-3 9' stroke='#5AA9E6' stroke-width='2' stroke-linecap='round'/>"
                   for i in range(n))

def paintpot(x, y, c=GOLD, spilt=False):
    if spilt:
        return (f"<path d='M{x} {y+8}l12-7 3 8z' fill='{c}'/>"
                f"<path d='M{x-6} {y+13}q14-5 28 0q-14 5-28 0z' fill='{c}'/>")
    return (f"<rect x='{x}' y='{y}' width='13' height='13' rx='2' fill='{c}'/>"
            f"<rect x='{x-2}' y='{y-3}' width='17' height='4' rx='2' fill='{c}'/>")

def bird(x, y, c="#6E7C93", flying=False):
    if flying:
        return (f"<path d='M{x-10} {y}q6-7 10 0q4-7 10 0' stroke='{c}' stroke-width='3' fill='none' stroke-linecap='round'/>")
    return (f"<ellipse cx='{x}' cy='{y}' rx='8' ry='5.5' fill='{c}'/>"
            f"<circle cx='{x-7}' cy='{y-4}' r='4' fill='{c}'/>"
            f"<path d='M{x-11} {y-4}l-3 1 3 1z' fill='{GOLD}'/>"
            f"<path d='M{x+7} {y-1}q6-2 4-7' stroke='{c}' stroke-width='2.4' fill='none' stroke-linecap='round'/>")

def rope(x, y, c=GOLD):
    return f"<path d='M{x} {y}q-22 26 0 30' stroke='{c}' stroke-width='2.6' fill='none' stroke-linecap='round'/>"

def wateringcan(x, y, c=GREEN):
    return (f"<rect x='{x}' y='{y}' width='15' height='13' rx='2.5' fill='{c}'/>"
            f"<path d='M{x+15} {y+4}l7-4v8z' fill='{c}'/>"
            f"<path d='M{x+3} {y}q4-6 8 0' stroke='{c}' stroke-width='2.4' fill='none'/>")

def pot(x, y, droop=False, flower=False):
    stem = (f"<path d='M{x} {y}q2-10 9-12' stroke='{GREEN if not droop else '#8C7013'}' stroke-width='2.6' fill='none' stroke-linecap='round'/>"
            if droop else f"<path d='M{x} {y}v-14' stroke='{GREEN}' stroke-width='2.6' stroke-linecap='round'/>")
    leaf = (f"<path d='M{x} {y-10}q-8 2-9-5q7-1 9 5z' fill='{'#8C7013' if droop else GREEN}'/>"
            f"<path d='M{x} {y-13}q8 2 9-5q-7-1-9 5z' fill='{'#8C7013' if droop else GREEN}'/>")
    fl = f"<circle cx='{x}' cy='{y-17}' r='4.5' fill='{RED}'/>" if flower else ""
    return (f"<path d='M{x-8} {y}h16l-2 12h-12z' fill='{WOOD}'/>" + stem + leaf + fl)

def cake(x, y, w=26, candles=0, lopsided=False):
    tilt = f" transform='rotate(-7 {x+w/2} {y+6})'" if lopsided else ""
    c = "".join(f"<path d='M{x+6+i*7} {y}v-7' stroke='{PALE}' stroke-width='2'/>"
                f"<circle cx='{x+6+i*7}' cy='{y-9}' r='2.4' fill='{GOLD}'/>" for i in range(candles))
    return (f"<g{tilt}><rect x='{x}' y='{y}' width='{w}' height='13' rx='2' fill='#E8D5A3'/>"
            f"<rect x='{x}' y='{y}' width='{w}' height='4' rx='2' fill='#C9663C'/></g>" + c)

def coins(x, y, n=3):
    return "".join(f"<circle cx='{x+i*9}' cy='{y}' r='4' fill='{GOLD}'/>" for i in range(n))

def card(x, y, w=18, h=14):
    return (f"<rect x='{x}' y='{y}' width='{w}' height='{h}' rx='1.5' fill='#FFFFFF' stroke='{PLUM}' stroke-width='1.8'/>"
            f"<path d='M{x+5} {y+7}q4-4 8 0' stroke='{PLUM}' stroke-width='2' fill='none'/>")

def baton(x, y, c=RED):
    return f"<rect x='{x}' y='{y}' width='15' height='4.5' rx='2.2' fill='{c}' transform='rotate(-18 {x} {y})'/>"

def certificate(x, y, w=26, h=19):
    return (f"<rect x='{x}' y='{y}' width='{w}' height='{h}' rx='2' fill='#FFFFFF' stroke='{GOLD}' stroke-width='2'/>"
            f"<path d='M{x+4} {y+7}h{w-8}M{x+4} {y+12}h{w-13}' stroke='{SPEECH}' stroke-width='1.6' stroke-linecap='round'/>")

def stall(x, y, w=44, c=RED):
    return (f"<rect x='{x}' y='{y}' width='{w}' height='9' rx='2' fill='{c}'/>"
            f"<rect x='{x+2}' y='{y+9}' width='{w-4}' height='{96-y-9}' rx='2' fill='{PALE}'/>")

def fruit(x, y, n=3, c=GOLD):
    return "".join(f"<circle cx='{x+i*11}' cy='{y}' r='5' fill='{c if i%2==0 else GREEN}'/>" for i in range(n))

def tornbag(x, y, c=GREEN):
    return (f"<path d='M{x} {y}h16l-2 14h-5l-3-5-3 5h-1z' fill='{c}'/>"
            f"<path d='M{x+3} {y}q5-7 10 0' stroke='{c}' stroke-width='2.2' fill='none'/>")

def easel(x, y, w=26):
    return (f"<rect x='{x}' y='{y}' width='{w}' height='22' rx='2' fill='#FFFFFF' stroke='{PALE}' stroke-width='2'/>"
            f"<path d='M{x+3} {y+22}l-4 {96-y-22}M{x+w-3} {y+22}l4 {96-y-22}' stroke='{WOOD}' stroke-width='3'/>")

def lane(y, n=3):
    return "".join(f"<path d='M4 {y+i*7}h152' stroke='#FFFFFF' stroke-width='1.6' opacity='.7'/>" for i in range(n))

def fallen(x, y, c):
    """A figure lying on the ground, seen from the side."""
    return (f"<circle cx='{x}' cy='{y}' r='9' fill='{c}'/>"
            f"<rect x='{x+8}' y='{y-7}' width='26' height='15' rx='7' fill='{c}'/>"
            f"<path d='M{x+30} {y-4}l11-6M{x+30} {y+4}l12 5' stroke='{c}' stroke-width='5' stroke-linecap='round'/>"
            f"<path d='M{x+12} {y-8}l6-9' stroke='{c}' stroke-width='4.6' stroke-linecap='round'/>")


def cat_in_box(x, y, w=40, h=18, c=WOOD, cc="#8C7350"):
    """A cat sitting inside a box, not balanced on top of it. The near wall of the
    box is drawn last, so it covers the cat's lower half the way a real box would."""
    return (f"<path d='M{x} {y}h{w}v{h}h-{w}z' fill='{c}'/>"
            + cat(x + w / 2, y + 2, cc)
            + f"<path d='M{x-3} {y+5}h{w+6}v{h-1}h-{w+6}z' fill='{c}'/>"
              f"<path d='M{x-3} {y+5}h{w+6}' stroke='#FFFFFF' stroke-width='1.6' opacity='.55'/>")
