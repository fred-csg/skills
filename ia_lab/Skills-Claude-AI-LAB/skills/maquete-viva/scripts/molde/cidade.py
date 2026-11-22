# Cidade-maquete premium + prédio-herói aberto (estilo "architectural microcosm").
# O 1º andar do prédio fica em z = 0..4.6 (onde mora a cena do ateliê). A rua fica em ZS = -4.6.
import bpy, bmesh, math
import mvb
from mvb import obj, empty, text3d, hexc, R, place, Person

A = mvb.ASSETS
def K(pack, name): return f"{A}/{pack}/x/Models/GLB format/{name}.glb"
ZS = -4.6
PURPLE = "#7B5BD6"; PURPLE_D = "#6447BE"

def rbox(name, x0, x1, y0, y1, z0, z1, color, bev=0.0, seg=4, mat=None):
    """caixa com tamanho real e quinas arredondadas de verdade (bevel na malha)."""
    me = bpy.data.meshes.new(name); bm = bmesh.new()
    bmesh.ops.create_cube(bm, size=1.0)
    for v in bm.verts:
        v.co.x = x0 if v.co.x < 0 else x1; v.co.y = y0 if v.co.y < 0 else y1; v.co.z = z0 if v.co.z < 0 else z1
    if bev > 0:
        bmesh.ops.bevel(bm, geom=list(bm.edges), offset=bev, segments=seg, profile=0.5, affect="EDGES")
    bm.to_mesh(me); bm.free()
    me.materials.append(mat or mvb.M)
    try:
        me.shade_smooth(); me.set_sharp_from_angle(angle=math.radians(35))
    except Exception: pass
    o = bpy.data.objects.new(name, me); mvb.COLL.objects.link(o); o.color = hexc(color)
    return o

LEAF = None
def leaf_mat():
    """folhagem: cor do objeto com variação + relevo de folhas."""
    global LEAF
    if LEAF: return LEAF
    m = bpy.data.materials.new("Mleaf"); m.use_nodes = True; nt = m.node_tree; P = nt.nodes["Principled BSDF"]
    oi = nt.nodes.new("ShaderNodeObjectInfo")
    vor = nt.nodes.new("ShaderNodeTexVoronoi"); vor.inputs["Scale"].default_value = 7.0
    nz = nt.nodes.new("ShaderNodeTexNoise"); nz.inputs["Scale"].default_value = 2.5
    mix = nt.nodes.new("ShaderNodeMix"); mix.data_type = "RGBA"; mix.blend_type = "MULTIPLY"
    ramp = nt.nodes.new("ShaderNodeValToRGB"); ramp.color_ramp.elements[0].color = (0.55, 0.62, 0.45, 1); ramp.color_ramp.elements[1].color = (1.25, 1.2, 0.85, 1)
    nt.links.new(nz.outputs["Fac"], ramp.inputs["Fac"])
    nt.links.new(oi.outputs["Color"], mix.inputs[6]); nt.links.new(ramp.outputs["Color"], mix.inputs[7]); mix.inputs[0].default_value = 0.9
    nt.links.new(mix.outputs[2], P.inputs["Base Color"])
    bump = nt.nodes.new("ShaderNodeBump"); bump.inputs["Strength"].default_value = 0.55; bump.inputs["Distance"].default_value = 0.08
    nt.links.new(vor.outputs["Distance"], bump.inputs["Height"]); nt.links.new(bump.outputs["Normal"], P.inputs["Normal"])
    P.inputs["Roughness"].default_value = 0.7
    try: P.inputs["Subsurface Weight"].default_value = 0.08
    except Exception: pass
    LEAF = m; return m

def fluffy_tree(x, y, z, s=1.0):
    obj("tronco", "cyl", (x, y, z + 1.0 * s), (0.18 * s, 0.18 * s, 2.0 * s), "#7A5A3C")
    S = mvb.random.Random(int(x * 13 + y * 7))
    c = S.choice(["#3F9A36", "#4FAE3E", "#2E8A33", "#5DBB45", "#3C9E52"])
    lm = leaf_mat()
    for k in range(11):
        if k == 0: dx = dy = 0; dz = 0.45; rr = 1.15
        else:
            a = k / 10 * 6.28 + S.uniform(-0.3, 0.3); r = S.uniform(0.6, 0.9)
            dx, dy = r * math.cos(a), r * math.sin(a); dz = S.uniform(-0.15, 0.55); rr = S.uniform(0.6, 0.85)
        obj("copa", "sph", (x + dx * s, y + dy * s, z + 2.55 * s + dz * s), (rr * s, rr * s, rr * s * 0.92), c, mat=lm)

def build(t_ia_hide=None):
    # ---- chão: asfalto + quarteirões elevados
    obj("asfalto", "boxb", (0, 0, ZS - 0.2), (600, 600, 0.2), "#6B6E75")
    BX, BY = 31.0, 29.0   # passo dos quarteirões
    for i in range(-3, 4):
        for j in range(-3, 4):
            cx, cy = i * BX, j * BY
            rbox("quarteirao", cx - 11, cx + 11, cy - 10, cy + 10, ZS, ZS + 0.18, "#D9D3C9", bev=0.08, seg=2)
            # faixas de pedestre em cada esquina (rua horizontal)
    for i in range(-3, 4):  # linhas tracejadas nas ruas
        x = i * BX + BX / 2
        for k in range(-40, 41, 3): obj("faixa_v", "boxb", (x, k * 2.5, ZS + 0.005), (0.18, 1.6, 0.01), "#F2F0EA")
    for j in range(-3, 4):
        y = j * BY + BY / 2
        for k in range(-40, 41, 3): obj("faixa_h", "boxb", (k * 2.5, y, ZS + 0.005), (1.6, 0.18, 0.01), "#F2F0EA")
    for (cx, cy) in ((15.5, -14.5), (-15.5, -14.5), (15.5, 14.5), (-15.5, 14.5)):   # zebras em volta do herói
        for k in range(7):
            obj("zebra", "boxb", (cx - 3.0 + k * 1.0, cy - 10.6 if cy < 0 else cy + 10.6, ZS + 0.006), (0.55, 3.2, 0.01), "#F7F6F2")
            obj("zebra", "boxb", (cx - 10.6 if cx > 0 else cx + 10.6, cy - 3.0 + k * 1.0, ZS + 0.006), (3.2, 0.55, 0.01), "#F7F6F2")
    # ---- outros quarteirões com prédios prontos (Kenney, escala ~9)
    tall = ["building-skyscraper-a", "building-skyscraper-b", "building-skyscraper-c", "building-skyscraper-d", "building-skyscraper-e"]
    mid = ["building-a", "building-b", "building-c", "building-d", "building-e", "building-f", "building-g", "building-h",
           "building-i", "building-j", "building-k", "building-l", "building-m", "building-n"]
    sub = ["building-type-a", "building-type-b", "building-type-c", "building-type-d", "building-type-e", "building-type-f",
           "building-type-g", "building-type-h", "building-type-i", "building-type-j", "building-type-k", "building-type-l"]
    S = mvb.random.Random(21)
    for i in range(-3, 4):
        for j in range(-3, 4):
            if i == 0 and j == 0: continue
            cx, cy = i * BX, j * BY
            for (dx, dy) in ((-5.5, -5), (5.5, -5), (-5.5, 5), (5.5, 5)):
                x, y = cx + dx, cy + dy
                if j <= -1 and abs(i) <= 1:      # quarteirões na frente da câmera: baixos
                    if S.random() < 0.45: fluffy_tree(x, y, ZS + 0.18, S.uniform(1.0, 1.3)); continue
                    place(K("suburban", S.choice(sub)), (x, y, ZS + 0.18), S.choice([0, math.pi / 2, math.pi, -math.pi / 2]), 7.5)
                elif j >= 1 and abs(i) <= 2:     # fundo: altos (skyline)
                    place(K("commercial", S.choice(tall if S.random() < 0.55 else mid)), (x, y, ZS + 0.18), S.choice([0, math.pi / 2, math.pi, -math.pi / 2]), 8.5)
                else:
                    place(K("commercial", S.choice(mid)), (x, y, ZS + 0.18), S.choice([0, math.pi / 2, math.pi, -math.pi / 2]), 8.5)
    # ---- quarteirão do herói: praça, árvores, postes, guarda-sóis, canteiros
    for (x, y) in ((-9.2, -8.4), (9.0, -8.6), (-9.6, 7.8), (9.4, 8.0), (-9.8, 0.0)):
        fluffy_tree(x, y, ZS + 0.18, 0.9)
    for x in (-10.5, -3.5, 3.5, 10.5):
        place(K("roads", "light-square"), (x, -10.2, ZS + 0.18), math.pi, 8.0)
    place(K("roads", "traffic-light"), (10.6, -9.8, ZS + 0.18), math.pi * 0.75, 8.0)
    place(K("roads", "traffic-light"), (-10.6, -9.8, ZS + 0.18), -math.pi * 0.75, 8.0)
    for x in (-6.0, 6.0):
        place(K("commercial", "detail-parasol-a"), (x, -8.0, ZS + 0.18), 0, 8.0)
    for x in (-1.5, 1.5):
        place(K("suburban", "planter"), (x, -7.6, ZS + 0.18), 0, 6.0)
    for k in range(13):  # gradil da calçada
        obj("grade", "boxb", (-9 + k * 1.5, -9.6, ZS + 0.18), (0.06, 0.06, 0.9), "#3A3F47")
    obj("grade_t", "boxb", (0, -9.6, ZS + 1.05), (18.2, 0.06, 0.06), "#3A3F47")
    # ---- prédio-herói (roxo, cantos arredondados, aberto na frente e na lateral direita)
    X0, X1, Y0, Y1 = -7.4, 7.4, -6.0, 5.65
    # térreo: loja com vitrine
    rbox("terreo", X0, X1, Y0 + 0.4, Y1, ZS + 0.18, -0.8, PURPLE, bev=0.5)
    obj("vitrine", "boxb", (0.0, Y0 + 0.35, ZS + 0.5), (11.0, 0.08, 2.6), (0.62, 0.78, 0.88, 0.55), mat=mvb.MGLASS)
    obj("vit_in", "boxb", (0.0, Y0 + 0.6, ZS + 0.18), (11.6, 0.1, 3.4), "#F3E6C8", mat=mvb.MG)
    for x in (-5.5, -2.75, 0.0, 2.75, 5.5):
        obj("caixilho", "boxb", (x, Y0 + 0.3, ZS + 0.5), (0.12, 0.12, 2.6), "#2B2F36")
    obj("porta_rua", "boxb", (5.9, Y0 + 0.28, ZS + 0.18), (1.2, 0.1, 2.5), "#2B2F36")
    rbox("placa_rua", -4.2, 4.2, Y0 - 0.05, Y0 + 0.4, ZS + 3.25, ZS + 4.15, "#2B2F36", bev=0.15)
    text3d("placa_rua_t", "ATELIÊ", 0.75, (0, Y0 - 0.1, ZS + 3.7), "#FFFFFF", 0.03, rot=(math.radians(90), 0, 0))
    for x in (-5.2, 5.2):
        place(K("commercial", "detail-awning-wide"), (x, Y0 + 0.4, ZS + 3.0), math.pi, (7.5, 6.0, 6.0))
    # lajes (com borda arredondada saliente, como o prédio da Nike)
    rbox("laje1", X0 - 0.2, X1 + 0.2, Y0 - 0.2, Y1 + 0.2, -0.8, 0.0, PURPLE, bev=0.35)
    rbox("laje2", X0 - 0.2, X1 + 0.2, Y0 - 0.2, Y1 + 0.2, 4.4, 5.3, PURPLE, bev=0.35)
    rbox("laje3", X0 - 0.2, X1 + 0.2, Y0 - 0.2, Y1 + 0.2, 9.6, 10.5, PURPLE, bev=0.35)
    # paredes que ficam (fundo + esquerda) e pilares
    for z0, z1 in ((0.0, 4.4), (5.3, 9.6)):
        rbox("parede_f", X0, X1, 5.25, Y1, z0, z1, PURPLE)
        rbox("parede_e", X0, -6.75, Y0, Y1, z0, z1, PURPLE)
        rbox("pilar", X0, -6.2, Y0, -4.9, z0, z1, PURPLE, bev=0.3)
        rbox("pilar2", 6.2, X1, 4.3, Y1, z0, z1, PURPLE, bev=0.3)
    # guarda-corpo nas bordas abertas
    for (z, ) in ((0.0,), (5.3,)):
        for k in range(14): obj("gc", "cyl", (-5.8 + k * 0.98, Y0 - 0.1, z + 0.5), (0.03, 0.03, 1.0), "#C9CED6")
        for k in range(10): obj("gc", "cyl", (X1 + 0.05, -5.6 + k * 0.98, z + 0.5), (0.03, 0.03, 1.0), "#C9CED6")
        obj("gc_t", "cyl", (0.2, Y0 - 0.1, z + 1.0), (0.04, 0.04, 13.2), "#C9CED6", rot=(0, math.pi / 2, 0))
        obj("gc_t", "cyl", (X1 + 0.05, -1.0, z + 1.0), (0.04, 0.04, 9.6), "#C9CED6", rot=(math.pi / 2, 0, 0))
    # 2º andar: estoque de tecidos
    obj("piso2", "boxb", (0, 0, 5.3), (13.6, 10.6, 0.04), "#E6D8C0")
    for r in range(3):
        y = 4.6 - r * 0.0
        rbox("estante", -6.0 + r * 4.2, -3.2 + r * 4.2, 4.3, 5.1, 5.3, 8.2, "#F4EEE4", bev=0.05)
        for lv in range(3):
            for k in range(4):
                c = S.choice(["#E5484D", "#2F7CF6", "#F2B33D", "#25A55F", "#E86A8C", PURPLE, "#5FB7C9"])
                obj("rolo", "cyl", (-5.6 + r * 4.2 + k * 0.6, 4.5, 5.75 + lv * 0.95), (0.25, 0.25, 0.7), c, rot=(math.pi / 2, 0, 0))
    for k, x in enumerate((-3.0, 0.5, 3.5)):
        obj("manequim", "cyl", (x, 1.0, 6.3), (0.05, 0.05, 2.0), "#9AA0A8")
        obj("manequim_c", "sph", (x, 1.0, 7.3), (0.32, 0.22, 0.45), ["#F6E7D0", "#E86A8C", "#2F7CF6"][k])
    rbox("mesa2", -1.5, 2.5, -2.5, -0.8, 5.3, 6.15, "#B08A63", bev=0.05)
    # telhado: letreiro deitado + ar-condicionado + guarda-corpo
    text3d("teto_t", "ATELIÊ", 2.4, (0, -0.4, 10.52), "#FFFFFF", 0.06)
    for (x, y) in ((-5.0, 3.6), (-3.2, 3.6), (5.2, -3.8)):
        rbox("ar", x - 0.7, x + 0.7, y - 0.5, y + 0.5, 10.5, 11.3, "#C9CED6", bev=0.1)
    for k in range(16): obj("gr_t", "cyl", (X0 + 0.2 + k * 0.95, Y0 + 0.0, 11.0), (0.03, 0.03, 1.0), "#C9CED6")
    obj("gr_tt", "cyl", (0, Y0 + 0.0, 11.5), (0.04, 0.04, 14.6), "#C9CED6", rot=(0, math.pi / 2, 0))
    # luzes internas (quentes) nos andares
    for z in (4.2, 9.4):
        ld = bpy.data.lights.new("luz_in", "AREA"); ld.energy = 800 if z < 5 else 450; ld.size = 10; ld.size_y = 7; ld.shape = "RECTANGLE"
        ld.color = hexc("#FFE6C7")[:3]
        lo = bpy.data.objects.new("luz_in", ld); mvb.COLL.objects.link(lo); lo.location = (0, 0.5, z)

# ---- trânsito e pedestres na rua
CARS = []; WALK = []
def traffic():
    S = mvb.random.Random(8)
    kinds = ["sedan", "taxi", "van", "suv", "hatchback-sports", "delivery", "sedan-sports", "police"]
    lanes = [((-80, 80), -12.3, 1), ((-80, 80), -16.7, -1)]           # rua da frente (y = -14.5)
    lanes += [((-80, 80), 16.7, 1), ((-80, 80), 12.3, -1)]             # rua de trás
    vlanes = [(13.3, 1), (17.7, -1), (-17.7, 1), (-13.3, -1)]           # ruas laterais (x)
    for (_, y, d) in lanes:
        for k in range(4):
            o = place(K("cars", S.choice(kinds)), (0, y, ZS), -d * math.pi / 2, 1.75)
            CARS.append((o, "x", y, d, S.uniform(-80, 80), S.uniform(5, 8)))
    for (x, d) in vlanes:
        for k in range(3):
            o = place(K("cars", S.choice(kinds)), (x, 0, ZS), (0 if d > 0 else math.pi), 1.75)
            CARS.append((o, "y", x, d, S.uniform(-80, 80), S.uniform(5, 8)))
    # estacionados
    for x in (-12.0, 12.5):
        place(K("cars", S.choice(kinds)), (x, -11.0, ZS), math.pi / 2, 1.75)
    for i in range(18):
        p = Person(f"pedestre{i}", scale=1.0)
        side = S.choice([-10.7, 10.7]); along = S.choice(["x", "y"])
        WALK.append((p, along, side, S.choice([-1, 1]), S.uniform(-11, 11), S.uniform(0.9, 1.3)))

def animate(t):
    for (o, ax, c, d, x0, v) in CARS:
        u = (x0 + d * v * t + 80) % 160 - 80
        o.location = (u, c, ZS) if ax == "x" else (c, u, ZS)
    for (p, along, side, d, x0, v) in WALK:
        u = (x0 + d * v * t + 11) % 22 - 11
        x, y = (u, side) if along == "x" else (side, u)
        yaw = (-d * math.pi / 2) if along == "x" else (0 if d > 0 else math.pi)
        p.pose(x, y, ZS + 0.18, yaw, math.sin(t * v * 5.4 + x0), 1.0)
