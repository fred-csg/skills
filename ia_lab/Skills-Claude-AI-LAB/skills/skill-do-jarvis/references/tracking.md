# Tracking (caixas, malhas, callouts e miras presos ao vídeo)

Regra: nenhum elemento de detecção fica em coordenada fixa. Se o alvo ou a câmera mexe, o elemento acompanha.

## Rosto
- Âncora por frame original (cx, cy, topo da cabeça pela máscara, altura do rosto), lida via `fm` (mapa frame novo → frame original da EDL).
- No Remotion: calcular a partir de `useCurrentFrame()` → `fm` → âncora, e aplicar no `style` do elemento.

## Objetos — `track.mjs` (Node, sem Python)
Dependências só via npm: `@techstark/opencv-js` (OpenCV em WASM) + `ffmpeg-static`.
- Lista de elementos num `.ts`/`.json` (`els.json`): `{id, x, y, w, h, tin, tout}`. No Remotion, um wrapper 1080x1920 por elemento: a animação mexe no elemento, o tracking mexe no wrapper.
- Frames: `ffmpeg -i corte.mp4 -vf scale=540:960,format=gray -f rawvideo -` (pipe) → `cv.matFromArray(960,540,cv.CV_8UC1,buf)`.
- Pipeline por elemento (cinza 540x960):
  - features em 80% da bbox, máx. 100. O opencv-js NÃO tem `goodFeaturesToTrack`: usar `cv.cornerMinEigenVal(img, eig, 3, 3)` e pegar os N maiores com distância mínima de ~5 px;
  - `cv.calcOpticalFlowPyrLK` (win 31, 4 níveis) + checagem forward-backward < 1 px;
  - o opencv-js NÃO tem `estimateAffinePartial2D`: usar `cv.estimateAffine2D(p0, p1, inliers, cv.RANSAC, 2)` e reduzir para similaridade (escala = √|det| da parte 2x2, sem rotação/cisalhamento; translação = coluna 3). Testado: recupera deslocamento sintético (5, 3) exato;
  - escala limitada a 0.92–1.08 por frame; repor features quando sobrarem < 30;
  - rastrear de `tref` para frente até `tout` e para trás até `tin`, parando no corte de cena;
  - suavizar com gaussiana 1D (σ 1.6 em dx/dy, 2.4 em log s) — função própria em JS.
- `noscale` para rostos falando (a escala derivava a 0.7), mãos em superfície lisa (colapsava a 0.28) e callouts.
- Config por elemento em `trkcfg.json` (chave = tin com 2 casas: tref, noscale, bbox, smooth).
- Saída `tracks.json`: `{id:{f0,ref,d:[[dx,dy,s]...]}}`, aplicado como `translate(dx,dy) scale(s)` com origin no centro da ref.
- Alternativa: se o usuário já tiver Python, o mesmo pipeline em `opencv-python` + `scipy` (`goodFeaturesToTrack`, `estimateAffinePartial2D`, `gaussian_filter1d`).

## Validação (sempre)
- Contact sheet com a caixa rastreada em 5 frames por elemento ANTES do render (stills do Remotion ou `tile` do ffmpeg-static); corrigir e repetir.
- Erro mais comum: coordenada medida errada. O contact sheet pega.

## Casos difíceis
- Zoom > 2×/s → dividir em dois elementos (o segundo com tref no meio do zoom).
- Conteúdo de IA mudando de forma → callout em vez de caixa justa.
- Tela rolando trackeia bem como objeto.
- Encerrar o elemento antes de o alvo sair de quadro, e 0.05 s antes de um corte.
