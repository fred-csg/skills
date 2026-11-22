# Utilitários de áudio (decodifica via ffmpeg, mixa em numpy).
# Sons: procura na biblioteca do usuário (se configurada, ver ambiente.pastas_sfx);
# se não achar, gera por código (sfx_synth.py). Assim a skill funciona em qualquer computador.
import subprocess, numpy as np, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ambiente import ffmpeg, pastas_sfx
import sfx_synth

FFM = ffmpeg()
SR = 48000
EXT = (".wav", ".aac", ".mp3", ".flac", ".ogg", ".aif", ".aiff", ".m4a")

_cache = {}
def load(path):
    if path in _cache: return _cache[path]
    if path.startswith("synth:"):
        a = sfx_synth.synth(path[6:])
    else:
        raw = subprocess.run([FFM, "-v", "error", "-i", path, "-f", "f32le", "-ac", "2", "-ar", str(SR), "-"],
                             capture_output=True, check=True).stdout
        a = np.frombuffer(raw, dtype=np.float32).reshape(-1, 2).copy()
    _cache[path] = a
    return a

_avisou = False
def find(name, root=None):
    """Acha o som pelo trecho do nome na biblioteca do usuário; se não houver, devolve um som gerado por código."""
    global _avisou
    if os.path.exists(name): return name
    n = name.lower()
    for r in ([root] if root else pastas_sfx()):
        for dp, _, fs in os.walk(r):
            for f in fs:
                if f.lower().endswith(EXT) and n in f.lower(): return os.path.join(dp, f)
    if not _avisou:
        print("sons: usando efeitos gerados por código" + (" (alguns nomes não estão na biblioteca)" if pastas_sfx() else ""))
        _avisou = True
    return "synth:" + name

def env_db(a, win=0.02):
    m = np.abs(a).max(axis=1); n = int(SR * win)
    k = len(m) // n
    return 20 * np.log10(m[:k * n].reshape(k, n).max(axis=1) + 1e-9)

def peak_idx(a, within=None):
    m = np.abs(a).max(axis=1)
    if within: m = m[:int(within * SR)]
    return int(m.argmax())

def onset_idx(a, thresh_db=-30):
    m = np.abs(a).max(axis=1); pk = m.max()
    idx = np.where(m > pk * 10 ** (thresh_db / 20))[0]
    return int(idx[0]) if len(idx) else 0
