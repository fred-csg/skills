# Modelo de recorte BiRefNet-portrait (licença MIT, ~973 MB).
# Procura nesta ordem: pasta "modelos" da própria skill -> ~/.rembg (onde o rembg guarda).
# Se não achar, baixar() busca na fonte oficial (releases do rembg no GitHub) e confere o MD5.
import os, sys, hashlib, urllib.request

SKILL = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
NOME = "birefnet-portrait.onnx"
URL = "https://github.com/danielgatis/rembg/releases/download/v0.0.0/BiRefNet-portrait-epoch_150.onnx"
TAMANHO = 972666916
MD5 = "c3a64a6abf20250d090cd055f12a3b67"
LOCAIS = [os.path.join(SKILL, "modelos", NOME),
          os.path.join(os.path.expanduser("~"), ".rembg", "models", "birefnet-portrait", NOME)]


def caminho_modelo():
    for p in LOCAIS:
        if os.path.exists(p) and os.path.getsize(p) == TAMANHO: return p
    return None


def baixar():
    p = caminho_modelo()
    if p: print("modelo já está em", p); return p
    dst = LOCAIS[1]; os.makedirs(os.path.dirname(dst), exist_ok=True)
    tmp = dst + ".parcial"
    print(f"baixando o modelo de recorte ({TAMANHO / 1e9:.2f} GB) de {URL}")
    def prog(b, bs, tot):
        if b % 400 == 0: print(f"  {min(100, b * bs * 100 // max(tot, 1))}%", flush=True)
    urllib.request.urlretrieve(URL, tmp, prog)
    h = hashlib.md5()
    with open(tmp, "rb") as f:
        for ch in iter(lambda: f.read(1 << 20), b""): h.update(ch)
    if h.hexdigest() != MD5:
        os.remove(tmp); raise SystemExit("o arquivo baixado veio corrompido (MD5 diferente). Tente de novo.")
    os.replace(tmp, dst); print("modelo pronto em", dst)
    return dst


if __name__ == "__main__":
    print(caminho_modelo() or "modelo não encontrado") if "--onde" in sys.argv else baixar()
