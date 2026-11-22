# Roteiro de edição "etiqueta-brutal" — Donos de negócio (impulsionar post ruim)
# Uso: python roteiro.py <video_fonte> <saida_sem_audio.mp4> [inicio fim]  (inicio/fim = preview parcial)
import sys, json, math, random
from eb import *

SRC, OUT = sys.argv[1], sys.argv[2]
T0 = float(sys.argv[3]) if len(sys.argv) > 3 else 0.0
T1 = float(sys.argv[4]) if len(sys.argv) > 4 else None
HERE = os.path.dirname(os.path.abspath(__file__))
PW = json.load(open(os.path.join(HERE, "fonte", "palavras.json"), encoding="utf8"))
FIX = {"panflete": "panfleto", "200,": "200,"}
for w in PW: w["w"] = FIX.get(w["w"], w["w"])
S = [w["s"] for w in PW]

SRC_END = 25.0          # último instante útil do vídeo-fonte
DUR = 26.5              # +1,5 s de congelado com CTA
MARCA = ("LK", "motion")

# ---------------------------------------------------------------- legendas (grupos de palavras)
# (i0, i1, destaques, cor, y)
G = [(0, 2, (2,), "amarelo", 1150), (3, 5, (5,), "amarelo", 1150),
     (6, 9, (8, 9), "amarelo", 1150), (10, 14, (13, 14), "amarelo", 1150),
     (15, 19, (19,), "amarelo", 1150),
     (21, 24, (23, 24), "vermelho", 1150), (25, 28, (27, 28), "vermelho", 1150), (29, 32, (31, 32), "amarelo", 1150),
     (33, 36, (35,), "amarelo", 1150), (39, 40, (), "amarelo", 1150),
     (42, 44, (44,), "vermelho", 1112), (45, 46, (45, 46), "vermelho", 1112),
     (47, 50, (48, 49), "verde", 1112), (51, 52, (), "amarelo", 1112),
     (53, 57, (56, 57), "amarelo", 1150), (58, 63, (63,), "lilas", 1150)]

def legenda(base, t):
    for k, (i0, i1, hl, cor, y) in enumerate(G):
        ini = S[i0] - 0.04
        nxt = S[G[k + 1][0]] - 0.06 if k + 1 < len(G) else 99
        fim = nxt if nxt - PW[i1]["e"] < 1.3 else PW[i1]["e"] + 0.6
        if k == len(G) - 1: fim = 24.98
        if not ini <= t < fim + 0.12: continue
        n = sum(1 for i in range(i0, i1 + 1) if S[i] <= t + 0.02)
        words = tuple(PW[i]["w"] for i in range(i0, i1 + 1))
        spr = etiqueta(words, tuple(h - i0 for h in hl), max(1, n), hl_col=cor)
        last = S[i0 + max(0, n - 1)]
        bump = 1 + 0.06 * (1 - eout(lin(t, last, last + 0.12)))
        e = pop(t, ini, fim, 0.18, 0.12)
        if e: put(base, spr, 540, y, e[0] * bump, 0, e[1])

# ---------------------------------------------------------------- câmera / cartão
HOOK = (540, 930, 780, 1386, 44)
FULL = (540, 960, 1032, 1872, 48)
WIN = (540, 646, 668, 756, 16)
def geom(t):
    def L(a, b, x): return tuple(mix(p, q, x) for p, q in zip(a, b))
    if t < 3.82: g = HOOK
    elif t < 4.22: g = L(HOOK, FULL, eout(lin(t, 3.82, 4.22)))
    elif t < 18.22: g = FULL
    elif t < 18.56: g = L(FULL, WIN, eio(lin(t, 18.22, 18.56)))
    elif t < 21.98: g = WIN
    elif t < 22.32: g = L(WIN, FULL, eio(lin(t, 21.98, 22.32)))
    else: g = FULL
    return g

ZK = [(0, 1.0, .5), (3.82, 1.0, .36), (5.78, 1.10, .33), (8.26, 1.0, .36), (9.8, 1.26, .31), (11.66, 1.0, .36),
      (13.56, 1.07, .35), (14.92, 1.13, .33), (16.64, 1.0, .36), (17.2, 1.16, .33), (18.22, 1.0, .33),
      (22.32, 1.0, .36), (23.58, 1.10, .34)]
def zoom(t):
    z, fy = ZK[0][1], ZK[0][2]
    for i, (tk, zk, fk) in enumerate(ZK):
        if t >= tk:
            pz, pf = (ZK[i - 1][1], ZK[i - 1][2]) if i else (zk, fk)
            x = eout(lin(t, tk, tk + 0.14)); z, fy = mix(pz, zk, x), mix(pf, fk, x)
    if t > 24.9: z *= 1 + 0.10 * eio(lin(t, 24.9, DUR))
    return z, fy

def tremor(t):
    a = 16 * max(0, 1 - (t - 9.8) / 0.32) if t >= 9.8 else 0
    return a * math.sin(t * 95), a * math.cos(t * 71)

# ---------------------------------------------------------------- sprites fixos
def asterisco(cv, cx, cy, r, col=VERMELHO, w=5):
    for i in range(6):
        a = math.pi * i / 6
        cv.line([(cx - r * math.cos(a), cy - r * math.sin(a)), (cx + r * math.cos(a), cy + r * math.sin(a))], col, w)

def cabecalho():
    a, b = MARCA; f = 62
    wa, wb = tw(a + "/", "serif", f), tw(" " + b, "serif", f)
    cv = Cv(70 + wa + wb, 80); asterisco(cv, 28, 40, 24)
    cv.text(66, 40, a + "/", "serif", f, TINTA, "lm"); cv.text(66 + wa, 40, " " + b, "serif", f, TINTA, "lm")
    return cv.done()

def rodape():
    cv = Cv(600, 100); cv.rect(0, 10, 76, 76, r=16, fill=VERMELHO, ow=0); asterisco(cv, 38, 48, 24, PAPEL, 5)
    cv.text(96, 34, "comente “VÍDEO”", "serif_i", 44, TINTA, "lm")
    cv.text(98, 76, "e eu te mando o passo a passo", "serif_i", 29, TINTA, "lm")
    return cv.done()

@lru_cache(None)
def post_ruim(selo_ruim=True):
    w, h = 300, 390; cv = Cv(w, h, pad=30)
    cv.rect(0, 0, w, h, r=18, fill=PAPEL, ow=4, shadow=8)
    cv.ell(16, 14, 40, 40, fill=CINZA, ow=2.5); cv.text(66, 34, "@sualoja", "bold", 22, TINTA, "lm")
    cv.rect(14, 66, w - 28, 250, r=8, fill=(214, 210, 200), ow=3)
    cv.text(w / 2, 140, "PROMOÇÃO!!!", "feio", 40, (210, 30, 30), "mm")
    cv.text(w / 2, 196, "tudo barato", "feio", 30, (30, 60, 200), "mm")
    cv.text(w / 2, 262, "liga já 9999-9999", "feio", 22, TINTA, "mm")
    cv.text(18, 346, "2 curtidas · 0 vendas", "med", 22, TINTA, "lm")
    if selo_ruim:
        cv.rect(w - 112, -14, 124, 50, r=12, fill=VERMELHO, ow=4)
        cv.text(w - 50, 11, "RUIM", "black", 28, PAPEL, "mm")
    return cv.done()

@lru_cache(None)
def flyer_feio():
    w, h = 330, 440; cv = Cv(w, h, pad=30)
    cv.rect(0, 0, w, h, r=4, fill=(233, 230, 222), ow=4, shadow=8)
    cv.text(w / 2, 70, "PROMOÇÃO!!!", "feio", 46, (210, 30, 30), "mm")
    cv.text(w / 2, 130, "TUDO BARATO", "feio", 38, (30, 60, 200), "mm")
    P = [(165 + 52 * math.cos(math.pi * i / 5 - math.pi / 2) * (1 if i % 2 == 0 else .45),
          235 + 52 * math.sin(math.pi * i / 5 - math.pi / 2) * (1 if i % 2 == 0 else .45)) for i in range(10)]
    cv.poly(P, fill=(250, 230, 40), ow=2)
    cv.text(w / 2, 330, "venha conferir!!", "feio", 30, (20, 140, 40), "mm")
    cv.text(w / 2, 390, "liga ja 9999-9999", "feio", 24, TINTA, "mm")
    return cv.done()

@lru_cache(None)
def flyer_bonito():
    w, h = 330, 440; cv = Cv(w, h, pad=30)
    cv.rect(0, 0, w, h, r=14, fill=PAPEL, ow=4, shadow=8)
    cv.rect(18, 18, w - 36, 150, r=10, fill=VERMELHO, ow=3.5)
    cv.text(36, 62, "COMBO", "black", 54, PAPEL, "lm"); cv.text(36, 120, "DE SEXTA", "black", 46, PAPEL, "lm")
    cv.ell(196, 140, 112, 112, fill=AMARELO, ow=4); cv.text(252, 196, "2x1", "black", 40, TINTA, "mm")
    cv.text(30, 222, "a partir de", "med", 24, TINTA, "lm"); cv.text(28, 280, "R$ 39", "black", 64, TINTA, "lm")
    cv.rect(18, 352, w - 36, 68, r=12, fill=TINTA, ow=0)
    cv.text(w / 2, 386, "PEÇA PELO DIRECT", "black", 26, AMARELO, "mm")
    return cv.done()

@lru_cache(None)
def marca_x():
    cv = Cv(240, 240, pad=20); cv.line([(20, 20), (220, 220)], VERMELHO, 26); cv.line([(220, 20), (20, 220)], VERMELHO, 26)
    return cv.done()

@lru_cache(None)
def check():
    cv = Cv(150, 150, pad=20); cv.ell(0, 0, 150, 150, fill=VERDE_OK, ow=5)
    cv.line([(40, 78), (66, 104), (112, 50)], TINTA, 14); return cv.done()

@lru_cache(None)
def janela_impulso(valor, knob_q, estado):
    w, h = 600, 470; cv = janela(w, h, "Impulsionar publicação", "Anúncio")
    # miniatura do post
    cv.rect(24, 80, 170, 170, r=10, fill=(214, 210, 200), ow=3)
    cv.text(109, 140, "PROMO!!!", "feio", 30, (210, 30, 30), "mm"); cv.text(109, 186, "liga já", "feio", 24, (30, 60, 200), "mm")
    cv.text(220, 96, "ORÇAMENTO", "mono", 20, CINZA, "lm")
    cv.text(218, 150, f"R$ {valor}", "black", 64, TINTA, "lm")
    cv.text(220, 214, "Duração · 7 dias", "med", 24, TINTA, "lm")
    x0, x1, y = 220, 566, 280
    k = mix(x0, x1, knob_q / 40)
    cv.rect(x0, y - 7, x1 - x0, 14, r=7, fill=PAPEL, ow=3); cv.rect(x0, y - 7, k - x0, 14, r=7, fill=AMARELO, ow=3)
    cv.ell(k - 17, y - 17, 34, 34, fill=AMARELO, ow=4)
    cv.text(24, 330, "Público: automático", "med", 24, TINTA, "lm")
    if estado == 0: cv.rect(24, 375, w - 48, 70, r=16, fill=AZUL, ow=4, shadow=6); cv.text(w / 2, 410, "Impulsionar", "black", 32, PAPEL, "mm")
    elif estado == 1: cv.rect(28, 380, w - 48, 70, r=16, fill=(40, 60, 190), ow=4); cv.text(w / 2 + 4, 415, "Impulsionar", "black", 32, PAPEL, "mm")
    else: cv.rect(24, 375, w - 48, 70, r=16, fill=VERDE_OK, ow=4, shadow=6); cv.text(w / 2, 410, "Impulsionado!", "black", 32, TINTA, "mm")
    return cv.done()
JI = (540, 1555)  # centro da janela de impulso (sprite tem pad 30)
def ji_abs(lx, ly): return JI[0] - 300 + lx, JI[1] - 235 + ly

@lru_cache(None)
def janela_result(alc, pisca):
    w, h = 600, 390; cv = janela(w, h, "Resultados da campanha", "7 dias")
    rows = [("Pessoas alcançadas", f"{alc:,}".replace(",", "."), TINTA, PAPEL),
            ("Mensagens", "0", TINTA, PAPEL), ("Vendas", "0", PAPEL if pisca else TINTA, VERMELHO if pisca else PAPEL)]
    for i, (a, b, fc, bg) in enumerate(rows):
        y = 82 + i * 98
        cv.rect(22, y, w - 44, 80, r=14, fill=bg, ow=3.5)
        cv.text(44, y + 40, a, "bold", 30, fc if bg != PAPEL else TINTA, "lm")
        cv.text(w - 44, y + 40, b, "black", 44, fc, "rm")
    return cv.done()

@lru_cache(None)
def janela_editor():
    w, h = 680, 830; cv = janela(w, h, "anuncio_da_loja.mp4", "Editor")
    return cv.done()

@lru_cache(None)
def barra_comentario(txt, enviado):
    w, h = 820, 96; cv = Cv(w, h)
    cv.rect(0, 0, w, h, r=48, fill=PAPEL, ow=4, shadow=7)
    cv.ell(16, 16, 64, 64, fill=VERMELHO, ow=3); asterisco(cv, 48, 48, 18, PAPEL, 4)
    if enviado: cv.text(100, 48, "Comentário enviado!", "bold", 32, (60, 140, 80), "lm")
    elif txt: cv.text(100, 48, txt + "|", "black", 36, TINTA, "lm")
    else: cv.text(100, 48, "Adicione um comentário…", "med", 30, CINZA, "lm")
    cv.ell(w - 82, 14, 68, 68, fill=AZUL, ow=3)
    cv.poly([(w - 62, 34), (w - 30, 48), (w - 62, 62), (w - 56, 48)], fill=PAPEL, ow=0)
    return cv.done()

# ---------------------------------------------------------------- frame
CAB, ROD = cabecalho(), rodape()
BG_CREME = Image.new("RGBA", (W, H), (*CREME, 255)); BG_LILAS = fundo_pontos(LILAS)
COPIAS = [(165, 990, -9), (915, 965, 8), (175, 1330, 7), (905, 1320, -6), (215, 760, -5), (870, 745, 6), (330, 1760, 4), (760, 1770, -5)]
random.seed(4)

def card_layer(base, frame, t):
    cx, cy, w, h, r = geom(t)
    z, fy = zoom(t)
    if t < 3.82:  # gancho: entrada + giro de 180°
        sc = mix(0.9, 1, eback(lin(t, 0, 0.35)))
        im = cartao(frame, w, h, r, z, .5, .5, outline=0)
        x = eio(lin(t, 3.14, 3.80)); ang = 180 * x
        if 0 < x < 1:
            vel = 180 * 6 * x * (1 - x) / 0.66 / FPS  # graus por frame
            D = int(math.hypot(w, h)) + 4; sq = Image.new("RGBA", (D, D)); sq.alpha_composite(im, ((D - im.width) // 2, (D - im.height) // 2))
            imgs = [sq.rotate(ang + d, Image.BICUBIC) for d in (-vel * .5, 0, vel * .5)]
            spr = Image.blend(Image.blend(imgs[0], imgs[2], .5), imgs[1], .5)
            put(base, spr, cx, cy, sc * mix(1, 0.86, math.sin(math.pi * x)))
        else:
            put(base, im.rotate(ang, Image.BICUBIC, expand=True) if ang else im, cx, cy, sc)
        return
    dx, dy = tremor(t)
    im = cartao(frame, w, h, r, z, .5, fy)
    base.alpha_composite(im, (int(cx - w / 2 + dx), int(cy - h / 2 + dy)))

def render(t, frame):
    lil = lin(t, 18.22, 18.45) * (1 - lin(t, 21.98, 22.2))
    base = BG_CREME.copy() if lil <= 0 else (BG_LILAS.copy() if lil >= 1 else Image.blend(BG_CREME, BG_LILAS, lil))
    # --- moldura do editor (atrás do cartão)
    e = pop(t, 18.4, 21.95, .3, .2)
    if e: put(base, janela_editor(), 540, 625, e[0], 0, e[1])
    card_layer(base, frame, t)

    # --- gancho
    a = 1 - lin(t, 3.6, 3.95)
    if a > 0:
        put(base, CAB, 540, 150, 1, 0, a * lin(t, 0, .25)); put(base, ROD, 540, 1745, 1, 0, a * lin(t, .15, .4))
    e = pop(t, 0.25, 3.0)
    if e: put(base, bloco("SEU ANÚNCIO", "vermelho", 92), 520, 520, e[0], 5, e[1])
    e = pop(t, 0.6, 3.0)
    if e: put(base, bloco("TÁ DE\nPONTA-CABEÇA?", "amarelo", 82), 560, 720, e[0], -3, e[1])
    for i, (x, y, s0) in enumerate([(230, 400, 70), (880, 600, 54), (210, 850, 44)]):
        e = pop(t, 0.9 + i * .12, 3.0)
        if e: put(base, brilho(s0), x, y, e[0], t * 40 % 360 * 0 + 10 * math.sin(t * 4 + i), e[1])

    # --- 1 · impulsionar
    if 4.38 <= t < 8.5:
        q = 14 + 10 * eio(lin(t, 6.42, 6.78)); val = 200 if t < 6.64 else 300
        est = 0 if t < 7.3 else (1 if t < 7.45 else 2)
        e = pop(t, 4.38, 8.2, .3, .2)
        if e: put(base, janela_impulso(val, int(round(q)), est), JI[0], JI[1], e[0], 0, e[1])
        kx0, ky = ji_abs(mix(220, 566, 14 / 40), 280); kx1, _ = ji_abs(mix(220, 566, 24 / 40), 280); bx, by = ji_abs(300, 410)
        P = [(5.9, (900, 1880)), (6.35, (kx0, ky)), (6.42, (kx0, ky)), (6.78, (kx1, ky)), (7.0, (kx1, ky)), (7.26, (bx + 40, by)), (8.2, (bx + 40, by))]
        if 5.9 <= t < 8.2:
            px, py = P[0][1]
            for (ta, pa), (tb, pb) in zip(P, P[1:]):
                if ta <= t < tb:
                    x = eio(lin(t, ta, tb)); px, py = mix(pa[0], pb[0], x), mix(pa[1], pb[1], x)
            press = 6.42 <= t < 6.78 or 7.26 <= t < 7.4
            anel(base, px, py, lin(t, 7.28, 7.6))
            put(base, cursor(press), px + 20, py + 30, 1, 0, lin(t, 5.9, 6.05))
    # --- 2 · resultados + NADA
    if 8.26 <= t < 11.2:
        alc = int(12430 * eout(lin(t, 8.45, 9.35)) / 10) * 10
        e = pop(t, 8.3, 10.9, .3, .2)
        if e: put(base, janela_result(alc, t > 9.8 and int(t * 6) % 2 == 0), 540, 1580, e[0], 0, e[1])
    e = pop(t, 9.8, 11.45, .22, .2)
    if e: put(base, bloco("NADA.", "vermelho", 200), 540, 1170, e[0] * (1 + .02 * math.sin(t * 20)), 6, e[1])
    # --- 3 · post ruim se multiplicando
    e = pop(t, 12.62, 14.85)
    if e: put(base, post_ruim(), 540, 1560, e[0], 4, e[1])
    for i, (x, y, r) in enumerate(COPIAS):
        e = pop(t, 13.56 + i * .07, 14.85 + i * .02, .25, .15)
        if e: put(base, post_ruim(False), x, y, e[0] * .56, r, e[1])
    # --- 4 · alcance × conteúdo
    e = pop(t, 16.06, 16.72, .25, .25)
    if e:
        put(base, bloco("O ALCANCE", "amarelo", 112), 540, 1430, e[0], 4 + 30 * lin(t, 16.72, 16.97), e[1])
        s = eout(lin(t, 16.3, 16.5))
        if s > 0:
            lay = Image.new("RGBA", (W, H)); d = ImageDraw.Draw(lay)
            d.line([(250, 1450), (mix(250, 830, s), mix(1450, 1405, s))], fill=(*VERMELHO, 255), width=20)
            lay = lay.rotate(4, Image.BICUBIC, center=(540, 1430))
            if e[1] < 1: lay.putalpha(lay.getchannel("A").point(lambda v: int(v * e[1])))
            base.alpha_composite(lay)
    e = pop(t, 17.2, 18.15, .25, .18)
    if e:
        put(base, bloco("CONTEÚDO", "vermelho", 130), 540, 1440, e[0], -3, e[1])
        e2 = pop(t, 17.42, 18.15)
        if e2: put(base, selo("O REAL\nPROBLEMA", "amarelo", 120, 14, 30), 860, 1250, e2[0], -12 + 6 * math.sin(t * 3), e2[1])
        for i, (x, y) in enumerate([(170, 1300), (930, 1580), (230, 1600)]):
            e3 = pop(t, 17.3 + i * .08, 18.15)
            if e3: put(base, brilho(56), x, y, e3[0], 8 * math.sin(t * 5 + i), e3[1])
    # --- 5 · panfletos (fundo lilás)
    e = pop(t, 18.82, 21.95, .3, .2)
    if e:
        put(base, flyer_feio(), 290, 1460, e[0], 5, e[1])
        e2 = pop(t, 19.42, 21.95, .16, .2)
        if e2: put(base, marca_x(), 290, 1460, e2[0] * 1.1, 0, e2[1])
    e = pop(t, 20.16, 21.95, .3, .2)
    if e:
        put(base, flyer_bonito(), 790, 1460, e[0], -4, e[1])
        e2 = pop(t, 20.9, 21.95)
        if e2: put(base, check(), 930, 1260, e2[0], 0, e2[1])
    # --- 6 · panfleto = vídeo
    e = pop(t, 24.1, 25.0, .3, .15)
    if e: put(base, flyer_bonito(), 270, 1500, e[0] * .72, -8, e[1])
    e = pop(t, 24.42, 25.0, .26, .15)
    if e: put(base, selo("O PANFLETO\nAGORA É\nVÍDEO", "amarelo", 190, 16, 40), 760, 1490, e[0], 8 + 4 * math.sin(t * 3), e[1])
    # --- CTA final
    if t >= 25.0:
        e = pop(t, 25.05, None, .3)
        if e: put(base, bloco("COMENTE", "tinta", 96), 500, 1150, e[0], -3, e[1])
        e = pop(t, 25.2, None, .3)
        if e: put(base, bloco("“VÍDEO”", "lilas", 96), 620, 1300, e[0], 4, e[1])
        e = pop(t, 25.35, None, .3)
        typed = "VÍDEO"[:int(clamp((t - 25.55) / 0.08, 0, 5))]
        if e: put(base, barra_comentario(typed, t > 26.05), 540, 1500, e[0], 0, e[1])
        e = pop(t, 25.5, None, .3)
        if e: put(base, etiqueta(("e", "eu", "te", "mando", "o", "passo", "a", "passo"), (5, 6, 7), size=44), 540, 1625, e[0], 0, e[1])
        for i, (x, y) in enumerate([(170, 1180), (940, 1200), (900, 1640), (160, 1560)]):
            e = pop(t, 25.3 + i * .1, None)
            if e: put(base, brilho(50), x, y, e[0], 10 * math.sin(t * 4 + i), e[1])
        anel(base, 540 + 410 - 48, 1500, lin(t, 25.98, 26.3))
    legenda(base, t)
    return base

if __name__ == "__main__":
    fonte = Fonte(SRC); out = Saida(OUT)
    nf = int(round(DUR * FPS)); f0 = int(T0 * FPS); f1 = nf if T1 is None else int(T1 * FPS)
    import time; t_ini = time.time()
    for f in range(f0, f1):
        t = f / FPS
        frame = fonte.get(int(min(t, SRC_END) * FPS))
        out.write(render(t, frame))
        if f % 60 == 0: print(f"{t:5.1f}s  ({time.time() - t_ini:.0f}s)", flush=True)
    out.close()
