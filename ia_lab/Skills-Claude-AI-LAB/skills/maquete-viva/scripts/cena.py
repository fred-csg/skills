# Cena 3D "A rua virou o feed" — estilo low-poly claro (referência raiox).
# Uso: blender -b --factory-startup --python cena.py -- <out_dir> <res%> <frames: "a-b" | "a,b,c" | "a-b:step"> [shard i/n]
import bpy, bmesh, math, random, json, sys, os
from mathutils import Vector, Matrix
from bpy_extras.object_utils import world_to_camera_view

argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
OUT = argv[0] if len(argv) > 0 else os.path.join(os.environ.get("TEMP", "."), "cena_out")
RES = int(argv[1]) if len(argv) > 1 else 50
FRAMES_ARG = argv[2] if len(argv) > 2 else "0"
SHARD = argv[3] if len(argv) > 3 else "0/1"
os.makedirs(OUT, exist_ok=True)

FPS = 30
DUR = 72.6
NF = int(DUR * FPS)

def tf(t): return int(round(t * FPS))

# ---------------------------------------------------------------- timeline (s), alinhada à locução
T = dict(
    vitrine_open=6.70, reveal=8.50, panf_title=15.62, pan_on=17.0, pan_off=30.4,
    follow_cam=21.7, bin_cam=25.68, feed=31.14, cards=33.15, scroll=34.9, perfil=38.9,
    ad=41.18, coins=43.6, ad_fire=43.9, ad_stop=49.96, org=52.6, post=56.42, end=64.98,
)
PLACA_T = [56.42, 57.25, 57.95, 58.5, 59.15, 59.75, 60.4, 61.0, 61.7, 62.35, 62.8, 63.2, 63.55, 63.85, 64.1]
BURST = (65.0, 66.2)  # "anúncio acelera" — rajada final

# ---------------------------------------------------------------- utilidades
def ease(a):  # smootherstep
    a = max(0.0, min(1.0, a)); return a * a * a * (a * (a * 6 - 15) + 10)
def eout(a):
    a = max(0.0, min(1.0, a)); return 1 - (1 - a) ** 3
def eback(a):
    a = max(0.0, min(1.0, a)); c1 = 1.70158; c3 = c1 + 1
    return 1 + c3 * (a - 1) ** 3 + c1 * (a - 1) ** 2
def lerp(a, b, k): return a + (b - a) * k
def vlerp(a, b, k): return tuple(lerp(a[i], b[i], k) for i in range(len(a)))
def hexc(h, a=1.0):
    h = h.lstrip("#"); r, g, b = (int(h[i:i + 2], 16) / 255 for i in (0, 2, 4))
    lin = lambda c: c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4
    return (lin(r), lin(g), lin(b), a)

R = random.Random(7)

# ---------------------------------------------------------------- cena limpa
for o in list(bpy.data.objects): bpy.data.objects.remove(o, do_unlink=True)
sc = bpy.context.scene
sc.render.engine = "BLENDER_EEVEE"
sc.render.resolution_x, sc.render.resolution_y = 1080, 1920
sc.render.resolution_percentage = RES
sc.render.fps = FPS
sc.render.image_settings.file_format = "PNG"
sc.render.film_transparent = False
ee = sc.eevee
ee.taa_render_samples = 24
for k, v in dict(use_shadows=True, use_raytracing=True, use_fast_gi=True, shadow_ray_count=2, shadow_step_count=8).items():
    try: setattr(ee, k, v)
    except Exception: pass
for vt in ("Standard", "AgX"):
    try: sc.view_settings.view_transform = vt; break
    except Exception: pass
try: sc.view_settings.look = "None"
except Exception: pass
sc.view_settings.exposure = 0.0

world = bpy.data.worlds.new("W"); sc.world = world; world.use_nodes = True
bg = world.node_tree.nodes["Background"]
bg.inputs[0].default_value = hexc("#F6F1E8"); bg.inputs[1].default_value = 0.72

sun_d = bpy.data.lights.new("sun", "SUN"); sun_d.energy = 3.4; sun_d.angle = math.radians(14)
sun_d.color = hexc("#FFF6EA")[:3]
sun = bpy.data.objects.new("sun", sun_d); sc.collection.objects.link(sun)
sun.rotation_euler = (math.radians(48), math.radians(-14), math.radians(-30))

# material único guiado por obj.color (cor + alpha)
def make_mat(name, rough=0.85, emit=0.0):
    m = bpy.data.materials.new(name); m.use_nodes = True
    nt = m.node_tree; P = nt.nodes["Principled BSDF"]
    oi = nt.nodes.new("ShaderNodeObjectInfo")
    nt.links.new(oi.outputs["Color"], P.inputs["Base Color"])
    nt.links.new(oi.outputs["Alpha"], P.inputs["Alpha"])
    P.inputs["Roughness"].default_value = rough
    if "Specular IOR Level" in P.inputs: P.inputs["Specular IOR Level"].default_value = 0.15
    if emit > 0:
        nt.links.new(oi.outputs["Color"], P.inputs["Emission Color"])
        P.inputs["Emission Strength"].default_value = emit
    try: m.surface_render_method = "DITHERED"
    except Exception: pass
    return m
M = make_mat("M")
MG = make_mat("Mglow", 0.6, 1.4)
MGLASS = make_mat("Mglass", 0.08)

# ---------------------------------------------------------------- malhas base
def bm_mesh(name, fn, smooth=False):
    me = bpy.data.meshes.new(name); bm = bmesh.new(); fn(bm); bm.to_mesh(me); bm.free()
    me.materials.append(M)
    if smooth: me.shade_smooth()
    return me
def _cube(bm, dz):
    bmesh.ops.create_cube(bm, size=1.0)
    for v in bm.verts: v.co.z += dz
ME = dict(
    box=bm_mesh("box", lambda bm: _cube(bm, 0.0)),
    boxb=bm_mesh("boxb", lambda bm: _cube(bm, 0.5)),     # base no z=0
    boxt=bm_mesh("boxt", lambda bm: _cube(bm, -0.5)),    # topo no z=0 (pivô de membros)
    cyl=bm_mesh("cyl", lambda bm: bmesh.ops.create_cone(bm, cap_ends=True, cap_tris=False, segments=14, radius1=1, radius2=1, depth=1)),
    cyl24=bm_mesh("cyl24", lambda bm: bmesh.ops.create_cone(bm, cap_ends=True, cap_tris=False, segments=28, radius1=1, radius2=1, depth=1), True),
    sph=bm_mesh("sph", lambda bm: bmesh.ops.create_uvsphere(bm, u_segments=18, v_segments=12, radius=1), True),
    ico=bm_mesh("ico", lambda bm: bmesh.ops.create_icosphere(bm, subdivisions=1, radius=1)),
)
def _arrow(bm):
    pts = [(-0.5, -0.14), (0.12, -0.14), (0.12, -0.32), (0.5, 0), (0.12, 0.32), (0.12, 0.14), (-0.5, 0.14)]
    vs = [bm.verts.new((x, y, 0)) for x, y in pts]; f = bm.faces.new(vs)
    r = bmesh.ops.extrude_face_region(bm, geom=[f])
    for v in [e for e in r["geom"] if isinstance(e, bmesh.types.BMVert)]: v.co.z += 1
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
ME["arrow"] = bm_mesh("arrow", _arrow)

COLL = sc.collection
def obj(name, mesh, loc=(0, 0, 0), scale=(1, 1, 1), color="#FFFFFF", rot=(0, 0, 0), parent=None, mat=None):
    o = bpy.data.objects.new(name, ME[mesh] if isinstance(mesh, str) else mesh)
    COLL.objects.link(o); o.location = loc; o.scale = scale; o.rotation_euler = rot
    o.color = hexc(color) if isinstance(color, str) else color
    if parent: o.parent = parent
    if mat:
        o.material_slots[0].link = "OBJECT"; o.material_slots[0].material = mat
    return o
def empty(name, loc=(0, 0, 0), parent=None):
    e = bpy.data.objects.new(name, None); COLL.objects.link(e); e.location = loc
    if parent: e.parent = parent
    return e

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ambiente import achar_fonte
_fp = achar_fonte("segoeuib.ttf", "Poppins-Bold.ttf", "arialbd.ttf", "Arial Bold.ttf")
FONT = bpy.data.fonts.load(_fp) if _fp else bpy.data.fonts.load("<builtin>")   # sem fonte: a padrão do Blender
def text3d(name, body, size, loc, color="#222222", extrude=0.02, parent=None, rot=(0, 0, 0)):
    cu = bpy.data.curves.new(name, "FONT"); cu.body = body; cu.font = FONT; cu.size = size
    cu.extrude = extrude; cu.align_x = "CENTER"; cu.align_y = "CENTER"
    o = bpy.data.objects.new(name, cu); COLL.objects.link(o); o.location = loc; o.rotation_euler = rot
    o.data.materials.append(M); o.color = hexc(color)
    if parent: o.parent = parent
    return o

# ---------------------------------------------------------------- cidade
GROUND = "#EFE6D2"; PAVE = "#E6E3DD"; CURB = "#D3CFC6"
obj("ground", "boxb", (0, 0, -0.2), (500, 500, 0.2), GROUND)
obj("avenida", "boxb", (0, 0, 0), (200, 8.4, 0.02), PAVE)
obj("rua", "boxb", (10, 7.1, 0), (4.0, 6.0, 0.021), PAVE)
obj("beco", "boxb", (10, 11.7, 0), (28, 3.4, 0.021), PAVE)
for s in (-1, 1):
    obj(f"meio_fio{s}", "boxb", (0, s * 4.25, 0), (200, 0.14, 0.07), CURB)
# faixa de pedestre na esquina
for i in range(7):
    obj(f"faixa{i}", "boxb", (10 - 1.6 + i * 0.53, 0, 0.022), (0.3, 7.6, 0.004), "#F7F6F2")

BUILD_COLS = ["#F2F1EE", "#E9E6E0", "#DDE2E6", "#ECE5D8", "#E4E7E1", "#F0EBE3"]
GLASS = "#BCCDD9"
def building(x0, x1, y0, y1, h, face_sign, strips=True, col=None):
    w, d = x1 - x0, y1 - y0
    c = col or R.choice(BUILD_COLS)
    obj("b", "boxb", ((x0 + x1) / 2, (y0 + y1) / 2, 0), (w, d, h), c)
    obj("bt", "boxb", ((x0 + x1) / 2, (y0 + y1) / 2, h), (w + 0.12, d + 0.12, 0.18), "#D9D6CF")
    if strips and face_sign != 0:
        yf = (y0 if face_sign < 0 else y1) + face_sign * 0.03
        fl = 0
        z = 1.2
        while z + 1.2 < h:
            obj("w", "boxb", ((x0 + x1) / 2, yf, z), (w - 0.7, 0.08, 1.05), GLASS)
            # laje entre andares
            obj("l", "boxb", ((x0 + x1) / 2, yf + face_sign * 0.04, z + 1.55), (w, 0.14, 0.16), "#FAF9F6")
            z += 3.0; fl += 1

def tree(x, y, s=1.0):
    obj("tr", "cyl", (x, y, 0.9 * s), (0.13 * s, 0.13 * s, 1.8 * s), "#8A6A48")
    obj("tc", "ico", (x, y, 2.35 * s), (1.15 * s, 1.15 * s, 1.15 * s), R.choice(["#6DB35A", "#78BD62", "#62A851"]))
def row(xa, xb, y0, y1, face, hfun, skip=None, strips=True):
    x = xa
    while x < xb:
        w = R.uniform(4.5, 8.5); x1 = min(x + w, xb)
        if skip and not (x1 <= skip[0] or x >= skip[1]):
            x = skip[1] + 0.3; continue
        if x1 - x > 2.0:
            building(x, x1, y0, y1, hfun((x + x1) / 2), face, strips)
        x = x1 + 0.35

def h_north(x):  # baixo perto da loja (câmera alta enxerga a rua), alto longe
    d = abs(x - 10)
    return R.uniform(4.2, 7.2) if d < 16 else R.choice([3, 4, 5, 6]) * 3.0
row(-95, 95, 5.0, 9.8, -1, h_north, skip=(7.7, 12.3))
row(-95, -32, -11.8, -7.6, 1, lambda x: R.uniform(3.6, 6.0))
row(42, 95, -11.8, -7.6, 1, lambda x: R.uniform(3.6, 6.0))
row(-40, 7.3, 13.6, 18.8, -1, lambda x: R.uniform(4.5, 8.5))
row(12.7, 50, 13.6, 18.8, -1, lambda x: R.uniform(4.5, 8.5))
row(-95, 95, 21, 29, 0, lambda x: R.choice([3, 4, 5, 6, 7]) * 3.0, strips=False)
row(-95, 95, 31, 41, 0, lambda x: R.choice([5, 6, 7, 8, 10]) * 3.0, strips=False)
row(-95, -40, -21, -14, 0, lambda x: R.uniform(3.5, 7.0), strips=False)
row(50, 95, -21, -14, 0, lambda x: R.uniform(3.5, 7.0), strips=False)
# parque ao sul (árvores low-poly no lugar dos prédios, deixa a câmera livre)
obj("parque", "boxb", (5, -22, 0), (78, 28, 0.015), "#DCE6C8")
for k in range(70):
    tx = R.uniform(-34, 44); ty = R.uniform(-36, -9)
    if abs(tx - 6) < 5 and ty > -14: continue
    tree(tx, ty, R.uniform(0.8, 1.25))
row(-95, 95, -60, -40, 0, lambda x: R.uniform(4.0, 9.0), strips=False)
# praça ao sul da avenida (calçada larga com árvores e bancos)
obj("praca", "boxb", (0, -5.9, 0), (200, 3.2, 0.018), "#ECE7DE")
for k in range(40):
    bx = -90 + k * 4.6 + R.uniform(-0.5, 0.5)
    if 2 < bx < 14: continue
    if k % 3 == 1:
        obj("banco", "boxb", (bx, -6.6, 0.38), (1.4, 0.45, 0.07), "#B08A63")
        obj("banco_p", "boxb", (bx, -6.6, 0), (1.2, 0.3, 0.38), "#8E9399")

x = -80
while x < 80:
    for s in (-1, 1):
        if not (3 < x < 15) and R.random() < 0.8: tree(x + R.uniform(-1, 1), 4.75 if s > 0 else -6.9, R.uniform(0.85, 1.05))
    x += R.uniform(7, 10)
for (tx, ty) in ((2.0, 12.6), (18.5, 12.6), (-3.5, 12.4)): tree(tx, ty, 0.9)

# ---------------------------------------------------------------- loja
STORE = "#F08A3C"
SX0, SX1, SY0, SY1, SH = 7.5, 12.5, 13.6, 17.6, 3.6
obj("loja", "boxb", (10, (SY0 + SY1) / 2, 0), (SX1 - SX0, SY1 - SY0, SH), STORE)
obj("loja_top", "boxb", (10, (SY0 + SY1) / 2, SH), (SX1 - SX0 + 0.16, SY1 - SY0 + 0.16, 0.2), "#E07428")
obj("porta", "boxb", (11.4, SY0 - 0.01, 0), (1.0, 0.06, 2.3), "#3A3F47")
obj("puxador", "boxb", (11.1, SY0 - 0.05, 1.1), (0.05, 0.05, 0.3), "#C9CED6")
obj("toldo", "box", (10, SY0 - 0.55, 3.0), (5.2, 1.2, 0.12), "#FFFFFF", rot=(math.radians(-14), 0, 0))
for i in range(5):
    obj("toldo_f", "box", (7.92 + i * 1.04, SY0 - 0.56, 3.01), (0.5, 1.21, 0.125), "#E86A2A", rot=(math.radians(-14), 0, 0))
obj("placa_loja", "boxb", (10, SY0 - 0.05, SH - 0.05), (2.6, 0.12, 0.8), "#2B2F36")
text3d("txt_loja", "LOJA", 0.55, (10, SY0 - 0.13, SH + 0.36), "#FFFFFF", 0.01, rot=(math.radians(90), 0, 0))
# vitrine (caixa saliente na fachada: moldura + fundo iluminado + produtos + vidro)
VX = 9.2
obj("vit_frame", "boxb", (VX, SY0 - 0.25, 0.45), (2.6, 0.5, 2.35), "#3A3F47")
vit_back = obj("vit_back", "boxb", (VX, SY0 - 0.52, 0.6), (2.3, 0.04, 2.05), "#FFE8C2", mat=MG)
prods = []
for i, (c, sh) in enumerate([("#7B5BD6", "boxb"), ("#2F7CF6", "cyl"), ("#25A55F", "boxb"), ("#E5484D", "boxb"), ("#F5C542", "cyl"), ("#2F7CF6", "boxb")]):
    row_i, col_i = divmod(i, 3)
    z = 0.72 + row_i * 0.95
    if col_i == 0: obj("shelf", "boxb", (VX, SY0 - 0.68, z - 0.06), (2.2, 0.3, 0.05), "#FFFFFF")
    sx = VX - 0.7 + col_i * 0.7
    if sh == "cyl": prods.append(obj("p", "cyl", (sx, SY0 - 0.7, z + 0.22), (0.15, 0.15, 0.44), c))
    else: prods.append(obj("p", "boxb", (sx, SY0 - 0.7, z), (0.36, 0.2, 0.42 + 0.1 * col_i), c))
obj("vidro", "boxb", (VX, SY0 - 0.9, 0.6), (2.32, 0.03, 2.05), (0.75, 0.88, 1.0, 0.18), mat=MGLASS)
shutter = obj("shutter", "boxt", (VX, SY0 - 0.95, 2.68), (2.62, 0.06, 2.2), STORE)

# ---------------------------------------------------------------- personagens (estilo bloquinho)
SHIRTS = ["#F2B33D", "#3DAA5A", "#9AA0A8", "#E8E8E8", "#3C7DD9", "#E5484D", "#F08A3C", "#7B5BD6", "#5FB7C9", "#D9D2C5"]
PANTS = ["#3B4A63", "#4A4F57", "#2F3A4F", "#6B6F78", "#8A7A63"]
SKIN = ["#EBC6A3", "#D9A57E", "#B98058", "#8D5A3B", "#F1D2B6"]
HAIR = ["#2E2420", "#4A3324", "#1C1C1C", "#6B4A2E", "#8C8C8C"]

class Person:
    def __init__(s, name, shirt=None, hat=None, cap=None, scale=1.0):
        s.root = empty(name)
        pant = R.choice(PANTS); skin = R.choice(SKIN); hair = R.choice(HAIR)
        shirt = shirt or R.choice(SHIRTS)
        s.parts = []
        P = s.parts.append
        s.legL = obj(name + "lL", "boxt", (0.105, 0, 0.82), (0.16, 0.18, 0.82), pant, parent=s.root); P(s.legL)
        s.legR = obj(name + "lR", "boxt", (-0.105, 0, 0.82), (0.16, 0.18, 0.82), pant, parent=s.root); P(s.legR)
        P(obj(name + "t", "boxb", (0, 0, 0.8), (0.46, 0.26, 0.62), shirt, parent=s.root))
        s.armL = obj(name + "aL", "boxt", (0.29, 0, 1.38), (0.12, 0.14, 0.58), shirt, parent=s.root); P(s.armL)
        s.armR = obj(name + "aR", "boxt", (-0.29, 0, 1.38), (0.12, 0.14, 0.58), shirt, parent=s.root); P(s.armR)
        P(obj(name + "h", "sph", (0, 0, 1.6), (0.16, 0.16, 0.17), skin, parent=s.root))
        if hat:
            P(obj(name + "hb", "cyl", (0, 0, 1.73), (0.25, 0.25, 0.025), hat, parent=s.root))
            P(obj(name + "ht", "cyl", (0, 0, 1.88), (0.15, 0.15, 0.3), hat, parent=s.root))
        elif cap:
            P(obj(name + "c", "sph", (0, 0, 1.66), (0.168, 0.168, 0.11), cap, parent=s.root))
            P(obj(name + "cv", "boxb", (0, 0.14, 1.66), (0.26, 0.16, 0.025), cap, parent=s.root))
        else:
            P(obj(name + "hr", "sph", (0, -0.015, 1.665), (0.168, 0.168, 0.12), hair, parent=s.root))
        s.root.scale = (scale,) * 3
        s.base_scale = scale
        s.vis = True
    def pose(s, x, y, z, yaw, swing, sc, armR_extra=0.0):
        vis = sc > 0.002
        if vis != s.vis:
            for p in s.parts: p.hide_render = not vis
            s.vis = vis
        if not vis: return
        s.root.location = (x, y, z); s.root.rotation_euler = (0, 0, yaw)
        k = sc * s.base_scale; s.root.scale = (k, k, k)
        s.legL.rotation_euler.x = 0.5 * swing; s.legR.rotation_euler.x = -0.5 * swing
        s.armL.rotation_euler.x = -0.38 * swing; s.armR.rotation_euler.x = 0.38 * swing - armR_extra

def head_of(st): return (st[0], st[1], st[2] + 1.62 * st[5])

# ---------------------------------------------------------------- objetos animados
# lixeira
BIN = (5.7, 4.55)
obj("lixo", "cyl", (BIN[0], BIN[1], 0.42), (0.32, 0.32, 0.84), "#5E656E")
obj("lixo_b", "cyl", (BIN[0], BIN[1], 0.85), (0.35, 0.35, 0.04), "#4A5058")
BIN_TOP = 0.86

# máquina de moedas (anúncio)
COINBOX = (4.0, 4.1)
coinbox = empty("coinbox_root", (COINBOX[0], COINBOX[1], 0))
obj("cb", "boxb", (0, 0, 0), (0.95, 0.95, 1.05), "#2F7CF6", parent=coinbox)
obj("cb_slot", "boxb", (0, 0, 1.05), (0.5, 0.12, 0.03), "#1A2233", parent=coinbox)
obj("cb_l", "boxb", (0, -0.48, 0.4), (0.6, 0.02, 0.35), "#FFFFFF", parent=coinbox)
coinbox.scale = (0.001,) * 3

# cards do feed (posts deitados na avenida, "topo" virado pra +X)
IMG_COLS = ["#F6A04D", "#7AC6E8", "#E86A8C", "#8BD17C", "#B58CE8", "#F5D04E", "#5FB7C9", "#F08A3C"]
CARD_X = [-77 + 7.0 * i for i in range(23)]
cards = []
for i, cx in enumerate(CARD_X):
    r = empty(f"card{i}", (cx, 0, 0.0))
    obj("cb", "boxb", (0, 0, 0), (6.6, 5.9, 0.05), "#FFFFFF", parent=r)
    obj("ci", "boxb", (-0.15, 0, 0.05), (4.9, 5.2, 0.015), IMG_COLS[i % len(IMG_COLS)], parent=r)
    # "foto": formas simples sobre a imagem
    obj("cs", "cyl", (0.4, -1.2, 0.07), (0.7, 0.7, 0.01), "#FFFFFF", parent=r).color = (1, 1, 1, 0.55)
    obj("cm", "boxb", (-1.2, 0.8, 0.065), (1.6, 2.4, 0.01), "#FFFFFF", parent=r).color = (1, 1, 1, 0.35)
    obj("ca", "cyl", (2.85, 2.35, 0.06), (0.26, 0.26, 0.02), IMG_COLS[(i + 3) % len(IMG_COLS)], parent=r)
    obj("cn", "boxb", (2.85, 1.2, 0.05), (0.18, 1.5, 0.01), "#3A3F47", parent=r)
    for j, c in enumerate(["#E5484D", "#9AA0A8", "#9AA0A8"]):
        obj("cf", "cyl", (-2.95, 2.35 - j * 0.62, 0.06), (0.18, 0.18, 0.015), c, parent=r)
    r.scale = (0.001,) * 3
    cards.append(r)

# placas (posts orgânicos que ficam)
PLACA_X = [3.5, 16.5, -1.5, 21.5, -6.5, 26.5, -11.5, 31.5, -16.5, 36.5, -21.5, 41.5, -26.5, 46.5, -31.5]
placas = []
for i, px in enumerate(PLACA_X[:len(PLACA_T)]):
    side = 1 if i % 2 == 0 else -1
    py = side * 4.55
    r = empty(f"placa{i}", (px, py, 0))
    obj("pp", "cyl", (0, 0, 1.2), (0.06, 0.06, 2.4), "#9AA0A8", parent=r)
    obj("pb", "boxb", (0, 0, 2.2), (1.5, 0.1, 1.75), "#FFFFFF", parent=r)
    obj("pi", "boxb", (0, -side * 0.06, 2.42), (1.25, 0.02, 1.2), IMG_COLS[(i + 1) % len(IMG_COLS)], parent=r)
    obj("ph", "cyl", (-0.45, -side * 0.06, 3.78), (0.1, 0.1, 0.02), "#E5484D", rot=(math.pi / 2, 0, 0), parent=r)
    ar = obj("pa", "arrow", (0, -side * 0.02, 1.62), (0.95, 0.9, 0.08), "#25A55F", parent=r)
    ar.rotation_euler = (math.pi / 2, 0, 0) if px < 10 else (math.pi / 2, math.pi, 0)
    r.scale = (0.001,) * 3
    placas.append(r)

# pool de panfletos
flyer_objs = []
def new_flyer(color):
    o = obj("fly", "box", (0, 0, -50), (0.3, 0.4, 0.015), color)
    o.hide_render = True
    flyer_objs.append(o); return len(flyer_objs) - 1
coins = []

# "?" sobre passantes
qmarks = [text3d(f"q{i}", "?", 0.55, (0, 0, -50), "#2B2F36", 0.04) for i in range(2)]

# ---------------------------------------------------------------- pessoas
N_CROWD = 230
crowd = [Person(f"c{i}") for i in range(N_CROWD)]
owner = Person("owner", shirt="#F2B33D")
pan = Person("pan", shirt="#E5484D", hat="#2B2F36")
adg = Person("adg", shirt="#2F7CF6", cap="#1E4FA8")
pass1 = Person("pass1", shirt="#9AA0A8"); pass2 = Person("pass2", shirt="#3DAA5A")
DOOR = (11.4, 13.45)

# ---------------------------------------------------------------- simulação (determinística)
S = random.Random(11)
AV_X = 78.0
class CS:  # estado de um pedestre
    pass
cs = []
for i in range(N_CROWD):
    c = CS(); c.x = S.uniform(-AV_X, AV_X); c.y = S.uniform(-3.7, 3.7); c.dir = S.choice([-1, 1])
    c.v = S.uniform(0.95, 1.4); c.mode = "crowd"; c.phase = S.uniform(0, 6.28); c.path = None; c.pi = 0
    c.scale = 1.0; c.timer = 0; c.flyered = False; c.flyer = None; c.yaw = 0; c.swing_amp = 1.0; c.z = 0.0
    cs.append(c)

flyers = []  # dicts com estado
landed = 0
visits = 0
state_people = []   # por frame: lista de tuplas
state_fly = []
state_misc = []
events = {}  # rótulos especiais rastreados
share_marks = []
pending = []  # (t, fn)

def sched(t, fn): pending.append((t, fn))

def divert(i, t):
    c = cs[i]
    if c.mode != "crowd": return False
    j = S.uniform(-1.2, 1.2)
    c.mode = "divert"
    c.path = [(10 + j, S.uniform(3.6, 4.0)), (10 + j * 0.5, 11.2), (DOOR[0] + S.uniform(-0.15, 0.15), 12.7), (DOOR[0], DOOR[1] + 0.35)]
    c.pi = 0; c.v2 = S.uniform(3.1, 3.6)
    return True

def give_flyer(src_fn, i, t, color, dur, peak, then):
    k = new_flyer(color)
    flyers.append(dict(k=k, kind="fly", t0=t, dur=dur, src=src_fn(), tgt=i, peak=peak, then=then, rz=S.uniform(0, 6.28)))
    cs[i].flyered = True

def heads():
    return [(c.x, c.y, c.z + 1.62 * c.scale) for c in cs]

pan_pos = (7.0, 3.25); adg_pos = (5.3, 3.3)
pan_throw = []; adg_throw = []
ad_fire_times = []
t = T["ad_fire"]
while t < T["ad_stop"] - 0.45:
    ad_fire_times.append(t); t += S.uniform(0.09, 0.16)
t = BURST[0]
while t < BURST[1]:
    ad_fire_times.append(t); t += S.uniform(0.08, 0.13)
coin_times = []
t = T["coins"]
while t < T["ad_stop"] - 0.2: coin_times.append(t); t += 0.32
t = BURST[0] - 0.4
while t < BURST[1] - 0.3: coin_times.append(t); t += 0.25
for k, ct in enumerate(coin_times):
    o = obj(f"coin{k}", "cyl24", (0, 0, -50), (0.2, 0.2, 0.05), "#F5C542", rot=(math.pi / 2, 0, 0))
    o.hide_render = True; coins.append((ct, o, S.uniform(-0.2, 0.2)))
ad_ptr = 0
share_targets = []  # (t, i) pra callouts
org_divs = []

tracked = {}

for f in range(NF + 1):
    t = f / FPS; dt = 1 / FPS
    # eventos agendados
    due = [p for p in pending if p[0] <= t]
    pending[:] = [p for p in pending if p[0] > t]
    for _, fn in due: fn(t)
    # tiros do anúncio
    while ad_ptr < len(ad_fire_times) and ad_fire_times[ad_ptr] <= t:
        cand = [i for i, c in enumerate(cs) if c.mode == "crowd" and not c.flyered and 0 < c.x < 22]
        if cand:
            i = S.choice(cand)
            adg_throw.append(t)
            def then_ad(tt, i=i):
                divert(i, tt)
            give_flyer(lambda: (adg_pos[0], adg_pos[1] - 0.3, 1.9), i, t, "#2F7CF6", 0.75, 4.5, then_ad)
        ad_ptr += 1
    # pedestres
    hb = heads()
    for i, c in enumerate(cs):
        ox = c.x
        moving = True
        if c.mode == "crowd":
            c.x += c.dir * c.v * dt
            if c.x > AV_X: c.x -= 2 * AV_X; c.flyered = False
            if c.x < -AV_X: c.x += 2 * AV_X; c.flyered = False
            c.yaw = math.atan2(0, c.dir) - math.pi / 2
            dist = c.v * dt
            # panfleteiro
            if T["pan_on"] + 0.4 < t < T["pan_off"] and not c.flyered and c.y > -1.8:
                if (ox - pan_pos[0]) * (c.x - pan_pos[0]) <= 0:
                    pan_throw.append(t)
                    if S.random() < 0.55:
                        then = lambda tt, i=i: divert(i, tt)
                        give_flyer(lambda: (pan_pos[0] - 0.3, pan_pos[1] - 0.2, 1.3), i, t, "#FFFFFF", 0.35, 0.5, then)
                    else:
                        give_flyer(lambda: (pan_pos[0] - 0.3, pan_pos[1] - 0.2, 1.3), i, t, "#FFFFFF", 0.35, 0.5, "toss")
            # placas
            for pk, ptime in enumerate(PLACA_T):
                if t > ptime + 0.3:
                    px = PLACA_X[pk]
                    if (ox - px) * (c.x - px) <= 0 and S.random() < 0.6:
                        if divert(i, t):
                            c.flyered = True
                            k = new_flyer("#FFFFFF")
                            flyers.append(dict(k=k, kind="pop", t0=t, tgt=i, rz=0))
                            org_divs.append((t, i))
                            if S.random() < 0.55:
                                def share(tt, i=i):
                                    best, bd = None, 9.0
                                    for j2, c2 in enumerate(cs):
                                        if c2.mode == "crowd" and not c2.flyered:
                                            d2 = math.hypot(c2.x - cs[i].x, c2.y - cs[i].y)
                                            if d2 < bd: best, bd = j2, d2
                                    if best is not None:
                                        share_targets.append((tt, i, best))
                                        give_flyer(lambda: head_of((cs[i].x, cs[i].y, cs[i].z, 0, 0, cs[i].scale)), best, tt, "#FFFFFF", 0.5, 1.2,
                                                   lambda t3, b=best: divert(b, t3))
                                sched(t + 0.7, share)
                        break
        elif c.mode == "divert":
            tx, ty = c.path[c.pi]
            dx, dy = tx - c.x, ty - c.y; d = math.hypot(dx, dy)
            step = c.v2 * dt
            if d <= step:
                c.x, c.y = tx, ty; c.pi += 1
                if c.pi == 1: visits += 1  # entrou na rua da loja
                if c.pi >= len(c.path):
                    c.mode = "enter"; c.timer = 0
            else:
                c.x += dx / d * step; c.y += dy / d * step
                target_yaw = math.atan2(dy, dx) - math.pi / 2
                dyaw = (target_yaw - c.yaw + math.pi) % (2 * math.pi) - math.pi
                c.yaw += dyaw * min(1, dt * 10)
            dist = step
        elif c.mode == "enter":
            c.timer += dt; c.scale = max(0.0, 1 - c.timer / 0.3); dist = 0.02
            if c.timer >= 0.3:
                c.mode = "inside"; c.timer = 0
                for fl in flyers:
                    if fl.get("tgt") == i and fl.get("held"): fl["gone"] = t
        elif c.mode == "inside":
            c.timer += dt; dist = 0
            if c.timer > 2.5:
                c.mode = "crowd"; c.scale = 1.0; c.dir = S.choice([-1, 1])
                c.x = S.choice([S.uniform(-62, -30), S.uniform(40, 70)])
                c.y = S.uniform(-3.7, 3.7); c.flyered = False
        c.phase += dist * 2 * math.pi / 1.15
        c.z = 0.055 * ease((t - T["cards"]) / 1.0) if t > T["cards"] else 0.0
    # panfletos
    hb = heads()
    fs = {}
    for fl in flyers:
        k = fl["k"]; dtn = t - fl["t0"]
        if dtn < 0 or fl.get("gone", 1e9) < t: continue
        c = cs[fl["tgt"]]
        hold = (c.x, c.y, c.z + 1.25 * c.scale + 0.0)
        if fl["kind"] == "pop":
            s = eback(dtn / 0.35)
            fs[k] = (hold[0], hold[1], hold[2] + 0.75, fl["rz"] + c.yaw, s, 1.0); fl["held"] = True
            if c.mode in ("inside",) or c.scale <= 0.01: fl["gone"] = t
            continue
        if dtn < fl["dur"]:
            a = dtn / fl["dur"]; sx, sy, sz = fl["src"]
            hx, hy, hz = hold[0], hold[1], hold[2] + 0.45
            x = lerp(sx, hx, a); y = lerp(sy, hy, a); z = lerp(sz, hz, a) + fl["peak"] * 4 * a * (1 - a)
            fs[k] = (x, y, z, fl["rz"] + a * 9, 1.0, 1.0)
            continue
        if not fl.get("arrived"):
            fl["arrived"] = t
            if callable(fl["then"]): fl["then"](t)
            elif fl["then"] == "toss": fl["toss_t"] = t + S.uniform(2.3, 3.0)
        if fl.get("toss_t") and t >= fl["toss_t"]:
            if not fl.get("toss_src"): fl["toss_src"] = (hold[0], hold[1], hold[2] + 0.45)
            a = (t - fl["toss_t"]) / 0.6
            if a < 1:
                sx, sy, sz = fl["toss_src"]
                if not fl.get("land"):
                    landed_n = landed; landed += 1
                    if landed_n < 34:
                        ang = S.uniform(0, 6.28); r = S.uniform(0, 0.22)
                        fl["land"] = (BIN[0] + math.cos(ang) * r, BIN[1] + math.sin(ang) * r, BIN_TOP - 0.02 + min(landed_n, 30) * 0.012)
                    else:
                        ang = S.uniform(0, 6.28); r = S.uniform(0.45, 1.3)
                        fl["land"] = (BIN[0] + math.cos(ang) * r, BIN[1] + math.sin(ang) * r, 0.03)
                lx, ly, lz = fl["land"]
                fs[k] = (lerp(sx, lx, a), lerp(sy, ly, a), lerp(sz, lz, a) + 1.4 * 4 * a * (1 - a), fl["rz"] + a * 12, 1.0, 1.0)
            else:
                lx, ly, lz = fl["land"]
                fs[k] = (lx, ly, lz, fl["rz"], 1.0, 0.0)
            continue
        fl["held"] = True
        if c.mode in ("inside",) or c.scale <= 0.01:
            fl["gone"] = t; continue
        fs[k] = (hold[0], hold[1], hold[2] + 0.45, c.yaw, max(c.scale, 0.0), 1.0)
    state_fly.append(fs)
    state_people.append([(c.x, c.y, c.z, c.yaw, math.sin(c.phase) * (1.0 if c.mode in ("crowd", "divert") else 0.0), c.scale) for c in cs])
    state_misc.append(dict(visits=visits))

print("SIM OK flyers", len(flyer_objs), "visits", visits)

# ---------------------------------------------------------------- câmera
cam_d = bpy.data.cameras.new("cam"); cam_d.sensor_fit = "VERTICAL"; cam_d.sensor_height = 36
cam_d.clip_start = 0.1; cam_d.clip_end = 600
cam = bpy.data.objects.new("cam", cam_d); COLL.objects.link(cam); sc.camera = cam

Z = (0, 0, 1); XU = (1, 0, 0)
# (t, loc, alvo, lente, up)
CK = [
    (0.0, (3.0, -9.0, 16.0), (10.0, 13.0, 1.4), 32, Z),
    (2.0, (8.0, 4.2, 3.6), (10.0, 13.6, 1.9), 30, Z),
    (6.4, (8.8, 6.6, 2.9), (10.0, 13.6, 1.8), 30, Z),
    (8.4, (9.0, 7.2, 2.8), (9.9, 13.6, 1.8), 30, Z),
    (11.0, (10.5, -14.0, 24.0), (10.0, 6.0, 0.0), 30, Z),
    (15.4, (12.5, -15.5, 25.0), (10.0, 6.0, 0.0), 30, Z),
    (17.6, (1.8, -6.2, 3.3), (7.0, 3.0, 1.1), 30, Z),
    (21.5, (3.0, -5.6, 3.0), (7.2, 3.2, 1.1), 30, Z),
    (24.6, (2.0, -3.5, 13.5), (10.5, 9.5, 0.4), 30, Z),
    (25.7, (2.4, -3.2, 13.8), (10.5, 9.8, 0.4), 30, Z),
    (26.9, (3.6, 1.4, 2.0), (5.8, 4.5, 0.75), 30, Z),
    (30.9, (4.0, 1.9, 1.8), (5.8, 4.5, 0.75), 30, Z),
    (33.0, (6.0, 0.2, 30.0), (6.0, 0.0, 0.0), 30, XU),
    (38.5, (6.5, 0.2, 29.0), (6.5, 0.0, 0.0), 30, XU),
    (40.4, (10.4, 3.0, 6.0), (10.2, 13.6, 1.8), 30, Z),
    (41.0, (10.4, 3.4, 5.8), (10.2, 13.6, 1.8), 30, Z),
    (43.0, (-3.0, -17.0, 14.0), (7.5, 5.5, 0.0), 30, Z),
    (52.3, (-1.0, -18.0, 15.0), (7.5, 5.5, 0.0), 30, Z),
    (54.6, (-9.0, -15.0, 15.0), (5.0, 5.0, 0.0), 30, Z),
    (64.5, (-6.0, -19.0, 18.0), (5.0, 5.0, 0.0), 30, Z),
    (69.5, (-2.0, -30.0, 30.0), (7.0, 6.0, 0.0), 30, Z),
    (72.6, (-1.0, -31.5, 31.0), (7.0, 6.0, 0.0), 30, Z),
]
def cam_at(t):
    for a, b in zip(CK, CK[1:]):
        if a[0] <= t <= b[0]:
            k = ease((t - a[0]) / (b[0] - a[0]))
            return vlerp(a[1], b[1], k), vlerp(a[2], b[2], k), lerp(a[3], b[3], k), vlerp(a[4], b[4], k)
    a = CK[-1] if t > CK[-1][0] else CK[0]
    return a[1], a[2], a[3], a[4]
def set_cam(t):
    loc, tg, lens, up = cam_at(t)
    loc = Vector(loc); f = (Vector(tg) - loc).normalized(); up = Vector(up).normalized()
    r = f.cross(up)
    if r.length < 1e-4: r = f.cross(Vector((1, 0, 0)))
    r.normalize(); u = r.cross(f)
    m = Matrix(((r.x, u.x, -f.x), (r.y, u.y, -f.y), (r.z, u.z, -f.z)))
    cam.matrix_world = Matrix.Translation(loc) @ m.to_4x4()
    cam_d.lens = lens

# ---------------------------------------------------------------- aplicar frame
def apply(f):
    t = f / FPS
    set_cam(t)
    P = state_people[f]
    for i, p in enumerate(crowd):
        x, y, z, yaw, sw, s = P[i]
        p.pose(x, y, z, yaw, sw, s)
    # dono
    owner.pose(12.95, 12.95, 0, math.pi - 0.35, 0, 1.0)
    # panfleteiro
    s_pan = eback((t - T["pan_on"]) / 0.5) * (1 - eout((t - T["pan_off"]) / 0.4))
    thr = max([0] + [1 - abs(t - tt - 0.12) / 0.18 for tt in pan_throw if abs(t - tt - 0.12) < 0.18])
    pan.pose(pan_pos[0], pan_pos[1], 0, math.pi + 0.5, 0, max(0, s_pan), armR_extra=1.3 * thr + 0.5)
    # cara do anúncio
    on_ad = eback((t - (T["ad"] + 0.6)) / 0.5) * (1 - eout((t - (T["org"] + 0.2)) / 0.4))
    on_burst = eback((t - (BURST[0] - 0.6)) / 0.4) * (1 - eout((t - (BURST[1] + 0.6)) / 0.4))
    s_ad = max(on_ad, on_burst)
    thr = max([0] + [1 - abs(t - tt - 0.1) / 0.15 for tt in adg_throw if abs(t - tt - 0.1) < 0.15])
    adg.pose(adg_pos[0], adg_pos[1], 0.055 if t > T["cards"] else 0, math.pi, 0, max(0, s_ad), armR_extra=2.2 * thr + 0.3)
    coinbox.scale = (max(0.001, s_ad),) * 3
    coinbox.location.z = 0.055 if t > T["cards"] else 0
    for ct, o, jx in coins:
        a = (t - ct) / 0.55
        if 0 <= a <= 1:
            o.hide_render = False; z = lerp(8.0, 1.12, a * a)
            o.location = (COINBOX[0] + jx * (1 - a), COINBOX[1], z); o.rotation_euler = (math.pi / 2, 0, a * 8)
        else: o.hide_render = True
    # passantes com "?"
    for k, (p, yl, t0) in enumerate(((pass1, 11.3, 0.4), (pass2, 12.1, 1.2))):
        a = (t - t0) / 7.0
        if 0 <= a <= 1 and t < 9.0:
            x = lerp(2.5, 19.5, a)
            ph = (t - t0) * 2.0 / 1.15 * 2 * math.pi
            # olham pra loja ao passar
            near = max(0, 1 - abs(x - 10) / 3.0)
            p.pose(x, yl, 0, -math.pi / 2 + near * 0.9, math.sin(ph), 1.0)
            q = qmarks[k]; qs = eback((t - (t0 + 1.4)) / 0.4) * (1 - eout((t - 7.6) / 0.3))
            q.location = (x, yl, 2.25 + 0.05 * math.sin(t * 4)); q.scale = (max(qs, 0.001),) * 3
            q.rotation_euler = cam.matrix_world.to_euler()
            q.hide_render = qs <= 0.002
        else:
            p.pose(0, 0, 0, 0, 0, 0); qmarks[k].hide_render = True
    # vitrine
    a = ease((t - T["vitrine_open"]) / 1.0)
    shutter.scale.z = max(0.001, 2.2 * (1 - a)); shutter.hide_render = a >= 0.999
    glow = 0.15 + 1.6 * a
    vit_back.material_slots[0].material = MG if a > 0.01 else M
    vit_back.color = hexc("#FFE8C2") if a > 0.01 else hexc("#3A3F47")
    for j, pr in enumerate(prods):
        k = eback((t - T["vitrine_open"] - 0.5 - j * 0.07) / 0.4)
        pr.hide_render = k <= 0.01
    # cards
    if t < T["cards"]:
        for r in cards: r.scale = (0.001,) * 3
    else:
        # rolagem
        def spd(tt):
            if tt < T["scroll"]: return 0
            if tt < T["perfil"]: return 3.0 * ease((tt - T["scroll"]) / 0.6)
            return lerp(3.0, 0.55, ease((tt - T["perfil"]) / 1.2))
        # integral simples
        off = 0.0; tt = T["scroll"]
        while tt < t: off += spd(tt) / FPS; tt += 1 / FPS
        for i, r in enumerate(cards):
            d = abs(CARD_X[i] - 6.0)
            k = eback((t - T["cards"] - d * 0.012) / 0.45)
            x = CARD_X[i] + off
            x = (x + 80.5) % 161.0 - 80.5
            r.location = (x, 0, 0.0); r.scale = (max(k, 0.001),) * 3
    # placas
    for i, r in enumerate(placas):
        k = eback((t - PLACA_T[i]) / 0.45)
        r.scale = (max(k, 0.001),) * 3
    # panfletos
    fs = state_fly[f]
    for k, o in enumerate(flyer_objs):
        st = fs.get(k)
        if st is None:
            if not o.hide_render: o.hide_render = True
            continue
        x, y, z, rz, s, tilt = st
        o.hide_render = s <= 0.002
        o.location = (x, y, z); o.scale = (0.3 * s, 0.4 * s, 0.015)
        o.rotation_euler = (0.9 * tilt * 0 + (0 if tilt == 0 else 0.25), 0, rz)
        if tilt == 1.0 and z > 1.0: o.rotation_euler = (math.radians(70), 0, rz)

# âncoras pra overlay
ANCH = dict(
    loja=(10, SY0, SH + 0.9), porta=(DOOR[0], SY0, 2.4), vitrine=(VX, SY0, 2.9),
    dono=(12.95, 12.95, 2.0), pan=(pan_pos[0], pan_pos[1], 2.25), lixo=(BIN[0], BIN[1], 1.0),
    anuncio=(adg_pos[0], adg_pos[1], 2.1), moedas=(COINBOX[0], COINBOX[1], 1.3),
    avenida=(-2.0, 0.0, 0.5), rua=(10.0, 8.5, 0.2), placa0=(PLACA_X[0], 4.55, 4.0), placa1=(PLACA_X[1], -4.55, 4.0),
    placa2=(PLACA_X[2], 4.55, 4.0),
)
def proj(p):
    v = world_to_camera_view(sc, cam, Vector(p))
    return [round(v.x, 4), round(1 - v.y, 4), round(v.z, 3)]

# ---------------------------------------------------------------- frames
def parse_frames(s):
    out = []
    for part in s.split(","):
        step = 1
        if ":" in part: part, st = part.split(":"); step = int(st)
        if "-" in part:
            a, b = part.split("-"); out += list(range(int(a), int(b) + 1, step))
        else: out.append(int(part))
    return [x for x in out if 0 <= x <= NF]
frames = parse_frames(FRAMES_ARG)
si, sn = map(int, SHARD.split("/"))
frames = frames[si::sn]

# anotações de rastreio (todos os frames, só no shard 0)
if si == 0:
    meta = dict(fps=FPS, nf=NF, T=T, placas=PLACA_T, burst=BURST, frames=[])
    shares = sorted(share_targets)
    picks = []
    for want in (59.6, 60.68, 61.32):
        best = min(shares, key=lambda s: abs(s[0] - want)) if shares else None
        picks.append(best)
    meta["picks"] = [list(p) if p else None for p in picks]
    meta["ev"] = dict(pan=pan_throw, ad=adg_throw, coins=coin_times,
                      land=sorted(fl["toss_t"] + 0.6 for fl in flyers if fl.get("toss_t") and fl.get("land")),
                      org=[x[0] for x in org_divs], shares=[x[0] for x in share_targets])
    for f in range(NF + 1):
        t = f / FPS; set_cam(t)
        d = {k: proj(v) for k, v in ANCH.items()}
        P = state_people[f]
        for n, pk in enumerate(picks):
            if pk:
                _, a_i, b_i = pk
                for tag, idx in (("A", a_i), ("B", b_i)):
                    st = P[idx]; d[f"share{n}{tag}"] = proj(head_of(st)) + [st[5]]
        d["visits"] = state_misc[f]["visits"]
        meta["frames"].append(d)
    with open(os.path.join(OUT, "meta.json"), "w") as fh: json.dump(meta, fh)

for f in frames:
    apply(f)
    sc.frame_current = f
    sc.render.filepath = os.path.join(OUT, f"f{f:05d}.png")
    bpy.ops.render.render(write_still=True)
    print("FRAME", f, flush=True)
print("DONE")
