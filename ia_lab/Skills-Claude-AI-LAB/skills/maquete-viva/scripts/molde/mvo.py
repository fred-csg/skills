import sys as _s, os as _o
_s.path.insert(0, _o.path.dirname(_o.path.dirname(_o.path.abspath(__file__))))  # scripts/ (ambiente.py)
import ambiente
# Maquete Viva — camada de interface reutilizável da série (PIL 2x + ffmpeg).
# Cada vídeo: overlay.py define C = Cfg(...) e chama mvo.main(C).
import sys, json, math, os, subprocess, argparse
from functools import lru_cache
from PIL import Image, ImageDraw, ImageFont, ImageFilter

W, H = 1080, 1920
SAFE = (90, 300, 900, 1220)
CX = (SAFE[0] + SAFE[2]) // 2
SS = 2
FFM = ambiente.ffmpeg()

# Fontes do Windows; no Mac (ou sem elas) usa equivalentes do sistema.
_ALT = {"segoeuib.ttf": ("Poppins-Bold.ttf", "arialbd.ttf", "Arial Bold.ttf", "DejaVuSans-Bold.ttf"),
        "segoeui.ttf": ("Poppins-Regular.ttf", "arial.ttf", "Arial.ttf", "DejaVuSans.ttf"),
        "seguibl.ttf": ("Poppins-Black.ttf", "ariblk.ttf", "Arial Black.ttf", "DejaVuSans-Bold.ttf"),
        "consolab.ttf": ("CascadiaMono.ttf", "Menlo.ttc", "Courier New Bold.ttf", "courbd.ttf", "DejaVuSansMono-Bold.ttf"),
        "seguisym.ttf": ("Segoe UI Symbol.ttf", "Apple Symbols.ttf", "Arial Unicode.ttf", "DejaVuSans.ttf")}
_FPC = {}
def fpath(name):
    if name not in _FPC:
        p = ambiente.achar_fonte(name, *_ALT.get(name, ()))
        if not p: raise FileNotFoundError(f"fonte {name} (e alternativas) não encontrada")
        _FPC[name] = p
    return _FPC[name]
def font(name, size): return ImageFont.truetype(fpath(name), int(size * SS))
F_CAP = font("segoeuib.ttf", 50)
F_MONO = font("consolab.ttf", 25)
F_MONO_S = font("consolab.ttf", 17)
F_MONO_M = font("consolab.ttf", 21)
F_NUM = font("consolab.ttf", 62)
F_CHIPN = font("segoeuib.ttf", 30)
F_TITLE_N = font("seguibl.ttf", 230)
F_TITLE = font("seguibl.ttf", 64)
F_BIG = font("seguibl.ttf", 92)
F_B34 = font("segoeuib.ttf", 34)
F_B40 = font("segoeuib.ttf", 40)
F_R24 = font("segoeui.ttf", 24)
F_SYM = font("seguisym.ttf", 25)

DARK = (30, 30, 34); WHITE = (255, 255, 255)
COL = dict(orange=(240, 127, 46), red=(229, 72, 77), purple=(123, 91, 214), blue=(47, 124, 246), green=(37, 165, 95),
           yellow=(242, 179, 61), teal=(48, 170, 160), pink=(226, 92, 140))
def _redes():
    """redes.json na pasta da skill: [["youtube","@canal"],["instagram","@perfil"],["tiktok","@perfil"]] (rode instalar.py --redes)."""
    import json
    p = os.path.join(ambiente.SKILL, "redes.json")
    try: return [tuple(x) for x in json.load(open(p, encoding="utf-8"))]
    except Exception: return [("youtube", "@seu_canal"), ("instagram", "@seu_perfil"), ("tiktok", "@seu_perfil")]
HANDLES = _redes()

def ease(a): a = max(0., min(1., a)); return a * a * a * (a * (a * 6 - 15) + 10)
def eout(a): a = max(0., min(1., a)); return 1 - (1 - a) ** 3
def eback(a):
    a = max(0., min(1., a)); c1 = 1.70158; c3 = c1 + 1
    return 1 + c3 * (a - 1) ** 3 + c1 * (a - 1) ** 2
def lerp(a, b, k): return a + (b - a) * k
def env(t, t0, t1, fi=0.25, fo=0.2):
    if t < t0 or t > t1: return 0.0
    return min(eout((t - t0) / fi), 1 - ease((t - (t1 - fo)) / fo) if t > t1 - fo else 1.0)

SHADOW = False
def paste(base, el, x, y, alpha=1.0, scale=1.0, anchor="tl", shadow=None):
    w, h = el.size[0] / SS * scale, el.size[1] / SS * scale
    if w < 1 or h < 1 or alpha <= 0.01: return
    im = el.resize((max(1, int(round(w))), max(1, int(round(h)))), Image.LANCZOS)
    if alpha < 1:
        a = im.getchannel("A").point(lambda v: int(v * alpha)); im.putalpha(a)
    if anchor == "c": x, y = x - im.size[0] / 2, y - im.size[1] / 2
    elif anchor == "tc": x = x - im.size[0] / 2
    elif anchor == "bc": x, y = x - im.size[0] / 2, y - im.size[1]
    if (SHADOW if shadow is None else shadow) and im.size[0] > 30:
        pad = 28
        sh = Image.new("RGBA", (im.size[0] + 2 * pad, im.size[1] + 2 * pad), (0, 0, 0, 0))
        m = im.getchannel("A").point(lambda v: int(v * 0.32))
        blk = Image.new("RGBA", im.size, (20, 16, 40, 255)); blk.putalpha(m)
        sh.alpha_composite(blk, (pad, pad)); sh = sh.filter(ImageFilter.GaussianBlur(11))
        base.alpha_composite(sh, (int(round(x)) - pad, int(round(y)) - pad + 9))
    base.alpha_composite(im, (int(round(x)), int(round(y))))
def rr(d, box, r, fill=None, outline=None, width=0):
    d.rounded_rectangle([int(v) for v in box], radius=int(r), fill=fill, outline=outline, width=int(width))

def txt(d, xy, s, f, fill, anchor="lm"):
    """texto com fallback de símbolo (✓ ✕ ♥ ▶ °)."""
    x, y = xy
    if not any(c in s for c in "✓✕♥▶●♪"):
        d.text((x, y), s, font=f, fill=fill, anchor=anchor); return
    sym = ImageFont.truetype(fpath("seguisym.ttf"), f.size)
    parts = []; cur = ""
    for c in s:
        if c in "✓✕♥▶●♪":
            if cur: parts.append((cur, f)); cur = ""
            parts.append((c, sym))
        else: cur += c
    if cur: parts.append((cur, f))
    tw = sum(ff.getlength(p) for p, ff in parts)
    if anchor[0] == "m": x -= tw / 2
    elif anchor[0] == "r": x -= tw
    for p, ff in parts:
        d.text((x, y), p, font=ff, fill=fill, anchor="l" + anchor[1]); x += ff.getlength(p)
def tlen(s, f):
    sym = ImageFont.truetype(fpath("seguisym.ttf"), f.size)
    return sum((sym if c in "✓✕♥▶●♪" else f).getlength(c) for c in s)

class Cfg:
    def __init__(s, **k):
        s.chips = []          # [(n, label, color, t)]
        s.chips_on = (0.0, 1e9)
        s.chips_all = None    # t em que todos acendem
        s.calls = []          # (t0,t1,texto,âncora|None,dx,dy,estilo,cor)
        s.titles = []         # (t0,t1,n,label,cor)   n="" → título-palavra grande
        s.counters = None     # fn(base, t, f)
        s.extra = []          # fns(base,t,f) -> base|None, desenhadas antes dos chips
        s.late = []           # fns desenhadas por cima de tudo (antes da legenda)
        s.phone = None        # (t0, t1)
        s.flash = []          # tempos de flash branco
        s.vignette = []       # (t0,t1,cor rgb)
        s.cta = None          # (t_pergunta, t_redes)
        s.fix = {}
        s.tag = ("ilustrativo", 0.4)
        s.cap_hide = []       # intervalos sem legenda
        s.grade = None        # (saturação, contraste, calor) aplicado no 3D
        s.chip_style = "chips"  # ou "stepper"
        s.shadow = False
        s.steps_hide = []
        s.__dict__.update(k)

# ------------------------------------------------------------------ chips
CHIP_W, CHIP_H, CHIP_GAP = 152, 58, 12
@lru_cache(None)
def chip_img(n, lab, c, state):
    col = COL[c]; w, h = CHIP_W * SS, CHIP_H * SS
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    if state == "active":
        rr(d, (0, 0, w - 1, h - 1), 12 * SS, fill=col + (255,)); tc = WHITE; nc = WHITE
    elif state == "done":
        rr(d, (0, 0, w - 1, h - 1), 12 * SS, fill=(255, 255, 255, 240), outline=col + (255,), width=3 * SS); tc = col; nc = col
    else:
        rr(d, (0, 0, w - 1, h - 1), 12 * SS, fill=(255, 255, 255, 215), outline=(214, 214, 214, 255), width=3 * SS); tc = (165, 165, 165); nc = (175, 175, 175)
    d.text((12 * SS, h / 2), n, font=F_CHIPN, fill=nc, anchor="lm")
    d.text((38 * SS, h / 2 + 1 * SS), lab, font=F_MONO_S, fill=tc, anchor="lm")
    return im
def draw_chips(C, base, t):
    t0, t1 = C.chips_on
    a = env(t, t0, t1, 0.4, 0.4)
    if a <= 0 or not C.chips: return
    k = -1
    for i, ch in enumerate(C.chips):
        if t >= ch[3]: k = i
    final = C.chips_all is not None and t >= C.chips_all
    n = len(C.chips)
    for i, (num, lab, c, tc) in enumerate(C.chips):
        st = "active" if (i == k or final) else ("done" if i < k else "future")
        x = SAFE[0] + i * (CHIP_W + CHIP_GAP)
        sc = 1.0
        if i == k and not final and t - tc < 0.35: sc = 1 + 0.12 * math.sin(min(1, (t - tc) / 0.35) * math.pi)
        if final and t - C.chips_all < 1.2:
            u = (t - C.chips_all - i * 0.08) / 0.3
            if 0 < u < 1: sc = 1 + 0.12 * math.sin(u * math.pi)
        paste(base, chip_img(num, lab, c, st), x + CHIP_W / 2, SAFE[1] + CHIP_H / 2, a, sc, "c")

STEP_X0, STEP_W, STEP_Y, STEP_H = 90, 810, 262, 86
@lru_cache(None)
def steps_img(labels, cols, k, final):
    n = len(labels); w, h = STEP_W * SS, STEP_H * SS
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    rr(d, (0, 0, w - 1, h - 1), 26 * SS, fill=(255, 255, 255, 236), outline=(225, 222, 232, 255), width=2 * SS)
    sw = w / n; fN = font("segoeuib.ttf", 22); fL = font("segoeuib.ttf", 19)
    for i, (lab, c) in enumerate(zip(labels, cols)):
        col = COL[c]; x0 = i * sw
        if i == k and not final:
            rr(d, (x0 + 6 * SS, 7 * SS, x0 + sw - 6 * SS, h - 7 * SS), 21 * SS, fill=col + (255,))
            d.ellipse([x0 + 16 * SS, h / 2 - 17 * SS, x0 + 50 * SS, h / 2 + 17 * SS], fill=WHITE)
            d.text((x0 + 33 * SS, h / 2), str(i + 1), font=fN, fill=col, anchor="mm")
            d.text((x0 + 58 * SS, h / 2), lab, font=fL, fill=WHITE, anchor="lm")
        elif i < k or final:
            d.ellipse([x0 + 16 * SS, h / 2 - 17 * SS, x0 + 50 * SS, h / 2 + 17 * SS], fill=col)
            txt(d, (x0 + 33 * SS, h / 2), "✓", font("segoeuib.ttf", 20), WHITE, "mm")
            d.text((x0 + 58 * SS, h / 2), lab, font=fL, fill=(60, 60, 68), anchor="lm")
        else:
            d.ellipse([x0 + 16 * SS, h / 2 - 17 * SS, x0 + 50 * SS, h / 2 + 17 * SS], outline=(200, 200, 206), width=3 * SS)
            d.text((x0 + 33 * SS, h / 2), str(i + 1), font=fN, fill=(170, 170, 178), anchor="mm")
            d.text((x0 + 58 * SS, h / 2), lab, font=fL, fill=(170, 170, 178), anchor="lm")
    return im
def draw_steps(C, base, t):
    t0, t1 = C.chips_on
    a = env(t, t0, t1, 0.4, 0.4)
    for (h0, h1) in C.steps_hide:
        if h0 - 0.3 <= t <= h1 + 0.3: a *= 1 - min(1.0, (t - (h0 - 0.3)) / 0.3, ((h1 + 0.3) - t) / 0.3)
    if a <= 0.01 or not C.chips: return
    k = -1
    for i, ch in enumerate(C.chips):
        if t >= ch[3]: k = i
    final = C.chips_all is not None and t >= C.chips_all
    labels = tuple(c[1] for c in C.chips); cols = tuple(c[2] for c in C.chips)
    sc = 1.0
    if 0 <= k and t - C.chips[k][3] < 0.3: sc = 1 + 0.03 * math.sin((t - C.chips[k][3]) / 0.3 * math.pi)
    paste(base, steps_img(labels, cols, k, final), STEP_X0 + STEP_W / 2, STEP_Y + STEP_H / 2, a, sc, "c", shadow=True)
    # barra de progresso
    n = len(C.chips); prog = 0.0
    if k >= 0:
        nxt = C.chips[k + 1][3] if k + 1 < n else (C.chips_all or t + 1)
        prog = (k + min(1.0, max(0.0, (t - C.chips[k][3]) / max(0.1, nxt - C.chips[k][3])))) / n
    if final: prog = 1.0
    d = ImageDraw.Draw(base); y = STEP_Y + STEP_H + 12
    d.rounded_rectangle([STEP_X0 + 20, y, STEP_X0 + STEP_W - 20, y + 7], radius=4, fill=(255, 255, 255, int(170 * a)))
    if prog > 0:
        c = COL[C.chips[max(k, 0)][2]]
        d.rounded_rectangle([STEP_X0 + 20, y, STEP_X0 + 20 + (STEP_W - 40) * prog, y + 7], radius=4, fill=c + (int(255 * a),))

# ------------------------------------------------------------------ cards de contador
@lru_cache(None)
def counter_img(num, label, col=None, w=250):
    h = 110
    im = Image.new("RGBA", (w * SS, h * SS), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    oc = COL[col] if col else DARK
    rr(d, (0, 0, w * SS - 1, h * SS - 1), 14 * SS, fill=(255, 255, 255, 245), outline=oc + (255,), width=3 * SS)
    nf = F_NUM if tlen(num, F_NUM) < (w - 40) * SS else font("consolab.ttf", 44)
    txt(d, (22 * SS, 52 * SS), num, nf, oc if col else DARK, "ls")
    d.text((22 * SS, 88 * SS), label, font=F_MONO_S if len(label) > 18 else F_MONO_M, fill=(70, 70, 76), anchor="ls")
    return im
def counter(base, t, t0, t1, num, label, col=None, slot=0, w=None, bump=False):
    a = env(t, t0, t1, 0.35, 0.3)
    if a <= 0: return
    x = SAFE[0] + (0 if slot == 0 else 266)
    paste(base, counter_img(num, label, col, w or (250 if slot == 0 else 290)), x, 378, a, 1.08 if bump else 1.0)

@lru_cache(None)
def tag_img(text):
    tw = F_MONO_S.getlength(text)
    w, h = int(tw + 28 * SS), 30 * SS
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    rr(d, (0, 0, w - 1, h - 1), h / 2, fill=(255, 255, 255, 170), outline=(150, 150, 150, 255), width=2 * SS)
    d.text((w / 2, h / 2), text, font=F_MONO_S, fill=(110, 110, 110), anchor="mm")
    return im

# ------------------------------------------------------------------ legenda karaokê
G = []
def build_caption(C, words_path):
    words = []
    for w in json.load(open(words_path, encoding="utf8")):
        tx = w["w"].strip(); base = tx.strip(".,?!:")
        if base.lower() in C.fix: tx = tx.replace(base, C.fix[base.lower()])
        if tx: words.append(dict(w=tx, s=w["s"], e=w["e"]))
    groups = []; cur = []
    for w in words:
        ln = len(" ".join(x["w"] for x in cur + [w]))
        if cur and ln > 24: groups.append(cur); cur = []
        cur.append(w)
        if w["w"][-1] in ".?:!" or (w["w"][-1] == "," and len(" ".join(x["w"] for x in cur)) >= 12):
            groups.append(cur); cur = []
    if cur: groups.append(cur)
    for i, g in enumerate(groups):
        t0 = g[0]["s"] - 0.12
        t1 = groups[i + 1][0]["s"] - 0.1 if i + 1 < len(groups) else g[-1]["e"] + 1.5
        t1 = min(t1, g[-1]["e"] + 0.9)
        G.append((t0, t1, g))
@lru_cache(None)
def cap_img(gi, nspoken):
    g = G[gi][2]; texts = [w["w"] for w in g]
    sp = F_CAP.getlength(" ")
    tw = sum(F_CAP.getlength(x) for x in texts) + sp * (len(texts) - 1)
    padx, h = 30 * SS, 84 * SS
    w = int(tw + 2 * padx)
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    rr(d, (0, 0, w - 1, h - 1), h / 2, fill=(38, 38, 42, 236))
    x = padx
    for i, tx in enumerate(texts):
        d.text((x, h / 2 + 1 * SS), tx, font=F_CAP, fill=WHITE if i < nspoken else (128, 128, 134), anchor="lm")
        x += F_CAP.getlength(tx) + sp
    return im
def draw_caption(C, base, t, y=1150):
    if any(a <= t <= b for a, b in C.cap_hide): return
    for gi, (t0, t1, g) in enumerate(G):
        if t0 <= t <= t1:
            n = sum(1 for w in g if t >= w["s"] - 0.03)
            a = env(t, t0, t1, 0.12, 0.1)
            sc = 0.94 + 0.06 * eout((t - t0) / 0.18)
            paste(base, cap_img(gi, n), CX, y, a, sc, "c")

# ------------------------------------------------------------------ callouts
@lru_cache(None)
def pill_img(text, style, col, big=False):
    c = COL.get(col, DARK) if col else DARK
    f = font("consolab.ttf", 31) if big else F_MONO
    tw = tlen(text, f)
    w, h = int(tw + 32 * SS), (54 if big else 44) * SS
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    if style == "fill": rr(d, (0, 0, w - 1, h - 1), h / 2, fill=c + (255,)); tc = WHITE
    elif style == "dark": rr(d, (0, 0, w - 1, h - 1), h / 2, fill=DARK + (255,)); tc = WHITE
    else: rr(d, (0, 0, w - 1, h - 1), h / 2, fill=(255, 255, 255, 250), outline=c + (255,), width=3 * SS); tc = c
    txt(d, (w / 2, h / 2 + 1 * SS), text, f, tc, "mm")
    return im
MF = []
def anchor_px(f, key):
    d = MF[min(f, len(MF) - 1)].get(key)
    if not d or d[2] <= 0: return None
    return d[0] * W, d[1] * H
def draw_callouts(C, base, t, f):
    d = ImageDraw.Draw(base)
    for c in C.calls:
        t0, t1, text, key, dx, dy, style, col = c[:8]
        big = len(c) > 8 and c[8]
        if not (t0 <= t <= t1): continue
        a = env(t, t0, t1, 0.3, 0.22)
        im = pill_img(text, style, col, big)
        if key is None:
            paste(base, im, CX + dx, dy, a, 0.6 + 0.4 * eback((t - t0) / 0.3), "c"); continue
        ap_ = anchor_px(f, key)
        if ap_ is None: continue
        ax, ay = ap_
        pw, ph = im.size[0] / SS, im.size[1] / SS
        px = min(max(ax + dx, SAFE[0] + pw / 2), SAFE[2] - pw / 2)
        py = min(max(ay + dy, SAFE[1] + 210 + ph / 2), SAFE[3] - 110 - ph / 2)
        k = eout((t - t0) / 0.25)
        ex, ey = ax + (px - ax) * k, ay + (py - ay) * k
        if 0 <= ax <= W and 0 <= ay <= H and (dx or dy):
            d.line([(ax, ay), (ex, ey)], fill=(DARK + (int(200 * a),)), width=2)
            r = 6
            d.ellipse([ax - r, ay - r, ax + r, ay + r], fill=(255, 255, 255, int(255 * a)), outline=DARK + (int(255 * a),), width=2)
        paste(base, im, px, py, a, 0.6 + 0.4 * eback((t - t0 - 0.12) / 0.3), "c")

# ------------------------------------------------------------------ títulos
@lru_cache(None)
def title_img(n, lab, col):
    w, h = 900 * SS, 420 * SS
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    if n:
        d.text((w / 2, 190 * SS), n, font=F_TITLE_N, fill=COL[col], anchor="mm", stroke_width=9 * SS, stroke_fill=DARK)
        d.text((w / 2, 350 * SS), lab, font=F_TITLE, fill=WHITE, anchor="mm", stroke_width=7 * SS, stroke_fill=DARK)
    else:
        f = F_BIG
        while f.getlength(lab) > (w - 40 * SS): f = font("seguibl.ttf", f.size / SS - 6)
        d.text((w / 2, h / 2), lab, font=f, fill=COL[col], anchor="mm", stroke_width=8 * SS, stroke_fill=DARK)
    return im
def draw_titles(C, base, t):
    for (t0, t1, n, lab, col) in C.titles:
        if t0 <= t <= t1:
            a = env(t, t0, t1, 0.15, 0.25)
            sc = 0.55 + 0.45 * eback((t - t0) / 0.38)
            paste(base, title_img(n, lab, col), CX, 700, a, sc, "c")

# ------------------------------------------------------------------ celular
PH_BOX = (150, 170, 840, 1560)
def phone_k(C, t):
    if not C.phone: return 0.0
    t0, t1 = C.phone
    if t < t0 or t > t1 + 0.1: return 0.0
    return min(ease((t - t0) / 0.8), 1 - ease((t - (t1 - 0.6)) / 0.6))
def draw_phone(C, base, t):
    k = phone_k(C, t)
    if k <= 0: return base
    box = [lerp(0, PH_BOX[0], k), lerp(0, PH_BOX[1], k), lerp(W, PH_BOX[2], k), lerp(H, PH_BOX[3], k)]
    r = 70 * k
    bg = base.filter(ImageFilter.GaussianBlur(18)).convert("RGBA")
    bg.alpha_composite(Image.new("RGBA", (W, H), (246, 241, 232, int(205 * k))))
    mask = Image.new("L", (W, H), 0); ImageDraw.Draw(mask).rounded_rectangle([int(v) for v in box], radius=int(r), fill=255)
    out = Image.composite(base, bg, mask)
    d = ImageDraw.Draw(out)
    bw = int(20 * k)
    if bw > 0:
        d.rounded_rectangle([int(box[0] - bw / 2), int(box[1] - bw / 2), int(box[2] + bw / 2), int(box[3] + bw / 2)], radius=int(r + bw / 2), outline=(28, 28, 32, 255), width=bw)
        cx = (box[0] + box[2]) / 2
        d.rounded_rectangle([int(cx - 70 * k), int(box[1] + 22 * k), int(cx + 70 * k), int(box[1] + 58 * k)], radius=int(18 * k), fill=(20, 20, 24, 255))
        d.rounded_rectangle([int(cx - 90 * k), int(box[3] - 22 * k), int(cx + 90 * k), int(box[3] - 14 * k)], radius=4, fill=(30, 30, 30, 255))
    return out

def rec_badge(base, t, t0, t1):
    a = env(t, t0, t1, 0.25, 0.25)
    if a <= 0: return
    im = Image.new("RGBA", (190 * SS, 56 * SS), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    rr(d, (0, 0, im.size[0] - 1, im.size[1] - 1), 28 * SS, fill=(20, 20, 24, 220))
    blink = 0.5 + 0.5 * math.cos(t * 6)
    d.ellipse([18 * SS, 16 * SS, 42 * SS, 40 * SS], fill=(229, 72, 77, int(120 + 135 * blink)))
    s = int(max(0, t - t0)); d.text((56 * SS, 28 * SS), f"REC 00:{s:02d}", font=F_MONO, fill=WHITE, anchor="lm")
    paste(base, im, 200, 250, a, 0.7 + 0.3 * eback((t - t0) / 0.3))

def play_button(base, t, t0, t1, x=CX, y=860):
    a = env(t, t0, t1, 0.25, 0.25)
    if a <= 0: return
    im = Image.new("RGBA", (170 * SS, 170 * SS), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.ellipse([0, 0, im.size[0] - 1, im.size[1] - 1], fill=(255, 255, 255, 225), outline=DARK, width=4 * SS)
    s = SS; d.polygon([(66 * s, 48 * s), (66 * s, 122 * s), (126 * s, 85 * s)], fill=DARK)
    paste(base, im, x, y, a, 0.6 + 0.4 * eback((t - t0) / 0.35), "c")

@lru_cache(None)
def notif_img(app, msg, col):
    w, h = 700 * SS, 150 * SS
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    rr(d, (0, 0, w - 1, h - 1), 34 * SS, fill=(255, 255, 255, 245), outline=(30, 30, 34, 255), width=3 * SS)
    rr(d, (24 * SS, 30 * SS, 112 * SS, 118 * SS), 22 * SS, fill=COL[col])
    txt(d, (68 * SS, 75 * SS), "♥", font("segoeuib.ttf", 40), WHITE, "mm")
    d.text((136 * SS, 52 * SS), app, font=F_MONO_M, fill=(110, 110, 116), anchor="lm")
    d.text((w - 30 * SS, 52 * SS), "agora", font=F_MONO_S, fill=(140, 140, 146), anchor="rm")
    txt(d, (136 * SS, 100 * SS), msg, F_B34, DARK, "lm")
    return im
def notif(base, t, t0, t1, app, msg, col="teal", y=560):
    a = env(t, t0, t1, 0.3, 0.3)
    if a <= 0: return
    yy = y - 60 * (1 - eout((t - t0) / 0.4))
    paste(base, notif_img(app, msg, col), CX, yy, a, 1.0, "c")

@lru_cache(None)
def list_img(title, items, n, col):
    w = int(max(380, 120 + max(F_B34.getlength(it) for it in items) / SS)); h = 70 + 58 * len(items)
    im = Image.new("RGBA", (w * SS, h * SS), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    rr(d, (0, 0, w * SS - 1, h * SS - 1), 20 * SS, fill=(255, 255, 255, 245), outline=DARK + (255,), width=3 * SS)
    d.text((24 * SS, 38 * SS), title, font=F_MONO_M, fill=(90, 90, 96), anchor="lm")
    for i, it in enumerate(items):
        y = (92 + 58 * i) * SS
        done = i < n
        rr(d, (24 * SS, y - 20 * SS, 64 * SS, y + 20 * SS), 10 * SS, fill=COL[col] if done else (235, 235, 235), outline=None)
        if done: txt(d, (44 * SS, y), "✓", font("segoeuib.ttf", 26), WHITE, "mm")
        d.text((82 * SS, y), it, font=F_B34, fill=DARK if done else (170, 170, 175), anchor="lm")
    return im
def checklist(base, t, t0, t1, title, items, times, col="green", x=None, y=520):
    a = env(t, t0, t1, 0.3, 0.3)
    if a <= 0: return
    n = sum(1 for tt in times if t >= tt)
    im = list_img(title, tuple(items), n, col)
    xx = SAFE[2] - im.size[0] / SS if x is None else x
    paste(base, im, xx, y, a, 1.0)

# ------------------------------------------------------------------ CTA padrão da série
def _icon(kind, s):
    im = Image.new("RGBA", (s, s), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    if kind == "youtube":
        rr(d, (0, s * 0.15, s - 1, s * 0.85), s * 0.2, fill=(255, 0, 0))
        d.polygon([(s * 0.4, s * 0.33), (s * 0.4, s * 0.67), (s * 0.7, s * 0.5)], fill=WHITE)
    elif kind == "instagram":
        g = Image.new("RGBA", (s, s))
        stops = [(254, 196, 60), (230, 50, 110), (131, 58, 180)]
        gd = ImageDraw.Draw(g)
        for i in range(2 * s):
            k = i / (2 * s)
            a, b, u = (stops[0], stops[1], k * 2) if k < 0.5 else (stops[1], stops[2], (k - 0.5) * 2)
            c = tuple(int(lerp(a[j], b[j], u)) for j in range(3))
            gd.line([(i, s), (i - s, 0)], fill=c + (255,), width=2)
        m = Image.new("L", (s, s), 0); ImageDraw.Draw(m).rounded_rectangle([0, 0, s - 1, s - 1], radius=int(s * 0.26), fill=255)
        im.paste(g, (0, 0), m); d = ImageDraw.Draw(im)
        lw = max(2, int(s * 0.07))
        rr(d, (s * 0.2, s * 0.2, s * 0.8, s * 0.8), s * 0.17, outline=WHITE, width=lw)
        d.ellipse([s * 0.36, s * 0.36, s * 0.64, s * 0.64], outline=WHITE, width=lw)
        d.ellipse([s * 0.66, s * 0.27, s * 0.73, s * 0.34], fill=WHITE)
    else:
        rr(d, (0, 0, s - 1, s - 1), s * 0.24, fill=(15, 15, 18))
        fn = ImageFont.truetype(fpath("seguisym.ttf"), int(s * 0.62))
        d.text((s * 0.53, s * 0.53), "♪", font=fn, fill=(37, 244, 238), anchor="mm")
        d.text((s * 0.57, s * 0.5), "♪", font=fn, fill=(254, 44, 85), anchor="mm")
        d.text((s * 0.55, s * 0.515), "♪", font=fn, fill=WHITE, anchor="mm")
    return im
@lru_cache(None)
def cta_head():
    w, h = 820 * SS, 250 * SS
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.text((w / 2, 60 * SS), "Quer aprender a fazer", font=F_B40, fill=DARK, anchor="mm")
    d.text((w / 2, 118 * SS), "vídeos assim?", font=font("seguibl.ttf", 66), fill=DARK, anchor="mm")
    rr(d, (w / 2 - 300 * SS, 166 * SS, w / 2 + 300 * SS, 226 * SS), 30 * SS, fill=COL["orange"])
    d.text((w / 2, 196 * SS), "automático, usando IA", font=font("consolab.ttf", 30), fill=WHITE, anchor="mm")
    return im
@lru_cache(None)
def cta_row(i):
    kind, handle = HANDLES[i]
    w, h = 620 * SS, 104 * SS
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    rr(d, (0, 0, w - 1, h - 1), 26 * SS, fill=(255, 255, 255, 250), outline=DARK + (255,), width=3 * SS)
    ic = _icon(kind, 72 * SS); im.alpha_composite(ic, (18 * SS, 16 * SS))
    d.text((112 * SS, 52 * SS), handle, font=font("segoeuib.ttf", 40), fill=DARK, anchor="lm")
    d.text((w - 26 * SS, 52 * SS), {"youtube": "YouTube", "instagram": "Instagram", "tiktok": "TikTok"}[kind], font=F_MONO_M, fill=(130, 130, 136), anchor="rm")
    return im
def draw_cta(C, base, t):
    if not C.cta: return base
    t0, t_redes = C.cta
    if t < t0: return base
    k = ease((t - t0) / 0.7)
    bg = base.filter(ImageFilter.GaussianBlur(14 * k + 0.01)).convert("RGBA")
    bg.alpha_composite(Image.new("RGBA", (W, H), (246, 241, 232, int(170 * k))))
    paste(bg, cta_head(), CX, 500, k, 0.75 + 0.25 * eback((t - t0) / 0.45), "c")
    rows_t = t_redes - 0.15
    if t >= rows_t - 2.6:
        lab = pill_img("me segue nas redes", "dark", None)
        paste(bg, lab, CX, 690, env(t, rows_t - 0.3, 1e9, 0.3, 0.2), 0.6 + 0.4 * eback((t - rows_t + 0.3) / 0.3), "c")
    for i in range(len(HANDLES)):
        ti = rows_t + i * 0.22
        if t >= ti:
            paste(bg, cta_row(i), CX, 790 + i * 118, eout((t - ti) / 0.25), 0.6 + 0.4 * eback((t - ti) / 0.35), "c")
    return bg

def draw_flash(C, base, t):
    for t0 in C.flash:
        a = max(0.0, 1 - abs(t - t0) / 0.18)
        if a > 0: base.alpha_composite(Image.new("RGBA", (W, H), (255, 255, 255, int(200 * a))))
    return base
@lru_cache(None)
def vign_mask():
    m = Image.new("L", (W // 4, H // 4), 0); d = ImageDraw.Draw(m)
    for i in range(60):
        k = i / 60; d.rounded_rectangle([int(k * 90), int(k * 160), int(W // 4 - k * 90), int(H // 4 - k * 160)], radius=40, outline=int(255 * (1 - k) ** 2), width=3)
    return m.resize((W, H), Image.BILINEAR).filter(ImageFilter.GaussianBlur(30))
def draw_vignette(C, base, t):
    for (t0, t1, col) in C.vignette:
        a = env(t, t0, t1, 0.3, 0.5)
        if a > 0:
            v = Image.new("RGBA", (W, H), col + (0,)); v.putalpha(vign_mask().point(lambda p: int(p * 0.55 * a)))
            base.alpha_composite(v)
    return base

# ------------------------------------------------------------------ composição
def grade(base, g):
    from PIL import ImageEnhance
    sat, con, warm = g
    rgb = base.convert("RGB")
    rgb = ImageEnhance.Color(rgb).enhance(sat); rgb = ImageEnhance.Contrast(rgb).enhance(con)
    if warm:
        r, gg, b = rgb.split(); r = r.point(lambda v: min(255, int(v * (1 + warm)))); b = b.point(lambda v: int(v * (1 - warm * 0.6)))
        rgb = Image.merge("RGB", (r, gg, b))
    return rgb.convert("RGBA")

def compose(C, frames_dir, f, FPS):
    global SHADOW
    SHADOW = C.shadow
    t = f / FPS
    base = Image.open(os.path.join(frames_dir, f"f{f:05d}.png")).convert("RGBA")
    if base.size != (W, H): base = base.resize((W, H), Image.LANCZOS)
    if C.grade: base = grade(base, C.grade)
    for fn in C.extra:
        r = fn(base, t, f)
        if r is not None: base = r
    base = draw_phone(C, base, t)
    draw_callouts(C, base, t, f)
    base = draw_vignette(C, base, t)
    base = draw_flash(C, base, t)
    if (not C.cta or t < C.cta[0] + 0.3) and phone_k(C, t) < 0.05:
        (draw_steps if C.chip_style == "stepper" else draw_chips)(C, base, t)
        if C.counters: C.counters(base, t, f)
        if C.tag:
            tg = tag_img(C.tag[0]); paste(base, tg, SAFE[2] - tg.size[0] / SS, 392, env(t, C.tag[1], C.cta[0] if C.cta else 1e9, 0.4, 0.3))
    for fn in C.late:
        r = fn(base, t, f)
        if r is not None: base = r
    draw_titles(C, base, t)
    base = draw_cta(C, base, t)
    draw_caption(C, base, t)
    return base

def main(C):
    ap = argparse.ArgumentParser()
    ap.add_argument("frames"); ap.add_argument("words"); ap.add_argument("out")
    ap.add_argument("--audio"); ap.add_argument("--qa"); ap.add_argument("--range"); ap.add_argument("--png"); ap.add_argument("--times")
    A = ap.parse_args()
    meta = json.load(open(os.path.join(A.frames, "meta.json")))
    FPS = meta["fps"]; NF = meta["nf"]; MF.extend(meta["frames"])
    build_caption(C, A.words)
    frames = list(range(0, NF + 1))
    if A.range:
        a, b = A.range.split("-"); frames = [x for x in frames if int(a) <= x <= int(b)]
    if A.times: frames = [int(float(x) * FPS) for x in A.times.split(",")]
    qa = Image.open(A.qa).convert("RGBA").resize((W, H)) if A.qa else None
    if A.png:
        os.makedirs(A.png, exist_ok=True)
        for f in [x for x in frames if os.path.exists(os.path.join(A.frames, f"f{x:05d}.png"))]:
            im = compose(C, A.frames, f, FPS)
            if qa: im.alpha_composite(qa)
            im.convert("RGB").save(os.path.join(A.png, f"o{f:05d}.png"))
        return
    cmd = [FFM, "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-"]
    if A.audio: cmd += ["-i", A.audio, "-af", "loudnorm=I=-14:TP=-1.5:LRA=11,aresample=48000,apad", "-c:a", "aac", "-b:a", "192k", "-shortest"]
    cmd += ["-c:v", "libx264", "-preset", "slow", "-crf", "17", "-pix_fmt", "yuv420p", "-movflags", "+faststart", A.out]
    pr = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    for f in frames:
        im = compose(C, A.frames, f, FPS)
        pr.stdin.write(im.convert("RGB").tobytes())
        if f % 300 == 0: print("overlay", f, flush=True)
    pr.stdin.close(); pr.wait()
    print("OK", A.out)
