import json,sys
from faster_whisper import WhisperModel
try: m=WhisperModel("large-v3",device="cpu",compute_type="int8")
except Exception as e:
    print("cpu",e); m=WhisperModel("medium",device="cpu",compute_type="int8")
segs,_=m.transcribe(sys.argv[1],language="pt",word_timestamps=True)
W=[]
for s in segs:
    print(f"[{s.start:.2f}-{s.end:.2f}] {s.text}")
    for w in s.words: W.append(dict(w=w.word.strip(),s=round(w.start,2),e=round(w.end,2)))
json.dump(W,open(sys.argv[2],"w",encoding="utf8"),ensure_ascii=False,indent=0)
