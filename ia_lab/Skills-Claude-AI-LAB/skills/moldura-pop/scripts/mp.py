# moldura-pop · motor (PIL + numpy + ffmpeg)
# Vídeo falado dentro de uma moldura arredondada com contorno de cor de destaque; a cabeça da
# pessoa "sai" pela borda de cima (recorte BiRefNet). Em volta: letterings, cartões de UI,
# pílulas, janelas de vidro, avatar em círculo, legenda palavra a palavra com desfoque→nítido.
import math, os, json, subprocess, numpy as np
from functools import lru_cache
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageChops

import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ambiente import ffmpeg, achar_fonte
FFM = ffmpeg()
W, H = 1080, 1920
FPS_NUM, FPS_DEN = 30000, 1001          # 29,97 (mesmo da câmera -> sem dessincronizar)
FPS = FPS_NUM / FPS_DEN
DEC = 1.5                               # fonte decodificada em 1,5× a largura final (1620×2880)
K = 2                                   # supersampling dos sprites

# ---------------------------------------------------------------- tema visual (cores + fontes)
# 3 caminhos (ver SKILL.md, passo 0):
#   "classico" -> padrão APROVADO original: papel claro pontilhado + cor de destaque, Cera Pro + Georgia.
#   "ai-lab"   -> estilo Higgsfield/AI LAB: tudo preto #050505 + verde-limão #D7FF3A, Poppins + JetBrains Mono.
#   tema.json  -> personalizado (print de referência ou cores do próprio vídeo; gere com tema_da_referencia.py).
# Escolha: variável MP_TEMA (nome ou caminho de .json) ou um tema.json na pasta de trabalho / do roteiro.
# Sem nada disso = "classico".
def _hex(c):
    if isinstance(c, str):
        c = c.lstrip("#"); return tuple(int(c[i:i + 2], 16) for i in (0, 2, 4))
    return tuple(int(v) for v in c[:3])
def _lum(c): return (0.2126 * c[0] + 0.7152 * c[1] + 0.0722 * c[2]) / 255

FONTES_CLASSICO = dict(black="CeraPro-Black.otf", bold="CeraPro-Bold.otf", med="CeraPro-Medium.otf",
                       reg="CeraPro-Regular.otf", serif_i="georgiai.ttf", serif_bi="georgiaz.ttf",
                       serif_b="georgiab.ttf", mono="CascadiaMono.ttf", icon="segmdl2.ttf")
FONTES_POPPINS = dict(black="Poppins-Black.ttf", bold="Poppins-Bold.ttf", med="Poppins-Medium.ttf",
                      reg="Poppins-Regular.ttf", serif_i="Poppins-ExtraBoldItalic.ttf", serif_bi="Poppins-BlackItalic.ttf",
                      serif_b="Poppins-Bold.ttf", mono="JetBrainsMono.ttf", icon="segmdl2.ttf")
TEMAS = {
    # escuro=False: fundo claro, cartões brancos | escuro=True: tudo escuro, cartões de vidro, texto claro
    "classico": dict(escuro=False, acc="#E8302A", acc2="#FF785C", ink="#111113", ink2="#46464C", gray="#96969E",
                     line="#E4E4E8", paper="#FAFAF9", dark="#0E0A0A", glass="#221A19",
                     fontes="classico", sqz=0.80, ser=1.32, brilho=0.42),
    "ai-lab":   dict(escuro=True, acc="#D7FF3A", acc2="#E8FF96", ink="#F5F5F2", ink2="#A0A09A", gray="#787872",
                     line="#313131", paper="#050505", dark="#050505", glass="#111111", surf="#111111", surf2="#1E1E1E",
                     fontes="poppins", sqz=0.94, ser=1.12, brilho=0.17),
}
TEMAS["higgsfield"] = TEMAS["ai-lab"]

def _ler_tema():
    esc = os.environ.get("MP_TEMA", "").strip()
    if not esc:
        import sys
        for d in (os.getcwd(), os.path.dirname(os.path.abspath(sys.argv[0])) if sys.argv and sys.argv[0] else ""):
            if d and os.path.exists(os.path.join(d, "tema.json")): esc = os.path.join(d, "tema.json"); break
    if not esc: esc = "classico"
    if esc.lower().endswith(".json"):
        t = json.load(open(esc, encoding="utf8"))
        base = dict(TEMAS[t.get("base", "ai-lab" if t.get("escuro") else "classico")])
        base.update({k: v for k, v in t.items() if k != "base"})
        base.setdefault("nome", os.path.splitext(os.path.basename(esc))[0])
        base["_proprio"] = list(t.keys())          # campos escritos no json (não são trocados pelo estilo de fundo)
        return base
    t = dict(TEMAS[esc.lower()]); t["nome"] = esc.lower(); return t

TEMA = _ler_tema()
UI_ESCURA = bool(TEMA["escuro"])
ACC = _hex(TEMA["acc"])                 # destaque (troque pela cor da marca no tema.json ou com MP_ACC=#RRGGBB)
if os.environ.get("MP_ACC"): ACC = _hex(os.environ["MP_ACC"])
ACC2 = _hex(TEMA["acc2"]) if TEMA.get("acc2") and not os.environ.get("MP_ACC") else \
       tuple(min(255, int(v + (255 - v) * 0.45)) for v in ACC)          # destaque claro (brilho)
ACC_INK = (11, 11, 11) if _lum(ACC) > 0.6 else (255, 255, 255)          # texto em cima do destaque
INK = _hex(TEMA["ink"]); INK2 = _hex(TEMA["ink2"]); GRAY = _hex(TEMA["gray"]); LINE = _hex(TEMA["line"])
PAPER = _hex(TEMA["paper"]); WHITE = (255, 255, 255)
DARK = _hex(TEMA["dark"]); GLASS = _hex(TEMA["glass"])
SURF = _hex(TEMA.get("surf", TEMA["glass"])); SURF2 = _hex(TEMA.get("surf2", TEMA["glass"]))
# Estilo do fundo escuro (cenas "dark"): "brilho" = o original (quase preto + brilho da cor no topo).
# Outros: cinza-grao, grid-cinza, grid-azul, azul-grao, cinza-azul. Campo "fundo_escuro" no tema.json ou MP_FUNDO.
# Cada estilo traz a cor do vidro (cartões/janelas nas cenas escuras) combinando.
FUNDOS_ESCUROS = {"cinza-grao": "#2A2A2A", "grid-cinza": "#28282A", "grid-azul": "#181E32",
                  "azul-grao": "#1A1E30", "cinza-azul": "#24262E"}
FUNDO_ESCURO = (os.environ.get("MP_FUNDO") or TEMA.get("fundo_escuro") or "brilho").strip().lower()
if FUNDO_ESCURO in FUNDOS_ESCUROS and "glass" not in TEMA.get("_proprio", ()):
    GLASS = _hex(FUNDOS_ESCUROS[FUNDO_ESCURO])
def tint(c, a): return (*c[:3], int(a))

# ---------------------------------------------------------------- fontes
FP = os.path.join(os.path.dirname(os.path.abspath(__file__)), "fontes")   # Poppins + JetBrains Mono (OFL), vêm junto
# Se a fonte do tema não estiver no computador, usa a próxima da lista (Cera Pro é paga -> Poppins, grátis, que vem junto).
RESERVA = dict(
    black=("Poppins-Black.ttf", "seguibl.ttf", "ariblk.ttf", "Arial Black.ttf"),
    bold=("Poppins-Bold.ttf", "segoeuib.ttf", "arialbd.ttf", "Arial Bold.ttf"),
    med=("Poppins-Medium.ttf", "seguisb.ttf", "arial.ttf", "Arial.ttf"),
    reg=("Poppins-Regular.ttf", "segoeui.ttf", "arial.ttf", "Arial.ttf"),
    serif_i=("georgiai.ttf", "Georgia Italic.ttf", "Poppins-ExtraBoldItalic.ttf"),
    serif_bi=("georgiaz.ttf", "Georgia Bold Italic.ttf", "Poppins-BlackItalic.ttf"),
    serif_b=("georgiab.ttf", "Georgia Bold.ttf", "Poppins-Bold.ttf"),
    mono=("JetBrainsMono.ttf", "CascadiaMono.ttf", "consola.ttf", "Menlo.ttc", "Courier New.ttf"),
    icon=("segmdl2.ttf", "SegoeIcons.ttf"))       # ícones: fonte do Windows (no Mac viram um ponto)
FONTES = dict({"poppins": FONTES_POPPINS, "classico": FONTES_CLASSICO}.get(TEMA["fontes"], TEMA["fontes"]) if isinstance(TEMA["fontes"], str) else {**FONTES_CLASSICO, **TEMA["fontes"]})
@lru_cache(None)
def _fp(kind):
    nomes = (FONTES[kind],) + RESERVA.get(kind, ())
    for n in nomes:                               # na ordem: a do tema primeiro, depois as reservas
        p = os.path.join(FP, n) if os.path.exists(os.path.join(FP, n)) else achar_fonte(n)
        if p: return p
    if kind != "icon": raise FileNotFoundError(f"nenhuma fonte para '{kind}': {nomes}")
    return None
@lru_cache(None)
def font(kind, size):
    f = ImageFont.truetype(_fp(kind), max(1, int(size)))
    if kind == "mono":
        try: f.set_variation_by_name("Medium")      # JetBrains Mono é variável
        except Exception: pass
    return f
# condensação horizontal por estilo (serif itálico "editorial" fica condensado como na referência)
SQZ = dict(serif_i=TEMA["sqz"], serif_bi=TEMA["sqz"])

ICON = dict(camera="\uE722", globe="\uE774", home="\uE80F", people="\uE716", person="\uE77B",
            card="\uE8C7", shield="\uEA18", calc="\uE8EF", pin="\uE707", video="\uE714", film="\uE8B2",
            bolt="\uE945", heart="\uEB51", x="\uE711", check="\uE73E", chat="\uE8BD", send="\uE724",
            bug="\uEBE8", robot="\uE99A", warn="\uE7BA", bank="\uE825", news="\uE8A1", help="\uE897",
            key="\uE8D7", grid="\uF0E2", calendar="\uE787", city="\uF404", contact="\uE8D4", info="\uE946")

# ---------------------------------------------------------------- easing
def clamp(x, a=0., b=1.): return max(a, min(b, x))
def lin(t, a, b): return clamp((t - a) / (b - a)) if b > a else float(t >= a)
def eio(x): x = clamp(x); return x * x * (3 - 2 * x)
def eio5(x): x = clamp(x); return x * x * x * (x * (6 * x - 15) + 10)
def eout(x): x = clamp(x); return 1 - (1 - x) ** 3
def eout5(x): x = clamp(x); return 1 - (1 - x) ** 5
def ein(x): x = clamp(x); return x ** 3
def eback(x, s=1.6):
    x = clamp(x) - 1; return x * x * ((s + 1) * x + s) + 1
def mix(a, b, x): return a + (b - a) * x
def mixc(a, b, x): return tuple(int(round(mix(p, q, x))) for p, q in zip(a, b))

# ---------------------------------------------------------------- texto
def text_img(txt, kind="bold", size=60, fill=INK, track=0.0, sqz=None):
    """Texto num RGBA justo (com folga). track = espaçamento extra em fração do tamanho."""
    sqz = SQZ.get(kind, 1.0) if sqz is None else sqz
    f = font(kind, size * K)
    asc, desc = f.getmetrics()
    if track == 0:
        wid = f.getlength(txt)
    else:
        wid = sum(f.getlength(c) for c in txt) + track * size * K * (len(txt) - 1)
    pad = int(size * K * 0.25)
    im = Image.new("RGBA", (int(wid) + 2 * pad, asc + desc + 2 * pad), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    if track == 0:
        d.text((pad, pad), txt, font=f, fill=fill)
    else:
        x = pad
        for c in txt:
            d.text((x, pad), c, font=f, fill=fill); x += f.getlength(c) + track * size * K
    im = im.resize((max(1, int(im.width / K * sqz)), max(1, int(im.height / K))), Image.LANCZOS)
    im.info["base"] = (pad + asc) / K      # linha de base (px do topo)
    im.info["pad"] = pad / K
    im.info["l"] = pad / K * sqz; im.info["adv"] = wid / K * sqz
    return im

def glow(im, radius=14, col=ACC, strength=0.9, pad=None):
    """Brilho colorido atrás de um RGBA."""
    pad = pad or radius * 2
    big = Image.new("RGBA", (im.width + 2 * pad, im.height + 2 * pad), (0, 0, 0, 0))
    a = Image.new("L", big.size, 0); a.paste(im.getchannel("A"), (pad, pad))
    a = a.filter(ImageFilter.GaussianBlur(radius)).point(lambda v: min(255, int(v * strength)))
    g = Image.new("RGBA", big.size, (*col[:3], 255)); g.putalpha(a)
    g.alpha_composite(im, (pad, pad))
    g.info.update(im.info); g.info["base"] = im.info.get("base", 0) + pad
    g.info["l"] = im.info.get("l", 0) + pad
    return g

def shadow(im, radius=18, alpha=0.22, dy=10, col=(0, 0, 0)):
    pad = radius * 2 + abs(dy)
    big = Image.new("RGBA", (im.width + 2 * pad, im.height + 2 * pad), (0, 0, 0, 0))
    a = Image.new("L", big.size, 0); a.paste(im.getchannel("A"), (pad, pad + dy))
    a = a.filter(ImageFilter.GaussianBlur(radius)).point(lambda v: int(v * alpha))
    s = Image.new("RGBA", big.size, (*col, 255)); s.putalpha(a)
    s.alpha_composite(im, (pad, pad))
    return s

def hstack(parts, gap=0, valign="base"):
    """Junta sprites de texto lado a lado alinhando pela linha de base."""
    base = max(p.info.get("base", p.height / 2) for p in parts)
    below = max(p.height - p.info.get("base", p.height / 2) for p in parts)
    L = lambda p: p.info.get("l", 0); A = lambda p: p.info.get("adv", p.width)
    adv = sum(A(p) for p in parts) + gap * (len(parts) - 1)
    left = L(parts[0]); right = max(0, parts[-1].width - L(parts[-1]) - A(parts[-1]))
    im = Image.new("RGBA", (int(left + adv + right) + 2, int(base + below)), (0, 0, 0, 0))
    x = left
    for p in parts:
        y = base - p.info.get("base", p.height / 2) if valign == "base" else (im.height - p.height) / 2
        im.alpha_composite(p, (int(x - L(p)), int(y))); x += A(p) + gap
    im.info["base"] = base; im.info["l"] = left; im.info["adv"] = adv
    return im

def vstack(parts, gap=0, align="c"):
    w = max(p.width for p in parts); h = sum(p.height for p in parts) + gap * (len(parts) - 1)
    im = Image.new("RGBA", (int(w), int(h)), (0, 0, 0, 0)); y = 0
    for p in parts:
        x = {"c": (w - p.width) / 2, "l": 0, "r": w - p.width}[align]
        im.alpha_composite(p, (int(x), int(y))); y += p.height + gap
    return im

def icon_img(name, size=40, fill=INK):
    if not _fp("icon"):                                  # sem fonte de ícones (Mac): um ponto no lugar
        r = int(size * K * 0.5); im = Image.new("RGBA", (r, r), (0, 0, 0, 0))
        ImageDraw.Draw(im).ellipse((0, 0, r - 1, r - 1), fill=fill); return im
    return text_img(ICON.get(name, name), "icon", size, fill, sqz=1.0)

# ---------------------------------------------------------------- formas (supersampled)
class Cv:
    def __init__(s, w, h):
        s.w, s.h = int(w), int(h)
        s.im = Image.new("RGBA", (s.w * K, s.h * K), (0, 0, 0, 0)); s.d = ImageDraw.Draw(s.im)
    def rr(s, x, y, w, h, r, fill=None, ol=None, ow=2):
        s.d.rounded_rectangle([x * K, y * K, (x + w) * K - 1, (y + h) * K - 1], r * K, fill=fill,
                              outline=ol, width=int(ow * K) if ol else 0)
    def ell(s, x, y, w, h, fill=None, ol=None, ow=2):
        s.d.ellipse([x * K, y * K, (x + w) * K - 1, (y + h) * K - 1], fill=fill, outline=ol, width=int(ow * K) if ol else 0)
    def line(s, pts, col, w=3):
        s.d.line([(x * K, y * K) for x, y in pts], fill=col, width=int(w * K), joint="curve")
    def paste(s, im, x, y):
        big = im.resize((im.width * K, im.height * K), Image.LANCZOS)
        s.im.alpha_composite(big, (int(x * K), int(y * K)))
    def done(s): return s.im.resize((s.w, s.h), Image.LANCZOS)

def paste_c(cv, im, cx, cy):
    cv.paste(im, cx - im.width / 2, cy - im.height / 2)

# ---------------------------------------------------------------- componentes visuais
def badge(icon, size=96, fill=ACC, fg=WHITE, r=26, ring=None):
    """Quadradinho arredondado com ícone (o 'escudo laranja' da referência)."""
    if fill == ACC and fg == WHITE: fg = ACC_INK
    if UI_ESCURA and fill == INK: fill, ring = SURF2, ring or LINE
    c = Cv(size, size); c.rr(0, 0, size, size, r, fill=fill, ol=ring, ow=3)
    paste_c(c, icon_img(icon, size * 0.42, fg), size / 2, size / 2 + 1)
    return shadow(c.done(), 14, 0.28, 8)

def pill(txt, icon=None, size=44, fill=ACC, fg=WHITE, kind="black", padx=0.6, glow_col=None, ol=None):
    if fill == ACC and fg == WHITE: fg = ACC_INK
    if UI_ESCURA and fill == INK: fill, ol = SURF2, ol or LINE
    if UI_ESCURA and fill == WHITE: fill, ol = SURF, ol or LINE
    t = text_img(txt, kind, size, fg)
    parts = [t]
    if icon: parts = [icon_img(icon, size * 0.78, fg), t]
    row = hstack(parts, gap=int(size * 0.28), valign="c")
    h = int(size * 1.62); w = int(row.width + size * padx * 2)
    c = Cv(w, h); c.rr(0, 0, w, h, h * 0.3, fill=fill, ol=ol, ow=2)
    paste_c(c, row, w / 2, h / 2)
    im = c.done()
    return glow(im, 22, glow_col, 0.75) if glow_col else im

def chip(txt, icon=None, theme="dark", size=30, accent=True):
    """Etiqueta pequena (ex.: 'auditoria de segurança')."""
    if UI_ESCURA: theme = "dark"
    fg = WHITE if theme == "dark" else INK
    bg = tint(GLASS, 235) if theme == "dark" else tint(WHITE, 255)
    ol = tint(ACC, 150) if accent else (tint(WHITE, 40) if theme == "dark" else LINE)
    t = text_img(txt, "bold", size, fg)
    parts = [t]
    if icon:
        ib = Cv(size * 1.25, size * 1.25); ib.rr(0, 0, size * 1.25, size * 1.25, size * 0.3, ol=tint(ACC, 255), ow=2)
        paste_c(ib, icon_img(icon, size * 0.62, ACC), size * 0.625, size * 0.64)
        parts = [ib.done(), t]
    row = hstack(parts, gap=int(size * 0.4), valign="c")
    h = int(size * 1.95); w = int(row.width + size * 1.1)
    c = Cv(w, h); c.rr(0, 0, w, h, h * 0.32, fill=bg, ol=ol, ow=2)
    paste_c(c, row, w / 2, h / 2)
    im = c.done()
    return shadow(im, 16, 0.16 if theme == "light" else 0.4, 8)

def status(txt, ok=True, size=24):
    col = ACC if ok else (196, 62, 58)
    if ok:
        return pill(txt, "check", size, fill=col, fg=WHITE, kind="bold", padx=0.45)
    if UI_ESCURA: return pill(txt, "x", size, fill=(48, 18, 16), fg=(255, 120, 100), kind="bold", padx=0.45)
    return pill(txt, "x", size, fill=(253, 232, 230), fg=col, kind="bold", padx=0.45)

def card(title, sub=None, icon=None, w=480, h=150, theme="light", active=True, icon_fill=None, extra=None):
    """Cartão branco (ou vidro escuro) com disco de ícone, título e subtítulo mono."""
    dark = theme == "dark" or UI_ESCURA
    c = Cv(w, h)
    c.rr(0, 0, w, h, 26, fill=tint(GLASS, 240) if dark else WHITE,
         ol=tint(ACC, 255 if active else 0) if active else (tint(WHITE, 30) if dark else LINE), ow=3 if active else 2)
    x = 26
    if icon:
        d = h * 0.46
        c.ell(x, (h - d) / 2, d, d, fill=icon_fill or (INK if not dark else ACC), ol=tint(ACC, 255), ow=3)
        paste_c(c, icon_img(icon, d * 0.45, ACC if not dark else ACC_INK), x + d / 2, h / 2 + 1)
        x += d + 22
    tt = text_img(title, "black", 42, WHITE if dark else INK)
    if sub:
        st = text_img(sub, "mono", 24, GRAY if not dark else (200, 180, 176))
        blk = vstack([tt, st], gap=-14, align="l")
    else:
        blk = tt
    c.paste(blk, x - tt.info["pad"], (h - blk.height) / 2)
    if extra is not None:
        c.paste(extra, w - extra.width - 22, (h - extra.height) / 2)
    return shadow(c.done(), 22, 0.14 if not dark else 0.45, 12)

def glass_window(w, h, title, icon="chat", theme="dark"):
    """Janela tipo app (cabeçalho com ícone + título + três pontinhos)."""
    dark = theme == "dark" or UI_ESCURA
    c = Cv(w, h)
    c.rr(0, 0, w, h, 30, fill=tint(GLASS, 238) if dark else WHITE, ol=tint(WHITE, 28) if dark else LINE, ow=2)
    ib = Cv(44, 44)
    if UI_ESCURA:
        ib.rr(0, 0, 44, 44, 12, fill=ACC); paste_c(ib, icon_img(icon, 22, ACC_INK), 22, 23)
    else:
        ib.rr(0, 0, 44, 44, 12, fill=WHITE if dark else INK); paste_c(ib, icon_img(icon, 22, INK if dark else WHITE), 22, 23)
    c.paste(ib.done(), 28, 26)
    tt = text_img(title, "bold", 34, WHITE if dark else INK)
    c.paste(tt, 88 - tt.info["pad"], 48 - tt.height / 2)
    for i in range(3): c.ell(w - 82 + i * 18, 44, 9, 9, fill=tint(WHITE if dark else INK, 90))
    return shadow(c.done(), 30, 0.5 if dark else 0.16, 16)

def bricks(w, h, col=ACC):
    """Parede de tijolinho desenhada (com janela)."""
    c = Cv(w, h); c.rr(0, 0, w, h, 26, fill=(120, 40, 30))
    bw, bh = 74, 30
    rng = np.random.default_rng(7)
    for row in range(int(h / bh) + 1):
        off = (bw / 2) * (row % 2)
        for i in range(-1, int(w / bw) + 2):
            x = i * bw - off; y = row * bh
            v = rng.uniform(-18, 18)
            fill = (int(clamp(col[0] - 40 + v, 0, 255)), int(clamp(col[1] + 10 + v * .4, 0, 255)), int(clamp(col[2] + 10 + v * .4, 0, 255)))
            c.rr(x + 3, y + 3, bw - 6, bh - 6, 4, fill=fill)
    m = Image.new("L", (w * K, h * K), 0); ImageDraw.Draw(m).rounded_rectangle([0, 0, w * K - 1, h * K - 1], 26 * K, fill=255)
    a = ImageChops.multiply(c.im.getchannel("A"), m); c.im.putalpha(a)
    return c

# ---------------------------------------------------------------- composição de sprites
def put(base, spr, cx, cy, sc=1.0, rot=0.0, alpha=1.0, blur=0.0):
    if spr is None or alpha <= 0.003 or sc <= 0.01: return
    im = spr
    if abs(sc - 1) > 1e-3:
        im = im.resize((max(1, int(im.width * sc)), max(1, int(im.height * sc))), Image.BICUBIC)
    if blur > 0.3:
        p = int(blur * 2.5) + 2
        big = Image.new("RGBA", (im.width + 2 * p, im.height + 2 * p), (0, 0, 0, 0)); big.paste(im, (p, p))
        im = big.filter(ImageFilter.GaussianBlur(blur))
    if abs(rot) > 0.05: im = im.rotate(rot, Image.BICUBIC, expand=True)
    if alpha < 0.999:
        im = im.copy(); im.putalpha(im.getchannel("A").point(lambda v: int(v * alpha)))
    x, y = int(round(cx - im.width / 2)), int(round(cy - im.height / 2))
    base.alpha_composite(im, (x, y)) if (x >= 0 and y >= 0 and x + im.width <= base.width and y + im.height <= base.height) \
        else _paste_clip(base, im, x, y)

def _paste_clip(base, im, x, y):
    x0, y0 = max(0, x), max(0, y); x1, y1 = min(base.width, x + im.width), min(base.height, y + im.height)
    if x1 <= x0 or y1 <= y0: return
    base.alpha_composite(im.crop((x0 - x, y0 - y, x1 - x, y1 - y)), (x0, y0))

class El:
    """Elemento animado. spr = sprite RGBA ou função t->sprite.
    entra: 'pop' (escala com overshoot), 'blur' (desfoque→nítido subindo), 'wipe' (revela da esquerda)."""
    def __init__(s, spr, cx, cy, t0, t1=None, enter="blur", dur=0.42, out=0.22, rot=0.0, float_amp=0.0,
                 dy=26, dx=0, layer="back", anchor="c"):
        s.spr, s.cx, s.cy, s.t0, s.t1 = spr, cx, cy, t0, t1
        s.enter, s.dur, s.out, s.rot, s.fa, s.dy, s.dx, s.layer, s.anchor = enter, dur, out, rot, float_amp, dy, dx, layer, anchor
    def draw(s, base, t, t_end):
        t1 = s.t1 if s.t1 is not None else t_end
        if t < s.t0 or t > t1 + s.out: return
        spr = s.spr(t) if callable(s.spr) else s.spr
        if spr is None: return
        p = lin(t, s.t0, s.t0 + s.dur); q = lin(t, t1, t1 + s.out)
        sc, a, bl, dy, dx = 1.0, 1.0, 0.0, 0.0, 0.0
        if s.enter == "pop":
            sc = mix(0.6, 1.0, eback(p, 2.2)); a = eout(lin(t, s.t0, s.t0 + s.dur * .4)); bl = (1 - eout(p)) * 6
        elif s.enter == "blur":
            a = eout(p); bl = (1 - eout(p)) * 14; dy = (1 - eout5(p)) * s.dy; dx = (1 - eout5(p)) * s.dx; sc = mix(0.96, 1, eout(p))
        elif s.enter == "wipe":
            a = 1.0
            if p < 1:
                spr = spr.copy(); w = spr.width
                g = np.clip((np.arange(w) - (eout(p) * 1.25 - 0.25) * w) / (0.25 * w), 0, 1)
                m = Image.fromarray(((1 - g) * 255).astype(np.uint8)[None, :].repeat(spr.height, 0), "L")
                spr.putalpha(ImageChops.multiply(spr.getchannel("A"), m)); bl = (1 - eout(p)) * 5
        if q > 0:
            a *= 1 - eio(q); bl += eio(q) * 10; sc *= mix(1, 0.94, eio(q))
        fl = math.sin((t - s.t0) * 1.7 + s.cx * 0.01) * s.fa
        cx, cy = s.cx + dx, s.cy + dy + fl
        if s.anchor == "l": cx += spr.width * sc / 2
        elif s.anchor == "r": cx -= spr.width * sc / 2
        put(base, spr, cx, cy, sc, s.rot + fl * 0.3, a, bl)

# ---------------------------------------------------------------- fundos
@lru_cache(None)
def fundo(theme):
    """'light' = papel pontilhado (claro no clássico; escuro com pontinhos discretos em tema escuro).
    'dark' = quase preto com brilho da cor de destaque no topo."""
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    if theme == "light":
        a = np.zeros((H, W, 3), np.float32) + np.array(PAPER, np.float32)
        dots = ((xx.astype(int) % 36 == 18) & (yy.astype(int) % 36 == 18))
        if _lum(PAPER) < 0.5:
            a[dots] += 22
            d = np.sqrt(((xx - W / 2) / (W * 0.9)) ** 2 + ((yy - H * 0.30) / (H * 0.5)) ** 2)
            a += (np.clip(1 - d, 0, 1) ** 2 * 10)[..., None]
        else:
            a[dots] -= 26
    elif FUNDO_ESCURO in FUNDOS_ESCUROS:
        a = _fundo_escuro(FUNDO_ESCURO, xx, yy)
    else:
        d = np.sqrt(((xx - W / 2) / (W * 0.85)) ** 2 + ((yy - H * 0.16) / (H * 0.42)) ** 2)
        gl = np.clip(1 - d, 0, 1) ** 1.8
        warm = 0 if UI_ESCURA else np.array([16, 8, 4], np.float32)
        a = np.array(DARK, np.float32) + gl[..., None] * (np.array(ACC, np.float32) * TEMA["brilho"] + warm)
        a = a + np.random.default_rng(1).normal(0, 2.0 if UI_ESCURA else 2.2, (H, W, 1))
    return Image.fromarray(np.clip(a, 0, 255).astype(np.uint8), "RGB").convert("RGBA")

def _fundo_escuro(nome, xx, yy):
    """Estilos do fundo 'dark' (escolhidos no passo 0): cinza granulado, grids, azul."""
    acc = np.array(ACC, np.float32)
    def blob(cx, cy, rx, ry, p=2.0):
        return np.clip(1 - np.sqrt(((xx - cx) / rx) ** 2 + ((yy - cy) / ry) ** 2), 0, 1) ** p
    def grid(a, cor, passo=60, cruz=40):
        xi, yi = xx.astype(int), yy.astype(int)
        a[(xi % passo == 0) | (yi % passo == 0)] += np.array(cor, np.float32)
        a[((xi % (passo * 4) == 0) & (yi % (passo * 4) < 9)) | ((yi % (passo * 4) == 0) & (xi % (passo * 4) < 9))] += cruz
        return a
    def vinheta(a, f=0.55):
        d = np.sqrt(((xx - W / 2) / (W * 0.75)) ** 2 + ((yy - H * 0.45) / (H * 0.62)) ** 2)
        return a * (1 - np.clip(d, 0, 1.4)[..., None] ** 2 * f)
    def base(rgb): return np.zeros((H, W, 3), np.float32) + np.array(rgb, np.float32)
    def spot(rgb, cy=0.40): return blob(W * 0.5, H * cy, W * 0.85, H * 0.48, 1.4)[..., None] * np.array(rgb, np.float32)
    if nome == "cinza-grao":        # fundo de estúdio cinza com luz atrás da moldura + grão de filme
        a = base([22, 22, 22]) + spot([60, 60, 60]) + blob(W * 0.5, H * 0.08, W * 0.5, H * 0.18)[..., None] * acc * 0.08
        a, g = vinheta(a), 6.5
    elif nome == "grid-cinza":      # cinza granulado + grade fina de planta técnica
        a = grid(base([22, 22, 23]), [13, 13, 13]) + spot([48, 48, 50])
        a, g = vinheta(a), 5.0
    elif nome == "grid-azul":       # azul-tinta + grade + luz azul no topo e um toque da cor de destaque no canto
        a = grid(base([11, 15, 30]), [12, 18, 34], cruz=34)
        a += blob(W * 0.5, H * 0.18, W * 0.95, H * 0.42, 1.7)[..., None] * np.array([30, 60, 140], np.float32)
        a += blob(W * 0.05, H * 0.05, W * 0.55, H * 0.25)[..., None] * acc * 0.28
        a, g = vinheta(a, 0.5), 4.0
    elif nome == "azul-grao":       # azul com manchas de luz desfocadas (azul + roxo + destaque), sem grade
        a = base([12, 15, 28]) + blob(W * 0.5, H * 0.20, W * 1.0, H * 0.45, 1.6)[..., None] * np.array([35, 65, 150], np.float32)
        a += blob(W * 0.95, H * 0.35, W * 0.6, H * 0.30, 1.8)[..., None] * np.array([36, 27, 81], np.float32)
        a += blob(W * 0.05, H * 0.08, W * 0.5, H * 0.22)[..., None] * acc * 0.30
        g = 5.5
    else:                           # "cinza-azul": grade cinza com luz azul por cima
        a = grid(base([20, 21, 24]), [13, 13, 15])
        a += blob(W * 0.5, H * 0.16, W * 0.95, H * 0.42, 1.7)[..., None] * np.array([28, 50, 105], np.float32)
        a, g = vinheta(a), 5.0
    return a + np.random.default_rng(1).normal(0, g, (H, W, 1))

# ---------------------------------------------------------------- vídeo: moldura / tela cheia / círculo
class Track:
    """Posição da cabeça (topo, centro x, largura) por quadro, medida na máscara e suavizada."""
    def __init__(s, path):
        s.d = json.load(open(path))
    def at(s, i):
        i = int(clamp(i, 0, len(s.d["top"]) - 1))
        return s.d["top"][i], s.d["cx"][i], s.d["hw"]

def medir_cabeca(matte_path, out_json, sigma_s=0.35):
    """Lê a máscara (540×960) e mede a cabeça quadro a quadro. Coordenadas em px da fonte a 1080 de largura."""
    p = subprocess.Popen([FFM, "-v", "error", "-i", matte_path, "-f", "rawvideo", "-pix_fmt", "gray", "-"], stdout=subprocess.PIPE)
    tops, cxs, hws = [], [], []
    while True:
        raw = p.stdout.read(540 * 960)
        if len(raw) < 540 * 960: break
        m = np.frombuffer(raw, np.uint8).reshape(960, 540) > 128
        rows = m.sum(1)
        ys = np.where(rows > 8)[0]
        top = ys[0] if len(ys) else 200
        band = m[top:top + 70]
        xs = np.where(band.any(0))[0]
        cx = xs.mean() if len(xs) else 270
        r = m[min(959, top + 75)]; xr = np.where(r)[0]
        hw = (xr[-1] - xr[0]) if len(xr) else 200
        tops.append(top * 2); cxs.append(cx * 2); hws.append(hw * 2)
    def smooth(v):
        v = np.array(v, np.float32); n = len(v); s = sigma_s * FPS
        k = np.exp(-0.5 * (np.arange(-int(3 * s), int(3 * s) + 1) / s) ** 2); k /= k.sum()
        pad = np.pad(v, len(k) // 2, mode="edge")
        return np.convolve(pad, k, mode="valid")[:n].tolist()
    hw_med = float(np.median(hws))
    json.dump(dict(top=smooth(tops), cx=smooth(cxs), hw=hw_med, n=len(tops)), open(out_json, "w"))
    return hw_med

class Modo:
    """Estado da janela de vídeo: retângulo (x,y,w,h,r), onde a cabeça fica (ax, top) e o tamanho da cabeça (hw),
    pop = quanto a cabeça sai pela borda, ring = espessura do contorno, sh = sombra."""
    def __init__(s, x, y, w, h, r, ax, top, hw, pop=0.0, ring=4.0, gl=1.0):
        s.v = dict(x=x, y=y, w=w, h=h, r=r, ax=ax, top=top, hw=hw, pop=pop, ring=ring, gl=gl)
    def lerp(s, o, k):
        m = Modo(0, 0, 0, 0, 0, 0, 0, 0); m.v = {a: mix(s.v[a], o.v[a], k) for a in s.v}; return m

def CARD(top=960, w=830, head_w=430, over=100):
    return Modo((W - w) / 2, top, w, H - top + 140, 64, W / 2, top - over, head_w, pop=1.0, ring=4)
def FULL(head_top=250, head_w=600):
    return Modo(0, 0, W, H, 0, W / 2, head_top, head_w, pop=0.0, ring=0, gl=0)
def CIRCLE(cx, cy, r=150, head_w=None):
    hw = head_w or r * 1.25
    return Modo(cx - r, cy - r, 2 * r, 2 * r, r, cx, cy - r * 0.78, hw, pop=0.0, ring=5)

@lru_cache(64)
def _rr_mask(x, y, w, h, r):
    m = Image.new("L", (W * 2, H * 2), 0)
    ImageDraw.Draw(m).rounded_rectangle([x * 2, y * 2, (x + w) * 2 - 1, (y + h) * 2 - 1], r * 2, fill=255)
    return m.resize((W, H), Image.BILINEAR)

@lru_cache(64)
def _ring(x, y, w, h, r, ring, gl, theme):
    lay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    if ring <= 0.2: return lay
    d = Image.new("RGBA", (W * 2, H * 2), (0, 0, 0, 0))
    ImageDraw.Draw(d).rounded_rectangle([x * 2, y * 2, (x + w) * 2 - 1, (y + h) * 2 - 1], r * 2,
                                        outline=(*ACC, 255), width=int(ring * 2))
    d = d.resize((W, H), Image.LANCZOS)
    if gl > 0.05:
        a = d.getchannel("A").filter(ImageFilter.GaussianBlur(16)).point(lambda v: min(255, int(v * 1.6 * gl)))
        g = Image.new("RGBA", (W, H), (*ACC2, 255)); g.putalpha(a)
        # brilho mais forte em cima, some pra baixo (como a referência)
        grad = np.clip(1.25 - (np.arange(H) - y) / max(1, h * 0.75), 0.25, 1.0)
        gm = Image.fromarray((grad[:, None].repeat(W, 1) * 255).astype(np.uint8), "L")
        g.putalpha(ImageChops.multiply(g.getchannel("A"), gm))
        lay.alpha_composite(g)
    lay.alpha_composite(d)
    return lay

@lru_cache(64)
def _soft_shadow(x, y, w, h, r, theme):
    lay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    m = Image.new("L", (W // 2, H // 2), 0)
    ImageDraw.Draw(m).rounded_rectangle([x / 2, (y + 16) / 2, (x + w) / 2, (y + h + 16) / 2], r / 2, fill=255)
    m = m.filter(ImageFilter.GaussianBlur(18)).resize((W, H), Image.BILINEAR)
    lay.putalpha(m.point(lambda v: int(v * (0.30 if theme == "light" else 0.55))))
    return lay

def compor_video(base, src, matte, head, modo, theme, extra_zoom=1.0, shake=(0, 0)):
    """Desenha o vídeo no estado `modo`. src = PIL RGB 1620×2880, matte = PIL L 540×960,
    head = (top, cx, hw) medidos na fonte (escala 1080). Retorna a camada da cabeça 'saltando' (ou None)."""
    v = modo.v
    top, hcx, hw = head
    k = v["hw"] / hw * extra_zoom                       # px finais por px-fonte(1080)
    # transformação: ponto-fonte (sx,sy) -> (ax + (sx-hcx)*k, top_out + (sy-top)*k)
    ax, ty = v["ax"] + shake[0], v["top"] + shake[1]
    x, y, w, h, r = [int(round(v[a])) for a in ("x", "y", "w", "h", "r")]
    # nunca deixar faltar imagem dentro da moldura: zoom mínimo + trava das bordas
    vx0, vy0, vx1, vy1 = max(0, x), max(0, y), min(W, x + w), min(H, y + h)
    k = max(k, (vx1 - vx0) / W * 1.01, (vy1 - vy0) / H * 1.01)
    ax = clamp(ax, vx1 - (W - hcx) * k, vx0 + hcx * k)
    ty = clamp(ty, vy1 - (H - top) * k, vy0 + top * k)
    def to_src(X, Y): return (hcx + (X - ax) / k, top + (Y - ty) / k)
    pop = v["pop"]
    # região da tela que precisa de pixels de vídeo
    rx0, ry0, rx1, ry1 = max(0, x), max(0, y), min(W, x + w), min(H, y + h)
    if pop > 0.01:
        ry0 = max(0, min(ry0, int(ty - 60)))
        rx0 = max(0, x - 40); rx1 = min(W, x + w + 40)
    if rx1 <= rx0 or ry1 <= ry0: return None
    sx0, sy0 = to_src(rx0, ry0); sx1, sy1 = to_src(rx1, ry1)
    box = (sx0 * DEC, sy0 * DEC, sx1 * DEC, sy1 * DEC)
    patch = src.transform((rx1 - rx0, ry1 - ry0), Image.EXTENT, box, Image.BILINEAR, fillcolor=(10, 10, 10))
    # sombra + moldura
    if v["ring"] > 0.2 or theme == "light":
        base.alpha_composite(_soft_shadow(x, y, w, h, r, theme))
    mask = _rr_mask(x, y, w, h, r).crop((rx0, ry0, rx1, ry1))
    base.paste(patch, (rx0, ry0), mask)
    base.alpha_composite(_ring(x, y, w, h, r, round(v["ring"], 1), round(v["gl"], 2), theme))
    if pop <= 0.01: return None
    mbox = (sx0 / 2, sy0 / 2, sx1 / 2, sy1 / 2)
    mp = matte.transform((rx1 - rx0, ry1 - ry0), Image.EXTENT, mbox, Image.BILINEAR, fillcolor=0)
    # só o que está ACIMA da borda de cima (e dentro da faixa lateral do cartão)
    lim = np.zeros((ry1 - ry0, rx1 - rx0), np.float32)
    edge = y + r * 0.55 - ry0
    yy = np.arange(ry1 - ry0)[:, None]
    lim[:] = np.clip((edge - yy) / 6.0, 0, 1)
    xx = np.arange(rx1 - rx0)[None, :] + rx0
    side = np.clip(np.minimum(xx - (x - 10), (x + w + 10) - xx) / 20.0, 0, 1)
    a = (np.asarray(mp, np.float32) / 255.0) * lim * side * pop
    a = np.clip((a - 0.04) * 1.08, 0, 1)
    head_l = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    pr = patch.convert("RGBA"); pr.putalpha(Image.fromarray((a * 255).astype(np.uint8), "L"))
    head_l.paste(pr, (rx0, ry0))
    return head_l

# ---------------------------------------------------------------- legenda palavra a palavra
@lru_cache(512)
def palavra_spr(txt, style, theme, size=62):
    """style: 'n' normal, 'acc' destaque colorido com brilho, 'ser' serif itálico condensado CAIXA ALTA."""
    on_video = theme in ("video",)
    fg = WHITE if theme in ("video", "dark") else INK
    if style == "ser":
        im = text_img(txt.upper(), "serif_i", size * TEMA["ser"], fg)
    elif style == "acc":
        im = text_img(txt, "bold", size, ACC2 if theme != "light" else ACC)
    else:
        im = text_img(txt, "bold", size, fg)
    if style == "acc":
        im = glow(im, 16, ACC, 0.95)
    elif theme in ("video", "dark"):
        im = glow(im, 14, (0, 0, 0), 0.55)
    return im

class Legenda:
    """grupos = [(t_ini, t_fim, [(palavra, t_palavra, estilo), ...]), ...]"""
    def __init__(s, grupos, y=1450, size=62, maxw=900):
        s.g, s.y, s.size, s.maxw = grupos, y, size, maxw
    def draw(s, base, t, theme_fn):
        for (g0, g1, ws) in s.g:
            if not (g0 - 0.05 <= t <= g1 + 0.12): continue
            th = theme_fn(t)
            sprs = [palavra_spr(w, st, th, s.size) for (w, tw_, st) in ws]
            gap = int(s.size * 0.28)
            A = lambda sp: sp.info.get("adv", sp.width); L = lambda sp: sp.info.get("l", 0)
            # quebra em linhas
            lines, cur, cw = [], [], 0
            for i, sp in enumerate(sprs):
                if cur and cw + A(sp) + gap > s.maxw:
                    lines.append(cur); cur, cw = [], 0
                cur.append(i); cw += A(sp) + gap
            lines.append(cur)
            q = lin(t, g1, g1 + 0.11)
            lh = s.size * 1.25
            y0 = s.y - (len(lines) - 1) * lh / 2
            for li, idx in enumerate(lines):
                base_y = max(sprs[i].info.get("base", 0) for i in idx)
                wsum = sum(A(sprs[i]) for i in idx) + gap * (len(idx) - 1)
                x = W / 2 - wsum / 2
                for i in idx:
                    sp = sprs[i]; tw_ = ws[i][1]
                    p = lin(t, tw_ - 0.04, tw_ + 0.2)
                    if p <= 0: x += A(sp) + gap; continue
                    a = eout(p) * (1 - eio(q)); bl = (1 - eout(p)) * 9 + eio(q) * 8
                    dy = (1 - eout5(p)) * 22 - eio(q) * 10
                    cy = y0 + li * lh + (sp.height / 2 - sp.info.get("base", sp.height / 2)) + dy
                    put(base, sp, x - L(sp) + sp.width / 2, cy, mix(0.92, 1, eout(p)), 0, a, bl)
                    x += A(sp) + gap

# ---------------------------------------------------------------- leitura / escrita de vídeo
class Fonte:
    """Lê o vídeo (1620×2880) e a máscara (540×960) em sequência. Depois do fim repete o último quadro."""
    def __init__(s, path, matte):
        s.p = subprocess.Popen([FFM, "-v", "error", "-i", path, "-vf", f"scale={int(W*DEC)}:{int(H*DEC)}:flags=bicubic",
                                "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], stdout=subprocess.PIPE, bufsize=10**8)
        s.m = subprocess.Popen([FFM, "-v", "error", "-i", matte, "-f", "rawvideo", "-pix_fmt", "gray", "-"],
                               stdout=subprocess.PIPE, bufsize=10**7)
        s.last = None; s.i = -1
    def next(s):
        n = int(W * DEC) * int(H * DEC) * 3
        raw = s.p.stdout.read(n); mr = s.m.stdout.read(540 * 960)
        if len(raw) == n and len(mr) == 540 * 960:
            s.i += 1
            s.last = (Image.frombuffer("RGB", (int(W * DEC), int(H * DEC)), raw, "raw", "RGB", 0, 1),
                      Image.frombuffer("L", (540, 960), mr, "raw", "L", 0, 1), s.i)
        return s.last

def quadro_em(path, matte, t):
    """Um quadro avulso (para folhas de teste)."""
    def grab(p, vf, fmt, n):
        return subprocess.run([FFM, "-v", "error", "-ss", f"{t:.3f}", "-i", p, "-frames:v", "1", "-vf", vf, "-f", "rawvideo",
                               "-pix_fmt", fmt, "-"], capture_output=True).stdout[:n]
    n = int(W * DEC) * int(H * DEC) * 3
    raw = grab(path, f"scale={int(W*DEC)}:{int(H*DEC)}:flags=bicubic", "rgb24", n)
    mr = grab(matte, "null", "gray", 540 * 960)
    return (Image.frombuffer("RGB", (int(W * DEC), int(H * DEC)), raw, "raw", "RGB", 0, 1),
            Image.frombuffer("L", (540, 960), mr, "raw", "L", 0, 1), int(round(t * FPS)))

class Saida:
    def __init__(s, path, crf=16):
        s.p = subprocess.Popen([FFM, "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}",
                                "-r", f"{FPS_NUM}/{FPS_DEN}", "-i", "-", "-c:v", "libx264", "-preset", "medium", "-crf", str(crf),
                                "-pix_fmt", "yuv420p", "-movflags", "+faststart", path], stdin=subprocess.PIPE)
    def write(s, im): s.p.stdin.write(im.convert("RGB").tobytes())
    def close(s): s.p.stdin.close(); s.p.wait()

# ---------------------------------------------------------------- cenas
class Cena:
    def __init__(s, t0, t1, theme, modo, els=(), zoom=None):
        s.t0, s.t1, s.theme, s.modo, s.els, s.zoom = t0, t1, theme, modo, list(els), zoom

class Edicao:
    """Junta cenas, transições (fundo + moldura interpolados), elementos e legenda."""
    def __init__(s, cenas, legenda, track, trans=0.42, dur=None):
        s.c, s.leg, s.tr, s.T = cenas, legenda, track, trans
        s.dur = dur or cenas[-1].t1
    def _idx(s, t):
        for i, c in enumerate(s.c):
            if t < c.t1: return i
        return len(s.c) - 1
    def estado(s, t):
        i = s._idx(t); c = s.c[i]
        modo, theme_k = c.modo, (1.0 if c.theme == "dark" else 0.0)
        # transição de entrada desta cena (centrada no corte)
        if i > 0:
            p = lin(t, c.t0 - s.T * 0.5, c.t0 + s.T * 0.5)
            if p < 1:
                pv = s.c[i - 1]; k = eio5(p)
                modo = pv.modo.lerp(c.modo, k)
                theme_k = mix(1.0 if pv.theme == "dark" else 0.0, theme_k, k)
        if i + 1 < len(s.c):
            nx = s.c[i + 1]; p = lin(t, nx.t0 - s.T * 0.5, nx.t0 + s.T * 0.5)
            if p > 0:
                k = eio5(p); modo = c.modo.lerp(nx.modo, k)
                theme_k = mix(theme_k, 1.0 if nx.theme == "dark" else 0.0, k)
        return modo, theme_k, c
    def frame(s, t, src, matte, fi):
        modo, thk, c = s.estado(t)
        bg = fundo("light") if thk < 0.002 else (fundo("dark") if thk > 0.998 else
             Image.blend(fundo("light"), fundo("dark"), eio(thk)))
        base = bg.copy()
        theme = "dark" if thk > 0.5 else "light"
        t_end = c.t1
        cur = [c]
        i = s.c.index(c)
        if i > 0: cur.insert(0, s.c[i - 1])
        if i + 1 < len(s.c): cur.append(s.c[i + 1])
        for cc in cur:
            for e in cc.els:
                if e.layer == "back": e.draw(base, t, cc.t1)
        zoom = 1.0
        if c.zoom: zoom = c.zoom(t)
        head = s.tr.at(fi)
        head_l = compor_video(base, src, matte, head, modo, theme, zoom)
        if head_l is not None: base.alpha_composite(head_l)
        for cc in cur:
            for e in cc.els:
                if e.layer == "front": e.draw(base, t, cc.t1)
        on_video = modo.v["w"] > 600 and modo.v["y"] < 1300
        s.leg.draw(base, t, lambda tt: "video" if on_video else theme)
        return base


# ---------------------------------------------------------------- amostra do tema (aprovar as cores antes do render)
def amostra(saida):
    """Folha lado a lado (fundo 'light' e 'dark') com os componentes no tema atual."""
    folhas = []
    for th in ("light", "dark"):
        b = fundo(th).copy()
        def put(im, x, y): b.alpha_composite(im, (int(x - im.width / 2), int(y - im.height / 2)))
        claro = th == "light" and not UI_ESCURA and _lum(PAPER) >= 0.5
        put(text_img("TEMA " + TEMA["nome"].upper(), "black", 92, INK if claro else WHITE), W / 2, 330)
        put(text_img("nova profissão", "serif_i", 84, ACC), W / 2, 450)
        put(pill("QUAL PROFISSÃO?", "send", 46, glow_col=ACC), W / 2, 620)
        put(chip("auditoria de segurança", "shield"), W / 2, 770)
        put(card("Peter Parker", "fotógrafo · esquecido", "camera", theme=th, extra=status("R$ 0", ok=False)), W / 2, 950)
        put(glass_window(700, 300, "Conversa", theme=th), W / 2, 1240)
        put(badge("camera"), 300, 1510); put(badge("help", fill=INK, fg=WHITE), 780, 1510)
        lg = hstack([palavra_spr("a", "n", th), palavra_spr("nova", "ser", th), palavra_spr("profissão", "acc", th)], gap=18, valign="c")
        put(lg, W / 2, 1720)
        folhas.append(b.convert("RGB"))
    out = Image.new("RGB", (W * 2 + 40, H), (40, 40, 40))
    out.paste(folhas[0], (0, 0)); out.paste(folhas[1], (W + 40, 0))
    out.resize((out.width // 2, out.height // 2), Image.LANCZOS).save(saida, quality=90)
    print("amostra:", saida, "| tema:", TEMA["nome"], "| fundo escuro:", FUNDO_ESCURO, "| destaque:", "#%02X%02X%02X" % ACC)

def amostra_fundos(saida):
    """Folha com os estilos de fundo escuro lado a lado (pra pessoa escolher no passo 0)."""
    global GLASS, FUNDO_ESCURO
    antes = GLASS, FUNDO_ESCURO
    nomes = ["brilho"] + list(FUNDOS_ESCUROS)
    rot = {"brilho": "BRILHO (original)", "cinza-grao": "CINZA GRÃO", "grid-cinza": "GRID CINZA",
           "grid-azul": "GRID AZUL", "azul-grao": "AZUL GRÃO", "cinza-azul": "CINZA + AZUL"}
    folhas = []
    for n in nomes:
        FUNDO_ESCURO = n; GLASS = _hex(FUNDOS_ESCUROS.get(n, TEMA["glass"])); fundo.cache_clear()
        b = fundo("dark").copy()
        def put(im, x, y): b.alpha_composite(im, (int(x - im.width / 2), int(y - im.height / 2)))
        put(text_img(rot[n], "black", 80, WHITE), W / 2, 330)
        put(text_img(n, "mono", 40, GRAY, track=0.1), W / 2, 430)
        put(pill("QUAL PROFISSÃO?", "send", 46, glow_col=ACC), W / 2, 620)
        put(card("Peter Parker", "fotógrafo · esquecido", "camera", theme="dark", extra=status("R$ 0", ok=False)), W / 2, 900)
        put(glass_window(700, 300, "Conversa", theme="dark"), W / 2, 1220)
        lg = hstack([palavra_spr("a", "n", "dark"), palavra_spr("nova", "ser", "dark"), palavra_spr("profissão", "acc", "dark")], gap=18, valign="c")
        put(lg, W / 2, 1650)
        folhas.append(b.convert("RGB"))
    GLASS, FUNDO_ESCURO = antes; fundo.cache_clear()
    col = 3; lin = (len(folhas) + col - 1) // col; gap = 30
    out = Image.new("RGB", (W * col + gap * (col - 1), H * lin + gap * (lin - 1)), (40, 40, 40))
    for i, f in enumerate(folhas):
        out.paste(f, ((i % col) * (W + gap), (i // col) * (H + gap)))
    out.resize((out.width // 3, out.height // 3), Image.LANCZOS).save(saida, quality=90)
    print("fundos:", saida)

if __name__ == "__main__":
    import sys
    if len(sys.argv) >= 3 and sys.argv[1] == "amostra": amostra(sys.argv[2])
    elif len(sys.argv) >= 3 and sys.argv[1] == "fundos": amostra_fundos(sys.argv[2])
    else: print("uso: python -I mp.py amostra saida.jpg   (MP_TEMA=classico | ai-lab | caminho/tema.json; MP_FUNDO=grid-cinza…)\n"
                "     python -I mp.py fundos saida.jpg    (folha com todos os estilos de fundo escuro)")

