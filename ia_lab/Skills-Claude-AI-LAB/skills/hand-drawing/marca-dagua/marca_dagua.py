# Marca d'água padrão pra todas as skills de vídeo (proteção contra repost sem crédito).
# A configuração fica em ~/.claude/marca-dagua.json e vale pra todas as próximas produções.
# Uso:
#   python marca_dagua.py status
#   python marca_dagua.py configurar --texto "@seuperfil"        (ou --logo caminho.png, ou --nenhuma)
#                                    [--opacidade 0.45] [--tamanho 34]
#   python marca_dagua.py aplicar entrada.mp4 saida.mp4           -> aplica no vídeo final (áudio copiado)
#   python marca_dagua.py amostra [saida.png]                    -> quadro de exemplo pra mostrar ao usuário
# A marca é sutil (branca, ~45% de opacidade, sombra leve) e troca de lado a cada 8 s (direita ↔ esquerda),
# sempre dentro da safe zone v2 (acima da coluna de botões e abaixo da barra do app), o que dificulta cortar fora.
import os, re, sys, json, shutil, subprocess, tempfile

CFG = os.path.join(os.path.expanduser("~"), ".claude", "marca-dagua.json")
W, H = 1080, 1920
LAT, BOT_Y = 95, 800
PADRAO = {"cor": "auto", "ativo": False, "tipo": "texto", "texto": "", "logo": "", "opacidade": 0.45, "tamanho": 34, "troca_s": 8}


def ler():
    try:
        c = dict(PADRAO); c.update(json.load(open(CFG, encoding="utf-8"))); return c
    except Exception:
        return None   # None = ainda não configurado -> a skill PERGUNTA ao usuário


def salvar(c):
    os.makedirs(os.path.dirname(CFG), exist_ok=True)
    json.dump(c, open(CFG, "w", encoding="utf-8"), ensure_ascii=False, indent=1)


def _fonte(s):
    from PIL import ImageFont
    for f in ("seguisb.ttf", "segoeuib.ttf", "arialbd.ttf", "Arial Bold.ttf", "DejaVuSans-Bold.ttf", "Helvetica.ttc"):
        for d in ("", r"C:\Windows\Fonts", "/Library/Fonts", "/System/Library/Fonts", "/usr/share/fonts/truetype/dejavu"):
            try: return ImageFont.truetype(os.path.join(d, f) if d else f, s)
            except Exception: pass
    return ImageFont.load_default()


def marca_png(c, escura=False):
    """PNG RGBA da marca (texto ou logo) já com opacidade e sombra suave.
    escura=True: texto grafite com halo claro (pra vídeos de fundo claro, onde o branco some)."""
    from PIL import Image, ImageDraw, ImageFilter
    cor, halo = ((30, 32, 40), (255, 255, 255)) if escura else ((255, 255, 255), (0, 0, 0))
    if c["tipo"] == "logo" and c.get("logo") and os.path.isfile(c["logo"]):
        lg = Image.open(c["logo"]).convert("RGBA"); h = int(c["tamanho"] * 1.7)
        lg = lg.resize((max(1, int(lg.width * h / lg.height)), h), Image.LANCZOS)
        pad = 12; im = Image.new("RGBA", (lg.width + 2 * pad, lg.height + 2 * pad), (0, 0, 0, 0)); im.alpha_composite(lg, (pad, pad))
    else:
        f = _fonte(int(c["tamanho"])); t = c.get("texto") or ""
        w = int(f.getlength(t)) + 30; h = int(c["tamanho"] * 1.6)
        im = Image.new("RGBA", (w, h), (0, 0, 0, 0)); ImageDraw.Draw(im).text((15, h / 2), t, font=f, fill=cor + (255,), anchor="lm")
    sombra = Image.new("RGBA", im.size, halo + (0,)); sombra.putalpha(im.getchannel("A").filter(ImageFilter.GaussianBlur(4)).point(lambda v: int(v * 0.55)))
    out = Image.new("RGBA", im.size, (0, 0, 0, 0)); out.alpha_composite(sombra, (0, 0)); out.alpha_composite(im)
    out.putalpha(out.getchannel("A").point(lambda v: int(v * float(c["opacidade"]))))
    return out


def posicoes(mw, mh, w=W, h=H):
    k = w / W
    y = int((BOT_Y - 20) * k) - mh                        # logo acima da coluna de botões
    return [(int((W - LAT) * k) - mw, y), (int(LAT * k), y)]   # direita, esquerda


def _ffmpeg():
    try:
        import imageio_ffmpeg; return imageio_ffmpeg.get_ffmpeg_exe()
    except Exception:
        return shutil.which("ffmpeg") or "ffmpeg"


def _tamanho(ff, v):
    r = subprocess.run([ff, "-i", v], capture_output=True, text=True, errors="ignore").stderr
    import re
    m = re.search(r"Video:.*?(\d{3,5})x(\d{3,5})", r)
    return (int(m.group(1)), int(m.group(2))) if m else (W, H)


def _fundo_claro(ff, entrada, vw, vh):
    """Brilho médio da faixa onde a marca fica (6 quadros espalhados). True = fundo claro -> usar marca escura."""
    from PIL import Image
    import io
    r =subprocess.run([ff, "-i", entrada], capture_output=True, text=True, errors="ignore").stderr
    m = re.search(r"Duration: (\d+):(\d+):([\d.]+)", r)
    dur = int(m.group(1)) * 3600 + int(m.group(2)) * 60 + float(m.group(3)) if m else 10
    k = vw / W; y0, y1 = int((BOT_Y - 120) * k), int((BOT_Y - 10) * k); vals = []
    for i in range(6):
        p = subprocess.run([ff, "-v", "error", "-ss", f"{dur * (i + .5) / 6:.2f}", "-i", entrada, "-frames:v", "1", "-f", "image2pipe", "-vcodec", "png", "-"],
                           capture_output=True).stdout
        if p:
            im = Image.open(io.BytesIO(p)).convert("L")
            for x0, x1 in ((int(LAT * k), int(LAT * k) + int(260 * k)), (int((W - LAT - 260) * k), int((W - LAT) * k))):
                reg = im.crop((x0, y0, x1, y1)); vals.append(sum(reg.tobytes()) / (reg.width * reg.height))
    return bool(vals) and sorted(vals)[len(vals) // 2] > 150


def aplicar(entrada, saida, c=None):
    c = c or ler()
    if not c or not c.get("ativo"):
        if os.path.abspath(entrada) != os.path.abspath(saida): shutil.copy2(entrada, saida)
        return "sem marca d'água (desativada)"
    ff = _ffmpeg(); vw, vh = _tamanho(ff, entrada)
    cor = c.get("cor", "auto")   # auto | clara | escura
    escura = _fundo_claro(ff, entrada, vw, vh) if cor == "auto" else (cor == "escura")
    m = marca_png(c, escura)
    if vw != W: m = m.resize((max(1, int(m.width * vw / W)), max(1, int(m.height * vw / W))))
    tmp = tempfile.mkdtemp(); png = os.path.join(tmp, "marca.png"); m.save(png)
    (x1, y1), (x2, y2) = posicoes(m.width, m.height, vw, vh); T = int(c.get("troca_s", 8))
    fil = (f"[0:v][1:v]overlay={x1}:{y1}:enable='lt(mod(t,{2 * T}),{T})'[a];"
           f"[a][1:v]overlay={x2}:{y2}:enable='gte(mod(t,{2 * T}),{T})',format=yuv420p[v]")
    destino = saida if os.path.abspath(entrada) != os.path.abspath(saida) else os.path.join(tmp, "out.mp4")
    subprocess.run([ff, "-v", "error", "-y", "-i", entrada, "-loop", "1", "-i", png, "-filter_complex", fil,
                    "-map", "[v]", "-map", "0:a?", "-c:v", "libx264", "-crf", "17", "-preset", "medium",
                    "-c:a", "copy", "-shortest", "-movflags", "+faststart", destino], check=True)
    if destino != saida: shutil.move(destino, saida)
    shutil.rmtree(tmp, ignore_errors=True)
    return saida


def amostra(saida):
    from PIL import Image, ImageDraw
    c = ler() or PADRAO
    im = Image.new("RGBA", (W, H), (70, 90, 120, 255)); d = ImageDraw.Draw(im)
    for y in range(0, H, 60): d.line([(0, y), (W, y)], fill=(85, 105, 140), width=2)
    m = marca_png(c); (x1, y1), (x2, y2) = posicoes(m.width, m.height)
    im.alpha_composite(m, (x1, y1)); im.alpha_composite(m.copy(), (x2, y2 + 0))
    im.convert("RGB").save(saida); return saida


if __name__ == "__main__":
    try: sys.stdout.reconfigure(encoding="utf-8")
    except Exception: pass
    a = sys.argv[1:]
    cmd = a[0] if a else "status"
    if cmd == "status":
        c = ler(); print("NAO CONFIGURADA - perguntar ao usuário" if c is None else json.dumps(c, ensure_ascii=False))
    elif cmd == "configurar":
        c = ler() or dict(PADRAO)
        if "--nenhuma" in a: c["ativo"] = False
        if "--texto" in a: c.update(ativo=True, tipo="texto", texto=a[a.index("--texto") + 1])
        if "--logo" in a: c.update(ativo=True, tipo="logo", logo=os.path.abspath(a[a.index("--logo") + 1]))
        if "--opacidade" in a: c["opacidade"] = float(a[a.index("--opacidade") + 1])
        if "--tamanho" in a: c["tamanho"] = int(a[a.index("--tamanho") + 1])
        if "--cor" in a: c["cor"] = a[a.index("--cor") + 1]   # auto | clara | escura
        salvar(c); print(CFG); print(json.dumps(c, ensure_ascii=False))
    elif cmd == "aplicar":
        print(aplicar(a[1], a[2]))
    elif cmd == "amostra":
        print(amostra(a[1] if len(a) > 1 else "marca_dagua_amostra.png"))
