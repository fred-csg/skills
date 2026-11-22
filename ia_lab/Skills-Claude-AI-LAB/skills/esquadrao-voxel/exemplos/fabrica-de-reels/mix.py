# som da "Fábrica de Reels" (exemplo) — voz + SFX que vêm com a skill (scripts/molde/sfx).
# Tem biblioteca própria de sons? Troque SFX pela sua pasta e os nomes dos arquivos. Uso: python mix.py
import sys, os, json, itertools
MOLDE = os.path.expanduser(r"~/.claude/skills/esquadrao-voxel/scripts/molde"); sys.path.insert(0, MOLDE)
import mix as MX

AQUI = os.path.dirname(os.path.abspath(__file__)); P = os.path.dirname(AQUI)
SFX = os.path.join(MOLDE, "sfx")
POP = itertools.cycle(["pop.mp3", "titulo.mp3"])
C = []
def entra(t, g=-8): C.append((next(POP), t, g, "onset", 0.4))           # elemento aparecendo
def move(t, g=-7): C.append(("whoosh.mp3", t - 0.15, g, "peak", 0.7))    # câmera / chicote
def impacto(t, g=-5): C.append(("porta.mp3", t, g, "onset", 0.5)); C.append(("pop.mp3", t, g - 4, "onset", 0.3))

entra(0.05); C.append(("whoosh.mp3", 1.15, -11, "onset", 0.5)); impacto(1.6, -7)   # joga a ideia no funil
move(2.15); impacto(3.45); entra(3.38, -9)                                     # Reel pronto no fim
move(4.45); entra(4.52, -11); entra(4.85, -9)                                  # volta e mostra por dentro
for a, b in zip([5.85, 7.55, 9.45, 12.3], [6.5, 8.35, 10.2, 13.05]):
    C.append(("foto.mp3", a, -12, "onset", 0.4))                               # máquina liga
    impacto(b, -5); entra(b + 0.03, -10)                                       # sai transformado
entra(10.6); C.append(("celular.mp3", 13.15, -8, "onset", 0.8))                # selo + notificação
impacto(14.35, -5); C.append(("foto.mp3", 14.5, -10, "onset", 0.4))
move(16.45); C.append(("apagar.mp3", 16.6, -10, "onset", 0.8))                 # planta desenrola
impacto(18.15, -3); C.append(("redes.mp3", 18.2, -8, "onset", 0.9))            # carimbo GUIA
W = json.load(open(os.path.join(AQUI, "palavras.json"), encoding="utf-8"))
for w in W: C.append(("pop.mp3", w["s"] - 0.04, -24, "onset", 0.2))            # toque leve em cada palavra

MX.mix(os.path.join(P, "audio", "locucao.mp3"), None, C, 20.2, os.path.join(P, "audio", "mix.wav"), SFX)
print(len(C), "cues")
