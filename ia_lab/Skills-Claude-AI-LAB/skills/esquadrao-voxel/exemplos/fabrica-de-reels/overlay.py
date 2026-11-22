# HUD da "Fábrica de Reels"
import sys, os, json
sys.path.insert(0, os.path.expanduser(r"~\.claude\skills\esquadrao-voxel\scripts\molde"))
import hud
from hud import LIMA, CORAL, AZUL, VERDE, AMARELO, ROXO

AQUI = os.path.dirname(os.path.abspath(__file__))
W = json.load(open(os.path.join(AQUI, "palavras.json"), encoding="utf-8"))
for w in W:
    if w["w"].strip(".,!?").lower() == "reel": w["w"] = w["w"].replace("reel", "Reel")
    if w["w"].strip(".,!?").lower() == "guia": w["w"] = "GUIA."
    if w["w"] == "eu" and 14.7 < w["s"] < 15.1: w["w"] = "eu?"   # "E eu?" — quebra a frase

POS = dict(bloom=0.1, limiar=0.9, vinheta=0.3)   # cena de dia: menos brilho
H = hud.HUD()
H.legenda(W, chaves=["ideia", "Reel", "pronto", "roteiro", "voz", "vídeo", "legenda", "agendado", "Instagram", "mão", "planta", "fábrica", "GUIA"])
H.titulos = [(0.0, "IDEIA ENTRA, REEL SAI", None), (14.5, "ZERO MÃO NA MASSA", None),
             (16.45, "A PLANTA É SUA", None), (18.0, "COMENTA GUIA", None)]
# durante a esteira o título sai e entra a barra de etapas (acende quando o objeto sai de cada máquina)
_tit = H._tit
def _tit_novo(img, t):
    if 4.45 <= t < 14.5: return
    _tit(img, t)
H._tit = _tit_novo
ETAPAS = ["IDEIA", "ROTEIRO", "VOZ", "VÍDEO", "POST ✓"]
H.extras = [
    hud.flash(2.15, 0.07), hud.flash(4.45, 0.07),
    hud.trilho(4.5, 14.45, ETAPAS, [4.5, 6.5, 8.35, 10.2, 13.05], cy=312),
    hud.selo(3.35, 4.4, "PRONTO ✓", LIMA, cx=640, cy=640, rot=6),
    hud.selo(10.6, 11.95, "+ LEGENDA", AMARELO, cx=660, cy=600, rot=-5),
    hud.notificacao(13.15, 14.4, "Instagram", "Reel agendado ✓", "hoje às 18:00", cx=490, cy=560),
    hud.cartao_planta(16.6, 20.3, "PLANTA DA FÁBRICA", ETAPAS, cx=490, cy=760, carimbo_t=18.15, carimbo_txt="GUIA"),
    hud.confete(18.15, 20.2, 80, 5),
]
def desenhar(img, t):
    H.desenhar(img, t)
