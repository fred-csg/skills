# Render paralelo do diario-experimento.
#   python render.py roteiro.py saida.mp4 [--proc N] [--audio mix.wav]
#   python render.py roteiro.py folha.jpg --stills 0.5,2,4.2      (folha de quadros pra conferir)
# Cada processo renderiza um trecho contínuo de quadros; no fim junta tudo sem recomprimir.
import os, sys, math, time, argparse, importlib.util, subprocess, multiprocessing as mp
AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)

def carrega(path):
    sys.path.insert(0, os.path.dirname(os.path.abspath(path)))
    spec = importlib.util.spec_from_file_location("roteiro", path)
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
    return m

def _trecho(args):
    rot, a, b, out = args
    import dx
    R = carrega(rot)
    p = subprocess.Popen([dx.FFM, "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{dx.W}x{dx.H}",
                          "-r", str(dx.FPS), "-i", "-", "-c:v", "libx264", "-preset", "medium", "-crf", "18",
                          "-pix_fmt", "yuv420p", out], stdin=subprocess.PIPE)
    for fi in range(a, b):
        p.stdin.write(dx.quadro(fi / dx.FPS, fi, R).tobytes())
    p.stdin.close(); p.wait()
    return out

def _still(args):
    rot, t = args
    import dx
    R = carrega(rot)
    return t, dx.quadro(t, int(t * dx.FPS), R).tobytes()

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("roteiro"); ap.add_argument("saida")
    ap.add_argument("--proc", type=int, default=max(1, (os.cpu_count() or 4) - 4))
    ap.add_argument("--audio"); ap.add_argument("--stills")
    ap.add_argument("--de", type=float, default=0); ap.add_argument("--ate", type=float)
    A = ap.parse_args()
    import dx
    from PIL import Image
    R = carrega(A.roteiro)
    t0 = time.time()
    if A.stills:
        ts = [float(x) for x in A.stills.split(",")]
        with mp.Pool(min(len(ts), A.proc)) as pool:
            res = dict(pool.map(_still, [(A.roteiro, t) for t in ts]))
        cols = min(5, len(ts)); rows = math.ceil(len(ts) / cols); tw_, th_ = 324, 576
        sheet = Image.new("RGB", (cols * tw_, rows * (th_ + 30)), (30, 30, 30))
        from PIL import ImageDraw
        d = ImageDraw.Draw(sheet)
        for i, t in enumerate(ts):
            im = Image.frombytes("RGB", (dx.W, dx.H), res[t]).resize((tw_, th_), Image.LANCZOS)
            x, y = (i % cols) * tw_, (i // cols) * (th_ + 30)
            sheet.paste(im, (x, y + 30)); d.text((x + 8, y + 8), f"{t:.2f}s", fill=(255, 255, 255))
        sheet.save(A.saida, quality=90); print("folha", A.saida, f"{time.time() - t0:.1f}s"); sys.exit()
    dur = A.ate if A.ate else R.CFG["dur"]
    f0, f1 = int(A.de * dx.FPS), int(math.ceil(dur * dx.FPS))
    n = max(1, min(A.proc, (f1 - f0) // 15))
    tmp = os.path.splitext(A.saida)[0] + "_partes"; os.makedirs(tmp, exist_ok=True)
    step = math.ceil((f1 - f0) / n)
    jobs = [(A.roteiro, f0 + i * step, min(f1, f0 + (i + 1) * step), os.path.join(tmp, f"p{i:03d}.mp4")) for i in range(n)]
    jobs = [j for j in jobs if j[2] > j[1]]
    print(f"{f1 - f0} quadros em {len(jobs)} processos...")
    with mp.Pool(len(jobs)) as pool:
        partes = pool.map(_trecho, jobs)
    lista = os.path.join(tmp, "lista.txt")
    with open(lista, "w", encoding="utf8") as f:
        for p in partes: f.write(f"file '{os.path.abspath(p)}'\n")
    mudo = A.saida if not A.audio else os.path.splitext(A.saida)[0] + "_mudo.mp4"
    subprocess.run([dx.FFM, "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", lista, "-c", "copy", mudo], check=True)
    if A.audio:
        subprocess.run([dx.FFM, "-v", "error", "-y", "-i", mudo, "-i", A.audio, "-c:v", "copy", "-c:a", "aac", "-b:a", "192k",
                        "-shortest", "-movflags", "+faststart", A.saida], check=True)
    for p in partes: os.remove(p)
    os.remove(lista); os.rmdir(tmp)
    print("ok", A.saida, f"{time.time() - t0:.1f}s")
