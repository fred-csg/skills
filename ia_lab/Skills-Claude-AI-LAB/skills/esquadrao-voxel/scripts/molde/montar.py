# Esquadrão Voxel — monta o vídeo: quadros do Blender + HUD (overlay.py do projeto) + pós (brilho, aberração, grão, vinheta).
#   python montar.py <frames_dir> <overlay.py> <audio.wav|-> <saida.mp4>
#   python montar.py <frames_dir> <overlay.py> - <folha.jpg> --folha 0.5,3,6.2,...   (só alguns quadros, pra conferir)
# O overlay.py precisa ter:  def desenhar(img, t)   (img = PIL RGBA 1080x1920)
import sys as _s, os as _o
_s.path.insert(0, _o.path.dirname(_o.path.dirname(_o.path.abspath(__file__))))
_s.path.insert(0, _o.path.dirname(_o.path.abspath(__file__)))
import ambiente
import os, sys, subprocess, importlib.util, glob
import numpy as np
from PIL import Image, ImageFilter
from multiprocessing import Pool

W, H = 1080, 1920
FPS = 30
POS = dict(bloom=0.32, limiar=0.72, aberracao=2, grao=7.0, vinheta=0.22)
_ov = None; _vig = None; _dir = None

def _init(frames_dir, ov_path):
    global _ov, _vig, _dir
    _dir = frames_dir
    sys.path.insert(0, os.path.dirname(os.path.abspath(ov_path)))
    spec = importlib.util.spec_from_file_location("overlay_proj", ov_path)
    _ov = importlib.util.module_from_spec(spec); spec.loader.exec_module(_ov)
    POS.update(getattr(_ov, "POS", {}))
    yy, xx = np.mgrid[0:H, 0:W]
    r = np.sqrt(((xx - W / 2) / (W / 2)) ** 2 + ((yy - H / 2) / (H / 2)) ** 2)
    _vig = (1 - POS["vinheta"] * np.clip(r - 0.45, 0, 1) ** 1.6 * 1.6)[..., None].astype(np.float32)

def _pos3d(im):
    a = np.asarray(im.convert("RGB"), np.float32) / 255
    if POS["bloom"] > 0:
        lum = a.max(axis=2, keepdims=True)
        hi = np.clip((lum - POS["limiar"]) / (1 - POS["limiar"]), 0, 1) * a
        small = Image.fromarray((hi * 255).astype(np.uint8)).resize((W // 4, H // 4), Image.BILINEAR)
        b1 = np.asarray(small.filter(ImageFilter.GaussianBlur(6)).resize((W, H), Image.BILINEAR), np.float32) / 255
        b2 = np.asarray(small.filter(ImageFilter.GaussianBlur(18)).resize((W, H), Image.BILINEAR), np.float32) / 255
        a = 1 - (1 - a) * (1 - np.clip((b1 * 0.6 + b2 * 0.8) * POS["bloom"] * 2, 0, 1))   # screen
    a = a * _vig
    return Image.fromarray((np.clip(a, 0, 1) * 255).astype(np.uint8)).convert("RGBA")

def _pos_final(im, f):
    a = np.asarray(im.convert("RGB"), np.int16)
    k = POS["aberracao"]
    if k:
        out = a.copy(); out[:, k:, 0] = a[:, :-k, 0]; out[:, :-k, 2] = a[:, k:, 2]; a = out
    if POS["grao"] > 0:
        rng = np.random.default_rng(f)
        n = rng.normal(0, POS["grao"], (H // 2, W // 2, 1)).astype(np.int16)
        n = np.repeat(np.repeat(n, 2, 0), 2, 1)
        a = a + n
    return np.clip(a, 0, 255).astype(np.uint8)

def quadro(f):
    p = os.path.join(_dir, f"f{f:05d}.png")
    if not os.path.exists(p):
        ps = sorted(glob.glob(os.path.join(_dir, "f*.png")))
        p = min(ps, key=lambda q: abs(int(os.path.basename(q)[1:6]) - f))
    im = Image.open(p)
    if im.size != (W, H): im = im.resize((W, H), Image.LANCZOS)
    im = _pos3d(im)
    _ov.desenhar(im, f / FPS)
    return _pos_final(im, f).tobytes()

if __name__ == "__main__":
    frames_dir, ov, audio, saida = sys.argv[1:5]
    ff = ambiente.ffmpeg()
    nums = sorted(int(os.path.basename(p)[1:6]) for p in glob.glob(os.path.join(frames_dir, "f*.png")))
    if "--folha" in sys.argv:
        ts = [float(x) for x in sys.argv[sys.argv.index("--folha") + 1].split(",")]
        _init(frames_dir, ov)
        ims = [Image.frombytes("RGB", (W, H), quadro(int(round(t * FPS)))) for t in ts]
        cols = min(6, len(ims)); rows = (len(ims) + cols - 1) // cols; tw, th = 360, 640
        sh = Image.new("RGB", (cols * tw, rows * th), "#000")
        for i, im in enumerate(ims): sh.paste(im.resize((tw, th), Image.LANCZOS), ((i % cols) * tw, (i // cols) * th))
        sh.save(saida, quality=90); print(saida); sys.exit()
    nf = nums[-1] + 1
    cmd = [ff, "-y", "-v", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-"]
    if audio != "-": cmd += ["-i", audio]
    cmd += ["-c:v", "libx264", "-crf", "17", "-preset", "medium", "-pix_fmt", "yuv420p", "-movflags", "+faststart"]
    if audio != "-": cmd += ["-c:a", "aac", "-b:a", "192k", "-af", "loudnorm=I=-14:TP=-1.5", "-ar", "48000", "-shortest"]   # loudnorm sobe pra 96 kHz: volta pra 48k (celular toca mudo)
    cmd += [saida]
    pr = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    with Pool(max(2, (os.cpu_count() or 4) - 4), initializer=_init, initargs=(frames_dir, ov)) as pool:
        for i, b in enumerate(pool.imap(quadro, range(nf), chunksize=4)):
            pr.stdin.write(b)
            if i % 60 == 0: print(f"{i}/{nf}", flush=True)
    pr.stdin.close(); pr.wait()
    print("OK", saida)
