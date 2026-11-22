# Render completo de uma cena (Windows ou Mac).
# Uso: python render.py <cena.py> <pasta_frames> [resolucao%=100] [partes=1]
#   partes=1 (padrão): um processo usando todas as placas de vídeo.
#   partes=N: N processos, um por placa (use quando tiver 2+ placas NVIDIA iguais).
import sys, os, subprocess
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from ambiente import achar_blender

cena, out = os.path.abspath(sys.argv[1]), os.path.abspath(sys.argv[2])
res = sys.argv[3] if len(sys.argv) > 3 else "100"
n = int(sys.argv[4]) if len(sys.argv) > 4 else 1
bl, ver = achar_blender()
if not bl: raise SystemExit("Blender 5 não encontrado (rode instalar.py).")
os.makedirs(out, exist_ok=True)
procs = []
for i in range(n):
    env = dict(os.environ)
    if n > 1: env["VOX_GPU"] = str(i)
    log = open(os.path.join(out, f"log_{i}.txt"), "w")
    procs.append(subprocess.Popen([bl, "-b", "--factory-startup", "--python", cena, "--", out, res, "0-99999", f"{i}/{n}"],
                                  cwd=os.path.dirname(cena), stdout=log, stderr=subprocess.STDOUT, env=env))
for p in procs: p.wait()
erros = [l for i in range(n) for l in open(os.path.join(out, f"log_{i}.txt"), encoding="utf-8", errors="replace") if "Traceback" in l or "Error:" in l]
print("\n".join(erros[:10]) or "sem erros")
print(len([f for f in os.listdir(out) if f.endswith(".png")]), "quadros em", out)
