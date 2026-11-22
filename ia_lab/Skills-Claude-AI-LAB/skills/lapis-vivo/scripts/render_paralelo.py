"""Lápis Vivo — render completo em paralelo: divide o vídeo em partes, renderiza todas ao mesmo tempo
(um Chromium por parte) e emenda sem recomprimir.

uso: python -I render_paralelo.py <pasta_projeto> <saida_mudo.mp4> [--fps 30] [--partes N] [--q tema=creme]

Também grava cues.json (sons) ao lado da saída. N padrão = metade dos núcleos (máx. 12).
"""
import json, os, shutil, subprocess, sys, tempfile, time

args = sys.argv[1:]
def opt(n, d=None):
    if n in args: i = args.index(n); v = args[i + 1]; del args[i:i + 2]; return v
    return d
fps = int(opt("--fps", 30)); q = opt("--q")
partes = int(opt("--partes", max(2, min(12, (os.cpu_count() or 4) // 2))))
proj, out = os.path.abspath(args[0]), os.path.abspath(args[1])
AQUI = os.path.dirname(os.path.abspath(__file__))
FF = os.environ.get("FFMPEG", "ffmpeg")
NODE = shutil.which("node") or "node"
extra = ["--q", q] if q else []
tmp = tempfile.mkdtemp(prefix="lv_")
base = [NODE, os.path.join(AQUI, "render.mjs"), proj]

r = subprocess.run(base + [os.path.join(tmp, "info", "x.mp4"), str(fps), "--info"] + extra, capture_output=True, text=True, encoding="utf-8", errors="replace")
if r.returncode: sys.exit((r.stdout or "") + (r.stderr or ""))
dur = json.loads(r.stdout.strip().splitlines()[-1])["dur"]
total = round(dur * fps)
partes = max(1, min(partes, total // 30 or 1))
cortes = [round(total * i / partes) for i in range(partes + 1)]
t = time.time(); procs = []
for i in range(partes):
    o = os.path.join(tmp, f"p{i:02d}", "parte.mp4")
    procs.append((o, subprocess.Popen(base + [o, str(fps), repr(cortes[i] / fps), repr(cortes[i + 1] / fps)] + extra,
                                      stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)))
print(f"{total} quadros ({dur:.2f}s) em {partes} partes…", flush=True)
for o, p in procs:
    err = p.communicate()[1]
    if p.returncode: sys.exit("falhou: " + err.decode("utf-8", "replace")[-800:])
lista = os.path.join(tmp, "lista.txt")
open(lista, "w", encoding="utf-8").write("".join(f"file '{o.replace(os.sep, '/')}'\n" for o, _ in procs))
os.makedirs(os.path.dirname(out), exist_ok=True)
subprocess.run([FF, "-y", "-v", "error", "-f", "concat", "-safe", "0", "-i", lista, "-c", "copy", "-movflags", "+faststart", out], check=True)
shutil.copy2(os.path.join(tmp, "info", "cues.json"), os.path.join(os.path.dirname(out), "cues.json"))
shutil.rmtree(tmp, ignore_errors=True)
print(f"ok -> {out}  ({total} quadros em {time.time() - t:.0f}s)  duracao={dur:.3f}")
