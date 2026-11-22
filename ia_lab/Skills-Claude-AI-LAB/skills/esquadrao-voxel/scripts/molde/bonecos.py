# Esquadrão Voxel — bonecos de bloco (cabeça grande, olhos de retângulo) + acessórios + gestos.
#   b = Boneco("pesq", pele=CLAUDE, roupa="#3B5BA9", numero=1, chapeu="detetive", rosto=["bigode"], mao="lupa")
#   b.trilha = [(t, (x, y), yaw)]            posição (pula de um ponto pro outro, estilo jogo de bloco)
#   b.surge(t0, "pula"|"cai"|"pop")          entrada;  b.some(t1)
#   b.gesto("acena"|"ergue"|"digita"|"aponta"|"comemora"|"bate"|"olha"|"pula"|"tremer", t0, t1)
#   b.update(t)  -> chamar no apply(t) da cena
# Frente do boneco = -Y (onde fica a câmera).
import math, random
import vox
from vox import box, prim, empty, text3d, painel, hexc, ease, eout, eback, spring, clamp, lerp

CLAUDE = "#DE7350"       # laranja Claude
PELES = dict(claude=CLAUDE, lima="#B7E04A", lilas="#A58BE8", azul="#5FA8E8", rosa="#F08BB0", menta="#5CCB9F",
             robo="#B9C2CC", humano="#E9B48F", humano2="#B97C56", humano3="#8D5A3B")

# medidas (unidade ~ metro). cabeça grande = cara de mascote
LEG_H, TOR_H, TOR_W, TOR_D = 0.16, 0.40, 0.74, 0.52
HEAD_H, HEAD_W, HEAD_D = 0.80, 0.92, 0.84
Z_HEAD = LEG_H + TOR_H
FRONT = -HEAD_D / 2


class Boneco:
    def __init__(s, nome, pele=CLAUDE, roupa="#3B5BA9", calca="#2A2D3A", numero=None, chapeu=None,
                 rosto=(), mao=None, mao_esq=None, cabelo=None, extras=(), olhos="#16131F", cor_chapeu=None,
                 escala=1.0, braco="pele"):
        s.nome = nome; s.pele = pele; s.roupa = roupa
        s.root = empty(nome)
        s.corpo = empty(nome + "_corpo", parent=s.root)
        P = s.corpo
        for x in (-0.18, 0.18):
            box(nome + "_perna", (0.22, 0.26, LEG_H + 0.04), (x, 0, -0.02), calca, P, 0.03, z0=True)
        s.tronco = box(nome + "_tronco", (TOR_W, TOR_D, TOR_H + 0.02), (0, 0, LEG_H - 0.01), roupa, P, 0.05, z0=True)
        s.cab = empty(nome + "_cab", (0, 0, Z_HEAD), P)
        s.head = box(nome + "_head", (HEAD_W, HEAD_D, HEAD_H), (0, 0, 0), pele, s.cab, 0.07, z0=True)
        # olhos (piscam)
        s.olhos = []
        s.olho_y = FRONT - 0.012
        for x in (-0.2, 0.2):
            o = box(nome + "_olho", (0.105, 0.03, 0.22), (x, s.olho_y, 0.4), olhos, s.cab, 0.012)
            s.olhos.append(o)
        # braços (pivô no ombro)
        cb = pele if braco == "pele" else roupa
        s.brL = empty(nome + "_brL", (-(TOR_W / 2 + 0.08), 0, LEG_H + TOR_H - 0.04), P)
        s.brR = empty(nome + "_brR", ((TOR_W / 2 + 0.08), 0, LEG_H + TOR_H - 0.04), P)
        for br in (s.brL, s.brR):
            box(nome + "_braco", (0.15, 0.2, 0.36), (0, 0, -0.18), cb, br, 0.04)
        s.maoL = empty(nome + "_maoL", (0, -0.04, -0.36), s.brL)
        s.maoR = empty(nome + "_maoR", (0, -0.04, -0.36), s.brR)
        if numero is not None:
            prim("cyl", nome + "_n", (0.2, -TOR_D / 2 - 0.01, LEG_H + 0.2), (0.11, 0.11, 0.02), "#FFC83D", P, (math.pi / 2, 0, 0))
            text3d(nome + "_nt", str(numero), 0.13, (0.2, -TOR_D / 2 - 0.03, LEG_H + 0.2), "#16131F", 0.005, P)
        s.props = {}; s.anims = []
        if chapeu: ACESS[chapeu](s, cor_chapeu)
        if cabelo: ACESS["cabelo"](s, cabelo)
        for r in rosto: ACESS[r](s, None)
        for e in extras: ACESS[e](s, None)
        if mao: s.props["mao"] = MAO[mao](s, s.maoR)
        if mao_esq: s.props["mao_esq"] = MAO[mao_esq](s, s.maoL)
        s.esc = escala
        s.chao = []   # [(t, z)] altura do chão (ex. em cima do teclado, num banquinho)
        s.trilha = []; s.entradas = []; s.saidas = []; s.gestos = []; s.placas = []
        s.pisca = sorted(random.Random(hash(nome) & 0xffff).uniform(0, 1) + i * random.Random(i + len(nome)).uniform(2.2, 4.0) for i in range(30))
        s.vis = True
        s.fase = random.Random(nome).uniform(0, 6.28)

    # ---------------------------------------------------------------- roteiro do boneco
    def surge(s, t0, modo="pula", dur=0.45): s.entradas.append((t0, modo, dur)); return s
    def some(s, t1, dur=0.25): s.saidas.append((t1, dur)); return s
    def gesto(s, nome, t0, t1=None): s.gestos.append((nome, t0, t1 if t1 is not None else t0 + 1.0)); return s
    def segura_placa(s, img, t0, t1, w=1.3, h=0.75, mao="R", cor_haste="#8A6A48"):
        """placa num cabo erguida pela mão (imagem gerada pelo telas.py)."""
        m = s.maoR if mao == "R" else s.maoL
        g = empty(s.nome + "_placa", (0, -0.06, 0), m)
        g.rotation_euler = (math.pi, 0, 0)   # braço erguido: cabo segue o braço e a placa fica de frente
        box("haste", (0.05, 0.05, 1.0), (0, 0, 0.02), cor_haste, g, 0.01, z0=True)
        box("placa_fundo", (w + 0.06, 0.04, h + 0.06), (0, 0.02, 1.0 + h / 2), "#16131F", g, 0.02)
        painel("placa", img, w, h, (0, -0.005, 1.0 + h / 2), g, emit=0.7)
        vox.show(g, 0)
        s.placas.append((g, t0, t1, mao))
        s.gesto("ergueR" if mao == "R" else "ergueL", t0 - 0.05, t1)
        return g

    def _pos(s, t):
        tr = s.trilha
        if not tr: return 0, 0, 0, 0, 0
        if t <= tr[0][0]: (x, y), yaw = tr[0][1], tr[0][2]; return x, y, 0, yaw, 0
        for (ta, pa, ya), (tb, pb, yb) in zip(tr, tr[1:]):
            if ta <= t < tb:
                d = math.hypot(pb[0] - pa[0], pb[1] - pa[1])
                if d < 0.01 or tb - ta < 0.02:
                    return pa[0], pa[1], 0, ya, 0
                if d > 6:  # teleporte (troca de cenário, acontece durante corte)
                    return pa[0], pa[1], 0, ya, 0
                k = (t - ta) / (tb - ta)
                n = max(1, round(d / 0.55))            # pulinhos
                ph = k * n; kk = (math.floor(ph) + ease(ph - math.floor(ph))) / n
                z = 0.22 * math.sin(math.pi * (ph - math.floor(ph)))
                x, y = lerp(pa[0], pb[0], kk), lerp(pa[1], pb[1], kk)
                yaw = math.atan2(pb[0] - pa[0], -(pb[1] - pa[1])) if True else ya
                yaw = lerp(ya, yaw, min(1, k * 4)) if k < 0.9 else lerp(yaw, yb, (k - 0.9) * 10)
                return x, y, z, yaw, (ph - math.floor(ph))
        (x, y), yaw = tr[-1][1], tr[-1][2]
        return x, y, 0, yaw, 0

    def update(s, t):
        # visível?
        vis = True; sc_in = 1.0; dz = 0.0; sq = 0.0
        if s.entradas:
            t0, modo, dur = max((e for e in s.entradas if e[0] <= t), default=(None, None, None), key=lambda e: e[0])
            if t0 is None: vis = False
            else:
                k = (t - t0) / dur
                if k < 1:
                    if modo == "pula":   # sobe de baixo com salto
                        dz = -1.6 * (1 - eback(k, 1.4)) + 0.5 * math.sin(math.pi * clamp(k)) ; sc_in = clamp(k * 3)
                    elif modo == "cai":  # cai do alto
                        dz = 3.0 * (1 - ease(k) ** 0.7) * (1 - k); sc_in = 1
                    else:                # pop
                        sc_in = eback(k, 2.2)
                kl = (t - t0 - dur * 0.85) / 0.35   # amassa ao pousar
                if 0 < kl < 1: sq = 0.22 * math.sin(math.pi * kl) * (1 - kl)
        for t1, d in s.saidas:
            if t >= t1:
                k = (t - t1) / d; sc_in = min(sc_in, 1 - ease(k))
                if k >= 1: vis = False
        if not vis or sc_in <= 0.002:
            if s.vis:
                for o in [s.root] + list(s.root.children_recursive): o.hide_render = True
                s.vis = False
            return
        if not s.vis:
            for o in [s.root] + list(s.root.children_recursive): o.hide_render = False
            s.vis = True
            for g, *_ in s.placas: vox.show(g, 0)
        x, y, zj, yaw, hop = s._pos(t)
        if zj > 0.01 and hop > 0.85: sq = max(sq, 0.15 * (1 - (hop - 0.85) / 0.15))
        # respiração / balanço
        bob = 0.012 * math.sin(t * 4.2 + s.fase)
        z0 = 0.0
        for tc, zc in s.chao:
            if t >= tc: z0 = zc
        s.root.location = (x, y, z0 + zj + dz)
        s.root.rotation_euler = (0, 0, yaw)
        e = s.esc * sc_in
        s.root.scale = (e, e, e)
        sy = 1 - sq + bob; sx = 1 + sq * 0.6 - bob * 0.5
        s.corpo.scale = (sx, sx, sy)
        # braços em repouso (balanço leve)
        aL = [0.0, 0.0]; aR = [0.0, 0.0]   # (x: frente/trás, y: lado)
        sw = 0.08 * math.sin(t * 3.1 + s.fase)
        aL[0] = sw; aR[0] = -sw
        aL[1] = -0.1; aR[1] = 0.1
        cab_rz = 0.0; cab_rx = 0.0; cab_ry = 0.05 * math.sin(t * 1.7 + s.fase)
        for nome, t0, t1 in s.gestos:
            if not (t0 - 0.05 <= t <= t1 + 0.35): continue
            a = ease((t - t0) / 0.25) * (1 - ease((t - t1) / 0.3))
            lt = t - t0
            if nome == "acena":
                aR[1] = lerp(aR[1], 2.5 + 0.35 * math.sin(lt * 16), a)
            elif nome in ("ergueR", "ergue"):
                aR[0] = lerp(aR[0], -2.7 - 0.06 * math.sin(lt * 5), a); aR[1] = lerp(aR[1], 0.15, a)
            elif nome == "ergueL":
                aL[0] = lerp(aL[0], -2.7 - 0.06 * math.sin(lt * 5), a); aL[1] = lerp(aL[1], -0.15, a)
            elif nome == "digita":
                aL[0] = lerp(aL[0], -1.25 + 0.18 * math.sin(lt * 26), a)
                aR[0] = lerp(aR[0], -1.25 + 0.18 * math.sin(lt * 26 + 2), a)
                cab_rx = lerp(cab_rx, 0.12, a)
            elif nome == "aponta":
                aR[0] = lerp(aR[0], -1.9, a); aR[1] = lerp(aR[1], 0.5, a)
            elif nome == "segura":   # mostra o objeto (braço pra cima e pra frente, lê de frente)
                aR[0] = lerp(aR[0], -2.05 - 0.05 * math.sin(lt * 4), a); aR[1] = lerp(aR[1], -0.3, a)
            elif nome == "segura2":
                aL[0] = lerp(aL[0], -1.2, a); aR[0] = lerp(aR[0], -1.2, a)
            elif nome == "mostra":   # mostra o objeto da mão direita na frente do corpo (objetos do ELENCO)
                aR[0] = lerp(aR[0], -0.75, a); aR[1] = lerp(aR[1], -0.32, a)
            elif nome == "mostra2":  # as duas mãos (bastões, cartazes)
                aR[0] = lerp(aR[0], -0.75, a); aR[1] = lerp(aR[1], -0.25, a)
                aL[0] = lerp(aL[0], -0.75, a); aL[1] = lerp(aL[1], 0.25, a)
            elif nome == "comemora":
                aL[1] = lerp(aL[1], -2.6 - 0.3 * math.sin(lt * 14), a)
                aR[1] = lerp(aR[1], 2.6 + 0.3 * math.sin(lt * 14), a)
                s.root.location.z += a * 0.3 * abs(math.sin(lt * 7))
            elif nome == "bate":     # bate (claquete, botão)
                kk = abs(math.sin(lt * 9)) ** 3
                aR[0] = lerp(aR[0], -2.2 + 0.8 * kk, a); aR[1] = lerp(aR[1], -0.25, a)
            elif nome == "olha":     # olha pros lados
                cab_rz = lerp(cab_rz, 0.45 * math.sin(lt * 4.5), a)
            elif nome == "pula":
                s.root.location.z += a * 0.35 * abs(math.sin(lt * 8))
            elif nome == "tremer":
                s.root.location.x += a * 0.02 * math.sin(lt * 70)
            elif nome == "fala":     # balança a cabeça no ritmo
                cab_rx = lerp(cab_rx, 0.05 * math.sin(lt * 13), a); cab_rz = lerp(cab_rz, 0.06 * math.sin(lt * 5), a)
        s.brL.rotation_euler = (aL[0], aL[1], 0)
        s.brR.rotation_euler = (aR[0], aR[1], 0)
        s.cab.rotation_euler = (cab_rx, cab_ry * 0.3, cab_rz)
        # piscar
        blink = any(0 <= t - b < 0.12 for b in s.pisca)
        for o in s.olhos: o.scale = (1, 1, 0.12 if blink else 1)
        # placas
        for g, t0, t1, _ in s.placas:
            vox.show(g, vox.win(t, t0, t1, 0.35, 0.25))
        for a in s.anims: a(t)

    def topo(s):
        """ponto acima da cabeça (pra âncoras de overlay)."""
        x, y, z = s.root.location
        return (x, y, z + (Z_HEAD + HEAD_H + 0.25) * s.esc)


# ---------------------------------------------------------------- acessórios de cabeça / rosto / corpo
def _safari(b, cor):
    c = cor or "#E8D7A2"; H = HEAD_H
    prim("cyl", "brim", (0, 0, H + 0.02), (0.78, 0.74, 0.03), c, b.cab)
    prim("dome", "copa", (0, 0, H + 0.02), (0.46, 0.44, 0.36), c, b.cab)
    prim("cyl", "fita", (0, 0, H + 0.08), (0.47, 0.45, 0.04), "#7A4E2D", b.cab)
def _detetive(b, cor):
    c = cor or "#9A7448"; H = HEAD_H
    prim("dome", "copa", (0, 0, H - 0.06), (0.52, 0.48, 0.38), c, b.cab)
    box("aba_f", (0.6, 0.26, 0.05), (0, FRONT - 0.08, H - 0.02), c, b.cab, 0.02, rot=(0.25, 0, 0))
    box("aba_t", (0.6, 0.2, 0.05), (0, -FRONT + 0.08, H - 0.02), c, b.cab, 0.02, rot=(-0.25, 0, 0))
    for x in (-1, 1):
        box("xadrez", (0.04, 0.5, 0.3), (x * 0.25, 0, H + 0.04), "#6E5232", b.cab, 0.01)
    prim("cyl", "botao", (0, 0, H + 0.33), (0.06, 0.06, 0.04), "#6E5232", b.cab)
def _bone(b, cor):
    c = cor or "#3C7DD9"; H = HEAD_H
    prim("dome", "bone", (0, 0.02, H - 0.08), (0.5, 0.46, 0.3), c, b.cab)
    box("pala", (0.62, 0.34, 0.05), (0, FRONT - 0.12, H - 0.02), c, b.cab, 0.02)
    prim("cyl", "botao", (0, 0.02, H + 0.21), (0.05, 0.05, 0.03), "#FFFFFF", b.cab)
def _boina(b, cor):
    c = cor or "#2A2533"; H = HEAD_H
    prim("cyl", "boina", (0.05, 0, H + 0.05), (0.52, 0.5, 0.09), c, b.cab, (0, 0.18, 0))
    prim("cyl", "pino", (0.1, 0, H + 0.15), (0.04, 0.04, 0.06), c, b.cab)
def _cartola(b, cor):
    c = cor or "#1D1B24"; H = HEAD_H
    prim("cyl", "aba", (0, 0, H + 0.02), (0.62, 0.6, 0.03), c, b.cab)
    prim("cyl", "copa", (0, 0, H + 0.3), (0.38, 0.36, 0.55), c, b.cab)
    prim("cyl", "fita", (0, 0, H + 0.1), (0.39, 0.37, 0.08), "#C0392B", b.cab)
def _capacete(b, cor):
    c = cor or "#F2C14E"; H = HEAD_H
    prim("dome", "cap", (0, 0, H - 0.1), (0.56, 0.52, 0.38), c, b.cab)
    box("aba", (1.0, 0.95, 0.04), (0, 0, H - 0.08), c, b.cab, 0.02)
def _coroa(b, cor):
    c = cor or "#F5C542"; H = HEAD_H
    box("aro", (0.7, 0.6, 0.12), (0, 0, H + 0.05), c, b.cab, 0.02)
    for x in (-0.28, 0, 0.28):
        box("ponta", (0.12, 0.6, 0.18), (x, 0, H + 0.18), c, b.cab, 0.02)
def _chef(b, cor):
    H = HEAD_H
    prim("cyl", "faixa", (0, 0, H + 0.08), (0.42, 0.4, 0.12), "#FFFFFF", b.cab)
    for x, y in ((-0.18, 0), (0.18, 0), (0, -0.12), (0, 0.14)):
        prim("sph", "puf", (x, y, H + 0.32), (0.24, 0.24, 0.2), "#FFFFFF", b.cab)
def _fone(b, cor):
    c = cor or "#24212D"; H = HEAD_H; W = HEAD_W / 2
    box("arco", (HEAD_W + 0.16, 0.12, 0.08), (0, 0, H + 0.06), c, b.cab, 0.03)
    for x in (-1, 1):
        box("haste", (0.08, 0.12, 0.3), (x * (W + 0.06), 0, H - 0.1), c, b.cab, 0.02)
        box("concha", (0.14, 0.34, 0.34), (x * (W + 0.07), 0, 0.42), c, b.cab, 0.05)
        box("almof", (0.04, 0.26, 0.26), (x * (W + 0.15), 0, 0.42), vox.PAL.get("acento", "#C6F432"), b.cab, 0.015)
def _cabelo(b, cor):
    c = cor or "#3A2A22"; H = HEAD_H
    box("cabelo", (HEAD_W + 0.04, HEAD_D + 0.04, 0.2), (0, 0.01, H - 0.06), c, b.cab, 0.04, z0=True)
    box("franja", (HEAD_W + 0.04, 0.12, 0.16), (0, FRONT - 0.02, H - 0.1), c, b.cab, 0.03)
    box("nuca", (HEAD_W + 0.04, 0.12, 0.45), (0, -FRONT + 0.02, H - 0.4), c, b.cab, 0.03)
def _oculos(b, cor, sol=False):
    c = cor or "#16131F"; y = FRONT - 0.03
    for x in (-0.2, 0.2):
        box("aro", (0.3, 0.03, 0.27), (x, y, 0.42), c, b.cab, 0.02)
        box("lente", (0.24, 0.035, 0.21), (x, y - 0.006, 0.42), "#1E2633" if sol else "#CFE9F5", b.cab, 0.01)
    box("ponte", (0.12, 0.03, 0.04), (0, y, 0.46), c, b.cab, 0.005)
    for o in b.olhos:
        o.location.y = y - 0.03
        if sol: o.hide_render = True
def _oculos_sol(b, cor): _oculos(b, cor, True)
def _bigode(b, cor):
    c = cor or "#F4EEE2"
    for x, r in ((-0.13, 0.25), (0.13, -0.25)):
        box("bigode", (0.24, 0.05, 0.08), (x, FRONT - 0.02, 0.2), c, b.cab, 0.03, rot=(0, r, 0))
def _barba(b, cor):
    c = cor or "#F4EEE2"
    box("barba", (HEAD_W + 0.02, 0.1, 0.28), (0, FRONT - 0.02, 0.1), c, b.cab, 0.04)
def _bochecha(b, cor):
    for x in (-0.33, 0.33):
        box("boch", (0.12, 0.02, 0.06), (x, FRONT - 0.01, 0.24), "#F29C8F", b.cab, 0.01)
def _gravata(b, cor):
    c = cor or "#C0392B"
    box("gravata", (0.1, 0.03, 0.3), (0, -TOR_D / 2 - 0.01, LEG_H + 0.2), c, b.corpo, 0.01)
def _gola(b, cor):
    box("gola", (0.5, 0.04, 0.08), (0, -TOR_D / 2 - 0.01, LEG_H + TOR_H - 0.06), "#FFFFFF", b.corpo, 0.01)
def _moletom(b, cor):
    for x in (-0.1, 0.1):
        box("cordao", (0.03, 0.03, 0.22), (x, -TOR_D / 2 - 0.01, LEG_H + TOR_H - 0.13), "#F4EEE2", b.corpo, 0.005)
    box("bolso", (0.44, 0.03, 0.12), (0, -TOR_D / 2 - 0.01, LEG_H + 0.08), "#00000022" if False else "#1C1F2B", b.corpo, 0.01)
def _cracha(b, cor):
    box("cracha", (0.16, 0.03, 0.2), (-0.2, -TOR_D / 2 - 0.01, LEG_H + 0.22), "#FFFFFF", b.corpo, 0.01)
    box("cracha_t", (0.12, 0.035, 0.04), (-0.2, -TOR_D / 2 - 0.012, LEG_H + 0.27), vox.PAL.get("acento", "#C6F432"), b.corpo, 0.005)
def _antena(b, cor):
    H = HEAD_H
    box("ant", (0.04, 0.04, 0.3), (0, 0, H), "#3A3F4B", b.cab, 0.01, z0=True)
    o = prim("sph", "ant_luz", (0, 0, H + 0.33), (0.08, 0.08, 0.08), cor or "#FF5A5A", b.cab, mat=vox.MATS["glow"])

ACESS = dict(safari=_safari, detetive=_detetive, bone=_bone, boina=_boina, cartola=_cartola, capacete=_capacete,
             coroa=_coroa, chef=_chef, fone=_fone, cabelo=_cabelo, oculos=_oculos, oculos_sol=_oculos_sol,
             bigode=_bigode, barba=_barba, bochecha=_bochecha, gravata=_gravata, gola=_gola, moletom=_moletom,
             cracha=_cracha, antena=_antena)


# ---------------------------------------------------------------- objetos de mão (presos no fim do braço)
def _lupa(b, m):
    g = empty("lupa", (0, -0.05, 0.02), m)
    box("cabo", (0.06, 0.06, 0.28), (0, 0, 0), "#6B4A2E", g, 0.015, z0=True)
    prim("torus", "aro", (0, 0, 0.45), (0.17, 0.17, 0.17), "#F2B33D", g, (math.pi / 2, 0, 0), r=0.2)
    prim("cyl", "vidro", (0, 0, 0.45), (0.16, 0.16, 0.02), "#D6F0FF", g, (math.pi / 2, 0, 0))
    g.rotation_euler = (-1.2, 0, 0.3)
    return g
def _lapis(b, m):
    g = empty("lapis", (0, -0.05, 0), m)
    box("corpo", (0.07, 0.07, 0.42), (0, 0, -0.05), "#F2C14E", g, 0.01, z0=True)
    box("borracha", (0.07, 0.07, 0.07), (0, 0, 0.37), "#F08BB0", g, 0.01, z0=True)
    prim("cone", "ponta", (0, 0, -0.1), (0.045, 0.045, 0.1), "#E8D2AE", g, (math.pi, 0, 0))
    g.rotation_euler = (-1.4, 0, 0)
    return g
def _microfone(b, m):
    g = empty("mic", (0, -0.06, 0), m)
    prim("cyl", "cabo", (0, 0, 0.1), (0.045, 0.045, 0.24), "#24212D", g)
    prim("sph", "globo", (0, 0, 0.28), (0.1, 0.1, 0.1), "#AEB4BE", g)
    g.rotation_euler = (-1.3, 0, 0)
    return g
def _claquete(b, m):
    g = empty("claq", (0, -0.08, 0.05), m)
    box("placa", (0.46, 0.05, 0.32), (0, 0, 0.18), "#24212D", g, 0.015, z0=True)
    box("linha", (0.4, 0.055, 0.03), (0, 0, 0.32), "#FFFFFF", g, 0.005)
    hin = empty("dob", (-0.23, 0, 0.52), g)
    for i in range(4):
        box("faixa", (0.115, 0.06, 0.08), (0.06 + i * 0.115, 0, 0.04), "#FFFFFF" if i % 2 == 0 else "#24212D", hin, 0.005)
    g.rotation_euler = (-1.45, 0, 0)
    def anim(t, hin=hin, b=b):
        ang = 0.0
        for nome, t0, t1 in b.gestos:
            if nome == "bate" and t0 <= t <= t1:
                ang = 0.5 * (1 - abs(math.sin((t - t0) * 9)) ** 3)
        hin.rotation_euler = (0, -ang, 0)
    b.anims.append(anim)
    return g
def _celular(b, m):
    g = empty("cel", (0, -0.06, 0.04), m)
    box("cel", (0.2, 0.035, 0.36), (0, 0, 0.18), "#1D1B24", g, 0.03, z0=True)
    box("tela", (0.17, 0.04, 0.31), (0, -0.002, 0.18), vox.PAL.get("acento", "#C6F432"), g, 0.02, z0=True, mat=vox.MATS["glow"])
    g.rotation_euler = (-1.45, 0, 0)
    return g
def _caneca(b, m):
    g = empty("caneca", (0, -0.08, 0.02), m)
    prim("cyl", "caneca", (0, 0, 0.1), (0.1, 0.1, 0.2), "#FFFFFF", g)
    g.rotation_euler = (-1.5, 0, 0)
    return g
def _prancheta(b, m):
    g = empty("pranch", (0, -0.08, 0.02), m)
    box("tabua", (0.34, 0.03, 0.44), (0, 0, 0.22), "#A9774A", g, 0.015, z0=True)
    box("folha", (0.3, 0.035, 0.36), (0, -0.003, 0.22), "#FFFFFF", g, 0.005, z0=True)
    box("presilha", (0.14, 0.05, 0.05), (0, -0.01, 0.45), "#AEB4BE", g, 0.01)
    g.rotation_euler = (-1.45, 0, 0)
    return g
def _envelope(b, m):
    g = empty("env", (0, -0.08, 0.02), m)
    box("env", (0.38, 0.03, 0.26), (0, 0, 0.13), "#F4EEE2", g, 0.01, z0=True)
    box("selo", (0.08, 0.035, 0.08), (0.12, -0.003, 0.2), "#E5484D", g, 0.005)
    g.rotation_euler = (-1.45, 0, 0)
    return g

MAO = dict(lupa=_lupa, lapis=_lapis, microfone=_microfone, claquete=_claquete, celular=_celular,
           caneca=_caneca, prancheta=_prancheta, envelope=_envelope)

# ---------------------------------------------------------------- receitas prontas (tipos de personagem)
RECEITAS = {
    "pesquisador": dict(chapeu="detetive", mao="lupa", roupa="#7A5A3C"),
    "explorador":  dict(chapeu="safari", rosto=["bigode"], mao="prancheta", roupa="#6F7A3C", extras=["gola"]),
    "roteirista":  dict(rosto=["oculos"], mao="lapis", roupa="#E9E4F2", extras=["gravata"], cabelo="#2A2230"),
    "narrador":    dict(chapeu="fone", mao="microfone", roupa="#2E3A59"),
    "editor":      dict(chapeu="boina", mao="claquete", roupa="#24212D", extras=["cracha"]),
    "postador":    dict(chapeu="bone", mao="celular", roupa="#F2B33D", extras=["cracha"]),
    "hacker":      dict(rosto=["oculos_sol"], roupa="#1D1B24", extras=["moletom"]),
    "chefe":       dict(chapeu="cartola", roupa="#2E3A59", extras=["gravata", "gola"]),
    "senior":      dict(rosto=["oculos", "barba"], mao="caneca", roupa="#8E3B2E"),
    "testador":    dict(chapeu="capacete", mao="prancheta", roupa="#EDEDED", extras=["cracha"]),
    "chef":        dict(chapeu="chef", roupa="#FFFFFF", extras=["gola"]),
    "robo":        dict(pele=PELES["robo"], extras=["antena"], roupa="#5B6270"),
    "rei":         dict(chapeu="coroa", roupa="#6B3E73", extras=["gola"]),
    "voce":        dict(pele=PELES["humano"], cabelo="#2A1F1A", roupa="#3B4256", extras=["moletom"], braco="roupa"),
}
def receita(nome, tipo, **kw):
    d = dict(RECEITAS[tipo]); d.update(kw)
    return Boneco(nome, **d)



# ================================================================ ELENCO PRÓPRIO (out/2026)
# Estudo de 5 Reels de referência (ver references/ESTUDO-REFERENCIAS.md): lá os bonecos usam chapéu de
# detetive + lupa, boné azul, boina + claquete, óculos de tela, terno com gravata, safari, homem das cavernas.
# Pra não parecer cópia, o nosso elenco usa outras roupas/props e tem uma ASSINATURA em todo boneco ("marca"):
# brilho branco no olho, bochecha coral, tênis branco com faixa limão e pin de asterisco limão no peito.
LIMA = "#C6F432"; TINTA = "#16131F"; CREME = "#F4F1EA"; OURO = "#F2C14E"


def _marca(b, cor):
    for o in b.olhos:                                       # brilho no olho (pisca junto)
        box("brilho", (0.04, 0.012, 0.06), (0.024, -0.018, 0.062), "#FFFFFF", o, 0.004)
    for x in (-0.33, 0.33):
        box("boch", (0.13, 0.02, 0.07), (x, FRONT - 0.01, 0.23), "#F7A58F", b.cab, 0.012)
    for x in (-0.18, 0.18):                                 # tênis
        box("tenis", (0.26, 0.34, 0.085), (x, -0.035, -0.035), CREME, b.corpo, 0.03, z0=True)
        box("tenis_faixa", (0.272, 0.2, 0.028), (x, -0.03, 0.0), LIMA, b.corpo, 0.006)
    y = -TOR_D / 2 - 0.055                                  # pin de asterisco (fica por cima de colete/avental)
    box("pin", (0.13, 0.025, 0.13), (0.2, y, LEG_H + 0.29), LIMA, b.corpo, 0.02)
    for a in (0, 1.047, 2.094):
        box("pin_ast", (0.095, 0.012, 0.022), (0.2, y - 0.016, LEG_H + 0.29), TINTA, b.corpo, 0.004, rot=(0, a, 0))


# ---------------------------------------------------------------- cabeça
def _quepe(b, cor):                      # quepe de capitã (branco, aba preta, âncora dourada)
    H = HEAD_H
    prim("cyl", "quepe_copa", (0, 0.02, H + 0.07), (0.52, 0.49, 0.16), cor or CREME, b.cab)
    prim("cyl", "quepe_faixa", (0, 0.02, H + 0.0), (0.485, 0.455, 0.08), "#1D2B44", b.cab)
    box("quepe_aba", (0.58, 0.26, 0.035), (0, FRONT - 0.08, H - 0.01), TINTA, b.cab, 0.015, rot=(0.22, 0, 0))
    box("quepe_ancora", (0.13, 0.03, 0.1), (0, -0.475, H + 0.07), OURO, b.cab, 0.015)
def _cabelo_prata(b, cor):               # topete penteado pra trás (maestro)
    c = cor or "#C9CDD6"; H = HEAD_H
    box("cab_topo", (HEAD_W + 0.05, HEAD_D + 0.05, 0.16), (0, 0.02, H - 0.04), c, b.cab, 0.06, z0=True)
    box("cab_topete", (0.84, 0.42, 0.24), (0, FRONT + 0.16, H + 0.1), c, b.cab, 0.1, rot=(-0.45, 0, 0))
    box("cab_onda", (0.6, 0.3, 0.16), (0.05, 0.12, H + 0.14), c, b.cab, 0.07, rot=(-0.2, 0, 0.1))
    box("cab_nuca", (HEAD_W + 0.05, 0.14, 0.5), (0, -FRONT + 0.02, H - 0.42), c, b.cab, 0.04)
    for x in (-1, 1):
        box("cab_lado", (0.06, 0.4, 0.3), (x * (HEAD_W / 2 + 0.02), 0.08, H - 0.28), c, b.cab, 0.02)
def _lanterna(b, cor):                   # faixa com lanterna de testa acesa
    box("lant_faixa", (HEAD_W + 0.035, HEAD_D + 0.035, 0.1), (0, 0, 0.62), "#3A3F4B", b.cab, 0.02)
    box("lant_corpo", (0.26, 0.12, 0.2), (0, FRONT - 0.07, 0.64), "#F2C14E", b.cab, 0.03)
    prim("cyl", "lant_luz", (0, FRONT - 0.135, 0.64), (0.085, 0.085, 0.02), "#FFF6C8", b.cab, (math.pi / 2, 0, 0), mat=vox.MATS["glow"])
def _bandana(b, cor):                    # bandana amarrada com nó atrás
    c = cor or LIMA
    box("band", (HEAD_W + 0.035, HEAD_D + 0.035, 0.14), (0, 0, 0.64), c, b.cab, 0.03)
    for r in (0.5, -0.4):
        box("band_no", (0.08, 0.2, 0.06), (0.1 if r > 0 else -0.05, -FRONT + 0.1, 0.62), c, b.cab, 0.02, rot=(r, 0, r * 0.6))
def _chapeu_papel(b, cor):               # chapéu de jornal dobrado (pintora)
    H = HEAD_H; c = cor or CREME
    for s in (-1, 1):
        box("papel", (0.98, 0.05, 0.46), (0, s * 0.13, H + 0.12), c, b.cab, 0.01, rot=(s * 0.55, 0, 0))
    box("papel_aba", (1.02, 0.56, 0.08), (0, 0, H - 0.02), c, b.cab, 0.01)
    for i, x in enumerate((-0.3, -0.1, 0.12)):
        box("papel_letra", (0.14, 0.02, 0.03), (x, -0.27, H + 0.16 - i * 0.04), "#8E8A86", b.cab, 0.003, rot=(-0.55, 0, 0))
def _cabelo_cachos(b, cor):              # cachos (escriba)
    c = cor or "#3A2A22"; H = HEAD_H
    box("cach_base", (HEAD_W + 0.04, HEAD_D + 0.04, 0.12), (0, 0.01, H - 0.05), c, b.cab, 0.04, z0=True)
    for x in (-0.32, -0.1, 0.12, 0.33):
        for y in (-0.26, 0.0, 0.26):
            prim("sph", "cacho", (x, y, H + 0.08), (0.15, 0.15, 0.12), c, b.cab)
    box("cach_nuca", (HEAD_W + 0.04, 0.12, 0.42), (0, -FRONT + 0.02, H - 0.38), c, b.cab, 0.03)
def _abafador(b, cor):                   # abafador de pista (laranja)
    c = cor or "#FF7A2F"; H = HEAD_H; W = HEAD_W / 2
    box("abaf_arco", (HEAD_W + 0.12, 0.1, 0.07), (0, 0.05, H + 0.04), "#2A2D3A", b.cab, 0.03)
    for x in (-1, 1):
        box("abaf_haste", (0.06, 0.1, 0.32), (x * (W + 0.04), 0.05, H - 0.15), "#2A2D3A", b.cab, 0.02)
        prim("cyl", "abaf_concha", (x * (W + 0.08), 0.05, 0.42), (0.2, 0.2, 0.16), c, b.cab, (0, math.pi / 2, 0))
def _canotier(b, cor):                   # chapéu de palha reto (feirante)
    c = cor or "#E3C27A"; H = HEAD_H
    prim("cyl", "palha_aba", (0, 0, H + 0.02), (0.74, 0.7, 0.04), c, b.cab)
    prim("cyl", "palha_copa", (0, 0, H + 0.13), (0.44, 0.42, 0.22), c, b.cab)
    prim("cyl", "palha_fita", (0, 0, H + 0.08), (0.445, 0.425, 0.07), "#2E4A7A", b.cab)
def _gorro(b, cor):                      # gorro de lã com pompom limão (influencer)
    c = cor or "#E5484D"; H = HEAD_H
    prim("dome", "gorro", (0, 0, H - 0.12), (0.52, 0.48, 0.42), c, b.cab)
    box("gorro_barra", (HEAD_W + 0.06, HEAD_D + 0.06, 0.15), (0, 0, H - 0.1), c, b.cab, 0.05)
    prim("sph", "pompom", (0, 0, H + 0.33), (0.13, 0.13, 0.13), LIMA, b.cab)
def _helice(b, cor):                     # boné de hélice (novato)
    H = HEAD_H
    prim("dome", "hel_cap", (0, 0, H - 0.1), (0.5, 0.46, 0.3), cor or "#F2C14E", b.cab)
    box("hel_pala", (0.5, 0.26, 0.04), (0, FRONT - 0.1, H - 0.03), "#E5484D", b.cab, 0.015)
    box("hel_haste", (0.04, 0.04, 0.16), (0, 0, H + 0.18), "#3A3F4B", b.cab, 0.01, z0=True)
    g = empty("helice", (0, 0, H + 0.35), b.cab)
    box("hel_pa", (0.6, 0.1, 0.025), (0.0, 0, 0), "#5FA8E8", g, 0.01)
    box("hel_pa2", (0.1, 0.6, 0.025), (0.0, 0, 0.005), "#E5484D", g, 0.01)
    def anim(t, g=g): g.rotation_euler = (0, 0, t * 9.0)
    b.anims.append(anim)
def _viseira(b, cor):                    # viseira verde de telegrafista
    box("vis_faixa", (HEAD_W + 0.035, HEAD_D + 0.035, 0.06), (0, 0, 0.7), "#2F6F5A", b.cab, 0.015)
    box("vis_aba", (0.8, 0.3, 0.025), (0, FRONT - 0.12, 0.7), "#3FAF6A", b.cab, 0.01, rot=(0.3, 0, 0))
def _coque(b, cor):                      # cabelo grisalho com coque (arquivista)
    c = cor or "#B9BCC4"; H = HEAD_H
    box("coq_base", (HEAD_W + 0.04, HEAD_D + 0.04, 0.14), (0, 0.01, H - 0.06), c, b.cab, 0.05, z0=True)
    box("coq_nuca", (HEAD_W + 0.04, 0.12, 0.42), (0, -FRONT + 0.02, H - 0.38), c, b.cab, 0.03)
    prim("sph", "coque", (0, 0.06, H + 0.18), (0.22, 0.2, 0.17), c, b.cab)
    box("coq_lapis", (0.04, 0.04, 0.42), (0.02, 0.06, H + 0.18), "#F2C14E", b.cab, 0.01, rot=(0, 1.1, 0))
def _oculos_meia(b, cor):                # óculos meia-lua na ponta (olhos ficam livres em cima)
    c = cor or "#C9973A"; y = FRONT - 0.03
    for x in (-0.2, 0.2):
        box("meia_lente", (0.24, 0.025, 0.09), (x, y, 0.23), "#DDEFF7", b.cab, 0.02)
        box("meia_aro", (0.26, 0.02, 0.025), (x, y - 0.005, 0.185), c, b.cab, 0.008)
    box("meia_ponte", (0.12, 0.02, 0.025), (0, y, 0.25), c, b.cab, 0.005)
    for x in (-1, 1):
        box("meia_cord", (0.012, 0.012, 0.34), (x * 0.36, y + 0.02, 0.06), c, b.cab, 0.003, rot=(0, x * 0.25, 0))
def _bone_tras(b, cor):                  # boné virado pra trás (câmera)
    c = cor or "#E5484D"; H = HEAD_H
    prim("dome", "bt_copa", (0, 0, H - 0.08), (0.5, 0.46, 0.3), c, b.cab)
    box("bt_pala", (0.6, 0.32, 0.05), (0, -FRONT + 0.12, H - 0.04), c, b.cab, 0.02)
    box("bt_regulador", (0.24, 0.03, 0.08), (0, FRONT + 0.0, H + 0.0), CREME, b.cab, 0.01)
def _cabelo_arrepiado(b, cor):           # cabelo espetado (cientista)
    c = cor or "#A58BE8"; H = HEAD_H
    box("arr_base", (HEAD_W + 0.04, HEAD_D + 0.04, 0.12), (0, 0.01, H - 0.05), c, b.cab, 0.04, z0=True)
    R = random.Random(5)
    for x in (-0.34, -0.12, 0.1, 0.32):
        for y in (-0.2, 0.15):
            box("espeto", (0.16, 0.16, 0.3), (x, y, H + 0.02), c, b.cab, 0.03, z0=True,
                rot=(R.uniform(-0.35, 0.35), x * 0.9 + R.uniform(-0.2, 0.2), 0))
def _goggles(b, cor):                    # óculos de proteção na testa
    box("gog_faixa", (HEAD_W + 0.035, HEAD_D + 0.035, 0.08), (0, 0, 0.7), "#3A3F4B", b.cab, 0.02)
    for x in (-0.18, 0.18):
        prim("cyl", "gog_aro", (x, FRONT - 0.04, 0.71), (0.13, 0.13, 0.08), "#3A3F4B", b.cab, (math.pi / 2, 0, 0))
        prim("cyl", "gog_lente", (x, FRONT - 0.085, 0.71), (0.1, 0.1, 0.02), cor or LIMA, b.cab, (math.pi / 2, 0, 0))
def _chanel(b, cor):                     # cabelo chanel (jurada)
    c = cor or "#2A1F1A"; H = HEAD_H
    box("ch_topo", (HEAD_W + 0.06, HEAD_D + 0.06, 0.16), (0, 0.01, H - 0.06), c, b.cab, 0.05, z0=True)
    box("ch_franja", (HEAD_W + 0.06, 0.12, 0.14), (0, FRONT - 0.03, H - 0.12), c, b.cab, 0.04)
    for x in (-1, 1):
        box("ch_lado", (0.08, HEAD_D + 0.06, 0.62), (x * (HEAD_W / 2 + 0.03), 0.01, H - 0.6), c, b.cab, 0.03, z0=True)
    box("ch_nuca", (HEAD_W + 0.06, 0.1, 0.62), (0, -FRONT + 0.03, H - 0.6), c, b.cab, 0.03, z0=True)
def _quepe_maquinista(b, cor):           # boné listrado de maquinista
    H = HEAD_H
    prim("cyl", "maq_copa", (0, 0.02, H + 0.06), (0.5, 0.47, 0.2), "#3B5BA9", b.cab)
    for a in range(0, 360, 30):
        r = math.radians(a)
        box("maq_lista", (0.05, 0.02, 0.2), (0.5 * math.sin(r), 0.02 - 0.47 * math.cos(r), H + 0.06), CREME, b.cab, 0.004, rot=(0, 0, r))
    prim("cyl", "maq_topo", (0, 0.02, H + 0.165), (0.5, 0.47, 0.02), "#3B5BA9", b.cab)
    box("maq_pala", (0.56, 0.24, 0.04), (0, FRONT - 0.08, H - 0.02), "#2A3D73", b.cab, 0.015, rot=(0.2, 0, 0))
def _headset(b, cor):                    # microfone de bochecha (apresentador de palco)
    c = cor or "#3A3F4B"; W = HEAD_W / 2
    box("hs_arco", (HEAD_W + 0.06, 0.05, 0.04), (0, 0.1, HEAD_H + 0.02), c, b.cab, 0.015)
    box("hs_orelha", (0.05, 0.12, 0.14), (W + 0.03, 0.08, 0.45), c, b.cab, 0.02)
    box("hs_haste", (0.035, 0.035, 0.5), (W + 0.03, -0.12, 0.4), c, b.cab, 0.01, rot=(0, 0, 0))
    box("hs_haste2", (0.035, 0.035, 0.42), (0.27, FRONT - 0.03, 0.17), c, b.cab, 0.01, rot=(0, math.pi / 2, 0))
    prim("sph", "hs_mic", (0.06, FRONT - 0.04, 0.17), (0.06, 0.06, 0.06), LIMA, b.cab)
def _topete(b, cor):                     # cabelo com topete (você)
    c = cor or "#2A1F1A"; H = HEAD_H
    box("top_base", (HEAD_W + 0.04, HEAD_D + 0.04, 0.16), (0, 0.01, H - 0.06), c, b.cab, 0.04, z0=True)
    box("top_topete", (0.62, 0.3, 0.16), (0.04, FRONT + 0.14, H + 0.06), c, b.cab, 0.06, rot=(-0.3, 0, -0.1))
    box("top_nuca", (HEAD_W + 0.04, 0.12, 0.4), (0, -FRONT + 0.02, H - 0.36), c, b.cab, 0.03)
    for x in (-1, 1):
        box("top_lado", (0.05, 0.34, 0.24), (x * (HEAD_W / 2 + 0.015), 0.1, H - 0.22), c, b.cab, 0.02)


# ---------------------------------------------------------------- corpo
YF = -TOR_D / 2                          # frente do tronco
def _dragonas(b, cor):
    for x in (-1, 1):
        box("drag", (0.26, 0.34, 0.06), (x * 0.3, 0, LEG_H + TOR_H + 0.0), OURO, b.corpo, 0.02)
        for i in range(4):
            box("drag_franja", (0.03, 0.03, 0.08), (x * (0.2 + i * 0.06), YF - 0.02, LEG_H + TOR_H - 0.06), OURO, b.corpo, 0.005)
def _botoes(b, cor):
    for x in (-0.1, 0.1):
        for z in (0.24, 0.36, 0.48):
            prim("cyl", "botao", (x, YF - 0.012, z), (0.032, 0.032, 0.02), cor or OURO, b.corpo, (math.pi / 2, 0, 0))
def _gravata_borboleta(b, cor):
    c = cor or LIMA; z = LEG_H + TOR_H - 0.06
    for s in (-1, 1):
        box("borb", (0.12, 0.03, 0.1), (s * 0.07, YF - 0.02, z), c, b.corpo, 0.02, rot=(0, s * 0.2, 0))
    box("borb_no", (0.05, 0.035, 0.06), (0, YF - 0.025, z), c, b.corpo, 0.01)
def _gola_alta(b, cor):
    box("gola_alta", (0.56, 0.4, 0.09), (0, 0, LEG_H + TOR_H - 0.02), cor or CREME, b.corpo, 0.02, z0=True)
def _colete_bolsos(b, cor):
    c = cor or "#6F7D4B"
    box("colete", (0.78, 0.56, 0.36), (0, 0, LEG_H + 0.02), c, b.corpo, 0.04, z0=True)
    for x, z in ((-0.2, 0.24), (0.2, 0.24), (-0.2, 0.4)):
        box("col_bolso", (0.18, 0.03, 0.11), (x, YF - 0.04, z), "#55613A", b.corpo, 0.015)
def _macacao(b, cor):
    c = cor or "#2F5D73"
    box("mac_peito", (0.4, 0.03, 0.2), (0, YF - 0.012, LEG_H + 0.2), c, b.corpo, 0.015)
    box("mac_bolso", (0.16, 0.035, 0.08), (0, YF - 0.02, LEG_H + 0.25), "#24495C", b.corpo, 0.01)
    for x in (-0.15, 0.15):
        box("mac_alca", (0.07, TOR_D + 0.03, 0.04), (x, 0, LEG_H + TOR_H + 0.005), c, b.corpo, 0.01)
        box("mac_alca_f", (0.07, 0.03, 0.2), (x, YF - 0.012, LEG_H + 0.3), c, b.corpo, 0.01, z0=True)
        prim("cyl", "mac_fivela", (x, YF - 0.03, LEG_H + 0.32), (0.03, 0.03, 0.02), OURO, b.corpo, (math.pi / 2, 0, 0))
def _respingos(b, cor):
    R = random.Random(11)
    for i in range(9):
        c = ("#F08BB0", "#F2C14E", "#5FA8E8", LIMA, "#E5484D")[i % 5]
        s = R.uniform(0.04, 0.08)
        box("resp", (s, 0.02, s), (R.uniform(-0.3, 0.3), YF - 0.012, R.uniform(LEG_H + 0.05, LEG_H + TOR_H - 0.05)), c, b.corpo, 0.01)
def _cachecol(b, cor):
    c = cor or "#E0A82E"
    box("cach_volta", (0.8, 0.6, 0.13), (0, 0, LEG_H + TOR_H - 0.06), c, b.corpo, 0.05)
    box("cach_ponta", (0.16, 0.05, 0.42), (-0.18, YF - 0.04, LEG_H - 0.02), c, b.corpo, 0.02, z0=True)
    for z in (0.06, 0.18, 0.3):
        box("cach_lista", (0.165, 0.055, 0.04), (-0.18, YF - 0.04, LEG_H + z), "#7A2E3A", b.corpo, 0.005)
def _colete_refletivo(b, cor):
    c = cor or LIMA
    box("refl", (0.78, 0.56, 0.36), (0, 0, LEG_H + 0.03), c, b.corpo, 0.04, z0=True)
    for z in (0.14, 0.28):
        box("refl_faixa", (0.79, 0.57, 0.05), (0, 0, LEG_H + z), "#D9DEE5", b.corpo, 0.01)
def _avental_listrado(b, cor):
    for i in range(7):
        x = -0.27 + i * 0.09
        box("av_lista", (0.09, 0.03, 0.44), (x, YF - 0.02, LEG_H - 0.06), "#3F8F6E" if i % 2 == 0 else CREME, b.corpo, 0.004, z0=True)
    box("av_bolso", (0.3, 0.035, 0.1), (0, YF - 0.035, LEG_H + 0.06), "#2E6E53", b.corpo, 0.01)
    box("av_cordao", (TOR_W + 0.02, TOR_D + 0.02, 0.035), (0, 0, LEG_H + 0.3), "#3F8F6E", b.corpo, 0.01)
def _puffer(b, cor):
    c = b.roupa
    for i in range(4):
        box("puf", (TOR_W + 0.08, TOR_D + 0.08, 0.11), (0, 0, LEG_H + 0.01 + i * 0.1), c, b.corpo, 0.05, z0=True)
    box("puf_ziper", (0.03, 0.03, 0.4), (0, YF - 0.05, LEG_H + 0.01), CREME, b.corpo, 0.005, z0=True)
def _mochila(b, cor):
    c = cor or "#E5484D"
    box("moch", (0.56, 0.24, 0.44), (0, -YF + 0.12, LEG_H + 0.04), c, b.corpo, 0.06, z0=True)
    box("moch_bolso", (0.36, 0.06, 0.18), (0, -YF + 0.26, LEG_H + 0.08), "#B83A3F", b.corpo, 0.03, z0=True)
    for x in (-0.22, 0.22):
        box("moch_alca", (0.07, 0.03, 0.34), (x, YF - 0.012, LEG_H + 0.1), "#B83A3F", b.corpo, 0.01, z0=True)
def _suspensorio(b, cor):
    for x in (-0.18, 0.18):
        box("susp", (0.06, 0.03, TOR_H), (x, YF - 0.01, LEG_H), cor or "#7A2E3A", b.corpo, 0.008, z0=True)
        box("susp_c", (0.06, TOR_D + 0.02, 0.03), (x, 0, LEG_H + TOR_H), cor or "#7A2E3A", b.corpo, 0.008)
def _cardiga(b, cor):
    box("card_v", (0.18, 0.03, 0.16), (0, YF - 0.012, LEG_H + TOR_H - 0.16), CREME, b.corpo, 0.01, z0=True)
    for z in (0.12, 0.22, 0.32):
        prim("cyl", "card_bt", (0, YF - 0.02, LEG_H + z - 0.02), (0.028, 0.028, 0.02), "#7A4E2D", b.corpo, (math.pi / 2, 0, 0))
    for x in (-0.22, 0.22):
        box("card_bolso", (0.16, 0.025, 0.1), (x, YF - 0.012, LEG_H + 0.1), "#C08E33", b.corpo, 0.01)
def _colete_prod(b, cor):
    box("prod", (0.78, 0.56, 0.36), (0, 0, LEG_H + 0.03), cor or "#24212D", b.corpo, 0.04, z0=True)
    box("prod_fita", (0.32, 0.03, 0.06), (-0.12, YF - 0.04, LEG_H + 0.3), "#C9CDD6", b.corpo, 0.005, rot=(0, 0.2, 0))
    box("prod_radio", (0.1, 0.05, 0.16), (-0.24, YF - 0.06, LEG_H + 0.08), TINTA, b.corpo, 0.015)
    box("prod_ant", (0.02, 0.02, 0.12), (-0.27, YF - 0.06, LEG_H + 0.24), TINTA, b.corpo, 0.005)
def _jaleco(b, cor):
    box("jal", (TOR_W + 0.04, TOR_D + 0.04, TOR_H + 0.08), (0, 0, LEG_H - 0.08), cor or "#F7F7F2", b.corpo, 0.05, z0=True)
    for s in (-1, 1):
        box("jal_lapela", (0.08, 0.03, 0.26), (s * 0.08, YF - 0.035, LEG_H + 0.2), "#DCDCD3", b.corpo, 0.01, z0=True, rot=(0, s * 0.35, 0))
    box("jal_bolso", (0.16, 0.035, 0.1), (-0.2, YF - 0.035, LEG_H + 0.24), "#DCDCD3", b.corpo, 0.01)
    for i, c in enumerate(("#E5484D", "#5FA8E8")):
        box("jal_caneta", (0.025, 0.03, 0.1), (-0.23 + i * 0.05, YF - 0.045, LEG_H + 0.3), c, b.corpo, 0.005)
def _jabot(b, cor):
    for i in range(3):
        box("jabot", (0.2 - i * 0.03, 0.04, 0.07), (0, YF - 0.03, LEG_H + TOR_H - 0.06 - i * 0.07), CREME, b.corpo, 0.025)
def _fita_metrica(b, cor):
    for x, r in ((-0.15, 0.06), (0.15, -0.06)):
        box("fita", (0.07, 0.02, 0.42), (x, YF - 0.05, LEG_H + 0.02), OURO, b.corpo, 0.004, z0=True, rot=(0, r, 0))
        for k in range(6):
            box("fita_marca", (0.035, 0.022, 0.008), (x - 0.01, YF - 0.06, LEG_H + 0.06 + k * 0.06), TINTA, b.corpo, 0.0)
    box("fita_nuca", (0.5, TOR_D + 0.08, 0.025), (0, 0, LEG_H + TOR_H + 0.01), OURO, b.corpo, 0.004)
def _colete_alfaiate(b, cor):
    c = cor or "#5B6270"
    box("alf", (0.78, 0.56, 0.34), (0, 0, LEG_H + 0.02), c, b.corpo, 0.04, z0=True)
    box("alf_v", (0.2, 0.03, 0.16), (0, YF - 0.025, LEG_H + 0.22), CREME, b.corpo, 0.01, z0=True)
    for z in (0.08, 0.15):
        prim("cyl", "alf_bt", (0, YF - 0.035, LEG_H + z), (0.025, 0.025, 0.02), TINTA, b.corpo, (math.pi / 2, 0, 0))
    prim("dome", "alfinetes", (-0.1, -0.02, -0.3), (0.11, 0.11, 0.07), "#E5484D", b.brL, (0, -math.pi / 2, 0))
def _lenco(b, cor):
    c = cor or "#E5484D"
    box("lenco_volta", (0.62, 0.42, 0.07), (0, 0, LEG_H + TOR_H - 0.02), c, b.corpo, 0.02)
    box("lenco_ponta", (0.2, 0.03, 0.2), (0, YF - 0.03, LEG_H + TOR_H - 0.14), c, b.corpo, 0.02, rot=(0, 0.785, 0))
def _blazer(b, cor):
    box("blz_camisa", (0.2, 0.03, 0.26), (0, YF - 0.012, LEG_H + TOR_H - 0.26), CREME, b.corpo, 0.01, z0=True)
    for s in (-1, 1):
        box("blz_lapela", (0.1, 0.035, 0.24), (s * 0.12, YF - 0.02, LEG_H + 0.16), "#B83A3F", b.corpo, 0.01, z0=True, rot=(0, -s * 0.3, 0))
def _fone_pescoco(b, cor):
    c = cor or "#24212D"
    box("fp_arco", (0.86, 0.1, 0.06), (0, -0.08, LEG_H + TOR_H + 0.04), c, b.corpo, 0.03)
    for x in (-1, 1):
        prim("cyl", "fp_concha", (x * 0.4, -0.12, LEG_H + TOR_H - 0.02), (0.13, 0.13, 0.09), c, b.corpo, (0, math.pi / 2, 0))
        prim("cyl", "fp_alm", (x * 0.35, -0.12, LEG_H + TOR_H - 0.02), (0.1, 0.1, 0.04), LIMA, b.corpo, (0, math.pi / 2, 0))
def _capuz(b, cor):
    box("capuz", (0.7, 0.24, 0.16), (0, -YF - 0.02, LEG_H + TOR_H - 0.06), b.roupa, b.corpo, 0.06)
    for x in (-0.1, 0.1):
        box("cordao", (0.03, 0.03, 0.2), (x, YF - 0.012, LEG_H + TOR_H - 0.22), CREME, b.corpo, 0.005)

ACESS.update(marca=_marca, quepe=_quepe, cabelo_prata=_cabelo_prata, lanterna=_lanterna, bandana=_bandana,
             chapeu_papel=_chapeu_papel, cabelo_cachos=_cabelo_cachos, abafador=_abafador, canotier=_canotier,
             gorro=_gorro, helice=_helice, viseira=_viseira, coque=_coque, oculos_meia=_oculos_meia,
             bone_tras=_bone_tras, cabelo_arrepiado=_cabelo_arrepiado, goggles=_goggles, chanel=_chanel,
             quepe_maquinista=_quepe_maquinista, headset=_headset, topete=_topete,
             dragonas=_dragonas, botoes=_botoes, gravata_borboleta=_gravata_borboleta, gola_alta=_gola_alta,
             colete_bolsos=_colete_bolsos, macacao=_macacao, respingos=_respingos, cachecol=_cachecol,
             colete_refletivo=_colete_refletivo, avental_listrado=_avental_listrado, puffer=_puffer,
             mochila=_mochila, suspensorio=_suspensorio, cardiga=_cardiga, colete_prod=_colete_prod,
             jaleco=_jaleco, jabot=_jabot, fita_metrica=_fita_metrica, colete_alfaiate=_colete_alfaiate,
             lenco=_lenco, blazer=_blazer, fone_pescoco=_fone_pescoco, capuz=_capuz)


# ---------------------------------------------------------------- objetos de mão novos (em pé, na frente do braço)
def _segura(m, nome, dy=-0.16):
    # pega inclinada pra frente: no gesto "mostra" (braço a -0,75) o objeto fica em pé na frente do corpo
    pega = empty(nome + "_pega", (0, -0.02, 0.0), m); pega.rotation_euler = (0.75, 0, 0); pega.scale = (1.3, 1.3, 1.3)
    return empty(nome, (0, dy, 0.02), pega)
def _luneta(b, m):
    g = _segura(m, "luneta")
    for i, (r, h) in enumerate(((0.07, 0.22), (0.058, 0.2), (0.046, 0.16))):
        prim("cyl", "lun", (0, 0, 0.11 + i * 0.19), (r, r, h), OURO if i != 1 else "#7A4E2D", g)
    prim("cyl", "lun_vidro", (0, 0, 0.5), (0.04, 0.04, 0.02), "#D6F0FF", g)
    g.rotation_euler = (0.15, 0, 0.25); return g
def _batuta(b, m):
    g = _segura(m, "batuta")
    prim("cyl", "bat_cabo", (0, 0, 0.05), (0.035, 0.035, 0.1), "#7A4E2D", g)
    prim("cyl", "bat_vara", (0, 0, 0.3), (0.012, 0.012, 0.42), CREME, g)
    g.rotation_euler = (0.15, 0, 0.35); return g
def _mapa(b, m):
    g = _segura(m, "mapa")
    prim("cyl", "mapa_rolo", (0, 0, 0.18), (0.065, 0.065, 0.5), "#EBDDBB", g)
    prim("cyl", "mapa_fita", (0, 0, 0.18), (0.068, 0.068, 0.05), "#E5484D", g)
    g.rotation_euler = (0.15, 0, 0.3); return g
def _chave(b, m):
    g = _segura(m, "chave")
    box("ch_cabo", (0.06, 0.035, 0.38), (0, 0, 0), "#AEB4BE", g, 0.012, z0=True)
    for x in (-0.055, 0.055):
        box("ch_boca", (0.04, 0.04, 0.12), (x, 0, 0.38), "#AEB4BE", g, 0.01, z0=True)
    box("ch_base", (0.15, 0.04, 0.05), (0, 0, 0.36), "#AEB4BE", g, 0.01)
    return g
def _rolo(b, m):
    g = _segura(m, "rolo")
    box("rolo_cabo", (0.04, 0.04, 0.3), (0, 0, 0), "#E5484D", g, 0.01, z0=True)
    box("rolo_haste", (0.2, 0.03, 0.03), (0.08, 0, 0.3), "#AEB4BE", g, 0.005)
    prim("cyl", "rolo_rolo", (0.2, 0, 0.36), (0.07, 0.07, 0.28), "#F08BB0", g, (0, math.pi / 2, 0))
    return g
def _pena(b, m):
    g = _segura(m, "pena")
    box("pena_haste", (0.02, 0.02, 0.5), (0, 0, 0), "#F4EEE2", g, 0.005, z0=True)
    for i in range(5):
        w = 0.16 - abs(i - 1.5) * 0.03
        box("pena_pluma", (w, 0.015, 0.08), (0.02, 0, 0.16 + i * 0.07), CREME if i % 2 else "#E9E4F2", g, 0.02, rot=(0, -0.3, 0))
    prim("cone", "pena_ponta", (0, 0, -0.03), (0.02, 0.02, 0.06), TINTA, g, (math.pi, 0, 0))
    g.rotation_euler = (0.15, 0, 0.3); return g
def _bastao(b, m):
    g = _segura(m, "bastao", -0.1)
    box("bast_cabo", (0.06, 0.06, 0.12), (0, 0, 0), TINTA, g, 0.015, z0=True)
    prim("cyl", "bast_luz", (0, 0, 0.32), (0.05, 0.05, 0.42), "#FF7A2F", g, mat=vox.MATS["glow"])
    g.rotation_euler = (0.15, 0, 0); return g
def _sineta(b, m):
    g = _segura(m, "sineta")
    box("sin_cabo", (0.05, 0.05, 0.2), (0, 0, 0.12), "#7A4E2D", g, 0.015, z0=True)
    prim("dome", "sin_sino", (0, 0, 0.14), (0.15, 0.15, 0.17), OURO, g, (math.pi, 0, 0))
    return g
def _selfie(b, m):
    g = _segura(m, "selfie")
    box("sf_vara", (0.035, 0.035, 0.75), (0, 0, 0), "#24212D", g, 0.01, z0=True)
    box("sf_cel", (0.24, 0.04, 0.4), (0, -0.02, 0.85), "#1D1B24", g, 0.03)
    box("sf_tela", (0.2, 0.01, 0.35), (0, -0.045, 0.85), LIMA, g, 0.02, mat=vox.MATS["glow"])
    g.rotation_euler = (0.15, 0, 0.3); return g
def _bilhete(b, m):
    g = _segura(m, "bilhete")
    box("bil", (0.34, 0.02, 0.22), (0, 0, 0.2), CREME, g, 0.01, z0=True)
    text3d("bil_t", "STOP.", 0.09, (0, -0.02, 0.31), TINTA, 0.004, g)
    g.rotation_euler = (0, 0, 0.15); return g
def _fichas(b, m):
    g = _segura(m, "fichas", -0.2)
    for i, c in enumerate(("#F2C14E", "#F08BB0", "#5FA8E8", CREME, LIMA)):
        box("ficha", (0.3, 0.2, 0.035), (0, 0, 0.04 + i * 0.04), c, g, 0.008, rot=(0, 0, (i - 2) * 0.08))
    return g
def _camera(b, m):
    g = _segura(m, "camera", -0.2)
    box("cam_corpo", (0.3, 0.42, 0.26), (0, 0, 0.12), "#24212D", g, 0.04)
    prim("cyl", "cam_lente", (0, -0.28, 0.13), (0.1, 0.1, 0.18), "#3A3F4B", g, (math.pi / 2, 0, 0))
    prim("cyl", "cam_vidro", (0, -0.37, 0.13), (0.08, 0.08, 0.02), "#5FA8E8", g, (math.pi / 2, 0, 0))
    prim("sph", "cam_rec", (0.1, 0.05, 0.27), (0.03, 0.03, 0.03), "#FF3B3B", g, mat=vox.MATS["glow"])
    return g
def _frasco(b, m):
    g = _segura(m, "frasco")
    prim("sph", "fr_bola", (0, 0, 0.12), (0.14, 0.14, 0.14), "#DDF7E8", g)
    prim("sph", "fr_liq", (0, 0, 0.1), (0.115, 0.115, 0.1), LIMA, g, mat=vox.MATS["glow"])
    prim("cyl", "fr_gargalo", (0, 0, 0.3), (0.045, 0.045, 0.16), "#DDF7E8", g)
    for i in range(3):
        prim("sph", "fr_bolha", (0.02 * (i - 1), 0, 0.42 + i * 0.07), (0.035, 0.035, 0.035), LIMA, g, mat=vox.MATS["glow"])
    return g
def _placa_nota(b, m):
    g = _segura(m, "nota")
    box("nota_cabo", (0.04, 0.04, 0.32), (0, 0, 0), "#7A4E2D", g, 0.01, z0=True)
    box("nota_placa", (0.36, 0.04, 0.3), (0, 0, 0.44), CREME, g, 0.03)
    text3d("nota_t", "10", 0.2, (0, -0.03, 0.44), TINTA, 0.01, g)
    return g
def _tesoura(b, m):
    g = _segura(m, "tesoura")
    for s in (-1, 1):
        box("tes_lam", (0.03, 0.02, 0.32), (s * 0.02, 0, 0.12), "#D9DEE5", g, 0.006, z0=True, rot=(0, s * 0.18, 0))
        prim("torus", "tes_anel", (s * 0.05, 0, 0.07), (0.05, 0.05, 0.05), "#E5484D", g, (math.pi / 2, 0, 0), r=0.3)
    return g
def _relogio(b, m):
    g = _segura(m, "relogio")
    prim("cyl", "rel_caixa", (0, 0, 0.2), (0.14, 0.14, 0.05), OURO, g, (math.pi / 2, 0, 0))
    prim("cyl", "rel_mostr", (0, -0.03, 0.2), (0.115, 0.115, 0.02), CREME, g, (math.pi / 2, 0, 0))
    box("rel_ponteiro", (0.015, 0.01, 0.08), (0, -0.045, 0.23), TINTA, g, 0.0)
    box("rel_ponteiro2", (0.06, 0.01, 0.015), (0.025, -0.045, 0.2), TINTA, g, 0.0)
    box("rel_corrente", (0.02, 0.02, 0.12), (0, 0, 0.06), OURO, g, 0.005, z0=True)
    return g
def _cartoes(b, m):
    g = _segura(m, "cartoes")
    for i in range(3):
        box("cartao", (0.3, 0.02, 0.2), (0.01 * i, 0.012 * i, 0.16 + 0.01 * i), ("#F4EEE2", "#FFFFFF", LIMA)[i], g, 0.01, z0=True)
    return g

MAO.update(luneta=_luneta, batuta=_batuta, mapa=_mapa, chave=_chave, rolo=_rolo, pena=_pena, bastao=_bastao,
           sineta=_sineta, selfie=_selfie, bilhete=_bilhete, fichas=_fichas, camera=_camera, frasco=_frasco,
           placa_nota=_placa_nota, tesoura=_tesoura, relogio=_relogio, cartoes=_cartoes)


# ---------------------------------------------------------------- ELENCO (use estes; as RECEITAS antigas ficam só pra projetos velhos)
M_ = ["marca"]
ELENCO = {
    #  tipo             função na história                       receita
    "capita":       ("Comandante / dona do projeto",          dict(chapeu="quepe", mao="luneta", roupa="#1D3B5C", extras=M_ + ["dragonas", "botoes"])),
    "maestro":      ("Coordena o time / divide tarefas",      dict(cabelo=None, chapeu="cabelo_prata", roupa="#2B2A33", mao="batuta", extras=M_ + ["gola_alta", "gravata_borboleta"])),
    "mapeadora":    ("Pesquisa / acha informação",            dict(chapeu="lanterna", cabelo="#7A4E2D", mao="mapa", roupa="#E9DCC2", extras=M_ + ["colete_bolsos"])),
    "mecanica":     ("Programa / conserta / automatiza",      dict(chapeu="bandana", mao="chave", roupa="#2F5D73", extras=M_ + ["macacao"])),
    "pintora":      ("Design / deixa bonito",                 dict(chapeu="chapeu_papel", mao="rolo", roupa="#7FA3CC", extras=M_ + ["respingos"])),
    "escriba":      ("Escreve texto / roteiro / copy",        dict(chapeu="cabelo_cachos", mao="pena", roupa="#7A2E3A", extras=M_ + ["cachecol"])),
    "pista":        ("Tráfego / anúncios / direciona gente",  dict(chapeu="abafador", mao="bastao", mao_esq="bastao", roupa="#2A2D3A", extras=M_ + ["colete_refletivo"])),
    "feirante":     ("Vende / oferta / atende",               dict(chapeu="canotier", mao="sineta", roupa="#F4F1EA", extras=M_ + ["avental_listrado"])),
    "influencer":   ("Social media / posta / grava story",    dict(chapeu="gorro", mao="selfie", roupa="#3FB8A9", extras=M_ + ["puffer"])),
    "novato":       ("Iniciante / estagiário / dúvida",       dict(chapeu="helice", roupa="#5FA8E8", extras=M_ + ["mochila", "cracha"])),
    "telegrafista": ("Economiza / resume / fala pouco",       dict(chapeu="viseira", cabelo="#3A2A22", mao="bilhete", roupa="#F4F1EA", extras=M_ + ["suspensorio"])),
    "arquivista":   ("Memória / organiza / biblioteca",       dict(chapeu="coque", rosto=["oculos_meia"], mao="fichas", roupa="#D9A441", extras=M_ + ["cardiga"])),
    "camera":       ("Vídeo / grava / edita",                 dict(chapeu="bone_tras", mao="camera", roupa="#3B4256", extras=M_ + ["colete_prod"])),
    "cientista":    ("Experimento / o mais doido / teste",    dict(chapeu="cabelo_arrepiado", rosto=["goggles"], mao="frasco", roupa="#F7F7F2", extras=M_ + ["jaleco"])),
    "jurada":       ("Avalia / dá nota / decide",             dict(chapeu="chanel", mao="placa_nota", roupa="#1D1B24", extras=M_ + ["jabot"])),
    "alfaiate":     ("Humaniza / ajusta sob medida",          dict(cabelo="#8A5A3B", mao="tesoura", roupa="#F4F1EA", extras=M_ + ["colete_alfaiate", "fita_metrica"])),
    "maquinista":   ("Agenda / calendário / no horário",      dict(chapeu="quepe_maquinista", mao="relogio", roupa="#3B5BA9", extras=M_ + ["lenco", "macacao"])),
    "apresentador": ("Apresenta / abre portas / host",        dict(chapeu="headset", cabelo="#E8C15A", mao="cartoes", roupa="#E5484D", extras=M_ + ["blazer"])),
    "voce":         ("Você (humano)",                         dict(pele=PELES["humano"], chapeu="topete", roupa="#6F7A3C", braco="roupa", extras=M_ + ["capuz", "fone_pescoco"])),
}
def elenco(nome, tipo, **kw):
    """b = elenco("cap", "capita")  — boneco do elenco próprio (com assinatura)."""
    d = dict(ELENCO[tipo][1]); d.update(kw)
    return Boneco(nome, **d)
def _microfone2(b, m):                   # microfone de mão em pé (gesto "mostra" leva perto da boca)
    g = _segura(m, "microfone2")
    prim("cyl", "mic_cabo", (0, 0, 0.12), (0.05, 0.05, 0.26), "#24212D", g)
    prim("sph", "mic_globo", (0, 0, 0.32), (0.1, 0.1, 0.1), "#AEB4BE", g)
    prim("cyl", "mic_anel", (0, 0, 0.25), (0.06, 0.06, 0.03), LIMA, g)
    return g
MAO["microfone2"] = _microfone2
