# Caderno Tech — vídeo de apresentação da skill (paleta cobalto)
import json, os, sys
sys.path.insert(0, os.path.expanduser(r"~\.claude\skills\caderno-tech\scripts"))
import ct

AQUI = os.path.dirname(os.path.abspath(__file__))  # coloque os vídeos/imagens do exemplo em ./material e a voz em ./fonte

VSC = os.path.join(AQUI, "material")
MID = VSC
VID = VSC
def m(n): return os.path.join(MID, n)
def v(n): return os.path.join(VID, n)

CFG = dict(dur=26.4, paleta="cobalto", voz=os.path.join(AQUI, "fonte", "voz.mp3"))
ct.set_paleta(CFG["paleta"])
PAL = json.load(open(os.path.join(AQUI, "fonte", "palavras.json"), encoding="utf8"))
F = lambda txt, t0, t1, **k: ct.fala(txt, t0, t1, PAL, **{"size": 70, **k})

# ícones
I_MOTION = "Mo|#1d2330|#ffffff"; I_LOC = "Lo|#2a1f3a|#ffffff"; I_3D = "3D|#33261a|#ffffff"
I_EDIT = "Ed|#3a1a1a|#ffffff"; I_BANCO = "Bi|#1a3326|#ffffff"
I_KN = m("kinetic-noir.jpg"); I_MV = m("maquete-viva.jpg")
I_VOZ = "♪|#243ae2|#ffffff"
GRADE = [(m("jarvis-cortes.jpg"), "Jarvis"), (m("kinetic-creme.jpg"), "K. Creme"), (m("kinetic-noir.jpg"), "K. Noir"),
         (m("etiqueta-brutal.jpg"), "Etiqueta"), (m("moldura-pop.jpg"), "Moldura"), (m("maquete-viva.jpg"), "Maquete"),
         (m("manifesto-feed.jpg"), "Manifesto"), (v("hand-drawing.jpg"), "Hand Draw"), (v("mascote-apresentador.jpg"), "Mascote"),
         (v("esquadrao-voxel.jpg"), "Voxel"), (os.path.join(VSC, "diario-experimento.jpg"), "Diário"),
         ("Aa|#243ae2|#ffffff", "Caderno")]

CENAS = [
    dict(t0=-1, fundo="escuro", rotulo="skill nova", status="CADERNO TECH", fantasma="01", prog=0.12),
    dict(t0=3.70, fundo="papel", rotulo="a conta", status="R$ 4.100/MÊS", fantasma="R$", prog=0.25),
    dict(t0=7.72, fundo="escuro", rotulo="as trocas", status="3 TROCAS", fantasma="03", prog=0.36),
    dict(t0=9.30, fundo="papel", rotulo="troca 1", status="#01", fantasma="01", prog=0.45),
    dict(t0=12.00, fundo="escuro", rotulo="troca 2", status="VOZ CLONADA", fantasma="02", prog=0.55),
    dict(t0=14.74, fundo="papel", rotulo="troca 3", status="#03", fantasma="03", prog=0.66),
    dict(t0=18.12, fundo="escuro", rotulo="a soma", status="12 ESTILOS", fantasma="12", prog=0.82),
    dict(t0=22.60, fundo="escuro", rotulo="o guia", status="COMENTA GUIA", fantasma="GUIA", prog=1.0),
]

EL = [
    # ---------- GANCHO: cartão de troca + carimbo já na tela no quadro 0
    F("Essa skill do *Claude* transforma qualquer lista num *Reels* assim.", -0.3, 3.55, adianta=0.25),
    dict(tipo="item", t0=-0.4, t1=3.5, y=650, num="#01 / 03", nome="Motion designer", preco="pago por vídeo", icone=I_MOTION, apaga=-0.4),
    dict(tipo="troca", t0=-0.4, t1=3.5, y=880, nome="Kinetic Noir", desc="motion 3D feito por código", rodape="skills/kinetic-noir", selo="★ AI LAB", icone=I_KN),
    dict(tipo="carimbo", txt="0 CRÉDITO", t0=-0.4, t1=3.5, cx=760, cy=1150, rot=-7),
    dict(tipo="clip", src=m("kinetic-noir.mp4"), ini=14.0, t0=-0.4, t1=3.5, modo="cartao", larg=890, alt=260, cx=540, cy=1345, foco=(0.5, 0.33), entrada="sobe", saida="some", r=24),

    # ---------- A CONTA (papel): recibo
    F("Primeiro, a *conta*: tudo que você paga por mês vira um *recibo*.", 3.7, 7.65),
    dict(tipo="recibo", t0=4.4, t1=7.65, y=640, cab_e="SEU MÊS DE CONTEÚDO", cab_d="POR MÊS",
         linhas=[dict(rot="Motion designer", val="R$ 2.000", icone=I_MOTION), dict(rot="Locutor", val="R$ 600", icone=I_LOC),
                 dict(rot="Modelador 3D", val="R$ 1.500", icone=I_3D)],
         nota="valores de exemplo\ntroque pelos seus", total="R$ 4.100", t_total=5.0, conta=1.2),

    # ---------- AS TROCAS (escuro): grade dos 3 "de"
    F("Agora, as *trocas*.", 7.72, 9.2),
    dict(tipo="grade", t0=8.3, t1=9.2, y=640, cols=1, alt_linha=120, icone_s=84, size=34, mono=True, stagger=0.12,
         itens=[(I_MOTION, "Motion designer  →  ?"), (I_LOC, "Locutor  →  ?"), (I_3D, "Modelador 3D  →  ?")]),

    # ---------- TROCA 1 (papel)
    F("No lugar do motion designer, o *Kinetic Noir*.", 9.3, 11.95),
    dict(tipo="item", t0=9.55, t1=11.95, y=650, num="#01 / 03", nome="Motion designer", preco="pago por vídeo", icone=I_MOTION, apaga=11.1),
    dict(tipo="troca", t0=11.12, t1=11.95, y=880, nome="Kinetic Noir", desc="motion 3D feito por código", rodape="skills/kinetic-noir", selo="★ AI LAB", icone=I_KN),
    dict(tipo="clip", src=m("kinetic-noir.mp4"), ini=15.0, t0=11.25, t1=11.95, modo="cartao", larg=890, alt=260, cx=540, cy=1345, foco=(0.5, 0.33), entrada="sobe", saida="some", r=24),
    dict(tipo="carimbo", txt="0 CRÉDITO", t0=11.55, t1=11.95, cx=760, cy=1150, rot=-7),

    # ---------- TROCA 2 (escuro)
    F("No lugar do locutor, o seu *clone de voz*.", 12.0, 14.7),
    dict(tipo="item", t0=12.25, t1=14.7, y=650, num="#02 / 03", nome="Locutor", preco="pago por áudio", icone=I_LOC, apaga=13.5),
    dict(tipo="onda", t0=13.55, t1=14.7, y=880, titulo="SUA VOZ · TOCANDO AGORA", rot="clone de voz"),
    dict(tipo="carimbo", txt="É VOCÊ", t0=14.15, t1=14.7, cx=760, cy=1200, rot=-6),

    # ---------- TROCA 3 (papel)
    F("E no lugar do modelador *3D*, a *Maquete Viva*.", 14.74, 18.05),
    dict(tipo="item", t0=15.05, t1=18.05, y=650, num="#03 / 03", nome="Modelador 3D", preco="pago por cena", icone=I_3D, apaga=16.75),
    dict(tipo="troca", t0=16.8, t1=18.05, y=880, nome="Maquete Viva", desc="cidade 3D no Blender", rodape="skills/maquete-viva", selo="★ AI LAB", icone=I_MV),
    dict(tipo="clip", src=m("maquete-viva.mp4"), ini=10.0, t0=16.95, t1=18.05, modo="cartao", larg=890, alt=260, cx=540, cy=1345, foco=(0.5, 0.33), entrada="sobe", saida="some", r=24),
    dict(tipo="carimbo", txt="0 CRÉDITO", t0=17.4, t1=18.05, cx=760, cy=1150, rot=-7),

    # ---------- A SOMA (escuro)
    F("Somando, são *12 estilos* de edição, com *zero crédito* de IA no render.", 18.12, 22.5),
    dict(tipo="grade", t0=18.4, t1=22.5, y=560, cols=3, alt_linha=96, icone_s=64, size=26, stagger=0.05, itens=GRADE),
    dict(tipo="contador", t0=18.95, t1=22.5, y=1060, v="12", pre="★ ", suf=" estilos", size=88, conta=0.8),
    dict(tipo="carimbo", txt="R$ 0 DE IA", t0=20.7, t1=22.5, cx=740, cy=1220, rot=-6, size=56),

    # ---------- CTA
    F("Comenta *GUIA* que eu te mando o *catálogo* completo.", 22.6, None),
    dict(tipo="comentar", palavra="GUIA", t0=22.85, t_digita=23.0, y=610),
    dict(tipo="seguir", t0=23.5, y=790, nome="Seu Nome", sub="IA, skills e conteúdo", t_ok=24.1),
    dict(tipo="dm", t0=24.1, y=940, de="Seu Nome", tag="CATÁLOGO", stagger=0.18,
         itens=[("Kinetic Noir", "motion 3D"), ("Maquete Viva", "cidade 3D"), ("Diário de Experimento", "série"),
                ("Caderno Tech", "listas"), ("+ 8 estilos", "no catálogo")]),
]
