# diario-experimento · motor gráfico (PIL + numpy + ffmpeg)
# Palco escuro com brilho colorido, selo "DIA 06/30" + barra de progresso no topo, títulos
# condensados com palavra-chave colorida, números grandes, cartões de vidro, calendário 3D,
# bateria, rabisco à mão, CTA (seguir, curtir, comentar, DM) e legenda palavra a palavra.
import math, os, re, sys, subprocess, numpy as np
from functools import lru_cache
from PIL import Image, ImageDraw, ImageFont, ImageFilter

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ambiente import ffmpeg, achar_fonte
FFM = ffmpeg()
W, H, FPS = 1080, 1920, 30
K = 2  # supersampling

# ---------------------------------------------------------------- paletas
# acento = cor da marca (selo, barra, palavra-chave, sublinhado) · ruim/bom = semáforo dos números
PALETAS = {
    "lima":       dict(acento=(196, 255, 62),  ruim=(255, 92, 80),  bom=(196, 255, 62)),   # padrão AI LAB
    "eletrico":   dict(acento=(58, 134, 255),  ruim=(255, 86, 96),  bom=(70, 226, 140)),
    "ambar":      dict(acento=(255, 172, 40),  ruim=(255, 84, 84),  bom=(104, 226, 140)),
    "violeta":    dict(acento=(162, 108, 255), ruim=(255, 90, 112), bom=(104, 228, 150)),
    "ciano":      dict(acento=(36, 222, 236),  ruim=(255, 96, 96),  bom=(36, 222, 236)),
    "rosa":       dict(acento=(255, 70, 166),  ruim=(255, 122, 58), bom=(104, 228, 150)),
    "referencia": dict(acento=(232, 30, 46),   ruim=(232, 30, 46),  bom=(70, 220, 90)),     # vermelho do original
}
P = {}
FUNDO = (10, 10, 11); BRANCO = (246, 246, 243); CINZA = (150, 150, 150); ESCURO = (14, 14, 16)

def lum(c): return (0.299 * c[0] + 0.587 * c[1] + 0.114 * c[2]) / 255
def set_paleta(nome="lima", acento=None):
    """Escolhe a paleta (ou passa acento=(r,g,b) pra uma cor livre)."""
    P.clear(); P.update(PALETAS.get(nome, PALETAS["lima"]))
    if acento: P.update(acento=tuple(acento), bom=tuple(acento))
    P["nome"] = nome
    P["sobre"] = ESCURO if lum(P["acento"]) > 0.55 else BRANCO   # cor do texto em cima do acento
    _limpa_caches()
def cor(nome):
    if isinstance(nome, tuple): return nome
    return dict(branco=BRANCO, cinza=CINZA, escuro=ESCURO).get(nome) or P[nome]

# ---------------------------------------------------------------- fontes
FONTES = dict(
    titulo=("Anton-Regular.ttf", "BebasNeue-Regular.ttf", "Oswald-Bold.ttf", "impact.ttf", "Impact.ttf", "Poppins-Black.ttf"),
    black=("Poppins-Black.ttf", "seguibl.ttf", "ariblk.ttf"),
    bold=("Poppins-Bold.ttf", "segoeuib.ttf", "arialbd.ttf"),
    semi=("Poppins-SemiBold.ttf", "seguisb.ttf", "arial.ttf"),
    mono=("JetBrainsMono.ttf", "CascadiaMono.ttf", "consola.ttf", "Menlo.ttc", "Courier New.ttf"),
    mao=("PermanentMarker-Regular.ttf", "Inkfree.ttf", "segoepr.ttf"),
    serif_i=("georgiai.ttf", "Georgia Italic.ttf", "timesi.ttf"))
@lru_cache(None)
def _fp(kind):
    p = achar_fonte(*FONTES[kind])
    if not p: raise FileNotFoundError(f"nenhuma fonte para '{kind}': {FONTES[kind]}")
    return p
@lru_cache(None)
def font(kind, size): return ImageFont.truetype(_fp(kind), max(4, int(size)))
def tw(txt, kind, size):
    if not txt: return 0
    return font(kind, size).getlength(txt)

# ---------------------------------------------------------------- easing
def clamp(x, a=0., b=1.): return max(a, min(b, x))
def lin(t, a, b): return clamp((t - a) / (b - a)) if b > a else float(t >= a)
def eio(x): x = clamp(x); return x * x * (3 - 2 * x)
def eout(x): x = clamp(x); return 1 - (1 - x) ** 3
def ein(x): x = clamp(x); return x ** 3
def eback(x, s=1.7):
    x = clamp(x); x -= 1; return x * x * ((s + 1) * x + s) + 1
def mix(a, b, x): return a + (b - a) * x
def mixc(c1, c2, x): return tuple(int(mix(a, b, x)) for a, b in zip(c1, c2))

def janela(t, e, din=0.35, dout=0.25):
    """(entrada 0..1, saída 0..1) do elemento, ou None se não está na tela."""
    t0, t1 = e["t0"], e.get("t1")
    if t < t0: return None
    if t1 is not None and t >= t1 + dout: return None
    a = lin(t, t0, t0 + din)
    b = lin(t, t1, t1 + dout) if t1 is not None else 0.0
    return a, b

# ---------------------------------------------------------------- canvas supersampled
class Cv:
    def __init__(s, w, h, pad=20):
        s.w, s.h, s.pad = int(w), int(h), pad
        s.im = Image.new("RGBA", ((s.w + 2 * pad) * K, (s.h + 2 * pad) * K), (0, 0, 0, 0))
        s.d = ImageDraw.Draw(s.im)
    def _p(s, x, y): return ((x + s.pad) * K, (y + s.pad) * K)
    def rect(s, x, y, w, h, r=14, fill=None, ol=None, ow=0):
        s.d.rounded_rectangle([*s._p(x, y), *s._p(x + w, y + h)], max(0, r) * K, fill=fill,
                              outline=ol, width=int(ow * K) if ow else 0)
    def ell(s, x, y, w, h, fill=None, ol=None, ow=0):
        s.d.ellipse([*s._p(x, y), *s._p(x + w, y + h)], fill=fill, outline=ol, width=int(ow * K) if ow else 0)
    def poly(s, pts, fill=None): s.d.polygon([s._p(x, y) for x, y in pts], fill=fill)
    def line(s, pts, col, w=4): s.d.line([s._p(x, y) for x, y in pts], fill=col, width=int(w * K), joint="curve")
    def text(s, x, y, txt, kind, size, fill, anchor="la"):
        s.d.text(s._p(x, y), txt, font=font(kind, size * K), fill=fill, anchor=anchor)
    def done(s):
        return s.im.resize((s.w + 2 * s.pad, s.h + 2 * s.pad), Image.LANCZOS)

# ---------------------------------------------------------------- composição
def put(base, spr, cx, cy, sc=1.0, rot=0.0, alpha=1.0):
    if spr is None or alpha <= 0.003 or sc <= 0.01: return
    im = spr
    if abs(sc - 1) > 1e-3:
        im = im.resize((max(1, int(im.width * sc)), max(1, int(im.height * sc))), Image.BICUBIC)
    if abs(rot) > 0.05: im = im.rotate(rot, Image.BICUBIC, expand=True)
    if alpha < 0.999:
        im = im.copy(); im.putalpha(im.getchannel("A").point(lambda v: int(v * alpha)))
    x, y = int(round(cx - im.width / 2)), int(round(cy - im.height / 2))
    bw, bh = base.size
    if x >= bw or y >= bh or x + im.width <= 0 or y + im.height <= 0: return
    sx, sy = max(0, -x), max(0, -y)
    im = im.crop((sx, sy, min(im.width, bw - x), min(im.height, bh - y)))
    base.alpha_composite(im, (x + sx, y + sy))

def put_tl(base, spr, x, y, alpha=1.0):
    put(base, spr, x + spr.width / 2, y + spr.height / 2, alpha=alpha)

def texto_tl(base, txt, kind, size, rgb, x, y, alpha=1.0, track=0.0):
    """Escreve com o canto de cima-esquerdo do texto em (x, y)."""
    if not txt: return 0
    spr = spr_palavra(txt, kind, int(size), rgb, 0, track)
    pad = int(int(size) * 0.35 + 6)
    put_tl(base, spr, x - pad, y - pad, alpha)
    return spr.width - 2 * pad

def borrao_v(im, px, n=7):
    """Desfoque de movimento vertical (px = deslocamento total)."""
    px = int(abs(px))
    if px < 3: return im
    a = np.asarray(im).astype(np.float32)
    pad = np.zeros((px, a.shape[1], 4), np.float32)
    a = np.concatenate([pad, a, pad], 0)
    acc = np.zeros_like(a)
    for k in range(n):
        acc += np.roll(a, int(round(px * (k / (n - 1) - 0.5))), axis=0)
    return Image.fromarray(np.clip(acc / n, 0, 255).astype(np.uint8), "RGBA")

def borrao_h(im, px, n=7):
    return borrao_v(im.transpose(Image.Transpose.ROTATE_90), px, n).transpose(Image.Transpose.ROTATE_270)

@lru_cache(64)
def mascara(w, h, r):
    m = Image.new("L", (w * K, h * K), 0)
    ImageDraw.Draw(m).rounded_rectangle([0, 0, w * K - 1, h * K - 1], r * K, fill=255)
    return m.resize((w, h), Image.LANCZOS)

@lru_cache(16)
def brilho_blob(w, h, rgb, a=90, blur=60):
    """Mancha de luz desfocada (sombra/brilho atrás de cartões)."""
    pad = blur * 2
    im = Image.new("RGBA", (w + 2 * pad, h + 2 * pad), (0, 0, 0, 0))
    ImageDraw.Draw(im).rounded_rectangle([pad, pad, pad + w, pad + h], 40, fill=(*rgb, a))
    return im.filter(ImageFilter.GaussianBlur(blur))

def vidro(base, x, y, w, h, r=28, alpha=1.0, escuro=0.62, tint=16, borda=46, blur=22):
    """Cartão de vidro: desfoca o que está atrás, escurece e põe borda clarinha."""
    x, y, w, h = int(x), int(y), int(w), int(h)
    if alpha <= 0.01 or w < 4 or h < 4: return
    reg = base.crop((x, y, x + w, y + h)).convert("RGB").filter(ImageFilter.GaussianBlur(blur))
    a = np.asarray(reg).astype(np.float32) * escuro + tint
    g = np.linspace(1.10, 0.92, h, dtype=np.float32)[:, None, None]   # luz de cima
    reg = Image.fromarray(np.clip(a * g, 0, 255).astype(np.uint8)).convert("RGBA")
    m = mascara(w, h, int(r))
    if alpha < 0.999: m = m.point(lambda v: int(v * alpha))
    reg.putalpha(m)
    base.alpha_composite(reg, (x, y))
    deco = Image.new("RGBA", (w * K, h * K), (0, 0, 0, 0))
    ImageDraw.Draw(deco).rounded_rectangle([1, 1, w * K - 2, h * K - 2], r * K,
                                           outline=(255, 255, 255, int(borda * alpha)), width=2 * K)
    base.alpha_composite(deco.resize((w, h), Image.LANCZOS), (x, y))

# ---------------------------------------------------------------- fundo (palco escuro com brilho)
_GRAO = []
def _grao(i):
    if not _GRAO:
        rng = np.random.default_rng(7)
        for _ in range(6): _GRAO.append(rng.normal(0, 4.2, (H, W, 1)).astype(np.float32))
    return _GRAO[i % len(_GRAO)]

def fundo(t, fi=0, cfg=None):
    cfg = cfg or {}
    w, h = 108, 192
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    cx = w * (0.30 + 0.07 * math.sin(t * 0.33)); cy = h * (0.48 + 0.05 * math.cos(t * 0.27))
    g = np.exp(-(((xx - cx) / (w * 0.72)) ** 2 + ((yy - cy) / (h * 0.40)) ** 2) * 1.5) * cfg.get("brilho", 0.40)
    g2 = np.exp(-(((xx - w * 0.78) / (w * 0.55)) ** 2 + ((yy - h * 0.86) / (h * 0.26)) ** 2) * 2.0) * 0.10
    acc = np.array(P["acento"], np.float32) * 0.62
    img = np.array(FUNDO, np.float32) + g[..., None] * acc + g2[..., None] * np.array([70, 70, 72], np.float32)
    v = 1 - 0.62 * np.clip(((xx / w - .5) ** 2 * 1.4 + (yy / h - .5) ** 2) * 2.2, 0, 1)
    img = img * v[..., None]
    big = np.asarray(Image.fromarray(np.clip(img, 0, 255).astype(np.uint8)).resize((W, H), Image.BICUBIC)).astype(np.float32)
    big = big + _grao(fi)
    return Image.fromarray(np.clip(big, 0, 255).astype(np.uint8)).convert("RGBA")

# ---------------------------------------------------------------- texto com marcação *destaque*
def partes(linha):
    """'NÃO JOGA *FORA*' -> [('NÃO',False),('JOGA',False),('FORA',True)]. Pontuação colada ao *...* fica colorida."""
    out = []
    for tok in re.findall(r"\*[^*]+\*\S*|\S+", linha):
        m = re.match(r"\*([^*]+)\*(\S*)$", tok)
        if m:
            ws = m.group(1).split()
            ws[-1] += m.group(2)
            out += [(x, True) for x in ws]
        else:
            out.append((tok, False))
    return out

@lru_cache(4096)
def spr_palavra(txt, kind, size, rgb, blur_q=0, track=0.0):
    pad = int(size * 0.35 + blur_q * 3 + 6)
    f = font(kind, size)
    if track:
        wd = sum(f.getlength(c) for c in txt) + track * size * (len(txt) - 1)
    else:
        wd = f.getlength(txt)
    asc, desc = f.getmetrics()
    im = Image.new("RGBA", (int(wd + 2 * pad), int(asc + desc + 2 * pad)), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    if track:
        x = pad
        for c in txt:
            d.text((x, pad), c, font=f, fill=(*rgb, 255)); x += f.getlength(c) + track * size
    else:
        d.text((pad, pad), txt, font=f, fill=(*rgb, 255))
    if blur_q: im = im.filter(ImageFilter.GaussianBlur(blur_q))
    return im

def _limpa_caches():
    for fn in (spr_palavra, brilho_blob, _spr_numero_rot, _spr_rabisco, _spr_leg, _selo, _avatar):
        try: fn.cache_clear()
        except Exception: pass

def texto_revela(base, linhas, cx, y, t, t0, t1=None, kind="titulo", size=120, cor_txt=BRANCO,
                 stagger=0.06, lh=1.0, gap=0.24, blur=14, alinhar="centro", x0=95):
    """Palavra a palavra: sobe, desfoca->nítido. Sai desfocando. Retorna altura usada."""
    if isinstance(linhas, str): linhas = linhas.split("\n")
    i = 0
    for li, L in enumerate(linhas):
        ps = partes(L)
        ws = [tw(w, kind, size) for w, _ in ps]
        total = sum(ws) + gap * size * (len(ps) - 1)
        x = cx - total / 2 if alinhar == "centro" else x0
        yy = y + li * size * lh
        for (w, acc), ww in zip(ps, ws):
            st = t0 + i * stagger; i += 1
            a = lin(t, st, st + 0.38)
            if a <= 0: x += ww + gap * size; continue
            ea = eout(a); al = clamp(a * 1.8); dy = (1 - ea) * size * 0.42; bq = (1 - ea) * blur
            if t1 is not None and t > t1:
                b = lin(t, t1, t1 + 0.25); al *= 1 - b; bq += b * blur; dy -= eio(b) * size * 0.18
            col = P["acento"] if acc else cor_txt
            bqq = int(round(bq / 2)) * 2
            spr = spr_palavra(w, kind, int(size), col, bqq)
            pad = int(int(size) * 0.35 + bqq * 3 + 6)
            put(base, spr, x + ww / 2, yy + dy - pad + spr.height / 2, alpha=al)
            x += ww + gap * size
    return len(linhas) * size * lh

# ---------------------------------------------------------------- topo: selo + barra + @
def topo(base, t, cfg):
    dur = cfg["dur"]; y = cfg.get("topo_y", 252)
    x0, x1 = 95, W - 95
    al = 1.0
    lay = Image.new("RGBA", (W, 120), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    d.rounded_rectangle([x0, 0, x1, 6], 3, fill=(255, 255, 255, 34))
    fx = x0 + (x1 - x0) * clamp(t / dur)
    if fx > x0 + 4: d.rounded_rectangle([x0, 0, fx, 6], 3, fill=(*P["acento"], 255))
    base.alpha_composite(lay, (0, y))
    if cfg.get("selo"):
        s = _selo(cfg["selo"])
        put_tl(base, s, x0 - 4, y + 18)
    if cfg.get("handle"):
        h = spr_palavra(cfg["handle"], "mono", 26, (190, 190, 190))
        put(base, h, x1 - h.width / 2 + 10, y + 18 + 30, alpha=0.85)

@lru_cache(8)
def _selo(txt):
    size = 36; w = tw(txt, "titulo", size) + 30; h = 50
    cv = Cv(w, h, pad=4)
    cv.rect(0, 0, w, h, r=12, fill=(*P["acento"], 255))
    cv.text(w / 2, h / 2 + 1, txt, "titulo", size, (*P["sobre"], 255), "mm")
    return cv.done()

# ---------------------------------------------------------------- legenda palavra a palavra
def grupos_legenda(palavras, max_pal=3, pausa=0.32, fix=None, tirar=(), destaques=()):
    fix = fix or {}
    ws = []
    for p in palavras:
        w = fix.get(p["w"], p["w"])
        if w in tirar or not w.strip(): continue
        ws.append(dict(w=w, s=p["s"], e=p["e"]))
    G, cur = [], []
    for i, p in enumerate(ws):
        if cur and (len(cur) >= max_pal or p["s"] - cur[-1]["e"] > pausa or re.search(r"[.!?,:]$", cur[-1]["w"])):
            G.append(cur); cur = []
        cur.append(p)
    if cur: G.append(cur)
    norm = lambda s: re.sub(r"[^\wÀ-ÿ]", "", s).lower()
    dset = {norm(d) for d in destaques}
    out = []
    for gi, g in enumerate(G):
        fim = G[gi + 1][0]["s"] if gi + 1 < len(G) else g[-1]["e"] + 0.6
        fim = min(fim, g[-1]["e"] + 0.9)
        out.append(dict(ws=[(x["w"], x["s"], norm(x["w"]) in dset) for x in g], t0=g[0]["s"], t1=fim))
    return out

@lru_cache(512)
def _spr_leg(key, words, n, size):
    ws = words[:n]
    f = font("bold", size); gap = size * 0.28
    wl = [f.getlength(w) for w, _ in ws]
    total = sum(wl) + gap * (len(ws) - 1)
    pad = 40; hh = int(size * 1.6 + 2 * pad)
    im = Image.new("RGBA", (int(total + 2 * pad), hh), (0, 0, 0, 0))
    sh = Image.new("RGBA", im.size, (0, 0, 0, 0))
    d, ds = ImageDraw.Draw(im), ImageDraw.Draw(sh)
    x = pad; y = pad
    for (w, hl), ww in zip(ws, wl):
        ds.text((x, y + 3), w, font=f, fill=(0, 0, 0, 210))
        d.text((x, y), w, font=f, fill=(*BRANCO, 255))
        if hl:
            uy = y + size * 1.22
            d.rounded_rectangle([x, uy, x + ww, uy + max(4, size * 0.11)], 3, fill=(*P["acento"], 255))
        x += ww + gap
    sh = sh.filter(ImageFilter.GaussianBlur(7))
    sh.alpha_composite(im)
    return sh

def legenda(base, t, grupos, y=1430, size=46, ocultar=()):
    for a, b in ocultar:
        if a <= t < b: return
    for gi, g in enumerate(grupos):
        if g["t0"] <= t < g["t1"]:
            n = sum(1 for _, s, _ in g["ws"] if s <= t + 0.02)
            if n == 0: return
            words = tuple((w, hl) for w, _, hl in g["ws"])
            spr = _spr_leg(gi, words, n, size)
            sc = 1.0 if spr.width <= W - 190 else (W - 190) / spr.width
            put(base, spr, W / 2, y, sc=sc)
            return

# ================================================================= ELEMENTOS (tipo -> função)
TIPOS = {}
def tipo(nome):
    def deco(fn): TIPOS[nome] = fn; return fn
    return deco

# ---------- título: "NÃO JOGA *FORA*" + subtítulo itálico
@tipo("titulo")
def el_titulo(base, t, e):
    if janela(t, e) is None: return
    size = e.get("size", 118)
    h = texto_revela(base, e["txt"], e.get("cx", W / 2), e.get("y", 350), t, e["t0"], e.get("t1"),
                     kind=e.get("fonte", "titulo"), size=size, stagger=e.get("stagger", 0.07), lh=e.get("lh", 0.98))
    if e.get("sub"):
        texto_revela(base, e["sub"], e.get("cx", W / 2), e.get("y", 350) + h + size * 0.10, t,
                     e["t0"] + e.get("sub_atraso", 0.28), e.get("t1"), kind="serif_i", size=int(size * 0.40),
                     cor_txt=(205, 205, 200), stagger=0.04, gap=0.28, blur=8)

# ---------- texto simples (frase de apoio, "30 experimentos com *Claude*")
@tipo("texto")
def el_texto(base, t, e):
    if janela(t, e) is None: return
    texto_revela(base, e["txt"], e.get("cx", W / 2), e.get("y", 1300), t, e["t0"], e.get("t1"),
                 kind=e.get("fonte", "bold"), size=e.get("size", 40), stagger=e.get("stagger", 0.05),
                 gap=0.28, blur=8, lh=1.25)

# ---------- números grandes: "4 GB" / "MEMÓRIA" (contador sobe)
def _num_fmt(v, alvo_txt, de):
    m = re.match(r"^(\d+(?:[.,]\d+)?)(.*)$", alvo_txt)
    if not m: return alvo_txt
    num, resto = m.group(1), m.group(2)
    sep = "," if "," in num else ("." if "." in num else "")
    dec = len(num.split(sep)[1]) if sep else 0
    alvo = float(num.replace(",", "."))
    x = mix(de, alvo, v)
    s = f"{x:.{dec}f}"
    if sep == ",": s = s.replace(".", ",")
    return s + resto

@lru_cache(64)
def _spr_numero_rot(rot, size):
    return spr_palavra(rot, "semi", size, (200, 200, 200), 0, 0.32)

@tipo("numeros")
def el_numeros(base, t, e):
    j = janela(t, e)
    if j is None: return
    size = e.get("size", 150); y = e.get("y", 400); itens = e["itens"]
    gap = e.get("gap", 70)
    larg = [max(tw(it["v"], "titulo", size), tw(it.get("rot", ""), "semi", 24) * 1.3) for it in itens]
    total = sum(larg) + gap * (len(itens) - 1)
    x = W / 2 - total / 2
    for it, lw in zip(itens, larg):
        ti = it.get("t", e["t0"])
        a = lin(t, ti, ti + 0.42)
        if a > 0:
            v = eout(lin(t, ti, ti + it.get("conta", 0.7)))
            txt = _num_fmt(v, it["v"], it.get("de", 0)) if it.get("de") is not None or it.get("conta") else it["v"]
            al = clamp(a * 1.8) * (1 - j[1]); bq = int((1 - eout(a)) * 12 / 2) * 2
            col = cor(it.get("cor", "branco"))
            spr = spr_palavra(txt, "titulo", size, col, bq)
            sc = mix(0.7, 1.0, eback(a))
            cx = x + lw / 2
            put(base, spr, cx, y, sc=sc, alpha=al)
            if it.get("rot"):
                r = _spr_numero_rot(it["rot"], 24)
                put(base, r, cx, y + size * 0.62, alpha=al * clamp(lin(t, ti + 0.15, ti + 0.45)))
        x += lw + gap

# ---------- pílula cronômetro: "WINDOWS  17,30 s"
@tipo("timer")
def el_timer(base, t, e):
    j = janela(t, e, 0.3)
    if j is None: return
    a, b = j; al = clamp(a * 1.6) * (1 - b)
    x, y = e.get("x", 95), e.get("y", 420)
    ti, tf = e.get("conta_de", e["t0"]), e.get("conta_ate", e["t0"] + 1)
    v = e["valor"] * clamp((t - ti) / max(1e-3, tf - ti))
    txt = f"{v:.2f}".replace(".", ",") + " s"
    rot = e.get("rot", "TEMPO").upper()
    lw = tw(rot, "mono", 20) * 1.25 + 16; vw = tw("00,00 s", "mono", 34) + 8
    w, h = 36 + lw + vw + 20, 66
    dy = (1 - eout(a)) * 30
    vidro(base, x, y + dy, w, h, r=h / 2, alpha=al)
    texto_tl(base, rot, "mono", 20, (175, 175, 175), x + 24, y + dy + 20, al, 0.22)
    fim = t >= tf
    col = cor(e.get("cor", "acento")) if fim or e.get("cor_sempre") else BRANCO
    texto_tl(base, txt, "mono", 34, col, x + 26 + lw, y + dy + 12, al)

# ---------- barras de comparação num cartão de vidro
@tipo("barras")
def el_barras(base, t, e):
    j = janela(t, e, 0.3)
    if j is None: return
    a, b = j; al = clamp(a * 1.6) * (1 - b)
    x, y, w = e.get("x", 140), e.get("y", 400), e.get("w", 800)
    linhas = e["linhas"]; lh = 74; h = 44 + lh * len(linhas)
    dy = (1 - eout(a)) * 30
    vidro(base, x, y + dy, w, h, r=30, alpha=al)
    for i, L in enumerate(linhas):
        yy = y + dy + 26 + i * lh
        f = eout(lin(t, e["t0"] + 0.25 + i * 0.18, e["t0"] + 0.95 + i * 0.18)) * L["frac"]
        destaque = L.get("destaque")
        texto_tl(base, L["rot"], "semi", 24, (220, 220, 220), x + 28, yy + 6, al)
        bx, bw = x + 280, w - 280 - 140
        lay = Image.new("RGBA", (int(bw) + 4, 30), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
        d.rounded_rectangle([0, 6, bw, 26], 10, fill=(255, 255, 255, 30))
        if f > 0.01:
            c = P["acento"] if destaque else (235, 235, 235)
            d.rounded_rectangle([0, 6, max(20, bw * f), 26], 10, fill=(*c, 255))
        put_tl(base, lay, bx, yy + 14, alpha=al)
        texto_tl(base, L["val"], "titulo", 38, cor("acento") if destaque else BRANCO, x + w - 116, yy + 2, al)

# ---------- calendário 3D (série de N dias / episódios)
def _coef(dst, src):
    A, B = [], []
    for (x, y), (X, Y) in zip(dst, src):
        A.append([x, y, 1, 0, 0, 0, -X * x, -X * y]); B.append(X)
        A.append([0, 0, 0, x, y, 1, -Y * x, -Y * y]); B.append(Y)
    return np.linalg.solve(np.array(A, float), np.array(B, float)).tolist()

@tipo("calendario")
def el_calendario(base, t, e):
    j = janela(t, e, 0.4, 0.3)
    if j is None: return
    a, b = j
    total, dia, cols = e.get("total", 30), e["dia"], e.get("cols", 6)
    rows = math.ceil(total / cols)
    kw, kh, g = 118, 96, 18
    w, h = cols * kw + (cols - 1) * g, rows * kh + (rows - 1) * g + 14
    cv = Cv(w, h, pad=10)
    acc = P["acento"]
    for i in range(total):
        n = i + 1
        ai = lin(t, e["t0"] + 0.02 * i, e["t0"] + 0.02 * i + 0.30)
        if ai <= 0: continue
        r_, c_ = divmod(i, cols)
        x = c_ * (kw + g); y = r_ * (kh + g) - (1 - eout(ai)) * 40
        if n < dia: face, side, tc = (62, 62, 66), (30, 30, 33), (180, 180, 180)
        elif n == dia: face, side, tc = acc, mixc(acc, (0, 0, 0), 0.55), P["sobre"]
        else: face, side, tc = (34, 34, 37), (18, 18, 20), (96, 96, 98)
        press = 0.0
        if n == dia:
            tp = e.get("t_press", e["t0"] + 0.02 * total + 0.35)
            press = math.sin(math.pi * lin(t, tp, tp + 0.22)) * 8
        al = int(255 * clamp(ai * 1.7))
        cv.rect(x, y + 12, kw, kh, r=16, fill=(*side, al))
        cv.rect(x, y + press, kw, kh, r=16, fill=(*face, al))
        cv.text(x + kw / 2, y + press + kh / 2, f"{n:02d}", "mono", 30, (*tc, al), "mm")
    spr = cv.done()
    # perspectiva: inclina pra trás
    k = mix(0.13, 0.07, eio(lin(t, e["t0"], e["t0"] + 2.5)))
    sw, sh = spr.size
    dst = [(sw * k, 0), (sw * (1 - k), 0), (sw, sh * 0.88), (0, sh * 0.88)]
    src = [(0, 0), (sw, 0), (sw, sh), (0, sh)]
    spr = spr.transform((sw, int(sh * 0.88)), Image.PERSPECTIVE, _coef(dst, src), Image.BICUBIC)
    cx, cy = e.get("cx", W / 2), e.get("y", 760)
    sc = e.get("escala", 1.0) * mix(0.92, 1.0, eout(a))
    al = 1 - b
    # brilho atrás da tecla do dia
    put(base, brilho_blob(220, 160, acc, 110, 50), cx, cy, sc=sc, alpha=al * clamp(lin(t, e["t0"] + 0.3, e["t0"] + 0.9)) * 0.8)
    put(base, spr, cx, cy, sc=sc, rot=e.get("rot", -4) * (1 - 0.3 * eio(lin(t, e["t0"], e["t0"] + 2.5))), alpha=al)

# ---------- bateria (antes vermelha -> depois cheia)
@tipo("bateria")
def el_bateria(base, t, e):
    j = janela(t, e, 0.35)
    if j is None: return
    a, b = j; al = clamp(a * 1.7) * (1 - b)
    tf0, tf1 = e.get("enche_de", e["t0"] + 0.6), e.get("enche_ate", e["t0"] + 1.6)
    v = eio(lin(t, tf0, tf1)); frac = mix(e.get("de", 0.12), e.get("ate", 1.0), v)
    c = mixc(cor("ruim"), cor("bom"), v)
    bw, bh = 250, 118
    cv = Cv(bw + 26, bh, pad=8)
    cv.rect(0, 0, bw, bh, r=26, ol=(*BRANCO, 255), ow=8)
    cv.rect(bw + 6, bh * 0.32, 18, bh * 0.36, r=6, fill=(*BRANCO, 255))
    if frac > 0.02: cv.rect(16, 16, (bw - 32) * frac, bh - 32, r=14, fill=(*c, 255))
    spr = cv.done()
    cx, cy = e.get("cx", 300), e.get("y", 430)
    put(base, spr, cx, cy, sc=mix(0.75, 1, eback(a)), alpha=al)
    if e.get("rot_de"):
        lbl = e["rot_ate"] if v >= 0.5 else e["rot_de"]
        lc = c if v >= 0.5 else (170, 170, 170)
        pa = lin(t, tf0 + (tf1 - tf0) * 0.5, tf0 + (tf1 - tf0) * 0.5 + 0.3) if v >= 0.5 else 1
        put(base, spr_palavra(lbl, "titulo", 100, lc), cx + 300, cy, sc=mix(0.8, 1, eback(pa)), alpha=al)

# ---------- rabisco à mão ("olha a minha *reação* ↓")
@lru_cache(256)
def _spr_rabisco(txt, n, size, seta):
    f = font("mao", size)
    linhas = txt.split("\n"); cont = 0
    pad = 30; lh = size * 1.25
    larg = max(f.getlength(l.replace("*", "")) for l in linhas)
    im = Image.new("RGBA", (int(larg + 2 * pad + (60 if seta else 0)), int(lh * len(linhas) + 2 * pad + (40 if seta else 0))), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    for li, L in enumerate(linhas):
        x = pad + (larg - f.getlength(L.replace("*", ""))) / 2; acc = False
        for ch in L:
            if ch == "*": acc = not acc; continue
            if cont >= n: break
            d.text((x, pad + li * lh), ch, font=f, fill=(*(P["acento"] if acc else BRANCO), 255), stroke_width=max(2, size // 14), stroke_fill=(10, 10, 12, 255))
            x += f.getlength(ch); cont += 1
    if seta and n >= len(txt.replace("*", "").replace("\n", "")):
        x0, y0 = im.width - pad - 30, pad + lh * len(linhas) - size * 0.3
        d.line([(x0, y0), (x0 + 6, y0 + 46)], fill=(10, 10, 12, 255), width=11); d.line([(x0 - 12, y0 + 30), (x0 + 6, y0 + 48), (x0 + 20, y0 + 26)], fill=(10, 10, 12, 255), width=11, joint="curve")
        d.line([(x0 - 12, y0 + 30), (x0 + 6, y0 + 48), (x0 + 20, y0 + 26)], fill=(*BRANCO, 255), width=5, joint="curve")
    return im

@tipo("rabisco")
def el_rabisco(base, t, e):
    j = janela(t, e, 0.2)
    if j is None: return
    nchars = len(e["txt"].replace("*", "").replace("\n", ""))
    n = int(nchars * lin(t, e["t0"], e["t0"] + e.get("escreve", 0.6)))
    if n <= 0: return
    spr = _spr_rabisco(e["txt"], n, e.get("size", 52), e.get("seta", True))
    put(base, spr, e.get("cx", W / 2), e.get("y", 420), rot=e.get("rot", 3), alpha=1 - j[1])

# ---------- chip de vidro ("MINHA REAÇÃO REAL ✓")
def _check(d, x, y, s, col, w=4):
    d.line([(x, y + s * 0.5), (x + s * 0.38, y + s * 0.85), (x + s, y + s * 0.1)], fill=col, width=w, joint="curve")

@tipo("chip")
def el_chip(base, t, e):
    j = janela(t, e, 0.3)
    if j is None: return
    a, b = j; al = clamp(a * 1.6) * (1 - b)
    fk = e.get("fonte", "mao"); size = e.get("size", 28)
    txtw = tw(e["txt"], fk, size)
    w, h = txtw + 44 + (40 if e.get("check", True) else 0), size * 2.0
    x = e.get("x", 95); y = e.get("y", 330) + (1 - eout(a)) * 24
    if e.get("cx"): x = e["cx"] - w / 2
    vidro(base, x, y, w, h, r=h / 2, alpha=al)
    texto_tl(base, e["txt"], fk, size, BRANCO, x + 24, y + (h - size * 1.3) / 2, al)
    if e.get("check", True):
        lay = Image.new("RGBA", (40, 40), (0, 0, 0, 0)); _check(ImageDraw.Draw(lay), 6, 8, 24, (*P["acento"], 255), 4)
        put_tl(base, lay, x + w - 52, y + h / 2 - 20, alpha=al)

# ---------- ícone redondo: erro (X) ou ok (✓)
@tipo("icone")
def el_icone(base, t, e):
    j = janela(t, e, 0.35)
    if j is None: return
    a, b = j
    r = e.get("r", 34); ok = e.get("ok", False)
    col = cor("bom") if ok else cor("ruim")
    cv = Cv(2 * r, 2 * r, pad=6)
    cv.ell(0, 0, 2 * r, 2 * r, fill=(*col, 255))
    s = r * 0.42; c = r
    tc = P["sobre"] if ok and lum(col) > 0.55 else BRANCO
    if ok: cv.line([(c - s, c), (c - s * 0.25, c + s * 0.7), (c + s, c - s * 0.6)], (*tc, 255), r * 0.17)
    else:
        cv.line([(c - s, c - s), (c + s, c + s)], (*tc, 255), r * 0.17); cv.line([(c + s, c - s), (c - s, c + s)], (*tc, 255), r * 0.17)
    put(base, cv.done(), e["cx"], e["y"], sc=mix(0.3, 1, eback(a, 2.4)), alpha=clamp(a * 2) * (1 - b))

# ---------- vídeo / clipe (palco, cheio ou cartão)
_DIMS = {}
def dims(path):
    if path not in _DIMS:
        r = subprocess.run([FFM, "-i", path], capture_output=True, text=True, errors="replace").stderr
        m = re.search(r"Video:.*?(\d{2,5})x(\d{2,5})", r)
        _DIMS[path] = (int(m.group(1)), int(m.group(2))) if m else (1080, 1920)
    return _DIMS[path]

class Leitor:
    def __init__(s, path, w, h):
        s.path, s.w, s.h = path, w, h; s.p = None; s.cur = -10; s.last = None
    def _abre(s, fr):
        if s.p:
            try: s.p.kill()
            except Exception: pass
        s.p = subprocess.Popen([FFM, "-v", "error", "-ss", f"{fr / FPS:.3f}", "-i", s.path, "-an", "-vf",
                                f"fps={FPS},scale={s.w}:{s.h}:flags=bicubic", "-pix_fmt", "rgb24", "-f", "rawvideo", "-"],
                               stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
        s.cur = fr - 1
    def frame(s, tl):
        fr = max(0, int(round(tl * FPS)))
        if s.p is None or fr < s.cur or fr > s.cur + 45: s._abre(fr)
        n = s.w * s.h * 3
        while s.cur < fr:
            bts = s.p.stdout.read(n)
            if len(bts) < n:
                s.cur = fr; break
            s.last = Image.frombytes("RGB", (s.w, s.h), bts); s.cur += 1
        if s.last is None: s.last = Image.new("RGB", (s.w, s.h), (0, 0, 0))
        return s.last

_LEIT = {}
def leitor(path, w, h):
    k = (path, w, h)
    if k not in _LEIT: _LEIT[k] = Leitor(path, w, h)
    return _LEIT[k]

@lru_cache(16)
def _mask_palco(w, h, fy=0.16, fx=0.06):
    yy = np.linspace(0, 1, h, dtype=np.float32)[:, None]; xx = np.linspace(0, 1, w, dtype=np.float32)[None, :]
    my = np.clip(np.minimum(yy, 1 - yy) / fy, 0, 1); mx = np.clip(np.minimum(xx, 1 - xx) / fx, 0, 1)
    m = (my * my * (3 - 2 * my)) * (mx * mx * (3 - 2 * mx))
    return Image.fromarray((m * 255).astype(np.uint8), "L")

@lru_cache(4)
def _grad_cheio():
    yy = np.linspace(0, 1, H, dtype=np.float32)[:, None]
    a = np.clip((0.22 - yy) / 0.22, 0, 1) * 0.75 + np.clip((yy - 0.62) / 0.38, 0, 1) * 0.85
    a = np.repeat(a, W, axis=1)
    im = Image.new("RGBA", (W, H), (*FUNDO, 0)); im.putalpha(Image.fromarray((a * 255).astype(np.uint8), "L"))
    return im

@tipo("clip")
def el_clip(base, t, e):
    din = 0.0 if e.get("entrada", "sobe") == "corte" else 0.32
    dout = 0.0 if e.get("saida", "corte") == "corte" else 0.28
    j = janela(t, e, din if din else 0.001, dout if dout else 0.001)
    if j is None: return
    a, b = j
    modo = e.get("modo", "cartao")
    sw, sh = dims(e["src"])
    if modo == "cheio": Wt, Ht = W, H
    else:
        Wt = int(e.get("larg", 860)); Ht = int(e.get("alt", Wt * sh / sw))
    Wt -= Wt % 2; Ht -= Ht % 2
    sc0 = max(Wt / sw, Ht / sh); rw, rh = int(math.ceil(sw * sc0 / 2) * 2), int(math.ceil(sh * sc0 / 2) * 2)
    tl = e.get("ini", 0.0) + (t - e["t0"]) * e.get("vel", 1.0)
    fr = leitor(e["src"], rw, rh).frame(tl)
    z0, z1 = e.get("zoom", (1.0, 1.06))
    z = mix(z0, z1, eio(lin(t, e["t0"], e.get("t1", e["t0"] + 5))))
    cw, ch = Wt / z, Ht / z
    fx, fy = e.get("foco", (0.5, 0.5))
    x0 = clamp(fx * rw - cw / 2, 0, rw - cw); y0 = clamp(fy * rh - ch / 2, 0, rh - ch)
    im = fr.crop((int(x0), int(y0), int(x0 + cw), int(y0 + ch))).resize((Wt, Ht), Image.BILINEAR).convert("RGBA")
    if e.get("escurecer"):
        im = Image.blend(im, Image.new("RGBA", im.size, (0, 0, 0, 255)), e["escurecer"])
    if modo == "palco": im.putalpha(_mask_palco(Wt, Ht))
    elif modo == "cartao":
        r = int(e.get("r", 34)); m = mascara(Wt, Ht, r); im.putalpha(m)
        d = ImageDraw.Draw(im); d.rounded_rectangle([0, 0, Wt - 1, Ht - 1], r, outline=(255, 255, 255, 60), width=2)
    cx, cy = e.get("cx", W / 2), e.get("cy", 1000 if modo != "cheio" else H / 2)
    al, sc, dx, dy, blur = 1.0, 1.0, 0.0, 0.0, 0.0
    ent = e.get("entrada", "sobe"); sai = e.get("saida", "corte")
    if a < 1 and din:
        ea = eout(a)
        if ent == "sobe": dy = (1 - ea) * 900; blur = (1 - ea) * 220
        elif ent == "desce": dy = -(1 - ea) * 900; blur = (1 - ea) * 220
        elif ent == "lado": dx = (1 - ea) * 1000
        elif ent == "zoom": sc = mix(0.55, 1, eback(a)); al = clamp(a * 2)
        elif ent == "some": al = a
    if b > 0 and dout:
        eb = ein(b)
        if sai == "sobe": dy -= eb * 900; blur = max(blur, eb * 220)
        elif sai == "desce": dy += eb * 900; blur = max(blur, eb * 220)
        elif sai == "lado": dx -= eb * 1000
        elif sai == "zoom": sc *= mix(1, 1.25, eb); al *= 1 - b
        elif sai == "some": al *= 1 - b; sc *= mix(1, 0.92, eb)
    if modo == "cartao" and e.get("sombra", True):
        put(base, brilho_blob(Wt, Ht, (0, 0, 0), 200, 40), cx + dx, cy + dy + 28, sc=sc, rot=e.get("rot", 0), alpha=al)
        if e.get("aura", True):
            put(base, brilho_blob(Wt, Ht, P["acento"], 70, 70), cx + dx, cy + dy, sc=sc * 1.02, rot=e.get("rot", 0), alpha=al * 0.8)
    if blur > 3: im = borrao_v(im, blur * sc)
    put(base, im, cx + dx, cy + dy, sc=sc, rot=e.get("rot", 0), alpha=al)
    if modo == "cheio": base.alpha_composite(_grad_cheio())

# ---------- imagem parada (print, logo, foto) com as mesmas entradas do clipe
@tipo("imagem")
def el_imagem(base, t, e):
    j = janela(t, e, 0.32, 0.25)
    if j is None: return
    a, b = j
    im = _img(e["src"], int(e.get("larg", 700)), int(e.get("r", 28)))
    sc = mix(0.6, 1, eback(a)) * mix(1, 0.9, ein(b)); al = clamp(a * 2) * (1 - b)
    put(base, im, e.get("cx", W / 2), e.get("cy", 1000), sc=sc, rot=e.get("rot", 0), alpha=al)

@lru_cache(32)
def _img(path, larg, r):
    im = Image.open(path).convert("RGBA")
    im = im.resize((larg, int(larg * im.height / im.width)), Image.LANCZOS)
    if r: m = mascara(im.width, im.height, r); a = np.minimum(np.asarray(m), np.asarray(im.getchannel("A"))); im.putalpha(Image.fromarray(a))
    return im

# ---------- CTA: seguir / curtir / comentar / dm
@lru_cache(8)
def _avatar(path, r, iniciais="LK"):
    d = 2 * r
    if path and os.path.exists(path):
        im = Image.open(path).convert("RGBA"); s = min(im.size)
        im = im.crop(((im.width - s) // 2, (im.height - s) // 2, (im.width + s) // 2, (im.height + s) // 2)).resize((d, d), Image.LANCZOS)
    else:
        cv = Cv(d, d, pad=0); cv.ell(0, 0, d, d, fill=(*P["acento"], 255))
        cv.text(r, r, iniciais, "black", r * 0.8, (*P["sobre"], 255), "mm"); im = cv.done()
    m = Image.new("L", (d * K, d * K), 0); ImageDraw.Draw(m).ellipse([0, 0, d * K - 1, d * K - 1], fill=255)
    im.putalpha(m.resize((d, d), Image.LANCZOS))
    return im

@tipo("seguir")
def el_seguir(base, t, e):
    j = janela(t, e, 0.35)
    if j is None: return
    a, b = j; al = clamp(a * 2) * (1 - b); r = e.get("r", 110)
    cx, cy = e.get("cx", W / 2), e.get("y", 760)
    av = _avatar(e.get("avatar"), r, e.get("iniciais", "LK"))
    sc = mix(0.6, 1, eback(a))
    ring = Image.new("RGBA", (2 * r + 16, 2 * r + 16), (0, 0, 0, 0))
    ImageDraw.Draw(ring).ellipse([2, 2, 2 * r + 13, 2 * r + 13], outline=(*BRANCO, 255), width=5)
    put(base, ring, cx, cy, sc=sc, alpha=al); put(base, av, cx, cy, sc=sc, alpha=al)
    ok = t >= e.get("t_ok", e["t0"] + 0.8)
    pb = lin(t, e.get("t_ok", e["t0"] + 0.8), e.get("t_ok", e["t0"] + 0.8) + 0.25)
    br = 28; cv = Cv(2 * br, 2 * br, pad=4)
    cv.ell(0, 0, 2 * br, 2 * br, fill=(*(BRANCO if ok else P["acento"]), 255))
    tc = ESCURO if ok else P["sobre"]
    if ok: cv.line([(br - 11, br), (br - 3, br + 9), (br + 12, br - 9)], (*tc, 255), 5)
    else: cv.line([(br - 12, br), (br + 12, br)], (*tc, 255), 5); cv.line([(br, br - 12), (br, br + 12)], (*tc, 255), 5)
    put(base, cv.done(), cx, cy + r * 0.92 * sc, sc=mix(1.3, 1, eout(pb)) if ok else sc, alpha=al)
    if e.get("handle"):
        put(base, spr_palavra(e["handle"], "bold", 40, BRANCO), cx, cy + r + 70, alpha=al)

def _coracao(s):
    pts = []
    for i in range(90):
        u = 2 * math.pi * i / 90
        x = 16 * math.sin(u) ** 3; y = 13 * math.cos(u) - 5 * math.cos(2 * u) - 2 * math.cos(3 * u) - math.cos(4 * u)
        pts.append((s * (x + 17) / 34 * 2, s * (17 - y) / 34 * 2))
    return pts

@tipo("curtir")
def el_curtir(base, t, e):
    j = janela(t, e, 0.35)
    if j is None: return
    a, b = j; al = clamp(a * 2) * (1 - b); s = e.get("size", 100)
    tf = e.get("t_ok", e["t0"] + 0.5); cheio = t >= tf
    cv = Cv(2 * s, 2 * s, pad=12); pts = _coracao(s)
    if cheio: cv.poly(pts, fill=(*P["acento"], 255))
    else: cv.line(pts + [pts[0]], (*BRANCO, 255), 9)
    bump = 1 + 0.25 * math.sin(math.pi * lin(t, tf, tf + 0.3)) if cheio else 1
    put(base, cv.done(), e.get("cx", W / 2), e.get("y", 760), sc=mix(0.5, 1, eback(a)) * bump, alpha=al)

@tipo("comentar")
def el_comentar(base, t, e):
    j = janela(t, e, 0.3)
    if j is None: return
    a, b = j; al = clamp(a * 2) * (1 - b)
    w, h = e.get("w", 700), 100; x = W / 2 - w / 2; y = e.get("y", 760) - h / 2 + (1 - eout(a)) * 30
    vidro(base, x, y, w, h, r=h / 2, alpha=al, escuro=0.5, tint=24)
    pal = e["palavra"]; td = e.get("t_digita", e["t0"] + 0.3)
    n = int(len(pal) * lin(t, td, td + 0.09 * len(pal)))
    texto_tl(base, pal[:n], "bold", 42, BRANCO, x + 44, y + 22, al)
    if (int(t * 2.4) % 2 == 0) and n < len(pal):
        cw = tw(pal[:n], "bold", 42)
        put_tl(base, Image.new("RGBA", (4, 48), (*P["acento"], 255)), x + 44 + cw, y + 26, alpha=al)
    enviado = t >= td + 0.09 * len(pal) + 0.25
    br = 30; cv = Cv(2 * br, 2 * br, pad=4)
    cv.ell(0, 0, 2 * br, 2 * br, fill=(*(P["acento"] if enviado else (90, 90, 92)), 255))
    tc = P["sobre"] if enviado else BRANCO
    cv.line([(br, br + 12), (br, br - 12)], (*tc, 255), 5); cv.line([(br - 10, br - 2), (br, br - 12), (br + 10, br - 2)], (*tc, 255), 5)
    pb = lin(t, td + 0.09 * len(pal) + 0.25, td + 0.09 * len(pal) + 0.5)
    put(base, cv.done(), x + w - 54, y + h / 2, sc=1 + 0.2 * math.sin(math.pi * pb), alpha=al)

@tipo("dm")
def el_dm(base, t, e):
    j = janela(t, e, 0.35)
    if j is None: return
    a, b = j; al = clamp(a * 2) * (1 - b)
    w, h = e.get("w", 760), 250; x = W / 2 - w / 2; y = e.get("y", 640) + (1 - eout(a)) * 40
    vidro(base, x, y, w, h, r=36, alpha=al, escuro=0.55, tint=22)
    put(base, _avatar(e.get("avatar"), 30, e.get("iniciais", "LK")), x + 58, y + 58, alpha=al)
    texto_tl(base, e.get("handle", "@perfil"), "bold", 30, BRANCO, x + 104, y + 26, al)
    texto_tl(base, "agora", "semi", 22, (150, 150, 150), x + 104, y + 66, al)
    msg = e["msg"]; nm = int(len(msg) * lin(t, e["t0"] + 0.35, e["t0"] + 0.35 + 0.025 * len(msg)))
    bw = min(w - 70, tw(msg, "semi", 30) + 50)
    lay = Image.new("RGBA", (int(bw), 76), (0, 0, 0, 0))
    ImageDraw.Draw(lay).rounded_rectangle([0, 0, bw - 1, 75], 24, fill=(255, 255, 255, 34))
    put_tl(base, lay, x + 34, y + 130, alpha=al)
    if nm: texto_tl(base, msg[:nm], "semi", 30, BRANCO, x + 34 + 25, y + 130 + 16, al)

# ---------- efeitos globais
@tipo("flash")
def el_flash(base, t, e):
    x = lin(t, e["t0"], e["t0"] + e.get("dur", 0.2))
    if t < e["t0"] or x >= 1: return
    c = cor(e.get("cor", "acento")) if e.get("cor") != "branco" else BRANCO
    base.alpha_composite(Image.new("RGBA", (W, H), (*c, int(255 * e.get("forca", 0.35) * (1 - x)))))

TIPOS_POS = {"tremor"}  # aplicados no quadro inteiro, depois de tudo

def tremor(img, t, els):
    dx = dy = 0.0
    for e in els:
        if e["tipo"] != "tremor": continue
        x = lin(t, e["t0"], e["t0"] + e.get("dur", 0.3))
        if t < e["t0"] or x >= 1: continue
        amp = e.get("amp", 18) * (1 - x)
        dx += amp * math.sin(t * 91); dy += amp * math.cos(t * 77)
    if abs(dx) < 0.5 and abs(dy) < 0.5: return img
    return img.transform(img.size, Image.AFFINE, (1, 0, -dx, 0, 1, -dy), Image.BILINEAR)

# ================================================================= quadro completo
def quadro(t, fi, R):
    cfg = R.CFG
    base = fundo(t, fi, cfg)
    for e in R.EL:
        fn = TIPOS.get(e["tipo"])
        if fn: fn(base, t, e)
    if cfg.get("topo", True): topo(base, t, cfg)
    if getattr(R, "GRUPOS", None):
        legenda(base, t, R.GRUPOS, y=cfg.get("legenda_y", 1430), size=cfg.get("legenda_size", 46),
                ocultar=cfg.get("sem_legenda", ()))
    for e in R.EL:
        if e["tipo"] == "flash_final": el_flash(base, t, e)
    img = base.convert("RGB")
    return tremor(img, t, R.EL)

set_paleta("lima")
