# Esquadrão Voxel — peças de cenário. Cada personagem ganha uma "sala" (set) com cor dominante própria.
#   sala(cx, parede="#2F6F73", piso="madeira"|"azulejo"|"carpete", larg=9, prof=7, alt=6, fundo=None)
#   mesa(...), notebook(...), monitor(...), quadro(...), neon(...), luminaria(...), planta(...), estante(...)
import math, random
import vox
from vox import box, prim, empty, painel, ponto, hexc

R = random.Random(11)

def _tom(h, k):
    """clareia (k>0) ou escurece (k<0) uma cor hex."""
    h = h.lstrip("#"); c = [int(h[i:i + 2], 16) for i in (0, 2, 4)]
    c = [max(0, min(255, int(v + (255 - v) * k if k > 0 else v * (1 + k)))) for v in c]
    return "#%02X%02X%02X" % tuple(c)

def piso(cx, cy, larg, prof, tipo="madeira", cor=None):
    if tipo == "madeira":
        base = cor or "#9A6A44"; w = 0.42
        n = int(larg / w) + 1
        for i in range(n):
            x = cx - larg / 2 + (i + 0.5) * w
            # tábuas com emenda em alturas diferentes
            cut = R.uniform(0.2, 0.8) * prof
            for (y0, y1) in ((0, cut), (cut, prof)):
                box("tabua", (w - 0.02, (y1 - y0) - 0.02, 0.1), (x, cy - prof / 2 + (y0 + y1) / 2, -0.1),
                    _tom(base, R.uniform(-0.12, 0.08)), bevel=0.012, z0=True)
    elif tipo == "azulejo":
        base = cor or vox.PAL["piso"]; w = 0.9
        nx, ny = int(larg / w) + 1, int(prof / w) + 1
        box("rejunte", (larg + 1, prof + 1, 0.1), (cx, cy, -0.12), vox.PAL["rejunte"], bevel=0, z0=True)
        for i in range(nx):
            for j in range(ny):
                box("az", (w - 0.05, w - 0.05, 0.1), (cx - larg / 2 + (i + 0.5) * w, cy - prof / 2 + (j + 0.5) * w, -0.1),
                    _tom(base, R.uniform(-0.06, 0.06)), bevel=0.02, z0=True)
    else:  # carpete liso
        box("carpete", (larg, prof, 0.1), (cx, cy, -0.1), cor or "#3A3650", bevel=0.02, z0=True)

def sala(cx, parede="#2F6F73", piso_tipo="madeira", larg=9.0, prof=7.0, alt=6.0, cor_piso=None, fundo=None,
         rodape=True, lateral=True, luz=None):
    """set de um personagem centrado em (cx, 0). Parede no fundo (y = prof/2). Câmera fica em -Y.
    fundo: imagem (ex. janela da cidade) aplicada na parede."""
    cy = 0.0; yb = cy + prof / 2
    piso(cx, cy, larg, prof, piso_tipo, cor_piso)
    box("parede", (larg, 0.3, alt), (cx, yb + 0.15, 0), parede, bevel=0.0, z0=True)
    if lateral:
        for s in (-1, 1):
            box("lat", (0.3, prof, alt), (cx + s * (larg / 2 + 0.15), cy, 0), _tom(parede, -0.18), bevel=0, z0=True)
    if rodape:
        box("rodape", (larg, 0.08, 0.22), (cx, yb - 0.02, 0), _tom(parede, -0.3), bevel=0.01, z0=True)
    # faixa de textura na parede (painéis verticais) — dá leitura de profundidade
    for i in range(int(larg / 1.2)):
        x = cx - larg / 2 + 0.6 + i * 1.2
        box("ripa", (0.06, 0.05, alt - 0.5), (x, yb - 0.02, 0.22), _tom(parede, -0.08), bevel=0.01, z0=True)
    if fundo:
        fw, fh = fundo[1], fundo[2]
        box("moldura", (fw + 0.3, 0.12, fh + 0.3), (cx, yb - 0.06, fundo[3] + fh / 2), "#1A1724", bevel=0.03)
        painel("fundo", fundo[0], fw, fh, (cx, yb - 0.13, fundo[3] + fh / 2), emit=1.1)
    if luz:
        ponto((cx, cy - 1, alt - 0.6), luz, 900, 1.5)

def mesa(x, y, w=2.6, d=1.3, h=0.9, cor="#8A5A3A", pes="#5A3A26"):
    box("tampo", (w, d, 0.1), (x, y, h - 0.1), cor, bevel=0.03, z0=True)
    for sx in (-1, 1):
        for sy in (-1, 1):
            box("pe", (0.1, 0.1, h - 0.1), (x + sx * (w / 2 - 0.12), y + sy * (d / 2 - 0.12), 0), pes, bevel=0.02, z0=True)
    return h

def notebook(x, y, z, larg=4.6, tela_img=None, cor="#2B2A33", inclina=0.18):
    """notebook (pode ser gigante: os bonecos saem de dentro da tela)."""
    alt = larg * 0.64; prof = larg * 0.68
    base = box("nb_base", (larg, prof, 0.14), (x, y, z), cor, bevel=0.05, z0=True)
    box("nb_teclado", (larg * 0.88, prof * 0.52, 0.02), (x, y - prof * 0.06, z + 0.14), "#1C1B22", bevel=0.01, z0=True)
    # teclas
    for i in range(14):
        for j in range(5):
            box("tecla", (larg * 0.88 / 14 - 0.05, prof * 0.52 / 5 - 0.05, 0.03),
                (x - larg * 0.44 + (i + 0.5) * larg * 0.88 / 14, y - prof * 0.32 + (j + 0.5) * prof * 0.52 / 5, z + 0.15),
                "#3A3946", bevel=0.01, z0=True)
    box("touch", (larg * 0.3, prof * 0.2, 0.02), (x, y - prof * 0.38, z + 0.14), "#34333E", bevel=0.01, z0=True)
    tampa = empty("nb_tampa", (x, y + prof / 2 - 0.05, z + 0.12))
    tampa.rotation_euler = (-inclina, 0, 0)
    box("nb_tampa_box", (larg, 0.12, alt), (0, 0, 0), cor, tampa, 0.05, z0=True)
    if tela_img:
        painel("nb_tela", tela_img, larg * 0.93, alt * 0.9, (0, -0.07, alt * 0.5), tampa, emit=1.2)
    return dict(tampa=tampa, topo_teclado=z + 0.17, prof=prof, alt=alt)

def monitor(x, y, z, w=2.4, h=1.4, img=None, cor="#1D1B24", pe=True):
    g = empty("mon", (x, y, z))
    box("mon_caixa", (w + 0.14, 0.12, h + 0.14), (0, 0, h / 2 + (0.45 if pe else 0)), cor, g, 0.04)
    if img: painel("mon_tela", img, w, h, (0, -0.065, h / 2 + (0.45 if pe else 0)), g, emit=1.2)
    if pe:
        box("mon_pe", (0.12, 0.12, 0.45), (0, 0.05, 0), cor, g, 0.02, z0=True)
        box("mon_base", (0.7, 0.4, 0.05), (0, 0.05, 0), cor, g, 0.02, z0=True)
    return g

def quadro(x, y, z, w, h, img, moldura="#7A4E2D"):
    box("q_moldura", (w + 0.2, 0.1, h + 0.2), (x, y, z + h / 2), moldura, bevel=0.03)
    return painel("q", img, w, h, (x, y - 0.055, z + h / 2), emit=1.0)

def neon(x, y, z, w, h, img, cor="#C6F432", energia=500):
    p = painel("neon", img, w, h, (x, y, z), emit=2.6, alpha=True)
    ponto((x, y - 0.8, z), cor, energia, 1.2)
    return p

def luminaria(x, y, z=0.0, cor="#2F6F5A", luz="#FFD58A"):
    box("lum_base", (0.3, 0.3, 0.05), (x, y, z), cor, bevel=0.02, z0=True)
    box("lum_haste", (0.05, 0.05, 0.6), (x, y, z), "#C9C2B4", bevel=0.01, z0=True)
    prim("cone", "lum_cup", (x, y, z + 0.72), (0.28, 0.28, 0.25), cor)
    prim("sph", "lum_bulbo", (x, y, z + 0.6), (0.08, 0.08, 0.08), luz, mat=vox.MATS["glow"])
    ponto((x, y, z + 0.5), luz, 60, 0.2)

def planta(x, y, z=0.0, s=1.0):
    box("vaso", (0.36 * s, 0.36 * s, 0.38 * s), (x, y, z), "#C9603E", bevel=0.03, z0=True)
    for i in range(6):
        a = i * 1.05
        box("folha", (0.12 * s, 0.05 * s, 0.5 * s), (x + 0.08 * s * math.cos(a), y + 0.08 * s * math.sin(a), z + 0.38 * s),
            R.choice(["#4FA35A", "#5DB86A", "#3F8F4E"]), bevel=0.02, z0=True, rot=(0.35 * math.sin(a), 0.35 * math.cos(a), a))

def caneca(x, y, z, cor="#FFFFFF"):
    prim("cyl", "caneca", (x, y, z + 0.12), (0.11, 0.11, 0.24), cor)
    box("alca", (0.05, 0.04, 0.12), (x + 0.13, y, z + 0.12), cor, bevel=0.01)

def estante(x, y, w=1.6, h=2.4, cor="#6B4A2E"):
    box("est", (w, 0.45, h), (x, y, 0), cor, bevel=0.03, z0=True)
    cores = ["#E5484D", "#3C7DD9", "#F2C14E", "#3DAA5A", "#7B5BD6", "#F08A3C", "#E9E4F2"]
    for k in range(4):
        zz = 0.15 + k * (h - 0.2) / 4
        box("prat", (w - 0.1, 0.4, 0.04), (x, y - 0.04, zz), _tom(cor, -0.3), bevel=0.005, z0=True)
        xx = x - w / 2 + 0.12
        while xx < x + w / 2 - 0.15:
            bw = R.uniform(0.08, 0.14); bh = R.uniform(0.32, 0.48)
            box("livro", (bw, 0.3, bh), (xx + bw / 2, y - 0.06, zz + 0.04), R.choice(cores), bevel=0.01, z0=True)
            xx += bw + 0.015

def pedestal(x, y, h, cor="#F2C14E", texto=None):
    box("pedestal", (1.3, 1.1, h), (x, y, 0), cor, bevel=0.05, z0=True)
    if texto: vox.text3d("ped_t", texto, 0.35, (x, y - 0.56, h * 0.5), "#16131F", 0.01)

def tripe_mic(x, y, h=1.35, cor="#24212D"):
    box("tri_base", (0.5, 0.5, 0.05), (x, y, 0), cor, bevel=0.02, z0=True)
    box("tri_haste", (0.05, 0.05, h), (x, y, 0), cor, bevel=0.01, z0=True)
    prim("sph", "tri_mic", (x, y - 0.05, h + 0.08), (0.12, 0.12, 0.16), "#AEB4BE")
    box("tri_pop", (0.32, 0.02, 0.32), (x, y - 0.25, h + 0.08), "#3A3946", bevel=0.02)

def botao_grande(x, y, z, cor="#3DDC84"):
    box("bt_base", (0.7, 0.7, 0.2), (x, y, z), "#2B2A33", bevel=0.04, z0=True)
    cap = prim("cyl", "bt_cap", (x, y, z + 0.28), (0.26, 0.26, 0.16), cor)
    ponto((x, y - 0.3, z + 0.7), cor, 6, 0.2)
    return cap
