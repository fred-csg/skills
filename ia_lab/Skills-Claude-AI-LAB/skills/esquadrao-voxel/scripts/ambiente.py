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


# ---------------------------------------------------------------- Blender (só a Maquete Viva usa)
def achar_blender():
    """Blender 5+: variável BLENDER -> PATH -> pastas de instalação padrão. Devolve (caminho, versão) ou (None, None)."""
    import glob, re, subprocess
    cands = [os.environ.get("BLENDER", ""), shutil.which("blender") or ""]
    if WIN:
        pf = [os.environ.get("ProgramFiles", r"C:\Program Files"), os.environ.get("ProgramFiles(x86)", "")]
        for b in pf:
            if b: cands += sorted(glob.glob(os.path.join(b, "Blender Foundation", "Blender *", "blender.exe")), reverse=True)
        cands += glob.glob(os.path.expanduser(r"~\AppData\Local\Microsoft\WindowsApps\blender*.exe"))
    elif MAC:
        cands += ["/Applications/Blender.app/Contents/MacOS/Blender",
                  os.path.expanduser("~/Applications/Blender.app/Contents/MacOS/Blender")]
    melhor = (None, None)
    for c in cands:
        if not c or not os.path.exists(c): continue
        try:
            out = subprocess.run([c, "--version"], capture_output=True, text=True, timeout=60).stdout
        except Exception:
            continue
        m = re.search(r"Blender (\d+)\.(\d+)", out)
        if m:
            v = (int(m.group(1)), int(m.group(2)))
            if melhor[1] is None or v > melhor[1]: melhor = (c, v)
    return melhor


def memoria_gb():
    """RAM total do computador em GB (para decidir quantas partes renderizar ao mesmo tempo)."""
    try:
        if WIN:
            import ctypes
            class M(ctypes.Structure):
                _fields_ = [("l", ctypes.c_ulong), ("load", ctypes.c_ulong), ("total", ctypes.c_ulonglong),
                            ("a", ctypes.c_ulonglong), ("b", ctypes.c_ulonglong), ("c", ctypes.c_ulonglong),
                            ("d", ctypes.c_ulonglong), ("e", ctypes.c_ulonglong), ("f", ctypes.c_ulonglong)]
            m = M(); m.l = ctypes.sizeof(M); ctypes.windll.kernel32.GlobalMemoryStatusEx(ctypes.byref(m))
            return m.total / 2**30
        if MAC:
            import subprocess
            return int(subprocess.run(["sysctl", "-n", "hw.memsize"], capture_output=True, text=True).stdout) / 2**30
        return os.sysconf("SC_PAGE_SIZE") * os.sysconf("SC_PHYS_PAGES") / 2**30
    except Exception:
        return 8.0
