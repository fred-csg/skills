# Folha de paletas: mesma cena em todas as cores.  python paletas.py roteiro.py saida.jpg 2.6,11.8
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ct
from render import carrega
from PIL import Image, ImageDraw
rot, out = sys.argv[1], sys.argv[2]
ts = [float(x) for x in (sys.argv[3] if len(sys.argv) > 3 else "2.6").split(",")]
R = carrega(rot)
nomes = list(ct.PALETAS)
tw_, th_ = 270, 480
sheet = Image.new("RGB", (len(nomes) * tw_, len(ts) * th_ + 40), (24, 24, 24)); d = ImageDraw.Draw(sheet)
for i, n in enumerate(nomes):
    ct.set_paleta(n)
    d.text((i * tw_ + 10, 12), n.upper(), fill=ct.C["claro"], font=ct.font("bold", 20))
    for j, t in enumerate(ts):
        sheet.paste(ct.quadro(t, int(t * 30), R).resize((tw_, th_), Image.LANCZOS), (i * tw_, 40 + j * th_))
sheet.save(out, quality=92); print("ok", out)
