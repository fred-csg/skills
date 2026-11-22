# Recorte da pessoa quadro a quadro (BiRefNet portrait, ONNX) -> vídeo de máscara cinza.
# Uso: python matte.py <video> <saida_mascara.mp4> [max_frames]
# Placa NVIDIA: usa a GPU (onnxruntime-gpu + bibliotecas CUDA instaladas pelo instalar.py).
# Mac com chip Apple: tenta o CoreML. Sem nada disso: roda no processador (bem mais lento).
import sys, os, time, subprocess, numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ambiente import ffmpeg
from modelo import caminho_modelo
import onnxruntime as ort

def _cuda():
    """Carrega CUDA/cuDNN: primeiro dos pacotes pip nvidia-* (onnxruntime-gpu[cuda,cudnn]);
    se faltar, de uma pasta indicada em CUDA_DLLS ou do torch de um ComfyUI já instalado (opcional)."""
    if "CUDAExecutionProvider" not in ort.get_available_providers() or not hasattr(ort, "preload_dlls"): return
    if not sys.platform.startswith("win"):
        try: ort.preload_dlls()
        except Exception: pass
        return
    # Windows: carregar UM conjunto só, da versão de CUDA com que o onnxruntime foi feito (misturar versões
    # faz o recorte cair no processador sem avisar).
    try:
        from onnxruntime.capi import build_and_package_info as bi
        major = str(bi.cuda_version).split(".")[0]
    except Exception:
        major = "13"
    alvo = f"cublasLt64_{major}.dll"
    import site, glob
    sp = site.getsitepackages() + [site.getusersitepackages()]
    if any(glob.glob(os.path.join(p, "nvidia", "**", alvo), recursive=True) for p in sp):
        ort.preload_dlls(); return                       # pacotes pip certos (instalar.py)
    extras = [os.environ.get("CUDA_DLLS", ""),        # opcional: torch de um ComfyUI já instalado
              r"C:\ComfyUI\ComfyUI_windows_portable\python_embeded\Lib\site-packages\torch\lib",
              os.path.expanduser(r"~\ComfyUI-Installs\ComfyUI\ComfyUI\.venv\Lib\site-packages\torch\lib")]
    for d in extras:
        if d and os.path.exists(os.path.join(d, alvo)):
            os.add_dll_directory(d); os.environ["PATH"] = d + os.pathsep + os.environ["PATH"]
            ort.preload_dlls(directory=d); return
    print(f"aviso: bibliotecas CUDA {major} não encontradas; o recorte vai rodar no processador. Rode: python instalar.py")
_cuda()

FFM = ffmpeg()
MODEL = caminho_modelo()
if not MODEL: raise SystemExit("Modelo de recorte não encontrado. Rode:  python instalar.py")
src, out = sys.argv[1], sys.argv[2]
NMAX = int(sys.argv[3]) if len(sys.argv) > 3 else 10**9
S = 1024; OW, OH = 540, 960
prov = [p for p in ("CUDAExecutionProvider", "CoreMLExecutionProvider") if p in ort.get_available_providers()] + ["CPUExecutionProvider"]
sess = ort.InferenceSession(MODEL, ort.SessionOptions(), providers=prov)
usa = sess.get_providers()[0]
print("recorte rodando em:", {"CUDAExecutionProvider": "placa NVIDIA", "CoreMLExecutionProvider": "chip Apple"}.get(usa, "processador (lento)"))
iname = sess.get_inputs()[0].name
dec = subprocess.Popen([FFM, "-v", "error", "-i", src, "-vf", f"scale={S}:{S}:flags=area", "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], stdout=subprocess.PIPE)
enc = subprocess.Popen([FFM, "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "gray", "-s", f"{OW}x{OH}", "-r", "29.97", "-i", "-",
                        "-c:v", "libx264", "-crf", "8", "-pix_fmt", "yuv420p", out], stdin=subprocess.PIPE)
mean = np.array([0.485, 0.456, 0.406], np.float32); std = np.array([0.229, 0.224, 0.225], np.float32)
from PIL import Image
n = 0; t0 = time.time()
while n < NMAX:
    raw = dec.stdout.read(S * S * 3)
    if len(raw) < S * S * 3: break
    x = (np.frombuffer(raw, np.uint8).reshape(S, S, 3).astype(np.float32) / 255 - mean) / std
    y = sess.run(None, {iname: x.transpose(2, 0, 1)[None]})[0][0, 0]
    m = 1 / (1 + np.exp(-y))
    m = np.asarray(Image.fromarray((np.clip(m,0,1)*255).astype(np.uint8)).resize((OW, OH), Image.BILINEAR)).astype(np.float32)/255
    enc.stdin.write((np.clip(m, 0, 1) * 255).astype(np.uint8).tobytes())
    n += 1
    if n % 50 == 0: print(n, f"{(time.time()-t0)/n:.3f}s/q", flush=True)
enc.stdin.close(); enc.wait(); dec.kill()
print("ok", n, f"{time.time()-t0:.1f}s")
