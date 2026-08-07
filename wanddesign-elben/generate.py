#!/usr/bin/env python3
"""
Generator für 10 Wanddesigns im elbisch-kalligrafischen Stil.

- Schwarzer Hintergrund, helle (silber/weiße) fließende Linien.
- Vollständig eigene, erfundene Zierglyphen im "elbischen" Look
  (keine echten Tolkien-/Tengwar-Schriftzeichen).
- Vektor (SVG) -> ideal zum Nachzeichnen, Projizieren oder Drucken.

Ausgabe: svg/wanddesign-01.svg ... svg/wanddesign-10.svg
"""

import math
import os

W, H = 1600, 1000          # Grundformat (skaliert verlustfrei)
BG = "#0a0a0a"             # fast-schwarz
INK = "#e9e6dc"            # warmes silber-weiss
INK2 = "#b9c7d6"           # kühles silber (Akzent)
GOLD = "#c8a24a"           # sparsamer gold-akzent

# --------------------------------------------------------------------------
# Deterministischer Pseudo-Zufall (kein random-Modul -> reproduzierbar)
# --------------------------------------------------------------------------
class Rng:
    def __init__(self, seed):
        self.s = seed & 0xFFFFFFFF
    def next(self):
        # xorshift32
        x = self.s
        x ^= (x << 13) & 0xFFFFFFFF
        x ^= (x >> 17)
        x ^= (x << 5) & 0xFFFFFFFF
        self.s = x & 0xFFFFFFFF
        return self.s / 0xFFFFFFFF
    def rng(self, a, b):
        return a + (b - a) * self.next()
    def pick(self, seq):
        return seq[int(self.next() * len(seq)) % len(seq)]


# --------------------------------------------------------------------------
# Baustein: eine fließende "elbische" Zierglyphe entlang einer Grundlinie.
# Erzeugt geschwungene Schäfte, Bögen, Schleifen und Punkte (tehta-artig).
# --------------------------------------------------------------------------
def flourish_glyph(x, y, scale, r, up=True):
    """Gibt eine Liste von SVG-Pfad-/Kreis-Fragmenten zurück."""
    parts = []
    s = scale
    d = -1 if up else 1
    style = int(r.rng(0, 5))

    if style == 0:  # Schleifen-Schaft
        parts.append(
            f'<path d="M {x:.1f} {y:.1f} '
            f'c {0.2*s:.1f} {d*0.9*s:.1f} {0.9*s:.1f} {d*0.9*s:.1f} {0.9*s:.1f} {d*0.1*s:.1f} '
            f'c 0 {-d*0.5*s:.1f} {-0.7*s:.1f} {-d*0.4*s:.1f} {-0.35*s:.1f} {d*0.35*s:.1f}" />'
        )
        parts.append(f'<circle cx="{x+0.9*s:.1f}" cy="{y+d*0.55*s:.1f}" r="{0.05*s:.1f}" class="dot"/>')
    elif style == 1:  # Doppelbogen mit Punkten
        parts.append(
            f'<path d="M {x:.1f} {y:.1f} q {0.45*s:.1f} {d*0.8*s:.1f} {0.9*s:.1f} 0 '
            f'q {0.45*s:.1f} {-d*0.8*s:.1f} {0.9*s:.1f} 0" />'
        )
        parts.append(f'<circle cx="{x+0.45*s:.1f}" cy="{y+d*0.62*s:.1f}" r="{0.045*s:.1f}" class="dot"/>')
        parts.append(f'<circle cx="{x+1.35*s:.1f}" cy="{y+d*0.62*s:.1f}" r="{0.045*s:.1f}" class="dot"/>')
    elif style == 2:  # Hoher Schaft mit Fahne
        parts.append(
            f'<path d="M {x:.1f} {y:.1f} c 0 {d*0.9*s:.1f} {0.1*s:.1f} {d*1.1*s:.1f} {0.5*s:.1f} {d*1.1*s:.1f} '
            f'c {0.4*s:.1f} 0 {0.5*s:.1f} {-d*0.4*s:.1f} {0.1*s:.1f} {-d*0.55*s:.1f}" />'
        )
    elif style == 3:  # Spiralknospe
        cx, cy = x + 0.5*s, y + d*0.5*s
        parts.append(
            f'<path d="M {x:.1f} {y:.1f} q {0.5*s:.1f} {d*0.2*s:.1f} {0.5*s:.1f} {d*0.5*s:.1f} '
            f'a {0.28*s:.1f} {0.28*s:.1f} 0 1 {1 if up else 0} {0.001*s:.1f} 0" />'
        )
        parts.append(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{0.05*s:.1f}" class="dot"/>')
    else:  # verschlungenes S mit Krönchen
        parts.append(
            f'<path d="M {x:.1f} {y:.1f} c {0.5*s:.1f} {d*0.5*s:.1f} {-0.5*s:.1f} {d*0.6*s:.1f} '
            f'0 {d*1.1*s:.1f} c {0.4*s:.1f} {d*0.3*s:.1f} {0.7*s:.1f} {-d*0.1*s:.1f} {0.5*s:.1f} {-d*0.4*s:.1f}" />'
        )
        parts.append(f'<circle cx="{x:.1f}" cy="{y+d*1.15*s:.1f}" r="{0.05*s:.1f}" class="dot"/>')
    return parts


def script_band(x0, y, x1, scale, seed, jitter=0.0):
    """Eine Zeile fortlaufender elbischer Zierschrift zwischen x0 und x1."""
    r = Rng(seed)
    parts = []
    # Grundlinie (fein)
    parts.append(f'<line x1="{x0:.1f}" y1="{y:.1f}" x2="{x1:.1f}" y2="{y:.1f}" class="baseline"/>')
    x = x0 + scale * 0.4
    while x < x1 - scale:
        up = r.next() > 0.35
        yy = y + r.rng(-jitter, jitter)
        parts += flourish_glyph(x, yy, scale, r, up=up)
        x += scale * r.rng(0.85, 1.25)
    return "\n".join(parts)


def vine(x, y, length, scale, seed, angle=-90):
    """Rankende Vertikal-/Horizontal-Linie mit Blättern und Knospen."""
    r = Rng(seed)
    parts = []
    a = math.radians(angle)
    px, py = x, y
    pts = []
    steps = int(length / (scale*0.5))
    for i in range(steps):
        sway = math.sin(i*0.5) * scale*0.6
        na = a + math.radians(sway*0.15)
        px += math.cos(na) * scale*0.5
        py += math.sin(na) * scale*0.5
        pts.append((px, py))
    # Hauptranke als glatter Pfad
    d = f'M {pts[0][0]:.1f} {pts[0][1]:.1f} '
    for i in range(1, len(pts)-1, 2):
        cx, cy = pts[i]
        ex, ey = pts[i+1]
        d += f'Q {cx:.1f} {cy:.1f} {ex:.1f} {ey:.1f} '
    parts.append(f'<path d="{d}" />')
    # Blätter/Knospen entlang der Ranke
    for i in range(2, len(pts)-2, 3):
        bx, by = pts[i]
        side = 1 if (i//3) % 2 == 0 else -1
        lx = bx + side*scale*0.9
        ly = by - scale*0.2
        parts.append(
            f'<path d="M {bx:.1f} {by:.1f} q {side*scale*0.7:.1f} {-scale*0.6:.1f} '
            f'{side*scale*0.9:.1f} {scale*0.1:.1f} q {-side*scale*0.4:.1f} {scale*0.3:.1f} '
            f'{-side*scale*0.9:.1f} {-scale*0.1:.1f} z" class="leaf"/>'
        )
        parts.append(f'<circle cx="{lx:.1f}" cy="{ly:.1f}" r="{scale*0.06:.1f}" class="dot"/>')
    return "\n".join(parts)


def ring_inscription(cx, cy, radius, scale, seed, rings=1):
    """Kreisförmige Zierschrift (eigene Glyphen) – wie eine Inschrift auf einem Ring."""
    r = Rng(seed)
    parts = []
    for k in range(rings):
        rad = radius - k*scale*2.2
        parts.append(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{rad:.1f}" class="baseline"/>')
        n = int(2*math.pi*rad / (scale*1.3))
        for i in range(n):
            ang = 2*math.pi*i/n
            gx = cx + math.cos(ang)*rad
            gy = cy + math.sin(ang)*rad
            # kleine tangentiale Glyphe
            t = ang + math.pi/2
            up = r.next() > 0.5
            d = -1 if up else 1
            l = scale*0.9
            ex = gx + math.cos(t)*l
            ey = gy + math.sin(t)*l
            nx = math.cos(ang)*d*scale*0.7
            ny = math.sin(ang)*d*scale*0.7
            parts.append(
                f'<path d="M {gx:.1f} {gy:.1f} q {nx+ (ex-gx)*0.5:.1f} {ny+(ey-gy)*0.5:.1f} '
                f'{ex-gx:.1f} {ey-gy:.1f}" transform="translate(0,0)"/>'
            )
            if i % 3 == 0:
                parts.append(f'<circle cx="{gx+math.cos(ang)*d*scale*1.1:.1f}" '
                             f'cy="{gy+math.sin(ang)*d*scale*1.1:.1f}" r="{scale*0.05:.1f}" class="dot"/>')
    return "\n".join(parts)


def star_burst(cx, cy, rad, points, seed):
    r = Rng(seed)
    parts = []
    pts = []
    for i in range(points*2):
        ang = math.pi*i/points - math.pi/2
        rr = rad if i % 2 == 0 else rad*0.42
        pts.append((cx+math.cos(ang)*rr, cy+math.sin(ang)*rr))
    d = "M " + " L ".join(f"{p[0]:.1f} {p[1]:.1f}" for p in pts) + " Z"
    parts.append(f'<path d="{d}" class="thin"/>')
    parts.append(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{rad*0.14:.1f}" class="thin"/>')
    return "\n".join(parts)


# --------------------------------------------------------------------------
# SVG-Gerüst
# --------------------------------------------------------------------------
def svg_header(title, subtitle):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">
  <title>{title}</title>
  <defs>
    <style>
      .bg {{ fill: {BG}; }}
      path, line, circle {{ fill: none; }}
      path {{ stroke: {INK}; stroke-width: 3; stroke-linecap: round; stroke-linejoin: round; }}
      .thin {{ stroke: {INK2}; stroke-width: 2; }}
      .baseline {{ stroke: {INK2}; stroke-width: 1.2; opacity: 0.5; }}
      .dot {{ fill: {GOLD}; stroke: none; }}
      .leaf {{ stroke: {INK}; stroke-width: 2.2; }}
      .frame {{ stroke: {GOLD}; stroke-width: 2; opacity: 0.7; }}
      .label {{ fill: {INK2}; font-family: Georgia, 'Times New Roman', serif;
                font-size: 22px; letter-spacing: 4px; opacity: 0.65; }}
    </style>
  </defs>
  <rect class="bg" x="0" y="0" width="{W}" height="{H}"/>
  <rect class="frame" x="40" y="40" width="{W-80}" height="{H-80}" rx="6"/>
  <text class="label" x="{W/2}" y="{H-58}" text-anchor="middle">{subtitle}</text>
'''

def svg_footer():
    return "</svg>\n"


# --------------------------------------------------------------------------
# Die 10 Designs
# --------------------------------------------------------------------------
def design_01():  # Fließende Schrift-Friese (3 Bänder)
    s = svg_header("Wanddesign 01 – Schriftbänder", "I · SCHRIFTBAENDER")
    for i, yy in enumerate((300, 500, 700)):
        s += script_band(120, yy, W-120, 70, seed=101+i, jitter=6) + "\n"
    return s + svg_footer()

def design_02():  # Großer Ring mit Inschrift
    s = svg_header("Wanddesign 02 – Inschrift-Ring", "II · INSCHRIFT-RING")
    s += ring_inscription(W/2, H/2-10, 300, 26, seed=202, rings=2) + "\n"
    s += star_burst(W/2, H/2-10, 70, 6, seed=222) + "\n"
    return s + svg_footer()

def design_03():  # Vertikale Ranken-Bordüre (Paar)
    s = svg_header("Wanddesign 03 – Ranken-Bordüre", "III · RANKEN-BORDUERE")
    s += vine(220, H-120, 780, 46, seed=303, angle=-90) + "\n"
    s += vine(W-220, H-120, 780, 46, seed=333, angle=-90) + "\n"
    s += script_band(360, H/2, W-360, 54, seed=353, jitter=4) + "\n"
    return s + svg_footer()

def design_04():  # Lebensbaum / verzweigte Ranke
    s = svg_header("Wanddesign 04 – Lebensbaum", "IV · LEBENSBAUM")
    cx = W/2
    s += vine(cx, H-120, 640, 52, seed=404, angle=-90) + "\n"
    for k, ang in enumerate((-125, -55, -145, -35, -100, -80)):
        s += vine(cx + math.cos(math.radians(ang))*40,
                  H-120 - 220 - k*55, 320, 34, seed=414+k, angle=ang) + "\n"
    s += star_burst(cx, 190, 46, 7, seed=444) + "\n"
    return s + svg_footer()

def design_05():  # Eckornamente (4 Ecken) + Zentrum
    s = svg_header("Wanddesign 05 – Eckornamente", "V · ECKORNAMENTE")
    corners = [(160,160,1,1),(W-160,160,-1,1),(160,H-160,1,-1),(W-160,H-160,-1,-1)]
    for i,(x,y,sx,sy) in enumerate(corners):
        s += (f'<g transform="translate({x},{y}) scale({sx},{sy})">'
              + vine(0,0,300,40,seed=505+i,angle=0)
              + vine(0,0,300,40,seed=515+i,angle=90)
              + '</g>\n')
    s += ring_inscription(W/2, H/2, 130, 22, seed=555, rings=1) + "\n"
    return s + svg_footer()

def design_06():  # Durchgehendes Wiederhol-Muster (Kachel-Fries)
    s = svg_header("Wanddesign 06 – Flächenmuster", "VI · FLAECHENMUSTER")
    for row, yy in enumerate(range(180, H-120, 150)):
        s += script_band(120, yy, W-120, 58, seed=606+row, jitter=3) + "\n"
    return s + svg_footer()

def design_07():  # Torbogen / Portal
    s = svg_header("Wanddesign 07 – Torbogen", "VII · TORBOGEN")
    cx = W/2
    top, bottom, half = 180, H-140, 330
    s += (f'<path d="M {cx-half:.1f} {bottom:.1f} L {cx-half:.1f} {top+180:.1f} '
          f'A {half:.1f} {half:.1f} 0 0 1 {cx+half:.1f} {top+180:.1f} '
          f'L {cx+half:.1f} {bottom:.1f}" class="thin"/>\n')
    s += ring_inscription(cx, top+180, 250, 22, seed=707, rings=1) + "\n"
    s += vine(cx-half, bottom, 520, 40, seed=717, angle=-90) + "\n"
    s += vine(cx+half, bottom, 520, 40, seed=727, angle=-90) + "\n"
    s += script_band(cx-260, bottom-40, cx+260, 46, seed=737) + "\n"
    return s + svg_footer()

def design_08():  # Sternenkarte mit Zier-Glyphen
    s = svg_header("Wanddesign 08 – Sternenkarte", "VIII · STERNENKARTE")
    r = Rng(808)
    for _ in range(9):
        cx, cy = r.rng(220, W-220), r.rng(150, H-200)
        s += star_burst(cx, cy, r.rng(24, 60), int(r.rng(5,8)), seed=int(r.rng(1,9999))) + "\n"
    s += script_band(140, H-140, W-140, 50, seed=828, jitter=5) + "\n"
    return s + svg_footer()

def design_09():  # Verschlungenes Band (Knotwork-artig)
    s = svg_header("Wanddesign 09 – Flechtband", "IX · FLECHTBAND")
    y = H/2
    amp, per = 120, 220
    d1 = f'M 120 {y:.1f} '
    d2 = f'M 120 {y:.1f} '
    x = 120
    k = 0
    while x < W-120:
        d1 += f'q {per/2:.1f} {(-amp if k%2==0 else amp):.1f} {per:.1f} 0 '
        d2 += f'q {per/2:.1f} {(amp if k%2==0 else -amp):.1f} {per:.1f} 0 '
        x += per; k += 1
    s += f'<path d="{d1}" />\n<path d="{d2}" class="thin"/>\n'
    # Knospen an den Kreuzungspunkten
    x = 120
    while x < W-120:
        s += f'<circle cx="{x:.1f}" cy="{y:.1f}" r="7" class="dot"/>\n'
        x += per
    s += script_band(140, y-200, W-140, 46, seed=909) + "\n"
    s += script_band(140, y+200, W-140, 46, seed=919) + "\n"
    return s + svg_footer()

def design_10():  # Großes Zentral-Emblem
    s = svg_header("Wanddesign 10 – Zentral-Emblem", "X · ZENTRAL-EMBLEM")
    cx, cy = W/2, H/2-10
    s += ring_inscription(cx, cy, 320, 24, seed=1010, rings=3) + "\n"
    s += star_burst(cx, cy, 150, 8, seed=1020) + "\n"
    s += star_burst(cx, cy, 90, 6, seed=1030) + "\n"
    for ang in range(0, 360, 45):
        a = math.radians(ang)
        x = cx + math.cos(a)*360
        y = cy + math.sin(a)*360
        s += vine(x, y, 120, 26, seed=1040+ang, angle=ang) + "\n"
    return s + svg_footer()


DESIGNS = [design_01, design_02, design_03, design_04, design_05,
           design_06, design_07, design_08, design_09, design_10]


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    out = os.path.join(here, "svg")
    os.makedirs(out, exist_ok=True)
    for i, fn in enumerate(DESIGNS, 1):
        path = os.path.join(out, f"wanddesign-{i:02d}.svg")
        with open(path, "w", encoding="utf-8") as f:
            f.write(fn())
        print("geschrieben:", path)


if __name__ == "__main__":
    main()
