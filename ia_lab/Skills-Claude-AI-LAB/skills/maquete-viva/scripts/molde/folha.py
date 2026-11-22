import sys as _s, os as _o
_s.path.insert(0, _o.path.dirname(_o.path.dirname(_o.path.abspath(__file__))))  # scripts/ (ambiente.py)
import ambiente
# Folha de contato: python folha.py <dir> <out.jpg> [cols] [prefix]
import sys, os, glob
from PIL import Image, ImageDraw, ImageFont
d, out = sys.argv[1:3]
cols = int(sys.argv[3]) if len(sys.argv) > 3 else 6
pre = sys.argv[4] if len(sys.argv) > 4 else "f"
fs = sorted(glob.glob(os.path.join(d, pre + "*.png")))
w = 300; h = int(w * 16 / 9)
rows = (len(fs) + cols - 1) // cols
sheet = Image.new("RGB", (cols * w, rows * h), (40, 40, 40))
F = ImageFont.truetype(ambiente.achar_fonte("consolab.ttf", "Menlo.ttc", "courbd.ttf", "arialbd.ttf", "Arial Bold.ttf"), 22)
for i, p in enumerate(fs):
    im = Image.open(p).convert("RGB").resize((w, h))
    dr = ImageDraw.Draw(im)
    n = int("".join(c for c in os.path.basename(p) if c.isdigit()))
    dr.rectangle([0, 0, 110, 30], fill=(0, 0, 0)); dr.text((5, 4), f"{n/30:.1f}s", font=F, fill=(255, 255, 0))
    sheet.paste(im, ((i % cols) * w, (i // cols) * h))
sheet.save(out, quality=85)
print(out, len(fs))
