# Gera safe_zone_guia.png (diagrama explicado) e o overlay. Rodar uma vez quando as medidas mudarem.
import os
from PIL import Image, ImageDraw
from safe_zone import W, H, TOPO, BASE, LAT, BOT_X, BOT_Y, SLOTS, overlay, _fonte
AQUI = os.path.dirname(os.path.abspath(__file__))
overlay().save(os.path.join(AQUI, "safe_zone_overlay_1080x1920.png"))
im = Image.new("RGBA", (W, H), (34, 38, 48, 255)); d = ImageDraw.Draw(im)
for x in range(0, W, 60): d.line([(x, 0), (x, H)], fill=(44, 50, 62), width=2)
for y in range(0, H, 60): d.line([(0, y), (W, y)], fill=(44, 50, 62), width=2)
cores = {"titulo": (198, 244, 50), "heroi": (90, 170, 255), "legenda": (255, 200, 60)}
nomes = {"titulo": "TÍTULO  y 250–430", "heroi": "HERÓI  y 430–1150", "legenda": "LEGENDA  y 1150–1470"}
for k, (x0, y0, x1, y1) in SLOTS.items():
    c = cores[k]; L = Image.new("RGBA", (W, H), (0, 0, 0, 0)); dl = ImageDraw.Draw(L)
    dl.rounded_rectangle([x0 + 12, y0 + 6, x1 - 12, y1 - 6], radius=26, outline=c + (255,), width=5, fill=c + (45,))
    im.alpha_composite(L); d = ImageDraw.Draw(im)
    d.text(((x0 + x1) / 2, (y0 + y1) / 2), nomes[k], font=_fonte(44), fill=c + (255,), anchor="mm", stroke_width=3, stroke_fill=(0, 0, 0, 255))
im.alpha_composite(overlay()); d = ImageDraw.Draw(im)
k = dict(fill=(255, 255, 255, 255), stroke_width=3, stroke_fill=(0, 0, 0, 255))
d.text((LAT + 10, TOPO + 8), f"x {LAT}", font=_fonte(26), **k)
d.text((BOT_X - 120, BOT_Y - 40), f"x {BOT_X} / y {BOT_Y}", font=_fonte(26), **k)
d.text((W / 2, H - 120), "fundo e vídeo podem passar das linhas — só o essencial fica dentro", font=_fonte(30), anchor="mm", **k)
im.convert("RGB").save(os.path.join(AQUI, "safe_zone_guia.png"))
print("ok")
