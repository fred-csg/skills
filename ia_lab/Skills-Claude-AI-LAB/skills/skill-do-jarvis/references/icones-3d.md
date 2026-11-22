# Ícones 3D (three.js)

Cada ideia forte da fala ganha um ícone 3D real (não emoji, não ícone chapado). No máximo 1 ícone grande por vez.

## Como fazer
- Renderizar o ícone direto na composição do Remotion com `@remotion/three` (`ThreeCanvas` em `AbsoluteFill` com fundo transparente), oscilando a partir de `useCurrentFrame()` (rotY ±0.55 + float em seno).
- `NeutralToneMapping` (ACES lava as cores claras), RoomEnvironment, key branca + rim no acento.
- Materiais do look do config (`look_padrao`): VIDRO (transmission + arestas gelo) ou HOLOGRAMA (ciano translúcido + arestas). Ver `estilo-visual.md` e `assets/remotion-3d-template/src/scene/looks.ts`.
- Vidro em canvas transparente refrata preto: no ícone sobre vídeo, preferir holograma ou vidro fosco, ou dar ao vidro um `scene.background`/envMap próprio.
- Biblioteca usada até aqui (modelar com primitivas/ExtrudeGeometry/TextGeometry): claquete, chip AI, microfone, lâmpada, foguete, play, core (rede), alerta, varinha, numeral do ano (TextGeometry helvetiker_bold), interrogação, tesoura, cadeado, balão de chat.

## Entrada e saída
- Entra com out back + blur → 0, sai com in back; drop-shadow + glow na cor de acento (gelo no vidro, ciano no holograma).
- Posições no 9:16: atrás da cabeça entre y 250–650 (camada "atrás" de `segmentacao.md`), ou nas laterais (x<300 / x>760, y 650–1100).
