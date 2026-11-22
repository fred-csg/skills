# Esquadrão Voxel — texturas (PIL) pras telas, placas, letreiros e fundos do Blender.
# Rodar no Python normal ANTES do Blender:  python texturas.py   (o script do projeto chama estas funções)
# Tudo sai em PNG na pasta blender/tex do projeto.
import sys as _s, os as _o
_s.path.insert(0, _o.path.dirname(_o.path.dirname(_o.path.abspath(__file__))))
import ambiente
import os, math, random
from PIL import Image, ImageDraw, ImageFont, ImageFilter

# paleta da interface (mesma do hud.py)
INK, CREME, LIMA, CORAL, AZUL, ROXO, AMARELO, VERDE = "#16131F", "#FFF6E5", "#C6F432", "#FF6B5B", "#4C8DFF", "#8B6CFF", "#FFC83D", "#2FD27A"
FD = os.path.join(ambiente.SKILL, "assets", "fonts")
def F(nome, tam):
    p = {"titulo": "ArchivoBlack-Regular.ttf", "bold": "Poppins-Bold.ttf", "semi": "Poppins-SemiBold.ttf",
         "mono": "JetBrainsMono.ttf", "serif": "Fraunces.ttf"}[nome]
    f = ImageFont.truetype(os.path.join(FD, p), tam)
    if nome == "serif":
        try: f.set_variation_by_axes([48, 850, 100, 0])   # opsz, wght, SOFT (arredondada), WONK
        except Exception: pass
    return f
def texto(d, xy, s, font, fill, **kw):
    """d.text que desenha o ✓ como traço (as fontes não têm o glifo)."""
    x, y = xy; partes = s.split("✓")
    for i, p in enumerate(partes):
        if p: d.text((x, y), p, font=font, fill=fill, **kw); x += d.textlength(p, font=font)
        if i < len(partes) - 1:
            sz = font.size * 0.62; by = y + font.size * 0.28
            d.line([(x + sz * 0.1, by + sz * 0.5), (x + sz * 0.42, by + sz * 0.85), (x + sz * 1.0, by + sz * 0.05)], fill=fill, width=max(3, int(font.size * 0.14)), joint="curve")
            x += sz * 1.15
    return x
def tlen(d, s, font):
    return sum(d.textlength(p, font=font) for p in s.split("✓")) + s.count("✓") * font.size * 0.62 * 1.15
def rr(d, box, r, fill, outline=None, width=0): d.rounded_rectangle(box, r, fill=fill, outline=outline, width=width)
def ctext(d, xy, txt, font, fill):
    x, y = xy; b = d.textbbox((0, 0), txt, font=font); d.text((x - (b[2] - b[0]) / 2 - b[0], y - (b[3] - b[1]) / 2 - b[1]), txt, font=font, fill=fill)
def _out(img, path):
    os.makedirs(os.path.dirname(path), exist_ok=True); img.save(path); return path

def placa(path, topo, texto, cor=LIMA, w=720, h=420, cor_txt=INK, icone=None):
    """placa de cartão: faixa colorida em cima (rótulo pequeno) + texto grande."""
    im = Image.new("RGB", (w, h), CREME); d = ImageDraw.Draw(im)
    d.rectangle((0, 0, w, int(h * 0.26)), fill=cor)
    ctext(d, (w / 2, h * 0.13), topo.upper(), F("bold", int(h * 0.1)), cor_txt if cor in (LIMA, AMARELO, CREME) else "#FFFFFF")
    lines = texto.split("|"); fs = int(h * (0.24 if len(lines) == 1 else 0.17))
    for i, l in enumerate(lines):
        ctext(d, (w / 2, h * 0.62 + (i - (len(lines) - 1) / 2) * fs * 1.15), l, F("titulo", fs), INK)
    return _out(im, path)

def letreiro(path, texto, bg=CREME, fg=INK, w=900, h=200):
    im = Image.new("RGB", (w, h), bg); d = ImageDraw.Draw(im)
    ctext(d, (w / 2, h / 2), texto.upper(), F("titulo", int(h * 0.48)), fg)
    return _out(im, path)

def cidade(path, w=2000, h=1200, ceu=("#120F2E", "#3B1F5C", "#C2566A"), seed=3, janelas=("#FFD27A", "#FFE9B0", "#9FE7FF", "#FF9F7A")):
    """janelão da cidade à noite: céu em degradê + prédios com janelas acesas."""
    R = random.Random(seed)
    im = Image.new("RGB", (w, h)); d = ImageDraw.Draw(im)
    def hx(c): return tuple(int(c.lstrip("#")[i:i + 2], 16) for i in (0, 2, 4))
    a, b, c = map(hx, ceu)
    for y in range(h):
        k = y / h
        col = tuple(int(a[i] + (b[i] - a[i]) * (k / 0.6)) if k < 0.6 else int(b[i] + (c[i] - b[i]) * ((k - 0.6) / 0.4)) for i in range(3))
        d.line((0, y, w, y), fill=col)
    for _ in range(140):
        x, y = R.uniform(0, w), R.uniform(0, h * 0.5); r = R.choice((1, 1, 2))
        d.ellipse((x - r, y - r, x + r, y + r), fill=(255, 245, 230))
    for camada, (escuro, hmin, hmax) in enumerate((("#2A2450", 0.35, 0.6), ("#1B1738", 0.45, 0.85))):
        x = -20
        while x < w:
            bw = R.randint(110, 260); bh = int(h * R.uniform(hmin, hmax))
            d.rectangle((x, h - bh, x + bw, h), fill=escuro)
            for wy in range(h - bh + 24, h - 10, 34):
                for wx in range(x + 14, x + bw - 18, 28):
                    if R.random() < (0.45 if camada else 0.3):
                        d.rectangle((wx, wy, wx + 14, wy + 18), fill=R.choice(janelas))
            x += bw + R.randint(4, 30)
    return _out(im, path)

def _janela(d, w, h, titulo, fundo="#1D1B2A", barra="#2A2738"):
    rr(d, (0, 0, w - 1, h - 1), 26, fundo)
    d.rectangle((0, 0, w, 64), fill=barra)
    for i, c in enumerate(("#FF5F57", "#FEBC2E", "#28C840")): d.ellipse((22 + i * 34, 20, 46 + i * 34, 44), fill=c)
    ctext(d, (w / 2, 32), titulo, F("semi", 26), "#C9C4DA")

def terminal(path, titulo, linhas, w=1400, h=900, cores=None):
    """editor/terminal escuro com linhas de código (cada linha: texto ou (texto, cor))."""
    im = Image.new("RGB", (w, h)); d = ImageDraw.Draw(im); _janela(d, w, h, titulo)
    f = F("mono", 34)
    for i, l in enumerate(linhas):
        t, c = (l, "#E9E4F2") if isinstance(l, str) else l
        d.text((40, 100 + i * 52), f"{i + 1:>2}", font=f, fill="#5B5670")
        texto(d, (120, 100 + i * 52), t, f, c)
    return _out(im, path)

def doc(path, titulo, linhas, w=1100, h=1400, destaque=None):
    im = Image.new("RGB", (w, h), "#FFFDF7"); d = ImageDraw.Draw(im)
    d.rectangle((0, 0, w, 150), fill=INK); d.text((60, 42), titulo.upper(), font=F("titulo", 60), fill=LIMA)
    y = 220
    for i, l in enumerate(linhas):
        if destaque is not None and i == destaque: d.rectangle((50, y - 8, w - 50, y + 62), fill=LIMA)
        d.text((60, y), l, font=F("semi", 44), fill=INK); y += 86
    for k in range(6):
        d.rounded_rectangle((60, y + k * 60, 60 + random.Random(k).randint(500, 950), y + k * 60 + 22), 10, fill="#E3DDD0")
    return _out(im, path)

def grafico(path, titulo="EM ALTA", w=1400, h=900, cor=LIMA):
    im = Image.new("RGB", (w, h)); d = ImageDraw.Draw(im); _janela(d, w, h, titulo)
    for k in range(5): d.line((80, 200 + k * 140, w - 80, 200 + k * 140), fill="#2E2A40", width=3)
    pts = [(80 + i * (w - 160) / 9, 760 - (i ** 1.7) * 18 - random.Random(i).uniform(-30, 30)) for i in range(10)]
    d.line(pts, fill=cor, width=14, joint="curve")
    for p in pts[-1:]: d.ellipse((p[0] - 26, p[1] - 26, p[0] + 26, p[1] + 26), fill=cor)
    rr(d, (w - 470, 100, w - 80, 190), 20, cor); ctext(d, (w - 275, 145), "+ 380%", F("titulo", 52), INK)
    return _out(im, path)

def onda(path, titulo="LOCUÇÃO — voz.wav", w=1400, h=900, cor=CORAL):
    im = Image.new("RGB", (w, h)); d = ImageDraw.Draw(im); _janela(d, w, h, titulo)
    R = random.Random(5)
    for i in range(70):
        x = 80 + i * (w - 160) / 70; a = (math.sin(i * 0.35) ** 2 * 0.7 + 0.3) * R.uniform(0.4, 1) * 260
        d.rounded_rectangle((x, 470 - a, x + 10, 470 + a), 5, fill=cor)
    rr(d, (70, 100, 300, 170), 35, CORAL); ctext(d, (185, 135), "● REC", F("bold", 36), "#FFFFFF")
    return _out(im, path)

def timeline(path, titulo="EDIÇÃO — reel.mp4", w=1600, h=900):
    im = Image.new("RGB", (w, h)); d = ImageDraw.Draw(im); _janela(d, w, h, titulo)
    rr(d, (60, 90, w - 60, 470), 18, "#0F0D18")
    ctext(d, (w / 2, 280), "▶  PREVIEW", F("titulo", 70), "#3A3550")
    cores = [LIMA, AZUL, CORAL, ROXO, AMARELO]
    R = random.Random(2)
    for tr in range(4):
        y = 520 + tr * 82; x = 70
        d.text((70, y + 14), ["V2", "V1", "A1", "A2"][tr], font=F("bold", 30), fill="#8F89A8")
        x = 150
        while x < w - 80:
            cw = R.randint(80, 260)
            rr(d, (x, y, min(w - 80, x + cw), y + 62), 12, cores[(tr + int(x)) % 5] if tr < 2 else "#4C8DFF55" if False else ["#2FD27A", "#4C8DFF"][tr - 2])
            x += cw + 8
    d.line((620, 500, 620, 860), fill="#FF3B3B", width=6); d.polygon([(600, 494), (640, 494), (620, 520)], fill="#FF3B3B")
    return _out(im, path)

def agenda(path, titulo="AGENDA", w=1400, h=1000, dia=17, hora="18:00"):
    im = Image.new("RGB", (w, h), CREME); d = ImageDraw.Draw(im)
    d.rectangle((0, 0, w, 170), fill=VERDE); ctext(d, (w / 2, 85), titulo, F("titulo", 80), INK)
    cw, ch = (w - 120) / 7, (h - 260) / 5
    for i in range(35):
        x = 60 + (i % 7) * cw; y = 220 + (i // 7) * ch; n = i - 2
        if 1 <= n <= 31:
            hot = n == dia
            rr(d, (x + 6, y + 6, x + cw - 6, y + ch - 6), 16, LIMA if hot else "#EFE6D2")
            d.text((x + 20, y + 14), str(n), font=F("bold", 38), fill=INK)
            if hot: ctext(d, (x + cw / 2, y + ch * 0.66), hora, F("bold", 30), INK)
    return _out(im, path)

def cortica(path, w=1600, h=1000, notas=("REELS", "IA", "TREND", "GANCHO", "VIRAL", "CLAUDE")):
    R = random.Random(9)
    im = Image.new("RGB", (w, h), "#C89B62"); d = ImageDraw.Draw(im)
    for _ in range(3000):
        x, y = R.uniform(0, w), R.uniform(0, h); d.point((x, y), fill=R.choice(("#B5874F", "#D8AE76", "#A97B45")))
    cores = [LIMA, "#FFE27A", "#FF9FB5", "#9FD3FF", "#FFFFFF"]
    for i, n in enumerate(notas):
        x = 120 + (i % 3) * 480 + R.uniform(-30, 30); y = 120 + (i // 3) * 430 + R.uniform(-20, 20)
        nt = Image.new("RGBA", (360, 300), cores[i % len(cores)]); nd = ImageDraw.Draw(nt)
        ctext(nd, (180, 150), n, F("titulo", 64), INK)
        nt = nt.rotate(R.uniform(-7, 7), expand=True, resample=Image.BICUBIC)
        im.paste(nt, (int(x), int(y)), nt)
        d.ellipse((x + 160, y - 4, x + 196, y + 32), fill=CORAL)
    return _out(im, path)

def neon(path, texto, cor=LIMA, w=1400, h=500):
    """letreiro de neon com fundo transparente (usar com painel(alpha=True))."""
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    f = F("titulo", int(h * 0.55))
    rr(d, (30, 30, w - 30, h - 30), h // 2 - 30, None, cor, 18)
    ctext(d, (w / 2, h / 2), texto, f, cor)
    glow = im.filter(ImageFilter.GaussianBlur(18))
    out = Image.alpha_composite(glow, glow); out = Image.alpha_composite(out, im)
    core = Image.new("RGBA", (w, h), (0, 0, 0, 0)); cd = ImageDraw.Draw(core)
    ctext(cd, (w / 2, h / 2), texto, f, "#FFFFFF")
    core = core.filter(ImageFilter.GaussianBlur(2))
    out = Image.alpha_composite(out, Image.blend(Image.new("RGBA", (w, h), (0, 0, 0, 0)), core, 0.6))
    return _out(out, path)

def app(path, titulo, botao="APROVAR", cor=VERDE, w=1400, h=900, linhas=("Roteiro ✓", "Locução ✓", "Edição ✓", "Agendado ✓")):
    im = Image.new("RGB", (w, h)); d = ImageDraw.Draw(im); _janela(d, w, h, titulo)
    for i, l in enumerate(linhas):
        rr(d, (90, 120 + i * 120, w - 90, 210 + i * 120), 20, "#2A2738")
        texto(d, (130, 140 + i * 120), l, F("bold", 44), "#E9E4F2")
        d.ellipse((w - 190, 138 + i * 120, w - 130, 198 + i * 120), fill=VERDE)
    rr(d, (w / 2 - 300, h - 170, w / 2 + 300, h - 60), 55, cor); ctext(d, (w / 2, h - 115), botao, F("titulo", 56), INK)
    return _out(im, path)


def dia(path, w=2400, h=1000, seed=4, ceu=("#7CC4F2", "#BFE4F8", "#FBE9CF")):
    """janelão de dia: céu claro, nuvens fofas e prédios pastel ao longe."""
    R = random.Random(seed)
    im = Image.new("RGB", (w, h)); d = ImageDraw.Draw(im)
    def hx(c): return tuple(int(c.lstrip("#")[i:i + 2], 16) for i in (0, 2, 4))
    a, b, c = map(hx, ceu)
    for y in range(h):
        k = y / h
        col = tuple(int(a[i] + (b[i] - a[i]) * (k / 0.6)) if k < 0.6 else int(b[i] + (c[i] - b[i]) * ((k - 0.6) / 0.4)) for i in range(3))
        d.line((0, y, w, y), fill=col)
    for _ in range(9):
        cx, cy = R.uniform(0, w), R.uniform(80, h * 0.45); s = R.uniform(60, 120)
        for k in range(6):
            r = s * R.uniform(0.5, 1.0); x = cx + (k - 3) * s * 0.5
            d.ellipse((x - r, cy - r * 0.7, x + r, cy + r * 0.7), fill="#FFFFFF")
    cores = ["#F4B6A6", "#A9D6C8", "#F6D58E", "#B9B4E8", "#F2C6D6", "#9FCBE8"]
    x = -20
    while x < w:
        bw = R.randint(120, 260); bh = int(h * R.uniform(0.22, 0.5)); col = R.choice(cores)
        d.rectangle((x, h - bh, x + bw, h), fill=col)
        for wy in range(h - bh + 26, h - 10, 40):
            for wx in range(x + 16, x + bw - 20, 32):
                d.rectangle((wx, wy, wx + 16, wy + 22), fill="#FFFFFF" if R.random() < 0.5 else "#DDEFF8")
        x += bw + R.randint(6, 40)
    return _out(im, path)
