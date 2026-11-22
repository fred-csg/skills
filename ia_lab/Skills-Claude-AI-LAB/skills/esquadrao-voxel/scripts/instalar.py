# Confere e instala o que o Esquadrão Voxel precisa. Rode com o Python que a skill vai usar.
# Uso:  python instalar.py            -> instala as bibliotecas que faltam + testa o Blender (1 quadro)
#       python instalar.py --checar   -> só mostra o que está pronto e o que falta (não instala nada)
import sys, os, subprocess, importlib.util, tempfile

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
from ambiente import achar_blender, memoria_gb, WIN, MAC
CHECAR = "--checar" in sys.argv

def tem(mod): return importlib.util.find_spec(mod) is not None

v = sys.version_info
print(f"Python {v.major}.{v.minor} · sistema: {'Mac' if MAC else ('Windows' if WIN else sys.platform)} · RAM: {memoria_gb():.0f} GB")
if not ((3, 10) <= (v.major, v.minor) <= (3, 13)):
    raise SystemExit("Use Python 3.10 a 3.13 (o faster-whisper ainda não tem versão para este Python).")

base = {"PIL": "pillow", "numpy": "numpy", "faster_whisper": "faster-whisper", "imageio_ffmpeg": "imageio-ffmpeg"}
falta = [p for m, p in base.items() if not tem(m)]
print("bibliotecas que faltam:", ", ".join(falta) or "nenhuma")
if falta and not CHECAR:
    subprocess.run([sys.executable, "-m", "pip", "install", "--upgrade", *falta], check=True)

blender, ver = achar_blender()
if not blender:
    print("\nBlender 5 NÃO encontrado. É grátis:")
    if WIN: print("  winget install -e --id BlenderFoundation.Blender   (ou blender.org/download)")
    elif MAC: print("  brew install --cask blender   (ou blender.org/download)")
    else: print("  blender.org/download")
    sys.exit(1)
print(f"Blender {ver[0]}.{ver[1]}: {blender}")
if ver < (5, 0): print("Aviso: a skill foi testada no Blender 5.x; atualize se der erro.")
if CHECAR: sys.exit(0)

# teste: 1 quadro de um boneco numa sala (prova que o Blender renderiza nesta máquina)
teste = os.path.join(tempfile.gettempdir(), "vox_teste")
os.makedirs(teste, exist_ok=True)
cena = os.path.join(teste, "cena_teste.py")
open(cena, "w", encoding="utf-8").write(f'''import sys; sys.path.insert(0, r"{os.path.join(AQUI, "molde")}")
import vox, cenario as C, bonecos as B
vox.setup(1.0, paleta="manha")
C.sala(0, "#5FA8D3", "madeira")
b = B.receita("teste", "pesquisador"); b.trilha = [(0, (0, 0), 0)]
vox.CAM = [(0, (0, -5, 2.2), (0, 0, 1.0), 40, "corte")]
vox.run(lambda t: b.update(t))
''')
print("renderizando 1 quadro de teste…")
r = subprocess.run([blender, "-b", "--factory-startup", "--python", cena, "--", teste, "30", "0"], capture_output=True, text=True, timeout=600)
ok = os.path.exists(os.path.join(teste, "f00000.png"))
print("TESTE OK:" if ok else "TESTE FALHOU:", os.path.join(teste, "f00000.png") if ok else (r.stdout[-1500:] + r.stderr[-800:]))
