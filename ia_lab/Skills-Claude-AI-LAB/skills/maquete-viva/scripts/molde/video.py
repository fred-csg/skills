# Utilidades de vídeo (Windows ou Mac).
#   python video.py preview <master.mp4>                       -> <master>_preview.mp4 (720p leve, pra celular)
#   python video.py lado <antes.mp4> <depois.mp4> <saida.mp4> [ROTULO_A] [ROTULO_B]  -> comparativo lado a lado
import sys, os, subprocess
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from ambiente import ffmpeg, achar_fonte
FF = ffmpeg()
cmd = sys.argv[1]
if cmd == "preview":
    src = sys.argv[2]; out = os.path.splitext(src)[0] + "_preview.mp4"
    subprocess.run([FF, "-v", "error", "-y", "-i", src, "-vf", "scale=720:1280", "-c:v", "libx264", "-crf", "25", "-preset", "fast",
                    "-c:a", "aac", "-b:a", "128k", out], check=True)
    print(out)
elif cmd == "lado":
    a, b, out = sys.argv[2:5]
    la = sys.argv[5] if len(sys.argv) > 5 else "ANTES"; lb = sys.argv[6] if len(sys.argv) > 6 else "DEPOIS"
    f = (achar_fonte("seguibl.ttf", "Poppins-Black.ttf", "ariblk.ttf", "Arial Black.ttf", "arialbd.ttf") or "").replace("\\", "/").replace(":", "\\:")
    dt = lambda t: f"drawtext=fontfile='{f}':text='{t}':x=(w-tw)/2:y=40:fontsize=54:fontcolor=white:borderw=6:bordercolor=black"
    fc = f"[0:v]scale=720:1280,{dt(la)}[a];[1:v]scale=720:1280,{dt(lb)}[b];[a][b]hstack=inputs=2[v]"
    subprocess.run([FF, "-v", "error", "-y", "-i", a, "-i", b, "-filter_complex", fc, "-map", "[v]", "-map", "1:a",
                    "-c:v", "libx264", "-crf", "22", "-preset", "fast", "-c:a", "aac", "-b:a", "160k", "-shortest", out], check=True)
    print(out)
