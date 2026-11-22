# Catálogo do elenco próprio: 1 retrato quadrado por personagem (quadro i = personagem i) + foto de grupo.
#   blender -b --factory-startup --python retratos.py -- <saida> 100 "0-18"        (retratos)
#   blender -b --factory-startup --python retratos.py -- <saida> 100 "19" grupo    (grupo, 16:9)
import sys, os
sys.path.insert(0, os.path.expanduser(r"~\.claude\skills\esquadrao-voxel\scripts\molde"))
import math, bpy, vox, bonecos as B
from vox import box, prim

GRUPO = "grupo" in sys.argv
TIPOS = list(B.ELENCO.keys())
N = len(TIPOS)
vox.PALETAS["manha"]["amb"] = 0.75
vox.setup((N + 3) / vox.FPS, paleta="manha")
vox.PAL["acento"] = "#C6F432"
vox.DRIFT = 0.0
sc = bpy.context.scene
if GRUPO: sc.render.resolution_x, sc.render.resolution_y = 1920, 1080
else: sc.render.resolution_x, sc.render.resolution_y = 1080, 1080
vox.LUZES["frente"].data.energy = 3200
vox.LUZES["lua"].data.energy = 2.4
FUNDOS = ["#F6D9C8", "#DCD6F2", "#E4EBCF", "#CFE3EE", "#F5E0B8", "#F2D0D6", "#D7EEDC", "#F4E6C9", "#CFEDEA",
          "#DCE8F7", "#E9E3D6", "#F3E3C3", "#DADCE6", "#E8DDF5", "#E6E1DA", "#E3E6EA", "#D3DDF0", "#F6D3CC", "#E0E8CC"]
GESTO = dict(pista="mostra2", novato="acena", voce="acena")
bons = []
for i, t in enumerate(TIPOS):
    x = i * 14
    box("fundo", (9, 0.3, 7), (x, 2.2, -0.5), FUNDOS[i % len(FUNDOS)], bevel=0, z0=True)
    box("chao", (9, 6, 0.2), (x, -0.8, -0.2), FUNDOS[i % len(FUNDOS)], bevel=0, z0=True)
    prim("cyl", "pedestal", (x, 0, -0.04), (0.85, 0.85, 0.08), "#FFFFFF")
    b = B.elenco(t, t); b.trilha = [(0, (x, 0), 0.0)]; b.pisca = []
    b.gesto(GESTO.get(t, "mostra"), -5, 999)
    bons.append(b)
    vox.CAM.append((i / vox.FPS, (x + 0.85, -3.35, 1.5), (x + 0.05, 0, 0.82), 55, "corte"))
# grupo: duas fileiras com todo mundo
GX = -60
if GRUPO:
    box("g_fundo", (30, 0.3, 12), (GX, 4.0, -0.5), "#F3E9D8", bevel=0, z0=True)
    box("g_chao", (30, 12, 0.2), (GX, -1, -0.2), "#EDE1CC", bevel=0, z0=True)
    for k, t in enumerate(TIPOS):
        fila = 0 if k < 10 else 1
        n = 10 if fila == 0 else N - 10
        j = k if fila == 0 else k - 10
        px = GX + (j - (n - 1) / 2) * 1.25 + (0.6 if fila else 0)
        py = 0.0 if fila == 0 else 1.6
        g = B.elenco("g" + t, t); g.trilha = [(0, (px, py), 0.0)]; g.pisca = []
        g.gesto(GESTO.get(t, "mostra"), -5, 999)
        if fila: g.chao = [(0, 0.95)]; box("degrau", (14, 1.3, 0.95), (GX + 0.6, 1.6, 0), "#E0D2B8", bevel=0.03, z0=True)
        bons.append(g)
    vox.CAM.append(((N + 0) / vox.FPS, (GX, -10.8, 1.9), (GX, 0.7, 1.15), 50, "corte"))
def apply(t):
    for b in bons: b.update(t)
vox.run(apply)
