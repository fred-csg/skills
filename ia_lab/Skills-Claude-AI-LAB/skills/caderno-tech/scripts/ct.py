# caderno-tech · motor gráfico (PIL + numpy + ffmpeg), em cima do dx.py (base comum das skills).
# Lista numerada estilo "caderno técnico": cenas alternando ESCURO (azul-noite com brilho e grade fina)
# e PAPEL (off-white quadriculado), a cena nova SOBE por cima da anterior como uma folha;
# cabeçalho mono "// troca 1 ......... STATUS #01", título que aparece palavra a palavra junto com a
# fala (sans pesada + palavra-chave em serif itálico colorida), número-fantasma gigante em serif no fundo,
# cartão "de" (ícone + nome + preço) que apaga, cartão "para" (branco, ícone, nome, descrição, rodapé
# mono + selo ★), carimbo inclinado ("US$ 0"), recibo com total contando e riscando, onda de áudio,
# contador grande, grade de chips, barra de busca digitando, comentário + seguir, DM com checklist.
import math, os, re, sys, numpy as np
from functools import lru_cache
from PIL import Image, ImageDraw, ImageFilter

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import dx
from dx import (W, H, FPS, FFM, K, Cv, put, put_tl, spr_palavra, font, tw, clamp, lin, eio, eout, ein, eback,
                mix, mixc, janela, brilho_blob, mascara, borrao_v, vidro, TIPOS, tipo, dims, leitor, partes)

X0 = 95                      # margem lateral (safe zone)
XW = W - 2 * X0              # largura útil (890)

# ---------------------------------------------------------------- paletas
# escuro: fundo base / brilho · papel: fundo claro · acento: preenchimento (selos, chips, carimbos)
# claro: palavra-chave no escuro · tinta: palavra-chave no papel · sobre: texto em cima do acento
PALETAS = {
    "cobalto":  dict(base=(5, 9, 34),   brilho=(38, 66, 225),  papel=(236, 236, 231), acento=(36, 58, 226),
                     claro=(132, 146, 255), tinta=(36, 58, 226), sobre=(255, 255, 255)),          # padrão
    "lima":     dict(base=(9, 11, 9),   brilho=(96, 140, 20),  papel=(238, 238, 230), acento=(196, 255, 62),
                     claro=(196, 255, 62), tinta=(70, 120, 0),   sobre=(14, 16, 10)),            # AI LAB
    "laranja":  dict(base=(16, 14, 14), brilho=(200, 80, 20),  papel=(240, 236, 228), acento=(255, 106, 26),
                     claro=(255, 150, 90), tinta=(222, 84, 10),  sobre=(255, 255, 255)),
    "vinho":    dict(base=(30, 6, 14),  brilho=(150, 28, 62),  papel=(242, 234, 222), acento=(176, 24, 64),
                     claro=(255, 140, 172), tinta=(166, 22, 60), sobre=(255, 255, 255)),
    "floresta": dict(base=(5, 22, 16),  brilho=(20, 120, 78),  papel=(236, 238, 230), acento=(14, 138, 88),
                     claro=(110, 230, 170), tinta=(10, 120, 76), sobre=(255, 255, 255)),
    "violeta":  dict(base=(14, 8, 34),  brilho=(110, 60, 230), papel=(238, 236, 242), acento=(112, 64, 240),
                     claro=(184, 160, 255), tinta=(104, 56, 226), sobre=(255, 255, 255)),
}
C = {}
TXT_ESC, TXT_PAP = (246, 247, 250), (22, 24, 34)
DIM_ESC, DIM_PAP = (150, 156, 190), (120, 122, 132)

def set_paleta(nome="cobalto", acento=None):
    C.clear(); C.update(PALETAS.get(nome, PALETAS["cobalto"]))
    if acento:
        a = tuple(acento)
        C.update(acento=a, claro=mixc(a, (255, 255, 255), 0.45), tinta=a, brilho=mixc(a, (0, 0, 0), 0.1),
                 sobre=(14, 14, 14) if dx.lum(a) > 0.55 else (255, 255, 255))
    C["nome"] = nome
    dx.set_paleta("lima")                         # base do dx (aura dos clipes etc.) segue o acento
    dx.P.update(acento=C["acento"], bom=C["acento"], sobre=C["sobre"])
    _bg_cache.clear()
    for fn in (_icone, _spr_item, _spr_card, _spr_carimbo, _spr_recibo_base, _chrome_static):
        fn.cache_clear()

# fontes extras desta skill
dx.FONTES.update(sans=("Inter-ExtraBold.ttf", "Poppins-Bold.ttf", "segoeuib.ttf"),
                 serif=("InstrumentSerif-Italic.ttf", "georgiai.ttf", "timesi.ttf"),
                 ui=("Poppins-SemiBold.ttf", "seguisb.ttf", "arial.ttf"),
                 uib=("Poppins-Bold.ttf", "segoeuib.ttf", "arialbd.ttf"))

def txt_cor(modo): return TXT_ESC if modo == "escuro" else TXT_PAP
def dim_cor(modo): return DIM_ESC if modo == "escuro" else DIM_PAP
def destaque_cor(modo): return C["claro"] if modo == "escuro" else C["tinta"]

# ---------------------------------------------------------------- fundos (cache por modo)
_bg_cache = {}
_GR = []
def _grao(i):
    if not _GR:
        rng = np.random.default_rng(11)
        for _ in range(5): _GR.append(rng.normal(0, 3.0, (H, W, 1)).astype(np.float32))
    return _GR[i % len(_GR)]

def _grade(img, cor_linha, passo=54, alpha=1.0):
    g = img.copy()
    for x in range(X0 % passo, W, passo): g[:, x:x + 1] = g[:, x:x + 1] * (1 - alpha) + np.array(cor_linha) * alpha
    for y in range(0, H, passo): g[y:y + 1, :] = g[y:y + 1, :] * (1 - alpha) + np.array(cor_linha) * alpha
    return g

def _fundo_np(modo):
    if modo in _bg_cache: return _bg_cache[modo]
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    if modo == "escuro":
        b = np.array(C["base"], np.float32); gl = np.array(C["brilho"], np.float32)
        g1 = np.exp(-(((xx - W * 0.42) / (W * 0.75)) ** 2 + ((yy - H * 0.30) / (H * 0.42)) ** 2) * 1.2)
        g2 = np.exp(-(((xx - W * 0.10) / (W * 0.45)) ** 2 + ((yy - H * 0.62) / (H * 0.30)) ** 2) * 1.6) * 0.45
        img = b + (g1 * 0.62 + g2)[..., None] * (gl - b)
        img = _grade(img, tuple(np.clip(np.array(C["brilho"]) * 0.55 + 30, 0, 255)), alpha=0.10)
        v = 1 - 0.55 * np.clip(((xx / W - .5) ** 2 * 1.2 + (yy / H - .45) ** 2) * 2.0, 0, 1)
        img = img * v[..., None]
    else:
        p = np.array(C["papel"], np.float32)
        img = np.repeat(np.repeat(p[None, None], H, 0), W, 1)
        img = _grade(img, tuple(p - 22), alpha=0.55)
        spot = np.exp(-(((xx - W * 0.55) / (W * 0.55)) ** 2 + ((yy - H * 0.42) / (H * 0.30)) ** 2) * 1.4)
        img = img + spot[..., None] * (np.array(C["acento"], np.float32) - p) * 0.06 + spot[..., None] * 8
        v = 1 - 0.30 * np.clip(((xx / W - .5) ** 2 * 1.6 + (yy / H - .5) ** 2) * 2.2, 0, 1)
        img = img * v[..., None]
    _bg_cache[modo] = img.astype(np.float32)
    return _bg_cache[modo]

def fundo(modo, fi):
    a = _fundo_np(modo) + _grao(fi)
    return Image.fromarray(np.clip(a, 0, 255).astype(np.uint8)).convert("RGBA")

# ---------------------------------------------------------------- cabeçalho + número-fantasma (fazem parte da "folha")
@lru_cache(64)
def _chrome_static(modo, rotulo, status, fantasma, prog):
    lay = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    tc, dc = txt_cor(modo), dim_cor(modo)
    y = 250
    # número-fantasma gigante (serif itálico) no canto de baixo
    if fantasma:
        f = font("serif", 400)
        col = (*mixc(C["base"] if modo == "escuro" else C["papel"], C["claro"] if modo == "escuro" else C["acento"], 0.16), 255)
        d.text((W - X0 + 40, 1720), fantasma, font=f, fill=col, anchor="rs")
    # rótulo "// troca 1"
    d.text((X0, y), "// " + rotulo, font=font("mono", 27), fill=(*mixc(tc, dc, 0.35), 255), anchor="lm")
    # status (direita)
    if status:
        sf = font("mono", 15); d.text((W - X0, y - 22), "S T A T U S", font=sf, fill=(*dc, 255), anchor="rm")
        texto_glifos(d, (W - X0, y + 6), status, font("mono", 28), (*destaque_cor(modo), 255), "rm")
    # linha com trecho de acento (progresso)
    ly = y + 32
    d.rectangle([X0, ly, W - X0, ly + 1], fill=(*dc, 90))
    d.rectangle([X0, ly - 1, X0 + int(XW * prog), ly + 2], fill=(*destaque_cor(modo), 255))
    return lay

def chrome(base, cena):
    lay = _chrome_static(cena["fundo"], cena.get("rotulo", ""), cena.get("status", ""), cena.get("fantasma", ""),
                         round(cena.get("prog", 0.62), 3))
    base.alpha_composite(lay)

# ---------------------------------------------------------------- fala: título que aparece palavra a palavra com a voz
def _norm(s): return re.sub(r"[^\wÀ-ÿ]", "", s).lower()

def fala(txt, t0, t1, palavras, **kw):
    """Cria o elemento de título sincronizado com a locução.
    txt: 'Primeiro, a *conta*: tudo que você paga' (* = palavra-chave em serif itálico colorida).
    Cada palavra entra no tempo em que é falada (palavras.json), com um leve adiantamento."""
    toks = partes(txt.replace("\n", " "))
    ws = [p for p in palavras if t0 - 0.12 <= p["s"] < (t1 if t1 else 1e9)]
    tempos, j, last = [], 0, t0
    for w, _ in toks:
        nw = _norm(w); achou = None
        for k in range(j, min(j + 4, len(ws))):
            nk = _norm(ws[k]["w"])
            if nk and nw and (nk[:3] == nw[:3] or nk.startswith(nw) or nw.startswith(nk)):
                achou = k; break
        if achou is not None:
            last = ws[achou]["s"]; j = achou + 1
        else:
            last = last + 0.16
        tempos.append(last)
    return dict(tipo="fala", txt=txt, t0=t0, t1=t1, tempos=tempos, **kw)

def _layout_fala(toks, size, maxw):
    sp = size * 0.27
    linhas, cur, cw = [], [], 0
    for i, (w, acc) in enumerate(toks):
        kind = "serif" if acc else "sans"; sz = size * (1.14 if acc else 1.0)
        ww = tw(w, kind, sz)
        if cur and cw + sp + ww > maxw:
            linhas.append(cur); cur, cw = [], 0
        cur.append((i, w, acc, kind, sz, ww)); cw += (sp if cw else 0) + ww
    if cur: linhas.append(cur)
    return linhas, sp

@tipo("fala")
def el_fala(base, t, e):
    if janela(t, e) is None: return
    modo = e["_modo"]; size = e.get("size", 74); y0 = e.get("y", 330); lh = size * 1.13
    toks = partes(e["txt"].replace("\n", " "))
    linhas, sp = _layout_fala(toks, size, e.get("larg", XW))
    asc_ref = font("sans", size).getmetrics()[0]
    adi = e.get("adianta", 0.10)
    for li, L in enumerate(linhas):
        x = X0
        for (i, w, acc, kind, sz, ww) in L:
            st = e["tempos"][i] - adi
            a = lin(t, st, st + 0.26)
            if a <= 0: x += ww + sp; continue
            ea = eout(a); al = clamp(a * 1.6); bq = (1 - ea) * 12; dy = (1 - ea) * 14
            if e.get("t1") is not None and t > e["t1"]:
                b = lin(t, e["t1"], e["t1"] + 0.22); al *= 1 - b; bq += b * 14; dy -= b * 10
            col = destaque_cor(modo) if acc else txt_cor(modo)
            bqq = int(round(bq / 2)) * 2
            spr = spr_palavra(w, kind, int(sz), col, bqq)
            pad = int(int(sz) * 0.35 + bqq * 3 + 6)
            asc = font(kind, int(sz)).getmetrics()[0]
            put_tl(base, spr, x - pad, y0 + li * lh + (asc_ref - asc) + dy - pad, alpha=al)
            x += ww + sp

def estrela(d, cx, cy, r, fill):
    pts = []
    for i in range(10):
        a = -math.pi / 2 + i * math.pi / 5; rr = r if i % 2 == 0 else r * 0.45
        pts.append((cx + rr * math.cos(a), cy + rr * math.sin(a)))
    d.polygon(pts, fill=fill)

def texto_glifos(d, xy, txt, f, fill, anchor="mm"):
    """Escreve texto trocando '★' por estrela desenhada e '✓' por check (fontes sem esses glifos)."""
    x, y = xy; size = f.size
    pecas = [p for p in re.split(r"([★✓])", txt) if p]
    larg = sum(size * 0.95 if p in "★✓" and len(p) == 1 else f.getlength(p) for p in pecas)
    if anchor[0] == "m": x -= larg / 2
    elif anchor[0] == "r": x -= larg
    for p in pecas:
        if p == "★": estrela(d, x + size * 0.42, y, size * 0.42, fill); x += size * 0.95
        elif p == "✓":
            d.line([(x + size * 0.12, y), (x + size * 0.38, y + size * 0.26), (x + size * 0.82, y - size * 0.3)], fill=fill, width=max(3, size // 9))
            x += size * 0.95
        else:
            d.text((x, y), p, font=f, fill=fill, anchor="l" + anchor[1]); x += f.getlength(p)

# ---------------------------------------------------------------- ícones (imagem real ou letra)
@lru_cache(128)
def _icone(spec, s):
    """spec: caminho de png/jpg (corta quadrado) ou 'letra|#rrggbb|#rrggbb' (letra, fundo, cor)."""
    if os.path.exists(spec):
        im = Image.open(spec).convert("RGBA"); q = min(im.size)
        im = im.crop(((im.width - q) // 2, (im.height - q) // 3, (im.width - q) // 2 + q, (im.height - q) // 3 + q))
        im = im.resize((s, s), Image.LANCZOS)
    else:
        parts = spec.split("|"); letra = parts[0]
        bg = tuple(int(parts[1][i:i + 2], 16) for i in (1, 3, 5)) if len(parts) > 1 else (30, 30, 36)
        fg = tuple(int(parts[2][i:i + 2], 16) for i in (1, 3, 5)) if len(parts) > 2 else (255, 255, 255)
        cv = Cv(s, s, pad=0); cv.rect(0, 0, s, s, r=s * 0.24, fill=(*bg, 255))
        cv.text(s / 2, s / 2 + s * 0.02, letra, "sans", s * (0.5 if len(letra) == 1 else 0.36), (*fg, 255), "mm")
        im = cv.done()
    m = mascara(s, s, int(s * 0.24)); a = np.minimum(np.asarray(m), np.asarray(im.getchannel("A")))
    im.putalpha(Image.fromarray(a)); return im

def icone(spec, s): return _icone(str(spec), int(s))

# ---------------------------------------------------------------- "#01 / 09" + cartão DE (ícone + nome + preço) que apaga
@lru_cache(64)
def _spr_item(nome, preco, icon, modo, apagado):
    s = 92; tc = txt_cor(modo)
    wn = tw(nome, "ui", 46); wp = tw(preco, "mono", 21) + 22 if preco else 0
    w = s + 26 + max(wn, wp) + 10; h = s + 8
    im = Image.new("RGBA", (int(w) + 8, int(h) + 8), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    ic = icone(icon, s)
    if apagado: ic = Image.blend(ic, Image.new("RGBA", ic.size, (*dim_cor(modo), 255)), 0.55); ic.putalpha(icone(icon, s).getchannel("A"))
    im.alpha_composite(ic, (0, 4))
    col = dim_cor(modo) if apagado else tc
    d.text((s + 26, 4), nome, font=font("ui", 46), fill=(*col, 255))
    if preco:
        py = 62
        chip_bg = (240, 242, 250) if modo == "escuro" else (18, 22, 60)
        chip_fg = (20, 26, 70) if modo == "escuro" else (245, 246, 252)
        if apagado: chip_bg, chip_fg = mixc(chip_bg, dim_cor(modo), 0.5), mixc(chip_fg, dim_cor(modo), 0.5)
        d.rounded_rectangle([s + 26, py, s + 26 + wp, py + 32], 5, fill=(*chip_bg, 255))
        d.text((s + 26 + 11, py + 16), preco, font=font("mono", 21), fill=(*chip_fg, 255), anchor="lm")
    return im

@tipo("item")
def el_item(base, t, e):
    j = janela(t, e, 0.32, 0.25)
    if j is None: return
    a, b = j; modo = e["_modo"]
    al = clamp(a * 1.8) * (1 - b)
    y = e.get("y", 600)
    if e.get("num"):
        dy = (1 - eout(lin(t, e["t0"] - 0.1, e["t0"] + 0.25))) * 16
        put_tl(base, spr_palavra(e["num"], "mono", 26, mixc(txt_cor(modo), dim_cor(modo), 0.3)), X0 - 15, y - 15 + dy, alpha=al)
    ap = e.get("apaga")
    apagado = ap is not None and t >= ap
    spr = _spr_item(e["nome"], e.get("preco", ""), str(e.get("icone", "?|#333333")), modo, apagado)
    bq = (1 - eout(a)) * 16
    if bq > 2: spr = spr.filter(ImageFilter.GaussianBlur(bq))
    k = lin(t, ap, ap + 0.3) if ap is not None else 0
    al2 = al * (1 - 0.35 * eio(k))
    put_tl(base, spr, X0, y + 60 + (1 - eout(a)) * 26 - 4, alpha=al2)

# ---------------------------------------------------------------- cartão PARA (branco): ícone, nome, descrição, rodapé, selo
@lru_cache(64)
def _spr_card(nome, desc, rodape, selo, icon, w, sombra_modo):
    h = 236; pad = 40
    im = Image.new("RGBA", (w + 2 * pad, h + 2 * pad), (0, 0, 0, 0))
    sh = Image.new("RGBA", im.size, (0, 0, 0, 0))
    ImageDraw.Draw(sh).rounded_rectangle([pad, pad + 14, pad + w, pad + h + 10], 26, fill=(0, 0, 0, 110 if sombra_modo == "escuro" else 55))
    im.alpha_composite(sh.filter(ImageFilter.GaussianBlur(20)))
    cv = Cv(w, h, pad=0)
    cv.rect(0, 0, w, h, r=24, fill=(252, 252, 250, 255))
    cv.rect(0, 0, w, h, r=24, ol=(255, 255, 255, 255), ow=2)
    card = cv.done()
    d = ImageDraw.Draw(card)
    s = 96
    card.alpha_composite(icone(icon, s), (30, 30))
    d.text((30 + s + 24, 34), nome, font=font("ui", 48), fill=(16, 18, 26, 255))
    d.text((30 + s + 26, 96), desc, font=font("ui", 24), fill=(120, 122, 130, 255))
    d.line([(30, h - 70), (w - 30, h - 70)], fill=(225, 226, 230, 255), width=2)
    yb = h - 36
    d.ellipse([30, yb - 12, 54, yb + 12], fill=(30, 32, 40, 255))
    d.text((42, yb), "›", font=font("mono", 22), fill=(255, 255, 255, 255), anchor="mm")
    d.text((66, yb), rodape, font=font("mono", 21), fill=(118, 120, 128, 255), anchor="lm")
    if selo:
        sw = tw(selo.replace("★", "  "), "mono", 24) + 30
        d.rounded_rectangle([w - 30 - sw, yb - 22, w - 30, yb + 22], 6, fill=(*C["acento"], 255))
        texto_glifos(d, (w - 30 - sw / 2, yb + 1), selo, font("mono", 24), (*C["sobre"], 255))
    im.alpha_composite(card, (pad, pad))
    return im

@tipo("troca")
def el_troca(base, t, e):
    j = janela(t, e, 0.34, 0.25)
    if j is None: return
    a, b = j
    spr = _spr_card(e["nome"], e.get("desc", ""), e.get("rodape", ""), e.get("selo", ""), str(e.get("icone", "?|#222222")),
                    int(e.get("larg", XW)), e["_modo"])
    ea = eout(a); dy = (1 - ea) * 120; bq = (1 - ea) * 70
    if bq > 3: spr = borrao_v(spr, bq)
    al = clamp(a * 1.6) * (1 - b)
    put_tl(base, spr, X0 - 40, e.get("y", 900) - 40 + dy - b * 30, alpha=al)

# ---------------------------------------------------------------- carimbo inclinado ("US$ 0", "GRÁTIS", "É UM CLONE")
@lru_cache(32)
def _spr_carimbo(txt, size):
    tw_ = tw(txt, "sans", size); w, h = tw_ + size * 0.75, size * 1.45
    cv = Cv(w + 16, h + 16, pad=20)
    cv.rect(0, 0, w + 16, h + 16, r=16, fill=(255, 255, 255, 255))
    cv.rect(7, 7, w + 2, h + 2, r=11, fill=(*C["acento"], 255))
    cv.text((w + 16) / 2, (h + 16) / 2 + size * 0.04, txt, "sans", size, (*C["sobre"], 255), "mm")
    im = cv.done()
    sh = Image.new("RGBA", im.size, (0, 0, 0, 0)); sh.putalpha(im.getchannel("A").point(lambda v: int(v * 0.45)))
    out = Image.new("RGBA", (im.width + 40, im.height + 40), (0, 0, 0, 0))
    out.alpha_composite(sh.filter(ImageFilter.GaussianBlur(10)), (20, 30)); out.alpha_composite(im, (20, 20))
    return out

@tipo("carimbo")
def el_carimbo(base, t, e):
    j = janela(t, e, 0.28, 0.2)
    if j is None: return
    a, b = j
    spr = _spr_carimbo(e["txt"], int(e.get("size", 62)))
    sc = mix(1.9, 1.0, eout(a)) * (1 + 0.06 * math.sin(math.pi * lin(t, e["t0"] + 0.28, e["t0"] + 0.5)))
    rot = e.get("rot", 7) + (1 - eout(a)) * 10
    put(base, spr, e.get("cx", 760), e.get("cy", 1150), sc=sc, rot=rot, alpha=clamp(a * 2.5) * (1 - b))

# ---------------------------------------------------------------- recibo: lista com valores, total contando e riscado
@lru_cache(16)
def _spr_recibo_base(cab_e, cab_d, w, h):
    cv = Cv(w, h, pad=0)
    cv.rect(0, 0, w, h, r=22, fill=(250, 250, 247, 255))
    im = cv.done(); d = ImageDraw.Draw(im)
    d.text((34, 40), " ".join(cab_e), font=font("mono", 19), fill=(130, 132, 140, 255), anchor="lm")
    d.text((w - 34, 40), " ".join(cab_d), font=font("mono", 19), fill=(130, 132, 140, 255), anchor="rm")
    for x in range(34, w - 34, 14): d.line([(x, 68), (x + 7, 68)], fill=(205, 206, 210, 255), width=2)
    return im

@tipo("recibo")
def el_recibo(base, t, e):
    j = janela(t, e, 0.34, 0.25)
    if j is None: return
    a, b = j
    linhas = e["linhas"]; w = int(e.get("larg", XW)); lh = 58
    h = 96 + lh * len(linhas) + 150
    im = _spr_recibo_base(e.get("cab_e", "SEU MÊS"), e.get("cab_d", "POR MÊS"), w, h).copy()
    d = ImageDraw.Draw(im)
    rt = e.get("risca")
    for i, L in enumerate(linhas):
        ti = e["t0"] + 0.15 + i * e.get("stagger", 0.09)
        ai = lin(t, ti, ti + 0.2)
        if ai <= 0: continue
        y = 104 + i * lh
        riscado = rt is not None and t >= rt + i * 0.06
        alpha = int(255 * ai)
        cn = (16, 18, 26) if not riscado else (170, 172, 178)
        im.alpha_composite(icone(L.get("icone", "?|#333333"), 34).copy(), (34, int(y)))
        d.text((84, y + 17), L["rot"], font=font("ui", 30), fill=(*cn, alpha), anchor="lm")
        d.text((w - 34, y + 17), L["val"], font=font("mono", 30), fill=(*cn, alpha), anchor="rm")
        if riscado:
            k = eout(lin(t, rt + i * 0.06, rt + i * 0.06 + 0.18))
            d.line([(30, y + 18), (30 + (w - 60) * k, y + 18)], fill=(*C["acento"], 255), width=4)
    yf = 104 + lh * len(linhas) + 14
    for x in range(34, w - 34, 14): d.line([(x, yf), (x + 7, yf)], fill=(205, 206, 210, 255), width=2)
    for k_, nota in enumerate(e.get("nota", "").split("\n")[:3]):
        d.text((34, yf + 30 + k_ * 26), nota, font=font("mono", 17), fill=(140, 142, 150, 255), anchor="lm")
    # total
    tt = e.get("t_total", e["t0"] + 0.15 + len(linhas) * e.get("stagger", 0.09))
    at = lin(t, tt, tt + 0.25)
    if at > 0:
        if rt is not None and t >= rt + len(linhas) * 0.06 + 0.1:
            txt = e.get("total_final", e["total"])
        else:
            txt = dx._num_fmt(eout(lin(t, tt, tt + e.get("conta", 0.8))), e["total"].replace("R$ ", "").replace("US$ ", "").replace(".", ""), 0)
            pre = "R$ " if e["total"].startswith("R$") else ("US$ " if e["total"].startswith("US$") else "")
            try: n = int(txt); txt = pre + f"{n:,}".replace(",", ".")
            except ValueError: txt = pre + txt
        f = font("mono", 54); bw = f.getlength(e["total"]) + 44
        bx, by = w - 30 - bw, yf + 22
        d.rounded_rectangle([bx, by, bx + bw, by + 84], 8, fill=(*C["acento"], int(255 * at)))
        d.text((bx + bw / 2, by + 43), txt, font=f, fill=(*C["sobre"], int(255 * at)), anchor="mm")
    sh = brilho_blob(w, h, (0, 0, 0), 120 if e["_modo"] == "escuro" else 60, 30)
    ea = eout(a); dy = (1 - ea) * 140
    spr = im if a >= 1 else borrao_v(im, (1 - ea) * 90)
    al = clamp(a * 1.6) * (1 - b)
    x, y = X0 + (XW - w) / 2, e.get("y", 560)
    put(base, sh, x + w / 2, y + h / 2 + 24 + dy, alpha=al)
    put_tl(base, spr, x, y + dy - b * 30, alpha=al)

# ---------------------------------------------------------------- onda de áudio "tocando agora"
@tipo("onda")
def el_onda(base, t, e):
    j = janela(t, e, 0.34, 0.25)
    if j is None: return
    a, b = j; modo = e["_modo"]
    w, h = int(e.get("larg", XW)), 320
    x, y = X0, e.get("y", 900) + (1 - eout(a)) * 90
    al = clamp(a * 1.6) * (1 - b)
    if modo == "escuro": vidro(base, x, y, w, h, r=30, alpha=al, escuro=0.75, tint=10, borda=60)
    else:
        put(base, brilho_blob(w, h, (0, 0, 0), 60, 30), x + w / 2, y + h / 2 + 20, alpha=al)
        lay = Cv(w, h, pad=0); lay.rect(0, 0, w, h, r=30, fill=(250, 250, 247, 255)); put_tl(base, lay.done(), x, y, alpha=al)
    tc = txt_cor(modo)
    lay = Image.new("RGBA", (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    # glifo de onda + título
    for k in range(5):
        hh = [10, 22, 14, 26, 12][k]
        d.rounded_rectangle([34 + k * 8, 46 - hh / 2, 38 + k * 8, 46 + hh / 2], 2, fill=(*C["claro" if modo == "escuro" else "acento"], 255))
    d.text((86, 46), " ".join(e.get("titulo", "TOCANDO AGORA")), font=font("mono", 20), fill=(*tc, 235), anchor="lm")
    n = 58; bw = (w - 68) / n; prog = lin(t, e["t0"] + 0.2, e.get("t1", e["t0"] + 3) + 0.2)
    rng = np.random.default_rng(5)
    base_h = rng.uniform(0.25, 1.0, n)
    for i in range(n):
        osc = 0.55 + 0.45 * math.sin(t * 9 + i * 0.7) * math.sin(t * 3.1 + i * 0.23)
        hh = 18 + 140 * base_h[i] * (0.6 + 0.4 * osc) * eout(lin(t, e["t0"] + i * 0.008, e["t0"] + 0.4 + i * 0.008))
        cx = 34 + i * bw + bw / 2
        played = i / n < prog
        col = (*(tc if played else (C["claro"] if modo == "escuro" else C["acento"])), 255)
        d.rounded_rectangle([cx - bw * 0.28, 170 - hh / 2, cx + bw * 0.28, 170 + hh / 2], 3, fill=col)
    secs = max(0.0, t - e["t0"])
    d.text((34, h - 40), f"0:{int(secs):02d}", font=font("mono", 22), fill=(*dim_cor(modo), 255), anchor="lm")
    d.text((w - 34, h - 40), e.get("rot", ""), font=font("mono", 22), fill=(*dim_cor(modo), 255), anchor="rm")
    put_tl(base, lay, x, y, alpha=al)

# ---------------------------------------------------------------- contador grande ("★ 351,5 mil")
@tipo("contador")
def el_contador(base, t, e):
    j = janela(t, e, 0.3, 0.25)
    if j is None: return
    a, b = j
    v = eout(lin(t, e["t0"], e["t0"] + e.get("conta", 0.9)))
    pre, suf = e.get("pre", ""), e.get("suf", "")
    num = dx._num_fmt(v, e["v"], e.get("de", 0))
    txt = pre + num + suf
    size = e.get("size", 96)
    f = font("mono", size); wfull = f.getlength(pre + e["v"] + suf) + 70; h = size * 1.45
    fim = v >= 0.999
    k = lin(t, e["t0"] + e.get("conta", 0.9), e["t0"] + e.get("conta", 0.9) + 0.2)
    bg = mixc((250, 250, 247), C["acento"], k); fg = mixc((16, 20, 50), C["sobre"], k)
    cv = Cv(wfull, h, pad=0); cv.rect(0, 0, wfull, h, r=14, fill=(*bg, 255)); im = cv.done()
    d = ImageDraw.Draw(im); texto_glifos(d, (wfull / 2, h / 2 + 2), txt, f, (*fg, 255))
    if not fim: im = borrao_v(im, 18 * (1 - v))
    cx, cy = e.get("cx", W / 2), e.get("y", 1200)
    if k > 0: put(base, brilho_blob(int(wfull), int(h), C["acento"], 110, 50), cx, cy, alpha=k * (1 - b))
    put(base, im, cx, cy, sc=mix(0.8, 1, eback(lin(t, e["t0"], e["t0"] + 0.35))) * (1 + 0.05 * math.sin(math.pi * k)),
        alpha=clamp(a * 2) * (1 - b))

# ---------------------------------------------------------------- grade de chips (ícone + texto)
@tipo("grade")
def el_grade(base, t, e):
    j = janela(t, e, 0.3, 0.25)
    if j is None: return
    a, b = j; modo = e["_modo"]
    itens = e["itens"]; cols = e.get("cols", 3); cw = XW / cols; ch = e.get("alt_linha", 84); s = e.get("icone_s", 52)
    for i, it in enumerate(itens):
        ti = e["t0"] + i * e.get("stagger", 0.07)
        ai = lin(t, ti, ti + 0.25)
        if ai <= 0: continue
        r, c = divmod(i, cols)
        x = X0 + c * cw; y = e.get("y", 560) + r * ch + (1 - eout(ai)) * 24
        al = clamp(ai * 2) * (1 - b) * (1 - 0.6 * lin(t, e.get("apaga", 1e9), e.get("apaga", 1e9) + 0.3))
        put_tl(base, icone(it[0], s), x, y, alpha=al)
        sz = e.get("size", 24); kind = "mono" if e.get("mono", True) else "ui"
        if "★" in it[1] or "✓" in it[1]:
            lay = Image.new("RGBA", (int(cw), int(s)), (0, 0, 0, 0))
            texto_glifos(ImageDraw.Draw(lay), (0, s / 2), it[1], font(kind, sz), (*txt_cor(modo), 255), "lm")
            put_tl(base, lay, x + s + 14, y, alpha=al)
        else:
            dx.texto_tl(base, it[1], kind, sz, txt_cor(modo), x + s + 14, y + s / 2 - sz * 0.62, al)

# ---------------------------------------------------------------- busca digitando
@tipo("busca")
def el_busca(base, t, e):
    j = janela(t, e, 0.3, 0.25)
    if j is None: return
    a, b = j; al = clamp(a * 2) * (1 - b)
    w, h = XW, 98; x, y = X0, e.get("y", 600) + (1 - eout(a)) * 30
    put(base, brilho_blob(w, h, (0, 0, 0), 90, 26), x + w / 2, y + h / 2 + 16, alpha=al)
    cv = Cv(w, h, pad=0); cv.rect(0, 0, w, h, r=h / 2, fill=(252, 252, 250, 255)); im = cv.done(); d = ImageDraw.Draw(im)
    d.ellipse([34, h / 2 - 15, 64, h / 2 + 15], outline=(30, 32, 40, 255), width=4)
    d.line([(58, h / 2 + 10), (70, h / 2 + 22)], fill=(30, 32, 40, 255), width=5)
    txt = e["txt"]; td = e.get("t_digita", e["t0"] + 0.3); n = int(len(txt) * lin(t, td, td + 0.055 * len(txt)))
    d.text((92, h / 2), txt[:n], font=font("mono", 34), fill=(22, 24, 34, 255), anchor="lm")
    if int(t * 2.6) % 2 == 0:
        cx_ = 92 + font("mono", 34).getlength(txt[:n]) + 4
        d.rectangle([cx_, h / 2 - 22, cx_ + 3, h / 2 + 22], fill=(*C["acento"], 255))
    put_tl(base, im, x, y, alpha=al)

# ---------------------------------------------------------------- comentário + seguir
@tipo("comentar")
def el_comentar(base, t, e):
    j = janela(t, e, 0.3, 0.25)
    if j is None: return
    a, b = j; modo = e["_modo"]; al = clamp(a * 2) * (1 - b)
    y = e.get("y", 600) + (1 - eout(a)) * 30
    dx.texto_tl(base, e.get("rot", "Comentários"), "ui", 26, txt_cor(modo), X0, y, al)
    w, h = XW, 92; yy = y + 50
    cv = Cv(w, h, pad=0); cv.rect(0, 0, w, h, r=20, fill=(252, 252, 250, 255)); im = cv.done(); d = ImageDraw.Draw(im)
    av = dx._avatar(e.get("avatar"), 24, e.get("iniciais", "LK")); im.alpha_composite(av, (26, h // 2 - 24))
    pal = e["palavra"]; td = e.get("t_digita", e["t0"] + 0.3); n = int(len(pal) * lin(t, td, td + 0.09 * len(pal)))
    d.text((94, h / 2), pal[:n] + ("|" if n < len(pal) and int(t * 2.6) % 2 == 0 else ""), font=font("uib", 36), fill=(18, 20, 28, 255), anchor="lm")
    env = t >= td + 0.09 * len(pal) + 0.2
    bw = 130; bx = w - 26 - bw
    d.rounded_rectangle([bx, h / 2 - 25, bx + bw, h / 2 + 25], 25, fill=(*(C["acento"] if env else (200, 202, 210)), 255))
    d.text((bx + bw / 2, h / 2 + 1), "Publicar", font=font("ui", 22), fill=(*(C["sobre"] if env else (255, 255, 255)), 255), anchor="mm")
    put_tl(base, im, X0, yy, alpha=al)

@tipo("seguir")
def el_seguir(base, t, e):
    j = janela(t, e, 0.3, 0.25)
    if j is None: return
    a, b = j; modo = e["_modo"]; al = clamp(a * 2) * (1 - b)
    w, h = XW, 110; x, y = X0, e.get("y", 800) + (1 - eout(a)) * 30
    if modo == "escuro": vidro(base, x, y, w, h, r=22, alpha=al, escuro=0.7, tint=14, borda=50)
    lay = Image.new("RGBA", (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    lay.alpha_composite(dx._avatar(e.get("avatar"), 30, e.get("iniciais", "LK")), (26, h // 2 - 30))
    d.text((100, h / 2 - 14), e.get("nome", "Lucas Sena"), font=font("ui", 30), fill=(*txt_cor(modo), 255), anchor="lm")
    d.text((100, h / 2 + 22), e.get("sub", ""), font=font("ui", 20), fill=(*dim_cor(modo), 255), anchor="lm")
    tok = e.get("t_ok", e["t0"] + 0.7); ok = t >= tok
    bw = 210; bx = w - 26 - bw
    d.rounded_rectangle([bx, h / 2 - 28, bx + bw, h / 2 + 28], 10, fill=(*((250, 250, 247) if not ok else C["acento"]), 255))
    texto_glifos(d, (bx + bw / 2, h / 2 + 1), "Seguindo ✓" if ok else "Seguir", font("ui", 26),
                 (*((20, 22, 30) if not ok else C["sobre"]), 255))
    put_tl(base, lay, x, y, alpha=al)
    # cursor indo até o botão
    k = eio(lin(t, e["t0"] + 0.1, tok)); cxp = mix(x + w * 0.45, x + bx + bw * 0.6, k); cyp = mix(y + h * 1.6, y + h / 2 + 8, k)
    if t < tok + 0.6:
        cur = Image.new("RGBA", (40, 50), (0, 0, 0, 0)); dc = ImageDraw.Draw(cur)
        dc.polygon([(4, 2), (4, 38), (14, 28), (22, 44), (28, 41), (20, 26), (34, 26)], fill=(255, 255, 255, 255), outline=(10, 10, 10, 255))
        put_tl(base, cur, cxp, cyp, alpha=al * (1 - lin(t, tok + 0.3, tok + 0.6)))

# ---------------------------------------------------------------- DM com checklist
@tipo("dm")
def el_dm(base, t, e):
    j = janela(t, e, 0.34, 0.25)
    if j is None: return
    a, b = j; al = clamp(a * 2) * (1 - b)
    itens = e["itens"]; w = XW; lh = 60; h = 120 + lh * len(itens) + 30
    x, y = X0, e.get("y", 600) + (1 - eout(a)) * 60
    put(base, brilho_blob(w, h, (0, 0, 0), 100, 30), x + w / 2, y + h / 2 + 24, alpha=al)
    cv = Cv(w, h, pad=0); cv.rect(0, 0, w, h, r=26, fill=(252, 252, 250, 255)); im = cv.done(); d = ImageDraw.Draw(im)
    im.alpha_composite(dx._avatar(e.get("avatar"), 26, e.get("iniciais", "LK")), (30, 30))
    d.text((96, 56), e.get("de", "Lucas Sena") + " · mensagem", font=font("ui", 28), fill=(16, 18, 26, 255), anchor="lm")
    tag = e.get("tag", "GUIA"); tgw = font("mono", 19).getlength(tag) + 24
    d.rounded_rectangle([w - 30 - tgw, 38, w - 30, 74], 4, fill=(*C["acento"], 255))
    d.text((w - 30 - tgw / 2, 57), tag, font=font("mono", 19), fill=(*C["sobre"], 255), anchor="mm")
    for i, it in enumerate(itens):
        ti = e["t0"] + 0.35 + i * e.get("stagger", 0.22)
        ai = lin(t, ti, ti + 0.2)
        if ai <= 0: continue
        yy = 126 + i * lh; A = int(255 * ai)
        d.text((34, yy), f"{i + 1}.", font=font("uib", 30), fill=(*C["tinta"], A), anchor="lm")
        nm = it[0] if isinstance(it, (list, tuple)) else it
        sub = it[1] if isinstance(it, (list, tuple)) and len(it) > 1 else ""
        d.text((84, yy), nm, font=font("ui", 32), fill=(18, 20, 28, A), anchor="lm")
        if sub: d.text((84 + font("ui", 32).getlength(nm) + 16, yy + 3), sub, font=font("ui", 21), fill=(150, 152, 160, A), anchor="lm")
        ck = lin(t, ti + 0.12, ti + 0.3)
        if ck > 0:
            r = 18 * mix(0.4, 1, eback(ck))
            d.ellipse([w - 52 - r, yy - r, w - 52 + r, yy + r], fill=(*C["acento"], 255))
            d.line([(w - 60, yy), (w - 54, yy + 7), (w - 43, yy - 7)], fill=(*C["sobre"], 255), width=4)
    put_tl(base, im, x, y, alpha=al)

# ---------------------------------------------------------------- vídeo em cartão branco (material real)
_clip_dx = TIPOS["clip"]
@tipo("clip")
def el_clip(base, t, e):
    e.setdefault("aura", False)
    _clip_dx(base, t, e)

# ================================================================= cenas + quadro
def prepara(R):
    """Marca em cada elemento a cena (índice) e o modo de fundo."""
    cenas = sorted(R.CENAS, key=lambda c: c["t0"])
    R.CENAS = cenas
    for e in R.EL:
        ci = e.get("cena")
        if ci is None:
            ci = 0
            for i, c in enumerate(cenas):
                if e["t0"] >= c["t0"] - 1e-6: ci = i
        e["_cena"] = ci; e["_modo"] = cenas[ci]["fundo"]
    R._prep = True

TRANS = 0.42
def _desenha_cena(base, t, R, ci):
    for e in R.EL:
        if e["_cena"] != ci: continue
        fn = TIPOS.get(e["tipo"])
        if fn: fn(base, t, e)

@lru_cache(4)
def _mask_folha(r=46):
    m = Image.new("L", (W * K, H * K), 0)
    ImageDraw.Draw(m).rounded_rectangle([0, 0, W * K - 1, (H + 200) * K], r * K, fill=255)
    return m.resize((W, H), Image.LANCZOS)

def quadro(t, fi, R):
    if not getattr(R, "_prep", False): prepara(R)
    cenas = R.CENAS
    ci = 0
    for i, c in enumerate(cenas):
        if t >= c["t0"]: ci = i
    c = cenas[ci]
    p = lin(t, c["t0"], c["t0"] + c.get("trans", TRANS)) if ci > 0 else 1.0
    if p >= 1:
        base = fundo(c["fundo"], fi); chrome(base, c); _desenha_cena(base, t, R, ci)
    else:
        pc = cenas[ci - 1]
        base = fundo(pc["fundo"], fi); chrome(base, pc); _desenha_cena(base, t, R, ci - 1)
        ep = eout(p)
        if p > 0.02: base = base.filter(ImageFilter.GaussianBlur(10 * ep))
        base.alpha_composite(Image.new("RGBA", (W, H), (0, 0, 0, int(110 * ep))))
        folha = fundo(c["fundo"], fi); chrome(folha, c); _desenha_cena(folha, t, R, ci)
        folha.putalpha(_mask_folha())
        yoff = int(H * (1 - ep))
        sh = Image.new("RGBA", (W, 160), (0, 0, 0, 0))
        ImageDraw.Draw(sh).rectangle([0, 80, W, 160], fill=(0, 0, 0, 150))
        sh = sh.filter(ImageFilter.GaussianBlur(28))
        if 0 < yoff < H: put_tl(base, sh, 0, yoff - 110)
        vel = (1 - p) * 140
        if vel > 6:
            folha = borrao_v(folha, vel)
            yoff -= int(vel)          # borrao_v acrescenta 'vel' px em cima e embaixo
        put_tl(base, folha, 0, yoff)
    for e in R.EL:
        if e["tipo"] == "flash": TIPOS["flash"](base, t, e)
    img = base.convert("RGB")
    return dx.tremor(img, t, R.EL)

set_paleta("cobalto")
