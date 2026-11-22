# Acha as ferramentas no computador de quem estiver usando a skill (Windows ou Mac):
# ffmpeg, fontes e a biblioteca de sons opcional. Nenhum caminho fixo de uma máquina só.
import os, sys, shutil, platform

AQUI = os.path.dirname(os.path.abspath(__file__))
SKILL = os.path.dirname(AQUI)
WIN, MAC = sys.platform.startswith("win"), sys.platform == "darwin"
for _s in (sys.stdout, sys.stderr):                  # acentos certos em qualquer terminal
    try: _s.reconfigure(encoding="utf-8", errors="replace")
    except Exception: pass


def ffmpeg():
    """ffmpeg: variável FFMPEG -> pacote imageio-ffmpeg (instalado pelo instalar.py) -> o do sistema."""
    if os.environ.get("FFMPEG") and os.path.exists(os.environ["FFMPEG"]): return os.environ["FFMPEG"]
    try:
        import imageio_ffmpeg
        return imageio_ffmpeg.get_ffmpeg_exe()
    except Exception:
        p = shutil.which("ffmpeg")
        if p: return p
    raise SystemExit("ffmpeg não encontrado. Rode:  python -m pip install imageio-ffmpeg")


def _pastas_fontes():
    ds = [os.path.join(SKILL, "assets", "fonts")]          # fontes que vierem junto com a skill
    if WIN:
        ds += [os.path.expanduser(r"~\AppData\Local\Microsoft\Windows\Fonts"),
               os.path.join(os.environ.get("WINDIR", r"C:\Windows"), "Fonts")]
    elif MAC:
        ds += [os.path.expanduser("~/Library/Fonts"), "/Library/Fonts", "/System/Library/Fonts",
               "/System/Library/Fonts/Supplemental"]
    else:
        ds += [os.path.expanduser("~/.fonts"), os.path.expanduser("~/.local/share/fonts"), "/usr/share/fonts"]
    return [d for d in ds if os.path.isdir(d)]


def achar_fonte(*nomes):
    """Primeiro arquivo de fonte que existir, na ordem dada. Procura também em subpastas."""
    pastas = _pastas_fontes()
    for n in nomes:
        for d in pastas:
            p = os.path.join(d, n)
            if os.path.exists(p): return p
    for n in nomes:                                       # busca mais lenta em subpastas (Linux / pastas de fontes)
        for d in pastas:
            for dp, _, fs in os.walk(d):
                if n in fs: return os.path.join(dp, n)
    return None


def pastas_sfx():
    """Biblioteca de sons do usuário (opcional). Ordem:
    1) variável de ambiente SFX_PASTA (várias separadas por ';')
    2) arquivo sfx_pasta.txt na pasta da skill (um caminho por linha)
    Sem nada configurado, os sons são gerados por código (sfx_synth.py)."""
    ps = []
    env = os.environ.get("SFX_PASTA", "")
    ps += [p for p in env.split(";") if p.strip()]
    cfg = os.path.join(SKILL, "sfx_pasta.txt")
    if os.path.exists(cfg):
        ps += [l.strip() for l in open(cfg, encoding="utf8") if l.strip() and not l.startswith("#")]
    return [p for p in ps if os.path.isdir(p)]
