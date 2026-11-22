import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "scripts", "molde"))  # no projeto: "../../lib"
import mvo
from mvo import Cfg, counter, checklist, notif, Image, ImageDraw, ImageFont, rr, txt, font, paste, env, eback, SS, COL, DARK, WHITE, CX, math
from functools import lru_cache

T = dict(ia=1.0, costureira=4.66, problema=5.72, balcao=7.88, cliente=8.64, pergunta=9.72, calcula=11.32, anota=12.48,
         esquece=13.62, app=15.64, foto=18.1, ajuste=19.3, barra=20.24, cintura=20.78, ziper=21.36, preco=22.38,
         fila=23.56, data=25.2, pronto=26.26, msg=27.38, continua=29.12, cuida=31.1, comenta=32.94, rodada=34.42,
         cta=36.26, redes=40.16)

PURP = (123, 91, 214); GRN = COL["green"]; INK = (30, 30, 36); GRAY = (140, 140, 150)
PW, PH = 440, 900
def lerp(a, b, k): return a + (b - a) * k
from mvo import ease

def _jeans(d, cx, top, sc, col=(52, 92, 168)):
    s_ = SS * sc
    d.rounded_rectangle([cx - 78 * s_, top, cx + 78 * s_, top + 34 * s_], radius=6 * s_, fill=col)
    d.polygon([(cx - 78 * s_, top + 30 * s_), (cx - 4 * s_, top + 30 * s_), (cx - 14 * s_, top + 200 * s_), (cx - 84 * s_, top + 200 * s_)], fill=col)
    d.polygon([(cx + 4 * s_, top + 30 * s_), (cx + 78 * s_, top + 30 * s_), (cx + 84 * s_, top + 200 * s_), (cx + 14 * s_, top + 200 * s_)], fill=col)
    lc = tuple(min(255, v + 60) for v in col)
    d.line([(cx, top + 34 * s_), (cx, top + 60 * s_)], fill=lc, width=int(3 * s_))
    d.arc([cx - 70 * s_, top + 34 * s_, cx - 20 * s_, top + 74 * s_], 0, 90, fill=lc, width=int(3 * s_))
    d.arc([cx + 20 * s_, top + 34 * s_, cx + 70 * s_, top + 74 * s_], 90, 180, fill=lc, width=int(3 * s_))
    for k in range(5): d.line([(cx - 60 * s_ + k * 30 * s_, top + 2 * s_), (cx - 60 * s_ + k * 30 * s_, top + 10 * s_)], fill=lc, width=int(2 * s_))

def phone_v2(t):
    w, h = PW * SS, PH * SS
    u = lambda v: int(v * SS)
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    rr(d, (0, 0, w - 1, h - 1), u(66), fill=(24, 24, 28))
    rr(d, (u(5), u(5), w - u(6), h - u(6)), u(62), outline=(70, 70, 78), width=u(2))
    X0, Y0, X1, Y1 = u(13), u(13), w - u(13), h - u(13)
    rr(d, (X0, Y0, X1, Y1), u(54), fill=(247, 245, 251))
    # status bar + ilha
    d.text((X0 + u(30), Y0 + u(28)), "9:41", font=font("segoeuib.ttf", 19), fill=INK, anchor="lm")
    rr(d, (w / 2 - u(58), Y0 + u(12), w / 2 + u(58), Y0 + u(44)), u(16), fill=(10, 10, 12))
    for k in range(4): d.rectangle([X1 - u(92) + k * u(7), Y0 + u(34) - u(4 + 3 * k), X1 - u(87) + k * u(7), Y0 + u(34)], fill=INK)
    rr(d, (X1 - u(56), Y0 + u(20), X1 - u(24), Y0 + u(36)), u(4), outline=INK, width=u(2))
    d.rectangle([X1 - u(53), Y0 + u(23), X1 - u(32), Y0 + u(33)], fill=INK)
    # cabeçalho
    d.ellipse([X0 + u(22), Y0 + u(66), X0 + u(72), Y0 + u(116)], fill=PURP)
    d.text((X0 + u(47), Y0 + u(91)), "A", font=font("seguibl.ttf", 24), fill=WHITE, anchor="mm")
    d.text((X0 + u(86), Y0 + u(80)), "Ateliê da Ana", font=font("segoeuib.ttf", 24), fill=INK, anchor="lm")
    d.text((X0 + u(86), Y0 + u(105)), "novo pedido", font=font("segoeui.ttf", 18), fill=GRAY, anchor="lm")
    rr(d, (X1 - u(74), Y0 + u(72), X1 - u(22), Y0 + u(110)), u(19), fill=(236, 232, 246))
    txt(d, (X1 - u(48), Y0 + u(91)), "●", font("segoeuib.ttf", 16), PURP, "mm")
    # cartão da foto
    cy0, cy1 = Y0 + u(134), Y0 + u(410)
    took = t >= T["foto"]
    if not took:
        rr(d, (X0 + u(18), cy0, X1 - u(18), cy1), u(28), fill=(28, 28, 34))
        _jeans(d, w / 2, cy0 + u(46), 0.9, (70, 70, 80))
        L = u(26)
        for (bx, by, sx, sy) in ((X0 + u(44), cy0 + u(26), 1, 1), (X1 - u(44), cy0 + u(26), -1, 1), (X0 + u(44), cy1 - u(70), 1, -1), (X1 - u(44), cy1 - u(70), -1, -1)):
            d.line([(bx, by), (bx + sx * L, by)], fill=WHITE, width=u(4)); d.line([(bx, by), (bx, by + sy * L)], fill=WHITE, width=u(4))
        d.ellipse([w / 2 - u(26), cy1 - u(60), w / 2 + u(26), cy1 - u(8)], fill=WHITE, outline=(120, 120, 128), width=u(4))
        d.text((w / 2, cy0 + u(10)), "aponte para a peça", font=font("segoeui.ttf", 15), fill=(200, 200, 208), anchor="mt")
    else:
        rr(d, (X0 + u(18), cy0, X1 - u(18), cy1), u(28), fill=(234, 229, 247))
        _jeans(d, w / 2, cy0 + u(44), 1.0)
        rr(d, (X0 + u(32), cy0 + u(14), X0 + u(146), cy0 + u(48)), u(17), fill=GRN)
        txt(d, (X0 + u(89), cy0 + u(31)), "✓ foto ok", font("segoeuib.ttf", 16), WHITE, "mm")
        fl = max(0.0, 1 - (t - T["foto"]) / 0.3)
        if fl > 0:
            ov = Image.new("RGBA", (w, h), (255, 255, 255, 0))
            ImageDraw.Draw(ov).rounded_rectangle([X0 + u(18), cy0, X1 - u(18), cy1], radius=u(28), fill=(255, 255, 255, int(255 * fl)))
            im.alpha_composite(ov); d = ImageDraw.Draw(im)
    # ajustes
    d.text((X0 + u(26), Y0 + u(436)), "AJUSTES", font=font("consolab.ttf", 15), fill=GRAY, anchor="lm")
    rows = [("Barra", "✂", 15, T["barra"]), ("Cintura", "◎", 12, T["cintura"]), ("Zíper", "⇕", 8, T["ziper"])]
    total = 0
    for i, (lab, ic, pr, tt) in enumerate(rows):
        y = Y0 + u(458 + i * 70)
        on = ease((t - tt) / 0.22)
        if t >= tt: total += pr
        rr(d, (X0 + u(18), y, X1 - u(18), y + u(60)), u(18), fill=WHITE, outline=(PURP if on > 0.5 else (232, 230, 238)), width=u(2))
        d.ellipse([X0 + u(30), y + u(10), X0 + u(70), y + u(50)], fill=(236, 232, 246))
        sym = ImageFont.truetype(r"C:\Windows\Fonts\seguisym.ttf", u(20))
        d.text((X0 + u(50), y + u(30)), ic, font=sym, fill=PURP, anchor="mm")
        d.text((X0 + u(84), y + u(30)), lab, font=font("segoeuib.ttf", 22), fill=INK, anchor="lm")
        d.text((X1 - u(104), y + u(30)), f"+R$ {pr}", font=font("segoeui.ttf", 17), fill=GRAY, anchor="rm")
        sx0 = X1 - u(88); c = tuple(int(lerp(a, b, on)) for a, b in zip((214, 214, 220), PURP))
        rr(d, (sx0, y + u(16), sx0 + u(56), y + u(44)), u(14), fill=c)
        kx = sx0 + u(14) + on * u(28); d.ellipse([kx - u(11), y + u(19), kx + u(11), y + u(41)], fill=WHITE)
    # total
    ty = Y0 + u(676); hot = t >= T["preco"]
    rr(d, (X0 + u(18), ty, X1 - u(18), ty + u(70)), u(20), fill=(GRN if hot else (236, 232, 246)))
    d.text((X0 + u(36), ty + u(24)), "total", font=font("segoeui.ttf", 17), fill=(WHITE if hot else GRAY), anchor="lm")
    d.text((X0 + u(36), ty + u(50)), "entrega: quinta" if hot else "selecione os ajustes", font=font("segoeuib.ttf", 15), fill=(WHITE if hot else GRAY), anchor="lm")
    pop = 1 + (0.12 * math.sin(min(1, (t - T["preco"]) / 0.3) * math.pi) if hot and t - T["preco"] < 0.3 else 0)
    d.text((X1 - u(36), ty + u(36)), f"R$ {total},00", font=font("seguibl.ttf", int(32 * pop)), fill=(WHITE if hot else INK), anchor="rm")
    # botão
    by = Y0 + u(764); pressed = T["preco"] + 0.35 <= t <= T["preco"] + 0.6
    rr(d, (X0 + u(18), by, X1 - u(18), by + u(64)), u(22), fill=(96, 68, 190) if pressed else PURP)
    d.text((w / 2, by + u(32)), "Confirmar pedido", font=font("segoeuib.ttf", 22), fill=WHITE, anchor="mm")
    d.rounded_rectangle([w / 2 - u(70), Y1 - u(14), w / 2 + u(70), Y1 - u(9)], radius=u(3), fill=INK)
    # toque do dedo
    taps = [(T["foto"] - 0.05, (w / 2, cy1 - u(34))), (T["barra"] - 0.05, (X1 - u(60), Y0 + u(488))),
            (T["cintura"] - 0.05, (X1 - u(60), Y0 + u(558))), (T["ziper"] - 0.05, (X1 - u(60), Y0 + u(628))), (T["preco"] + 0.35, (w / 2, by + u(32)))]
    for (tt, (px, py)) in taps:
        k = (t - tt) / 0.45
        if 0 <= k <= 1:
            r = u(18 + 26 * k); a = int(200 * (1 - k))
            ov = Image.new("RGBA", (w, h), (0, 0, 0, 0)); od = ImageDraw.Draw(ov)
            od.ellipse([px - r, py - r, px + r, py + r], outline=(30, 30, 36, a), width=u(4))
            od.ellipse([px - u(16), py - u(16), px + u(16), py + u(16)], fill=(30, 30, 36, int(110 * (1 - k))))
            im.alpha_composite(ov)
    return im

def counters(base, t, f):
    n = sum(1 for i in range(4) if t >= T["fila"] + 0.5 + i * 0.25)
    counter(base, t, T["fila"] - 0.1, T["continua"], f"{n}", "pedidos na fila", "orange" if n else None, 0)

def extras(base, t, f):
    a = env(t, 17.45, T["fila"] - 0.1, 0.35, 0.3)
    if a > 0:
        k = eback((t - 17.45) / 0.5)
        paste(base, phone_v2(t), CX, 690 + 120 * (1 - min(k, 1.0)), a, 0.85 + 0.15 * min(k, 1.1), "c", shadow=True)
    checklist(base, t, T["data"] - 0.2, T["continua"] - 0.2, "fila • data de entrega",
              ["#1 calça · qui", "#2 vestido · sex", "#3 camisa · sáb", "#4 saia · seg"], (T["pronto"],), "green", y=520)
    notif(base, t, T["msg"], T["continua"] - 0.1, "Ateliê • cliente", "Seu ajuste está pronto ✓", "purple", y=985)

C = Cfg(
    chips=[("1", "PROFISSÃO", "purple", T["costureira"] - 1.3), ("2", "PROBLEMA", "red", T["problema"]), ("3", "APP", "blue", T["app"]),
           ("4", "FILA", "orange", T["fila"]), ("5", "RESULTADO", "green", T["continua"])],
    chips_on=(T["costureira"] - 1.6, T["cta"]), chips_all=T["cuida"],
    calls=[
        (T["balcao"], 9.6, "o problema: o balcão", "balcao", 0, -260, "fill", "red", True),
        (T["calcula"], 12.4, "de cabeça", "cost", -170, -220, "line", "red"),
        (T["anota"], 13.6, "caderno", "caderno", -120, -160, "line", "red"),
        (T["esquece"] + 0.3, 15.5, "quem pediu o quê? ✕", None, 0, 1000, "fill", "red", True),
        (T["comenta"], 36.1, "comenta a sua profissão", None, 0, 900, "dark", None, True),
        (T["rodada"], 36.1, "próxima rodada ▶", None, 0, 980, "fill", "orange", True),
    ],
    titles_2d=[(T["costureira"] - 1.3, T["costureira"] - 0.1, "1", "PROFISSÃO", "purple"), (T["problema"], T["problema"] + 1.3, "2", "PROBLEMA", "red"),
            (T["app"], T["app"] + 1.0, "3", "APP", "blue"), (T["fila"], T["fila"] + 1.2, "4", "FILA", "orange"),
            (T["continua"], T["continua"] + 1.2, "5", "RESULTADO", "green"), (T["cuida"], T["comenta"] - 0.1, "", "IA NO BALCÃO", "purple")],
    titles=[], chip_style="stepper", shadow=True, steps_hide=[(T["app"] + 0.7, T["fila"] - 0.1)],
    counters=counters, late=[extras], flash=[T["foto"]], vignette=[(T["esquece"], 15.5, (200, 50, 60))],
    cta=(T["cta"], T["redes"]), tag=("ilustrativo", T["costureira"] - 1.6),
)
mvo.main(C)
