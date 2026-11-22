# Esquadrão Voxel — "Fábrica de Reels": a ideia entra no funil, anda na esteira e sai Reel agendado.
import sys, os
sys.path.insert(0, os.path.expanduser(r"~\.claude\skills\esquadrao-voxel\scripts\molde"))
import math, bpy, vox, cenario as C, bonecos as B
from vox import box, prim, empty, painel, ponto, show, win, ease, eout, eback, lerp, clamp

DUR = 20.2
vox.PALETAS["manha"]["amb"] = 0.5
vox.setup(DUR, paleta="manha")
vox.PAL["acento"] = "#C6F432"
GL = vox.MATS["glow"]
GL.node_tree.nodes["Principled BSDF"].inputs["Emission Strength"].default_value = 1.3   # de dia o brilho é menor
vox.LUZES["frente"].data.energy = 3800
vox.LUZES["lua"].data.energy = 2.6

BZ = 0.95                     # altura do topo da esteira
X0, X1 = -2.6, 30.0           # começo / fim da esteira
MQ = [(6.0, "roteiro", "#E9785F"), (12.0, "voz", "#5FA8D3"), (18.0, "video", "#B48EE0"), (24.0, "agenda", "#7BC67E")]
EXIT_X = 31.4

# ---------------------------------------------------------------- galpão
C.piso(15, 0.5, 52, 12, "azulejo", "#C9C2B6")
box("parede", (52, 0.4, 10), (15, 4.7, 0), "#F3E9D8", bevel=0, z0=True)
box("rodape", (52, 0.1, 0.5), (15, 4.48, 0), "#2F6F73", bevel=0.01, z0=True)
for i in range(8):
    x = -6 + i * 6.2
    box("jan_mold", (5.0, 0.2, 4.2), (x, 4.45, 4.9), "#2F6F73", bevel=0.04)
    painel("janela", "janela_dia.png", 4.7, 3.9, (x, 4.33, 4.9), emit=0.95)
    box("jan_cruz", (0.12, 0.22, 3.9), (x, 4.32, 4.9), "#2F6F73", bevel=0.01)
    box("pilar", (0.6, 0.6, 9.5), (x + 3.1, 4.2, 0), "#2F6F73", bevel=0.05, z0=True)
for z, cor in ((2.2, "#E9785F"), (2.55, "#F2C14E")):
    prim("cyl", "cano", (15, 4.35, z), (0.12, 0.12, 52), cor, rot=(0, math.pi / 2, 0))
painel("let_fabrica", "let_fabrica.png", 9.0, 1.2, (15, 4.3, 7.9), emit=1.0)
for i in range(9):   # luminárias penduradas
    x = -4 + i * 4.3
    box("fio", (0.03, 0.03, 2.2), (x, 0.6, 6.3), "#3A3946", bevel=0, z0=True)
    prim("cone", "cupula", (x, 0.6, 6.2), (0.5, 0.5, 0.4), "#2F6F73")
    prim("sph", "lamp", (x, 0.6, 6.05), (0.14, 0.14, 0.14), "#FFE6B0", mat=GL)
ar2 = bpy.data.lights.new("frente2", "AREA"); ar2.energy = 3800; ar2.size = 40; ar2.color = vox.hexc(vox.PAL["frente"])[:3]
o2 = bpy.data.objects.new("frente2", ar2); vox.COLL.objects.link(o2); o2.location = (28, -22, 14); o2.rotation_euler = (math.radians(58), 0, 0)

# ---------------------------------------------------------------- esteira
L = X1 - X0; XC = (X0 + X1) / 2
box("est_base", (L, 1.3, BZ - 0.3), (XC, 0, 0.2), "#3B4256", bevel=0.04, z0=True)
box("est_lona", (L, 1.1, 0.08), (XC, 0, BZ - 0.1), "#24212D", bevel=0.02, z0=True)
for s in (-1, 1):
    box("est_trilho", (L, 0.1, 0.16), (XC, s * 0.62, BZ - 0.14), "#F2C14E", bevel=0.02, z0=True)
x = X0 + 0.4
while x < X1:
    for s in (-1, 1): box("est_pe", (0.16, 0.16, 0.25), (x, s * 0.5, 0), "#2A2533", bevel=0.02, z0=True)
    x += 2.4
CLEAT_SP, CLEAT_V = 0.7, 1.8
cleats = [box("taco", (0.07, 1.0, 0.03), (X0 + i * CLEAT_SP, 0, BZ - 0.02), "#4A4558", bevel=0.01, z0=True) for i in range(int(L / CLEAT_SP))]

# funil de ideias + plataforma do apresentador (você)
box("funil_base", (1.5, 1.5, BZ + 0.7), (-2.0, 0, 0), "#F2C14E", bevel=0.06, z0=True)
prim("cone", "funil", (-2.0, 0, BZ + 1.75), (1.0, 1.0, 1.1), "#F2C14E", rot=(math.pi, 0, 0))
prim("cyl", "funil_boca", (-2.0, 0, BZ + 2.3), (1.0, 1.0, 0.06), "#E0A82E")
painel("let_ideias", "let_ideias.png", 1.3, 0.3, (-2.0, -0.77, BZ + 0.35), emit=0.9)
box("plataforma", (1.5, 1.5, 1.5), (-3.9, 0, 0), "#5FA8D3", bevel=0.05, z0=True)

# máquinas
MAQ = {}
for mx, nome, cor in MQ:
    g = empty("maq_" + nome, (mx, 0, 0))
    for y in (-0.88, 0.88):
        box("parede_maq", (2.4, 0.26, 2.0), (0, y, BZ - 0.15), cor, g, 0.08, z0=True)
    box("teto_maq", (2.6, 2.1, 0.5), (0, 0, BZ + 1.75), cor, g, 0.1, z0=True)
    box("faixa", (2.62, 2.12, 0.12), (0, 0, BZ + 1.62), "#24212D", g, 0.03, z0=True)
    box("moldura_tela", (1.7, 0.08, 1.05), (0, -1.03, BZ + 0.85), "#24212D", g, 0.03)
    painel("tela_" + nome, f"tela_{nome}.png", 1.55, 0.9, (0, -1.08, BZ + 0.85), g, emit=1.15)
    box("placa_maq", (2.1, 0.1, 0.55), (0, -0.9, BZ + 2.55), "#24212D", g, 0.03)
    painel("let_" + nome, f"let_{nome}.png", 1.95, 0.43, (0, -0.96, BZ + 2.55), g, emit=0.95)
    prim("cyl", "chamine", (0.75, 0.3, BZ + 2.5), (0.2, 0.2, 0.7), "#3B4256", g)
    lampadas = [prim("sph", "luz_maq", (-0.8 + k * 0.4, -0.95, BZ + 1.95), (0.09, 0.09, 0.09), "#FFE27A", g, mat=GL) for k in range(5)]
    for s in (-1, 1):   # cortina de tiras na entrada/saída
        for k in range(5):
            box("tira", (0.03, 0.28, 1.3), (s * 1.2, -0.56 + k * 0.28, BZ + 0.85), "#2A2533", g, 0.005)
    MAQ[nome] = dict(g=g, luzes=lampadas, x=mx)

# saída: rampa + pedestal + arco
box("rampa", (1.2, 1.0, 0.08), (30.6, 0, BZ - 0.3), "#AEB4BE", bevel=0.02, rot=(0, math.radians(25), 0))
box("pedestal", (1.3, 1.3, 0.62), (EXIT_X, 0, 0), "#24212D", bevel=0.06, z0=True)
box("ped_topo", (1.36, 1.36, 0.06), (EXIT_X, 0, 0.62), "#C6F432", bevel=0.02, z0=True)
for s in (-1, 1): box("arco_pe", (0.3, 0.3, 3.6), (EXIT_X + s * 1.3, 0.2, 0), "#E9785F", bevel=0.05, z0=True)
box("arco_topo", (2.9, 0.3, 0.5), (EXIT_X, 0.2, 3.6), "#E9785F", bevel=0.05, z0=True)
painel("let_saida", "let_saida.png", 1.8, 0.4, (EXIT_X, 0.03, 3.85), emit=0.95)
neon = C.neon(EXIT_X, 4.2, 5.4, 3.4, 1.2, "neon_guia.png", "#C6F432", 0)
# cantinho do apresentador
box("pufe", (1.1, 1.0, 0.42), (33.3, 0.1, 0), "#E9785F", bevel=0.12, z0=True)
box("pufe_enc", (1.1, 0.3, 0.7), (33.3, 0.55, 0.3), "#E9785F", bevel=0.1, z0=True)
C.planta(34.4, 0.6, 0, 1.3)

# ---------------------------------------------------------------- o objeto que viaja (muda de forma em cada máquina)
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
def item_video(g):
    box("tela", (0.8, 0.14, 0.52), (0, 0, 0.02), "#24212D", g, 0.04, z0=True)
    box("vidro", (0.68, 0.15, 0.4), (0, -0.002, 0.08), "#5FA8D3", g, 0.02, z0=True)
    prim("cone", "play", (0.02, -0.09, 0.28), (0.12, 0.12, 0.03), "#C6F432", g, (math.pi / 2, 0, -math.pi / 2), seg=3)
    box("leg", (0.4, 0.152, 0.05), (0, -0.003, 0.12), "#FFFFFF", g, 0.01, z0=True)
def item_post(g):
    box("cel", (0.44, 0.09, 0.8), (0, 0, 0.02), "#24212D", g, 0.06, z0=True)
    box("cel_tela", (0.38, 0.092, 0.68), (0, -0.003, 0.08), "#C6F432", g, 0.04, z0=True, mat=GL)
    box("chk1", (0.06, 0.1, 0.16), (-0.06, -0.006, 0.36), "#FFFFFF", g, 0.01, rot=(0, 0.75, 0))
    box("chk2", (0.06, 0.1, 0.3), (0.06, -0.006, 0.42), "#FFFFFF", g, 0.01, rot=(0, -0.6, 0))
FORMAS = []
for fn in (item_ideia, item_roteiro, item_voz, item_video, item_post):
    g = empty("forma"); fn(g); show(g, 0); FORMAS.append(g)
hook_post = empty("hook_post"); item_post(hook_post); show(hook_post, 0)

# trajeto do objeto: (t, x) — dentro das máquinas troca de forma
TRAJ = [(4.75, -1.6), (5.85, 5.0), (6.15, 6.0), (6.5, 7.1),
        (7.55, 11.0), (7.9, 12.0), (8.35, 13.1),
        (9.45, 17.0), (9.8, 18.0), (10.2, 19.1),
        (12.3, 23.0), (12.65, 24.0), (13.05, 25.1), (13.95, 29.9)]
TROCA = [6.15, 7.9, 9.8, 12.65]          # meio de cada máquina
SAI = [6.5, 8.35, 10.2, 13.05]           # objeto sai transformado
def ix(t):
    if t <= TRAJ[0][0]: return TRAJ[0][1]
    for (ta, xa), (tb, xb) in zip(TRAJ, TRAJ[1:]):
        if ta <= t <= tb: return lerp(xa, xb, (t - ta) / (tb - ta))
    return TRAJ[-1][1]
def item_pos(t):
    if t < 4.75: return None
    if t < 4.95:   # cai do funil na esteira
        k = (t - 4.75) / 0.2; return (lerp(-2.0, -1.6, k), 0, BZ + 0.8 * (1 - k * k))
    if t <= 13.95:
        z = BZ
        for s in SAI:
            if 0 <= t - s < 0.35: z += 0.28 * math.sin(math.pi * (t - s) / 0.35)
        return (ix(t), 0, z)
    k = clamp((t - 13.95) / 0.4)   # desce a rampa e pula no pedestal
    return (lerp(29.9, EXIT_X, k), 0, lerp(BZ, 0.68, k) + 0.5 * math.sin(math.pi * k))

# ---------------------------------------------------------------- personagens
voce = B.receita("voce", "voce")
bulbo_mao = prim("sph", "bulbo_mao", (0, -0.1, -0.05), (0.2, 0.2, 0.23), "#FFE27A", voce.maoR, mat=GL)
caneca = prim("cyl", "caneca_lk", (0, -0.12, 0.05), (0.1, 0.1, 0.2), "#C6F432", voce.maoL)
voce.trilha = [(0, (-3.9, 0.1), 0.0), (14.45, (-3.9, 0.1), 0.0), (14.5, (32.35, -0.85), 0.0), (DUR, (32.35, -0.85), 0.0)]
voce.chao = [(0, 1.5), (14.5, 0.0)]
voce.gesto("ergueR", 0.3, 1.1).gesto("fala", 2.0, 4.4).gesto("ergueL", 15.35, 16.4).gesto("acena", 18.1, 19.6).gesto("pula", 19.7, 20.2)

capacetes = ["#F2C14E", "#FF6B5B", "#C6F432", "#5FA8D3"]
OPS = []
for i, (mx, nome, cor) in enumerate(MQ):
    b = B.Boneco("op" + nome, roupa="#2F6F73", calca="#2F6F73", chapeu="capacete", cor_chapeu=capacetes[i],
                 extras=["cracha"] + (["oculos"] if i % 2 else []), mao="prancheta" if i == 0 else None)
    b.trilha = [(0, (mx + 1.75, 1.35), -0.25), (DUR, (mx + 1.75, 1.35), -0.25)]   # atrás da esteira: não tapa o objeto
    t_in = TRAJ[1 + 3 * i][0]
    b.gesto("aponta", t_in - 0.4, t_in + 0.1).gesto("bate", t_in + 0.1, SAI[i] - 0.05).gesto("comemora", SAI[i], SAI[i] + 0.7)
    b.gesto("pula", 16.6 + 0.12 * i, 17.9).gesto("acena", 17.9, 19.5)
    OPS.append(b)

# ---------------------------------------------------------------- câmera
def track(t):
    xs = sum(ix(t + d) for d in (-0.4, -0.2, 0, 0.2, 0.4)) / 5
    bump = sum(math.exp(-((t - s - 0.12) / 0.32) ** 2) for s in SAI)
    return ((xs - 1.1, -8.6 + 1.8 * bump, 3.3 - 0.4 * bump), (xs + 0.4, 0, 1.55 - 0.1 * bump), 30 + 6 * bump)
T_TR0, T_TR1 = 4.45, 14.5
vox.CAM = [
    (0.0, (-3.0, -7.6, 3.5), (-2.9, 0, 2.3), 30, "corte"),
    (2.15, (31.3, -6.0, 2.6), (31.3, 0, 1.35), 34, "chicote"),
    (T_TR0, *track(T_TR0), "chicote"),
    (T_TR1, (32.0, -5.8, 2.4), (32.2, -0.5, 1.4), 36, "corte"),
    (16.45, (24.5, -14.0, 10.5), (19.0, 1.0, 1.2), 26, "suave"),
    (18.0, (31.9, -7.4, 2.5), (31.9, 0, 1.75), 32, "suave"),
]
vox.DRIFT = 0.08
_cam_orig = vox.cam_at
def cam_at(t):
    if T_TR0 + vox.WHIP / 2 <= t < T_TR1: return track(t)
    return _cam_orig(t)
vox.cam_at = cam_at
vox.SHAKE = [(s, 0.35) for s in SAI] + [(14.35, 0.5), (18.05, 0.6)]

def apply(t):
    voce.update(t)
    for b in OPS: b.update(t)
    show(bulbo_mao, 1 if t < 1.15 else 0, (0.2, 0.2, 0.23))
    show(caneca, 1 if t >= 14.5 else 0, (0.1, 0.1, 0.2))
    for i, c in enumerate(cleats):   # tacos da esteira andando
        c.location.x = X0 + ((i * CLEAT_SP + CLEAT_V * t) % L)
    p = item_pos(t)
    st = sum(1 for s in TROCA if t >= s)
    for k, g in enumerate(FORMAS):
        if p is None or k != st:
            if 1.15 <= t < 1.6 and k == 0:   # arremesso da mão pro funil
                q = (t - 1.15) / 0.45
                g.location = (lerp(-3.55, -2.0, q), lerp(-0.1, 0, q), lerp(3.3, BZ + 2.2, q) + 0.9 * math.sin(math.pi * q))
                g.rotation_euler = (0, q * 6, 0); show(g, 1.3); continue
            show(g, 0); continue
        g.location = p; g.rotation_euler = (0, 0, 0)
        t_st = TROCA[st - 1] if st else 4.75
        s = eback(clamp((t - t_st) / 0.3), 2.4) if st else 1.0
        s *= 1.6   # objeto grande pra ler no celular
        if p[0] > 30.5: s *= 1.0 + 0.04 * math.sin(t * 6)
        show(g, s)
    if 2.2 <= t < 4.45:   # gancho: o Reel pronto já saindo lá no fim
        k = clamp((t - 3.0) / 0.45)
        hook_post.location = (lerp(29.9, EXIT_X, k), 0, lerp(BZ, 0.68, k) + 0.5 * math.sin(math.pi * k))
        hook_post.rotation_euler = (0, 0, 0.3 * math.sin(t * 3) * k)
        show(hook_post, 1.6 if t >= 3.0 else 0)
    else: show(hook_post, 0)
    if t >= 14.35:
        FORMAS[4].rotation_euler = (0, 0, 0.35 * math.sin((t - 14.35) * 2.2))
    for i, (mx, nome, cor) in enumerate(MQ):   # máquinas tremem e piscam com o objeto dentro
        t_in, t_out = TRAJ[1 + 3 * i][0], SAI[i]
        on = t_in <= t <= t_out
        m = MAQ[nome]
        m["g"].location = (mx + (0.025 * math.sin(t * 55) if on else 0), 0, 0)
        m["g"].scale = (1, 1, 1 + (0.04 * math.sin(t * 30) if on else 0))
        for j, l in enumerate(m["luzes"]):
            l.hide_render = not (on and (int(t * 12) + j) % 2 == 0) and not (t_out < t < t_out + 0.6)
    show(neon, win(t, 18.05, DUR + 1, 0.45))

vox.run(apply, anchors={"item": lambda t: item_pos(t) or (0, 0, -9)})
