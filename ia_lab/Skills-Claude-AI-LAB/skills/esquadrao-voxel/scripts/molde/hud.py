# Esquadrão Voxel — HUD 2D desenhado por cima do render (PIL). Identidade própria:
#   título = adesivo creme com contorno grosso e sombra dura (levemente torto), chip limão com o nº do personagem
#   contador = cartão-adesivo com rótulo + número colorido (sobe contando)
#   legenda = palavra por palavra em etiquetas escuras (serif), palavra-chave em etiqueta limão
#   terminal = pílula escura com prompt digitando
#   cartões = doc digitando, onda de áudio, notificação/DM, comentário, coração, carimbo, estouro, check
# Uso no overlay.py do projeto:  H = hud.HUD(); H.titulos = [...]; ...; def desenhar(img, t): H.desenhar(img, t)
import math, random, functools, json
from PIL import Image, ImageDraw, ImageFilter
from telas import F, texto, tlen, INK, CREME, LIMA, CORAL, AZUL, ROXO, AMARELO, VERDE

W, H_ = 1080, 1920
CX = 490                 # centro seguro na metade de baixo (botões do Instagram em x ≥ 870)
OUT = 7                  # contorno
SOMBRA = (9, 10)

def clamp(a, lo=0.0, hi=1.0): return max(lo, min(hi, a))
def ease(a): a = clamp(a); return a * a * a * (a * (a * 6 - 15) + 10)
def eout(a): a = clamp(a); return 1 - (1 - a) ** 3
def eback(a, c1=1.9):
    a = clamp(a); c3 = c1 + 1; return 1 + c3 * (a - 1) ** 3 + c1 * (a - 1) ** 2
def pop(t, t0, t1=1e9, fi=0.32, fo=0.2):
    if t < t0 or t > t1 + fo: return 0.0
    a = eback((t - t0) / fi)
    return a * (1 - eout((t - t1) / fo)) if t > t1 else a

def tsize(d, txt, f):
    b = d.textbbox((0, 0), txt, font=f); return b[2] - b[0], b[3] - b[1], b
_D = ImageDraw.Draw(Image.new("RGB", (8, 8)))

def adesivo(w, h, fill=CREME, r=24, outline=INK, sombra=True):
    """base de cartão estilo adesivo: contorno grosso + sombra dura."""
    w, h = int(w), int(h); sx, sy = SOMBRA if sombra else (0, 0)
    im = Image.new("RGBA", (w + sx + 4, h + sy + 4), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    if sombra: d.rounded_rectangle((sx + 2, sy + 2, w + sx, h + sy), r, fill=INK)
    d.rounded_rectangle((2, 2, w, h), r, fill=fill, outline=outline, width=OUT)
    return im, d

def colar(base, el, cx, cy, s=1.0, rot=0.0, alpha=1.0):
    """cola um elemento RGBA centrado em (cx,cy) com escala/rotação/opacidade."""
    if s <= 0.01 or alpha <= 0.01: return
    e = el
    if abs(s - 1) > 0.003: e = e.resize((max(1, int(e.width * s)), max(1, int(e.height * s))), Image.BICUBIC)
    if abs(rot) > 0.05: e = e.rotate(rot, expand=True, resample=Image.BICUBIC)
    if alpha < 0.999:
        a = e.split()[3].point(lambda v: int(v * alpha)); e = e.copy(); e.putalpha(a)
    base.alpha_composite(e, (int(cx - e.width / 2), int(cy - e.height / 2)))

@functools.lru_cache(maxsize=64)
def el_titulo(texto, num):
    chip = 96 if num is not None else 0
    tam = 58
    while True:   # encolhe a fonte até caber na safe zone (máx. 870 px de largura)
        f = F("titulo", tam); tw, th, b = tsize(_D, texto, f)
        if tw + 80 + chip <= 870 or tam <= 34: break
        tam -= 2
    w = tw + 80 + chip; h = 112
    im, d = adesivo(w, h)
    if num is not None:
        d.rounded_rectangle((18, 18, 18 + 76, h - 18), 16, fill=LIMA, outline=INK, width=4)
        ft = F("titulo", 40); cw, ch, cb = tsize(d, str(num), ft)
        d.text((18 + 38 - cw / 2 - cb[0], h / 2 - ch / 2 - cb[1]), str(num), font=ft, fill=INK)
    x0 = chip + (w - chip) / 2 - tw / 2 - b[0]
    d.text((x0, h / 2 - th / 2 - b[1] + 2), texto, font=f, fill=INK)
    return im

@functools.lru_cache(maxsize=256)
def el_contador(rotulo, valor, cor):
    l1, _, l2 = rotulo.partition("|")
    fl = F("bold", 26); fn = F("titulo", 64)
    vw = tlen(_D, valor, fn); _, vh, vb = tsize(_D, valor.replace("✓", "") or "0", fn)
    lw = max(tsize(_D, l1, fl)[0], tsize(_D, l2, fl)[0] if l2 else 0)
    w = lw + vw + 90; h = 104
    im, d = adesivo(w, h, r=20)
    if l2:
        d.text((28, 22), l1, font=fl, fill=INK); d.text((28, 54), l2, font=fl, fill=INK)
    else:
        d.text((28, 36), l1, font=fl, fill=INK)
    texto(d, (w - 26 - vw - vb[0], h / 2 - vh / 2 - vb[1]), valor, fn, cor)
    return im

@functools.lru_cache(maxsize=512)
def el_palavra(txt, chave):
    f = F("serif", 60)
    tw, th, b = tsize(_D, txt, f)
    w, h = tw + 36, 84
    im = Image.new("RGBA", (w + 8, h + 8), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle((6, 7, w + 6, h + 7), 14, fill=(0, 0, 0, 120))
    d.rounded_rectangle((0, 0, w, h), 14, fill=LIMA if chave else INK)
    d.text((w / 2 - tw / 2 - b[0], h / 2 - th / 2 - b[1] - 2), txt, font=f, fill=INK if chave else CREME)
    return im


class HUD:
    def __init__(s):
        s.titulos = []         # [(t, "TEXTO", numero_ou_None)]
        s.contadores = []      # [(t0, t1, "ROTULO|2ª LINHA", [(t, valor_int)], cor, sufixo)]
        s.palavras = []        # [{"w","s","e"}]
        s.chaves = set()       # palavras destacadas (minúsculas, sem pontuação)
        s.grupos = []
        s.terminais = []       # [(t0, t1, texto, t_dig0, t_dig1)]
        s.extras = []          # funções f(img, t) — cartões e efeitos do projeto
        s.y_titulo = 312; s.y_cont = 446; s.x_cont = 620; s.y_leg = 1395; s.y_term = 1270

    # ---------------------------------------------------------------- legenda
    def legenda(s, palavras, chaves=(), max_pal=3, gap=0.32):
        s.palavras = palavras; s.chaves = {c.lower() for c in chaves}
        g = []; cur = []
        for i, w in enumerate(palavras):
            if cur and (len(cur) >= max_pal or w["s"] - cur[-1]["e"] > gap): g.append(cur); cur = []
            cur.append(w)
            if w["w"][-1:] in ".,!?:": g.append(cur); cur = []
        if cur: g.append(cur)
        s.grupos = g

    def _leg(s, img, t):
        for gi, g in enumerate(s.grupos):
            t0 = g[0]["s"] - 0.05
            t1 = (s.grupos[gi + 1][0]["s"] - 0.05) if gi + 1 < len(s.grupos) else g[-1]["e"] + 0.8
            t1 = min(t1, g[-1]["e"] + 0.9)
            if not (t0 <= t < t1): continue
            els = []
            for w in g:
                if t < w["s"] - 0.04: break
                txt = w["w"].strip(",.!?:;")
                ch = txt.lower() in s.chaves
                els.append((el_palavra(txt, ch), w["s"] - 0.04, ch))
            if not els: return
            gapx = 10; tot = sum(e.width for e, *_ in els) + gapx * (len(els) - 1)
            x = CX - tot / 2
            for k, (e, ts, ch) in enumerate(els):
                a = eback((t - ts) / 0.22, 2.4); rnd = random.Random(int(ts * 100))
                rot = rnd.uniform(-3, 3) if ch else rnd.uniform(-1.2, 1.2)
                colar(img, e, x + e.width / 2, s.y_leg - (1 - clamp((t - ts) / 0.18)) * 18, 0.6 + 0.4 * a, rot, clamp((t - ts) / 0.08))
                x += e.width + gapx
            return

    # ---------------------------------------------------------------- título
    def _tit(s, img, t):
        cur = None
        for i, (ti, txt, num) in enumerate(s.titulos):
            if t >= ti: cur = i
        if cur is None: return
        ti, txt, num = s.titulos[cur]
        el = el_titulo(txt, num)
        a = eback((t - ti) / 0.38, 2.0) if cur > 0 or ti > 0 else 1.0
        wob = math.sin(t * 1.3) * 0.35
        rot = -1.6 + wob + (1 - clamp((t - ti) / 0.3)) * 6 * (1 if cur % 2 else -1)
        colar(img, el, W / 2, s.y_titulo, 0.55 + 0.45 * a, rot, clamp((t - ti) / 0.1) if ti > 0 else 1)

    # ---------------------------------------------------------------- contador
    def _cont(s, img, t):
        for (t0, t1, rot, keys, cor, suf) in s.contadores:
            a = pop(t, t0, t1, 0.35, 0.2)
            if a <= 0: continue
            v = keys[0][1]; tk = -9
            for (ta, va), (tb, vb) in zip(keys, keys[1:] + [keys[-1]]):
                if t >= ta: v = va; tk = ta
                if ta <= t < tb and tb > ta and vb != va and isinstance(vb, (int, float)) and (tb - ta) < 3:
                    v = round(va + (vb - va) * ease((t - ta) / (tb - ta))); tk = ta
            val = f"{v}{suf}" if not isinstance(v, str) else v
            el = el_contador(rot, val, cor)
            bump = 1 + 0.08 * max(0, 1 - (t - tk) / 0.18) if t - tk < 0.18 else 1
            colar(img, el, s.x_cont, s.y_cont, a * bump, 1.2)

    # ---------------------------------------------------------------- terminal
    def _term(s, img, t):
        for (t0, t1, txt, d0, d1) in s.terminais:
            a = pop(t, t0, t1, 0.3, 0.2)
            if a <= 0: continue
            n = int(len(txt) * clamp((t - d0) / max(0.01, d1 - d0)))
            w, h = 820, 82
            el = Image.new("RGBA", (w + 12, h + 12), (0, 0, 0, 0)); d = ImageDraw.Draw(el)
            d.rounded_rectangle((8, 10, w + 8, h + 10), 22, fill=(0, 0, 0, 140))
            d.rounded_rectangle((0, 0, w, h), 22, fill="#100E18", outline="#2E2A40", width=3)
            f = F("mono", 34)
            d.text((28, 18), ">", font=f, fill=LIMA)
            d.text((64, 18), txt[:n], font=f, fill="#F4F1FA")
            if int(t * 3) % 2 == 0 or n < len(txt):
                cw = d.textlength(txt[:n], font=f)
                d.rectangle((66 + cw, 20, 66 + cw + 18, 62), fill=LIMA)
            colar(img, el, CX, s.y_term, 0.8 + 0.2 * a, 0, clamp(a))

    def desenhar(s, img, t):
        """img: PIL RGBA 1080x1920 (o render). Desenha tudo por cima."""
        for f in s.extras: f(img, t)
        s._tit(img, t); s._cont(img, t); s._term(img, t); s._leg(img, t)


# ---------------------------------------------------------------- cartões prontos (usar em H.extras)
def cartao_doc(t0, t1, titulo, linhas, cx=480, cy=760, t_dig=(None, None), w=640, destaque=None, rot=-2.0):
    """folha que vai sendo escrita (letra por letra entre t_dig)."""
    d0, d1 = t_dig if t_dig[0] else (t0 + 0.3, t1 - 0.3)
    total = sum(len(l) for l in linhas)
    def f(img, t):
        a = pop(t, t0, t1)
        if a <= 0: return
        n = int(total * clamp((t - d0) / max(0.01, d1 - d0)))
        h = 120 + 66 * len(linhas)
        el, d = adesivo(w, h, "#FFFDF7", 22)
        d.rounded_rectangle((2, 2, w, 70), 22, fill=INK); d.rectangle((2, 40, w, 70), fill=INK)
        d.text((28, 16), titulo, font=F("titulo", 34), fill=LIMA)
        y = 96; k = n
        for i, l in enumerate(linhas):
            vis = l[:max(0, k)]; k -= len(l)
            if destaque is not None and i == destaque and len(vis) == len(l):
                d.rectangle((22, y - 4, 30 + d.textlength(l, font=F("bold", 34)), y + 46), fill=LIMA)
            d.text((28, y), vis, font=F("bold", 34), fill=INK)
            if 0 < len(vis) < len(l) and int(t * 6) % 2 == 0:
                d.rectangle((30 + d.textlength(vis, font=F("bold", 34)), y + 2, 40 + d.textlength(vis, font=F("bold", 34)), y + 42), fill=INK)
            y += 66
        colar(img, el, cx, cy, a, rot)
    return f

def cartao_onda(t0, t1, titulo="voz.wav", cx=480, cy=760, w=660, cor=CORAL, nivel=None):
    """onda de áudio viva (nivel(t)->0..1 opcional, ex. volume real da locução)."""
    def f(img, t):
        a = pop(t, t0, t1)
        if a <= 0: return
        h = 260; el, d = adesivo(w, h, "#100E18", 22, outline=INK)
        d.ellipse((26, 24, 50, 48), fill=CORAL if int(t * 2) % 2 == 0 else "#5B2A2A")
        d.text((62, 18), "REC  " + titulo, font=F("bold", 28), fill="#F4F1FA")
        lv = nivel(t) if nivel else 0.7
        for i in range(40):
            x = 30 + i * (w - 60) / 40
            amp = (0.25 + 0.75 * abs(math.sin(i * 0.7 + t * 9) * math.sin(i * 0.23 + t * 3.1))) * lv * 80 + 6
            d.rounded_rectangle((x, 160 - amp, x + 9, 160 + amp), 4, fill=cor)
        colar(img, el, cx, cy, a, 1.5)
    return f

def notificacao(t0, t1, app_nome, titulo, sub, cx=490, cy=640, w=770, icone=LIMA, rot=0.0):
    def f(img, t):
        a = pop(t, t0, t1, 0.4)
        if a <= 0: return
        h = 190; el, d = adesivo(w, h, "#FFFFFF", 30)
        d.rounded_rectangle((26, 26, 82, 82), 16, fill=icone, outline=INK, width=3)
        d.text((100, 30), app_nome, font=F("bold", 28), fill="#6A6578"); d.text((100 + d.textlength(app_nome, font=F("bold", 28)) + 14, 30), "agora", font=F("semi", 26), fill="#9C97A8")
        texto(d, (30, 96), titulo, F("titulo", 40), INK)
        d.text((30, 146), sub, font=F("semi", 28), fill="#4A4558")
        colar(img, el, cx, cy - (1 - clamp((t - t0) / 0.35)) * 60, a, rot)
    return f

def comentario(t0, t1, msg, t_dig, t_pub, cx=490, cy=1090, w=760):
    def f(img, t):
        a = pop(t, t0, t1)
        if a <= 0: return
        h = 96; el, d = adesivo(w, h, "#FFFFFF", 48)
        n = int(len(msg) * clamp((t - t_dig) / 0.5))
        d.ellipse((22, 22, 74, 74), fill=CORAL, outline=INK, width=3)
        txt = msg[:n] if n else "Adicione um comentário..."
        d.text((94, 26), txt, font=F("bold", 36) if n else F("semi", 32), fill=INK if n else "#9C97A8")
        pub = t >= t_pub
        bx = w - 230; d.rounded_rectangle((bx, 16, w - 16, h - 16), 32, fill=VERDE if pub else CORAL, outline=INK, width=3)
        lab = "Publicado ✓" if pub else "Publicar"
        fl = F("bold", 28); texto(d, (bx + (w - 16 - bx) / 2 - tlen(d, lab, fl) / 2, 30), lab, fl, INK if pub else "#FFFFFF")
        k = 1 + 0.06 * max(0, 1 - (t - t_pub) / 0.2) if t >= t_pub else 1
        colar(img, el, cx, cy, a * k)
    return f

@functools.lru_cache(maxsize=4)
def _coracao(sz=300):
    im = Image.new("RGBA", (sz + 20, sz + 20), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    pts = []
    for i in range(80):
        a = i / 80 * 2 * math.pi
        x = 16 * math.sin(a) ** 3; y = 13 * math.cos(a) - 5 * math.cos(2 * a) - 2 * math.cos(3 * a) - math.cos(4 * a)
        pts.append((sz / 2 + 10 + x * sz / 36, sz / 2 + 4 - y * sz / 36))
    d.polygon([(x + 10, y + 12) for x, y in pts], fill=INK)
    d.polygon(pts, fill="#FF4D6D", outline=INK, width=8)
    d.ellipse((sz * 0.25, sz * 0.22, sz * 0.38, sz * 0.36), fill=(255, 255, 255, 170))
    return im
def coracao(t0, t1, cx=480, cy=720):
    def f(img, t):
        a = pop(t, t0, t1, 0.4)
        if a <= 0: return
        colar(img, _coracao(), cx, cy, a * (1 + 0.05 * math.sin((t - t0) * 12)), -6)
    return f

def carimbo(t0, t1, texto, cor=CORAL, cx=520, cy=760, rot=-10):
    """carimbo que bate (entra grande e assenta)."""
    def f(img, t):
        if t < t0 or t > t1 + 0.2: return
        k = clamp((t - t0) / 0.18); s = 1.9 - 0.9 * eout(k)
        fo = 1 - eout((t - t1) / 0.2) if t > t1 else 1
        ft = F("titulo", 92); tw = _D.textlength(texto, font=ft)
        w, h = int(tw + 80), 150
        el = Image.new("RGBA", (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(el)
        d.rounded_rectangle((6, 6, w - 6, h - 6), 18, fill=(255, 250, 240, 235), outline=cor, width=12)
        d.text((40, 22), texto, font=ft, fill=cor)
        colar(img, el, cx, cy, s, rot, k * fo)
    return f

def estouro(t0, t1, texto, cor=LIMA, cx=490, cy=700):
    """estrela de quadrinho com a palavra (CTA)."""
    def f(img, t):
        a = pop(t, t0, t1, 0.35)
        if a <= 0: return
        sz = 620; el = Image.new("RGBA", (sz, sz), (0, 0, 0, 0)); d = ImageDraw.Draw(el)
        pts = []
        for i in range(28):
            r = sz * (0.47 if i % 2 == 0 else 0.33); ang = i / 28 * 2 * math.pi + t * 0.6
            pts.append((sz / 2 + r * math.cos(ang), sz / 2 + r * math.sin(ang)))
        d.polygon([(x + 12, y + 14) for x, y in pts], fill=INK)
        d.polygon(pts, fill=cor, outline=INK, width=8)
        ft = F("titulo", 150); tw, th, b = tsize(d, texto, ft)
        for dx, dy in ((6, 8),): d.text((sz / 2 - tw / 2 - b[0] + dx, sz / 2 - th / 2 - b[1] + dy), texto, font=ft, fill=INK)
        d.text((sz / 2 - tw / 2 - b[0], sz / 2 - th / 2 - b[1]), texto, font=ft, fill="#FFFFFF", stroke_width=8, stroke_fill=INK)
        colar(img, el, cx, cy, a, -8 + 3 * math.sin(t * 3))
    return f

def selo(t0, t1, txt, cor=VERDE, cx=700, cy=900, rot=6):
    """pílula de status ('✓ AGENDADO 18:00')."""
    def f(img, t):
        a = pop(t, t0, t1)
        if a <= 0: return
        ft = F("titulo", 46); tw = tlen(_D, txt, ft)
        el, d = adesivo(int(tw + 70), 96, cor, 48)
        texto(d, (36, 18), txt, ft, INK)
        colar(img, el, cx, cy, a, rot)
    return f

def cartao_img(t0, t1, path, cx, cy, largura=600, rot=0):
    """qualquer PNG (print real, logo, tela) num cartão-adesivo."""
    src = Image.open(path).convert("RGBA")
    k = largura / src.width; src = src.resize((largura, int(src.height * k)), Image.LANCZOS)
    el, d = adesivo(largura + 24, src.height + 24, "#FFFFFF", 22)
    el.alpha_composite(src, (14, 14))
    def f(img, t):
        a = pop(t, t0, t1)
        if a > 0: colar(img, el, cx, cy, a, rot)
    return f

def flash(t0, dur=0.12, cor=(255, 255, 255)):
    def f(img, t):
        if t0 <= t < t0 + dur:
            a = 1 - (t - t0) / dur
            img.alpha_composite(Image.new("RGBA", img.size, cor + (int(120 * a),)))
    return f

def confete(t0, t1, n=70, seed=4):
    R = random.Random(seed)
    ps = [(R.uniform(80, 1000), R.uniform(-200, 300), R.uniform(-120, 120), R.uniform(500, 900), R.choice([LIMA, CORAL, AZUL, AMARELO, ROXO, "#FFFFFF"]), R.uniform(0, 6)) for _ in range(n)]
    def f(img, t):
        if not (t0 <= t <= t1): return
        d = ImageDraw.Draw(img); lt = t - t0
        for (x, y, vx, vy, c, ph) in ps:
            px = x + vx * lt + 20 * math.sin(lt * 5 + ph); py = y + vy * lt * 0.9 + 160 * lt * lt
            if py > 1500: continue
            s = 9 + 5 * math.sin(lt * 9 + ph)
            d.rectangle((px - 7, py - s, px + 7, py + s), fill=c)
    return f


def trilho(t0, t1, etapas, tempos, cy=312, cor=LIMA):
    """barra de etapas: chips que acendem quando o objeto muda (tempos = quando cada etapa acende)."""
    fl = F("titulo", 30)
    ws = [int(tlen(_D, e, fl)) + 40 for e in etapas]; gap = 34
    tot = sum(ws) + gap * (len(ws) - 1)
    k = min(1.0, 780 / tot)
    def f(img, t):
        a = pop(t, t0, t1, 0.35)
        if a <= 0: return
        el = Image.new("RGBA", (tot + 30, 110), (0, 0, 0, 0)); d = ImageDraw.Draw(el)
        x = 6
        for i, (e, w) in enumerate(zip(etapas, ws)):
            on = t >= tempos[i]; cur = on and (i + 1 >= len(tempos) or t < tempos[i + 1])
            fill = cor if on else "#FFF6E5"
            y0 = 22 - (6 if cur else 0)
            d.rounded_rectangle((x + 6, y0 + 8, x + w + 6, y0 + 74), 18, fill=INK)
            d.rounded_rectangle((x, y0, x + w, y0 + 66), 18, fill=fill, outline=INK, width=5)
            texto(d, (x + 20, y0 + 14), e, fl, INK)
            if i < len(etapas) - 1:
                ax = x + w + 6; d.polygon([(ax, y0 + 24), (ax + gap - 12, y0 + 33), (ax, y0 + 42)], fill=INK)
            x += w + gap
        colar(img, el, W / 2, cy, a * k, 0)
    return f

def cartao_planta(t0, t1, titulo="PLANTA DA FÁBRICA", etapas=("IDEIA", "ROTEIRO", "VOZ", "VÍDEO", "POST"), cx=490, cy=720, w=780, carimbo_t=None, carimbo_txt="GUIA"):
    """planta azul (blueprint) que desenrola, com o fluxo desenhado e carimbo da palavra do CTA."""
    def f(img, t):
        a = pop(t, t0, t1, 0.4)
        if a <= 0: return
        k = eout((t - t0) / 0.5); h = int(60 + 520 * k)
        el, d = adesivo(w, h, "#1F4E9E", 18)
        for gx in range(20, w, 40): d.line((gx, 4, gx, h - 4), fill="#2E62B8", width=2)
        for gy in range(20, h, 40): d.line((4, gy, w - 4, gy), fill="#2E62B8", width=2)
        d.text((34, 24), titulo, font=F("titulo", 40), fill="#FFFFFF")
        if h > 200:
            n = len(etapas); bw = (w - 80) / n
            for i, e in enumerate(etapas):
                x0 = 40 + i * bw; yy = 150 + (i % 2) * 130
                if yy + 100 > h: continue
                d.rounded_rectangle((x0 + 6, yy, x0 + bw - 6, yy + 90), 12, outline="#FFFFFF", width=4)
                fe = F("bold", 24); d.text((x0 + bw / 2 - d.textlength(e, font=fe) / 2, yy + 30), e, font=fe, fill="#FFFFFF")
                if i < n - 1: d.line((x0 + bw - 6, yy + 45, x0 + bw + 6, 150 + ((i + 1) % 2) * 130 + 45), fill="#FFFFFF", width=3)
        colar(img, el, cx, cy, a, -2)
        if carimbo_t and t >= carimbo_t:
            carimbo(carimbo_t, t1, carimbo_txt, CORAL, cx + 150, cy + 170, -12)(img, t)
    return f
