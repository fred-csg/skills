# Instala tudo que a Moldura Pop precisa, no Python que rodar este arquivo (de preferência um venv só dela).
# Uso:  python instalar.py            -> instala bibliotecas + baixa o modelo de recorte (~973 MB) + testa
#       python instalar.py --checar   -> só mostra o que já está pronto e o que falta (não instala nada)
import sys, os, subprocess, shutil, importlib.util

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
CHECAR = "--checar" in sys.argv
MAC = sys.platform == "darwin"
NVIDIA = shutil.which("nvidia-smi") is not None and subprocess.run(["nvidia-smi"], capture_output=True).returncode == 0


def tem(mod): return importlib.util.find_spec(mod) is not None
def pip(*pkgs):
    print("instalando:", " ".join(pkgs), flush=True)
    subprocess.run([sys.executable, "-m", "pip", "install", "--upgrade", *pkgs], check=True)


v = sys.version_info
print(f"Python {v.major}.{v.minor} · sistema: {'Mac' if MAC else sys.platform} · placa NVIDIA: {'sim' if NVIDIA else 'não'}")
if not ((3, 10) <= (v.major, v.minor) <= (3, 13)):
    raise SystemExit("Use Python 3.10 a 3.13 (o faster-whisper e o onnxruntime ainda não têm versão para este Python).")

base = {"PIL": "pillow", "numpy": "numpy", "faster_whisper": "faster-whisper", "imageio_ffmpeg": "imageio-ffmpeg"}
falta = [p for m, p in base.items() if not tem(m)]
ort_pkg = "onnxruntime-gpu[cuda,cudnn]" if NVIDIA else "onnxruntime"
precisa_ort = not tem("onnxruntime")
if NVIDIA and tem("onnxruntime"):
    import onnxruntime as ort
    precisa_ort = "CUDAExecutionProvider" not in ort.get_available_providers()

from modelo import caminho_modelo, baixar, TAMANHO
print("bibliotecas que faltam:", ", ".join(falta + ([ort_pkg] if precisa_ort else [])) or "nenhuma")
print("modelo de recorte:", caminho_modelo() or f"falta baixar ({TAMANHO / 1e9:.2f} GB)")
if CHECAR: sys.exit(0)

if falta: pip(*falta)
if precisa_ort:
    if NVIDIA:
        print("placa NVIDIA: instalando o recorte na GPU com as bibliotecas CUDA (download grande, ~2 GB)")
    pip(ort_pkg)
baixar()

# teste rápido: abre o modelo e diz onde ele roda
r = subprocess.run([sys.executable, "-c",
    "import sys; sys.path.insert(0, r'%s'); exec(open(r'%s', encoding='utf8').read().split('FFM = ffmpeg()')[0]);"
    "from modelo import caminho_modelo; prov=[p for p in ('CUDAExecutionProvider','CoreMLExecutionProvider') if p in ort.get_available_providers()]+['CPUExecutionProvider'];"
    "s=ort.InferenceSession(caminho_modelo(), providers=prov); print('TESTE', s.get_providers()[0])"
    % (AQUI, os.path.join(AQUI, "matte.py"))], capture_output=True, text=True)
linha = next((l for l in r.stdout.splitlines() if l.startswith("TESTE")), "")
onde = {"CUDAExecutionProvider": "placa NVIDIA (rápido: ~3 min para 25 s de vídeo)",
        "CoreMLExecutionProvider": "chip Apple"}.get(linha[6:].strip(), "processador (lento: ~7 s por quadro, ~1 h 30 para 27 s)")
print("\nPronto. O recorte vai rodar em:", onde if linha else "ERRO no teste:\n" + r.stderr[-800:])
