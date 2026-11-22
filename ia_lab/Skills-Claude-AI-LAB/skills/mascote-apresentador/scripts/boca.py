"""Envelope da voz (30 valores por segundo, 0..1) pra boca do mascote mexer junto com a fala.

uso: python -I boca.py <locucao.mp3> <saida.js>
Saída: arquivo JS com `window.BOCA = [...]` (o index.html carrega com <script src="audio/boca.js">).
Sem locução: não crie o arquivo — o template usa uma boca "falando" sintética durante as legendas.
"""
import subprocess, sys, json
import numpy as np

audio, out = sys.argv[1], sys.argv[2]
SR, FPS = 16000, 30
raw = subprocess.run(["ffmpeg", "-v", "error", "-i", audio, "-ac", "1", "-ar", str(SR), "-f", "s16le", "-"],
                     capture_output=True, check=True).stdout
x = np.frombuffer(raw, np.int16).astype(np.float32) / 32768
# só a faixa da voz (200–3000 Hz) pra boca não abrir com sopro/respiração
X = np.fft.rfft(x); f = np.fft.rfftfreq(len(x), 1 / SR)
X[(f < 200) | (f > 3000)] = 0
x = np.fft.irfft(X, len(x))
hop = SR // FPS
n = len(x) // hop
rms = np.array([np.sqrt(np.mean(x[i * hop:(i + 1) * hop] ** 2)) for i in range(n)])
db = 20 * np.log10(rms + 1e-6)
ref = np.percentile(db[db > -60], 95) if np.any(db > -60) else -20
v = np.clip((db - (ref - 24)) / 24, 0, 1) ** 1.3
v = np.convolve(v, [0.25, 0.5, 0.25], "same")
open(out, "w", encoding="utf8").write("window.BOCA=" + json.dumps([round(float(a), 3) for a in v]) + ";\n")
print(f"{n} quadros ({n / FPS:.1f}s) -> {out}")
