# texturas da "Fábrica de Reels" (rodar antes do Blender):  python texturas.py
import sys, os
SK = os.path.expanduser(r"~\.claude\skills\esquadrao-voxel\scripts\molde"); sys.path.insert(0, SK)
import telas as T
D = os.path.join(os.path.dirname(os.path.abspath(__file__)), "tex")
p = lambda n: os.path.join(D, n)

T.dia(p("janela_dia.png"))
T.letreiro(p("let_fabrica.png"), "fábrica de reels", T.INK, T.LIMA, w=1800, h=240)
T.letreiro(p("let_roteiro.png"), "roteiro", T.CREME, T.INK)
T.letreiro(p("let_voz.png"), "voz", T.CREME, T.INK)
T.letreiro(p("let_video.png"), "vídeo", T.CREME, T.INK)
T.letreiro(p("let_agenda.png"), "agenda", T.CREME, T.INK)
T.letreiro(p("let_ideias.png"), "ideias", T.AMARELO, T.INK)
T.letreiro(p("let_saida.png"), "saída", T.CORAL, "#FFFFFF")
T.doc(p("tela_roteiro.png"), "roteiro", ["GANCHO", "Eu jogo uma ideia...", "", "CENA 1"], destaque=0)
T.onda(p("tela_voz.png"), "voz.wav")
T.timeline(p("tela_video.png"), "corte + legenda")
T.agenda(p("tela_agenda.png"), "OUTUBRO", dia=28)
T.neon(p("neon_guia.png"), "GUIA", T.LIMA)
print("ok", len(os.listdir(D)))
