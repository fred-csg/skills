# Mixagem etiqueta-brutal: áudio original (voz) + SFX de UI/etiqueta.
# Preferência: COMPILED SELECTIONS, complemento: Ocular. Nunca riser antes de revelação.
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

def place(name, t, gain=-12, align="onset", start=0.0, length=None, fout=0.12):
    a = load(find(name))[int(start * SR):]
    if length: a = a[:int(length * SR)]
    a = a.copy(); nfo = max(1, min(len(a) - 1, int(fout * SR)))
    a[:64] *= np.linspace(0, 1, 64)[:, None]; a[-nfo:] *= np.linspace(1, 0, nfo)[:, None]
    off = peak_idx(a) if align == "peak" else (onset_idx(a) if align == "onset" else 0)
    i0 = int(t * SR) - off; j0, j1 = max(0, i0), min(N, i0 + len(a))
    if j1 > j0: sfx[j0:j1] += a[j0 - i0:j1 - i0] * db(gain)

CLK = "Very Short Click_Camera"; CLK2 = "Short Click_Camera"; SHUT = "Single Click Shutter"
HIT = "Camera Clicks, Low Impact, Mech Double Hit"; WHIP = "Cartoonish Whoosh, Whip"
PAPER = "DSGNWhsh_Paper Whoosh"; CRISP = "Crispy Small Whoosh"; FLIP = "Book Page Flip"
TONE = "Treadmill Start Button, Tone"

# gancho
place(HIT, 0.25, -9, length=1.2, fout=.5); place(CLK, 0.6, -8); place(CRISP, 0.55, -16, length=.5)
place(WHIP, 3.47, -7, align="peak", length=1.0, fout=.3)
place(PAPER, 3.84, -17, length=.5)
# legendas: tique suave no início de cada grupo
for tt in (3.80, 4.76, 5.74, 7.10, 8.22, 11.62, 12.92, 13.80, 14.88, 16.60, 18.34, 19.38, 20.12, 21.44, 22.28, 23.54):
    place(CLK, tt, -21)
# impulsionar
place(PAPER, 4.38, -14, length=.6); place(CLK2, 6.42, -12)
place("Clicky Potentionmeter", 6.45, -15, length=.38, fout=.1)
place(SHUT, 7.28, -8); place(TONE, 7.45, -13, length=.8, fout=.3)
# resultados + NADA
place(PAPER, 8.30, -14, length=.6)
place("Stopwatch Clicks_Cinematic", 8.45, -17, length=.9, fout=.2)
place("Dry Break Impact, Crispy", 9.80, -5, align="peak", length=2.4, fout=.8)
# post ruim multiplicando
place(CLK, 12.62, -9)
for i in range(8): place(CLK2 if i % 2 else CLK, 13.56 + i * .07, -15)
place(CRISP, 14.85, -14, length=.5)
# alcance × conteúdo
place(HIT, 16.06, -10, length=1.0, fout=.4); place("Distorted Paper Whoosh", 16.30, -15, length=.35)
place(CRISP, 16.72, -16, length=.5)
place("Agressive Impact, Alarm Clock Wing_Cinematic", 17.20, -9, align="peak", length=2.0, fout=.7)
place(CLK, 17.42, -12)
# panfletos
place("Multi Small Gear Rotation, Double Low Whoosh", 18.22, -11, length=1.2, fout=.4)
place(FLIP, 18.82, -11, length=.6, fout=.2); place(HIT, 19.42, -11, length=.9, fout=.3)
place(FLIP, 20.16, -11, length=.6, fout=.2); place(TONE, 20.90, -12, length=.8, fout=.3)
place(WHIP, 22.10, -11, align="peak", length=1.0, fout=.3)
# panfleto = vídeo + CTA
place(CLK, 24.10, -11); place("Metal Lever Activation", 24.42, -9, length=1.2, fout=.4)
place(HIT, 25.05, -8, length=1.2, fout=.5); place(CLK2, 25.20, -10)
for i in range(5): place(CLK, 25.55 + i * .08, -17)
place(SHUT, 26.0, -10)

m = bus + sfx * db(-1)
pk = np.abs(m).max(); m *= min(1, db(-1) / pk)
m[-int(.25 * SR):] *= np.linspace(1, 0, int(.25 * SR))[:, None]
import wave
with wave.open(out_p, "wb") as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
    w.writeframes((np.clip(m, -1, 1) * 32767).astype(np.int16).tobytes())
print("ok", out_p, f"pico {20*np.log10(pk):.1f} dB")
