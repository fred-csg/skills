import sys as _s, os as _o
_s.path.insert(0, _o.path.dirname(_o.path.dirname(_o.path.abspath(__file__))))  # scripts/ (ambiente.py)
import ambiente
# Esquadrão Voxel — mixagem: voz + trilha (ducking) + SFX do ElevenLabs.
# mix(voz, trilha, cues, dur, out)   cues: [(arquivo, t, ganho_dB, alinhamento["start"|"peak"|"onset"], dur_max|None)]
import numpy as np, subprocess, os
FFM = ambiente.ffmpeg()
SR = 48000
_cache = {}
def load(p):
    if p in _cache: return _cache[p]
    r = subprocess.run([FFM, "-v", "error", "-i", p, "-f", "f32le", "-ac", "2", "-ar", str(SR), "-"], capture_output=True, check=True)
    a = np.frombuffer(r.stdout, np.float32).reshape(-1, 2).copy()
    _cache[p] = a; return a
def db(g): return 10 ** (g / 20)
def peak_idx(a):
    m = np.abs(a).max(axis=1); return int(np.argmax(m))
def onset_idx(a, th=0.25):
    m = np.abs(a).max(axis=1); pk = m.max() or 1
    i = np.argmax(m > pk * th); return int(i)

def mix(voz_p, trilha_p, cues, dur, out_p, sfx_dir, music_db=-14, duck_db=-9, music_fade_out=2.5, voice_offset=0.0, music_jump=None):
    N = int(dur * SR)
    out = np.zeros((N, 2), np.float32)
    # voz
    voz = load(voz_p)
    vm = np.abs(voz).max(axis=1); active = vm > vm.max() * 0.05
    voz = voz * (db(-17) / np.sqrt((voz[active] ** 2).mean()))
    v0 = int(voice_offset * SR)
    vv = np.zeros((N, 2), np.float32); n = min(len(voz), N - v0); vv[v0:v0 + n] = voz[:n]
    # envelope da voz p/ ducking (janela 0.25 s, ataque rápido, soltura lenta)
    env = np.abs(vv).max(axis=1)
    hop = 480; e = env[:len(env) // hop * hop].reshape(-1, hop).max(axis=1)
    on = (e > db(-34)).astype(np.float32)
    sm = np.zeros_like(on); s = 0
    for i, x in enumerate(on):
        s = s + (x - s) * (0.5 if x > s else 0.06); sm[i] = s
    g_duck = np.repeat(sm, hop); g_duck = np.pad(g_duck, (0, N - len(g_duck)), "edge")[:N]
    # trilha
    if trilha_p:
        mu = load(trilha_p)
        if music_jump:  # emenda: em cut_at, crossfade de 1 s para jump_to (estica trilhas curtas)
            ca, jt = int(music_jump[0] * SR), int(music_jump[1] * SR); xf = SR
            w = np.linspace(0, 1, xf)[:, None]
            mid = mu[ca:ca + xf] * (1 - w) + mu[jt:jt + xf] * w
            mu = np.concatenate([mu[:ca], mid, mu[jt + xf:]])
        if len(mu) < N: mu = np.concatenate([mu, np.zeros((N - len(mu), 2), np.float32)])
        mu = mu[:N]
        rms = np.sqrt((mu[:min(len(mu), SR * 20)] ** 2).mean()) or 1
        mu = mu * (db(-17) / rms)
        t = np.arange(N) / SR
        g = db(music_db) * (1 - g_duck * (1 - db(duck_db)))
        g *= np.clip(t / 0.6, 0, 1) * np.clip((dur - t) / music_fade_out, 0, 1)
        out += mu * g[:, None]
    log = []
    for c in cues:
        f, t0, gain, align = c[:4]; mx = c[4] if len(c) > 4 else None
        a = load(os.path.join(sfx_dir, f)).copy()
        if mx: a = a[:int(mx * SR)]
        nfo = min(len(a) - 1, int(0.12 * SR)); a[-nfo:] *= np.linspace(1, 0, nfo)[:, None]
        pk = np.abs(a).max() or 1; a = a / pk * db(-3)
        off = 0 if align == "start" else (peak_idx(a) if align == "peak" else onset_idx(a))
        i0 = int(t0 * SR) - off
        j0, j1 = max(0, i0), min(N, i0 + len(a))
        if j1 > j0: out[j0:j1] += a[j0 - i0:j1 - i0] * db(gain)
        log.append(f"{t0:6.2f} {gain:+4d} {f}")
    out += vv
    thr = db(-1.5)
    out = np.where(np.abs(out) > thr, np.sign(out) * (thr + (1 - thr) * np.tanh((np.abs(out) - thr) / (1 - thr))), out)
    out = out / max(1.0, np.abs(out).max() / db(-1.0))
    subprocess.run([FFM, "-y", "-v", "error", "-f", "f32le", "-ar", str(SR), "-ac", "2", "-i", "-", "-c:a", "pcm_s16le", out_p],
                   input=out.astype(np.float32).tobytes(), check=True)
    open(out_p + ".cues.txt", "w", encoding="utf8").write("\n".join(log))
    print("OK", out_p, len(log), "cues")
