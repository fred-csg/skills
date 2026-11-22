# Gera um .srt a partir de palavras.json (saída do transcrever.py).
# Uso: python gerar_srt.py palavras.json saida.srt [max_caracteres_por_legenda=32] [max_duracao_s=2.6]
# Quebra por pontuação, por pausa (> 0,35 s), por tamanho e por duração.
import json, sys

src, dst = sys.argv[1], sys.argv[2]
MAXC = int(sys.argv[3]) if len(sys.argv) > 3 else 32
MAXD = float(sys.argv[4]) if len(sys.argv) > 4 else 2.6
words = json.load(open(src, encoding='utf8'))

def ts(t):
    ms = int(round(t * 1000))
    h, ms = divmod(ms, 3600000)
    m, ms = divmod(ms, 60000)
    s, ms = divmod(ms, 1000)
    return f'{h:02d}:{m:02d}:{s:02d},{ms:03d}'

subs, cur = [], []
for k, w in enumerate(words):
    if cur:
        text = ' '.join(x['w'] for x in cur + [w])
        pause = w['a'] - cur[-1]['b'] > 0.35
        if pause or len(text) > MAXC or w['b'] - cur[0]['a'] > MAXD:
            subs.append(cur)
            cur = []
    cur.append(w)
    if w['w'][-1:] in '.!?,;:' and len(' '.join(x['w'] for x in cur)) > 12:
        subs.append(cur)
        cur = []
if cur:
    subs.append(cur)

out = []
for n, s in enumerate(subs, 1):
    a = s[0]['a']
    b = max(s[-1]['b'], a + 0.4)
    if n < len(subs):
        b = min(b + 0.15, subs[n][0]['a'] - 0.02)  # segura um pouco, sem encostar na próxima
    out.append(f"{n}\n{ts(a)} --> {ts(b)}\n{' '.join(x['w'] for x in s)}\n")
open(dst, 'w', encoding='utf8').write('\n'.join(out))
print(f'{len(subs)} legendas → {dst}')
