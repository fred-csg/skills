import sys as _s, os as _o
_s.path.insert(0, _o.path.dirname(_o.path.dirname(_o.path.abspath(__file__))))  # scripts/ (ambiente.py)
import ambiente
# capa.py <imagem_ia> <saida.jpg> "<TÍTULO LINHA 1|LINHA 2>" "<etiqueta>" <cor>
# Capa 1080x1920: arte por IA + título com contorno escuro + pílula; título dentro do recorte 3:4 do grid (y 240..1680).
import sys, os
from PIL import Image, ImageDraw, ImageFont, ImageFilter
src, out, title, tag, col = sys.argv[1:6]
COL = dict(orange=(240, 127, 46), red=(229, 72, 77), purple=(123, 91, 214), blue=(47, 124, 246), green=(37, 165, 95),
           yellow=(242, 179, 61), teal=(48, 170, 160), pink=(226, 92, 140))
W, H = 1080, 1920
im = Image.open(src).convert("RGB")
s = max(W / im.width, H / im.height)
im = im.resize((int(im.width * s + 0.5), int(im.height * s + 0.5)), Image.LANCZOS)
x0 = (im.width - W) // 2; y0 = (im.height - H) // 2
im = im.crop((x0, y0, x0 + W, y0 + H)).convert("RGBA")
# leve degradê creme no topo pra destacar o título
g = Image.new("L", (1, H))
for y in range(H): g.putpixel((0, y), int(150 * max(0, 1 - y / 900)))
veil = Image.new("RGBA", (W, H), (246, 241, 232, 255)); veil.putalpha(g.resize((W, H)))
im.alpha_composite(veil)
d = ImageDraw.Draw(im)
F = lambda n, s: ImageFont.truetype(ambiente.achar_fonte(n, "Poppins-Black.ttf", "ariblk.ttf", "Arial Black.ttf", "arialbd.ttf", "Arial Bold.ttf", "consolab.ttf", "Menlo.ttc"), s)
lines = title.split("|")
y = 330
for ln in lines:
    size = 118
    f = F("seguibl.ttf", size)
    while f.getlength(ln) > 900: size -= 4; f = F("seguibl.ttf", size)
    d.text((W / 2, y), ln, font=f, fill=(255, 255, 255), anchor="mm", stroke_width=12, stroke_fill=(30, 30, 34))
    y += int(size * 1.08)
ft = F("consolab.ttf", 40)
tw = ft.getlength(tag) + 60
y += 20
d.rounded_rectangle([W / 2 - tw / 2, y - 34, W / 2 + tw / 2, y + 34], radius=34, fill=COL[col] + (255,), outline=(30, 30, 34), width=5)
d.text((W / 2, y), tag, font=ft, fill=(255, 255, 255), anchor="mm")
im.convert("RGB").save(out, quality=92)
print(out)
