import sys, os, subprocess
src, outdir, ts = sys.argv[1], sys.argv[2], [float(x) for x in sys.argv[3].split(",")]
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.argv = ["r", src, "x"]
import roteiro as R  # renomeie roteiro_exemplo.py -> roteiro.py no projeto
from PIL import Image
ims = []
for t in ts:
    raw = subprocess.run([R.FFM, "-v", "error", "-ss", str(min(t, R.SRC_END)), "-i", src, "-frames:v", "1", "-vf", "scale=1080:1920", "-pix_fmt", "rgb24", "-f", "rawvideo", "-"], capture_output=True).stdout
    fr = Image.frombytes("RGB", (1080, 1920), raw)
    ims.append(R.render(t, fr).convert("RGB").resize((432, 768)))
sheet = Image.new("RGB", (432 * len(ims), 768))
for i, im in enumerate(ims): sheet.paste(im, (432 * i, 0))
sheet.save(outdir)
