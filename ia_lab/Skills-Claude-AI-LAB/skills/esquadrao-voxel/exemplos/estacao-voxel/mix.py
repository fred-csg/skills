# som da "Estação Voxel" (exemplo) — voz + SFX que vêm com a skill (scripts/molde/sfx).
# Tem biblioteca própria de sons? Troque SFX pela sua pasta e os nomes dos arquivos. Uso: python mix.py
import sys, os, json, itertools
MOLDE = os.path.expanduser(r"~/.claude/skills/esquadrao-voxel/scripts/molde"); sys.path.insert(0, MOLDE)
import mix as MX

AQUI = os.path.dirname(os.path.abspath(__file__)); P = os.path.dirname(AQUI)
SFX = os.path.join(MOLDE, "sfx")
POP = itertools.cycle(["pop.mp3", "titulo.mp3"])
C = []
def entra(t, g=-8): C.append((next(POP), t, g, "onset", 0.4))           # elemento aparecendo
def move(t, g=-7): C.append(("whoosh.mp3", t - 0.15, g, "peak", 0.7))    # câmera / chicote / trem saindo
def impacto(t, g=-5): C.append(("porta.mp3", t, g, "onset", 0.5)); C.append(("pop.mp3", t, g - 4, "onset", 0.3))

entra(0.05); C.append(("whoosh.mp3", 0.62, -11, "onset", 0.5)); impacto(1.12, -7)   # ideia cai no vagão
move(1.5, -10)                                                                      # trem parte
move(2.0); impacto(2.4); entra(2.6, -9)                                             # gancho: Reel no pedestal
move(5.05); entra(5.12, -11)
for t in (5.7, 8.85, 11.35, 14.85, 18.6): entra(t, -10)                             # chegou na estação
for t in (7.95, 10.45, 13.95, 17.6, 20.1): move(t, -10)                             # trem sai
for t in (7.5, 9.9, 13.75, 17.1): impacto(t, -5); entra(t + 0.05, -10)              # objeto se transforma + selo
for t in (15.55, 16.1): C.append(("foto.mp3", t, -8, "onset", 0.4))                 # flashes da câmera
impacto(18.65, -6); impacto(19.5, -3); entra(20.3, -10)                             # Reel no pedestal
move(21.75); impacto(21.9, -6)                                                      # letreiro acende
C.append(("apagar.mp3", 23.45, -12, "onset", 0.9))                                  # contador 0 -> 19
move(25.4, -9); impacto(26.35, -3); C.append(("redes.mp3", 26.4, -8, "onset", 0.9)) # GUIA
W = json.load(open(os.path.join(AQUI, "palavras.json"), encoding="utf-8"))
for w in W: C.append(("pop.mp3", w["s"] - 0.04, -24, "onset", 0.2))                 # toque leve em cada palavra

MX.mix(os.path.join(P, "audio", "locucao.mp3"), None, C, 28.4, os.path.join(P, "audio", "mix.wav"), SFX)
print(len(C), "cues")
