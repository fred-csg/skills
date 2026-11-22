# Analisa o vídeo quadro a quadro: máscara da pessoa, âncora do rosto, cortes de cena e cor de destaque.
import json, os, sys
import cv2
import numpy as np
import mediapipe as mp
from scipy.ndimage import gaussian_filter1d

src, out = sys.argv[1], sys.argv[2]
os.makedirs(os.path.join(out, 'mk'), exist_ok=True)
cap = cv2.VideoCapture(src)
W, H = int(cap.get(3)), int(cap.get(4))
MW, MH = 360, 640  # máscara em meia resolução

seg = mp.solutions.selfie_segmentation.SelfieSegmentation(model_selection=0)
fd = mp.solutions.face_detection.FaceDetection(model_selection=1, min_detection_confidence=0.4)

prev_mask, prev_small = None, None
anchors, diffs, hues = [], [], []
i = 0
while True:
    ok, frame = cap.read()
    if not ok:
        break
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    # máscara
    m = seg.process(rgb).segmentation_mask.astype(np.float32)
    m = cv2.resize(m, (MW, MH))
    guide = cv2.resize(frame, (MW, MH)).astype(np.float32) / 255
    m = cv2.ximgproc.guidedFilter(guide, m, 6, 1e-3)
    m = np.clip((m - 0.35) / 0.4, 0, 1)
    small = cv2.resize(cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY), (135, 240)).astype(np.float32)
    d = float(np.mean(np.abs(small - prev_small))) if prev_small is not None else 0.0
    diffs.append(d)
    if prev_mask is not None and d < 18:
        m = 0.55 * m + 0.45 * prev_mask  # suavização temporal (não atravessa corte)
    prev_mask, prev_small = m, small
    rgba = np.zeros((MH, MW, 4), np.uint8)
    rgba[..., :3] = 255
    rgba[..., 3] = (m * 255).astype(np.uint8)
    cv2.imwrite(os.path.join(out, 'mk', f'{i:05d}.png'), rgba)

    # rosto
    r = fd.process(rgb)
    a = None
    if r.detections:
        bb = max(r.detections, key=lambda x: x.score[0]).location_data.relative_bounding_box
        cx, cy, fw, fh = bb.xmin + bb.width / 2, bb.ymin + bb.height / 2, bb.width, bb.height
        # topo da cabeça pela máscara, nas colunas do rosto
        x0, x1 = int(max(0, (cx - fw / 3) * MW)), int(min(MW, (cx + fw / 3) * MW))
        col = m[:, x0:x1].max(axis=1)
        ys = np.where(col > 0.5)[0]
        top = ys[0] / MH if len(ys) else bb.ymin - fh * 0.4
        a = [cx, cy, fw, fh, top]
    anchors.append(a)

    # cores saturadas do cenário (fora da pessoa)
    if i % 6 == 0:
        hsv = cv2.cvtColor(cv2.resize(frame, (MW, MH)), cv2.COLOR_BGR2HSV)
        sel = (hsv[..., 1] > 150) & (hsv[..., 2] > 150) & (m < 0.2)
        hues.extend(hsv[..., 0][sel].tolist())
    i += 1

n = i
# preencher buracos do rosto e suavizar (sem atravessar cortes)
cuts = [k for k in range(1, n) if diffs[k] > 22 and diffs[k] > 2.2 * (np.median(diffs[max(1, k - 6):k + 6]) + 1e-3)]
arr = np.array([a if a else [np.nan] * 5 for a in anchors], dtype=np.float64)
bounds = [0] + cuts + [n]
for s, e in zip(bounds[:-1], bounds[1:]):
    seg_ = arr[s:e]
    for c in range(5):
        v = seg_[:, c]
        good = ~np.isnan(v)
        if good.sum() == 0:
            v[:] = [0.5, 0.25, 0.18, 0.12, 0.14][c]
        else:
            v[~good] = np.interp(np.where(~good)[0], np.where(good)[0], v[good])
        seg_[:, c] = gaussian_filter1d(v, 2.0 if c < 2 else 4.0, mode='nearest')
    arr[s:e] = seg_

hist = np.bincount(np.array(hues, dtype=np.int64), minlength=180) if hues else np.zeros(180)
top_h = np.argsort(gaussian_filter1d(hist.astype(float), 3, mode='wrap'))[::-1]
picked = []
for h in top_h:
    if all(min(abs(h - p), 180 - abs(h - p)) > 15 for p in picked):
        picked.append(int(h))
    if len(picked) == 3:
        break
cores = []
for h in picked:
    bgr = cv2.cvtColor(np.uint8([[[h, 230, 255]]]), cv2.COLOR_HSV2BGR)[0, 0]
    cores.append('#%02x%02x%02x' % (bgr[2], bgr[1], bgr[0]))

json.dump({'w': W, 'h': H, 'n': n, 'cuts': cuts, 'cores': cores,
           'anch': [[round(x, 4) for x in r] for r in arr.tolist()]}, open(os.path.join(out, 'analise.json'), 'w'))
print('quadros', n, 'cortes', cuts, 'cores', cores)
