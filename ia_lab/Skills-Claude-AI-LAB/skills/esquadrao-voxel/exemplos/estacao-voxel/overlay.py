# HUD da "Estação Voxel"
import sys, os, json
sys.path.insert(0, os.path.expanduser(r"~\.claude\skills\esquadrao-voxel\scripts\molde"))
import hud
from hud import LIMA, CORAL, AZUL, VERDE, AMARELO, ROXO

AQUI = os.path.dirname(os.path.abspath(__file__))
W = json.load(open(os.path.join(AQUI, "palavras.json"), encoding="utf-8"))
OUT = []
for w in W:
    k = w["w"].strip(".,!?").lower()
    if k == "a" and w["s"] > 26.5: continue                 # "Comenta a guia" -> "Comenta GUIA"
    if k == "guia": w["w"] = "GUIA."; w["s"] = min(w["s"], 26.7)   # na fala sai colado: "comentaGUIA"
    if k == "reel": w["w"] = w["w"].replace("reel", "Reel")
    if k == "skill": w["w"] = w["w"].replace("Skill", "skill")
    if k in ("roteiro", "voz", "cenário", "câmera", "escriba", "pintora", "mecânica") and 5 < w["s"] < 15:
        w["w"] = w["w"][0].upper() + w["w"][1:]
    OUT.append(w)
W = OUT

POS = dict(bloom=0.1, limiar=0.9, vinheta=0.3)   # cena de dia
H = hud.HUD()
H.legenda(W, chaves=["ideia", "trem", "vídeo", "3D", "Roteiro", "Escriba", "gancho", "Voz", "clonada", "Cenário", "Pintora",
                     "Mecânica", "Blender", "Câmera", "movimento", "legenda", "som", "Reel", "pronto", "edição", "Esquadrão",
                     "Voxel", "19", "personagens", "GUIA"])
H.titulos = [(0.0, "UMA IDEIA NO TREM", None), (2.0, "ÚLTIMA PARADA: VÍDEO 3D", None),
             (18.65, "REEL PRONTO", None), (21.75, "ESQUADRÃO VOXEL", None), (25.4, "COMENTA GUIA", None)]
_tit = H._tit
def _tit_novo(img, t):
    if 5.05 <= t < 18.65: return                           # na viagem o título dá lugar às estações
    _tit(img, t)
H._tit = _tit_novo
ESTACOES = ["ROTEIRO", "VOZ", "CENÁRIO", "CÂMERA", "REEL ✓"]
H.contadores = [(23.35, 25.35, "PERSONAGENS|NOVOS", [(23.5, 0), (24.6, 19)], LIMA, "")]
H.extras = [
    hud.flash(2.0, 0.08), hud.flash(5.05, 0.08), hud.flash(18.65, 0.08),
    hud.flash(15.55, 0.1), hud.flash(16.1, 0.1),
    hud.trilho(5.1, 18.6, ESTACOES, [5.7, 8.85, 11.35, 14.85, 17.6], cy=312),
    hud.selo(2.55, 4.95, "SAIU ASSIM ✓", LIMA, cx=650, cy=470, rot=6),
    hud.selo(7.55, 8.3, "+ GANCHO", AMARELO, cx=650, cy=470, rot=-5),
    hud.selo(9.95, 10.6, "VOZ CLONADA ✓", AZUL, cx=650, cy=470, rot=5),
    hud.selo(13.8, 14.4, "FEITO NO BLENDER", ROXO, cx=600, cy=470, rot=-4),
    hud.selo(17.15, 17.85, "+ LEGENDA + SOM", AMARELO, cx=620, cy=470, rot=5),
    hud.selo(20.3, 21.65, "SEM EDITOR ✓", LIMA, cx=650, cy=470, rot=-5),
    hud.estouro(26.35, 28.4, "GUIA", LIMA, cx=490, cy=640),
    hud.confete(26.4, 28.4, 80, 5),
]
def desenhar(img, t):
    H.desenhar(img, t)
