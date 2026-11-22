import sys, json
from faster_whisper import WhisperModel
src, out = sys.argv[1:3]
m = WhisperModel("medium", device="cpu", compute_type="int8")
segs, info = m.transcribe(src, language="pt", word_timestamps=True,
    initial_prompt="pet shop, tutor, banho, secagem, shampoo, pelo, laço, agendamento, tranquilidade, IA")
W = []
for s in segs:
    for w in s.words:
        W.append({"w": w.word.strip(), "s": round(w.start, 3), "e": round(w.end, 3)})
json.dump(W, open(out, "w", encoding="utf-8"), ensure_ascii=False, indent=0)
print(info.duration, len(W))
for x in W:
    print(f'{x["s"]:6.2f} {x["w"]}')
