# moldura-pop · mixagem do exemplo: voz original + SFX SUTIS (−14 a −24 dB) em cada entrada de elemento.
# Sons: biblioteca do usuário (sfx_pasta.txt) se houver; senão gerados por código. Nunca riser antes de revelação.
# Uso: python mix.py <video_fonte> <out.wav> <duracao>
import sys, os, numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from sfx_lib import *

src, out_p, DUR = sys.argv[1], sys.argv[2], float(sys.argv[3])
N = int(DUR * SR)
voz = load(src)[:N]
bus = np.zeros((N, 2), np.float32); bus[:len(voz)] += voz
sfx = np.zeros((N, 2), np.float32)
def db(g): return 10 ** (g / 20)

def place(name, t, gain=-18, align="onset", start=0.0, length=None, fout=0.12):
    a = load(find(name))[int(start * SR):]
    if length: a = a[:int(length * SR)]
    a = a.copy(); nfo = max(1, min(len(a) - 1, int(fout * SR)))
    a[:64] *= np.linspace(0, 1, 64)[:, None]; a[-nfo:] *= np.linspace(1, 0, nfo)[:, None]
    off = peak_idx(a) if align == "peak" else (onset_idx(a) if align == "onset" else 0)
    i0 = int(t * SR) - off; j0, j1 = max(0, i0), min(N, i0 + len(a))
    if j1 > j0: sfx[j0:j1] += a[j0 - i0:j1 - i0] * db(gain)

CLK = "Very Short Click_Camera"; CLK2 = "Short Click_Camera"; SHUT = "Single Click Shutter"
HIT = "Camera Clicks, Low Impact, Mech Double Hit"; PAPER = "DSGNWhsh_Paper Whoosh"; CRISP = "Crispy Small Whoosh"
GEAR = "Multi Small Gear Rotation, Double Low Whoosh"; DPW = "Distorted Paper Whoosh"
CHIME = "UI Bright Chime"; TYPE = "Computer Keyboard Quick Typing"; MINI = "Modern Minimize"

# transições de cena (claro<->escuro mais encorpadas, as outras só um sopro)
for t, nm, g in [(4.02, GEAR, -19), (6.22, CRISP, -17), (8.28, MINI, -19), (11.16, CRISP, -17),
                 (14.55, GEAR, -19), (20.40, CRISP, -17), (24.62, MINI, -20)]:
    place(nm, t - 0.18, g, length=1.0, fout=.35)
# 1 · gancho
place(CRISP, 0.05, -21, length=.5); place(PAPER, 0.28, -19, length=.6)
place(CLK, 1.22, -15); place(CLK, 1.42, -16); place(CLK2, 2.44, -16)
# 2 · fotógrafo
place(HIT, 4.55, -14, length=1.0, fout=.4); place(DPW, 4.95, -16, length=.35); place(CLK, 5.2, -19)
# 3 · spoiler
place(CLK, 6.42, -18); place(CLK2, 7.10, -20)
# 4 · Doutor Estranho
place(PAPER, 8.55, -21, length=.6); place(CLK2, 9.45, -19)
for i in range(10): place(CLK, 10.0 + i * 0.06, -25)
place(HIT, 10.92, -16, length=.9, fout=.3)
# 5 · herança
place(CLK2, 11.3, -18); place(SHUT, 11.82, -15); place(CLK2, 13.2, -18); place(SHUT, 13.5, -15)
place(HIT, 14.0, -15, length=.9, fout=.3)
# 6 · Nova York
place(PAPER, 14.85, -21, length=.6); place(PAPER, 16.3, -16, length=.6); place(CLK, 17.4, -20)
place("Stopwatch Clicks_Cinematic", 18.0, -19, length=.85, fout=.2); place(CHIME, 18.85, -17, length=1.2, fout=.4)
place(DPW, 19.36, -18, length=.35)
# 7 · apê
for i in range(3): place(CLK, 21.45 + i * 0.12, -18)
place(HIT, 22.62, -14, length=.9, fout=.3); place(CLK, 22.85, -18); place(CLK2, 23.46, -20); place(SHUT, 24.02, -15)
# 8 · CTA
place(CRISP, 24.75, -18, length=.5); place(TYPE, 24.95, -20, length=1.0, fout=.25); place(CLK, 25.75, -17)

mixd = bus + sfx * db(-1)
pk = np.abs(mixd).max(); mixd *= db(-1) / pk
nf = int(0.3 * SR); mixd[-nf:] *= np.linspace(1, 0, nf)[:, None]
raw = (np.clip(mixd, -1, 1) * 32767).astype("<i2").tobytes()
import wave
w = wave.open(out_p, "wb"); w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(raw); w.close()
print("ok", out_p)
