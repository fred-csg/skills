# legenda.py <palavras.json> <legenda.json> '{"leu":"lê"}' [drop_before_IA]
import json, sys
W = json.load(open(sys.argv[1], encoding="utf-8")); fix = json.loads(sys.argv[3]) if len(sys.argv) > 3 else {}
out = []; i = 0
while i < len(W):
    w = dict(W[i]); base = w["w"].strip(".,?!:")
    nx = W[i + 1]["w"] if i + 1 < len(W) else ""
    if base.lower() == "para" and nx == "o": out.append(dict(w="pro", s=w["s"], e=W[i + 1]["e"])); i += 2; continue
    if base == "o" and nx.startswith("IA"): i += 1; continue
    if base.lower() in fix: w["w"] = w["w"].replace(base, fix[base.lower()])
    out.append(w); i += 1
json.dump(out, open(sys.argv[2], "w", encoding="utf-8"), ensure_ascii=False)
print(len(W), "->", len(out))
