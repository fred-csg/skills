"""Tempos de cada palavra da locução (faster-whisper) + pausas (silencedetect), pra preencher o objeto W do template.

uso: python -I palavras.py <locucao.mp3> <saida.json> ["termos, que, aparecem, na, fala"]
Saída: imprime 'palavra@inicio-fim' e as pausas. Use o FIM DE CADA PAUSA como início da frase seguinte
(o whisper costuma adiantar o início da 1ª palavra depois de uma pausa).
GPU com erro de cublas → já roda em CPU int8.
"""
import json, re, subprocess, sys
from faster_whisper import WhisperModel

audio, out = sys.argv[1], sys.argv[2]
prompt = sys.argv[3] if len(sys.argv) > 3 else None
m = WhisperModel("small", device="cpu", compute_type="int8")
segs, _ = m.transcribe(audio, language="pt", word_timestamps=True, initial_prompt=prompt)
W = [{"w": w.word.strip(), "s": round(w.start, 3), "e": round(w.end, 3)} for s in segs for w in s.words]
json.dump(W, open(out, "w", encoding="utf8"), ensure_ascii=False, indent=0)
sys.stdout.reconfigure(encoding="utf-8")
print(" ".join(f'{x["w"]}@{x["s"]:.2f}-{x["e"]:.2f}' for x in W))
r = subprocess.run(["ffmpeg", "-hide_banner", "-i", audio, "-af", "silencedetect=n=-40dB:d=0.12", "-f", "null", "-"], capture_output=True, text=True, encoding="utf8", errors="ignore")
ini = re.findall(r"silence_start: ([\d.]+)", r.stderr); fim = re.findall(r"silence_end: ([\d.]+)", r.stderr)
print("pausas:", "  ".join(f"{float(a):.2f}→{float(b):.2f}" for a, b in zip(ini, fim)))
