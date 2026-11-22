# Profissão — ateliê de costura: o caos do balcão e o app simples que resolve.
import sys, os, math
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "scripts", "molde"))  # no projeto: "../../lib"
import mvb
from mvb import obj, empty, text3d, hexc, ease, eout, eback, lerp, vlerp, win, Person, walk_pose, R

DUR = 44.6
mvb.setup(DUR)
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import cidade, titulos3d
T = dict(ia=1.0, costureira=4.66, problema=5.72, balcao=7.88, cliente=8.64, pergunta=9.72, calcula=11.32, anota=12.48,
         esquece=13.62, app=15.64, foto=18.1, ajuste=19.3, barra=20.24, cintura=20.78, ziper=21.36, preco=22.38,
         fila=23.56, data=25.2, pronto=26.26, msg=27.38, continua=29.12, cuida=31.1, comenta=32.94, rodada=34.42,
         cta=36.26, redes=40.16)
PURPLE = "#7B5BD6"

# ---------------------------------------------------------------- ateliê
cidade.build()
cidade.traffic()
obj("piso", "boxb", (0, 0, 0), (13, 10, 0.06), "#E8DCC8")
for i in range(0, 13):
    obj("tabua", "boxb", (-6 + i, 0, 0.06), (0.04, 10, 0.006), "#D9CBB2")
obj("fundo", "boxb", (0, 5.1, 0), (13.4, 0.3, 4.0), "#EBDDF2")
obj("lado", "boxb", (-6.6, 0, 0), (0.3, 10.4, 4.0), "#EBDDF2")
obj("placa", "boxb", (-1.0, 4.92, 3.1), (4.0, 0.1, 0.8), PURPLE)
text3d("placa_t", "COSTURA", 0.5, (-1.0, 4.84, 3.5), "#FFFFFF", 0.01, rot=(math.radians(90), 0, 0))
ia_txt = text3d("ia_q", "IA ?", 4.0, (0, 0, 16.0), PURPLE, 0.3)
# mesa de costura + máquina
obj("mesa", "boxb", (-3.0, 2.4, 0.78), (1.9, 0.9, 0.07), "#B08A63")
for (lx, ly) in ((-3.85, 2.05), (-2.15, 2.05), (-3.85, 2.75), (-2.15, 2.75)): obj("pe", "boxb", (lx, ly, 0), (0.07, 0.07, 0.78), "#8A6A48")
maq = empty("maquina", (-3.0, 2.4, 0.85))
obj("m_base", "boxb", (0, 0, 0), (0.9, 0.36, 0.14), "#FFFFFF", parent=maq)
obj("m_col", "boxb", (0.33, 0, 0.14), (0.2, 0.3, 0.45), "#FFFFFF", parent=maq)
obj("m_braco", "boxb", (0.0, 0, 0.5), (0.86, 0.26, 0.16), "#FFFFFF", parent=maq)
obj("m_faixa", "boxb", (0.0, -0.135, 0.52), (0.86, 0.01, 0.06), PURPLE, parent=maq)
obj("m_cab", "boxb", (-0.36, 0, 0.32), (0.14, 0.22, 0.2), "#FFFFFF", parent=maq)
needle = obj("agulha", "cyl", (-0.36, 0, 0.28), (0.012, 0.012, 0.16), "#9AA0A8", parent=maq)
obj("m_volante", "cyl24", (0.46, 0, 0.55), (0.12, 0.12, 0.05), "#3A3F47", rot=(0, math.pi / 2, 0), parent=maq)
fabric = obj("tecido", "boxb", (-3.2, 2.3, 0.85), (0.9, 0.6, 0.02), "#2F7CF6")
for i, c in enumerate(["#F2B33D", "#E5484D", "#25A55F", PURPLE]):
    obj("carretel", "cyl", (-3.9 + i * 0.18, 2.75, 0.95), (0.06, 0.06, 0.18), c)
# balcão
obj("balcao", "boxb", (2.5, -0.8, 0), (3.2, 0.9, 1.0), "#C9A97A")
obj("balcao_t", "boxb", (2.5, -0.8, 1.0), (3.4, 1.05, 0.07), "#F6F0E6")
notebook = obj("caderno", "boxb", (1.6, -0.75, 1.07), (0.5, 0.36, 0.05), "#E5484D")
pencil = obj("lapis", "boxb", (1.75, -0.7, 1.13), (0.04, 0.32, 0.03), "#F2B33D", rot=(0, 0, 0.6))
PANTS = []
for i, c in enumerate(["#3B4A63", "#E86A8C", "#25A55F"]):
    p = obj("roupa", "boxb", (0, 0, -50), (0.55, 0.4, 0.06), c)
    PANTS.append(p)
# celular grande do app (sobe no balcão)
appph = empty("app_phone", (3.25, -0.55, 1.07))
obj("ap_body", "boxb", (0, 0, 0), (0.52, 0.06, 0.98), "#1E1E22", parent=appph)
app_scr = obj("ap_scr", "boxb", (0, -0.035, 0.05), (0.45, 0.01, 0.86), "#BFD9F6", parent=appph, mat=mvb.MG)
obj("ap_stand", "boxb", (0, 0.12, 0), (0.3, 0.2, 0.05), "#3A3F47", parent=appph)
appph.rotation_euler = (math.radians(-12), 0, 0)
# arara (fila) + prateleira PRONTO
obj("arara_p1", "cyl", (0.6, 4.2, 1.0), (0.04, 0.04, 2.0), "#9AA0A8"); obj("arara_p2", "cyl", (4.6, 4.2, 1.0), (0.04, 0.04, 2.0), "#9AA0A8")
obj("arara_b", "cyl", (2.6, 4.2, 2.0), (0.03, 0.03, 4.0), "#9AA0A8", rot=(0, math.pi / 2, 0))
QUEUE = []
QC = ["#3B4A63", "#E86A8C", "#25A55F", "#F2B33D"]
for i, c in enumerate(QC):
    g = empty(f"fila{i}")
    obj("cab", "boxb", (0, 0, -0.08), (0.04, 0.04, 0.16), "#9AA0A8", parent=g)
    obj("ombro", "boxb", (0, 0, -0.22), (0.62, 0.14, 0.08), c, parent=g)
    obj("corpo", "boxb", (0, 0, -0.92), (0.5, 0.12, 0.72), c, parent=g)
    obj("tag", "boxb", (0.18, -0.08, -0.5), (0.16, 0.02, 0.22), "#FFFFFF", parent=g)
    QUEUE.append(g)
obj("pronto_m", "boxb", (5.4, 3.0, 0), (1.4, 1.2, 1.1), "#25A55F")
obj("pronto_s", "boxb", (5.4, 2.38, 1.35), (1.3, 0.06, 0.45), "#FFFFFF")
text3d("pronto_t", "PRONTO", 0.25, (5.4, 2.34, 1.55), "#25A55F", 0.01, rot=(math.radians(90), 0, 0))
done_box = obj("pronto_cx", "boxb", (5.4, 3.0, 1.1), (0.55, 0.4, 0.2), "#3B4A63")
# porta
obj("porta", "boxb", (-6.5, -3.0, 0), (0.12, 1.2, 2.5), "#FFFFFF")

TIT = titulos3d.Placas([
    (3.25, 5.0, "1", "ETAPA 1 · PROFISSÃO", "Costureira", "a profissão escolhida de hoje", "#7B5BD6"),
    (5.72, 7.6, "2", "ETAPA 2 · PROBLEMA", "O balcão", "preço de cabeça, caderno, pedido esquecido", "#E5484D"),
    (15.64, 17.2, "3", "ETAPA 3 · SOLUÇÃO", "App simples", "foto da peça + ajuste = preço na hora", "#2F7CF6"),
    (23.56, 25.0, "4", "ETAPA 4 · ORGANIZAÇÃO", "Fila com data", "cada pedido com dia de entrega", "#F08A3C"),
    (29.12, 30.9, "5", "ETAPA 5 · RESULTADO", "Ela só costura", "a mensagem de pronto sai sozinha", "#25A55F"),
    (31.1, 32.8, "", "CONCLUSÃO", "IA no balcão", "você no que sabe fazer de melhor", "#7B5BD6"),
])
# pessoas
cost = Person("costureira", shirt=PURPLE, apron="#F6E7D0", hair="#2E2420")
clients = [Person("cl0", shirt="#F08A3C"), Person("cl1", shirt="#3DAA5A"), Person("cl2", shirt="#5FB7C9")]
qmarks = [text3d(f"q{i}", "?", 0.5, (0, 0, -50), "#2B2F36", 0.05) for i in range(4)]
nuvem = empty("nuvem")
for (dx, dz, r) in ((0, 0, 0.32), (0.3, 0.05, 0.24), (-0.3, 0.03, 0.24), (0.1, 0.25, 0.22)):
    obj("nv", "sph", (dx, 0, dz), (r, r * 0.6, r), "#FFFFFF", parent=nuvem)
nuvem_t = text3d("nv_t", "R$ ?", 0.22, (0, -0.25, 0.06), "#2B2F36", 0.02, parent=nuvem, rot=(math.radians(90), 0, 0))
papers = [obj("nota", "boxb", (0, 0, -50), (0.24, 0.3, 0.01), R.choice(["#FFFFFF", "#F6E7D0", "#FFF3B0"])) for _ in range(12)]
PAP = [(p, R.uniform(-1.6, 1.6), R.uniform(-1.4, 0.6), R.uniform(1.0, 2.2), R.uniform(0, 6)) for p in papers]
hearts = [obj(f"h{i}", "heart", (0, 0, -50), (0.3, 0.3, 0.3), "#E5484D") for i in range(3)]

MACH = (-3.0, 3.3); DESK = (2.5, 0.1)
COST_PATH = [(0.0, MACH), (T["cliente"] + 0.3, MACH), (T["cliente"] + 1.3, DESK), (T["fila"] - 0.2, DESK), (T["fila"] + 1.0, MACH)]
CL_PATHS = [
    [(0.0, (-6.0, -3.0)), (T["cliente"] - 0.4, (-6.0, -3.0)), (T["cliente"] + 0.8, (2.5, -2.0)), (T["fila"] + 0.2, (2.5, -2.0)), (T["fila"] + 1.6, (-6.0, -3.0))],
    [(0.0, (-6.0, -3.0)), (T["esquece"] - 0.5, (-6.0, -3.0)), (T["esquece"] + 0.6, (1.3, -2.5)), (T["app"] + 0.2, (1.3, -2.5)), (T["app"] + 1.6, (-6.0, -3.0))],
    [(0.0, (-6.0, -3.0)), (T["esquece"] - 0.2, (-6.0, -3.0)), (T["esquece"] + 0.8, (3.8, -2.6)), (T["app"] + 0.3, (3.8, -2.6)), (T["app"] + 1.5, (-6.0, -3.0))],
]
CL_IN = [T["cliente"] - 0.4, T["esquece"] - 0.5, T["esquece"] - 0.2]

# ---------------------------------------------------------------- câmera
mvb.CK[:] = [
    (0.0, (-22.0, -40.0, 34.0), (0.0, 0.0, 3.5), 34, mvb.Z),
    (2.4, (18.0, -33.0, 20.0), (0.0, -1.0, 2.5), 32, mvb.Z),
    (4.4, (3.0, -17.0, 3.2), (0.0, 0.0, 2.2), 30, mvb.Z),
    (5.6, (-1.4, -2.6, 2.6), (-3.0, 2.5, 1.2), 30, mvb.Z),
    (7.6, (-1.2, -2.4, 2.5), (-3.0, 2.5, 1.2), 30, mvb.Z),
    (8.6, (6.6, -6.2, 3.4), (2.2, -0.3, 1.3), 30, mvb.Z),
    (15.3, (6.3, -6.5, 3.3), (2.2, -0.3, 1.3), 30, mvb.Z),
    (16.4, (5.0, -3.0, 2.4), (3.0, -0.4, 1.4), 30, mvb.Z),
    (23.2, (5.2, -2.8, 2.35), (3.0, -0.4, 1.4), 30, mvb.Z),
    (24.2, (2.4, -2.8, 3.0), (3.0, 3.8, 1.5), 30, mvb.Z),
    (28.8, (2.8, -2.6, 2.9), (3.4, 3.6, 1.4), 30, mvb.Z),
    (29.6, (-1.4, -2.6, 2.6), (-3.0, 2.5, 1.2), 30, mvb.Z),
    (32.6, (-1.1, -2.3, 2.5), (-3.0, 2.5, 1.2), 30, mvb.Z),
    (34.8, (10.0, -32.0, 20.0), (0.0, 0.0, 3.0), 30, mvb.Z),
    (DUR, (-16.0, -50.0, 36.0), (0.0, 0.0, 2.0), 30, mvb.Z),
]

def apply(t):
    # "IA ?" flutuando
    k = win(t, T["ia"], T["costureira"] + 0.3, 0.4, 0.4)
    ia_txt.hide_render = k <= 0.01; ia_txt.scale = (max(k, 0.001),) * 3; ia_txt.location.z = 16.0 + 0.4 * math.sin(t * 2); cidade.animate(t); TIT.update(t)
    mvb.face_cam(ia_txt)
    # máquina costurando
    x, y, yaw, sw = walk_pose(COST_PATH, t)
    at_machine = math.hypot(x - MACH[0], y - MACH[1]) < 0.05
    sewing = at_machine and (t < T["cliente"] + 0.3 or t > T["continua"])
    needle.location.z = 0.28 - (0.05 * abs(math.sin(t * 25)) if sewing else 0)
    fabric.location.x = -3.2 + (0.25 * math.sin(t * 0.8) if sewing else 0)
    if yaw is None: yaw = math.pi
    cost.pose(x, y, 0.06, yaw, sw, 1.0, armL=(0.95 + 0.05 * math.sin(t * 9) if sewing else None),
              armR=(0.95 + 0.05 * math.sin(t * 9 + 1) if sewing else (1.3 if T["anota"] - 0.1 < t < T["esquece"] else None)))
    # clientes
    for i, (p, path) in enumerate(zip(clients, CL_PATHS)):
        cx, cy, cyaw, csw = walk_pose(path, t)
        vis = CL_IN[i] <= t <= path[-1][0] + 0.3
        s = 1.0 - ease((t - path[-1][0]) / 0.3) if t > path[-1][0] else 1.0
        if cyaw is None: cyaw = 0.0
        p.pose(cx, cy, 0.06, cyaw, csw, s if vis else 0.0, armR=(1.1 if i == 0 and T["cliente"] + 0.8 < t < T["foto"] else None))
        q = qmarks[i]
        t0 = T["pergunta"] if i == 0 else T["esquece"] + 0.6
        qk = win(t, t0, T["app"], 0.35, 0.3)
        q.hide_render = qk <= 0.01; q.location = (cx, cy, 2.25 + 0.06 * math.sin(t * 4 + i)); q.scale = (max(qk, 0.001),) * 3; mvb.face_cam(q)
    # "?" da costureira esquecendo
    q = qmarks[3]; qk = win(t, T["esquece"] + 0.3, T["app"], 0.35, 0.3)
    q.hide_render = qk <= 0.01; q.location = (x, y, 2.25 + 0.06 * math.sin(t * 5)); q.scale = (max(qk, 0.001),) * 3; mvb.face_cam(q)
    # nuvem de conta
    nk = win(t, T["calcula"], T["anota"], 0.35, 0.3)
    nuvem.location = (x + 0.45, y, 2.35 + 0.05 * math.sin(t * 3)); nuvem.scale = (max(nk, 0.001),) * 3; mvb.face_cam(nuvem)
    for c in nuvem.children: c.hide_render = nk <= 0.01
    pencil.rotation_euler = (0, 0, 0.6 + (0.25 * math.sin(t * 22) if T["anota"] < t < T["esquece"] else 0))
    # roupas no balcão (pedidos) → bagunça
    for i, p in enumerate(PANTS):
        t0 = [T["cliente"] + 0.9, T["esquece"] + 0.7, T["esquece"] + 0.9][i]
        k = eback((t - t0) / 0.3)
        p.hide_render = k <= 0.01 or t > T["fila"] + 0.4
        p.location = (2.3 + i * 0.5, -0.9 + 0.1 * i, 1.08 + i * 0.03); p.rotation_euler = (0, 0, 0.3 * i - 0.2)
        p.scale = (0.55 * max(k, .001), 0.4 * max(k, .001), 0.06)
    for (p, dx, dy, vz, ph) in PAP:
        u = t - T["esquece"]
        if 0 <= u <= 1.7:
            p.hide_render = False
            z = 1.1 + vz * u - 2.2 * u * u
            p.location = (2.0 + dx * u, -0.8 + dy * u, max(0.08, z)); p.rotation_euler = (u * 5 + ph, u * 3, ph)
        elif u > 1.7 and t < T["app"] + 0.2:
            p.hide_render = False
        else: p.hide_render = True
    # app
    ak = eback((t - (T["app"] + 0.3)) / 0.5)
    appph.scale = (max(ak, 0.001),) * 3
    for c in appph.children: c.hide_render = ak <= 0.01
    fl = max(0.0, 1 - abs(t - T["foto"]) / 0.15)
    app_scr.color = hexc("#FFFFFF") if fl > 0.3 else hexc("#BFD9F6")
    # fila na arara
    for i, g in enumerate(QUEUE):
        t0 = T["fila"] + 0.2 + i * 0.25
        k = ease((t - t0) / 0.6)
        x0 = 6.5; x1 = 1.1 + i * 0.95
        done = i == 0 and t > T["pronto"]
        if done:
            u = ease((t - T["pronto"]) / 0.6); g.location = (lerp(x1, 5.4, u), lerp(4.2, 3.0, u), lerp(2.0, 1.9, u) + 0.6 * 4 * u * (1 - u))
            g.scale = (max(1 - u, 0.001),) * 3
        else:
            g.location = (lerp(x0, x1, k), 4.2, 2.0); g.scale = (max(min(1, k * 3), 0.001),) * 3
        for c in g.children: c.hide_render = k <= 0.01 or (done and ease((t - T["pronto"]) / 0.6) > 0.98)
        g.rotation_euler = (0, 0, 0.08 * math.sin(t * 2 + i))
    dk = eback((t - (T["pronto"] + 0.5)) / 0.35)
    done_box.hide_render = dk <= 0.01; done_box.scale = (0.55 * max(dk, .001), 0.4 * max(dk, .001), 0.2 * max(dk, .001))
    # corações (continua costurando)
    for i, h in enumerate(hearts):
        h0 = T["continua"] + 0.6 + i * 0.35
        k = win(t, h0, h0 + 2.0, 0.35, 0.4)
        h.hide_render = k <= 0.01
        h.location = (MACH[0] - 0.3 + 0.35 * i, MACH[1], 2.3 + 0.25 * i); h.scale = (0.26 * k,) * 3; mvb.face_cam(h)

ANCH = dict(cost=lambda t: (lambda s: (s[0], s[1], 2.0))(walk_pose(COST_PATH, t)), maquina=(-3.0, 2.4, 1.6), balcao=(2.5, -1.3, 1.2),
            cl0=lambda t: (lambda s: (s[0], s[1], 2.0))(walk_pose(CL_PATHS[0], t)), caderno=(1.6, -0.75, 1.15),
            app=(3.25, -0.6, 1.9), arara=(2.6, 4.2, 2.2), fila0=(1.1, 4.2, 1.6), fila3=(3.95, 4.2, 1.6), pronto=(5.4, 2.4, 1.9))
mvb.run(apply, ANCH, dict(T=T))
