# Camada de interface (estilo raiox): chips de capítulo, contador, legenda karaokê, callouts, títulos, celular.
# Uso: python overlay.py <frames_dir> <voz_words.json> <out.mp4> [--qa overlay.png] [--frames a-b] [--png outdir]
import sys, json, math, os, subprocess, argparse
from functools import lru_cache
from PIL import Image, ImageDraw, ImageFont, ImageFilter

ap = argparse.ArgumentParser()
ap.add_argument("frames"); ap.add_argument("words"); ap.add_argument("out")
ap.add_argument("--audio"); ap.add_argument("--qa"); ap.add_argument("--range"); ap.add_argument("--png")
A = ap.parse_args()

W, H = 1080, 1920
SAFE = (90, 300, 900, 1220)
CX = (SAFE[0] + SAFE[2]) // 2
SS = 2  # supersampling dos elementos
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ambiente import achar_fonte, ffmpeg
# Fontes do Windows; no Mac (ou sem elas) usa equivalentes do sistema.
ALT = {"segoeuib.ttf": ("Poppins-Bold.ttf", "arialbd.ttf", "Arial Bold.ttf"),
       "segoeui.ttf": ("Poppins-Regular.ttf", "arial.ttf", "Arial.ttf"),
       "seguibl.ttf": ("Poppins-Black.ttf", "ariblk.ttf", "Arial Black.ttf"),
       "consolab.ttf": ("CascadiaMono.ttf", "Menlo.ttc", "Courier New Bold.ttf", "courbd.ttf")}
@lru_cache(None)
def _fp(name):
    p = achar_fonte(name, *ALT.get(name, ()))
    if not p: raise FileNotFoundError(f"fonte {name} (e alternativas) não encontrada")
    return p
def font(name, size): return ImageFont.truetype(_fp(name), size * SS)
F_CAP = font("segoeuib.ttf", 50)
F_MONO = font("consolab.ttf", 25)
F_MONO_S = font("consolab.ttf", 17)
F_NUM = font("consolab.ttf", 62)
F_CHIPN = font("segoeuib.ttf", 30)
F_TITLE_N = font("seguibl.ttf", 230)
F_TITLE = font("seguibl.ttf", 64)
F_PROF = font("segoeuib.ttf", 34)
F_PROF_S = font("segoeui.ttf", 24)

meta = json.load(open(os.path.join(A.frames, "meta.json")))
FPS = meta["fps"]; NF = meta["nf"]; T = meta["T"]; MF = meta["frames"]

DARK = (30, 30, 34); WHITE = (255, 255, 255)
COL = dict(orange=(240, 127, 46), red=(229, 72, 77), purple=(123, 91, 214), blue=(47, 124, 246), green=(37, 165, 95), yellow=(242, 179, 61))

def ease(a): a = max(0., min(1., a)); return a * a * a * (a * (a * 6 - 15) + 10)
def eout(a): a = max(0., min(1., a)); return 1 - (1 - a) ** 3
def eback(a):
    a = max(0., min(1., a)); c1 = 1.70158; c3 = c1 + 1
    return 1 + c3 * (a - 1) ** 3 + c1 * (a - 1) ** 2
def env(t, t0, t1, fi=0.25, fo=0.2):
    if t < t0 or t > t1: return 0.0
    return min(eout((t - t0) / fi), 1 - ease((t - (t1 - fo)) / fo) if t > t1 - fo else 1.0)

def paste(base, el, x, y, alpha=1.0, scale=1.0, anchor="tl"):
    """el: RGBA em 2x. x,y em 1x."""
    w, h = el.size[0] / SS * scale, el.size[1] / SS * scale
    if w < 1 or h < 1 or alpha <= 0.01: return
    im = el.resize((max(1, int(round(w))), max(1, int(round(h)))), Image.LANCZOS)
    if alpha < 1:
        a = im.getchannel("A").point(lambda v: int(v * alpha)); im.putalpha(a)
    if anchor == "c": x, y = x - im.size[0] / 2, y - im.size[1] / 2
    elif anchor == "tc": x = x - im.size[0] / 2
    elif anchor == "bc": x, y = x - im.size[0] / 2, y - im.size[1]
    base.alpha_composite(im, (int(round(x)), int(round(y))))

def rr(d, box, r, fill=None, outline=None, width=0):
    d.rounded_rectangle([int(v) for v in box], radius=int(r), fill=fill, outline=outline, width=int(width))

# ------------------------------------------------------------------ chips
CHIPS = [("1", "VITRINE", "orange", 0.0), ("2", "PANFLETO", "red", T["panf_title"]), ("3", "FEED", "purple", T["feed"]),
         ("4", "ANÚNCIO", "blue", T["ad"]), ("5", "ORGÂNICO", "green", T["org"])]
CHIP_W, CHIP_H, CHIP_GAP = 152, 58, 12
@lru_cache(None)
def chip_img(i, state):
    n, lab, c, _ = CHIPS[i]; col = COL[c]
    w, h = CHIP_W * SS, CHIP_H * SS
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

def chapter_idx(t):
    k = 0
    for i, ch in enumerate(CHIPS):
        if t >= ch[3]: k = i
    return k

def draw_chips(base, t):
    a = eout((t - 0.15) / 0.4)
    if a <= 0: return
    k = chapter_idx(t); final = t >= T["end"]
    for i in range(5):
        st = "active" if (i == k or final) else ("done" if i < k else "future")
        x = SAFE[0] + i * (CHIP_W + CHIP_GAP)
        # pulso no chip que acabou de ativar
        sc = 1.0
        if i == k and not final: sc = 1 + 0.12 * math.sin(min(1, (t - CHIPS[i][3]) / 0.35) * math.pi) if t - CHIPS[i][3] < 0.35 else 1.0
        if final and t - T["end"] < 1.2:
            u = (t - T["end"] - i * 0.08) / 0.3
            if 0 < u < 1: sc = 1 + 0.12 * math.sin(u * math.pi)
        paste(base, chip_img(i, st), x + CHIP_W / 2, SAFE[1] + CHIP_H / 2, a, sc, "c")

# ------------------------------------------------------------------ cards de contador
@lru_cache(None)
def counter_img(num, label, col=None, w=250):
    h = 110
    im = Image.new("RGBA", (w * SS, h * SS), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    oc = COL[col] if col else DARK
    rr(d, (0, 0, w * SS - 1, h * SS - 1), 14 * SS, fill=(255, 255, 255, 245), outline=oc + (255,), width=3 * SS)
    d.text((22 * SS, 52 * SS), num, font=F_NUM, fill=oc if col else DARK, anchor="ls")
    d.text((22 * SS, 88 * SS), label, font=F_MONO_S if len(label) > 18 else font("consolab.ttf", 21), fill=(70, 70, 76), anchor="ls")
    return im

def draw_counters(base, t, f):
    phone = phone_k(t)
    a = eout((t - 0.4) / 0.4) * (1 - phone)
    v = MF[f]["visits"]
    pv = MF[max(0, f - 6)]["visits"]
    bump = 1.0 + (0.08 if v != pv else 0.0)
    if a > 0:
        paste(base, counter_img(str(v), "visitas na loja", "green" if v > 0 else None), SAFE[0], 378, a, bump)
    # verba do anúncio
    t0, t1 = T["coins"] - 0.2, T["org"] - 0.1
    if t0 <= t <= t1:
        k = (t - T["coins"]) / (T["ad_stop"] - T["coins"])
        val = max(0, int(round(1000 * (1 - max(0, min(1, k))) / 10.0)) * 10)
        lab = "verba do anúncio" if val > 0 else "parou de pagar"
        txt = f"R${val:,}".replace(",", ".")
        paste(base, counter_img(txt, lab, "blue" if val > 0 else "red", 290), SAFE[0] + 266, 378, env(t, t0, t1))
    # dias postando
    t0, t1 = T["post"] - 0.2, T["end"] + 6.0
    if t0 <= t <= t1:
        k = (t - T["post"]) / (64.3 - T["post"])
        day = 1 + int(29 * ease(max(0, min(1, k))))
        paste(base, counter_img(f"dia {day}", "postando conteúdo", "green", 290), SAFE[0] + 266, 378, env(t, t0, t1))

@lru_cache(None)
def tag_img(text):
    tw = F_MONO_S.getlength(text)
    w, h = int(tw + 28 * SS), 30 * SS
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    rr(d, (0, 0, w - 1, h - 1), h / 2, fill=(255, 255, 255, 170), outline=(150, 150, 150, 255), width=2 * SS)
    d.text((w / 2, h / 2), text, font=F_MONO_S, fill=(110, 110, 110), anchor="mm")
    return im

# ------------------------------------------------------------------ legenda karaokê
words = []
FIX = {"descobririam": "descobriam"}
for seg in json.load(open(A.words, encoding="utf8")):
    for w in seg["words"]:
        tx = w["w"].strip()
        base = tx.strip(".,?!:")
        if base.lower() in FIX: tx = tx.replace(base, FIX[base.lower()])
        words.append(dict(w=tx, s=w["s"], e=w["e"]))
groups = []; cur = []
for w in words:
    ln = len(" ".join(x["w"] for x in cur + [w]))
    if cur and ln > 24: groups.append(cur); cur = []
    cur.append(w)
    if w["w"][-1] in ".?:" or (w["w"][-1] == "," and len(" ".join(x["w"] for x in cur)) >= 12):
        groups.append(cur); cur = []
if cur: groups.append(cur)
G = []
for i, g in enumerate(groups):
    t0 = g[0]["s"] - 0.12
    t1 = groups[i + 1][0]["s"] - 0.1 if i + 1 < len(groups) else g[-1]["e"] + 1.5
    t1 = min(t1, g[-1]["e"] + 0.9)
    G.append((t0, t1, g))

@lru_cache(None)
def cap_img(gi, nspoken):
    g = G[gi][2]
    texts = [w["w"] for w in g]
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

def draw_caption(base, t):
    for gi, (t0, t1, g) in enumerate(G):
        if t0 <= t <= t1:
            n = sum(1 for w in g if t >= w["s"] - 0.03)
            a = env(t, t0, t1, 0.12, 0.1)
            sc = 0.94 + 0.06 * eout((t - t0) / 0.18)
            paste(base, cap_img(gi, n), CX, 1150, a, sc, "c")

# ------------------------------------------------------------------ callouts
@lru_cache(None)
def pill_img(text, style, col):
    c = COL.get(col, DARK) if col else DARK
    tw = F_MONO.getlength(text)
    w, h = int(tw + 30 * SS), 44 * SS
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    if style == "fill":
        rr(d, (0, 0, w - 1, h - 1), h / 2, fill=c + (255,)); tc = WHITE
    elif style == "dark":
        rr(d, (0, 0, w - 1, h - 1), h / 2, fill=DARK + (255,)); tc = WHITE
    else:
        rr(d, (0, 0, w - 1, h - 1), h / 2, fill=(255, 255, 255, 250), outline=c + (255,), width=3 * SS); tc = c
    d.text((w / 2, h / 2 + 1 * SS), text, font=F_MONO, fill=tc, anchor="mm")
    return im

# (t0, t1, texto, âncora, dx, dy, estilo, cor)
CALL = [
    (1.8, 4.1, "sua loja", "loja", 0, -150, "line", None),
    (3.0, 6.3, "você", "dono", 110, -40, "line", "yellow"),
    (7.3, 11.6, "vitrine ✓", "vitrine", -150, -130, "line", "green"),
    (9.8, 15.3, "ninguém passa aqui", "rua", 40, -150, "line", "red"),
    (12.6, 15.3, "o movimento está aqui", "avenida", 0, -60, "dark", None),
    (18.0, 21.5, "panfleteiro", "pan", 90, -170, "line", "red"),
    (22.2, 25.5, "descobriram a loja", "loja", 0, -130, "line", "green"),
    (27.5, 30.95, "3 segundos", "lixo", -60, -230, "line", "red"),
    (29.9, 30.95, "lixo", "lixo", 90, -120, "fill", "red"),
    (42.4, 46.0, "panfleteiro pago", "anuncio", -30, -190, "line", "blue"),
    (46.0, 49.4, "milhares de pessoas", None, 0, 900, "fill", "blue"),
    (47.6, 49.8, "funciona rápido ✓", "loja", 0, -120, "line", "green"),
    (50.0, 52.4, "parou ✕", "anuncio", 0, -180, "fill", "red"),
    (56.4, 59.0, "post", "placa0", 60, -110, "line", "green"),
    (57.6, 59.1, "aponta pro seu negócio", "placa2", -40, -150, "line", "green"),
    (59.5, 61.2, "salvou ♥", "share0A", 0, -120, "line", "green"),
    (60.6, 62.0, "compartilhou", "share1A", 0, -130, "line", "green"),
    (61.3, 62.6, "mandou pra um amigo", "share2B", 0, -130, "line", "green"),
    (64.98, 66.4, "anúncio acelera", "anuncio", 0, -180, "fill", "blue"),
    (66.44, 68.6, "conteúdo constrói", "placa0", 0, -150, "fill", "green"),
    (68.6, 72.6, "loja cheia ✓", "loja", 0, -120, "fill", "green"),
]
def anchor_px(f, key):
    d = MF[f].get(key)
    if not d or d[2] <= 0: return None
    if len(d) > 3 and d[3] < 0.05: return None
    return d[0] * W, d[1] * H

def draw_callouts(base, t, f):
    d = ImageDraw.Draw(base)
    for (t0, t1, text, key, dx, dy, style, col) in CALL:
        if not (t0 <= t <= t1): continue
        if key is None:
            a = env(t, t0, t1, 0.3, 0.22)
            paste(base, pill_img(text, style, col), CX + dx, dy, a, 0.6 + 0.4 * eback((t - t0) / 0.3), "c"); continue
        ap_ = anchor_px(f, key)
        if ap_ is None: continue
        ax, ay = ap_
        a = env(t, t0, t1, 0.3, 0.22)
        im = pill_img(text, style, col)
        pw, ph = im.size[0] / SS, im.size[1] / SS
        px = min(max(ax + dx, SAFE[0] + pw / 2), SAFE[2] - pw / 2)
        py = min(max(ay + dy, SAFE[1] + 140 + ph / 2), SAFE[3] - 110 - ph / 2)
        # linha guia
        k = eout((t - t0) / 0.25)
        lc = (COL[col] if (col and style == "line") else DARK) + (int(255 * a),)
        ex, ey = ax + (px - ax) * k, ay + (py - ay) * k
        if 0 <= ax <= W and 0 <= ay <= H:
            d.line([(ax, ay), (ex, ey)], fill=(DARK + (int(200 * a),)), width=2)
            r = 6
            d.ellipse([ax - r, ay - r, ax + r, ay + r], fill=(255, 255, 255, int(255 * a)), outline=DARK + (int(255 * a),), width=2)
        paste(base, im, px, py, a, 0.6 + 0.4 * eback((t - t0 - 0.12) / 0.3), "c")

# ------------------------------------------------------------------ títulos de capítulo
TITLES = [(0.1, 1.75, "1", "VITRINE", "orange"), (T["panf_title"], T["panf_title"] + 1.7, "2", "PANFLETO", "red"),
          (T["feed"], T["feed"] + 1.6, "3", "FEED", "purple"), (T["ad"], T["ad"] + 1.7, "4", "ANÚNCIO", "blue"),
          (T["org"], T["org"] + 1.8, "5", "ORGÂNICO", "green")]
@lru_cache(None)
def title_img(n, lab, col):
    w, h = 820 * SS, 420 * SS
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.text((w / 2, 190 * SS), n, font=F_TITLE_N, fill=COL[col], anchor="mm", stroke_width=9 * SS, stroke_fill=DARK)
    d.text((w / 2, 350 * SS), lab, font=F_TITLE, fill=WHITE, anchor="mm", stroke_width=7 * SS, stroke_fill=DARK)
    return im
def draw_titles(base, t):
    for (t0, t1, n, lab, col) in TITLES:
        if t0 <= t <= t1:
            a = env(t, t0, t1, 0.15, 0.25)
            sc = 0.55 + 0.45 * eback((t - t0) / 0.38)
            paste(base, title_img(n, lab, col), CX, 700, a, sc, "c")

# ------------------------------------------------------------------ celular (rua = feed)
PH_T0, PH_T1 = 33.35, 41.25
PH_BOX = (150, 150, 840, 1590)
def phone_k(t):
    if t < PH_T0 or t > PH_T1 + 0.1: return 0.0
    return min(ease((t - PH_T0) / 0.8), 1 - ease((t - (PH_T1 - 0.6)) / 0.6))
def draw_phone(base, t):
    k = phone_k(t)
    if k <= 0: return base
    box = [lerp(0, PH_BOX[0], k), lerp(0, PH_BOX[1], k), lerp(W, PH_BOX[2], k), lerp(H, PH_BOX[3], k)]
    r = 70 * k
    # fundo fora do celular: cena desfocada e clareada
    bg = base.filter(ImageFilter.GaussianBlur(18)).convert("RGBA")
    veil = Image.new("RGBA", (W, H), (246, 241, 232, int(205 * k)))
    bg.alpha_composite(veil)
    mask = Image.new("L", (W, H), 0); ImageDraw.Draw(mask).rounded_rectangle([int(v) for v in box], radius=int(r), fill=255)
    out = Image.composite(base, bg, mask)
    d = ImageDraw.Draw(out)
    bw = int(20 * k)
    if bw > 0:
        d.rounded_rectangle([int(box[0] - bw / 2), int(box[1] - bw / 2), int(box[2] + bw / 2), int(box[3] + bw / 2)], radius=int(r + bw / 2), outline=(28, 28, 32, 255), width=bw)
        cx = (box[0] + box[2]) / 2
        d.rounded_rectangle([int(cx - 70 * k), int(box[1] + 22 * k), int(cx + 70 * k), int(box[1] + 58 * k)], radius=int(18 * k), fill=(20, 20, 24, 255))
        # barra inferior do app (ícones genéricos)
        yb = box[3] - 70 * k
        d.rectangle([int(box[0]), int(yb - 20 * k), int(box[2]), int(box[3] - 40 * k)], fill=(255, 255, 255, int(235 * k)))
        for i in range(5):
            x = box[0] + (box[2] - box[0]) * (i + 0.5) / 5
            s = 15 * k
            if i == 0: d.polygon([(x, yb - s - 6), (x - s - 2, yb - 4), (x + s + 2, yb - 4)], fill=DARK)
            elif i == 2: d.rounded_rectangle([int(x - s), int(yb - s - 4), int(x + s), int(yb + s - 4)], radius=6, outline=DARK, width=4)
            elif i == 4: d.ellipse([int(x - s), int(yb - s - 4), int(x + s), int(yb + s - 4)], fill=COL["orange"])
            else: d.ellipse([int(x - s * 0.8), int(yb - s * 0.8 - 4), int(x + s * 0.8), int(yb + s * 0.8 - 4)], outline=DARK, width=4)
        d.rounded_rectangle([int(cx - 90 * k), int(box[3] - 22 * k), int(cx + 90 * k), int(box[3] - 14 * k)], radius=4, fill=(30, 30, 30, 255))
    return out
def lerp(a, b, k): return a + (b - a) * k

def draw_swipe(base, t):
    t0, t1 = 36.95, 38.45
    if not (t0 <= t <= t1): return
    u = ((t - t0) / 0.75) % 1.0
    y = lerp(1120, 640, ease(u)); a = math.sin(u * math.pi)
    d = ImageDraw.Draw(base); x = 640; r = 38
    d.ellipse([x - r, y - r, x + r, y + r], fill=(255, 255, 255, int(150 * a)), outline=(30, 30, 34, int(200 * a)), width=4)
    for k in range(1, 6):
        yy = y + k * 26; aa = a * (1 - k / 6)
        d.ellipse([x - 10, yy - 10, x + 10, yy + 10], fill=(255, 255, 255, int(120 * aa)))

@lru_cache(None)
def profile_img():
    w, h = 600 * SS, 250 * SS
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    rr(d, (0, 0, w - 1, h - 1), 26 * SS, fill=(255, 255, 255, 238), outline=DARK + (255,), width=3 * SS)
    d.ellipse([28 * SS, 30 * SS, 138 * SS, 140 * SS], fill=COL["orange"], outline=DARK, width=3 * SS)
    d.text((83 * SS, 85 * SS), "L", font=F_PROF, fill=WHITE, anchor="mm")
    d.text((165 * SS, 58 * SS), "@sualoja", font=F_PROF, fill=DARK, anchor="lm")
    for i, (n, l) in enumerate([("128", "posts"), ("2,4 mil", "seguidores"), ("312", "seguindo")]):
        x = 165 * SS + i * 140 * SS
        d.text((x, 106 * SS), n, font=font("segoeuib.ttf", 26), fill=DARK, anchor="lm")
        d.text((x, 134 * SS), l, font=F_PROF_S, fill=(110, 110, 116), anchor="lm")
    rr(d, (28 * SS, 168 * SS, w - 28 * SS, 222 * SS), 14 * SS, fill=COL["purple"])
    d.text((w / 2, 195 * SS), "vitrine = perfil", font=F_MONO, fill=WHITE, anchor="mm")
    return im
def draw_profile(base, t):
    t0, t1 = 39.95, 41.25
    if t0 <= t <= t1:
        paste(base, profile_img(), CX, 560, env(t, t0, t1, 0.25, 0.25), 0.7 + 0.3 * eback((t - t0) / 0.35), "c")

def draw_vignette(base, t):
    a = env(t, 49.96, 52.4, 0.3, 0.5)
    if a <= 0: return base
    v = vign_mask()
    red = Image.new("RGBA", (W, H), (205, 40, 50, 0)); red.putalpha(v.point(lambda p: int(p * 0.55 * a)))
    base.alpha_composite(red); return base
@lru_cache(None)
def vign_mask():
    m = Image.new("L", (W // 4, H // 4), 0); d = ImageDraw.Draw(m)
    for i in range(60):
        k = i / 60; d.rounded_rectangle([int(k * 90), int(k * 160), int(W // 4 - k * 90), int(H // 4 - k * 160)], radius=40, outline=int(255 * (1 - k) ** 2), width=3)
    return m.resize((W, H), Image.BILINEAR).filter(ImageFilter.GaussianBlur(30))

# ------------------------------------------------------------------ composição
def compose(f):
    t = f / FPS
    p = os.path.join(A.frames, f"f{f:05d}.png")
    base = Image.open(p).convert("RGBA")
    if base.size != (W, H): base = base.resize((W, H), Image.LANCZOS)
    base = draw_phone(base, t)
    draw_swipe(base, t)
    draw_callouts(base, t, f)
    base = draw_vignette(base, t)
    draw_chips(base, t)
    draw_counters(base, t, f)
    tg = tag_img("ilustrativo"); paste(base, tg, SAFE[2] - tg.size[0] / SS, 392, eout((t - 0.4) / 0.4))
    draw_profile(base, t)
    draw_titles(base, t)
    draw_caption(base, t)
    return base

frames = list(range(0, NF + 1))
if A.range:
    a, b = A.range.split("-"); frames = [x for x in frames if int(a) <= x <= int(b)]
qa = Image.open(A.qa).convert("RGBA").resize((W, H)) if A.qa else None

if A.png:
    os.makedirs(A.png, exist_ok=True)
    for f in [x for x in frames if os.path.exists(os.path.join(A.frames, f"f{x:05d}.png"))]:
        im = compose(f)
        if qa: im.alpha_composite(qa)
        im.convert("RGB").save(os.path.join(A.png, f"o{f:05d}.png"))
    sys.exit(0)

FFM = ffmpeg()
cmd = [FFM, "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-"]
if A.audio: cmd += ["-i", A.audio, "-af", "loudnorm=I=-14:TP=-1.5:LRA=11,aresample=48000,apad", "-c:a", "aac", "-b:a", "192k", "-shortest"]
cmd += ["-c:v", "libx264", "-preset", "slow", "-crf", "17", "-pix_fmt", "yuv420p", "-movflags", "+faststart", A.out]
pr = subprocess.Popen(cmd, stdin=subprocess.PIPE)
for f in frames:
    im = compose(f)
    if qa: im.alpha_composite(qa)
    pr.stdin.write(im.convert("RGB").tobytes())
    if f % 150 == 0: print("overlay", f, flush=True)
pr.stdin.close(); pr.wait()
print("OK", A.out)
