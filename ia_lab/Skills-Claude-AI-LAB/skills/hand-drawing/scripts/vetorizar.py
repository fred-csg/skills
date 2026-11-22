"""Hand Drawing — transforma um doodle (imagem de traço preto + detalhes coloridos, fundo branco)
em "arte desenhável": a mão percorre o esqueleto dos traços e revela a imagem por baixo.

uso: python -I vetorizar.py <imagem.png> <pasta_projeto> <nome> [--max 900] [--sem-acc]

Gera em <pasta_projeto>/artes/:
  <nome>_ink.png  (traço escuro, branco + alfa → tingido com a cor do tema)
  <nome>_acc.png  (detalhes coloridos → cor de destaque do tema)
  artes.js        (window.HD_ARTES[nome] = {w, h, largura, ink, acc, tracos:[{pts, cor}]})
No roteiro: c.arte('<nome>', {x, y, w, at, dur})
"""
import json, os, sys
import numpy as np
from PIL import Image
from scipy.ndimage import distance_transform_edt, binary_dilation
from skimage.morphology import skeletonize, remove_small_objects

args = sys.argv[1:]
def opt(n, d=None, flag=False):
    if n in args:
        i = args.index(n)
        if flag: del args[i]; return True
        v = args[i + 1]; del args[i:i + 2]; return v
    return d
MAX = int(opt("--max", 900)); SEM_ACC = opt("--sem-acc", flag=True)
src, proj, nome = args
out = os.path.join(proj, "artes"); os.makedirs(out, exist_ok=True)

im = Image.open(src).convert("RGB")
s = MAX / max(im.size)
if s < 1: im = im.resize((round(im.width * s), round(im.height * s)), Image.LANCZOS)
a = np.asarray(im).astype(float)
lum = a @ [.299, .587, .114]
sat = a.max(2) - a.min(2)

acc_a = np.zeros_like(lum) if SEM_ACC else np.clip((sat - 45) / 70, 0, 1) * (lum > 50)
ink_a = np.clip((205 - lum) / 125, 0, 1) * (1 - acc_a)
ink_b, acc_b = ink_a > .45, acc_a > .45
tudo = remove_small_objects(ink_b | acc_b, max_size=24)
ink_b &= tudo; acc_b &= tudo
ink_a *= binary_dilation(tudo, iterations=2); acc_a *= binary_dilation(tudo, iterations=2)

# recorte na área com conteúdo
ys, xs = np.nonzero(tudo)
pad = 16
y0, y1 = max(0, ys.min() - pad), min(lum.shape[0], ys.max() + pad + 1)
x0, x1 = max(0, xs.min() - pad), min(lum.shape[1], xs.max() + pad + 1)
crop = lambda m: m[y0:y1, x0:x1]
ink_a, acc_a, ink_b, acc_b, tudo = map(crop, (ink_a, acc_a, ink_b, acc_b, tudo))
H, W = tudo.shape

def salvar(alpha, arq):
    rgba = np.zeros((H, W, 4), np.uint8); rgba[..., :3] = 255; rgba[..., 3] = (alpha * 255).astype(np.uint8)
    Image.fromarray(rgba).save(os.path.join(out, arq))
salvar(ink_a, f"{nome}_ink.png")
tem_acc = acc_b.sum() > 30
if tem_acc: salvar(acc_a, f"{nome}_acc.png")

# ---- esqueleto → polilinhas ----
sk = skeletonize(tudo)
dist = distance_transform_edt(tudo)
largura = float(np.median(dist[sk]) * 2) if sk.any() else 6.0
P = set(zip(*np.nonzero(sk)))
N8 = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
viz = {p: [(p[0] + dy, p[1] + dx) for dy, dx in N8 if (p[0] + dy, p[1] + dx) in P] for p in P}
grau = {p: len(v) for p, v in viz.items()}
usadas = set()
def aresta(p, q): return (p, q) if p < q else (q, p)
def andar(p, q):
    linha = [p, q]; usadas.add(aresta(p, q))
    while grau[q] == 2:
        nxt = [r for r in viz[q] if aresta(q, r) not in usadas]
        if not nxt: break
        p, q = q, nxt[0]; usadas.add(aresta(p, q)); linha.append(q)
    return linha
linhas = []
for ordem in ([p for p in P if grau[p] == 1], [p for p in P if grau[p] >= 3], list(P)):
    for p in sorted(ordem):
        for q in viz[p]:
            if aresta(p, q) not in usadas: linhas.append(andar(p, q))

def rdp(pts, eps=1.3):
    if len(pts) < 3: return pts
    a, b = np.array(pts[0], float), np.array(pts[-1], float)
    ab = b - a; n = np.hypot(*ab) or 1
    d = [abs(ab[0] * (p[1] - a[1]) - ab[1] * (p[0] - a[0])) / n for p in pts[1:-1]]
    i = int(np.argmax(d)) + 1
    return rdp(pts[:i + 1], eps)[:-1] + rdp(pts[i:], eps) if d[i - 1] > eps else [pts[0], pts[-1]]

def comp(l): return sum(np.hypot(l[i + 1][0] - l[i][0], l[i + 1][1] - l[i][1]) for i in range(len(l) - 1))

# junta pedaços que se encostam (menos levantadas de caneta)
linhas = [l for l in linhas if len(l) >= 2]
mudou = True
while mudou:
    mudou = False
    for i in range(len(linhas)):
        for j in range(i + 1, len(linhas)):
            A, B = linhas[i], linhas[j]
            for ra in (False, True):
                for rb in (False, True):
                    a_ = A[::-1] if ra else A; b_ = B[::-1] if rb else B
                    if max(abs(a_[-1][0] - b_[0][0]), abs(a_[-1][1] - b_[0][1])) <= 1:
                        linhas[i] = a_ + b_[1:]; del linhas[j]; mudou = True; break
                if mudou: break
            if mudou: break
        if mudou: break

tracos = []
for l in linhas:
    if comp(l) < max(4, largura * .6): continue
    cor = "acc" if tem_acc and np.mean([acc_b[y, x] for y, x in l]) > .5 else "ink"
    pts = [[int(x), int(y)] for y, x in rdp(l)]
    tracos.append({"pts": pts, "cor": cor})

# ordem de desenho: tinta primeiro, depois destaque; vizinho mais próximo a partir do topo-esquerda
def ordenar(ts):
    if not ts: return []
    rest = ts[:]; cur = min(rest, key=lambda t: min(t["pts"][0][1] + t["pts"][0][0] * .3, t["pts"][-1][1] + t["pts"][-1][0] * .3))
    if cur["pts"][-1][1] + cur["pts"][-1][0] * .3 < cur["pts"][0][1] + cur["pts"][0][0] * .3: cur["pts"].reverse()
    res = [cur]; rest.remove(cur)
    while rest:
        px, py = res[-1]["pts"][-1]
        def d(t, fim): x, y = t["pts"][-1 if fim else 0]; return (x - px) ** 2 + (y - py) ** 2
        nxt = min(rest, key=lambda t: min(d(t, False), d(t, True)))
        if d(nxt, True) < d(nxt, False): nxt["pts"].reverse()
        res.append(nxt); rest.remove(nxt)
    return res
tracos = ordenar([t for t in tracos if t["cor"] == "ink"]) + ordenar([t for t in tracos if t["cor"] == "acc"])

reg_path = os.path.join(out, "artes.js")
reg = {}
if os.path.exists(reg_path):
    txt = open(reg_path, encoding="utf-8").read()
    try: reg = json.loads(txt[txt.index("{"):txt.rindex("}") + 1])
    except ValueError: reg = {}
reg[nome] = {"w": int(W), "h": int(H), "largura": round(largura, 2), "ink": f"{nome}_ink.png",
             "acc": f"{nome}_acc.png" if tem_acc else None, "tracos": tracos}
open(reg_path, "w", encoding="utf-8").write("window.HD_ARTES = " + json.dumps(reg, ensure_ascii=False) + ";\n")
print(f"ok {nome}: {W}x{H}, {len(tracos)} traços, largura {largura:.1f}px, destaque={'sim' if tem_acc else 'não'}")
