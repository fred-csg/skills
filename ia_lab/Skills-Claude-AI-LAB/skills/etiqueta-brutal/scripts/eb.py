# etiqueta-brutal · motor gráfico (PIL + numpy + ffmpeg)
# Estilo neo-brutalista: fundo creme, cartão de vídeo arredondado, etiquetas com contorno
# preto + sombra dura, palavra-chave destacada, blocos inclinados, selos, janelas de app.
import math, os, subprocess, numpy as np
from functools import lru_cache
from PIL import Image, ImageDraw, ImageFont, ImageFilter

import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ambiente import ffmpeg, achar_fonte
FFM = ffmpeg()
W, H, FPS = 1080, 1920, 30
K = 2  # supersampling dos sprites

# ---------------------------------------------------------------- paleta
CREME = (251, 244, 222); PAPEL = (255, 250, 236); TINTA = (20, 18, 16)
AMARELO = (255, 214, 58); VERMELHO = (236, 88, 60); AZUL = (60, 90, 240)
LILAS = (201, 170, 245); VERDE = (32, 78, 48); VERDE_OK = (88, 196, 120)
PESSEGO = (247, 222, 204); CINZA = (150, 146, 138)

# Cera Pro (paga) se estiver instalada; senão Poppins (grátis, se vier em assets/fonts); senão as do sistema.
FONTES = dict(
    black=("CeraPro-Black.otf", "Poppins-Black.ttf", "seguibl.ttf", "ariblk.ttf", "Arial Black.ttf"),
    bold=("CeraPro-Bold.otf", "Poppins-Bold.ttf", "segoeuib.ttf", "arialbd.ttf", "Arial Bold.ttf"),
    med=("CeraPro-Medium.otf", "Poppins-Medium.ttf", "seguisb.ttf", "arial.ttf", "Arial.ttf"),
    reg=("CeraPro-Regular.otf", "Poppins-Regular.ttf", "segoeui.ttf", "arial.ttf", "Arial.ttf"),
    serif=("georgia.ttf", "Georgia.ttf"), serif_i=("georgiai.ttf", "Georgia Italic.ttf"),
    mono=("CascadiaMono.ttf", "consola.ttf", "Menlo.ttc", "Courier New.ttf"),
    feio=("timesbd.ttf", "Times New Roman Bold.ttf", "Georgia Bold.ttf"))
@lru_cache(None)
def _fp(kind):
    p = achar_fonte(*FONTES[kind])
    if not p: raise FileNotFoundError(f"nenhuma fonte para '{kind}': {FONTES[kind]}")
    return p
@lru_cache(None)
def font(kind, size): return ImageFont.truetype(_fp(kind), int(size))

# ---------------------------------------------------------------- easing
def clamp(x, a=0., b=1.): return max(a, min(b, x))
def lin(t, a, b): return clamp((t - a) / (b - a)) if b > a else float(t >= a)
def eio(x): x = clamp(x); return x * x * (3 - 2 * x)
def eout(x): x = clamp(x); return 1 - (1 - x) ** 3
def ein(x): x = clamp(x); return x ** 3
def eback(x, s=1.9):
    x = clamp(x); x -= 1; return x * x * ((s + 1) * x + s) + 1
def mix(a, b, x): return a + (b - a) * x

# ---------------------------------------------------------------- canvas supersampled
class Cv:
    """Desenha em K× e entrega RGBA reduzido. Coordenadas sempre em px finais."""
    def __init__(s, w, h, pad=24):
        s.w, s.h, s.pad = int(w), int(h), pad
        s.im = Image.new("RGBA", ((s.w + 2 * pad) * K, (s.h + 2 * pad) * K), (0, 0, 0, 0))
        s.d = ImageDraw.Draw(s.im)
    def _p(s, x, y): return ((x + s.pad) * K, (y + s.pad) * K)
    def rect(s, x, y, w, h, r=14, fill=PAPEL, ol=TINTA, ow=4, shadow=0, sh_col=TINTA):
        if shadow:
            s.d.rounded_rectangle([*s._p(x + shadow, y + shadow * 1.15), *s._p(x + w + shadow, y + h + shadow * 1.15)], r * K, fill=sh_col)
        s.d.rounded_rectangle([*s._p(x, y), *s._p(x + w, y + h)], r * K, fill=fill,
                              outline=ol if ow else None, width=int(ow * K) if ow else 0)
    def ell(s, x, y, w, h, fill=PAPEL, ol=TINTA, ow=3):
        s.d.ellipse([*s._p(x, y), *s._p(x + w, y + h)], fill=fill, outline=ol if ow else None, width=int(ow * K))
    def poly(s, pts, fill=PAPEL, ol=TINTA, ow=4):
        P = [s._p(x, y) for x, y in pts]
        s.d.polygon(P, fill=fill)
        if ow: s.d.line(P + [P[0]], fill=ol, width=int(ow * K), joint="curve")
    def line(s, pts, col=TINTA, w=4):
        s.d.line([s._p(x, y) for x, y in pts], fill=col, width=int(w * K), joint="curve")
    def text(s, x, y, txt, kind="bold", size=40, fill=TINTA, anchor="la"):
        s.d.text(s._p(x, y), txt, font=font(kind, size * K), fill=fill, anchor=anchor)
    def done(s):
        return s.im.resize(((s.w + 2 * s.pad), (s.h + 2 * s.pad)), Image.LANCZOS)

def tw(txt, kind, size):
    b = font(kind, size * K).getbbox(txt); return (b[2] - b[0]) / K

# ---------------------------------------------------------------- composição de sprites
def put(base, spr, cx, cy, sc=1.0, rot=0.0, alpha=1.0):
    """Cola sprite RGBA centrado em (cx,cy) com escala, rotação (graus) e opacidade."""
    if spr is None or alpha <= 0.003 or sc <= 0.01: return
    im = spr
    if abs(sc - 1) > 1e-3:
        im = im.resize((max(1, int(im.width * sc)), max(1, int(im.height * sc))), Image.BICUBIC)
    if abs(rot) > 0.05:
        im = im.rotate(rot, Image.BICUBIC, expand=True)
    if alpha < 0.999:
        a = im.getchannel("A").point(lambda v: int(v * alpha)); im = im.copy(); im.putalpha(a)
    x, y = int(round(cx - im.width / 2)), int(round(cy - im.height / 2))
    bw, bh = base.size
    if x >= bw or y >= bh or x + im.width <= 0 or y + im.height <= 0: return
    sx, sy = max(0, -x), max(0, -y)
    im = im.crop((sx, sy, min(im.width, bw - x), min(im.height, bh - y)))
    base.alpha_composite(im, (x + sx, y + sy))

def pop(t, t0, t1=None, dur_in=0.28, dur_out=0.16):
    """Envelope de entrada/saída: devolve (escala, alfa) ou None se fora do tempo."""
    if t < t0: return None
    if t1 is not None and t >= t1 + dur_out: return None
    a = lin(t, t0, t0 + dur_in)
    sc = mix(0.55, 1.0, eback(a)); al = clamp(a * 2.2)
    if t1 is not None and t > t1:
        b = lin(t, t1, t1 + dur_out); sc *= mix(1, 0.8, ein(b)); al *= 1 - b
    return sc, al

# ---------------------------------------------------------------- elementos de estilo
@lru_cache(None)
def etiqueta(words, hl=(), n=None, size=58, maxw=930, hl_col="amarelo", style="papel"):
    """Legenda: etiqueta com as n primeiras palavras; índices em hl ganham caixa colorida."""
    words = list(words); n = len(words) if n is None else n
    kind = "black"; sp = size * 0.30; padx, pady = size * 0.42, size * 0.30
    hs = set(hl); pre = lambda i: size * 0.18 if i in hs and i - 1 not in hs else 0
    post = lambda i: size * 0.18 if i in hs and i + 1 not in hs else 0
    lines, cur, wcur = [], [], 0
    for i, w in enumerate(words):
        ww = tw(w, kind, size) + pre(i) + post(i)
        if cur and wcur + sp + ww > maxw - 2 * padx: lines.append(cur); cur, wcur = [], 0
        cur.append((i, w, ww)); wcur += (sp if len(cur) > 1 else 0) + ww
    lines.append(cur)
    lh = size * 1.18
    vis = [[c for c in L if c[0] < n] for L in lines]; vis = [L for L in vis if L]
    if not vis: return None
    lw = [sum(c[2] for c in L) + sp * (len(L) - 1) for L in vis]
    bw, bh = max(lw) + 2 * padx, lh * len(vis) + 2 * pady - size * 0.12
    fill, tc = (PAPEL, TINTA) if style == "papel" else (TINTA, PAPEL)
    cv = Cv(bw, bh)
    cv.rect(0, 0, bw, bh, r=size * 0.22, fill=fill, ow=4, shadow=7)
    cols = dict(amarelo=(AMARELO, TINTA), vermelho=(VERMELHO, PAPEL), lilas=(LILAS, TINTA), azul=(AZUL, PAPEL), verde=(VERDE_OK, TINTA))
    bg, fc = cols[hl_col]
    for li, L in enumerate(vis):
        x = (bw - lw[li]) / 2; y = pady + li * lh; xs = []
        for i, w, ww in L: xs.append(x); x += ww + sp
        k = 0
        while k < len(L):  # caixas de destaque por sequência contínua
            if L[k][0] in hs:
                j = k
                while j + 1 < len(L) and L[j + 1][0] in hs: j += 1
                cv.rect(xs[k], y - size * 0.06, xs[j] + L[j][2] - xs[k], size * 1.06, r=size * 0.14, fill=bg, ow=3)
                k = j + 1
            else: k += 1
        for (i, w, ww), x in zip(L, xs):
            cv.text(x + pre(i), y + size * 0.47, w, kind, size, fc if i in hs else tc, "lm")
    return cv.done()

@lru_cache(None)
def bloco(txt, fill="vermelho", size=104, lines_gap=0.98):
    """Bloco grande de texto (caixa alta) — ex.: 'NADA.' / 'CONTEÚDO'."""
    cols = dict(vermelho=(VERMELHO, PAPEL), amarelo=(AMARELO, TINTA), azul=(AZUL, PAPEL),
                lilas=(LILAS, TINTA), papel=(PAPEL, TINTA), tinta=(TINTA, AMARELO))
    bg, fc = cols[fill]; L = txt.split("\n")
    lw = max(tw(l, "black", size) for l in L)
    padx, pady = size * 0.32, size * 0.22
    bw, bh = lw + 2 * padx, size * lines_gap * len(L) + 2 * pady
    cv = Cv(bw, bh, pad=30)
    cv.rect(0, 0, bw, bh, r=size * 0.12, fill=bg, ow=6, shadow=12)
    for i, l in enumerate(L):
        cv.text(padx, pady + size * lines_gap * (i + 0.5) + size * 0.04, l, "black", size, fc, "lm")
    return cv.done()

@lru_cache(None)
def selo(txt, fill="amarelo", r=170, pts=16, size=46, rot_txt=0):
    """Selo-estrela (starburst) com texto."""
    cols = dict(vermelho=(VERMELHO, PAPEL), amarelo=(AMARELO, TINTA), lilas=(LILAS, TINTA), azul=(AZUL, PAPEL))
    bg, fc = cols[fill]
    cv = Cv(2 * r, 2 * r, pad=30)
    P = []
    for i in range(pts * 2):
        a = math.pi * i / pts - math.pi / 2; rr = r if i % 2 == 0 else r * 0.80
        P.append((r + rr * math.cos(a), r + rr * math.sin(a)))
    cv.poly([(x + 9, y + 11) for x, y in P], fill=TINTA, ow=0)
    cv.poly(P, fill=bg, ow=5)
    L = txt.split("\n"); lh = size * 1.0
    for i, l in enumerate(L):
        cv.text(r, r + (i - (len(L) - 1) / 2) * lh, l, "black", size, fc, "mm")
    return cv.done()

@lru_cache(None)
def brilho(size=60, col="amarelo"):
    """Estrelinha de 4 pontas (sparkle)."""
    c = dict(amarelo=AMARELO, papel=PAPEL, lilas=LILAS)[col]
    cv = Cv(size, size, pad=8); r = size / 2
    P = []
    for i in range(8):
        a = math.pi * i / 4; rr = r if i % 2 == 0 else r * 0.28
        P.append((r + rr * math.cos(a), r + rr * math.sin(a)))
    cv.poly(P, fill=c, ow=3); return cv.done()

@lru_cache(None)
def cursor(press=False):
    cv = Cv(46, 64, pad=10)
    P = [(0, 0), (0, 50), (12, 39), (21, 60), (30, 56), (21, 36), (37, 36)]
    cv.poly(P, fill=PAPEL if not press else AMARELO, ow=3.5); return cv.done()

def anel(base, cx, cy, x):
    """Anel de clique expandindo (x = 0..1)."""
    if not 0 <= x <= 1: return
    r = mix(10, 60, eout(x)); a = int(255 * (1 - x))
    lay = Image.new("RGBA", (int(2 * r + 12), int(2 * r + 12)), (0, 0, 0, 0))
    ImageDraw.Draw(lay).ellipse([6, 6, 6 + 2 * r, 6 + 2 * r], outline=(*TINTA, a), width=5)
    base.alpha_composite(lay, (int(cx - r - 6), int(cy - r - 6)))

def janela(w, h, titulo, chip=None):
    """Janela de app (corpo vazio) — devolve Cv pra desenhar o conteúdo; topo = 56 px."""
    cv = Cv(w, h, pad=30)
    cv.rect(0, 0, w, h, r=22, fill=PAPEL, ow=4.5, shadow=10)
    cv.rect(0, 0, w, 56, r=22, fill=PESSEGO, ow=4.5)
    cv.rect(2.2, 34, w - 4.4, 20, r=0, fill=PESSEGO, ow=0)
    cv.line([(0, 56), (w, 56)], w=4.5)
    for i, c in enumerate((VERMELHO, AMARELO, VERDE_OK)):
        cv.ell(18 + i * 26, 19, 17, 17, fill=c, ow=2.5)
    cv.text(w / 2, 29, titulo, "bold", 25, TINTA, "mm")
    if chip:
        cw = tw(chip, "bold", 20) + 28
        cv.rect(w - cw - 16, 13, cw, 32, r=16, fill=LILAS, ow=3)
        cv.text(w - cw / 2 - 16, 29, chip, "bold", 20, TINTA, "mm")
    return cv

# ---------------------------------------------------------------- vídeo dentro do cartão
@lru_cache(64)
def mascara(w, h, r):
    m = Image.new("L", (w * K, h * K), 0)
    ImageDraw.Draw(m).rounded_rectangle([0, 0, w * K - 1, h * K - 1], r * K, fill=255)
    return m.resize((w, h), Image.LANCZOS)

def cartao(frame, w, h, r=46, zoom=1.0, fx=0.5, fy=0.36, outline=0):
    """Recorta o frame (cover) com zoom no ponto focal e devolve RGBA arredondado w×h."""
    w, h = int(w), int(h)
    sw, sh = frame.size
    s = max(w / sw, h / sh) * zoom
    cw, ch = w / s, h / s
    x0 = clamp(fx * sw - cw / 2, 0, sw - cw); y0 = clamp(fy * sh - ch / 2, 0, sh - ch)
    im = frame.crop((int(x0), int(y0), int(x0 + cw), int(y0 + ch))).resize((w, h), Image.BILINEAR).convert("RGBA")
    im.putalpha(mascara(w, h, int(r)))
    if outline:
        d = ImageDraw.Draw(im); d.rounded_rectangle([0, 0, w - 1, h - 1], r, outline=TINTA, width=outline)
    return im

# ---------------------------------------------------------------- leitura do vídeo-fonte em sequência
class Fonte:
    def __init__(s, path, fps=FPS, size=(W, H)):
        s.size = size
        s.p = subprocess.Popen([FFM, "-v", "error", "-i", path, "-vf", f"fps={fps},scale={size[0]}:{size[1]}",
                                "-pix_fmt", "rgb24", "-f", "rawvideo", "-"], stdout=subprocess.PIPE)
        s.i, s.last = -1, None
    def get(s, idx):
        n = s.size[0] * s.size[1] * 3
        while s.i < idx:
            b = s.p.stdout.read(n)
            if len(b) < n: break
            s.last = Image.frombytes("RGB", s.size, b); s.i += 1
        return s.last

class Saida:
    def __init__(s, path, fps=FPS):
        s.p = subprocess.Popen([FFM, "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}",
                                "-r", str(fps), "-i", "-", "-c:v", "libx264", "-preset", "medium", "-crf", "17",
                                "-pix_fmt", "yuv420p", path], stdin=subprocess.PIPE)
    def write(s, im): s.p.stdin.write(im.convert("RGB").tobytes())
    def close(s): s.p.stdin.close(); s.p.wait()

def fundo_pontos(col, dot=(0, 0, 0, 22), step=36):
    im = Image.new("RGBA", (W, H), (*col, 255)); d = ImageDraw.Draw(im)
    for y in range(step // 2, H, step):
        for x in range(step // 2, W, step): d.ellipse([x - 2, y - 2, x + 2, y + 2], fill=dot)
    return im
