import sys as _s, os as _o
_s.path.insert(0, _o.path.dirname(_o.path.dirname(_o.path.abspath(__file__))))  # scripts/ (ambiente.py)
import ambiente
# Títulos de capítulo como placas 3D dentro da cena (presas à câmera, entram girando como uma placa).
# uso: P = titulos3d.Placas([(t0, t1, n, kicker, titulo, sub, cor_hex), ...]); no apply(t): P.update(t)
import bpy, bmesh, math
from mathutils import Vector, Euler, Matrix
import mvb
from mvb import hexc, ease, eout, eback

def _curve(name, body, size, font, align="LEFT", extrude=0.02, bevel=0.004):
    cu = bpy.data.curves.new(name, "FONT"); cu.body = body; cu.font = font; cu.size = size
    cu.extrude = extrude; cu.bevel_depth = bevel; cu.bevel_resolution = 2
    cu.align_x = align; cu.align_y = "CENTER"
    o = bpy.data.objects.new(name, cu); mvb.COLL.objects.link(o)
    return o

def _rounded_plate(name, w, h, d, r, seg=10):
    """retângulo de cantos arredondados (contorno 2D extrudado em z)."""
    pts = []
    for cx, cy, a0 in ((w / 2 - r, h / 2 - r, 0), (-w / 2 + r, h / 2 - r, 90), (-w / 2 + r, -h / 2 + r, 180), (w / 2 - r, -h / 2 + r, 270)):
        for k in range(seg + 1):
            a = math.radians(a0 + 90 * k / seg); pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    me = bpy.data.meshes.new(name); bm = bmesh.new()
    vs = [bm.verts.new((x, y, -d / 2)) for x, y in pts]; f = bm.faces.new(vs)
    res = bmesh.ops.extrude_face_region(bm, geom=[f])
    for v in [e for e in res["geom"] if isinstance(e, bmesh.types.BMVert)]: v.co.z += d
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    bm.to_mesh(me); bm.free()
    try: me.shade_smooth(); me.set_sharp_from_angle(angle=math.radians(30))
    except Exception: pass
    o = bpy.data.objects.new(name, me); mvb.COLL.objects.link(o)
    return o

class Placas:
    W = 2.6; H = 0.95
    def __init__(s, items, big=None):
        s.mat = mvb.make_mat("Mtit", 0.45, 0.35, bevel=0.0, grain=0.0)
        def _ld(*nomes):
            f = ambiente.achar_fonte(*nomes)
            return bpy.data.fonts.load(f) if f else bpy.data.fonts.load("<builtin>")
        s.fB = _ld("seguibl.ttf", "Poppins-Black.ttf", "ariblk.ttf", "Arial Black.ttf")
        s.fS = _ld("segoeuib.ttf", "Poppins-Bold.ttf", "arialbd.ttf", "Arial Bold.ttf")
        s.fR = _ld("segoeui.ttf", "Poppins-Regular.ttf", "arial.ttf", "Arial.ttf")
        s.items = []
        for (t0, t1, n, kicker, title, sub, col) in items:
            root = bpy.data.objects.new("placa", None); mvb.COLL.objects.link(root)
            parts = []
            def add(o, color):
                o.parent = root
                if o.type == "MESH" or o.type == "FONT":
                    if o.type == "FONT": o.data.materials.append(s.mat)
                    else: o.data.materials.clear(); o.data.materials.append(s.mat)
                o.color = hexc(color); parts.append(o); return o
            W, H = s.W, s.H
            plate = add(_rounded_plate("placa_base", W, H, 0.12, 0.22), "#FFFFFF")
            if n:
                disc = bpy.data.objects.new("disc", mvb.ME["cyl24"]); mvb.COLL.objects.link(disc)
                add(disc, col); disc.location = (-W / 2 + 0.47, 0, 0.09); disc.scale = (0.33, 0.33, 0.07); disc.rotation_euler = (0, 0, 0)
                num = add(_curve("num", n, 0.48, s.fB, "CENTER", 0.03), "#FFFFFF"); num.location = (-W / 2 + 0.47, -0.02, 0.13)
                x0 = -W / 2 + 1.1
            else:
                x0 = -W / 2 + 1.1
            k = add(_curve("kicker", kicker, 0.13, s.fS, "LEFT", 0.008), col); k.location = (x0, 0.28, 0.07)
            tt = add(_curve("titulo", title, 0.3, s.fB, "LEFT", 0.02), "#1E1E22"); tt.location = (x0 - 0.01, 0.02, 0.07)
            sb = add(_curve("sub", sub, 0.14, s.fS, "LEFT", 0.008), "#4A4A55"); sb.location = (x0, -0.28, 0.07)
            # ajusta a largura do título pra caber
            bpy.context.view_layer.update()
            tw = tt.dimensions.x
            if tw > W - (x0 + W / 2) - 0.15:
                f = (W - (x0 + W / 2) - 0.15) / tw; tt.scale = (f, f, 1)
            sw = sb.dimensions.x
            if sw > W - (x0 + W / 2) - 0.15:
                f = (W - (x0 + W / 2) - 0.15) / sw; sb.scale = (f, f, 1)
            s.items.append((t0, t1, root, parts))

    def update(s, t):
        cam = mvb.cam; cd = mvb.cam_d
        for (t0, t1, root, parts) in s.items:
            if t < t0 - 0.01 or t > t1 + 0.45:
                for p in parts: p.hide_render = True
                continue
            kin = eback((t - t0) / 0.55); kout = ease((t - t1) / 0.4) if t > t1 else 0.0
            vis = kin > 0.01 and kout < 0.99
            for p in parts: p.hide_render = not vis
            if not vis: continue
            d = 2.6
            w = min(kin, 1.0) * (1 - kout)
            if cd.dof.use_dof: cd.dof.focus_distance = cd.dof.focus_distance + (d - cd.dof.focus_distance) * w
            lens = cd.lens
            halfw = d * 10.125 / lens; halfh = d * 18.0 / lens
            sc = (2 * halfw * 0.86) / s.W
            local = Vector((0.0, halfh * 0.28, -d))
            rot = Euler((0.06 * math.sin(t * 1.3), (1 - min(kin, 1.0)) * -1.45 + kout * 1.45 + 0.05 * math.sin(t * 0.9), 0.0), "XYZ")
            m = cam.matrix_world @ Matrix.Translation(local) @ rot.to_matrix().to_4x4()
            root.matrix_world = m
            k = sc * (0.7 + 0.3 * min(kin, 1.0)) * (1 - 0.3 * kout)
            root.scale = (k, k, k)
