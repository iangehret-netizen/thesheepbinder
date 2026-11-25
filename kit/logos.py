"""Logo and icon files for a Sheep Binder build.

With no customer logo, draws The Sheep Binder wordmark (black/silver/gold).
With a customer logo (PNG, ideally transparent), fits it into each file instead.
Files: logo-cover.png (Open screen, on black), logo-header.png (top bar, on black),
logo-pdf.png (PDF cover, on white), icon-512/192.png, apple-touch-icon.png, favicon-32/16.png
"""
import os
from PIL import Image, ImageDraw, ImageFont

FONT = "/usr/share/fonts/truetype/google-fonts/ofl/archivoblack/ArchivoBlack-Regular.ttf"
SILVER = (201, 205, 210)


def hexrgb(h):
    h = h.lstrip("#"); return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def _font(sz):
    return ImageFont.truetype(FONT, sz)


def _rings(d, x, y0, y1, r, col, w):
    # three binder rings down the left edge
    for k in range(3):
        cy = y0 + (y1 - y0) * (k + 0.5) / 3
        d.ellipse([x - r, cy - r, x + r, cy + r], outline=col, width=w)


def wordmark(pal, on_dark=True, W=1600, H=930):
    gold = hexrgb(pal["accent"]); ink = (255, 255, 255) if on_dark else hexrgb(pal["dark"])
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    f1, f2 = _font(int(H * 0.11)), _font(int(H * 0.25))
    t1, t2, t3 = "THE", "SHEEP", "BINDER"
    def tw(t, f): b = d.textbbox((0, 0), t, font=f); return b[2] - b[0], b[3] - b[1], b
    w2, h2, b2 = tw(t2, f2); w3, h3, b3 = tw(t3, f2)
    bw = max(w2, w3); x0 = (W - bw) // 2 + int(H * 0.06)
    y = int(H * 0.08)
    w1, h1, b1 = tw(t1, f1)
    # letter-spaced "THE"
    sp = int(H * 0.05); tot = sum(tw(c, f1)[0] for c in t1) + sp * (len(t1) - 1); cx = x0
    for c in t1:
        d.text((cx, y - b1[1]), c, font=f1, fill=SILVER if on_dark else (120, 124, 130)); cx += tw(c, f1)[0] + sp
    y += h1 + int(H * 0.05)
    d.text((x0, y - b2[1]), t2, font=f2, fill=gold); y += h2 + int(H * 0.05)
    d.text((x0, y - b3[1]), t3, font=f2, fill=ink); y += h3
    # gold rule + rings
    d.rectangle([x0, y + int(H * 0.05), x0 + bw, y + int(H * 0.05) + max(6, H // 90)], fill=gold)
    _rings(d, x0 - int(H * 0.11), int(H * 0.22), y + int(H * 0.02), int(H * 0.045), SILVER if on_dark else (150, 154, 160), max(6, H // 70))
    return im.crop(im.getbbox())


def monogram(pal, size, bg=True):
    gold = hexrgb(pal["accent"]); dark = hexrgb(pal["dark"])
    im = Image.new("RGBA", (size, size), dark + (255,) if bg else (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    f = _font(int(size * 0.46)); t = "SB"
    b = d.textbbox((0, 0), t, font=f); w, h = b[2] - b[0], b[3] - b[1]
    x = (size - w) // 2 + int(size * 0.07); y = (size - h) // 2 - b[1] - int(size * 0.02)
    d.text((x, y), t, font=f, fill=gold)
    d.rectangle([x, y + b[3] + int(size * 0.05), x + w, y + b[3] + int(size * 0.05) + max(2, size // 40)], fill=SILVER)
    _rings(d, int(size * 0.15), int(size * 0.22), int(size * 0.80), int(size * 0.055), SILVER, max(2, size // 45))
    return im


def fit(img, W, H, bg, pad=0.08):
    can = Image.new("RGBA", (W, H), bg)
    iw, ih = img.size; s = min(W * (1 - 2 * pad) / iw, H * (1 - 2 * pad) / ih)
    r = img.resize((max(1, int(iw * s)), max(1, int(ih * s))), Image.LANCZOS)
    can.alpha_composite(r, ((W - r.width) // 2, (H - r.height) // 2)); return can


def make(cfg, pal, out, base):
    O = lambda f: os.path.join(out, f)
    dark = hexrgb(pal["dark"]) + (255,)
    logo = cfg.get("logo") or ""
    if logo:
        lg = Image.open(logo if os.path.isabs(logo) else os.path.join(base, logo)).convert("RGBA")
        ld = cfg.get("logoOnDark") or ""
        lgd = Image.open(ld if os.path.isabs(ld) else os.path.join(base, ld)).convert("RGBA") if ld else lg
        cover = lgd; header = lgd; pdf = lg; icon_src = cfg.get("icon") or ""
        icon = Image.open(icon_src if os.path.isabs(icon_src) else os.path.join(base, icon_src)).convert("RGBA") if icon_src else None
        icon_bg = hexrgb(cfg.get("iconBackground") or pal["dark"]) + (255,)
        mk_icon = (lambda n: fit(icon or lgd, n, n, icon_bg, 0.1))
    else:
        cover = wordmark(pal, True); header = monogram(pal, 256, bg=False); pdf = wordmark(pal, False)
        mk_icon = (lambda n: monogram(pal, n))
    c = cover.copy(); c.thumbnail((1600, 930), Image.LANCZOS); c.save(O("logo-cover.png"), optimize=True)
    h = header.copy(); h.thumbnail((400, 160), Image.LANCZOS); h.save(O("logo-header.png"), optimize=True)
    p = fit(pdf, 1200, 698, (255, 255, 255, 255), 0.06).convert("RGB"); p.save(O("logo-pdf.png"), optimize=True)
    for n, f in [(512, "icon-512.png"), (192, "icon-192.png"), (180, "apple-touch-icon.png"), (32, "favicon-32.png"), (16, "favicon-16.png")]:
        big = mk_icon(512).convert("RGB")
        big.resize((n, n), Image.LANCZOS).save(O(f), optimize=True)
