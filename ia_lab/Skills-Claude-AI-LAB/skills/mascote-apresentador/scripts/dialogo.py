"""Monta a locução em DIÁLOGO (apresentador x mascote) a partir de dois áudios do ElevenLabs.

uso: python -I dialogo.py <roteiro.txt> <perguntas.mp3> <mascote.mp3> <pasta_audio> [tom_mascote=1.30] [respiro=0.22]
  roteiro.txt — uma fala por linha, na ordem do vídeo, começando com "P:" (apresentador) ou "M:" (mascote):
      P: Opa... quem é você?
      M: Oi! Eu sou o Faísca!
  perguntas.mp3 — TODAS as falas P, na ordem (um TTS só, falas separadas por linha em branco).
  mascote.mp3   — TODAS as falas M, na ordem.
  tom_mascote — 1.30 ≈ +4,5 semitons (voz de personagem, mesmo ritmo). 1 = sem mudar.
Os cortes são feitos pelas palavras (faster-whisper): cada fala pega o mesmo número de palavras do texto.
Saída: locucao.mp3 (mix), voz_mascote.wav (só o mascote → boca.py), falas.json ([{quem, txt, ini, fim}]).
"""
import json, re, subprocess, sys
import numpy as np
from faster_whisper import WhisperModel

rot, perg, masc, pasta = sys.argv[1:5]
tom = float(sys.argv[5]) if len(sys.argv) > 5 else 1.30
respiro = float(sys.argv[6]) if len(sys.argv) > 6 else 0.22
SR = 44100
sys.stdout.reconfigure(encoding="utf-8")
L = [(l[0].upper(), l[2:].strip()) for l in open(rot, encoding="utf8").read().splitlines() if re.match(r"^[PMpm]:", l)]
nw = lambda s: len(re.findall(r"[\wÀ-ÿ]+", s))

def ler(f, filtro=None):
    cmd = ["ffmpeg", "-v", "error", "-i", f] + (["-af", filtro] if filtro else []) + ["-ac", "1", "-ar", str(SR), "-f", "f32le", "-"]
    return np.frombuffer(subprocess.run(cmd, capture_output=True, check=True).stdout, np.float32).copy()

wm = WhisperModel("small", device="cpu", compute_type="int8")
def cortar(f, textos, filtro=None):
    x = ler(f, filtro)
    tmp = f + ".tmp.wav"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "f32le", "-ar", str(SR), "-ac", "1", "-i", "-", tmp], input=x.tobytes(), check=True)
    segs, _ = wm.transcribe(tmp, language="pt", word_timestamps=True, initial_prompt=" ".join(textos))
    ws = [w for s in segs for w in s.words if re.search(r"[\wÀ-ÿ]", w.word)]
    out, k = [], 0
    for i, tx in enumerate(textos):
        n = nw(tx); grupo = ws[k:k + n]; k += n
        if not grupo: sys.exit(f"ERRO: faltaram palavras no áudio para: {tx}")
        a = grupo[0].start - 0.06
        b = (ws[k].start - 0.04) if k < len(ws) else len(x) / SR
        b = min(b, grupo[-1].end + 0.25)
        out.append(x[int(max(0, a) * SR):int(b * SR)])
        print(f"  {tx[:40]:40s} ← {' '.join(w.word.strip() for w in grupo)[:50]}")
    if k != len(ws): print(f"  aviso: sobraram {len(ws) - k} palavras no fim de {f}")
    return out

print("apresentador:"); P = cortar(perg, [t for q, t in L if q == "P"])
print("mascote:"); M = cortar(masc, [t for q, t in L if q == "M"], f"rubberband=pitch={tom}:formant=preserved" if tom != 1 else None)
mix, so_m, info, t, ip, im = [], [], [], 0.12, 0, 0
z = np.zeros(int(SR * 0.12), np.float32); mix.append(z); so_m.append(z)
for q, tx in L:
    a = P[ip] if q == "P" else M[im]; ip += q == "P"; im += q == "M"
    info.append({"quem": q, "txt": tx, "ini": round(t, 3), "fim": round(t + len(a) / SR, 3)})
    mix.append(a); so_m.append(a if q == "M" else np.zeros_like(a))
    g = np.zeros(int(SR * respiro), np.float32); mix.append(g); so_m.append(g)
    t += len(a) / SR + respiro
mix = np.concatenate(mix + [np.zeros(SR // 2, np.float32)]); so_m = np.concatenate(so_m + [np.zeros(SR // 2, np.float32)])
def gravar(x, f, extra):
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "f32le", "-ar", str(SR), "-ac", "1", "-i", "-"] + extra + [f], input=x.tobytes(), check=True)
gravar(mix, f"{pasta}/locucao.mp3", ["-b:a", "192k"]); gravar(so_m, f"{pasta}/voz_mascote.wav", [])
json.dump(info, open(f"{pasta}/falas.json", "w", encoding="utf8"), ensure_ascii=False, indent=0)
for k, s in enumerate(info): print(f"{k:2d} {s['quem']} {s['ini']:6.2f}-{s['fim']:6.2f}  {s['txt']}")
print(f"total {t:.2f}s")
