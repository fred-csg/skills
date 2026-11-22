"""Hand Drawing — mixagem: risco de marcador/giz em cada traço + whoosh nas trocas de quadro + pop nas fotos.

uso: python -I mix.py <cues.json> <saida.wav> <duracao_s> [--voz voz.wav] [--trilha musica.wav] [--risco-db -32]

O render.mjs exporta cues.json: {t, type, dur?}. 'risco' é tocado por trechos de um loop longo
(marcador ou giz, conforme a ferramenta do tema), com fade curto e leve variação de volume.
Todos os sons ficam em assets/sfx/ (gerados no ElevenLabs pra esta skill): risco_marcador, risco_giz, whoosh, pop.
"""
import json, os, subprocess, sys
import numpy as np

SR = 48000
FF = os.environ.get("FFMPEG", "ffmpeg")
AQUI = os.path.dirname(os.path.abspath(__file__))
SFX = os.path.join(AQUI, "..", "assets", "sfx")
UNICO = {  # tipo: (arquivos, alinhamento, deslocamento, dB, duração máx) — sons embutidos em assets/sfx
    "whoosh": ([os.path.join(SFX, "whoosh.mp3")], "peak", 0, -13, 1.0),
    "pop":    ([os.path.join(SFX, "pop.mp3")], "onset", 0, -14, .5),
}


def load(path, maxdur=None):
    cmd = [FF, "-v", "error", "-i", path, "-ac", "2", "-ar", str(SR), "-f", "f32le", "-"]
    if maxdur: cmd[5:5] = ["-t", str(maxdur + .5)]
    return np.frombuffer(subprocess.run(cmd, capture_output=True, check=True).stdout, np.float32).reshape(-1, 2).copy()


def prep(a, align, maxdur):
    env = np.abs(a).max(1)
    if align == "onset":
        on = int(np.argmax(env > env.max() * .08)); a = a[max(0, on - int(.004 * SR)):]; ref = int(.004 * SR)
    else:
        ref = int(np.argmax(env))
    n = int(maxdur * SR)
    if len(a) > n:
        a = a[:n]; f = min(len(a), int(.08 * SR)); a[-f:] *= np.linspace(1, 0, f)[:, None]
    return a / (np.abs(a).max() + 1e-9), ref


def main():
    args = sys.argv[1:]
    def opt(n, d=None):
        if n in args: i = args.index(n); v = args[i + 1]; del args[i:i + 2]; return v
        return d
    voz, trilha, risco_db = opt("--voz"), opt("--trilha"), float(opt("--risco-db", -32))
    cues_p, out, dur = args[0], args[1], float(args[2])
    cues = json.load(open(cues_p, encoding="utf-8"))
    ferr = next((c["ferramenta"] for c in cues if "ferramenta" in c), "marcador")
    bus = np.zeros((int((dur + 2) * SR), 2), np.float32)

    # loop de escrita normalizado por RMS (o arquivo tem respiros; usamos só os trechos com som)
    loop = load(os.path.join(SFX, f"risco_{ferr}.mp3"))
    env = np.convolve(np.abs(loop).mean(1), np.ones(480) / 480, "same")
    vivo = np.nonzero(env > env.max() * .12)[0]
    rms = np.sqrt((loop[vivo] ** 2).mean()) + 1e-9
    loop = loop / rms
    rng = np.random.default_rng(3)
    for c in cues:
        if c.get("type") != "risco": continue
        n = int(c["dur"] * SR) + int(.03 * SR)
        st = int(rng.integers(0, max(1, len(loop) - n - 1)))
        trecho = loop[st:st + n].copy()
        if len(trecho) < n: trecho = np.concatenate([trecho, loop[:n - len(trecho)]])
        f = min(n // 3, int(.025 * SR))
        trecho[:f] *= np.linspace(0, 1, f)[:, None]; trecho[-f:] *= np.linspace(1, 0, f)[:, None]
        g = 10 ** ((risco_db + rng.uniform(-1.5, 1.5)) / 20)
        i0 = int(c["t"] * SR); i1 = min(len(bus), i0 + n)
        bus[i0:i1] += trecho[:i1 - i0] * g

    cache, count = {}, {}
    for c in sorted([c for c in cues if c.get("type") in UNICO], key=lambda c: c["t"]):
        files, align, shift, g, md = UNICO[c["type"]]
        k = count.get(c["type"], 0); count[c["type"]] = k + 1
        f = files[k % len(files)]
        if not os.path.exists(f): continue
        if f not in cache: cache[f] = prep(load(f, md if align == "onset" else None), align, md)
        a, ref = cache[f]
        start = int((c["t"] + shift) * SR) - ref
        if start < 0: a = a[-start:]; start = 0
        end = min(len(bus), start + len(a))
        bus[start:end] += a[:end - start] * 10 ** ((g + c.get("gain", 0)) / 20)
    bus = bus[:int(dur * SR)]
    if voz:
        v = load(voz)[:len(bus)]; r = np.sqrt((v ** 2).mean()) + 1e-9
        bus[:len(v)] += v * (10 ** (-16 / 20) / r)
    if trilha:
        m = load(trilha)[:len(bus)]; r = np.sqrt((m ** 2).mean()) + 1e-9
        bus[:len(m)] += m * (10 ** ((-28 if voz else -21) / 20) / r)
    pk = np.abs(bus).max()
    if pk > .89: bus *= .89 / pk
    tmp = out + ".raw"; bus.astype(np.float32).tofile(tmp)
    subprocess.run([FF, "-y", "-v", "error", "-f", "f32le", "-ar", str(SR), "-ac", "2", "-i", tmp, "-c:a", "pcm_s16le", out], check=True)
    os.remove(tmp)
    print(f"ok -> {out}  (ferramenta {ferr}, {sum(c.get('type') == 'risco' for c in cues)} riscos)")


if __name__ == "__main__":
    main()
