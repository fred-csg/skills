# Confere e instala o que a Maquete Viva precisa. Rode com o Python que a skill vai usar.
# Uso:  python instalar.py            -> instala as bibliotecas que faltam + testa o Blender (1 quadro)
#       python instalar.py --checar   -> só mostra o que está pronto e o que falta (não instala nada)
import sys, os, subprocess, importlib.util, platform, tempfile

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
from ambiente import achar_blender, memoria_gb, WIN, MAC
CHECAR = "--checar" in sys.argv
SKILL = os.path.dirname(AQUI)
ASSETS = os.path.join(SKILL, "assets", "modelos")

# ---------------------------------------------------------------- redes do CTA final
# python instalar.py --redes @meucanal @meuinsta @meutiktok   (use "-" pra pular uma rede)
if "--redes" in sys.argv:
    import json
    i = sys.argv.index("--redes"); vals = (sys.argv[i + 1:] + ["-", "-", "-"])[:3]
    redes = [[k, v] for k, v in zip(("youtube", "instagram", "tiktok"), vals) if v != "-"]
    json.dump(redes, open(os.path.join(SKILL, "redes.json"), "w", encoding="utf-8"), ensure_ascii=False)
    print("redes salvas:", redes); sys.exit(0)

# ---------------------------------------------------------------- modelos 3D gratuitos (modo premium)
def baixar_assets():
    """Pacotes Kenney (licença CC0, uso livre) + céu HDRI do Poly Haven (CC0). ~25 MB."""
    import urllib.request, re, zipfile, io
    os.makedirs(ASSETS, exist_ok=True)
    ua = {"User-Agent": "Mozilla/5.0"}
    for nome, pag in (("commercial", "city-kit-commercial"), ("cars", "car-kit"), ("roads", "city-kit-roads"), ("suburban", "city-kit-suburban")):
        dest = os.path.join(ASSETS, nome, "x")
        if os.path.isdir(os.path.join(dest, "Models")): print("ok:", nome); continue
        html = urllib.request.urlopen(urllib.request.Request(f"https://kenney.nl/assets/{pag}", headers=ua), timeout=60).read().decode("utf-8", "replace")
        m = re.search(r'https://kenney\.nl/media/pages/assets/[^"]+\.zip', html)
        if not m: print("não achei o download de", pag, "- baixe manualmente em kenney.nl/assets/" + pag); continue
        data = urllib.request.urlopen(urllib.request.Request(m.group(0), headers=ua), timeout=300).read()
        zipfile.ZipFile(io.BytesIO(data)).extractall(dest); print("baixado:", nome)
    h = os.path.join(ASSETS, "hdri", "ceu.hdr")
    if not os.path.exists(h):
        os.makedirs(os.path.dirname(h), exist_ok=True)
        url = "https://dl.polyhaven.org/file/ph-assets/HDRIs/hdr/2k/kloofendal_48d_partly_cloudy_puresky_2k.hdr"
        open(h, "wb").write(urllib.request.urlopen(urllib.request.Request(url, headers=ua), timeout=300).read()); print("baixado: céu HDRI")
if "--assets" in sys.argv:
    baixar_assets(); sys.exit(0)


def tem(mod): return importlib.util.find_spec(mod) is not None


v = sys.version_info
print(f"Python {v.major}.{v.minor} · sistema: {'Mac' if MAC else ('Windows' if WIN else sys.platform)} · RAM: {memoria_gb():.0f} GB")
if not ((3, 10) <= (v.major, v.minor) <= (3, 13)):
    raise SystemExit("Use Python 3.10 a 3.13 (o faster-whisper ainda não tem versão para este Python).")

# ---------------------------------------------------------------- bibliotecas Python
base = {"PIL": "pillow", "numpy": "numpy", "faster_whisper": "faster-whisper", "imageio_ffmpeg": "imageio-ffmpeg"}
falta = [p for m, p in base.items() if not tem(m)]
print("bibliotecas que faltam:", ", ".join(falta) or "nenhuma")

# ---------------------------------------------------------------- Blender
blender, ver = achar_blender()
aviso_blender = None
if MAC and platform.machine() == "x86_64":
    aviso_blender = ("Este Mac tem processador Intel. O Blender 5 só roda em Mac com chip Apple (M1 ou mais novo),\n"
                     "então a Maquete Viva não funciona aqui. As outras skills do pacote funcionam normalmente.")
elif not blender or ver < (5, 0):
    como = ("  Windows:  winget install -e --id BlenderFoundation.Blender\n" if WIN else
            "  Mac:      brew install --cask blender\n" if MAC else "")
    aviso_blender = ("PARA ESTA SKILL VOCÊ PRECISA INSTALAR O BLENDER 5 (grátis, ~1 GB).\n"
                     + (f"  Encontrei o Blender {ver[0]}.{ver[1]}, que é antigo para esta skill.\n" if blender else "")
                     + "  Jeito fácil: peça ao Claude \"instala o Blender pra mim\". Ele roda:\n" + como
                     + "  Ou baixe em https://www.blender.org/download/ e instale normalmente.\n"
                     "  Requisito: placa de vídeo de 2017 em diante (NVIDIA GTX 900+, AMD RX 400+, Intel 7ª geração+)\n"
                     "  ou Mac com chip Apple e macOS 13+.")
print("Blender:", f"{blender} (versão {ver[0]}.{ver[1]})" if blender and not aviso_blender else "NÃO ENCONTRADO")
if aviso_blender: print("\n" + "=" * 70 + "\n" + aviso_blender + "\n" + "=" * 70)

partes = 3 if memoria_gb() >= 15 else 1
print(f"render: {partes} parte(s) ao mesmo tempo ({'16 GB+ de RAM' if partes == 3 else 'menos de 16 GB de RAM: uma por vez'})")
if CHECAR: sys.exit(0)

if falta:
    print("instalando:", " ".join(falta), flush=True)
    subprocess.run([sys.executable, "-m", "pip", "install", "--upgrade", *falta], check=True)

try:
    baixar_assets()
except Exception as e:
    print("aviso: não consegui baixar os modelos 3D gratuitos agora (" + str(e) + "). Rode depois: python instalar.py --assets")
if not os.path.exists(os.path.join(SKILL, "redes.json")):
    print("\nDica: grave suas redes pro CTA final:  python instalar.py --redes @seucanal @seuinsta @seutiktok")
if aviso_blender: raise SystemExit("\nInstale o Blender e rode este arquivo de novo para o teste.")

# ---------------------------------------------------------------- teste: 1 quadro a 20 %
out = tempfile.mkdtemp(prefix="maquete_teste_")
print("testando o Blender (1 quadro em tamanho reduzido)…", flush=True)
r = subprocess.run([blender, "-b", "--factory-startup", "--python", os.path.join(AQUI, "cena.py"), "--", out, "20", "0"],
                   capture_output=True, text=True, timeout=1800)
pngs = [f for f in os.listdir(out) if f.lower().endswith(".png")]
if pngs:
    print(f"Pronto. O Blender renderizou o quadro de teste em {out}")
else:
    print("O teste do Blender falhou. Final do log:\n" + (r.stdout + r.stderr)[-1500:])
    print("\nCausa mais comum: placa de vídeo sem suporte ao Blender 5 (EEVEE precisa de GPU com OpenGL 4.3 / Vulkan).")
