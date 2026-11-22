# Exemplo da skill diario-experimento — "EP 01: Para de pagar editor" (paleta lima)
import json, os, sys
SKILL = os.path.expanduser(r"~\.claude\skills\diario-experimento\scripts")
sys.path.insert(0, SKILL)
import dx

AQUI = os.path.dirname(os.path.abspath(__file__))  # coloque os vídeos/imagens do exemplo em ./material e a voz em ./fonte

MID = os.path.join(AQUI, "material")
def m(n): return os.path.join(MID, n + ".mp4")

CFG = dict(dur=19.4, paleta="lima", selo="EP 01", handle="@seu.perfil",
           voz=os.path.join(AQUI, "fonte", "voz.mp3"),
           legenda_y=1430, sem_legenda=[(0, 1.95), (13.0, 14.35)])
dx.set_paleta(CFG["paleta"])

PAL = json.load(open(os.path.join(AQUI, "fonte", "palavras.json"), encoding="utf8"))
GRUPOS = dx.grupos_legenda(PAL, max_pal=3, fix={"Clod.": "Claude.", "guia": "GUIA", "10": "dez"},
                           destaques=("motion", "Claude", "Noir", "código", "Blender", "Zero", "GUIA", "catálogo", "dez", "render"))
# tira o "a" de "Comenta a guia" (a locução fala "Comenta GUIA")
for g in GRUPOS:
    g["ws"] = [w for w in g["ws"] if not (w[0] == "a" and abs(w[1] - 16.6) < 0.05)]

EL = [
    # ---------- GANCHO (0–1,9 s): 3 vídeos reais em leque + título
    dict(tipo="clip", src=m("etiqueta-brutal"), ini=3.0, t0=-0.35, t1=1.85, modo="cartao", larg=330, cx=235, cy=1090, rot=9, entrada="zoom", saida="sobe"),
    dict(tipo="clip", src=m("moldura-pop"), ini=5.0, t0=-0.30, t1=1.80, modo="cartao", larg=330, cx=845, cy=1090, rot=-9, entrada="zoom", saida="sobe"),
    dict(tipo="clip", src=m("kinetic-creme"), ini=2.0, t0=-0.25, t1=1.75, modo="cartao", larg=360, cx=540, cy=1060, entrada="zoom", saida="sobe"),
    dict(tipo="titulo", txt="PARA DE PAGAR\n*EDITOR*", sub="pra fazer motion", t0=-0.45, t1=1.8, y=335, size=128),
    dict(tipo="flash", t0=1.85, dur=0.18, forca=0.25),

    # ---------- 10 ESTILOS (2,0–5,1 s)
    dict(tipo="numeros", t0=2.05, t1=5.0, y=470, size=210, itens=[dict(v="10", de=0, conta=0.6, t=2.05, rot="ESTILOS DE EDIÇÃO", cor="branco")]),
    dict(tipo="calendario", t0=2.75, t1=5.0, total=10, dia=10, cols=5, y=900, escala=1.3),

    # ---------- KINETIC NOIR (5,15–9,0 s)
    dict(tipo="clip", src=m("kinetic-noir"), ini=2.0, t0=5.15, t1=8.95, modo="cartao", larg=600, cx=540, cy=1050, entrada="sobe", saida="sobe", zoom=(1.0, 1.08)),
    dict(tipo="titulo", txt="KINETIC *NOIR*", t0=5.9, t1=8.9, y=345, size=104),
    dict(tipo="chip", txt="câmera 3D", t0=6.95, t1=8.9, x=110, y=1200),
    dict(tipo="chip", txt="100% código", t0=8.0, t1=8.9, x=560, y=620),

    # ---------- MAQUETE VIVA (9,2–13,0 s)
    dict(tipo="clip", src=m("maquete-viva"), ini=6.0, t0=9.2, t1=12.95, modo="cartao", larg=600, cx=540, cy=1050, entrada="lado", saida="some", zoom=(1.0, 1.1)),
    dict(tipo="titulo", txt="MAQUETE *VIVA*", t0=9.95, t1=12.9, y=345, size=104),
    dict(tipo="rabisco", txt="cidade 3D\nno *Blender*", t0=11.15, t1=12.9, cx=300, y=720, size=50, rot=7, escreve=0.7),

    # ---------- QUANTO CUSTA? ZERO (13,05–16,0 s)
    dict(tipo="titulo", txt="QUANTO CUSTA\nO *RENDER*?", t0=13.05, t1=14.3, y=640, size=124),
    dict(tipo="numeros", t0=14.4, t1=15.95, y=700, size=320, itens=[dict(v="0", de=100, conta=0.55, t=14.4, rot="CRÉDITOS DE IA", cor="acento")]),
    dict(tipo="icone", ok=True, t0=15.0, t1=15.95, cx=690, y=600, r=40),
    dict(tipo="barras", t0=14.95, t1=15.95, x=140, y=1030, w=800, linhas=[
        dict(rot="vídeo com IA", val="$$$", frac=0.92),
        dict(rot="essas skills", val="R$ 0", frac=0.04, destaque=True)]),
    dict(tipo="flash", t0=14.42, dur=0.2, forca=0.3),
    dict(tipo="tremor", t0=14.42, dur=0.3, amp=16),

    # ---------- CTA (16,0–19,4 s)
    dict(tipo="titulo", txt="COMENTA *GUIA*", sub="que eu te mando o catálogo", t0=16.0, y=420, size=118),
    dict(tipo="comentar", palavra="GUIA", t0=16.35, t_digita=16.6, y=820),
    dict(tipo="dm", handle="@seu.perfil", iniciais="LK", msg="Toma o catálogo com os 10 estilos", t0=17.35, y=960),
]
