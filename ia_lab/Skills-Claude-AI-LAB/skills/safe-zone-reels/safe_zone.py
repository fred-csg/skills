# Safe zone 9:16 (1080x1920) para Reels / TikTok / Shorts — v2, medida em prints reais do Instagram (out/2026).
# Uso:
#   python safe_zone.py overlay  [saida.png]                       -> overlay transparente pra conferência
#   python safe_zone.py checar   video.mp4 [--tempos 1,5,9] [--saida folha.jpg]   -> folha de quadros com a guia por cima
#   python safe_zone.py caixa    x0 y0 x1 y1                         -> diz se a caixa está na área segura
# Importável: from safe_zone import TOPO, BASE, LAT, BOT_X, BOT_Y, problemas, overlay
import os, sys, shutil, subprocess, tempfile, json

W, H = 1080, 1920
TOPO = 240            # barra "Reels | Amigos" + status do celular
BASE = 1500           # daqui pra baixo: @perfil, legenda do post, música, barra do app
LAT = 95              # corte lateral em celulares altos
BOT_X, BOT_Y = 870, 800   # coluna de botões (curtir/comentar/compartilhar/salvar) à direita, de y 800 até a BASE
# Faixas recomendadas (não obrigatórias) — usar a área toda, sem encolher o vídeo:
SLOTS = {
    "titulo":  (LAT, 250, W - LAT, 430),      # título/lettering do topo
    "heroi":   (LAT, 430, BOT_X, 1150),       # o que está sendo explicado
    "legenda": (LAT, 1150, BOT_X, 1470),      # legenda palavra a palavra (centro x ≈ 482)
}
CENTRO_X = (LAT + BOT_X) // 2   # 482: centro horizontal seguro na metade de baixo
CAPA_GRADE = (0, 240, W, 1680)  # recorte 3:4 da grade do perfil (capa): título da capa dentro disso


def problemas(x0, y0, x1, y1):
    """Lista do que a caixa (em px 1080x1920) invade. Vazia = ok."""
    p = []
    if y0 < TOPO: p.append(f"topo: começa em y {y0} (mín. {TOPO})")
    if y1 > BASE: p.append(f"base: termina em y {y1} (máx. {BASE})")
    if x0 < LAT: p.append(f"lateral esquerda: x {x0} (mín. {LAT})")
    if x1 > W - LAT: p.append(f"lateral direita: x {x1} (máx. {W - LAT})")
    if x1 > BOT_X and y1 > BOT_Y: p.append(f"botões: caixa entra em x>{BOT_X} abaixo de y {BOT_Y}")
    return p


def _fonte(s):
    from PIL import ImageFont
    for f in ("segoeuib.ttf", "arialbd.ttf", "Arial Bold.ttf", "DejaVuSans-Bold.ttf", "Helvetica.ttc"):
        for d in ("", r"C:\Windows\Fonts", "/Library/Fonts", "/System/Library/Fonts", "/usr/share/fonts/truetype/dejavu"):
            try: return ImageFont.truetype(os.path.join(d, f) if d else f, s)
            except Exception: pass
    return ImageFont.load_default()


def overlay():
    from PIL import Image, ImageDraw
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    red = (229, 72, 77, 115); amb = (242, 179, 61, 95)
    d.rectangle([0, 0, W, TOPO], fill=red); d.rectangle([0, BASE, W, H], fill=red)
    d.rectangle([0, TOPO, LAT, BASE], fill=amb); d.rectangle([W - LAT, TOPO, W, BOT_Y], fill=amb)
    d.rectangle([BOT_X, BOT_Y, W, BASE], fill=red)
    d.line([(LAT, TOPO), (W - LAT, TOPO), (W - LAT, BOT_Y), (BOT_X, BOT_Y), (BOT_X, BASE), (LAT, BASE), (LAT, TOPO)],
           fill=(37, 165, 95, 255), width=6)
    k = dict(fill=(255, 255, 255, 255), anchor="mm", stroke_width=3, stroke_fill=(0, 0, 0, 255))
    d.text((W / 2, TOPO / 2 + 20), f"TOPO {TOPO} px — barra do app", font=_fonte(32), **k)
    d.text((W / 2, BASE + 110), f"BASE a partir de y {BASE} — @perfil, legenda, barra", font=_fonte(32), **k)
    d.text((BOT_X + (W - BOT_X) / 2, (BOT_Y + BASE) / 2), "botões", font=_fonte(28), **k)
    return im


def _ffmpeg():
    try:
        import imageio_ffmpeg; return imageio_ffmpeg.get_ffmpeg_exe()
    except Exception:
        return shutil.which("ffmpeg") or "ffmpeg"


def _duracao(ff, video):
    r = subprocess.run([ff, "-i", video], capture_output=True, text=True, errors="ignore").stderr
    for ln in r.splitlines():
        if "Duration:" in ln:
            h, m, s = ln.split("Duration:")[1].split(",")[0].strip().split(":"); return int(h) * 3600 + int(m) * 60 + float(s)
    return 10.0


def checar(video, tempos=None, saida=None):
    """Folha de contato com a guia por cima. Conferir TODOS os planos, a legenda mais longa e as entradas/saídas."""
    from PIL import Image
    ff = _ffmpeg(); ov = overlay()
    if not tempos:
        dur = _duracao(ff, video); n = 8; tempos = [round(dur * (i + 0.5) / n, 2) for i in range(n)]
    tmp = tempfile.mkdtemp(); tiles = []
    for i, t in enumerate(tempos):
        p = os.path.join(tmp, f"q{i}.png")
        subprocess.run([ff, "-v", "error", "-y", "-ss", str(t), "-i", video, "-frames:v", "1", p], check=True)
        q = Image.open(p).convert("RGBA").resize((W, H)); q.alpha_composite(ov); tiles.append(q.convert("RGB").resize((360, 640)))
    cols = min(4, len(tiles)); rows = (len(tiles) + cols - 1) // cols
    sheet = Image.new("RGB", (360 * cols, 640 * rows), (18, 18, 20))
    for i, tl in enumerate(tiles): sheet.paste(tl, ((i % cols) * 360, (i // cols) * 640))
    saida = saida or os.path.splitext(video)[0] + "_safezone.jpg"
    sheet.save(saida, quality=88); shutil.rmtree(tmp, ignore_errors=True)
    return saida


if __name__ == "__main__":
    try: sys.stdout.reconfigure(encoding="utf-8")
    except Exception: pass
    a = sys.argv[1:]
    if not a or a[0] == "overlay":
        out = a[1] if len(a) > 1 else os.path.join(os.path.dirname(os.path.abspath(__file__)), "safe_zone_overlay_1080x1920.png")
        overlay().save(out); print(out)
    elif a[0] == "checar":
        tempos = saida = None
        if "--tempos" in a: tempos = [float(x) for x in a[a.index("--tempos") + 1].split(",")]
        if "--saida" in a: saida = a[a.index("--saida") + 1]
        print(checar(a[1], tempos, saida))
    elif a[0] == "caixa":
        p = problemas(*map(int, a[1:5])); print("ok" if not p else "\n".join(p))
    elif a[0] == "json":
        print(json.dumps(dict(canvas=[W, H], topo=TOPO, base=BASE, lateral=LAT, botoes=[BOT_X, BOT_Y], slots=SLOTS), ensure_ascii=False, indent=1))
