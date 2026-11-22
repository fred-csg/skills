import json, sys, time
from faster_whisper import WhisperModel
src = sys.argv[1]
t0 = time.time()
try:
    m = WhisperModel("large-v3", device="cpu", compute_type="int8", cpu_threads=16); dev = "cpu"
except Exception as e:
    print("cuda falhou:", e); m = WhisperModel("medium", device="cpu", compute_type="int8"); dev = "cpu"
segs, info = m.transcribe(src, language="pt", word_timestamps=True, vad_filter=True, beam_size=5)
words = []
for s in segs:
    for w in s.words:
        words.append({"w": w.word.strip(), "a": round(w.start, 3), "b": round(w.end, 3), "p": round(w.probability, 2)})
json.dump(words, open("palavras.json", "w", encoding="utf8"), ensure_ascii=False, indent=0)
print(dev, f"{time.time()-t0:.1f}s", len(words), "palavras")
print(" ".join(f"{x['w']}[{x['a']}]" for x in words))
