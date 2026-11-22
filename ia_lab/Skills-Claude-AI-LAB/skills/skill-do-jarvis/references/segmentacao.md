# Segmentação da pessoa (elementos ATRÁS da cabeça)

## Máscara
Saída esperada: `mk/%05d.png` RGBA 540x960 (alpha = pessoa), indexada pelo frame original, com borda suave e estável no tempo.

- **Caminho validado (precisa de Python):** `selfie_segmentation.tflite` do pacote npm `@mediapipe/selfie_segmentation`, rodado com `ai-edge-litert` (Interpreter direto; a API tasks do mediapipe falha por metadata). Borda com `cv2.ximgproc.guidedFilter` (`opencv-contrib-python`) + suavização temporal (média com o frame anterior).
- **Sem Python (ainda não validado nesta skill):** rodar o segmentador do MediaPipe para web (`@mediapipe/tasks-vision`, ImageSegmenter) dentro do Chromium do Remotion/numa página local, ou um modelo de matting em ONNX com `onnxruntime-node`. Testar num trecho curto e conferir a borda num contact sheet antes de usar no vídeo todo.
- Se nenhum caminho estiver disponível, avisar o usuário e fazer a edição sem elementos atrás da cabeça (o resto do padrão de qualidade continua).

## Ordem das camadas (Remotion, `AbsoluteFill`s empilhados)
Dentro do grupo de câmera (transform-origin no centro da pessoa; é o que recebe zoom/punch/shake):
1. vídeo (`<OffthreadVideo>` ou frame)
2. "atrás" — números, palavras gigantes, ícones 3D e cards que ficam atrás da pessoa
3. contorno — a máscara com `filter: brightness(0) drop-shadow(<acento>)` = contorno luminoso da silhueta
4. vídeo de novo, com `maskImage: url(mk/NNNNN.png)` (mask-size 1080x1920) = a pessoa por cima
5. detecção trackeada (escala com o zoom)
6. cópias do glitch

Fora do grupo de câmera: vinheta, escurecimento, UI (perspective 1100), HUD, flash.
