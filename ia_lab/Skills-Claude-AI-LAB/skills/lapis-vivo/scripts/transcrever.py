"""Lápis Vivo — tempos palavra a palavra da locução → words.js (lido pelo index.html).

uso: python -I transcrever.py <audio_ou_video> <pasta_projeto> [--modelo medium] [--texto copy.txt]

--texto: copy original. Corrige a grafia das palavras (acentos, nomes) mantendo os tempos do Whisper,
         quando o número de palavras bate; senão só avisa.
Também grava <pasta_projeto>/voz.wav (48 kHz) pra mixagem.
"""
import json, os, re, subprocess, sys

args = sys.argv[1:]
def opt(n, d=None):
    if n in args: i = args.index(n); v = args[i + 1]; del args[i:i + 2]; return v
    return d
modelo, texto = opt("--modelo", "medium"), opt("--texto")
src, proj = args
FF = os.environ.get("FFMPEG", "ffmpeg")
voz = os.path.join(proj, "voz.wav")
subprocess.run([FF, "-y", "-v", "error", "-i", src, "-vn", "-ac", "1", "-ar", "48000", voz], check=True)

from faster_whisper import WhisperModel
try:
    m = WhisperModel(modelo, device="cuda", compute_type="float16")
    segs, _ = m.transcribe(voz, language="pt", word_timestamps=True, vad_filter=False)
    segs = list(segs)
except Exception as e:
    print("GPU falhou, indo de CPU:", str(e)[:80])
    m = WhisperModel(modelo, device="cpu", compute_type="int8")
    segs, _ = m.transcribe(voz, language="pt", word_timestamps=True, vad_filter=False)
    segs = list(segs)
words = [{"w": w.word.strip(), "s": round(w.start, 3), "e": round(w.end, 3)} for s in segs for w in s.words if w.word.strip()]

if texto:
    ref = re.findall(r"\S+", open(texto, encoding="utf-8").read().replace("*", ""))
    if len(ref) == len(words):
        for w, r in zip(words, ref): w["w"] = r
        print("grafia corrigida pela copy")
    else:
        print(f"aviso: copy tem {len(ref)} palavras e a transcrição {len(words)} — mantive a do Whisper")

open(os.path.join(proj, "words.js"), "w", encoding="utf-8").write("window.WORDS = " + json.dumps(words, ensure_ascii=False) + ";\n")
dur = float(subprocess.run([FF.replace("ffmpeg", "ffprobe") if "ffmpeg" in FF else "ffprobe", "-v", "error", "-show_entries",
                            "format=duration", "-of", "csv=p=0", voz], capture_output=True, text=True).stdout or 0)
print(f"ok {len(words)} palavras, voz {dur:.2f}s")
for w in words: print(f"{w['s']:7.2f} {w['e']:7.2f}  {w['w']}")
