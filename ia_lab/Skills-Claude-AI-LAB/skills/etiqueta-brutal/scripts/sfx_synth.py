# Efeitos sonoros gerados por código (numpy), para quem não tem biblioteca de sons.
# synth("Very Short Click_Camera") -> array estéreo float32 a 48 kHz.
# O nome é o mesmo que o mix.py usaria para procurar um arquivo; aqui ele escolhe a "receita" pelo tipo de som.
import numpy as np

SR = 48000
_rng = np.random.default_rng(7)


def _t(d): return np.arange(int(d * SR)) / SR
def _noise(d): return _rng.standard_normal(int(d * SR)).astype(np.float32)


def _lp(x, fc):
    """Passa-baixa de 1 polo. fc pode ser número ou array (filtro que varia no tempo)."""
    fc = np.broadcast_to(np.asarray(fc, np.float32), x.shape)
    a = 1 - np.exp(-2 * np.pi * fc / SR)
    y = np.empty_like(x); s = 0.0
    for i in range(len(x)):
        s += a[i] * (x[i] - s); y[i] = s
    return y


def _bp(x, lo, hi):
    """Passa-faixa por FFT (rápido, fixo)."""
    X = np.fft.rfft(x); f = np.fft.rfftfreq(len(x), 1 / SR)
    X[(f < lo) | (f > hi)] = 0
    return np.fft.irfft(X, len(x)).astype(np.float32)


def _env(n, a, d, curve=4.0):
    """Envelope ataque linear (a s) + queda exponencial (d s)."""
    t = np.arange(n) / SR
    e = np.where(t < a, t / max(a, 1e-4), np.exp(-(t - a) / max(d, 1e-4) * curve / 4))
    return e.astype(np.float32)


def _norm(x, peak=0.9):
    m = np.abs(x).max()
    return x * (peak / m) if m > 0 else x


def _stereo(x, width=0.0):
    """Mono -> estéreo; width > 0 descorrelaciona levemente os canais."""
    if width <= 0: return np.stack([x, x], 1).astype(np.float32)
    d = int(0.0006 * SR)
    r = np.concatenate([np.zeros(d, np.float32), x[:-d]])
    return np.stack([x, x * (1 - width) + r * width], 1).astype(np.float32)


def _place(dst, src, t):
    i = int(t * SR); j = min(len(dst), i + len(src))
    if j > i: dst[i:j] += src[:j - i]


# ------------------------------------------------------------------ receitas
def click(tone=3200, d=0.035, body=0.5):
    n = int(d * SR); t = _t(d)
    x = _bp(_noise(d), 1500, 9000) * _env(n, 0.0005, 0.006)
    x += body * np.sin(2 * np.pi * tone * t) * _env(n, 0.0005, 0.012)
    return _norm(x, 0.8)


def shutter():
    out = np.zeros(int(0.18 * SR), np.float32)
    _place(out, click(2600, 0.04, 0.4), 0.0)
    _place(out, click(1900, 0.05, 0.6) * 0.9, 0.055)
    x = _bp(_noise(0.18), 300, 2000) * _env(int(0.18 * SR), 0.002, 0.03) * 0.25
    return _norm(out + x, 0.85)


def impact(f0=110, f1=42, d=0.9, double=False):
    n = int(d * SR); t = _t(d)
    f = f1 + (f0 - f1) * np.exp(-t / 0.06)
    x = np.sin(2 * np.pi * np.cumsum(f) / SR) * _env(n, 0.002, 0.22)
    x += _bp(_noise(d), 800, 7000) * _env(n, 0.0005, 0.02) * 0.6
    x += _bp(_noise(d), 120, 900) * _env(n, 0.001, 0.08) * 0.3
    x = _norm(x, 0.9)
    if double:
        out = np.zeros(int((d + 0.09) * SR), np.float32)
        _place(out, x * 0.75, 0.0); _place(out, x, 0.09)
        return _norm(out, 0.9)
    return x


def whoosh(d=0.6, lo=300, hi=5000, peak_at=0.55, crackle=0.0, low=0.0):
    n = int(d * SR); t = _t(d); p = t / d
    shape = np.where(p < peak_at, (p / peak_at) ** 2, ((1 - p) / (1 - peak_at)) ** 1.6)
    fc = lo + (hi - lo) * shape
    x = _lp(_noise(d), fc) * shape
    if crackle:
        k = (_rng.random(n) < 0.004).astype(np.float32) * _rng.standard_normal(n).astype(np.float32)
        x += _bp(k, 2000, 9000) * shape * crackle * 4
    if low:
        x += np.sin(2 * np.pi * (55 + 40 * shape) * t) * shape * low
    return _norm(x, 0.85)


def chime(f=1320, d=1.2):
    n = int(d * SR); t = _t(d)
    x = (np.sin(2 * np.pi * f * t) + 0.5 * np.sin(2 * np.pi * f * 1.5 * t) * _env(n, 0.001, 0.35)
         + 0.25 * np.sin(2 * np.pi * f * 2.01 * t)) * _env(n, 0.003, 0.6)
    return _norm(x, 0.7)


def ticks(d=2.0, every=0.12, accel=1.0, tone=2600):
    out = np.zeros(int(d * SR), np.float32); t, step = 0.0, every
    while t < d - 0.05:
        _place(out, click(tone * _rng.uniform(.95, 1.05), 0.03, 0.6) * _rng.uniform(.7, 1), t)
        t += step; step = max(0.025, step / accel)
    return out


def typing(d=1.2):
    out = np.zeros(int(d * SR), np.float32); t = 0.0
    while t < d - 0.05:
        _place(out, click(_rng.uniform(1800, 3200), 0.03, 0.3) * _rng.uniform(.5, 1), t)
        t += _rng.uniform(0.045, 0.11)
    return out


def ratchet(d=1.0):
    """Engrenagem: tiques rápidos + sopro grave (Gear Rotation, Double Low Whoosh)."""
    out = whoosh(d, 150, 1800, 0.5, low=0.6) * 0.8
    tk = ticks(d, 0.035, 1.0, 1700)
    env = np.sin(np.pi * np.clip(_t(d) / d, 0, 1)) ** 1.5
    return _norm(out + tk[:len(out)] * env[:len(out)] * 0.5, 0.85)


def hits(n=6, gap=0.32, kind="paper"):
    """Arquivo com vários golpes separados (o mix recorta por onset): páginas, moedas."""
    out = np.zeros(int((n * gap + 0.4) * SR), np.float32)
    for i in range(n):
        s = whoosh(0.16, 800, 6000, 0.25, crackle=0.6) if kind == "paper" else click(_rng.uniform(3500, 5200), 0.12, 0.9)
        _place(out, s * _rng.uniform(.8, 1), i * gap + 0.05)
    return out


def ambiente_rua(d=12.0):
    """Ambiente urbano discreto: ruído rosado grave com variação lenta + passos/vozes abafados."""
    n = int(d * SR); t = _t(d)
    x = _bp(_noise(d), 60, 1400)
    x *= 0.75 + 0.25 * np.sin(2 * np.pi * 0.11 * t) * np.sin(2 * np.pi * 0.037 * t + 1)
    k = np.zeros(n, np.float32)
    for _ in range(int(d * 2.5)):
        _place(k, click(_rng.uniform(300, 700), 0.05, 0.8) * _rng.uniform(.1, .3), _rng.uniform(0, d - .1))
    return _norm(x + _bp(k, 100, 2500), 0.6)


def drop(d=1.6):
    """Algo 'desligando' / desacelerando (System Slowing Down)."""
    n = int(d * SR); t = _t(d)
    f = 180 * np.exp(-t / 0.5) + 35
    x = np.sin(2 * np.pi * np.cumsum(f) / SR) * _env(n, 0.005, 0.6)
    return _norm(x + impact(90, 40, d) * 0.6, 0.9)


# ------------------------------------------------------------------ nome do som -> receita
_REGRAS = [
    (("street", "ambien", "city", "urb"), lambda: ambiente_rua()),
    (("typing", "keyboard"), lambda: typing(1.4)),
    (("out of control", "rising"), lambda: ticks(8.0, 0.16, 1.035)),
    (("stopwatch", "clock", "pendulum"), lambda: ticks(3.0, 0.125)),
    (("page", "book", "paper flip"), lambda: hits(8, 0.3, "paper")),
    (("barbell", "coin", "drops", "moeda"), lambda: hits(8, 0.3, "metal")),
    (("slowing down", "system slow"), lambda: drop()),
    (("gear", "ratchet", "mech mini"), lambda: ratchet(1.2)),
    (("double hit", "double low", "assembling", "agressive", "aggressive"), lambda: impact(120, 40, 1.4, double=True)),
    (("impact", "hit", "drum", "break", "lever"), lambda: impact()),
    (("chime", "tone", "ding", "bell"), lambda: chime()),
    (("distorted",), lambda: whoosh(0.4, 600, 6000, 0.4, crackle=1.0)),
    (("paper whoosh", "paper"), lambda: whoosh(0.6, 500, 6500, 0.5, crackle=0.5)),
    (("synth bass", "bass"), lambda: whoosh(1.0, 120, 2500, 0.6, low=1.0)),
    (("minimize",), lambda: whoosh(0.35, 800, 7000, 0.3)),
    (("whip", "whoosh", "swipe", "swoosh"), lambda: whoosh(0.45, 400, 7000, 0.5)),
    (("shutter",), lambda: shutter()),
    (("very short click", "short shutter"), lambda: click(3600, 0.03)),
    (("click", "button", "pop", "switch"), lambda: click(2800, 0.045, 0.6)),
]
_cache = {}


def synth(name):
    n = name.lower()
    if n in _cache: return _cache[n]
    fn = next((f for keys, f in _REGRAS if any(k in n for k in keys)), lambda: click())
    a = _stereo(fn().astype(np.float32), 0.25)
    _cache[n] = a
    return a


if __name__ == "__main__":
    # Teste: gera um WAV com todos os sons em sequência.  python sfx_synth.py teste.wav
    import sys, wave
    nomes = ["Very Short Click_Camera", "Single Click Shutter", "Camera Clicks, Low Impact, Mech Double Hit",
             "Crispy Small Whoosh", "DSGNWhsh_Paper Whoosh", "Multi Small Gear Rotation, Double Low Whoosh",
             "Distorted Paper Whoosh", "UI Bright Chime", "Computer Keyboard Quick Typing", "Modern Minimize",
             "Stopwatch Clicks_Cinematic", "Book Page Flip", "Busy Street, People Passing By"]
    parts = []
    for nm in nomes:
        a = synth(nm)[: int(3 * SR)]
        parts += [a, np.zeros((int(0.4 * SR), 2), np.float32)]
    x = np.concatenate(parts) * 0.8
    w = wave.open(sys.argv[1] if len(sys.argv) > 1 else "sfx_teste.wav", "wb")
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
    w.writeframes((np.clip(x, -1, 1) * 32767).astype("<i2").tobytes()); w.close()
    print("ok", len(nomes), "sons")
