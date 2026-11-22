# Mixagem: locução + SFX. Sons da biblioteca do usuário (sfx_pasta.txt), se houver; senão gerados por código.
# Uso: python mix.py <voz.mp3> <meta.json> <out.wav>
import sys, os, json, subprocess, numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from sfx_lib import *

voz_p, meta_p, out_p = sys.argv[1:4]
meta = json.load(open(meta_p)); EV = meta["ev"]; T = meta["T"]
DUR = meta["nf"] / meta["fps"] + 0.05
N = int(DUR * SR)
bus_sfx = np.zeros((N, 2), np.float32)
bus_amb = np.zeros((N, 2), np.float32)
log = []

def db(g): return 10 ** (g / 20)

def place(name, t, gain=-12, align="peak", start=0.0, length=None, fin=0.005, fout=0.25, bus=None, pk_within=None):
    p = find(name); a = load(p)
    s0 = int(start * SR)
    a = a[s0:]
    if length: a = a[:int(length * SR)]
    a = a.copy()
    nfi = max(1, int(fin * SR)); nfo = max(1, min(len(a) - 1, int(fout * SR)))
    a[:nfi] *= np.linspace(0, 1, nfi)[:, None]
    a[-nfo:] *= np.linspace(1, 0, nfo)[:, None]
    if align == "peak": off = peak_idx(a, pk_within)
    elif align == "onset": off = onset_idx(a)
    elif align == "end": off = len(a)
    else: off = 0
    i0 = int(t * SR) - off
    b = bus if bus is not None else bus_sfx
    j0, j1 = max(0, i0), min(N, i0 + len(a))
    if j1 > j0: b[j0:j1] += a[j0 - i0:j1 - i0] * db(gain)
    log.append(f"{t:6.2f}  {gain:+4d}dB  {os.path.basename(p)}")

def slices(name, thresh_db=-16, min_gap=0.14, length=0.32):
    """Recorta golpes individuais (onsets) de um arquivo com vários eventos."""
    a = load(find(name)); m = np.abs(a).max(axis=1); pk = m.max()
    hop = int(0.005 * SR); env = m[:len(m) // hop * hop].reshape(-1, hop).max(axis=1)
    out, last = [], -1e9
    for i in range(1, len(env)):
        if env[i] > pk * db(thresh_db) and env[i - 1] <= pk * db(thresh_db) and (i - last) * 0.005 > min_gap:
            out.append(max(0, i * 0.005 - 0.01)); last = i
    return out

# ---------------------------------------------------------------- ambiente (cidade)
amb = load(find("Busy Street, People Passing By"))
reps = np.tile(amb, (int(np.ceil(N / len(amb))) + 1, 1))[:N].copy()
t = np.arange(N) / SR
g = np.full(N, db(-29), np.float32)
g *= np.clip(t / 0.8, 0, 1)
phone = (t > 33.4) & (t < 41.2)
g[phone] = db(-39)
g *= np.clip((DUR - t) / 2.5, 0, 1)
bus_amb += reps * g[:, None]

# ---------------------------------------------------------------- títulos de capítulo (mesma assinatura sonora)
for tt in (0.1, T["panf_title"], T["feed"], T["ad"], T["org"]):
    place("Camera Clicks, Low Impact, Mech Double Hit", tt + 0.08, -9, length=2.6, fout=0.9)

# ---------------------------------------------------------------- 1 · vitrine
place("Synth Bass Double Whoosh", 1.55, -14, length=3.6, fout=1.0)
place("Glitch 11_", 1.85, -21); place("Glitch 11_", 2.65, -22)
place("Metal Lever Activation", 6.78, -10)
place("Small Gear Rotation On Metal Surface", 6.7, -17, align="start", length=1.15, fout=0.35)
place("Treadmill Start Button", 7.35, -15, length=1.6, fout=0.6)
place("Multi Small Gear Rotation, Double Low Whoosh", 10.0, -13, fout=1.2)

# ---------------------------------------------------------------- 2 · panfleto
place("Medium Whoosh, Dark, Filtered", 16.7, -11)
flips = slices("Book Page Flip", -14, 0.12)
last = -9; k = 0
for tt in EV["pan"]:
    if tt - last < 0.17: continue
    far = 21.7 < tt < 25.7
    st = flips[k % len(flips)]; k += 1
    place("Book Page Flip", tt + 0.05, -24 if far else -18, align="onset", start=st, length=0.3, fout=0.12)
    last = tt
for tt in EV["land"]:
    near = tt > 25.9
    st = flips[(k + 3) % len(flips)]; k += 1
    place("Book Page Flip", tt, -19 if near else -27, align="onset", start=st, length=0.22, fout=0.1)
place("Multi Click Clock, Low Whoosh 1", 22.9, -16, fout=0.8)          # câmera sobe acompanhando
place("Medium Whoosh, Dark, Filtered", 26.4, -15)                     # desce na lixeira
place("Clock From Another World 6", 27.55, -12, align="start", length=2.75, fout=0.35)
place("Dry Break Impact, Crispy", 30.32, -9, length=2.0, fout=0.7)

# ---------------------------------------------------------------- 3 · feed
place("Time Control Clock, Pendulum", 32.55, -12, length=3.6, fout=1.0)
place("Mech Mini Gears, Camera Switch Buttons", 33.12, -14, align="onset", fout=0.5)
place("Short Whip, Short Whoosh 7_", 33.85, -11)
for tt in (36.95, 37.7):
    place("Short Whip, Short Whoosh 13", tt + 0.33, -13)
place("Medium Whoosh, Dark, Filtered", 39.75, -15)
place("Treadmill Parameter Button", 40.0, -15, align="onset", fout=0.4)
place("Short Whip, Short Whoosh 7_", 41.0, -13)

# ---------------------------------------------------------------- 4 · anúncio
place("Multi Click Clock, Low Whoosh 2", 42.2, -15, fout=0.8)
place("Mech Mini Gears Rotation 3", 41.78, -15, align="onset", fout=0.5)
drops = slices("Handling, Small Drops", -14, 0.1)
for k, ct in enumerate(EV["coins"]):
    if ct > 52: continue
    place("Handling, Small Drops", ct + 0.55, -19, align="onset", start=drops[k % len(drops)], length=0.25, fout=0.1)
place("Stopwatch That Goes Out Of Control, Metal Clicks, Rising", 43.9, -17, align="start", start=1.3, length=6.1, fin=0.3, fout=0.25)
place("Assembling Heavy Metal Parts, System Slowing", 49.97, -9, align="onset", length=4.2, fout=1.4)

# ---------------------------------------------------------------- 5 · orgânico
place("Granular Rocks, Multi Whoosh", 53.1, -17, fout=1.0)
shut = ["Clicky Shutter", "Cirpsy Short Shutter", "Crackling Shutter Short"]
for k, pt in enumerate(meta["placas"]):
    place(shut[k % 3], pt + 0.1, -13 if k < 6 else -16)
# (sem riser antes de revelação: preferência do usuário)

# ---------------------------------------------------------------- final
place("Agressive Impact, Alarm Clock Wing_", 65.02, -11, length=2.6, fout=0.9)
place("Stopwatch That Goes Out Of Control, Metal Clicks_", 64.95, -19, align="start", length=1.4, fin=0.05, fout=0.4)
place("Agressive Impact, Assembling Metal Parts, Slowing Down 1", 66.5, -11, length=3.2, fout=1.0)
place("Synth Bass Double Whoosh", 68.8, -16, length=3.6, fout=1.0)
place("Alarm Clock Wing, Weird High", 70.62, -10, length=2.0, fout=0.9)
place("Soft Transient, Deep Drum Hit", 70.62, -8, length=2.0, fout=0.8)

# ---------------------------------------------------------------- pops dos callouts (cliques suaves)
CALL_T = [1.8, 3.0, 7.3, 9.8, 12.6, 18.0, 22.2, 27.5, 29.9, 42.4, 46.0, 47.6, 50.0, 56.4, 57.6, 59.5, 60.6, 61.3, 64.98, 66.44, 68.6]
for k, tt in enumerate(CALL_T):
    place("Cirpsy Short Shutter" if k % 2 else "Clicky Shutter", tt + 0.14, -23)

# ---------------------------------------------------------------- voz + soma
voz = load(voz_p)
vm = np.abs(voz).max(axis=1)
active = vm > vm.max() * 0.05
rms = np.sqrt((voz[active] ** 2).mean())
voz = voz * (db(-17) / rms)
mix = bus_amb + bus_sfx
mix[:len(voz)] += voz[:N]
pk = np.abs(mix).max()
# limiter simples: comprime picos acima de -1.5 dBFS
thr = db(-1.5)
over = np.abs(mix) > thr
mix = np.where(over, np.sign(mix) * (thr + (1 - thr) * np.tanh((np.abs(mix) - thr) / (1 - thr))), mix)
mix = mix / max(1.0, np.abs(mix).max() / db(-1.0))
print(f"pico pré-limiter {20*np.log10(pk):.1f} dBFS; voz rms ajustada; {len(log)} eventos")
open(out_p + ".cues.txt", "w", encoding="utf8").write("\n".join(log))
subprocess.run([FFM, "-y", "-v", "error", "-f", "f32le", "-ar", str(SR), "-ac", "2", "-i", "-", "-c:a", "pcm_s16le", out_p],
               input=mix.astype(np.float32).tobytes(), check=True)
print("OK", out_p)
