import sys as _s, os as _o
_s.path.insert(0, _o.path.dirname(_o.path.dirname(_o.path.abspath(__file__))))  # scripts/ (ambiente.py)
import ambiente
# Maquete Viva — base (Blender 5.1, rodar com -b --factory-startup). Padrão: modo PREMIUM (Cycles).
# Cada cena faz:  import mvb; mvb.setup(DUR) ... e no fim mvb.run(apply, ANCH, extra_meta)
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

def tf(t): return int(round(t * FPS))
def ease(a):
    a = max(0.0, min(1.0, a)); return a * a * a * (a * (a * 6 - 15) + 10)
def eout(a):
    a = max(0.0, min(1.0, a)); return 1 - (1 - a) ** 3
def eback(a):
    a = max(0.0, min(1.0, a)); c1 = 1.70158; c3 = c1 + 1
    return 1 + c3 * (a - 1) ** 3 + c1 * (a - 1) ** 2
def lerp(a, b, k): return a + (b - a) * k
def vlerp(a, b, k): return tuple(lerp(a[i], b[i], k) for i in range(len(a)))
def win(t, t0, t1, fi=0.35, fo=0.35, back=True):
    """0..1 que entra (pop) em t0 e sai em t1."""
    if t < t0 or t > t1 + fo: return 0.0
    a = (eback if back else eout)((t - t0) / fi)
    return a * (1 - eout((t - t1) / fo)) if t > t1 else a
def hexc(h, a=1.0):
    h = h.lstrip("#"); r, g, b = (int(h[i:i + 2], 16) / 255 for i in (0, 2, 4))
    lin = lambda c: c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4
    return (lin(r), lin(g), lin(b), a)

R = random.Random(7)
sc = bpy.context.scene
NF = 0
DUR = 0
M = MG = MGLASS = None
ME = {}
COLL = sc.collection
FONT = None
cam = cam_d = None

PREMIUM = False
def make_mat(name, rough=0.85, emit=0.0, bevel=0.025, grain=0.035):
    m = bpy.data.materials.new(name); m.use_nodes = True
    nt = m.node_tree; P = nt.nodes["Principled BSDF"]
    oi = nt.nodes.new("ShaderNodeObjectInfo")
    nt.links.new(oi.outputs["Color"], P.inputs["Base Color"])
    nt.links.new(oi.outputs["Alpha"], P.inputs["Alpha"])
    P.inputs["Roughness"].default_value = rough
    if PREMIUM:
        P.inputs["Roughness"].default_value = min(rough, 0.62)
        bv = nt.nodes.new("ShaderNodeBevel"); bv.samples = 2; bv.inputs["Radius"].default_value = bevel
        bump = nt.nodes.new("ShaderNodeBump"); bump.inputs["Strength"].default_value = grain; bump.inputs["Distance"].default_value = 0.02
        nz = nt.nodes.new("ShaderNodeTexNoise"); nz.inputs["Scale"].default_value = 90.0; nz.inputs["Detail"].default_value = 4.0
        nt.links.new(nz.outputs["Fac"], bump.inputs["Height"]); nt.links.new(bv.outputs["Normal"], bump.inputs["Normal"])
        nt.links.new(bump.outputs["Normal"], P.inputs["Normal"])
    if "Specular IOR Level" in P.inputs: P.inputs["Specular IOR Level"].default_value = 0.15
    if emit > 0:
        nt.links.new(oi.outputs["Color"], P.inputs["Emission Color"])
        P.inputs["Emission Strength"].default_value = emit
    try: m.surface_render_method = "DITHERED"
    except Exception: pass
    return m

def bm_mesh(name, fn, smooth=False):
    me = bpy.data.meshes.new(name); bm = bmesh.new(); fn(bm); bm.to_mesh(me); bm.free()
    me.materials.append(M)
    if smooth: me.shade_smooth()
    return me
def _cube(bm, dz):
    bmesh.ops.create_cube(bm, size=1.0)
    for v in bm.verts: v.co.z += dz
def _arrow(bm):
    pts = [(-0.5, -0.14), (0.12, -0.14), (0.12, -0.32), (0.5, 0), (0.12, 0.32), (0.12, 0.14), (-0.5, 0.14)]
    vs = [bm.verts.new((x, y, 0)) for x, y in pts]; f = bm.faces.new(vs)
    r = bmesh.ops.extrude_face_region(bm, geom=[f])
    for v in [e for e in r["geom"] if isinstance(e, bmesh.types.BMVert)]: v.co.z += 1
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
def _heart(bm):
    pts = []
    for i in range(40):
        a = i / 40 * 2 * math.pi
        x = 16 * math.sin(a) ** 3; y = 13 * math.cos(a) - 5 * math.cos(2 * a) - 2 * math.cos(3 * a) - math.cos(4 * a)
        pts.append((x / 32, y / 32))
    vs = [bm.verts.new((x, y, 0)) for x, y in pts]; f = bm.faces.new(vs)
    r = bmesh.ops.extrude_face_region(bm, geom=[f])
    for v in [e for e in r["geom"] if isinstance(e, bmesh.types.BMVert)]: v.co.z += 0.25
    for v in bm.verts: v.co.z -= 0.125
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)

ASSETS = os.environ.get("MAQUETE_ASSETS", os.path.join(ambiente.SKILL, "assets", "modelos"))
def setup(dur, bg="#F6F1E8", bg_strength=0.72, sun_energy=3.4, premium=True, hdri="auto", samples=32):
    """premium=True (padrão): Cycles + HDRI + quinas arredondadas + grão + desfoque de miniatura.
    premium=False: modo rápido antigo (EEVEE, cores lisas) — só pra rascunho."""
    global NF, DUR, M, MG, MGLASS, FONT, cam, cam_d, PREMIUM
    PREMIUM = premium
    if hdri == "auto":
        hdri = os.path.join(ASSETS, "hdri", "ceu.hdr")
        if not os.path.exists(hdri): hdri = None
    DUR = dur; NF = int(dur * FPS)
    for o in list(bpy.data.objects): bpy.data.objects.remove(o, do_unlink=True)
    sc.render.engine = "BLENDER_EEVEE"
    sc.render.resolution_x, sc.render.resolution_y = 1080, 1920
    sc.render.resolution_percentage = RES
    sc.render.fps = FPS
    sc.render.image_settings.file_format = "PNG"
    ee = sc.eevee; ee.taa_render_samples = 24
    for k, v in dict(use_shadows=True, use_raytracing=True, use_fast_gi=True, shadow_ray_count=2, shadow_step_count=8).items():
        try: setattr(ee, k, v)
        except Exception: pass
    for vt in ("Standard", "AgX"):
        try: sc.view_settings.view_transform = vt; break
        except Exception: pass
    try: sc.view_settings.look = "None"
    except Exception: pass
    world = bpy.data.worlds.new("W"); sc.world = world; world.use_nodes = True
    b = world.node_tree.nodes["Background"]
    b.inputs[0].default_value = hexc(bg); b.inputs[1].default_value = bg_strength
    sun_d = bpy.data.lights.new("sun", "SUN"); sun_d.energy = sun_energy; sun_d.angle = math.radians(14)
    sun_d.color = hexc("#FFF6EA")[:3]
    sun = bpy.data.objects.new("sun", sun_d); COLL.objects.link(sun)
    sun.rotation_euler = (math.radians(48), math.radians(-14), math.radians(-30))
    if premium: _setup_cycles(hdri, samples, sun)
    M = make_mat("M"); MG = make_mat("Mglow", 0.6, 1.4); MGLASS = make_mat("Mglass", 0.08, bevel=0.0, grain=0.0)
    ME.update(
        box=bm_mesh("box", lambda bm: _cube(bm, 0.0)),
        boxb=bm_mesh("boxb", lambda bm: _cube(bm, 0.5)),
        boxt=bm_mesh("boxt", lambda bm: _cube(bm, -0.5)),
        cyl=bm_mesh("cyl", lambda bm: bmesh.ops.create_cone(bm, cap_ends=True, cap_tris=False, segments=14, radius1=1, radius2=1, depth=1)),
        cyl24=bm_mesh("cyl24", lambda bm: bmesh.ops.create_cone(bm, cap_ends=True, cap_tris=False, segments=28, radius1=1, radius2=1, depth=1), True),
        cone=bm_mesh("cone", lambda bm: bmesh.ops.create_cone(bm, cap_ends=True, cap_tris=False, segments=14, radius1=1, radius2=0, depth=1)),
        sph=bm_mesh("sph", lambda bm: bmesh.ops.create_uvsphere(bm, u_segments=18, v_segments=12, radius=1), True),
        ico=bm_mesh("ico", lambda bm: bmesh.ops.create_icosphere(bm, subdivisions=1, radius=1)),
        arrow=bm_mesh("arrow", _arrow),
        heart=bm_mesh("heart", _heart, False),
    )
    _f = ambiente.achar_fonte("segoeuib.ttf", "Poppins-Bold.ttf", "arialbd.ttf", "Arial Bold.ttf")
    FONT = bpy.data.fonts.load(_f) if _f else bpy.data.fonts.load("<builtin>")
    cam_d = bpy.data.cameras.new("cam"); cam_d.sensor_fit = "VERTICAL"; cam_d.sensor_height = 36
    cam_d.clip_start = 0.1; cam_d.clip_end = 600
    cam = bpy.data.objects.new("cam", cam_d); COLL.objects.link(cam); sc.camera = cam

def _setup_cycles(hdri, samples, sun):
    sc.render.engine = "CYCLES"
    cy = sc.cycles
    try:
        pr = bpy.context.preferences.addons["cycles"].preferences
        want = os.environ.get("MVB_GPU"); ok = False
        for tipo in ("OPTIX", "CUDA", "METAL", "HIP", "ONEAPI"):   # NVIDIA, Mac, AMD, Intel
            try: pr.compute_device_type = tipo
            except Exception: continue
            pr.get_devices(); k = 0
            for d in pr.devices:
                if d.type == tipo:
                    d.use = (want is None or str(k) == want); k += 1; ok = ok or d.use
                else: d.use = False
            if ok: break
        cy.device = "GPU" if ok else "CPU"
        print("Cycles:", cy.device, pr.compute_device_type if ok else "")
    except Exception as e: print("GPU?", e)
    cy.samples = samples; cy.use_adaptive_sampling = True; cy.adaptive_threshold = 0.03
    cy.use_denoising = True
    try: cy.denoiser = "OPTIX"
    except Exception: pass
    cy.max_bounces = 4; cy.diffuse_bounces = 2; cy.glossy_bounces = 1; cy.transmission_bounces = 4; cy.caustics_reflective = False; cy.caustics_refractive = False
    sc.render.use_persistent_data = True
    for vt, lk in (("AgX", "AgX - Punchy"), ("AgX", "Punchy"), ("AgX", "None")):
        try: sc.view_settings.view_transform = vt; sc.view_settings.look = lk; break
        except Exception: pass
    if hdri:
        nt = sc.world.node_tree; env = nt.nodes.new("ShaderNodeTexEnvironment"); env.image = bpy.data.images.load(hdri)
        nt.links.new(env.outputs["Color"], nt.nodes["Background"].inputs[0]); nt.nodes["Background"].inputs[1].default_value = 0.45
    sun.data.energy = 4.6; sun.data.angle = math.radians(2.5); sun.data.color = hexc("#FFE9CF")[:3]
    sun.rotation_euler = (math.radians(42), math.radians(-18), math.radians(-35))

# ---------------------------------------------------------------- kits (modelos prontos .glb, ex. Kenney CC0)
KIT = {}
def kit(path):
    if path in KIT: return KIT[path]
    before = set(bpy.data.objects)
    bpy.ops.import_scene.gltf(filepath=path)
    new = [o for o in bpy.data.objects if o not in before]
    meshes = [o for o in new if o.type == "MESH"]
    for o in new: o.select_set(False)
    for o in meshes:  # aplica a hierarquia antes de juntar
        mw = o.matrix_world.copy(); o.parent = None; o.matrix_world = mw
    if len(meshes) > 1:
        bpy.context.view_layer.objects.active = meshes[0]
        for o in meshes: o.select_set(True)
        bpy.ops.object.join()
    t = meshes[0]
    bpy.ops.object.select_all(action="DESELECT")
    t.select_set(True); bpy.context.view_layer.objects.active = t
    bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)
    for o in new:
        try:
            if o is not t and o.name in bpy.data.objects: bpy.data.objects.remove(o, do_unlink=True)
        except ReferenceError: pass
    t.parent = None; t.location = (0, 0, -999); t.hide_render = True
    for m in t.data.materials:
        if m and m.use_nodes and "Principled BSDF" in m.node_tree.nodes:
            m.node_tree.nodes["Principled BSDF"].inputs["Roughness"].default_value = 0.6
    KIT[path] = t
    return t
def place(path, loc, rz=0.0, s=1.0):
    t = kit(path)
    o = bpy.data.objects.new("kit", t.data); COLL.objects.link(o)
    o.location = loc; o.rotation_euler = (0, 0, rz); o.scale = (s, s, s) if not isinstance(s, tuple) else s
    return o

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
def text3d(name, body, size, loc, color="#222222", extrude=0.02, parent=None, rot=(0, 0, 0), font=None):
    cu = bpy.data.curves.new(name, "FONT"); cu.body = body; cu.font = font or FONT; cu.size = size
    cu.extrude = extrude; cu.align_x = "CENTER"; cu.align_y = "CENTER"
    o = bpy.data.objects.new(name, cu); COLL.objects.link(o); o.location = loc; o.rotation_euler = rot
    o.data.materials.append(M); o.color = hexc(color)
    if parent: o.parent = parent
    return o
def set_alpha_tree(root, a):
    """fade (alpha) de um objeto e de todos os filhos."""
    for o in [root] + list(root.children_recursive):
        if o.type in ("MESH", "FONT"):
            c = o.color; o.color = (c[0], c[1], c[2], a); o.hide_render = a <= 0.01
def show(o, s, base=(1, 1, 1)):
    """escala de pop (0 esconde)."""
    o.scale = tuple(max(s, 0.001) * b for b in base)
    for c in [o] + list(o.children_recursive):
        if c.type in ("MESH", "FONT"): c.hide_render = s <= 0.002

# ---------------------------------------------------------------- cenário genérico
BUILD_COLS = ["#F2F1EE", "#E9E6E0", "#DDE2E6", "#ECE5D8", "#E4E7E1", "#F0EBE3"]
GLASS = "#BCCDD9"
def building(x0, x1, y0, y1, h, face_sign, strips=True, col=None):
    w, d = x1 - x0, y1 - y0
    c = col or R.choice(BUILD_COLS)
    obj("b", "boxb", ((x0 + x1) / 2, (y0 + y1) / 2, 0), (w, d, h), c)
    obj("bt", "boxb", ((x0 + x1) / 2, (y0 + y1) / 2, h), (w + 0.12, d + 0.12, 0.18), "#D9D6CF")
    if strips and face_sign != 0:
        yf = (y0 if face_sign < 0 else y1) + face_sign * 0.03
        z = 1.2
        while z + 1.2 < h:
            obj("w", "boxb", ((x0 + x1) / 2, yf, z), (w - 0.7, 0.08, 1.05), GLASS)
            obj("l", "boxb", ((x0 + x1) / 2, yf + face_sign * 0.04, z + 1.55), (w, 0.14, 0.16), "#FAF9F6")
            z += 3.0
def tree(x, y, s=1.0):
    obj("tr", "cyl", (x, y, 0.9 * s), (0.13 * s, 0.13 * s, 1.8 * s), "#8A6A48")
    obj("tc", "ico", (x, y, 2.35 * s), (1.15 * s, 1.15 * s, 1.15 * s), R.choice(["#6DB35A", "#78BD62", "#62A851"]))
def bush(x, y, s=1.0):
    obj("bu", "ico", (x, y, 0.35 * s), (0.6 * s, 0.6 * s, 0.45 * s), R.choice(["#6DB35A", "#78BD62", "#62A851"]))

# ---------------------------------------------------------------- personagens
SHIRTS = ["#F2B33D", "#3DAA5A", "#9AA0A8", "#E8E8E8", "#3C7DD9", "#E5484D", "#F08A3C", "#7B5BD6", "#5FB7C9", "#D9D2C5"]
PANTS = ["#3B4A63", "#4A4F57", "#2F3A4F", "#6B6F78", "#8A7A63"]
SKIN = ["#EBC6A3", "#D9A57E", "#B98058", "#8D5A3B", "#F1D2B6"]
HAIR = ["#2E2420", "#4A3324", "#1C1C1C", "#6B4A2E", "#8C8C8C"]

class Person:
    def __init__(s, name, shirt=None, hat=None, cap=None, scale=1.0, pant=None, hair=None, apron=None, tie=None):
        s.root = empty(name)
        pant = pant or R.choice(PANTS); skin = R.choice(SKIN); hair = hair or R.choice(HAIR)
        shirt = shirt or R.choice(SHIRTS)
        s.parts = []; P = s.parts.append
        s.legL = obj(name + "lL", "boxt", (0.105, 0, 0.82), (0.16, 0.18, 0.82), pant, parent=s.root); P(s.legL)
        s.legR = obj(name + "lR", "boxt", (-0.105, 0, 0.82), (0.16, 0.18, 0.82), pant, parent=s.root); P(s.legR)
        P(obj(name + "t", "boxb", (0, 0, 0.8), (0.46, 0.26, 0.62), shirt, parent=s.root))
        if apron: P(obj(name + "ap", "boxb", (0, 0.135, 0.62), (0.4, 0.02, 0.7), apron, parent=s.root))
        if tie: P(obj(name + "tie", "boxb", (0, 0.135, 0.92), (0.09, 0.02, 0.48), tie, parent=s.root))
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
        s.root.scale = (scale,) * 3; s.base_scale = scale; s.vis = True
    def pose(s, x, y, z, yaw, swing, sc=1.0, armL=None, armR=None):
        vis = sc > 0.002
        if vis != s.vis:
            for p in s.parts: p.hide_render = not vis
            s.vis = vis
        if not vis: return
        s.root.location = (x, y, z); s.root.rotation_euler = (0, 0, yaw)
        k = sc * s.base_scale; s.root.scale = (k, k, k)
        s.legL.rotation_euler.x = 0.5 * swing; s.legR.rotation_euler.x = -0.5 * swing
        s.armL.rotation_euler.x = -0.38 * swing if armL is None else armL
        s.armR.rotation_euler.x = 0.38 * swing if armR is None else armR
    def hide(s): s.pose(0, 0, -50, 0, 0, 0)

def walk_pose(path, t, speed=1.25):
    """path: [(t0,(x,y)), (t1,(x,y)), ...] -> (x, y, yaw, swing). Anda entre pontos com ease."""
    if t <= path[0][0]:
        (x, y) = path[0][1]; nx, ny = path[1][1] if len(path) > 1 else (x, y + 1)
        return x, y, math.atan2(ny - y, nx - x) - math.pi / 2, 0.0
    for (ta, pa), (tb, pb) in zip(path, path[1:]):
        if ta <= t <= tb:
            k = (t - ta) / max(1e-6, tb - ta)
            x, y = lerp(pa[0], pb[0], k), lerp(pa[1], pb[1], k)
            d = math.hypot(pb[0] - pa[0], pb[1] - pa[1])
            moving = d > 0.01
            yaw = math.atan2(pb[1] - pa[1], pb[0] - pa[0]) - math.pi / 2 if moving else None
            ph = (t - ta) * (d / max(1e-6, tb - ta)) * 2 * math.pi / 1.15
            return x, y, yaw, (math.sin(ph) if moving else 0.0)
    x, y = path[-1][1]
    return x, y, None, 0.0

# ---------------------------------------------------------------- câmera
Z = (0, 0, 1)
CK = []
DOF_K = 4.0; DOF_MIN = 0.05
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
    if PREMIUM and DOF_K > 0:
        d = (Vector(tg) - loc).length
        cam_d.dof.use_dof = True; cam_d.dof.focus_distance = d
        cam_d.dof.aperture_fstop = max(DOF_MIN, min(8.0, DOF_K / d))
def face_cam(o):
    o.rotation_euler = cam.matrix_world.to_euler()

def proj(p):
    v = world_to_camera_view(sc, cam, Vector(p))
    return [round(v.x, 4), round(1 - v.y, 4), round(v.z, 3)]

def parse_frames(s):
    out = []
    for part in s.split(","):
        step = 1
        if ":" in part: part, st = part.split(":"); step = int(st)
        if "-" in part:
            a, b = part.split("-"); out += list(range(int(a), int(b) + 1, step))
        else: out.append(int(part))
    return [x for x in out if 0 <= x <= NF]

def run(apply, anchors, meta_extra=None):
    """anchors: dict nome -> função(t) -> (x,y,z) ou tupla fixa."""
    frames = parse_frames(FRAMES_ARG)
    si, sn = map(int, SHARD.split("/"))
    frames = frames[si::sn]
    if si == 0:
        meta = dict(fps=FPS, nf=NF, frames=[])
        if meta_extra: meta.update(meta_extra)
        for f in range(NF + 1):
            t = f / FPS; set_cam(t)
            d = {}
            for k, v in anchors.items():
                p = v(t) if callable(v) else v
                if p is not None: d[k] = proj(p)
            meta["frames"].append(d)
        with open(os.path.join(OUT, "meta.json"), "w") as fh: json.dump(meta, fh)
    for f in frames:
        set_cam(f / FPS)
        apply(f / FPS)
        sc.frame_current = f
        sc.render.filepath = os.path.join(OUT, f"f{f:05d}.png")
        bpy.ops.render.render(write_still=True)
        print("FRAME", f, flush=True)
    print("DONE")
