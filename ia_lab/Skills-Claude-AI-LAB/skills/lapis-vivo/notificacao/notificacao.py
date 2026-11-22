# Notificação "Segue pra mais…" no topo do vídeo — padrão OBRIGATÓRIO em todos os vídeos das skills.
# Um card escuro estilo notificação do iPhone (foto de perfil redonda, @ em negrito, frase em cinza e sino amarelo)
# DESCE do topo com mola, fica ~3,5 s e SOBE de volta (com uma puxadinha pra baixo antes de sair).
# A configuração fica em ~/.claude/notificacao.json e vale pra todas as próximas produções.
# Uso:
#   python notificacao.py status
#   python notificacao.py configurar --nome "seuperfil" --foto foto.jpg --texto "Segue pra ver mais vídeos de IA"
#                                    [--inicio 3] [--dura 3.5] [--verificado] [--som-entrada pop.wav] [--som-saida swish.wav]
#                                    [--som-db -14] [--nenhuma]
#   python notificacao.py aplicar entrada.mp4 saida.mp4 [--inicio 3] [--texto "..."]   -> aplica (áudio mantido)
#   python notificacao.py amostra [saida.png]                                           -> quadro de exemplo
#   python notificacao.py card [saida.png]                                              -> só o card (PNG transparente)
# Ordem no fim do pipeline: notificação → marca d'água → versão _celular.
import os, re, sys, json, math, shutil, subprocess, tempfile

CFG = os.path.join(os.path.expanduser("~"), ".claude", "notificacao.json")
W, H = 1080, 1920
TOPO = 160                 # igual à referência (notificação do iPhone): card começa em y 160 de 1920
CARD_W, CARD_H, RAIO = 800, 110, 30
PADRAO = {"ativo": False, "nome": "", "texto": "Segue pra ver mais vídeos de IA", "foto": "", "verificado": False,
          "inicio_s": 3.0, "dura_s": 3.5, "som_entrada": "", "som_saida": "", "som_db": -14}
SS = 3                     # supersampling do desenho


def ler():
    try:
        c = dict(PADRAO); c.update(json.load(open(CFG, encoding="utf-8"))); return c
    except Exception:
        return None        # None = ainda não configurado -> a skill PERGUNTA ao usuário


def salvar(c):
    os.makedirs(os.path.dirname(CFG), exist_ok=True)
    json.dump(c, open(CFG, "w", encoding="utf-8"), ensure_ascii=False, indent=1)


def _fonte(s, peso="sb"):
    from PIL import ImageFont
    nomes = {"sb": ("seguisb.ttf", "SF-Pro-Text-Semibold.otf", "Inter-SemiBold.ttf", "arialbd.ttf", "DejaVuSans-Bold.ttf"),
             "rg": ("segoeui.ttf", "SF-Pro-Text-Regular.otf", "Inter-Regular.ttf", "arial.ttf", "DejaVuSans.ttf")}[peso]
    for f in nomes:
        for d in ("", r"C:\Windows\Fonts", "/Library/Fonts", "/System/Library/Fonts", "/usr/share/fonts/truetype/dejavu"):
            try: return ImageFont.truetype(os.path.join(d, f) if d else f, s)
            except Exception: pass
    return ImageFont.load_default()


def _sino(d, cx, cy, s, cor):
    """Sino amarelo desenhado (s = altura em px)."""
    w = s * 0.86
    topo, base = cy - s * 0.42, cy + s * 0.26
    d.ellipse([cx - w * 0.30, topo, cx + w * 0.30, topo + w * 0.62], fill=cor)                     # cúpula
    d.polygon([(cx - w * 0.30, topo + w * 0.30), (cx + w * 0.30, topo + w * 0.30),
               (cx + w * 0.40, base - s * 0.06), (cx - w * 0.40, base - s * 0.06)], fill=cor)      # corpo
    d.rounded_rectangle([cx - w * 0.50, base - s * 0.12, cx + w * 0.50, base], radius=s * 0.06, fill=cor)  # aba
    r = s * 0.10; d.ellipse([cx - r, base + s * 0.04, cx + r, base + s * 0.04 + 2 * r], fill=cor)  # badalo
    r2 = s * 0.06; d.ellipse([cx - r2, topo - r2 * 1.2, cx + r2, topo + r2 * 0.8], fill=cor)        # pino


def _selo(d, cx, cy, r):
    """Selo de verificado azul."""
    pts = []
    for i in range(24):
        a = math.pi * 2 * i / 24; rr = r if i % 2 == 0 else r * 0.84
        pts.append((cx + rr * math.cos(a), cy + rr * math.sin(a)))
    d.polygon(pts, fill=(0, 149, 246))
    k = r * 0.42
    d.line([(cx - k, cy + k * 0.05), (cx - k * 0.25, cy + k * 0.75), (cx + k * 1.05, cy - k * 0.7)], fill=(255, 255, 255), width=max(2, int(r * 0.28)), joint="curve")


def card_png(c, texto=None):
    """PNG RGBA do card (com sombra suave em volta), em 1080 de largura."""
    from PIL import Image, ImageDraw, ImageFilter, ImageOps
    texto = texto or c.get("texto") or PADRAO["texto"]
    M = 40                                                     # margem pra sombra
    cw, ch = CARD_W * SS, CARD_H * SS
    im = Image.new("RGBA", (cw, ch), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle([0, 0, cw - 1, ch - 1], radius=RAIO * SS, fill=(30, 30, 32, 246), outline=(64, 64, 68, 255), width=int(1.6 * SS))
    # foto redonda
    av = 72 * SS; ax, ay = 19 * SS, (ch - av) // 2
    if c.get("foto") and os.path.isfile(c["foto"]):
        f = ImageOps.fit(Image.open(c["foto"]).convert("RGB"), (av, av), Image.LANCZOS, centering=(0.5, 0.42))
    else:
        f = Image.new("RGB", (av, av), (255, 204, 0)); fd = ImageDraw.Draw(f)
        ini = (c.get("nome") or "?").lstrip("@")[:1].upper()
        fd.text((av / 2, av / 2), ini, font=_fonte(int(av * 0.5)), fill=(20, 20, 20), anchor="mm")
    mask = Image.new("L", (av, av), 0); ImageDraw.Draw(mask).ellipse([0, 0, av - 1, av - 1], fill=255)
    im.paste(f, (ax, ay), mask)
    # textos
    tx = ax + av + 22 * SS
    nome = (c.get("nome") or "seuperfil").lstrip("@")
    fn, ft = _fonte(28 * SS, "sb"), _fonte(25 * SS, "rg")
    lim = cw - tx - 92 * SS
    while ft.getlength(texto) > lim and ft.size > 18 * SS: ft = _fonte(ft.size - SS, "rg")
    d.text((tx, ch * 0.36), nome, font=fn, fill=(245, 245, 247), anchor="lm")
    if c.get("verificado"):
        _selo(d, tx + fn.getlength(nome) + 19 * SS, ch * 0.36, 12 * SS)
    d.text((tx, ch * 0.68), texto, font=ft, fill=(168, 168, 174), anchor="lm")
    _sino(d, cw - 52 * SS, ch * 0.47, 46 * SS, (255, 204, 10))
    im = im.resize((CARD_W, CARD_H), Image.LANCZOS)
    # sombra (pra ler em cima de vídeo claro)
    out = Image.new("RGBA", (CARD_W + 2 * M, CARD_H + 2 * M), (0, 0, 0, 0))
    sh = Image.new("L", out.size, 0); ImageDraw.Draw(sh).rounded_rectangle([M, M + 8, M + CARD_W, M + CARD_H + 8], radius=RAIO, fill=110)
    sombra = Image.new("RGBA", out.size, (0, 0, 0, 0)); sombra.putalpha(sh.filter(ImageFilter.GaussianBlur(16)))
    out.alpha_composite(sombra); out.alpha_composite(im, (M, M))
    return out, M


def _ffmpeg():
    try:
        import imageio_ffmpeg; return imageio_ffmpeg.get_ffmpeg_exe()
    except Exception:
        return shutil.which("ffmpeg") or "ffmpeg"


def _info(ff, v):
    r = subprocess.run([ff, "-i", v], capture_output=True, text=True, errors="ignore").stderr
    m = re.search(r"Video:.*?(\d{3,5})x(\d{3,5})", r)
    dm = re.search(r"Duration: (\d+):(\d+):([\d.]+)", r)
    dur = int(dm.group(1)) * 3600 + int(dm.group(2)) * 60 + float(dm.group(3)) if dm else 0
    return (int(m.group(1)), int(m.group(2))) if m else (W, H), dur, ("Audio:" in r)


def y_expr(t0, dura, y_rest, y_fora):
    """Expressão ffmpeg do y do card: mola na entrada (0,55 s), parado, puxadinha + saída acelerada (0,42 s)."""
    A = y_fora - y_rest                                       # negativo (fora = acima)
    t1 = t0 + dura
    entra = f"{y_rest}+({A})*exp(-11*(t-{t0}))*cos(12*(t-{t0}))"
    puxa = f"{y_rest}+10*sin(PI*(t-{t1})/0.24)"               # desce 10 px em 0,12 s
    sai = f"{y_rest}+({A})*pow((t-{t1}-0.12)/0.30\\,2.4)"
    return (f"if(lt(t\\,{t0 + 0.6:.3f})\\,{entra}\\,"
            f"if(lt(t\\,{t1:.3f})\\,{y_rest}\\,"
            f"if(lt(t\\,{t1 + 0.12:.3f})\\,{puxa}\\,{sai})))")


def aplicar(entrada, saida, c=None, inicio=None, texto=None):
    c = c or ler()
    if not c or not c.get("ativo"):
        if os.path.abspath(entrada) != os.path.abspath(saida): shutil.copy2(entrada, saida)
        return "sem notificação (desativada)"
    ff = _ffmpeg(); (vw, vh), dur, tem_audio = _info(ff, entrada)
    t0 = float(inicio if inicio is not None else c.get("inicio_s", 3.0)); dura = float(c.get("dura_s", 3.5))
    if dur and t0 + dura + 0.6 > dur: t0 = max(0.3, dur - dura - 0.8)
    k = vw / W
    png, M = card_png(c, texto)
    if k != 1: png = png.resize((max(1, int(png.width * k)), max(1, int(png.height * k)))); M = int(M * k)
    tmp = tempfile.mkdtemp(); p = os.path.join(tmp, "notif.png"); png.save(p)
    x = (vw - png.width) // 2
    y_rest = int(TOPO * k) - M
    y_fora = -png.height - 10
    ye = y_expr(t0, dura, y_rest, y_fora)
    fil = (f"[0:v][1:v]overlay=x={x}:y='{ye}':eval=frame:enable='between(t\\,{t0:.3f}\\,{t0 + dura + 0.45:.3f})',format=yuv420p[v]")
    ins = [ff, "-v", "error", "-y", "-i", entrada, "-loop", "1", "-i", p]
    sons = [(c.get("som_entrada"), t0 + 0.02), (c.get("som_saida"), t0 + dura + 0.08)]
    sons = [(s, t) for s, t in sons if s and os.path.isfile(s)]
    amap = ["-map", "0:a?", "-c:a", "copy"]
    if sons:
        g = float(c.get("som_db", -14)); partes = []; rot = []
        for i, (s, t) in enumerate(sons):
            ins += ["-i", s]; ms = int(t * 1000)
            partes.append(f"[{i + 2}:a]aformat=sample_rates=48000:channel_layouts=stereo,volume={g}dB,adelay={ms}|{ms}[s{i}]"); rot.append(f"[s{i}]")
        if tem_audio:
            partes.append(f"[0:a]aformat=sample_rates=48000:channel_layouts=stereo[base]")
            mix = f"[base]{''.join(rot)}amix=inputs={len(rot) + 1}:normalize=0:duration=first[a]"
        else:
            mix = f"{''.join(rot)}amix=inputs={len(rot)}:normalize=0,apad[a]"
        fil += ";" + ";".join(partes) + ";" + mix
        amap = ["-map", "[a]", "-c:a", "aac", "-b:a", "256k"]
    destino = saida if os.path.abspath(entrada) != os.path.abspath(saida) else os.path.join(tmp, "out.mp4")
    subprocess.run(ins + ["-filter_complex", fil, "-map", "[v]"] + amap +
                   ["-c:v", "libx264", "-crf", "17", "-preset", "medium", "-shortest", "-movflags", "+faststart", destino], check=True)
    if destino != saida: shutil.move(destino, saida)
    shutil.rmtree(tmp, ignore_errors=True)
    return f"{saida}  (notificação de {t0:.1f}s a {t0 + dura:.1f}s)"


def amostra(saida):
    from PIL import Image, ImageDraw
    c = ler() or PADRAO
    im = Image.new("RGBA", (W, H), (70, 90, 120, 255)); d = ImageDraw.Draw(im)
    for y in range(0, H, 60): d.line([(0, y), (W, y)], fill=(85, 105, 140), width=2)
    png, M = card_png(c); im.alpha_composite(png, ((W - png.width) // 2, TOPO - M))
    im.convert("RGB").save(saida); return saida


def _arg(a, k, tipo=str):
    return tipo(a[a.index(k) + 1]) if k in a else None


if __name__ == "__main__":
    try: sys.stdout.reconfigure(encoding="utf-8")
    except Exception: pass
    a = sys.argv[1:]
    cmd = a[0] if a else "status"
    if cmd == "status":
        c = ler(); print("NAO CONFIGURADA - perguntar ao usuário" if c is None else json.dumps(c, ensure_ascii=False))
    elif cmd == "configurar":
        c = ler() or dict(PADRAO); c["ativo"] = "--nenhuma" not in a
        for k, ch, t in (("--nome", "nome", str), ("--texto", "texto", str), ("--inicio", "inicio_s", float), ("--dura", "dura_s", float),
                         ("--som-entrada", "som_entrada", str), ("--som-saida", "som_saida", str), ("--som-db", "som_db", float)):
            v = _arg(a, k, t)
            if v is not None: c[ch] = v.lstrip("@") if ch == "nome" else v
        if "--foto" in a:
            src = os.path.abspath(_arg(a, "--foto")); dst = os.path.join(os.path.dirname(CFG), "notificacao_foto" + os.path.splitext(src)[1].lower())
            shutil.copy2(src, dst); c["foto"] = dst
        if "--verificado" in a: c["verificado"] = True
        if "--sem-verificado" in a: c["verificado"] = False
        salvar(c); print(CFG); print(json.dumps(c, ensure_ascii=False))
    elif cmd == "aplicar":
        print(aplicar(a[1], a[2], inicio=_arg(a, "--inicio", float), texto=_arg(a, "--texto")))
    elif cmd == "amostra":
        print(amostra(a[1] if len(a) > 1 and not a[1].startswith("--") else "notificacao_amostra.png"))
    elif cmd == "card":
        c = ler() or PADRAO; out = a[1] if len(a) > 1 else "notificacao_card.png"; card_png(c)[0].save(out); print(out)
