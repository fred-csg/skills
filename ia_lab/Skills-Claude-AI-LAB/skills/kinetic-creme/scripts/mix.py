"""Kinetic Creme — mixagem de SFX a partir do cues.json que o render.mjs exporta.

uso: python mix.py <cues.json> <saida.wav> <duracao_s> [--voz voz.wav] [--trilha musica.wav]

Cada cue = {t, type, gain}. O tipo escolhe o arquivo (SOUNDS) e como alinhar:
  onset -> o começo audível do som cai em t   (cliques, pops, digitação)
  peak  -> o pico do som cai em t + shift      (whooshes, impactos)
Só usa SFX reais do acervo (nunca sintetizados). Sem riser antes de revelação.
"""
import json, subprocess, sys, os, numpy as np

SR = 48000
FAV = r"E:\Dropbox\ADDONS\SFX\COMPILED SELECTIONS"
OC = r"E:\Dropbox\ADDONS\SFX\Ocular Sounds\Ocular Sounds\Sound Effects - The Ultimate Sound FX Bundle (All in One)\The Ultimate Sound FX Bundle"
WHIP = OC + r"\The Complete Whooshes Collection\Quick Whips\DSGNWhsh_Short Whip, Short Whoosh {}_Quick Whips.wav"
CAM = OC + r"\The Complete Devices Collection\Camera Shutters\COMCam_{}_Camera Shutters.wav"

# tipo: (arquivos alternados, alinhamento, deslocamento s, ganho dB, duração máx s)
SOUNDS = {
    "whoosh":      ([WHIP.format(n) for n in (3, 7, 12, 16)], "peak", .2, -9, 1.0),
    "whoosh_soft": ([WHIP.format(n) for n in (5, 9)], "peak", .25, -17, .9),
    "swipe":       ([WHIP.format(n) for n in (14, 19)], "peak", .12, -19, .6),
    "pop":         ([CAM.format("Very Short Click"), CAM.format("Short Click")], "onset", 0, -11, .35),
    "flick":       ([CAM.format("Pre Shifted Very Short Metal Click")], "onset", 0, -20, .3),
    "type":        ([CAM.format("Very Short Click"), CAM.format("Pre Shifted Very Short Metal Click")], "onset", 0, -23, .2),
    "tick":        ([CAM.format("Pre Shifted Very Short Metal Click")], "onset", 0, -26, .15),
    "click":       ([CAM.format("Single Click Shutter")], "onset", 0, -10, .5),
    "impact":      ([FAV + r"\COMCam_Camera Clicks, Low Impact, Mech Double Hit_Cinematic Mechanics.wav"], "onset", -.01, -5, 1.6),
    "ding":        ([FAV + r"\MACHGym_Foley Kit, Treadmill Start Button, Tone_Cinematic Gym.wav"], "onset", 0, -9, 1.4),
}
FFMPEG = os.environ.get("FFMPEG", "ffmpeg")


sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ambiente import ffmpeg as _achar_ffmpeg
import sfx_synth
if FFMPEG == "ffmpeg":
    try: FFMPEG = _achar_ffmpeg()
    except SystemExit: pass

# Sem a biblioteca de sons do autor (outro computador), cada tipo de cue usa um som gerado por código.
SINTETICO = {"whoosh": "Short Whoosh", "whoosh_soft": "Crispy Small Whoosh", "swipe": "Quick Whip",
             "pop": "Very Short Click", "flick": "Very Short Click", "type": "Very Short Click",
             "tick": "Very Short Click", "click": "Single Click Shutter", "impact": "Mech Double Hit",
             "ding": "UI Bright Chime"}
_avisou = [False]


def load(path, maxdur=None):
    if not os.path.exists(path):
        tipo = next((t for t, v in SOUNDS.items() if path in v[0]), "pop")
        if not _avisou[0]: print("sons: usando efeitos gerados por código"); _avisou[0] = True
        a = sfx_synth.synth(SINTETICO.get(tipo, "click"))
        return a[: int((maxdur + .5) * SR)] if maxdur else a
    cmd = [FFMPEG, "-v", "error", "-i", path, "-ac", "2", "-ar", str(SR), "-f", "f32le", "-"]
    if maxdur: cmd[5:5] = ["-t", str(maxdur + .5)]
    a = np.frombuffer(subprocess.run(cmd, capture_output=True, check=True).stdout, np.float32).reshape(-1, 2).copy()
    return a


def prep(a, align, maxdur):
    env = np.abs(a).max(1)
    on = int(np.argmax(env > env.max() * .08))
    if align == "onset":
        a = a[max(0, on - int(.004 * SR)):]
        ref = int(.004 * SR)
    else:
        ref = int(np.argmax(env))
    n = int(maxdur * SR)
    if len(a) > n:  # corta com fade-out
        a = a[:n]; f = min(len(a), int(.08 * SR)); a[-f:] *= np.linspace(1, 0, f)[:, None]
    return a / (np.abs(a).max() + 1e-9), ref


def main():
    args = sys.argv[1:]
    def opt(n):
        if n in args: i = args.index(n); v = args[i + 1]; del args[i:i + 2]; return v
    voz, trilha = opt("--voz"), opt("--trilha")
    cues_p, out, dur = args[0], args[1], float(args[2])
    cues = json.load(open(cues_p, encoding="utf-8"))
    bus = np.zeros((int((dur + 1) * SR), 2), np.float32)
    cache, count = {}, {}
    for c in sorted(cues, key=lambda c: c["t"]):
        if c["type"] not in SOUNDS: continue
        files, align, shift, g, md = SOUNDS[c["type"]]
        k = count.get(c["type"], 0); count[c["type"]] = k + 1
        f = files[k % len(files)]
        if f not in cache: cache[f] = prep(load(f, md if align == "onset" else None), align, md)
        a, ref = cache[f]
        start = int((c["t"] + shift) * SR) - ref
        if start < 0: a = a[-start:]; start = 0
        end = min(len(bus), start + len(a))
        vari = 1 + .08 * ((k * 7919) % 5 - 2) / 2  # leve variação de volume em repetições
        bus[start:end] += a[:end - start] * (10 ** ((g + c.get("gain", 0)) / 20)) * vari
    bus = bus[:int(dur * SR)]
    if voz:
        v = load(voz)[:len(bus)]; rms = np.sqrt((v ** 2).mean()) + 1e-9
        bus[:len(v)] += v * (10 ** (-17 / 20) / rms)
    if trilha:
        m = load(trilha)[:len(bus)]; rms = np.sqrt((m ** 2).mean()) + 1e-9
        bus[:len(m)] += m * (10 ** ((-27 if voz else -21) / 20) / rms)
    peak = np.abs(bus).max()
    if peak > .89: bus *= .89 / peak  # teto ~ -1 dBFS
    tmp = out + ".raw"
    bus.astype(np.float32).tofile(tmp)
    subprocess.run([FFMPEG, "-y", "-v", "error", "-f", "f32le", "-ar", str(SR), "-ac", "2", "-i", tmp, "-c:a", "pcm_s16le", out], check=True)
    os.remove(tmp)
    print(f"ok -> {out}  ({len(cues)} cues, pico {20 * np.log10(np.abs(bus).max() + 1e-9):.1f} dBFS)")


if __name__ == "__main__":
    main()
