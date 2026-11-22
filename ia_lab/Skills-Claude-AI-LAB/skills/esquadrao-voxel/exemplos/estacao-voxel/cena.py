# Esquadrão Voxel — "Estação Voxel" (Reel de estreia da skill com o elenco novo).
# Um trem leva a ideia por estações (roteiro → voz → cenário 3D → câmera); na última o elenco espera o Reel pronto.
import sys, os
sys.path.insert(0, os.path.expanduser(r"~\.claude\skills\esquadrao-voxel\scripts\molde"))
import math, random, bpy, vox, cenario as C, bonecos as B
from vox import box, prim, empty, painel, show, win, ease, eout, eback, lerp, clamp

DUR = 28.4
vox.PALETAS["manha"]["amb"] = 0.6
vox.setup(DUR, paleta="manha")
vox.PAL["acento"] = "#C6F432"
GL = vox.MATS["glow"]
GL.node_tree.nodes["Principled BSDF"].inputs["Emission Strength"].default_value = 1.3
vox.LUZES["frente"].data.energy = 3400
vox.LUZES["lua"].data.energy = 2.8
vox.cam_d.shift_y = 0.07                  # desce o assunto pra faixa segura (y 800–1450)
R = random.Random(3)

# estações: (x, nome, cor do telhado, tela)
EST = [(0, "ideia", "#F2C14E", None), (12, "roteiro", "#E9785F", "tela_roteiro.png"), (24, "voz", "#5FA8D3", "tela_voz.png"),
       (36, "cenario", "#B48EE0", "tela_cenario.png"), (48, "camera", "#4FB3A9", "tela_camera.png")]
XF = 62.0                                  # estação final

# ---------------------------------------------------------------- chão, trilho, paisagem
box("grama", (140, 60, 0.2), (30, 8, -0.2), "#A6CF6E", bevel=0, z0=True)
box("brita", (92, 1.9, 0.1), (30, 0, -0.04), "#B9B1A6", bevel=0.02, z0=True)
for y in (-0.45, 0.45):
    box("trilho", (92, 0.09, 0.11), (30, y, 0.1), "#7A7F8A", bevel=0.015, z0=True)
x = -16
while x < 76:
    box("dormente", (0.22, 1.35, 0.08), (x, 0, 0.04), "#8A5A3A", bevel=0.01, z0=True); x += 0.62
for i in range(26):                                   # morros ao fundo
    hx = -14 + i * 3.6 + R.uniform(-1, 1)
    prim("dome", "morro", (hx, R.uniform(17, 24), -0.2), (R.uniform(4, 7), 3, R.uniform(2.5, 5)), R.choice(["#7FB85A", "#8CC465", "#6FA84E"]))
def arvore(x, y, s=1.0):
    box("tronco", (0.22 * s, 0.22 * s, 0.6 * s), (x, y, 0), "#8A5A3A", bevel=0.02, z0=True)
    for k, (w, z) in enumerate(((1.0, 0.55), (0.75, 1.05), (0.5, 1.45))):
        box("copa", (w * s, w * s, 0.5 * s), (x, y, z * s), R.choice(["#4FA35A", "#5DB86A", "#3F8F4E"]), bevel=0.05, z0=True)
def casinha(x, y, cor):
    box("casa", (1.6, 1.4, 1.2), (x, y, 0), cor, bevel=0.04, z0=True)
    box("telhado", (1.8, 1.6, 0.35), (x, y, 1.2), "#C9603E", bevel=0.04, z0=True)
    box("janela", (0.4, 0.05, 0.4), (x - 0.35, y - 0.72, 0.6), "#FFE6B0", bevel=0.01)
    box("porta", (0.38, 0.05, 0.7), (x + 0.35, y - 0.72, 0), "#7A4E2D", bevel=0.01, z0=True)
for i in range(30):
    ax = -12 + i * 2.9 + R.uniform(-0.8, 0.8)
    if any(abs(ax - e[0]) < 3.6 for e in EST) or abs(ax - XF) < 7.5: continue
    arvore(ax, R.uniform(5.5, 8.5), R.uniform(0.9, 1.4))
for i in range(12):
    casinha(-8 + i * 7.3 + R.uniform(-1, 1), R.uniform(10, 13), R.choice(["#F3E9D8", "#F2D0D6", "#CFE3EE", "#F5E0B8"]))

# ---------------------------------------------------------------- estações
def estacao(x, nome, cor, tela, larg=6.0):
    box("plat", (larg, 2.3, 0.5), (x, 2.05, 0), "#D9CFBE", bevel=0.04, z0=True)
    box("plat_borda", (larg, 0.18, 0.06), (x, 0.98, 0.5), "#F2C14E", bevel=0.01, z0=True)
    for sx in (-1, 1):
        box("poste", (0.16, 0.16, 2.9), (x + sx * (larg / 2 - 0.3), 2.9, 0.5), "#3B4256", bevel=0.02, z0=True)
    box("teto", (larg + 0.6, 2.8, 0.22), (x, 2.2, 3.4), cor, bevel=0.05, z0=True)
    box("teto_faixa", (larg + 0.62, 2.82, 0.08), (x, 2.2, 3.4), "#24212D", bevel=0.01, z0=True)
    box("placa_fundo", (3.0, 0.1, 0.72), (x, 0.74, 3.9), "#24212D", bevel=0.03)
    painel("placa_" + nome, f"let_{nome}.png", 2.85, 0.62, (x, 0.68, 3.9), emit=0.95)
    if tela:
        box("tela_moldura", (2.2, 0.12, 1.4), (x + 1.6, 3.0, 1.75), "#24212D", bevel=0.04)
        painel("tela_" + nome, tela, 2.05, 1.25, (x + 1.6, 2.93, 1.75), emit=1.1)
        box("tela_pe", (0.12, 0.12, 1.1), (x + 1.6, 3.05, 0.5), "#24212D", bevel=0.01, z0=True)
    C.planta(x - larg / 2 + 0.6, 2.8, 0.5, 0.9)
for x, nome, cor, tela in EST: estacao(x, nome, cor, tela)
# final: arquibancada pro elenco + pedestal do Reel + letreiro
box("fin_plat", (13, 5.6, 0.5), (XF, 3.6, 0), "#D9CFBE", bevel=0.04, z0=True)
box("fin_borda", (13, 0.18, 0.06), (XF, 0.88, 0.5), "#C6F432", bevel=0.01, z0=True)
for k, (y, h) in enumerate(((3.05, 0.5), (4.05, 1.0))):
    box("degrau", (8.0, 1.1, h), (XF, y, 0.5), ["#E9785F", "#5FA8D3"][k], bevel=0.05, z0=True)
for sx in (-1, 1):
    box("fin_poste", (0.2, 0.2, 4.6), (XF + sx * 6.1, 5.6, 0.5), "#3B4256", bevel=0.02, z0=True)
box("fin_teto", (13.6, 3.4, 0.3), (XF, 4.9, 5.1), "#24212D", bevel=0.05, z0=True)
painel("let_final", "let_final.png", 4.2, 0.6, (XF, 3.15, 5.0), emit=0.95)
neon = C.neon(XF, 3.1, 6.0, 5.4, 0.81, "neon_voxel.png", "#C6F432", 0)
box("pedestal", (1.1, 1.1, 0.65), (XF, 1.55, 0.5), "#24212D", bevel=0.06, z0=True)
box("ped_topo", (1.16, 1.16, 0.06), (XF, 1.55, 1.15), "#C6F432", bevel=0.02, z0=True)
PED = (XF, 1.55, 1.22)

# ---------------------------------------------------------------- trem
BZ = 0.62                                   # topo do vagão
trem = empty("trem")
box("vag", (1.9, 1.1, 0.26), (0, 0, 0.36), "#B48EE0", trem, 0.05, z0=True)
for sy in (-1, 1): box("vag_grade", (1.9, 0.08, 0.16), (0, sy * 0.51, 0.6), "#7B5BD6", trem, 0.02, z0=True)
box("engate", (0.7, 0.14, 0.1), (1.25, 0, 0.42), "#3B4256", trem, 0.02)
loc = empty("loco", (2.65, 0, 0), trem)
box("loco_base", (2.6, 1.15, 0.36), (0, 0, 0.3), "#24212D", loc, 0.04, z0=True)
prim("cyl", "caldeira", (0.35, 0, 1.08), (0.46, 0.46, 1.6), "#E5484D", loc, (0, math.pi / 2, 0))
for xx in (-0.15, 0.55): prim("cyl", "aro", (xx, 0, 1.08), (0.48, 0.48, 0.07), "#F2C14E", loc, (0, math.pi / 2, 0))
prim("cyl", "chamine", (0.85, 0, 1.75), (0.17, 0.17, 0.6), "#24212D", loc)
prim("cyl", "chamine_boca", (0.85, 0, 2.1), (0.26, 0.26, 0.12), "#24212D", loc)
prim("dome", "domo", (0.2, 0, 1.5), (0.2, 0.2, 0.2), "#F2C14E", loc)
prim("sph", "farol", (1.18, 0, 1.08), (0.15, 0.15, 0.15), "#FFF6C8", loc, mat=GL)
box("limpa", (0.4, 1.0, 0.3), (1.35, 0, 0.12), "#F2C14E", loc, 0.03, z0=True, rot=(0, 0.5, 0))
box("cab_piso", (1.0, 1.15, 0.14), (-0.85, 0, 0.66), "#24212D", loc, 0.02, z0=True)
for sy in (-1, 1): box("cab_lado", (1.0, 0.08, 0.5), (-0.85, sy * 0.54, 0.8), "#E5484D", loc, 0.02, z0=True)
box("cab_fundo", (0.08, 1.15, 0.5), (-1.32, 0, 0.8), "#E5484D", loc, 0.02, z0=True)
for xx in (-1.3, -0.4):
    for sy in (-1, 1): box("cab_poste", (0.08, 0.08, 0.95), (xx, sy * 0.52, 1.3), "#24212D", loc, 0.01, z0=True)
box("cab_teto", (1.25, 1.35, 0.14), (-0.85, 0, 2.22), "#24212D", loc, 0.04, z0=True)
box("faixa_lima", (2.0, 1.17, 0.07), (0.3, 0, 0.62), "#C6F432", loc, 0.01, z0=True)
RODAS = []
for gx, rr in ((-0.6, 0.2), (0.6, 0.2)):
    for sy in (-1, 1):
        g = empty("roda", (gx, sy * 0.58, 0.22), trem); prim("cyl", "r", (0, 0, 0), (rr, rr, 0.08), "#3B4256", g, (math.pi / 2, 0, 0))
        box("raio", (0.3, 0.09, 0.04), (0, sy * 0.01, 0), "#F2C14E", g, 0.005); RODAS.append(g)
for gx, rr in ((2.0, 0.24), (2.95, 0.3), (3.65, 0.24)):
    for sy in (-1, 1):
        g = empty("roda", (gx, sy * 0.6, rr), trem); prim("cyl", "r", (0, 0, 0), (rr, rr, 0.08), "#3B4256", g, (math.pi / 2, 0, 0))
        box("raio", (rr * 1.5, 0.09, 0.05), (0, sy * 0.01, 0), "#E5484D", g, 0.005); RODAS.append(g)
FUMACA = [prim("sph", "fumaca", (0, 0, -9), (0.3, 0.3, 0.3), "#FFFFFF") for _ in range(12)]

# horário do trem: (t, x do vagão) — paradas com rampa de aceleração
TR = [(0, 0), (1.5, 0), (5.7, 12), (7.95, 12), (8.85, 24), (10.45, 24), (11.35, 36), (13.95, 36), (14.85, 48), (17.6, 48), (18.6, XF), (20.1, XF), (21.7, XF + 18), (DUR + 1, XF + 18)]
def tx(t):
    if t <= TR[0][0]: return TR[0][1]
    for (ta, xa), (tb, xb) in zip(TR, TR[1:]):
        if ta <= t <= tb: return xa if xa == xb else lerp(xa, xb, ease((t - ta) / (tb - ta)))
    return TR[-1][1]
def andando(t): return abs(tx(t + 0.03) - tx(t - 0.03)) > 0.01

# ---------------------------------------------------------------- o objeto que viaja e se transforma
def item_ideia(g):
    prim("sph", "bulbo", (0, 0, 0.42), (0.26, 0.26, 0.3), "#FFE27A", g, mat=GL)
    prim("cyl", "rosca", (0, 0, 0.12), (0.13, 0.13, 0.18), "#AEB4BE", g)
def item_roteiro(g):
    box("folha", (0.52, 0.05, 0.68), (0, 0, 0.02), "#FFFDF7", g, 0.015, z0=True)
    box("cab", (0.52, 0.055, 0.12), (0, -0.002, 0.58), "#C6F432", g, 0.01, z0=True)
    for k in range(5): box("linha", (0.36 - 0.05 * (k % 2), 0.056, 0.035), (-0.02, -0.004, 0.46 - k * 0.08), "#24212D", g, 0.004, z0=True)
def item_voz(g):
    box("caixa", (0.74, 0.34, 0.44), (0, 0, 0.02), "#24212D", g, 0.05, z0=True)
    for k, hgt in enumerate((0.12, 0.26, 0.34, 0.2, 0.3, 0.14)):
        box("barra", (0.06, 0.05, hgt), (-0.25 + k * 0.1, -0.17, 0.24 - hgt / 2 + 0.02), "#FF6B5B", g, 0.01, z0=True)
def item_maquete(g):                         # mini cenário 3D: base de grama, casinha, árvore e um bonequinho
    box("base", (0.8, 0.6, 0.1), (0, 0, 0.02), "#A6CF6E", g, 0.02, z0=True)
    box("casa", (0.26, 0.22, 0.22), (-0.2, 0.08, 0.12), "#F3E9D8", g, 0.02, z0=True)
    box("tel", (0.3, 0.26, 0.08), (-0.2, 0.08, 0.34), "#C9603E", g, 0.02, z0=True)
    box("arv", (0.16, 0.16, 0.3), (0.25, 0.12, 0.12), "#4FA35A", g, 0.03, z0=True)
    box("bon_c", (0.16, 0.14, 0.16), (0.04, -0.12, 0.2), "#DE7350", g, 0.02, z0=True)
    box("bon_b", (0.12, 0.1, 0.1), (0.04, -0.12, 0.11), "#5FA8D3", g, 0.01, z0=True)
def item_video(g):
    box("tela", (0.8, 0.14, 0.52), (0, 0, 0.02), "#24212D", g, 0.04, z0=True)
    box("vidro", (0.68, 0.15, 0.4), (0, -0.002, 0.08), "#5FA8D3", g, 0.02, z0=True)
    prim("cone", "play", (0.02, -0.09, 0.28), (0.12, 0.12, 0.03), "#C6F432", g, (math.pi / 2, 0, -math.pi / 2), seg=3)
    box("leg", (0.4, 0.152, 0.05), (0, -0.003, 0.12), "#FFFFFF", g, 0.01, z0=True)
def item_post(g):
    box("cel", (0.44, 0.09, 0.8), (0, 0, 0.02), "#24212D", g, 0.06, z0=True)
    box("cel_tela", (0.38, 0.092, 0.68), (0, -0.003, 0.08), "#C6F432", g, 0.04, z0=True, mat=GL)
    prim("cone", "play", (0.03, -0.06, 0.42), (0.1, 0.1, 0.02), "#24212D", g, (math.pi / 2, 0, -math.pi / 2), seg=3)
FORMAS = []
for fn in (item_ideia, item_roteiro, item_voz, item_maquete, item_video, item_post):
    g = empty("forma"); fn(g); show(g, 0); FORMAS.append(g)
hook_post = empty("hook_post"); item_post(hook_post); show(hook_post, 0)
TROCA = [7.5, 9.9, 13.75, 17.1, 19.25]
T_JOGA = (0.62, 1.12)                        # a ideia voa da mão pro vagão
T_PULO = (19.0, 19.5)                        # o Reel pula do vagão pro pedestal
def item_pos(t):
    if t < T_JOGA[1]: return None
    if t < T_PULO[0]:
        z = BZ
        for s in TROCA[:4]:
            if 0 <= t - s < 0.35: z += 0.3 * math.sin(math.pi * (t - s) / 0.35)
        return (tx(t), 0, z)
    k = clamp((t - T_PULO[0]) / (T_PULO[1] - T_PULO[0]))
    return (lerp(XF, PED[0], k), lerp(0, PED[1], k), lerp(BZ, PED[2], k) + 1.1 * math.sin(math.pi * k))

# ---------------------------------------------------------------- personagens das estações
def em(b, x, y, z=0.5, yaw=0.0):
    b.trilha = [(0, (x, y), yaw), (DUR, (x, y), yaw)]; b.chao = [(0, z)]; return b
voce1 = em(B.elenco("voce1", "voce"), -0.9, 1.75)
bulbo_mao = prim("sph", "bulbo_mao", (0, -0.12, -0.04), (0.2, 0.2, 0.23), "#FFE27A", voce1.maoR, mat=GL)
voce1.gesto("ergueR", 0.05, 0.6).gesto("acena", 1.25, 2.0)
escriba = em(B.elenco("escriba1", "escriba"), 10.6, 1.75)
escriba.gesto("mostra", 5.4, 6.3).gesto("bate", 6.3, 7.3).gesto("aponta", 7.3, 7.6).gesto("comemora", 7.6, 8.3)
voce2 = em(B.elenco("voce2", "voce", mao="microfone2"), 22.6, 1.75)
voce2.gesto("mostra", 8.6, 10.0).gesto("fala", 8.8, 10.0).gesto("comemora", 10.0, 10.6)
pintora = em(B.elenco("pintora1", "pintora"), 34.1, 1.75, yaw=-0.25)
mecanica = em(B.elenco("mecanica1", "mecanica"), 35.15, 1.75, yaw=0.2)
pintora.gesto("bate", 11.3, 13.6).gesto("comemora", 13.75, 14.4)
mecanica.gesto("bate", 11.55, 13.6).gesto("comemora", 13.8, 14.4)
camera = em(B.elenco("camera1", "camera"), 46.8, 1.75)
camera.gesto("mostra", 14.7, 17.1).gesto("comemora", 17.15, 17.8)
maq = B.elenco("maq", "maquinista", escala=0.72)
maq.trilha = [(0, (0, 0), 0.0), (DUR, (0, 0), 0.0)]
maq.gesto("acena", 1.3, 2.0).gesto("acena", 18.7, 19.6).gesto("fala", 5.0, 18.0)
ESTACAO = [voce1, escriba, voce2, pintora, mecanica, camera]

# ---------------------------------------------------------------- elenco na estação final (18, o maquinista está no trem)
FILAS = [  # (y, z, tipos)  — frente com vão no meio pro pedestal
    (2.15, 0.5, ["escriba", "pintora", "novato", None, "voce", "mecanica", "camera"]),
    (3.05, 1.0, ["alfaiate", "telegrafista", "feirante", "pista", "influencer", "apresentador"]),
    (4.05, 1.5, ["capita", "maestro", "mapeadora", "arquivista", "jurada", "cientista"]),
]
ELENCO = []
for fi, (y, z, tipos) in enumerate(FILAS):
    n = len(tipos)
    for j, tp in enumerate(tipos):
        if tp is None: continue
        xx = XF + (j - (n - 1) / 2) * (1.0 if fi == 0 else 1.08)
        b = em(B.elenco("f_" + tp, tp), xx, y, z, yaw=-0.12 * (j - (n - 1) / 2) / 3)
        k = len(ELENCO)
        b.gesto("olha", 2.1 + 0.05 * k, 3.4).gesto("acena", 3.6 + 0.04 * k, 4.9)
        b.gesto("comemora", 19.35 + 0.03 * k, 20.6)
        b.gesto("pula", 23.55 + 0.06 * (xx - XF + 3.5) * 1.6, 24.5 + 0.06 * (xx - XF + 3.5) * 1.6)
        b.gesto("acena", 25.6 + 0.03 * k, 28.2)
        if tp in ("pista",): b.gesto("mostra2", 21.6, 23.4)
        elif tp not in ("novato", "voce"): b.gesto("mostra", 21.6, 23.4)
        ELENCO.append(b)

# ---------------------------------------------------------------- câmera
def track(t):
    xs = sum(tx(t + d) for d in (-0.4, -0.2, 0, 0.2, 0.4)) / 5
    bump = sum(math.exp(-((t - s - 0.1) / 0.35) ** 2) for s in TROCA[:4])
    return ((xs - 0.9, -7.6 + 1.6 * bump, 2.5 - 0.25 * bump), (xs + 0.1, 1.0, 1.45 - 0.1 * bump), 30 + 5 * bump)
T_TR0, T_TR1 = 5.05, 18.65
vox.CAM = [
    (0.0, (-0.7, -6.6, 2.45), (-0.2, 0.9, 1.55), 31, "corte"),
    (2.0, (XF, -9.6, 2.9), (XF, 2.4, 1.9), 28, "chicote"),
    (T_TR0, *track(T_TR0), "chicote"),
    (T_TR1, (XF - 0.6, -8.0, 2.4), (XF - 0.3, 1.6, 1.5), 30, "corte"),
    (21.75, (XF, -9.6, 3.7), (XF, 2.8, 2.45), 28, "suave"),
    (25.4, (XF, -7.4, 2.4), (XF, 2.0, 1.7), 30, "suave"),
]
vox.DRIFT = 0.07
_cam_orig = vox.cam_at
def cam_at(t):
    if T_TR0 + vox.WHIP / 2 <= t < T_TR1: return track(t)
    return _cam_orig(t)
vox.cam_at = cam_at
vox.SHAKE = [(s, 0.35) for s in TROCA[:4]] + [(1.12, 0.3), (19.5, 0.6), (26.35, 0.5)]

def apply(t):
    x = tx(t)
    trem.location = (x, 0, 0.012 * math.sin(t * 40) if andando(t) else 0)
    for g in RODAS: g.rotation_euler = (0, x / 0.24, 0)
    maq.update(t)
    maq.root.location = (x + 1.8, 0, 0.66 + trem.location.z)
    for b in ESTACAO + ELENCO: b.update(t)
    show(bulbo_mao, 1 if t < T_JOGA[0] else 0, (0.2, 0.2, 0.23))
    # fumaça: bolinhas sobem da chaminé enquanto o trem anda (e um pouco parado)
    for i, f in enumerate(FUMACA):
        ph = (t * 1.3 + i / len(FUMACA)) % 1.0
        t0 = t - ph / 1.3
        forte = 1.0 if andando(t0) else 0.45
        cx = tx(t0) + 2.65 + 0.85 - ph * 1.2
        f.location = (cx, 0.1 * math.sin(i * 2.1), 2.2 + ph * 1.1)
        s = (0.12 + 0.22 * ph) * forte * (1 - ph ** 2)
        show(f, s, (1, 1, 1))
    p = item_pos(t)
    st = sum(1 for s in TROCA if t >= s)
    for k, g in enumerate(FORMAS):
        if k == 0 and T_JOGA[0] <= t < T_JOGA[1]:          # arremesso da mão pro vagão
            q = (t - T_JOGA[0]) / (T_JOGA[1] - T_JOGA[0])
            g.location = (lerp(-0.5, 0.0, q), lerp(1.6, 0, q), lerp(2.05, BZ, q) + 0.9 * math.sin(math.pi * q))
            g.rotation_euler = (0, q * 6, 0); show(g, 1.15); continue
        if p is None or k != st: show(g, 0); continue
        g.location = p; g.rotation_euler = (0, 0, 0.25 * math.sin(t * 2.5) if k == 5 else 0)
        t_st = TROCA[st - 1] if st else T_JOGA[1]
        s = (eback(clamp((t - t_st) / 0.3), 2.4) if st else 1.0) * 1.25
        if k == 5: s *= 1.0 + 0.7 * clamp((t - T_PULO[0]) / 0.5)
        show(g, s)
    if 2.2 <= t < 5.05:                                     # gancho: o Reel pronto já no pedestal lá no fim
        hook_post.location = PED; hook_post.rotation_euler = (0, 0, 0.25 * math.sin(t * 2.5))
        show(hook_post, 2.25 * eback(clamp((t - 2.35) / 0.35), 2.4))
    else: show(hook_post, 0)
    show(neon, win(t, 21.85, DUR + 1, 0.5))

vox.run(apply, anchors={"item": lambda t: item_pos(t) or (0, 0, -9), "pedestal": PED})
