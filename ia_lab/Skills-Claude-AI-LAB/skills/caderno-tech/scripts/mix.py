# Mixagem automática do caderno-tech: lê o roteiro e põe um som em cada coisa que aparece ou se move.
#   python mix.py roteiro.py mix.wav [--sfx_db -1] [--sem_voz]
# Voz = CFG["voz"] (locução ou o áudio do vídeo). Sons: biblioteca do usuário (sfx_pasta.txt) ou gerados por código.
# Pra ajustar à mão: CUES_EXTRA = [(tempo, "tipo_de_som", ganho_db), ...] no roteiro.
import os, sys, re, wave, random, argparse, numpy as np
AQUI = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, AQUI)
from sfx_lib import load, find, peak_idx, onset_idx, SR
from render import carrega

# famílias de som (trecho do nome do arquivo). A 1ª que existir na biblioteca é usada, alternando.
SONS = dict(
    pop=["UI_04_POP", "UI_10_POP", "UI_12_POP", "UI_21_POP", "UI_22_POP", "UI_23_POP", "UI_27_POP", "UI_28_POP"],
    click=["UI_25_CLICK", "UI_26_CLICK", "HIT_01_CLICK", "HIT_05_CLICK", "UI_14_CLICK", "UI_16_CLICK"],
    swish=["UI_07_SWISH", "UI_09_SWISH", "UI_17_SWISH", "UI_18_SWISH"],
    whoosh=["UI_11_WHOOSH", "12_WHOOSH", "15_WHOOSH_b"],
    rockin=["Dry Break Impact, Crispy", "Rock Yielding To Pressure", "Heavy Rock Crackles, Tremolo", "Sequence, Smooth Massive Rock Breaks"],
    rockmove=["Granular Rocks, Multi Whoosh", "Massive Rocks Frictions, Liquify", "Liquid Rocks, Multi Whoosh and Impact"],
    impact=["UI_13_IMPACT", "HIT_24_IMPACT", "UI_29_IMPACT", "UI_24_IMPACT"],
    catraca=["03_CATRACA_MECANICA_x3", "09_CATRACA_MECANICA"],
    cascata=["11_CLICK_x5", "01_RISER_E_CLIQUES_x10"],
    sino=["Agressive Impact, Alarm Clock Wing_Cinematic"],
    obturador=["06_OBTURADOR_CLICK", "08_OBTURADOR_CLICK_b", "14_OBTURADOR_CLICK_c"],
)
CORTE = dict(rockin=0.55, rockmove=0.75, catraca=0.9, cascata=0.6, sino=1.4, whoosh=0.8, impact=0.8)
_rot = {k: 0 for k in SONS}

def db(g): return 10 ** (g / 20)

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("roteiro"); ap.add_argument("saida")
    ap.add_argument("--sfx_db", type=float, default=-1.0); ap.add_argument("--sem_voz", action="store_true")
    A = ap.parse_args()
    R = carrega(A.roteiro); cfg = R.CFG
    N = int(cfg["dur"] * SR)
    voz = np.zeros((N, 2), np.float32)
    if cfg.get("voz") and not A.sem_voz:
        v = load(cfg["voz"])[:N]; voz[:len(v)] = v
        rms = np.sqrt(np.mean(v[np.abs(v).max(1) > 0.02] ** 2) + 1e-12)
        voz *= db(-17) / rms                                  # voz em ~-17 dBFS RMS
    sfx = np.zeros((N, 2), np.float32)
    rnd = random.Random(3)

    def place(kind, t, gain=-12, length=None, align="onset", fout=None):
        lst = SONS[kind]; nome = lst[_rot[kind] % len(lst)]; _rot[kind] += 1
        a = load(find(nome)).copy()
        length = length or CORTE.get(kind, 0.5)
        a = a[:int(length * SR)]
        if len(a) < 64: return
        nfo = max(1, min(len(a) - 1, int((fout or min(0.25, length * 0.35)) * SR)))
        a[:64] *= np.linspace(0, 1, 64)[:, None]; a[-nfo:] *= np.linspace(1, 0, nfo)[:, None]
        pan = rnd.uniform(-0.35, 0.35); a[:, 0] *= 1 - max(0, pan); a[:, 1] *= 1 + min(0, pan)
        off = peak_idx(a) if align == "peak" else onset_idx(a)
        i0 = int(t * SR) - off; j0, j1 = max(0, i0), min(N, i0 + len(a))
        if j1 > j0: sfx[j0:j1] += a[j0 - i0:j1 - i0] * db(gain)

    from dx import partes
    for c in sorted(R.CENAS, key=lambda c: c["t0"])[1:]:
        place("whoosh", c["t0"] + 0.18, -8, align="peak"); place("rockmove", c["t0"], -12)
    for e in R.EL:
        tp, t0 = e["tipo"], e.get("t0", 0)
        t0c = max(0.0, t0)
        if tp == "fala":
            for ti in e.get("tempos", []):
                ti = ti - e.get("adianta", 0.10)
                if ti >= 0: place("pop", ti, -17)
        elif tp == "item":
            place("pop", t0c, -9)
            if e.get("apaga") is not None and e["apaga"] > 0: place("swish", e["apaga"], -11)
        elif tp == "troca": place("whoosh", t0c + 0.1, -9, align="peak"); place("rockin", t0c + 0.2, -8)
        elif tp == "carimbo": place("impact", t0c + 0.2, -6, align="peak"); place("rockin", t0c + 0.2, -6)
        elif tp == "recibo":
            place("whoosh", t0c + 0.1, -10, align="peak")
            for i in range(len(e["linhas"])): place("click", t0 + 0.15 + i * e.get("stagger", 0.09), -11)
            tt = e.get("t_total", t0 + 0.4)
            place("catraca", tt, -13, length=e.get("conta", 0.8) + 0.1); place("impact", tt + e.get("conta", 0.8), -9)
            if e.get("risca") is not None:
                for i in range(len(e["linhas"])): place("swish", e["risca"] + i * 0.06, -13)
        elif tp == "onda": place("pop", t0c, -9); place("rockin", t0c, -11)
        elif tp == "contador":
            place("catraca", t0c, -12, length=e.get("conta", 0.9) + 0.1); place("impact", t0 + e.get("conta", 0.9), -7)
        elif tp == "grade":
            n = len(e["itens"]); place("cascata", t0c, -12, length=n * e.get("stagger", 0.07) + 0.25)
        elif tp == "busca":
            td = e.get("t_digita", t0 + 0.3)
            for i in range(len(e["txt"])): place("click", td + 0.055 * i, -14)
        elif tp == "comentar":
            place("pop", t0c, -9); td = e.get("t_digita", t0 + 0.3); pal = e["palavra"]
            for i in range(len(pal)): place("click", td + 0.09 * i, -12)
            place("pop", td + 0.09 * len(pal) + 0.2, -7)
        elif tp == "seguir": place("pop", t0c, -9); place("click", e.get("t_ok", t0 + 0.7), -6)
        elif tp == "dm":
            place("rockin", t0c, -8); place("pop", t0c + 0.05, -8)
            for i in range(len(e["itens"])): place("click", t0 + 0.47 + i * e.get("stagger", 0.22), -12)
        elif tp == "clip":
            if e.get("entrada", "sobe") in ("sobe", "desce", "lado") and t0 > 0: place("whoosh", t0c + 0.12, -11, align="peak")
        elif tp == "flash": place("obturador", t0c, -12)
        elif tp == "tremor": place("rockin", t0c, -4)
    for gi, g in enumerate(getattr(R, "GRUPOS", []) or []):
        place("click", g["t0"], -21)
    for t, kind, g in getattr(R, "CUES_EXTRA", []):
        place(kind, t, g)

    # bus de SFX ~5 dB abaixo da voz (padrão: voz -15 LUFS, SFX -20 LUFS)
    act = sfx[np.abs(sfx).max(1) > 1e-3]
    if len(act):
        rms_s = np.sqrt(np.mean(act ** 2)); sfx *= db(-22 + A.sfx_db) / rms_s
    m = voz + sfx
    pk = np.abs(m).max(); m *= min(1, db(-1) / max(pk, 1e-9))
    m[-int(.25 * SR):] *= np.linspace(1, 0, int(.25 * SR))[:, None]
    with wave.open(A.saida, "wb") as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
        w.writeframes((np.clip(m, -1, 1) * 32767).astype(np.int16).tobytes())
    print("ok", A.saida, f"pico {20 * np.log10(pk + 1e-9):.1f} dB")

if __name__ == "__main__":
    main()
