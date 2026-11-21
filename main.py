#!/usr/bin/env python3
"""THE WORLD - Friday 20 November 2026.

A procedural front page of a newspaper summarising 20 November 2026
world news in a single 1024x1024 PNG image.

Pure Python standard library only (zlib + struct for the PNG encoder,
a hand-defined 5x7 bitmap font for all text). No external files, no
network, no randomness, no system date/time: running this script twice
produces a byte-identical entry.png.

Usage: python3 main.py   (writes entry.png next to this file)
"""

import os
import struct
import sys
import zlib

# ---------------------------------------------------------------------------
# Bitmap font: 5x7, one glyph = 7 rows of 5 characters ('#' = ink, '.' = blank)
# ---------------------------------------------------------------------------
FONT = {
    'A': (".###.", "#...#", "#...#", "#####", "#...#", "#...#", "#...#"),
    'B': ("####.", "#...#", "#...#", "####.", "#...#", "#...#", "####."),
    'C': (".####", "#....", "#....", "#....", "#....", "#....", ".####"),
    'D': ("####.", "#...#", "#...#", "#...#", "#...#", "#...#", "####."),
    'E': ("#####", "#....", "#....", "####.", "#....", "#....", "#####"),
    'F': ("#####", "#....", "#....", "####.", "#....", "#....", "#...."),
    'G': (".####", "#....", "#....", "#.###", "#...#", "#...#", ".###."),
    'H': ("#...#", "#...#", "#...#", "#####", "#...#", "#...#", "#...#"),
    'I': ("#####", "..#..", "..#..", "..#..", "..#..", "..#..", "#####"),
    'J': ("..###", "...#.", "...#.", "...#.", "...#.", "#..#.", ".##.."),
    'K': ("#...#", "#..#.", "#.#..", "##...", "#.#..", "#..#.", "#...#"),
    'L': ("#....", "#....", "#....", "#....", "#....", "#....", "#####"),
    'M': ("#...#", "##.##", "#.#.#", "#.#.#", "#...#", "#...#", "#...#"),
    'N': ("#...#", "##..#", "##..#", "#.#.#", "#..##", "#..##", "#...#"),
    'O': (".###.", "#...#", "#...#", "#...#", "#...#", "#...#", ".###."),
    'P': ("####.", "#...#", "#...#", "####.", "#....", "#....", "#...."),
    'Q': (".###.", "#...#", "#...#", "#...#", "#.#.#", "#..#.", ".##.#"),
    'R': ("####.", "#...#", "#...#", "####.", "#.#..", "#..#.", "#...#"),
    'S': (".####", "#....", "#....", ".###.", "....#", "....#", "####."),
    'T': ("#####", "..#..", "..#..", "..#..", "..#..", "..#..", "..#.."),
    'U': ("#...#", "#...#", "#...#", "#...#", "#...#", "#...#", ".###."),
    'V': ("#...#", "#...#", "#...#", "#...#", "#...#", ".#.#.", "..#.."),
    'W': ("#...#", "#...#", "#...#", "#.#.#", "#.#.#", "##.##", "#...#"),
    'X': ("#...#", "#...#", ".#.#.", "..#..", ".#.#.", "#...#", "#...#"),
    'Y': ("#...#", "#...#", ".#.#.", "..#..", "..#..", "..#..", "..#.."),
    'Z': ("#####", "....#", "...#.", "..#..", ".#...", "#....", "#####"),
    '0': (".###.", "#..##", "#.#.#", "##..#", "#...#", "#...#", ".###."),
    '1': ("..#..", ".##..", "..#..", "..#..", "..#..", "..#..", ".###."),
    '2': (".###.", "#...#", "....#", "...#.", "..#..", ".#...", "#####"),
    '3': ("####.", "....#", "....#", ".###.", "....#", "....#", "####."),
    '4': ("...#.", "..##.", ".#.#.", "#..#.", "#####", "...#.", "...#."),
    '5': ("#####", "#....", "####.", "....#", "....#", "#...#", ".###."),
    '6': (".###.", "#....", "#....", "####.", "#...#", "#...#", ".###."),
    '7': ("#####", "....#", "...#.", "...#.", "..#..", "..#..", "..#.."),
    '8': (".###.", "#...#", "#...#", ".###.", "#...#", "#...#", ".###."),
    '9': (".###.", "#...#", "#...#", ".####", "....#", "....#", ".###."),
    'a': (".....", ".....", ".###.", "....#", ".####", "#...#", ".####"),
    'b': ("#....", "#....", "####.", "#...#", "#...#", "#...#", "####."),
    'c': (".....", ".....", ".####", "#....", "#....", "#....", ".####"),
    'd': ("....#", "....#", ".####", "#...#", "#...#", "#...#", ".####"),
    'e': (".....", ".....", ".###.", "#...#", "#####", "#....", ".###."),
    'f': ("..##.", ".#..#", ".#...", "####.", ".#...", ".#...", ".#..."),
    'g': (".....", ".....", ".####", "#...#", "#...#", ".####", "....#", ".###."),
    'h': ("#....", "#....", "####.", "#...#", "#...#", "#...#", "#...#"),
    'i': ("..#..", ".....", ".##..", "..#..", "..#..", "..#..", ".###."),
    'j': ("...#.", ".....", "..##.", "...#.", "...#.", "...#.", "...#.", ".##.."),
    'k': ("#....", "#....", "#..#.", "#.#..", "##...", "#.#..", "#..#."),
    'l': (".##..", "..#..", "..#..", "..#..", "..#..", "..#..", ".###."),
    'm': (".....", ".....", "##.#.", "#.#.#", "#.#.#", "#.#.#", "#.#.#"),
    'n': (".....", ".....", "####.", "#...#", "#...#", "#...#", "#...#"),
    'o': (".....", ".....", ".###.", "#...#", "#...#", "#...#", ".###."),
    'p': (".....", ".....", "####.", "#...#", "#...#", "####.", "#....", "#...."),
    'q': (".....", ".....", ".####", "#...#", "#...#", ".####", "....#", "....#"),
    'r': (".....", ".....", "#.##.", "##..#", "#....", "#....", "#...."),
    's': (".....", ".....", ".####", "#....", ".###.", "....#", "####."),
    't': (".#...", ".#...", "####.", ".#...", ".#...", ".#...", "..##."),
    'u': (".....", ".....", "#...#", "#...#", "#...#", "#...#", ".###."),
    'v': (".....", ".....", "#...#", "#...#", "#...#", ".#.#.", "..#.."),
    'w': (".....", ".....", "#...#", "#.#.#", "#.#.#", "#.#.#", ".#.#."),
    'x': (".....", ".....", "#...#", ".#.#.", "..#..", ".#.#.", "#...#"),
    'y': (".....", ".....", "#...#", "#...#", "#...#", ".####", "....#", ".###."),
    'z': (".....", ".....", "#####", "...#.", "..#..", ".#...", "#####"),
    ' ': (".....", ".....", ".....", ".....", ".....", ".....", "....."),
    '.': (".....", ".....", ".....", ".....", ".....", ".##..", ".##.."),
    ',': (".....", ".....", ".....", ".....", ".##..", ".##..", ".#...", "#...."),
    ':': (".....", ".##..", ".##..", ".....", ".##..", ".##..", "....."),
    ';': (".....", ".##..", ".##..", ".....", ".##..", ".##..", ".#...", "#...."),
    "'": ("..#..", "..#..", ".#...", ".....", ".....", ".....", "....."),
    '"': (".#.#.", ".#.#.", ".....", ".....", ".....", ".....", "....."),
    '!': ("..#..", "..#..", "..#..", "..#..", "..#..", ".....", "..#.."),
    '?': (".###.", "#...#", "....#", "...#.", "..#..", ".....", "..#.."),
    '-': (".....", ".....", ".....", ".###.", ".....", ".....", "....."),
    '\u2014': (".....", ".....", ".....", "#####", ".....", ".....", "....."),
    '(': ("...#.", "..#..", ".#...", ".#...", ".#...", "..#..", "...#."),
    ')': (".#...", "..#..", "...#.", "...#.", "...#.", "..#..", ".#..."),
    '$': ("..#..", ".####", "#.#..", ".###.", "..#.#", "####.", "..#.."),
    '%': ("##..#", "##.#.", "...#.", "..#..", ".#...", "#.##.", "#..##"),
    '&': (".##..", "#..#.", "#..#.", ".#...", "#.#.#", "#..#.", ".##.#"),
    '/': ("....#", "....#", "...#.", "...#.", "..#..", ".#...", "#...."),
    '+': (".....", "..#..", "..#..", ".###.", "..#..", "..#..", "....."),
    '=': (".....", ".....", ".###.", ".....", ".###.", ".....", "....."),
    '*': (".....", ".#.#.", "..#..", "#####", "..#..", ".#.#.", "....."),
    '#': (".#.#.", ".#.#.", "#####", ".#.#.", "#####", ".#.#.", ".#.#."),
    '@': (".###.", "#...#", "#.###", "#.#.#", "#.#..", "#....", ".###."),
    '_': (".....", ".....", ".....", ".....", ".....", ".....", "#####"),
}

# Glyphs with descenders use 8 rows; normalise every glyph to 8 rows so
# drawing code can treat the font uniformly. The extra row is blank.
for _ch in list(FONT):
    _g = FONT[_ch]
    if len(_g) == 7:
        FONT[_ch] = _g + (".....",)
    elif len(_g) != 8:
        raise ValueError("bad glyph %r: %d rows" % (_ch, len(_g)))

FONT_ROWS = 8          # rows per glyph (7 drawn + 1 blank baseline gap)
FONT_COLS = 5          # columns per glyph


def glyph(ch):
    """Return the 8-row glyph for ch; fall back to '?' for unknown chars."""
    return FONT.get(ch, FONT['?'])


# ---------------------------------------------------------------------------
# Minimal PNG encoder (stdlib only): 8-bit RGB, no interlace.
# ---------------------------------------------------------------------------
def _chunk(kind, data):
    out = struct.pack(">I", len(data)) + kind + data
    out += struct.pack(">I", zlib.crc32(kind + data) & 0xFFFFFFFF)
    return out


def encode_png(width, height, rgb):
    """Encode raw RGB bytes (width*height*3) as a PNG file's bytes."""
    ihdr = struct.pack(">IIBBBBB", width, height, 8, 2, 0, 0, 0)
    raw = bytearray()
    stride = width * 3
    for y in range(height):
        raw.append(0)  # filter type 0 (none) for every scanline
        raw += rgb[y * stride:(y + 1) * stride]
    idat = zlib.compress(bytes(raw), 9)
    return (
        b"\x89PNG\r\n\x1a\n"
        + _chunk(b"IHDR", ihdr)
        + _chunk(b"IDAT", idat)
        + _chunk(b"IEND", b"")
    )


# ---------------------------------------------------------------------------
# Canvas: an RGB pixel buffer with simple drawing primitives.
# ---------------------------------------------------------------------------
class Canvas:
    def __init__(self, width, height, bg):
        self.w = width
        self.h = height
        self.px = bytearray(bg * (width * height))

    def set(self, x, y, color):
        if 0 <= x < self.w and 0 <= y < self.h:
            i = (y * self.w + x) * 3
            self.px[i:i + 3] = color

    def fill_rect(self, x, y, w, h, color):
        x0, y0 = max(0, x), max(0, y)
        x1, y1 = min(self.w, x + w), min(self.h, y + h)
        for yy in range(y0, y1):
            i = (yy * self.w + x0) * 3
            self.px[i:(i + (x1 - x0) * 3)] = color * (x1 - x0)

    def line(self, x0, y0, x1, y1, color, thick=1):
        """Bresenham line, with optional thickness."""
        dx, dy = abs(x1 - x0), abs(y1 - y0)
        sx = 1 if x0 < x1 else -1
        sy = 1 if y0 < y1 else -1
        err = dx - dy
        while True:
            if thick <= 1:
                self.set(x0, y0, color)
            else:
                r = thick // 2
                self.fill_rect(x0 - r, y0 - r, thick, thick, color)
            if x0 == x1 and y0 == y1:
                break
            e2 = 2 * err
            if e2 > -dy:
                err -= dy
                x0 += sx
            if e2 < dx:
                err += dx
                y0 += sy

    def circle(self, cx, cy, r, color, filled=True):
        if filled:
            for yy in range(cy - r, cy + r + 1):
                dx = int((r * r - (yy - cy) ** 2) ** 0.5)
                self.fill_rect(cx - dx, yy, 2 * dx + 1, 1, color)
        else:
            for a in range(360):
                import math
                rad = math.radians(a)
                self.set(int(cx + r * math.cos(rad)), int(cy + r * math.sin(rad)), color)

    def triangle(self, pts, color):
        (x0, y0), (x1, y1), (x2, y2) = pts
        ymin, ymax = min(y0, y1, y2), max(y0, y1, y2)
        for y in range(ymin, ymax + 1):
            xs = []
            for (ax, ay), (bx, by) in (((x0, y0), (x1, y1)),
                                       ((x1, y1), (x2, y2)),
                                       ((x2, y2), (x0, y0))):
                if ay == by:
                    continue
                if min(ay, by) <= y <= max(ay, by):
                    t = (y - ay) / (by - ay)
                    xs.append(ax + t * (bx - ax))
            if len(xs) >= 2:
                self.fill_rect(int(min(xs)), y, int(max(xs)) - int(min(xs)) + 1, 1, color)

    def png_bytes(self):
        return encode_png(self.w, self.h, bytes(self.px))


# ---------------------------------------------------------------------------
# Text rendering on the canvas.
# ---------------------------------------------------------------------------
def text_width(text, scale):
    """Pixel width of text drawn at the given scale."""
    if not text:
        return 0
    return len(text) * (FONT_COLS + 1) * scale - scale


def draw_text(cv, x, y, text, scale, color):
    """Draw text with its top-left at (x, y). Returns the width drawn."""
    cx = x
    for ch in text:
        g = glyph(ch)
        for row in range(FONT_ROWS):
            bits = g[row]
            for col in range(FONT_COLS):
                if bits[col] == '#':
                    cv.fill_rect(cx + col * scale, y + row * scale,
                                 scale, scale, color)
        cx += (FONT_COLS + 1) * scale
    return cx - x - scale


def wrap_text(text, max_width, scale):
    """Word-wrap text into lines that fit max_width pixels at scale.

    Returns a list of lines. Never splits a word; a single word longer
    than max_width is placed on its own line (callers must size boxes
    so this never happens for real content).
    """
    words = text.split(" ")
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if text_width(trial, scale) <= max_width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines

# ---------------------------------------------------------------------------
# Palette
# ---------------------------------------------------------------------------
PAPER = (250, 246, 236)      # newsprint cream
INK = (17, 17, 17)           # black ink
RED = (166, 58, 42)          # brick red accent (lead kicker only)
GREY = (110, 110, 110)       # thin rules
LIGHT = (210, 205, 190)      # hairline separators
NIGHT = (27, 42, 58)         # Kyiv night sky
NIGHT_BLD = (12, 20, 29)     # Kyiv building silhouettes
WINDOW = (255, 214, 120)     # lit windows
TRAIL = (255, 170, 60)       # missile trail
BLAST = (255, 120, 40)       # explosion orange
SMOKE = (96, 110, 124)       # smoke grey
SKY = (220, 233, 242)        # pale blue band
GLOBE = (46, 111, 163)       # globe ocean
LAND = (74, 154, 92)         # globe land
SUN = (230, 126, 34)         # sun orange
CHART = (34, 139, 84)        # rising chart green
STONE = (58, 58, 58)         # courthouse stone


def draw_centered(cv, y, text, scale, color):
    w = text_width(text, scale)
    draw_text(cv, (cv.w - w) // 2, y, text, scale, color)


# ---------------------------------------------------------------------------
# Illustrations (all procedural, fixed coordinates, no randomness)
# ---------------------------------------------------------------------------
def draw_kyiv(cv, x, y, w, h):
    """Night skyline of Kyiv under a missile attack."""
    cv.fill_rect(x, y, w, h, NIGHT)
    # stars (fixed positions)
    for sx, sy in [(18, 12), (70, 22), (140, 10), (210, 18), (300, 12),
                   (360, 24), (110, 34), (250, 30), (330, 38), (45, 44)]:
        cv.fill_rect(x + sx, y + sy, 2, 2, (220, 225, 235))
    # missile trails (bright diagonals from the upper sky)
    cv.line(x + 330, y + 6, x + 292, y + 78, TRAIL, 3)
    cv.line(x + 240, y + 4, x + 214, y + 66, (255, 220, 150), 3)
    cv.line(x + 150, y + 8, x + 132, y + 58, TRAIL, 2)
    cv.fill_rect(x + 288, y + 74, 6, 6, (255, 240, 180))
    cv.fill_rect(x + 210, y + 62, 6, 6, (255, 240, 180))
    cv.fill_rect(x + 129, y + 54, 5, 5, (255, 240, 180))
    # building silhouettes along the bottom
    base = y + h
    for bx, bw, bh in [(0, 62, 62), (66, 58, 88), (128, 60, 52),
                       (192, 66, 96), (262, 56, 68), (322, 78, 58)]:
        cv.fill_rect(x + bx, base - bh, bw, bh, NIGHT_BLD)
    # lit windows (fixed positions inside the buildings)
    for wx, wy in [(12, 96), (30, 108), (78, 70), (96, 86), (140, 104),
                   (204, 62), (224, 80), (244, 96), (276, 92), (296, 104),
                   (336, 100), (356, 88), (380, 106)]:
        cv.fill_rect(x + wx, base - wy, 4, 5, WINDOW)
    # explosion bursts above the skyline
    for ex, ey, r in [(168, 108, 13), (300, 116, 11)]:
        cv.circle(x + ex, y + ey, r, BLAST)
        cv.circle(x + ex, y + ey, r // 2, (255, 200, 90))
        for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1),
                       (1, 1), (-1, -1), (1, -1), (-1, 1)]:
            cv.line(x + ex, y + ey, x + ex + dx * (r + 7),
                    y + ey + dy * (r + 7), BLAST, 2)
    # smoke puffs drifting above the bursts
    for sx, sy, r in [(150, 88, 9), (168, 78, 11), (288, 96, 8), (306, 88, 10)]:
        cv.circle(x + sx, y + sy, r, SMOKE)


def draw_cop31(cv, x, y, w, h):
    """A globe and a rising thermometer: the climate story."""
    cv.fill_rect(x, y, w, h, SKY)
    cx, cy, r = x + 70, y + h // 2, 24
    cv.circle(cx, cy, r, GLOBE)
    # landmasses (simple blobs on the globe)
    cv.circle(cx - 8, cy - 8, 7, LAND)
    cv.circle(cx + 9, cy + 6, 8, LAND)
    cv.circle(cx + 2, cy - 14, 4, LAND)
    cv.circle(cx - 14, cy + 10, 4, LAND)
    # latitude lines across the globe
    cv.line(cx - r + 3, cy - 8, cx + r - 3, cy - 8, (200, 220, 235), 1)
    cv.line(cx - r + 3, cy + 8, cx + r - 3, cy + 8, (200, 220, 235), 1)
    # thermometer, right of the globe
    tx = x + 150
    cv.fill_rect(tx, y + 8, 10, h - 20, (255, 255, 255))
    cv.fill_rect(tx + 1, y + 9, 8, h - 22, RED)
    cv.circle(tx + 5, y + h - 12, 8, RED)
    for ty in range(y + 10, y + h - 14, 8):
        cv.line(tx + 10, ty, tx + 16, ty, INK, 1)
    # rising sun with rays, far right
    sx, sy = x + w - 70, y + h // 2
    cv.circle(sx, sy, 15, SUN)
    for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1),
                   (1, 1), (-1, -1), (1, -1), (-1, 1)]:
        cv.line(sx + dx * 18, sy + dy * 18, sx + dx * 24, sy + dy * 24, SUN, 2)
    # ground line
    cv.fill_rect(x, y + h - 6, w, 2, INK)


def draw_summit(cv, x, y, w, h):
    """Three flags on poles: the trilateral summit."""
    cv.fill_rect(x, y, w, h, SKY)
    # flag geometry: each flag 110 wide, 34 tall, pole 48 tall
    pole_top = y + 4
    pole_bot = y + h - 6
    flags = [
        ("us", x + 20),
        ("cn", x + 181),
        ("ru", x + 342),
    ]
    for kind, fx in flags:
        cv.fill_rect(fx - 3, pole_top, 3, pole_bot - pole_top, INK)
        fy = pole_top + 2
        if kind == "us":
            # red and white stripes with a blue canton
            for i in range(6):
                cv.fill_rect(fx, fy + i * 6, 110, 3,
                             (178, 34, 34) if i % 2 == 0 else (255, 255, 255))
            cv.fill_rect(fx, fy, 44, 18, (30, 60, 120))
            cv.fill_rect(fx + 8, fy + 5, 3, 3, (255, 255, 255))
            cv.fill_rect(fx + 24, fy + 5, 3, 3, (255, 255, 255))
            cv.fill_rect(fx + 8, fy + 11, 3, 3, (255, 255, 255))
            cv.fill_rect(fx + 24, fy + 11, 3, 3, (255, 255, 255))
        elif kind == "cn":
            cv.fill_rect(fx, fy, 110, 34, (222, 41, 16))
            cv.circle(fx + 18, fy + 12, 6, (255, 222, 0))
            cv.circle(fx + 34, fy + 6, 2, (255, 222, 0))
            cv.circle(fx + 40, fy + 12, 2, (255, 222, 0))
            cv.circle(fx + 34, fy + 18, 2, (255, 222, 0))
        else:
            cv.fill_rect(fx, fy, 110, 12, (255, 255, 255))
            cv.fill_rect(fx, fy + 12, 110, 11, (30, 80, 180))
            cv.fill_rect(fx, fy + 23, 110, 11, (200, 30, 30))
    cv.fill_rect(x, pole_bot, w, 2, INK)


def draw_anthropic(cv, x, y, w, h):
    """A steep rising stock chart: the record IPO."""
    cv.fill_rect(x, y, w, h, (255, 255, 255))
    # grid
    for gy in range(y + 8, y + h - 8, 12):
        cv.line(x + 8, gy, x + w - 8, gy, (228, 228, 228), 1)
    for gx in range(x + 8, x + w - 8, 36):
        cv.line(gx, y + 8, gx, y + h - 8, (228, 228, 228), 1)
    # candlestick bars (small, rising)
    bars = [(30, 40, 8), (80, 34, 10), (130, 28, 9), (180, 22, 11),
            (230, 16, 10), (280, 12, 12)]
    for bx, bh, bw in bars:
        cv.fill_rect(x + bx, y + h - 12 - bh, bw, bh, (150, 190, 170))
    # the steep rising line with an arrowhead
    pts = [(16, h - 16), (90, h - 26), (170, h - 30), (250, h - 44),
           (330, h - 46), (400, h - 52), (448, 12)]
    for (ax, ay), (bx, by) in zip(pts, pts[1:]):
        cv.line(x + ax, y + ay, x + bx, y + by, CHART, 4)
    ax, ay = x + 448, y + 12
    cv.line(ax, ay, ax - 14, ay + 2, CHART, 4)
    cv.line(ax, ay, ax - 2, ay + 14, CHART, 4)


def draw_icj(cv, x, y, w, h):
    """A courthouse facade: the world court."""
    cv.fill_rect(x, y, w, h, SKY)
    cx = x + w // 2
    # pediment (triangle) and entablature
    cv.triangle([(cx - 130, y + 18), (cx + 130, y + 18), (cx, y + 2)], STONE)
    cv.fill_rect(cx - 140, y + 18, 280, 6, STONE)
    # four columns
    for i in range(4):
        colx = cx - 118 + i * 72
        cv.fill_rect(colx, y + 24, 16, h - 34, STONE)
        cv.fill_rect(colx - 3, y + 24, 22, 4, STONE)
        cv.fill_rect(colx - 3, y + h - 14, 22, 4, STONE)
    # steps
    cv.fill_rect(cx - 150, y + h - 10, 300, 3, STONE)
    cv.fill_rect(cx - 160, y + h - 6, 320, 3, STONE)


# ---------------------------------------------------------------------------
# Front-page layout
# ---------------------------------------------------------------------------
W, H = 1024, 1024
MARGIN = 28
CONTENT_W = W - 2 * MARGIN  # 968

LEAD_HEADLINE = ["RUSSIA BLITZES KYIV HOURS", "AFTER PEACE SUMMIT"]
LEAD_SUMMARY = (
    "110+ missiles and 400 drones hit Kyiv overnight \u2014 nine killed, "
    "three Dnipro bridges damaged \u2014 hours after Putin met Trump and "
    "Xi in Shenzhen."
)

STORIES = [
    dict(kicker="CLIMATE",
         headline="COP31 DRAFT DROPS FOSSIL FUELS",
         headline_lines=["COP31 DRAFT DROPS", "FOSSIL FUELS"],
         summary=("Antalya talks spill into overtime as the draft strips "
                  "fossil-fuel phase-out language and the $120bn finance "
                  "target."),
         draw=draw_cop31),
    dict(kicker="DIPLOMACY",
         headline="TRUMP, XI, PUTIN: 'NUCLEAR WAR MUST NEVER BE FOUGHT'",
         summary=("First trilateral summit in Shenzhen ends with a "
                  "four-point declaration on nuclear risks, energy "
                  "and UN reform."),
         draw=draw_summit),
    dict(kicker="MARKETS",
         headline="ANTHROPIC SOARS 17% IN RECORD $81BN DEBUT",
         summary=("Claude maker opens at $111.50 from an $83 IPO price "
                  "and closes up 17% \u2014 the largest IPO ever \u2014 as "
                  "the Nasdaq falls 2.3%."),
         draw=draw_anthropic),
    dict(kicker="JUSTICE",
         headline="WORLD COURT: MYANMAR COMMITTED GENOCIDE",
         summary=("In a first, the ICJ holds a state guilty of genocide; "
                  "Myanmar calls it 'unfair' as the UN chief visits "
                  "Rohingya camps."),
         draw=draw_icj),
]


def build_front_page():
    cv = Canvas(W, H, PAPER)

    # --- masthead ------------------------------------------------------
    draw_centered(cv, 24, "THE WORLD", 12, INK)
    draw_centered(cv, 124, "FRIDAY 20 NOVEMBER 2026", 3, INK)
    cv.fill_rect(MARGIN, 156, CONTENT_W, 3, INK)   # thick rule
    cv.fill_rect(MARGIN, 163, CONTENT_W, 1, INK)   # thin rule

    # --- lead story ----------------------------------------------------
    lx, ly = MARGIN, 176
    draw_text(cv, lx, ly + 6, "WAR IN UKRAINE", 2, RED)
    hy = ly + 28
    for i, line in enumerate(LEAD_HEADLINE):
        draw_text(cv, lx, hy + i * 34, line, 4, INK)
    ill_y = ly + 102
    ill_h = 150
    draw_kyiv(cv, lx, ill_y, 400, ill_h)
    # lead summary, right of the illustration
    sum_x = lx + 424
    sum_w = CONTENT_W - 424
    lines = wrap_text(LEAD_SUMMARY, sum_w, 3)
    for i, line in enumerate(lines):
        draw_text(cv, sum_x, ill_y + 4 + i * 26, line, 3, INK)

    # --- divider -------------------------------------------------------
    cv.fill_rect(MARGIN, 448, CONTENT_W, 1, INK)

    # --- 2x2 grid ------------------------------------------------------
    cell_w = (CONTENT_W - 24) // 2   # 472
    cell_h = 266
    grid_y = 458
    for idx, st in enumerate(STORIES):
        col, row = idx % 2, idx // 2
        cx = MARGIN + col * (cell_w + 24)
        cy = grid_y + row * (cell_h + 10)
        # kicker
        draw_text(cv, cx, cy + 6, st["kicker"], 2, RED)
        # headline, wrapped to two balanced lines
        hlines = st.get("headline_lines") or wrap_text(st["headline"], cell_w, 3)
        for i, line in enumerate(hlines):
            draw_text(cv, cx, cy + 28 + i * 26, line, 3, INK)
        # illustration band
        iy = cy + 88
        st["draw"](cv, cx, iy, cell_w, 56)
        # summary, wrapped; must fit in the remaining space
        slines = wrap_text(st["summary"], cell_w, 3)
        for i, line in enumerate(slines):
            draw_text(cv, cx, iy + 62 + i * 23, line, 3, INK)

    return cv


def main():
    out_dir = os.path.dirname(os.path.abspath(__file__))
    out_path = os.path.join(out_dir, "entry.png")
    cv = build_front_page()
    with open(out_path, "wb") as f:
        f.write(cv.png_bytes())
    print("wrote %s (%dx%d)" % (out_path, W, H))


if __name__ == "__main__":
    main()
