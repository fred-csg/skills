# Folha de paletas: mesma cena em todas as cores.  python paletas.py roteiro.py saida.jpg 3.6,15.6
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import dx
from render import carrega
from PIL import Image, ImageDraw
rot, out = sys.argv[1], sys.argv[2]
ts = [float(x) for x in (sys.argv[3] if len(sys.argv) > 3 else "3.6").split(",")]
R = carrega(rot)
nomes = [n for n in dx.PALETAS if n != "referencia"]
tw_, th_ = 270, 480
sheet = Image.new("RGB", (len(nomes) * tw_, len(ts) * th_ + 40), (24, 24, 24)); d = ImageDraw.Draw(sheet)
for i, n in enumerate(nomes):
    dx.set_paleta(n)
    d.text((i * tw_ + 10, 12), n.upper(), fill=dx.P["acento"], font=dx.font("bold", 20))
    for j, t in enumerate(ts):
        sheet.paste(dx.quadro(t, int(t * 30), R).resize((tw_, th_), Image.LANCZOS), (i * tw_, 40 + j * th_))
sheet.save(out, quality=92); print("ok", out)
