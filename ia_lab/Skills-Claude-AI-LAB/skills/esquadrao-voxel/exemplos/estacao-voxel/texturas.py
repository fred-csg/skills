# texturas da "Estação Voxel" (rodar antes do Blender):  python texturas.py
import sys, os
SK = os.path.expanduser(r"~\.claude\skills\esquadrao-voxel\scripts\molde"); sys.path.insert(0, SK)
import telas as T
D = os.path.join(os.path.dirname(os.path.abspath(__file__)), "tex"); os.makedirs(D, exist_ok=True)
p = lambda n: os.path.join(D, n)

T.letreiro(p("let_ideia.png"), "ideia", T.AMARELO, T.INK)
T.letreiro(p("let_roteiro.png"), "roteiro", T.CREME, T.INK)
T.letreiro(p("let_voz.png"), "voz", T.CREME, T.INK)
T.letreiro(p("let_cenario.png"), "cenário 3D", T.CREME, T.INK)
T.letreiro(p("let_camera.png"), "câmera", T.CREME, T.INK)
T.letreiro(p("let_final.png"), "reel pronto", T.LIMA, T.INK, w=1400)
T.doc(p("tela_roteiro.png"), "roteiro", ["GANCHO", "Coloquei uma ideia", "nesse trem...", "CENA 1 — estação"], destaque=0)
T.onda(p("tela_voz.png"), "VOZ CLONADA — locucao.mp3")
T.terminal(p("tela_cenario.png"), "cena.py — Blender", [
    ("import vox, bonecos as B", "#C6F432"), "vox.setup(28, paleta='manha')",
    "trem = estacao.trem()", ("b = B.elenco('pin', 'pintora')", "#FFC83D"),
    "b.gesto('mostra', 11.4, 13.6)", "vox.CAM = [...]", ("vox.run(apply)", "#C6F432")])
T.timeline(p("tela_camera.png"), "reel.mp4 — legenda + som")
T.neon(p("neon_voxel.png"), "ESQUADRÃO VOXEL", T.LIMA, w=2800, h=420)
print("ok", len(os.listdir(D)))
