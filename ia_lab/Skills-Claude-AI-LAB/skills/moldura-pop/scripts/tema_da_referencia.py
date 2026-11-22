# moldura-pop · tema a partir de uma referência
# Lê um print/imagem de layout OU um vídeo (pega quadros espalhados) e propõe um tema.json:
# fundo (cor dominante), texto (contraste com o fundo) e destaque (a cor mais viva com presença real).
#   python -I tema_da_referencia.py <imagem|video> [tema.json] [--fundo claro|escuro] [--acc #RRGGBB]
# Depois: python -I mp.py amostra amostra_tema.jpg  (na pasta onde está o tema.json) e mostrar pro usuário aprovar.
import sys, os, json, subprocess, tempfile, colorsys
import numpy as np
from PIL import Image

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ambiente import ffmpeg
FFM = ffmpeg()
VID = (".mp4", ".mov", ".m4v", ".mkv", ".webm", ".avi")

def pixels(src):
    if src.lower().endswith(VID):
        tmp = tempfile.mkdtemp()
        subprocess.run([FFM, "-v", "error", "-i", src, "-vf", "fps=1/2,scale=270:-1", "-frames:v", "24",
                        os.path.join(tmp, "f%02d.png")], check=True)
        ims = [Image.open(os.path.join(tmp, f)).convert("RGB") for f in sorted(os.listdir(tmp))]
    else:
        im = Image.open(src).convert("RGB"); im.thumbnail((480, 480)); ims = [im]
    return np.concatenate([np.asarray(i, np.float32).reshape(-1, 3) for i in ims])

def kmeans(px, k=8, it=20, seed=0):
    rng = np.random.default_rng(seed)
    if len(px) > 60000: px = px[rng.choice(len(px), 60000, replace=False)]
    c = px[rng.choice(len(px), k, replace=False)]
    for _ in range(it):
        lab = np.argmin(((px[:, None] - c[None]) ** 2).sum(-1), 1)
        c = np.array([px[lab == i].mean(0) if (lab == i).any() else c[i] for i in range(k)])
    share = np.bincount(lab, minlength=k) / len(lab)
    return c, share

def lum(c): return (0.2126 * c[0] + 0.7152 * c[1] + 0.0722 * c[2]) / 255
def hx(c): return "#%02X%02X%02X" % tuple(int(round(v)) for v in c[:3])
def sat_val(c):
    h, s, v = colorsys.rgb_to_hsv(*(np.asarray(c) / 255)); return s, v

def main():
    a = [x for x in sys.argv[1:] if not x.startswith("--")]
    opts = dict(zip(sys.argv[1::1], sys.argv[2::1]))
    src = a[0]; out = a[1] if len(a) > 1 and a[1].endswith(".json") else "tema.json"
    c, share = kmeans(pixels(src))
    order = np.argsort(-share)
    bg = c[order[0]]
    escuro = lum(bg) < 0.45
    if opts.get("--fundo") in ("claro", "escuro"): escuro = opts["--fundo"] == "escuro"
    # destaque: mais saturado e vivo, com pelo menos 1,5% da imagem
    cand = [(sat_val(c[i])[0] * sat_val(c[i])[1], i) for i in range(len(c)) if share[i] > 0.015]
    acc = c[max(cand)[1]] if cand else np.array([215, 255, 58])
    if opts.get("--acc"): acc = np.array([int(opts["--acc"].lstrip("#")[j:j + 2], 16) for j in (0, 2, 4)])
    if not opts.get("--acc"):                     # destaque precisa "acender": mantém o tom, sobe saturação e brilho
        h, s, v = colorsys.rgb_to_hsv(*(acc / 255))
        acc = np.array(colorsys.hsv_to_rgb(h, max(s, 0.62), max(v, 0.88))) * 255
    if escuro:
        paper = bg if lum(bg) < 0.12 else bg * (0.10 / max(lum(bg), 1e-3))
        t = dict(base="ai-lab", escuro=True, paper=hx(paper), dark=hx(paper * 0.9),
                 glass=hx(np.clip(paper + 12, 0, 255)), surf=hx(np.clip(paper + 12, 0, 255)),
                 surf2=hx(np.clip(paper + 25, 0, 255)), line=hx(np.clip(paper + 44, 0, 255)),
                 ink="#F5F5F2", ink2="#A0A09A", gray="#787872")
    else:
        paper = bg if lum(bg) > 0.88 else bg + (255 - bg) * 0.7
        t = dict(base="classico", escuro=False, paper=hx(paper), line=hx(paper * 0.91),
                 ink="#111113", ink2="#46464C", gray="#96969E")
    t["acc"] = hx(acc); t["acc2"] = hx(acc + (255 - acc) * 0.45)
    t["origem"] = os.path.basename(src)
    t["paleta_encontrada"] = [[hx(c[i]), round(float(share[i]) * 100, 1)] for i in order]
    json.dump(t, open(out, "w", encoding="utf8"), indent=2, ensure_ascii=False)
    print(json.dumps(t, indent=2, ensure_ascii=False)); print("salvo:", out)

if __name__ == "__main__":
    main()
