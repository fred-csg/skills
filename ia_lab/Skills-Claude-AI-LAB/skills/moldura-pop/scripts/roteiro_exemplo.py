# moldura-pop · roteiro do exemplo "A nova profissão do Peter Parker" (Lucas, 25 s)
# Uso:  python roteiro.py render <video> <mascara> <head.json> <palavras.json> <saida.mp4>
#       python roteiro.py stills <video> <mascara> <head.json> <palavras.json> <folha.jpg> 0.8,4.6,...
import sys, os, json, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mp import *

VID, MAT, HEAD, PAL = sys.argv[2:6]
WDS = json.load(open(PAL, encoding="utf8"))
FIX = {69: "Pesquisei", 107: "apês", 25: "Diário"}           # correções de transcrição
FIM = 26.9                                                   # fala acaba 24,66; +2,2 s de CTA com quadro congelado

def wtxt(i):
    w = FIX.get(i, WDS[i]["w"]).strip().rstrip(".,")
    return w
def G(i0, i1, acc=(), ser=()):
    ws = []; i = i0
    while i <= i1:
        txt, st = wtxt(i), WDS[i]["s"]
        if i + 1 <= i1 and WDS[i + 1]["w"].startswith("-"):            # Homem + -Aranha
            txt += wtxt(i + 1); i += 1
        style = "ser" if i in ser else ("acc" if i in acc else "n")
        if i in ser: txt = txt.upper()
        ws.append((txt, st, style)); i += 1
    ws_end[id(ws)] = WDS[i1]["e"]
    return ws
ws_end = {}
grp = [G(0, 1), G(2, 3), G(4, 6, acc=(5, 6)), G(7, 8), G(9, 10, ser=(10,)), G(11, 13), G(14, 16, acc=(15, 16)),
       G(17, 20), G(21, 22, ser=(22,)), G(23, 25, acc=(24, 25)),
       G(26, 26), G(27, 30), G(31, 32, ser=(32,)), G(33, 35),
       G(36, 38), G(39, 41, acc=(40, 41)), G(42, 44), G(45, 45, ser=(45,)), G(46, 49),
       G(50, 51), G(52, 54), G(55, 55, ser=(55,)), G(56, 59, acc=(57, 58, 59)), G(60, 63), G(64, 65, acc=(65,)), G(66, 68),
       G(69, 70), G(71, 74), G(75, 76), G(77, 79, acc=(78, 79)), G(80, 83), G(84, 85), G(86, 88, acc=(86, 87, 88)),
       G(89, 91), G(92, 92, ser=(92,)), G(93, 94),
       G(95, 97, acc=(96, 97)), G(98, 99), G(100, 103), G(104, 105), G(106, 107), G(108, 109), G(110, 110, ser=(110,)),
       G(111, 112), G(113, 113)]
grupos = []
for k, ws in enumerate(grp):
    g0 = ws[0][1]
    last_end = ws_end[id(ws)]
    nxt = grp[k + 1][0][1] if k + 1 < len(grp) else 99
    grupos.append((g0, min(nxt - 0.13, last_end + 0.45), ws))
leg = Legenda(grupos, y=1452, size=64)

# ---------------------------------------------------------------- utilidades de cena
def header(icon, caps, serif, theme, caps_kind="black"):
    fg = INK if theme == "light" else WHITE
    parts = [icon_img(icon, 40, ACC), text_img(caps, caps_kind, 31, fg, track=0.16)]
    if serif: parts.append(text_img(serif, "serif_i", 46, INK2 if theme == "light" else (220, 205, 200)))
    return hstack(parts, gap=16, valign="base" if serif else "c")

def strike(t0, w=520):
    def f(t):
        p = eout(lin(t, t0, t0 + 0.28))
        if p <= 0: return None
        c = Cv(w + 20, 40); c.line([(10, 20), (10 + w * p, 20)], WHITE, 7)
        return glow(c.done(), 8, ACC, 0.9)
    return f

# ---------------------------------------------------------------- CENA 1 · gancho (claro, moldura)
c1 = []
c1.append(El(header("film", "HOMEM-ARANHA", "novo filme", "light"), 540, 172, 0.05))
hl = hstack([text_img("a", "black", 100, INK, track=-0.03), text_img("nova", "black", 100, ACC, track=-0.03),
             text_img("profissão", "black", 100, INK, track=-0.03)], gap=26)
c1.append(El(hl, 540, 292, 0.25, enter="wipe", dur=0.7))
sub = text_img("do Peter Parker", "serif_i", 66, INK)
def dots(t, t_on=2.44):
    c = Cv(5 * 50 + 4 * 10, 54)
    for i in range(5):
        x = i * 60
        on = i == 2 and t >= t_on
        k = eback(lin(t, t_on, t_on + 0.3)) if on else 0
        c.ell(x + 2, 2, 50, 50, fill=mixc(WHITE, ACC, clamp(k)) if on else WHITE, ol=ACC if on else LINE, ow=2)
        paste_c(c, icon_img("film", 22, WHITE if on else GRAY), x + 27, 28)
    return c.done()
row_w = sub.width + 20 + 290
c1.append(El(sub, 540 - row_w / 2 + sub.width / 2, 398, 0.85, dy=20))
c1.append(El(dots, 540 + row_w / 2 - 145, 404, 1.0, dy=20))
c1.append(El(badge("camera", 104), 228, 830, 1.22, enter="pop", rot=-9, float_amp=6))
c1.append(El(badge("help", 104, fill=INK), 852, 830, 1.42, enter="pop", rot=9, float_amp=6))

# ---------------------------------------------------------------- CENA 2 · "não é mais fotógrafo" (escuro, moldura)
c2 = []
c2.append(El(hstack([icon_img("news", 40, WHITE), text_img("CLARIM DIÁRIO", "serif_b", 40, WHITE, track=0.1)], 16, "c"), 540, 172, 4.02))
c2.append(El(pill("FOTÓGRAFO", "camera", 70, glow_col=ACC), 540, 318, 4.55, enter="pop"))
c2.append(El(strike(4.95, 470), 540, 318, 4.95, dur=0.01, enter="none"))
c2.append(El(chip("não é mais a profissão dele", "x", "dark", 30), 540, 476, 5.2))

# ---------------------------------------------------------------- CENA 3 · sem spoiler (tela cheia)
c3 = [El(pill("zero spoiler", "shield", 32, fill=tint(ACC, 215), kind="bold", glow_col=ACC), 540, 1352, 6.42, layer="front")]

# ---------------------------------------------------------------- CENA 4 · Doutor Estranho (claro, avatar)
c4 = []
hd4 = vstack([text_img("Doutor Estranho,", "black", 56, INK, track=-0.02),
              text_img("e todo mundo esqueceu", "serif_i", 50, INK2)], gap=-26, align="r")
c4.append(El(hd4, 690, 384, 8.55, anchor="r"))
def grade(t, t_forget=10.0):
    w, h = 880, 268
    c = Cv(w, h); c.rr(0, 0, w, h, 30, fill=WHITE, ol=LINE, ow=2)
    tw_, th_ = 148, 96
    for i in range(10):
        r, col = divmod(i, 5)
        x = 28 + col * (tw_ + 17); y = 30 + r * (th_ + 20)
        k = eio(lin(t, t_forget + i * 0.06, t_forget + i * 0.06 + 0.3))
        c.rr(x, y, tw_, th_, 18, fill=mixc((255, 244, 242), (240, 240, 242), k), ol=mixc(ACC, (215, 215, 220), k), ow=2)
        ic = icon_img("person" if k < 0.5 else "help", 36, mixc(ACC, (170, 170, 178), k))
        paste_c(c, ic, x + tw_ / 2, y + th_ / 2)
    return shadow(c.done(), 24, 0.12, 12)
c4.append(El(grade, 540, 760, 9.45))
c4.append(El(card("Peter Parker", "ninguém lembra quem é", "person", w=700, h=150, theme="dark",
                  extra=status("esquecido", ok=False, size=24)), 540, 1060, 10.92, enter="pop"))

# ---------------------------------------------------------------- CENA 5 · herança zero (claro, moldura)
c5 = []
c5.append(El(card("Homem de Ferro", "herança", "bolt", w=500, h=150), 290, 205, 11.3))
c5.append(El(status("R$ 0", ok=False, size=34), 438, 132, 11.82, enter="pop", rot=6))
c5.append(El(card("tia May", "herança", "heart", w=500, h=150), 790, 205, 13.2))
c5.append(El(status("R$ 0", ok=False, size=34), 940, 132, 13.5, enter="pop", rot=6))
tot = text_img("R$ 0,00", "black", 58, ACC)
c5.append(El(card("herança total", "peter parker", "bank", w=1000, h=150, active=False, extra=tot), 540, 390, 14.0, enter="pop"))

# ---------------------------------------------------------------- CENA 6 · Nova York (escuro, avatar)
c6 = []
hd6 = vstack([text_img("custo de vida", "black", 58, WHITE, track=-0.02),
              text_img("em Nova York", "serif_i", 54, ACC2)], gap=-26, align="l")
c6.append(El(hd6, 405, 334, 14.85, anchor="l"))
c6.append(El(glass_window(920, 540, "Nova York · aluguel", "city"), 540, 840, 16.3))
c6.append(El(text_img("MÉDIA POR MÊS", "mono", 24, (200, 180, 176), track=0.2), 128, 678, 17.3, anchor="l"))
def contador(t, t0=18.0, t1=18.85):
    v = int(round(15000 * eout(lin(t, t0, t1)) / 10) * 10)
    s = "R$ " + f"{v:,}".replace(",", ".")
    big = text_img(s, "black", 118, WHITE, track=-0.02)
    if t >= t1 - 0.05: big = glow(big, 18, ACC, 0.8 * eout(lin(t, t1 - 0.05, t1 + 0.3)) + 0.01)
    return hstack([big, text_img("/mês", "mono", 34, (200, 180, 176))], gap=6)
c6.append(El(contador, 108, 768, 17.4, anchor="l"))
def barra(t, t0=18.0, t1=18.85):
    c = Cv(800, 18); c.rr(0, 0, 800, 18, 9, fill=tint(WHITE, 30))
    p = eout(lin(t, t0, t1))
    if p > 0.01: c.rr(0, 0, 800 * p, 18, 9, fill=ACC)
    im = c.done()
    return glow(im, 10, ACC, 0.7) if p > 0.01 else im
c6.append(El(barra, 540, 872, 17.4))
def quarto(t, t0=19.36):
    k = eio5(lin(t, t0, t0 + 0.7))
    w, h = mix(420, 170, k), mix(150, 100, k)
    c = Cv(440, 170)
    x0, y0 = (440 - w) / 2, (170 - h) / 2
    c.rr(x0, y0, w, h, 14, fill=tint(ACC, 40), ol=ACC, ow=3)
    lab = text_img("quarto" if k < 0.5 else "cubículo", "bold", 30, WHITE)
    paste_c(c, lab, 220, 85)
    return c.done()
c6.append(El(quarto, 540, 1000, 19.0, enter="pop"))

# ---------------------------------------------------------------- CENA 7 · apê de tijolinho (claro, moldura)
c7 = []
for n in range(3):
    c7.append(El(card(f"filme {n + 1}", None, "film", w=310, h=120), 200 + n * 340, 210, 21.45 + n * 0.12, 22.5, enter="pop"))
def ape(t):
    w, h = 960, 330
    c = bricks(w, h)
    for j in range(3):                                    # janelinhas
        x = 120 + j * 290; c.rr(x, 70, 150, 190, 10, fill=(26, 34, 52), ol=(240, 228, 220), ow=6)
        c.line([(x + 75, 70), (x + 75, 260)], (240, 228, 220), 5); c.line([(x, 165), (x + 150, 165)], (240, 228, 220), 5)
    im = shadow(c.done(), 26, 0.22, 14)
    return im
c7.append(El(ape(0), 540, 300, 22.62, enter="pop"))
c7.append(El(pill("o apê clássico", "home", 34, fill=WHITE, fg=INK, kind="black"), 540, 138, 22.85, enter="pop", layer="back"))
c7.append(El(pill("meio velho", "warn", 30, fill=INK, fg=WHITE, kind="bold"), 820, 470, 24.02, enter="pop", rot=-6))

# ---------------------------------------------------------------- CENA 8 · CTA (claro, moldura, quadro congelado)
c8 = []
FRASE = "QUAL PROFISSÃO?"
def comenta(t, t0=24.95):
    w, h = 980, 180
    c = Cv(w, h); c.rr(0, 0, w, h, 30, fill=WHITE, ol=LINE, ow=2)
    c.paste(text_img("COMENTA", "mono", 20, GRAY, track=0.3), 92, 24)
    paste_c(c, icon_img("chat", 40, INK), 56, 104)
    n = int(clamp((t - t0) / 0.07, 0, len(FRASE)))
    txt = text_img(FRASE[:n] or " ", "black", 66, ACC, track=0.06)
    c.paste(txt, 88, 104 - txt.info["base"] + 26)
    if (t * 2.2) % 1 < 0.6:
        cx = 88 + txt.width - txt.info["pad"] + 2
        c.rr(cx, 64, 5, 70, 2, fill=INK)
    paste_c(c, icon_img("film", 44, ACC), w - 60, 100)
    return shadow(c.done(), 26, 0.14, 12)
c8.append(El(comenta, 540, 240, 24.75))
c8.append(El(pill("deixa seu palpite aqui embaixo", "send", 30, fill=INK, fg=WHITE, kind="bold"), 540, 410, 25.75, out=0.01))

cenas = [Cena(0.00, 4.02, "light", CARD(960, head_w=420), c1),
         Cena(4.02, 6.22, "dark", CARD(960, head_w=420), c2),
         Cena(6.22, 8.28, "dark", FULL(230, 520), c3),
         Cena(8.28, 11.16, "light", CIRCLE(860, 384, 150), c4),
         Cena(11.16, 14.55, "light", CARD(1000, head_w=420), c5),
         Cena(14.55, 20.40, "dark", CIRCLE(230, 334, 140), c6),
         Cena(20.40, 24.62, "light", CARD(1000, head_w=420), c7),
         Cena(24.62, FIM, "light", CARD(1040, head_w=420), c8,
              zoom=lambda t: 1 + 0.035 * eio(lin(t, 24.7, FIM)))]
ed = Edicao(cenas, leg, Track(HEAD), trans=0.44, dur=FIM)

if __name__ == "__main__":
    mode = sys.argv[1]
    if mode == "stills":
        out, ts = sys.argv[6], [float(x) for x in sys.argv[7].split(",")]
        ims = []
        for t in ts:
            src, mt, fi = quadro_em(VID, MAT, min(t, 24.9))
            im = ed.frame(t, src, mt, min(fi, 747)).convert("RGB")
            ImageDraw.Draw(im).text((20, 20), f"{t:.2f}", fill=(255, 0, 255), font=font("bold", 44))
            ims.append(im if len(ts) == 1 else im.resize((360, 640), Image.LANCZOS))
        tw_, th_ = ims[0].size
        cols = min(6, len(ims)); rows = (len(ims) + cols - 1) // cols
        sheet = Image.new("RGB", (cols * tw_, rows * th_), "black")
        for i, im in enumerate(ims): sheet.paste(im, (i % cols * tw_, i // cols * th_))
        sheet.save(out, quality=90)
    else:
        out = sys.argv[6]
        fonte = Fonte(VID, MAT); saida = Saida(out)
        N = int(FIM * FPS); t0 = time.time()
        for i in range(N):
            t = i / FPS
            src, mt, fi = fonte.next()
            saida.write(ed.frame(t, src, mt, fi))
            if i % 60 == 0: print(f"{i}/{N} {time.time() - t0:.0f}s", flush=True)
        saida.close(); print("ok", time.time() - t0)
