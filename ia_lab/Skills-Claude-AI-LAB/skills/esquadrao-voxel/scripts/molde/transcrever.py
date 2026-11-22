# transcrever.py <locucao.mp3> <palavras.json> ["vocabulário, separado, por vírgula"]
# Tempo de cada palavra (faster-whisper medium, CPU). Imprime a lista pra montar o dicionário T.
import sys, json
from faster_whisper import WhisperModel
src, out = sys.argv[1:3]
vocab = sys.argv[3] if len(sys.argv) > 3 else ""
m = WhisperModel("medium", device="cpu", compute_type="int8")
segs, info = m.transcribe(src, language="pt", word_timestamps=True,
                          initial_prompt="Claude, Claudes, Reels, gancho, locução, motion, legenda, GUIA, IA. " + vocab)
W = []
for s in segs:
    for w in s.words:
        W.append({"w": w.word.strip(), "s": round(w.start, 3), "e": round(w.end, 3)})
json.dump(W, open(out, "w", encoding="utf-8"), ensure_ascii=False, indent=0)
print(round(info.duration, 2), "s,", len(W), "palavras")
for x in W:
    print(f'{x["s"]:6.2f} {x["e"]:6.2f} {x["w"]}')
