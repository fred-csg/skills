import sys as _s, os as _o
_s.path.insert(0, _o.path.dirname(_o.path.dirname(_o.path.abspath(__file__))))  # scripts/ (ambiente.py)
import ambiente
# Esquadrão Voxel — base do Blender (5.x, rodar com -b --factory-startup).
# Cada cena faz:  import vox; vox.setup(DUR, paleta="crepusculo") ... e no fim vox.run(apply)
# Motor padrão: EEVEE (rápido, sombra suave, motion blur de câmera). cycles=True = mais bonito e ~4x mais lento.
import bpy, bmesh, math, random, json, os, sys
from mathutils import Vector, Matrix
from bpy_extras.object_utils import world_to_camera_view

argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
OUT = argv[0] if len(argv) > 0 else os.path.join(os.environ.get("TEMP", "."), "vox_out")
RES = int(argv[1]) if len(argv) > 1 else 50
FRAMES_ARG = argv[2] if len(argv) > 2 else "0"
SHARD = argv[3] if len(argv) > 3 else "0/1"
os.makedirs(OUT, exist_ok=True)
FPS = 30
TEX = os.path.abspath("tex")          # texturas geradas pelo telas.py (pasta blender/tex do projeto)

# ---------------------------------------------------------------- tempo / easing
def tf(t): return int(round(t * FPS))
def clamp(a, lo=0.0, hi=1.0): return max(lo, min(hi, a))
def ease(a): a = clamp(a); return a * a * a * (a * (a * 6 - 15) + 10)
def eout(a): a = clamp(a); return 1 - (1 - a) ** 3
def ein(a): a = clamp(a); return a * a * a
def eback(a, c1=1.9):
    a = clamp(a); c3 = c1 + 1; return 1 + c3 * (a - 1) ** 3 + c1 * (a - 1) ** 2
def spring(a, f=3.2, d=5.5):
    """0→1 com mola (passa e volta)."""
    if a <= 0: return 0.0
    return 1 - math.exp(-d * a) * math.cos(f * math.pi * a)
def lerp(a, b, k): return a + (b - a) * k
def vlerp(a, b, k): return tuple(lerp(a[i], b[i], k) for i in range(len(a)))
def win(t, t0, t1, fi=0.3, fo=0.25, back=True):
    """0..1 que entra (pop) em t0 e sai em t1."""
    if t < t0 or t > t1 + fo: return 0.0
    a = (eback if back else eout)((t - t0) / fi)
    return a * (1 - eout((t - t1) / fo)) if t > t1 else a
def hexc(h, a=1.0):
    h = h.lstrip("#"); r, g, b = (int(h[i:i + 2], 16) / 255 for i in (0, 2, 4))
    lin = lambda c: c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4
    return (lin(r), lin(g), lin(b), a)

# ---------------------------------------------------------------- paletas
PALETAS = {
    # céu (topo, meio, horizonte), chão, cor do luar, cor da luz de frente, lojas
    "crepusculo": dict(ceu=("#120F2E", "#3B1F5C", "#C2566A"), piso="#77707E", rejunte="#4E4858",
                       lua="#AFC3FF", frente="#FFD9B8", amb=0.55,
                       lojas=["#2F6F73", "#6B3E73", "#C9973A", "#2E4A7A", "#A34E3B", "#3F8F6E", "#7A5A9E"]),
    "noite": dict(ceu=("#0E1430", "#1F2A5E", "#4B3A86"), piso="#6E6E78", rejunte="#474754",
                  lua="#9FB4FF", frente="#FFE6CC", amb=0.5,
                  lojas=["#2D5F8A", "#5A4636", "#1F6B5A", "#3B4F8F", "#7A3B3B", "#2F7A6A", "#4A3F7A"]),
    "manha": dict(ceu=("#7CC4F2", "#B9E1F7", "#FBE7C6"), piso="#BDB6AC", rejunte="#9A9187",
                  lua="#FFF4DE", frente="#FFFFFF", amb=0.9,
                  lojas=["#E9785F", "#5FA8D3", "#F2C14E", "#7BC67E", "#B48EE0", "#F29BB7", "#4FB3A9"]),
}
PAL = PALETAS["crepusculo"]

R = random.Random(7)
sc = bpy.context.scene
NF = 0; DUR = 0
M = None
MATS = {}
COLL = sc.collection
FONT = None
cam = cam_d = None
CYCLES = False

def _mat_base(name, rough=0.72, emit=0.0):
    m = bpy.data.materials.new(name); m.use_nodes = True
    nt = m.node_tree; P = nt.nodes["Principled BSDF"]
    oi = nt.nodes.new("ShaderNodeObjectInfo")
    nt.links.new(oi.outputs["Color"], P.inputs["Base Color"])
    nt.links.new(oi.outputs["Alpha"], P.inputs["Alpha"])
    P.inputs["Roughness"].default_value = rough
    if "Specular IOR Level" in P.inputs: P.inputs["Specular IOR Level"].default_value = 0.25
    if emit > 0:
        nt.links.new(oi.outputs["Color"], P.inputs["Emission Color"])
        P.inputs["Emission Strength"].default_value = emit
    try: m.surface_render_method = "DITHERED"
    except Exception: pass
    return m

def mat_img(path, emit=1.0, alpha=False):
    """material de tela/placa: imagem com brilho próprio (lê bem em qualquer luz)."""
    key = (path, emit)
    if key in MATS: return MATS[key]
    m = bpy.data.materials.new(os.path.basename(path)); m.use_nodes = True
    nt = m.node_tree; P = nt.nodes["Principled BSDF"]
    im = nt.nodes.new("ShaderNodeTexImage"); im.image = bpy.data.images.load(path); im.interpolation = "Cubic"
    nt.links.new(im.outputs["Color"], P.inputs["Base Color"])
    nt.links.new(im.outputs["Color"], P.inputs["Emission Color"])
    P.inputs["Emission Strength"].default_value = emit
    P.inputs["Roughness"].default_value = 0.5
    if alpha:
        nt.links.new(im.outputs["Alpha"], P.inputs["Alpha"])
        try: m.surface_render_method = "DITHERED"
        except Exception: pass
    MATS[key] = m
    return m

def setup(dur, paleta="crepusculo", cycles=False, samples=48, blur=True):
    global NF, DUR, M, FONT, cam, cam_d, PAL, CYCLES
    PAL = PALETAS[paleta] if isinstance(paleta, str) else paleta
    CYCLES = cycles
    DUR = dur; NF = int(dur * FPS)
    for o in list(bpy.data.objects): bpy.data.objects.remove(o, do_unlink=True)
    r = sc.render
    r.resolution_x, r.resolution_y = 1080, 1920
    r.resolution_percentage = RES
    r.fps = FPS
    r.image_settings.file_format = "PNG"
    r.film_transparent = False
    if cycles: _cycles(samples)
    else:
        for eng in ("BLENDER_EEVEE", "BLENDER_EEVEE_NEXT"):
            try: r.engine = eng; break
            except Exception: pass
        ee = sc.eevee
        for k, v in dict(taa_render_samples=32, use_shadows=True, use_raytracing=True, use_fast_gi=True,
                         shadow_ray_count=2, shadow_step_count=10, fast_gi_distance=3.0,
                         use_shadow_jitter_viewport=True).items():
            try: setattr(ee, k, v)
            except Exception: pass
        try: ee.ray_tracing_options.resolution_scale = "2"
        except Exception: pass
    try:
        r.use_motion_blur = blur; r.motion_blur_shutter = 0.5
    except Exception: pass
    sc.view_settings.view_transform = "Standard"
    try: sc.view_settings.look = "None"
    except Exception: pass
    _world()
    _luzes()
    M = _mat_base("M")
    MATS["glow"] = _mat_base("Mglow", 0.6, 3.0)
    _f = ambiente.achar_fonte("Poppins-Bold.ttf", "ArchivoBlack-Regular.ttf", "segoeuib.ttf", "arialbd.ttf")
    FONT = bpy.data.fonts.load(_f) if _f else bpy.data.fonts.load("<builtin>")
    cam_d = bpy.data.cameras.new("cam"); cam_d.sensor_fit = "VERTICAL"; cam_d.sensor_height = 36
    cam_d.clip_start = 0.1; cam_d.clip_end = 900
    cam = bpy.data.objects.new("cam", cam_d); COLL.objects.link(cam); sc.camera = cam

def _cycles(samples):
    sc.render.engine = "CYCLES"; cy = sc.cycles
    try:
        pr = bpy.context.preferences.addons["cycles"].preferences
        want = os.environ.get("VOX_GPU"); ok = False
        for tipo in ("OPTIX", "CUDA", "METAL", "HIP", "ONEAPI"):
            try: pr.compute_device_type = tipo
            except Exception: continue
            pr.get_devices(); k = 0
            for d in pr.devices:
                if d.type == tipo: d.use = (want is None or str(k) == want); k += 1; ok = ok or d.use
                else: d.use = False
            if ok: break
        cy.device = "GPU" if ok else "CPU"
    except Exception as e: print("GPU?", e)
    cy.samples = samples; cy.use_adaptive_sampling = True; cy.adaptive_threshold = 0.03; cy.use_denoising = True
    try: cy.denoiser = "OPTIX"
    except Exception: pass
    cy.max_bounces = 4; cy.diffuse_bounces = 2; cy.glossy_bounces = 1
    sc.render.use_persistent_data = True

def _world():
    """céu em degradê (topo→horizonte) + estrelas procedurais."""
    w = bpy.data.worlds.new("W"); sc.world = w; w.use_nodes = True
    nt = w.node_tree; N = nt.nodes; L = nt.links
    bg = N["Background"]
    tc = N.new("ShaderNodeTexCoord"); sep = N.new("ShaderNodeSeparateXYZ")
    L.new(tc.outputs["Generated"], sep.inputs[0])
    ramp = N.new("ShaderNodeValToRGB"); cr = ramp.color_ramp
    top, mid, hor = PAL["ceu"]
    cr.elements[0].position = 0.0; cr.elements[0].color = hexc(hor)
    cr.elements[1].position = 0.55; cr.elements[1].color = hexc(top)
    e = cr.elements.new(0.16); e.color = hexc(mid)
    L.new(sep.outputs["Z"], ramp.inputs[0])
    # estrelas: voronoi na direção da vista, só acima do horizonte
    vor = N.new("ShaderNodeTexVoronoi"); vor.inputs["Scale"].default_value = 260.0
    try: vor.inputs["Randomness"].default_value = 1.0
    except Exception: pass
    L.new(tc.outputs["Generated"], vor.inputs["Vector"])
    st = N.new("ShaderNodeMapRange"); st.inputs["From Min"].default_value = 0.035; st.inputs["From Max"].default_value = 0.0
    L.new(vor.outputs["Distance"], st.inputs["Value"])
    nz = N.new("ShaderNodeTexNoise"); nz.inputs["Scale"].default_value = 40.0
    L.new(tc.outputs["Generated"], nz.inputs["Vector"])
    m1 = N.new("ShaderNodeMath"); m1.operation = "MULTIPLY"; L.new(st.outputs[0], m1.inputs[0]); L.new(nz.outputs["Fac"], m1.inputs[1])
    hz = N.new("ShaderNodeMapRange"); hz.inputs["From Min"].default_value = 0.08; hz.inputs["From Max"].default_value = 0.3
    L.new(sep.outputs["Z"], hz.inputs["Value"])
    m2 = N.new("ShaderNodeMath"); m2.operation = "MULTIPLY"; L.new(m1.outputs[0], m2.inputs[0]); L.new(hz.outputs[0], m2.inputs[1])
    m3 = N.new("ShaderNodeMath"); m3.operation = "MULTIPLY"; m3.inputs[1].default_value = 2.5; L.new(m2.outputs[0], m3.inputs[0])
    mix = N.new("ShaderNodeMix"); mix.data_type = "RGBA"; mix.blend_type = "ADD"
    L.new(m3.outputs[0], mix.inputs["Factor"]); L.new(ramp.outputs["Color"], mix.inputs[6])
    mix.inputs[7].default_value = (1, 0.96, 0.9, 1)
    # câmera vê o céu puro; a luz ambiente usa o céu mais fraco
    lp = N.new("ShaderNodeLightPath")
    amb = N.new("ShaderNodeBackground"); amb.inputs["Strength"].default_value = PAL["amb"]
    L.new(ramp.outputs["Color"], amb.inputs["Color"])
    L.new(mix.outputs[2], bg.inputs["Color"]); bg.inputs["Strength"].default_value = 1.0
    ms = N.new("ShaderNodeMixShader")
    L.new(lp.outputs["Is Camera Ray"], ms.inputs[0]); L.new(amb.outputs[0], ms.inputs[1]); L.new(bg.outputs[0], ms.inputs[2])
    L.new(ms.outputs[0], N["World Output"].inputs["Surface"])

LUZES = {}
def _luzes():
    lua = bpy.data.lights.new("lua", "SUN"); lua.energy = 1.6; lua.angle = math.radians(12); lua.color = hexc(PAL["lua"])[:3]
    o = bpy.data.objects.new("lua", lua); COLL.objects.link(o); o.rotation_euler = (math.radians(55), math.radians(-25), math.radians(-28))
    fr = bpy.data.lights.new("frente", "AREA"); fr.energy = 9000; fr.size = 40; fr.color = hexc(PAL["frente"])[:3]
    o2 = bpy.data.objects.new("frente", fr); COLL.objects.link(o2); o2.location = (0, -22, 14)
    o2.rotation_euler = (math.radians(58), 0, 0)
    LUZES.update(lua=o, frente=o2)

def ponto(loc, cor="#FFC98A", energia=180, raio=0.25):
    l = bpy.data.lights.new("p", "POINT"); l.energy = energia; l.color = hexc(cor)[:3]; l.shadow_soft_size = raio
    o = bpy.data.objects.new("p", l); COLL.objects.link(o); o.location = loc
    return o

# ---------------------------------------------------------------- geometria
def _box_mesh(sx, sy, sz, bevel, z0):
    me = bpy.data.meshes.new("bx"); bm = bmesh.new()
    bmesh.ops.create_cube(bm, size=1.0)
    for v in bm.verts:
        v.co.x *= sx; v.co.y *= sy; v.co.z = v.co.z * sz + (sz / 2 if z0 else 0)
    if bevel > 0:
        bv = min(bevel, sx / 2.2, sy / 2.2, sz / 2.2)
        bmesh.ops.bevel(bm, geom=list(bm.edges), offset=bv, segments=2, affect="EDGES", profile=0.5)
    bm.to_mesh(me); bm.free()
    me.materials.append(M)
    for p in me.polygons: p.use_smooth = True
    try: me.set_sharp_from_angle(angle=math.radians(35))
    except Exception: pass
    return me

_MESH_CACHE = {}
def box(name, size, loc=(0, 0, 0), color="#FFFFFF", parent=None, bevel=0.03, z0=False, rot=(0, 0, 0), mat=None):
    """caixa com quina arredondada. size=(x,y,z). z0=True: base em z=0 (cresce pra cima)."""
    key = (round(size[0], 4), round(size[1], 4), round(size[2], 4), bevel, z0)
    if key not in _MESH_CACHE: _MESH_CACHE[key] = _box_mesh(*size, bevel, z0)
    o = bpy.data.objects.new(name, _MESH_CACHE[key]); COLL.objects.link(o)
    o.location = loc; o.rotation_euler = rot
    o.color = hexc(color) if isinstance(color, str) else color
    if parent: o.parent = parent
    if mat:
        o.material_slots[0].link = "OBJECT"; o.material_slots[0].material = mat
    return o

def _prim(kind, **kw):
    me = bpy.data.meshes.new(kind); bm = bmesh.new()
    if kind == "cyl": bmesh.ops.create_cone(bm, cap_ends=True, cap_tris=False, segments=kw.get("seg", 24), radius1=1, radius2=1, depth=1)
    elif kind == "cone": bmesh.ops.create_cone(bm, cap_ends=True, cap_tris=False, segments=kw.get("seg", 16), radius1=1, radius2=0, depth=1)
    elif kind == "sph": bmesh.ops.create_uvsphere(bm, u_segments=24, v_segments=14, radius=1)
    elif kind == "dome":
        bmesh.ops.create_uvsphere(bm, u_segments=24, v_segments=14, radius=1)
        bmesh.ops.delete(bm, geom=[v for v in bm.verts if v.co.z < -1e-4], context="VERTS")
        bmesh.ops.holes_fill(bm, edges=bm.edges)
    elif kind == "torus":
        bmesh.ops.create_circle(bm, segments=1, radius=1)
        bm.clear()
        R0, r0, n, m = 1.0, kw.get("r", 0.18), 28, 10
        rings = []
        for i in range(n):
            a = 2 * math.pi * i / n; ring = []
            for j in range(m):
                b = 2 * math.pi * j / m
                ring.append(bm.verts.new(((R0 + r0 * math.cos(b)) * math.cos(a), (R0 + r0 * math.cos(b)) * math.sin(a), r0 * math.sin(b))))
            rings.append(ring)
        for i in range(n):
            for j in range(m):
                bm.faces.new((rings[i][j], rings[(i + 1) % n][j], rings[(i + 1) % n][(j + 1) % m], rings[i][(j + 1) % m]))
    bm.to_mesh(me); bm.free(); me.materials.append(M)
    for p in me.polygons: p.use_smooth = True
    return me
_PRIM = {}
def prim(kind, name, loc, scale, color, parent=None, rot=(0, 0, 0), mat=None, **kw):
    k = (kind, tuple(sorted(kw.items())))
    if k not in _PRIM: _PRIM[k] = _prim(kind, **kw)
    o = bpy.data.objects.new(name, _PRIM[k]); COLL.objects.link(o)
    o.location = loc; o.scale = scale; o.rotation_euler = rot
    o.color = hexc(color) if isinstance(color, str) else color
    if parent: o.parent = parent
    if mat: o.material_slots[0].link = "OBJECT"; o.material_slots[0].material = mat
    return o

def empty(name, loc=(0, 0, 0), parent=None):
    e = bpy.data.objects.new(name, None); COLL.objects.link(e); e.location = loc
    if parent: e.parent = parent
    return e

def text3d(name, body, size, loc, color="#222222", extrude=0.01, parent=None, rot=(math.pi / 2, 0, 0), font=None):
    """texto em pé, virado pra -Y (pra câmera)."""
    cu = bpy.data.curves.new(name, "FONT"); cu.body = body; cu.font = font or FONT; cu.size = size
    cu.extrude = extrude; cu.align_x = "CENTER"; cu.align_y = "CENTER"
    o = bpy.data.objects.new(name, cu); COLL.objects.link(o); o.location = loc; o.rotation_euler = rot
    o.data.materials.append(M); o.color = hexc(color)
    if parent: o.parent = parent
    return o

def painel(name, img, w, h, loc, parent=None, emit=1.0, rot=(0, 0, 0), alpha=False):
    """plano em pé (face pra -Y) com uma imagem (tela, placa, letreiro)."""
    me = bpy.data.meshes.new(name); bm = bmesh.new()
    vs = [bm.verts.new((x * w / 2, 0, z * h / 2)) for x, z in ((-1, -1), (1, -1), (1, 1), (-1, 1))]
    f = bm.faces.new(vs); uv = bm.loops.layers.uv.new()
    for lo, (u, v) in zip(f.loops, ((0, 0), (1, 0), (1, 1), (0, 1))): lo[uv].uv = (u, v)
    bmesh.ops.reverse_faces(bm, faces=[f])  # normal pra -Y
    bm.to_mesh(me); bm.free()
    me.materials.append(mat_img(img if os.path.isabs(img) else os.path.join(TEX, img), emit, alpha))
    o = bpy.data.objects.new(name, me); COLL.objects.link(o); o.location = loc; o.rotation_euler = rot
    if parent: o.parent = parent
    return o

def show(o, s, base=None):
    """escala de pop (0 esconde) de um objeto e filhos."""
    base = base or (1, 1, 1)
    o.scale = tuple(max(s, 0.0005) * b for b in base)
    for c in [o] + list(o.children_recursive):
        if c.type in ("MESH", "FONT"): c.hide_render = s <= 0.002

# ---------------------------------------------------------------- câmera (planos com corte seco ou chicote)
# CAM = [(t_inicio, pos, alvo, lente, "corte"|"chicote"|"suave"), ...]  — cada item começa um plano;
# dentro do plano a câmera vai de pos/alvo até o próximo "deriva" (empurrão lento) definido por DRIFT.
CAM = []
DRIFT = 0.10          # fração que a câmera avança em direção ao alvo durante o plano (push-in lento)
WHIP = 0.30           # duração do chicote (s)
def _plano(i, t):
    t0, p, a, ln, _ = CAM[i]
    t1 = CAM[i + 1][0] if i + 1 < len(CAM) else DUR
    k = ease((t - t0) / max(0.01, t1 - t0)) if t1 > t0 else 0
    p = Vector(p); a = Vector(a)
    return tuple(p + (a - p) * DRIFT * k), tuple(a), ln * (1 + 0.04 * k)
def cam_at(t):
    i = 0
    for j, c in enumerate(CAM):
        if t >= c[0]: i = j
    p, a, ln = _plano(i, t)
    if i + 1 < len(CAM) and CAM[i + 1][4] == "chicote" and t > CAM[i + 1][0] - WHIP / 2:
        # chicote: sai rápido do plano atual pro próximo (com motion blur real)
        tn = CAM[i + 1][0]; k = ein((t - (tn - WHIP / 2)) / (WHIP / 2))
        p2, a2, l2 = _plano(i + 1, tn)
        return vlerp(p, p2, k * 0.5), vlerp(a, a2, k * 0.5), lerp(ln, l2, k * 0.5)
    if CAM[i][4] == "chicote" and t < CAM[i][0] + WHIP / 2 and i > 0:
        tp = CAM[i][0]; k = 0.5 + 0.5 * eout((t - tp) / (WHIP / 2))
        p0, a0, l0 = _plano(i - 1, tp)
        return vlerp(p0, p, k), vlerp(a0, a, k), lerp(l0, ln, k)
    if CAM[i][4] == "suave" and i > 0:
        tp = CAM[i][0]; d = 0.9
        if t < tp + d:
            k = ease((t - tp) / d); p0, a0, l0 = _plano(i - 1, tp)
            return vlerp(p0, p, k), vlerp(a0, a, k), lerp(l0, ln, k)
    return p, a, ln
SHAKE = []   # [(t, força)] — tranco de câmera (impacto)
def set_cam(t):
    loc, tg, lens = cam_at(t)
    loc = Vector(loc); tg = Vector(tg)
    for (ts, f) in SHAKE:
        if ts <= t < ts + 0.35:
            k = (1 - (t - ts) / 0.35) * f
            loc += Vector((math.sin(t * 90) * 0.04 * k, 0, math.cos(t * 77) * 0.04 * k))
    f = (tg - loc).normalized(); up = Vector((0, 0, 1))
    r = f.cross(up); r.normalize(); u = r.cross(f)
    m = Matrix(((r.x, u.x, -f.x), (r.y, u.y, -f.y), (r.z, u.z, -f.z)))
    cam.matrix_world = Matrix.Translation(loc) @ m.to_4x4()
    cam_d.lens = lens
    d = (tg - loc).length
    cam_d.dof.use_dof = True; cam_d.dof.focus_distance = d
    cam_d.dof.aperture_fstop = max(0.9, min(8.0, d / 2.2))

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

def run(apply, anchors=None, meta_extra=None):
    """apply(t) posiciona tudo no tempo t. anchors: nome -> função(t)->(x,y,z) (vira meta.json pro overlay)."""
    frames = parse_frames(FRAMES_ARG)
    si, sn = map(int, SHARD.split("/"))
    frames = frames[si::sn]
    if si == 0:
        meta = dict(fps=FPS, nf=NF, frames=[])
        if meta_extra: meta.update(meta_extra)
        for f in range(NF + 1):
            t = f / FPS; set_cam(t); d = {}
            for k, v in (anchors or {}).items():
                p = v(t) if callable(v) else v
                if p is not None: d[k] = proj(p)
            meta["frames"].append(d)
        with open(os.path.join(OUT, "meta.json"), "w") as fh: json.dump(meta, fh)
    for f in frames:
        t = f / FPS
        set_cam(t); apply(t)
        sc.frame_current = f
        sc.render.filepath = os.path.join(OUT, f"f{f:05d}.png")
        bpy.ops.render.render(write_still=True)
        print("FRAME", f, flush=True)
    print("DONE")
