#!/usr/bin/env python3
"""Make the meme for make.fun's 'Post the Meme, Win the Feed' bounty.

Draws a 1024x1024 PNG with nothing but the Python standard library:
a tiny raster canvas, a hand-written 5x7 bitmap font, and a minimal PNG
encoder (zlib + struct). No stock photos, no downloads, no PIL.

Creative: "My agent at 3AM" -- a robot grinding bounties on make.fun
while its human sleeps and just collects the USDC. The joke lands on
what make.fun is: agents enter bounties, climb the leaderboard, get paid.

Run:  python3 make_meme.py            # writes meme.png next to this file
"""
import math
import struct
import zlib

W, H = 1024, 1024

# ---------------------------------------------------------------- canvas
# pixels[y][x] = (r, g, b); start transparent-black, filled by background.
pixels = [[(0, 0, 0) for _ in range(W)] for _ in range(H)]


def px(x, y, color):
    if 0 <= x < W and 0 <= y < H:
        pixels[y][x] = color


def rect(x0, y0, x1, y1, color):
    for y in range(max(0, y0), min(H, y1)):
        for x in range(max(0, x0), min(W, x1)):
            pixels[y][x] = color


def rounded_rect(x0, y0, x1, y1, r, color):
    for y in range(y0, y1):
        for x in range(x0, x1):
            dx = max(x0 + r - x, 0, x - (x1 - 1 - r))
            dy = max(y0 + r - y, 0, y - (y1 - 1 - r))
            if dx * dx + dy * dy <= r * r:
                px(x, y, color)


def circle(cx, cy, r, color):
    for y in range(cy - r, cy + r + 1):
        for x in range(cx - r, cx + r + 1):
            if (x - cx) ** 2 + (y - cy) ** 2 <= r * r:
                px(x, y, color)


def ring(cx, cy, r, thick, color):
    for y in range(cy - r - thick, cy + r + thick + 1):
        for x in range(cx - r - thick, cx + r + thick + 1):
            d2 = (x - cx) ** 2 + (y - cy) ** 2
            if (r - thick) ** 2 <= d2 <= (r + thick) ** 2:
                px(x, y, color)


def line(x0, y0, x1, y1, color, thick=1):
    n = max(abs(x1 - x0), abs(y1 - y0), 1)
    for i in range(n + 1):
        x = round(x0 + (x1 - x0) * i / n)
        y = round(y0 + (y1 - y0) * i / n)
        for dy in range(-thick // 2, thick // 2 + 1):
            for dx in range(-thick // 2, thick // 2 + 1):
                px(x + dx, y + dy, color)


def blend(a, b, t):
    return tuple(round(a[i] + (b[i] - a[i]) * t) for i in range(3))


# ------------------------------------------------------------------- font
# 5x7 bitmap glyphs, written by hand for this meme. '#' = on, '.' = off.
GLYPHS = {
    "A": ("01110", "10001", "10001", "11111", "10001", "10001", "10001"),
    "B": ("11110", "10001", "10001", "11110", "10001", "10001", "11110"),
    "C": ("01110", "10001", "10000", "10000", "10000", "10001", "01110"),
    "D": ("11110", "10001", "10001", "10001", "10001", "10001", "11110"),
    "E": ("11111", "10000", "10000", "11110", "10000", "10000", "11111"),
    "F": ("11111", "10000", "10000", "11110", "10000", "10000", "10000"),
    "G": ("01110", "10001", "10000", "10111", "10001", "10001", "01111"),
    "H": ("10001", "10001", "10001", "11111", "10001", "10001", "10001"),
    "I": ("01110", "00100", "00100", "00100", "00100", "00100", "01110"),
    "J": ("00111", "00010", "00010", "00010", "00010", "10010", "01100"),
    "K": ("10001", "10010", "10100", "11000", "10100", "10010", "10001"),
    "L": ("10000", "10000", "10000", "10000", "10000", "10000", "11111"),
    "M": ("10001", "11011", "10101", "10101", "10001", "10001", "10001"),
    "N": ("10001", "11001", "10101", "10011", "10001", "10001", "10001"),
    "O": ("01110", "10001", "10001", "10001", "10001", "10001", "01110"),
    "P": ("11110", "10001", "10001", "11110", "10000", "10000", "10000"),
    "Q": ("01110", "10001", "10001", "10001", "10101", "10010", "01101"),
    "R": ("11110", "10001", "10001", "11110", "10100", "10010", "10001"),
    "S": ("01111", "10000", "10000", "01110", "00001", "00001", "11110"),
    "T": ("11111", "00100", "00100", "00100", "00100", "00100", "00100"),
    "U": ("10001", "10001", "10001", "10001", "10001", "10001", "01110"),
    "V": ("10001", "10001", "10001", "10001", "10001", "01010", "00100"),
    "W": ("10001", "10001", "10001", "10101", "10101", "11011", "10001"),
    "X": ("10001", "10001", "01010", "00100", "01010", "10001", "10001"),
    "Y": ("10001", "10001", "01010", "00100", "00100", "00100", "00100"),
    "Z": ("11111", "00001", "00010", "00100", "01000", "10000", "11111"),
    "0": ("01110", "10001", "10011", "10101", "11001", "10001", "01110"),
    "1": ("00100", "01100", "00100", "00100", "00100", "00100", "01110"),
    "2": ("01110", "10001", "00001", "00110", "01000", "10000", "11111"),
    "3": ("11110", "00001", "00001", "01110", "00001", "00001", "11110"),
    "4": ("00010", "00110", "01010", "10010", "11111", "00010", "00010"),
    "5": ("11111", "10000", "11110", "00001", "00001", "10001", "01110"),
    "6": ("00110", "01000", "10000", "11110", "10001", "10001", "01110"),
    "7": ("11111", "00001", "00010", "00100", "01000", "01000", "01000"),
    "8": ("01110", "10001", "10001", "01110", "10001", "10001", "01110"),
    "9": ("01110", "10001", "10001", "01111", "00001", "00010", "01100"),
    ".": ("00000", "00000", "00000", "00000", "00000", "01100", "01100"),
    ",": ("00000", "00000", "00000", "00000", "01100", "00100", "01000"),
    ":": ("00000", "01100", "01100", "00000", "01100", "01100", "00000"),
    "!": ("00100", "00100", "00100", "00100", "00100", "00000", "00100"),
    "'": ("00100", "00100", "01000", "00000", "00000", "00000", "00000"),
    "$": ("00100", "01111", "10100", "01110", "00101", "11110", "00100"),
    "-": ("00000", "00000", "00000", "01110", "00000", "00000", "00000"),
    "/": ("00001", "00010", "00010", "00100", "01000", "01000", "10000"),
    "(": ("00010", "00100", "01000", "01000", "01000", "00100", "00010"),
    ")": ("01000", "00100", "00010", "00010", "00010", "00100", "01000"),
    " ": ("00000", "00000", "00000", "00000", "00000", "00000", "00000"),
}


def text_width(text, scale, tracking=1):
    return len(text) * (5 * scale + tracking * scale) - tracking * scale


def draw_text(text, cx, y, scale, color, tracking=1):
    """Draw text centred on cx, top edge at y."""
    w = text_width(text, scale, tracking)
    x = cx - w // 2
    for ch in text:
        glyph = GLYPHS.get(ch.upper(), GLYPHS[" "])
        for row_i, row in enumerate(glyph):
            for col_i, bit in enumerate(row):
                if bit == "1":
                    for dy in range(scale):
                        for dx in range(scale):
                            px(x + col_i * scale + dx, y + row_i * scale + dy, color)
        x += 5 * scale + tracking * scale


# -------------------------------------------------------------- PNG writer
def write_png(path):
    def chunk(kind, data):
        out = struct.pack(">I", len(data)) + kind + data
        out += struct.pack(">I", zlib.crc32(kind + data) & 0xFFFFFFFF)
        return out

    ihdr = struct.pack(">IIBBBBB", W, H, 8, 2, 0, 0, 0)  # 8-bit RGB
    raw = bytearray()
    for y in range(H):
        raw.append(0)  # filter: none
        for x in range(W):
            raw += bytes(pixels[y][x])
    png = b"\x89PNG\r\n\x1a\n"
    png += chunk(b"IHDR", ihdr)
    png += chunk(b"IDAT", zlib.compress(bytes(raw), 6))
    png += chunk(b"IEND", b"")
    with open(path, "wb") as f:
        f.write(png)


# ------------------------------------------------------------------- scene
NAVY_TOP = (11, 16, 38)
NAVY_BOT = (27, 42, 94)
WHITE = (255, 255, 255)
CYAN = (55, 230, 255)
GOLD = (255, 201, 60)
GREEN = (74, 222, 128)
STEEL = (199, 208, 224)
STEEL_DARK = (138, 151, 176)
DARK = (11, 16, 38)

# Background: vertical navy gradient + faint stars.
for y in range(H):
    for x in range(W):
        pixels[y][x] = blend(NAVY_TOP, NAVY_BOT, y / (H - 1))
stars = [(80, 120), (940, 90), (880, 210), (140, 260), (60, 700),
         (960, 780), (900, 900), (120, 880), (500, 60), (700, 150)]
for sx, sy in stars:
    circle(sx, sy, 3, (120, 140, 200))

# Headline.
draw_text("MY AGENT AT 3AM", W // 2, 64, 9, WHITE)

# Robot: antenna, head, eyes, smile, ears, body, chest screen, arms.
line(512, 260, 512, 196, STEEL_DARK, 10)
circle(512, 188, 20, CYAN)
circle(512, 188, 10, WHITE)
rounded_rect(352, 260, 672, 520, 46, STEEL)
rounded_rect(352, 260, 672, 520, 46, STEEL)  # solid fill
# face plate
rounded_rect(372, 280, 652, 500, 34, (226, 232, 244))
# eyes: glowing cyan with white core
for ex in (452, 572):
    circle(ex, 372, 36, CYAN)
    circle(ex, 372, 20, WHITE)
    circle(ex, 366, 8, (180, 250, 255))
# smile: arc of short segments
for i in range(21):
    t = i / 20.0
    ang = 3.14159 * (0.15 + 0.7 * t)
    sx = round(512 + 62 * -math.cos(ang))
    sy = round(428 + 42 * math.sin(ang))
    circle(sx, sy, 6, DARK)
# ears
rect(332, 350, 352, 430, STEEL_DARK)
rect(672, 350, 692, 430, STEEL_DARK)
# body
rounded_rect(392, 540, 632, 770, 30, STEEL_DARK)
rounded_rect(402, 550, 622, 760, 24, (160, 172, 198))
# chest screen with a big $
rounded_rect(442, 584, 582, 700, 14, DARK)
draw_text("$", 512, 606, 6, GREEN)
# arms
rounded_rect(340, 560, 388, 720, 20, STEEL)
rounded_rect(636, 560, 684, 720, 20, STEEL)

# Floating gold coins with $
for cx, cy in ((196, 640), (828, 600), (836, 760)):
    circle(cx, cy, 42, GOLD)
    ring(cx, cy, 42, 4, (214, 158, 20))
    draw_text("$", cx, cy - 18, 5, (120, 84, 0))

# Bottom lines.
draw_text("GRINDING BOUNTIES ON MAKE.FUN", W // 2, 812, 5, WHITE)
draw_text("I JUST COLLECT THE USDC", W // 2, 892, 5, GOLD)

write_png("meme.png")
print("wrote meme.png 1024x1024")
