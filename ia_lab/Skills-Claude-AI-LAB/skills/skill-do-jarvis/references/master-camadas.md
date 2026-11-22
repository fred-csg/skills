# Master em alta, em camadas (só após aprovação do preview + autorização explícita)

Destino: `<pasta_saida do config.json>\<PROJETO>_PACOTE\`.

## Camadas
- **BASE**: vídeo cortado + cor + câmera/glitch/escurecimento do fundo (vídeo, recorte e glitch visíveis; overlays escondidos).
- **MOTION_ALPHA**: só os gráficos, fundo transparente. Os elementos "atrás da cabeça" e o contorno vão com máscara invertida (`maskImage: linear-gradient(#000,#000), url(mk)` + `maskComposite: exclude` / `-webkit-mask-composite: xor`), para o recorte atrás da pessoa vir no alpha.
- **BASE_LIMPA**: vídeo cortado em SDR, sem câmera nem overlays.
- **MASTER_FINAL**: BASE + ALPHA compostos.

## Como renderizar (Remotion)
Uma prop `modo: 'base' | 'alpha' | 'limpa' | 'final'` na composição, escondendo/mostrando camadas.
- Opacos: `npx remotion render <Comp> out/BASE.mp4 --props='{"modo":"base"}' --gl=angle --crf=14`.
- Alpha: `--props='{"modo":"alpha"}' --codec=prores --prores-profile=4444 --pixel-format=yuva444p10le --image-format=png` (MOV com alpha) ou `--sequence --image-format=png`.

## Encodes
- BASE / LIMPA / MASTER: H.264 high, CRF 12–15, tags bt709, `-movflags +faststart`.
- ALPHA: MOV ProRes 4444 com alpha.

## Áudio
VOZ.wav, SFX_MIX.wav, MIX_FINAL.wav, SFX_USADOS/, SFX_CUES.csv (ver `sfx.md`).

## XML do Premiere (FCP7 xmeml v4)
- Sequência 1080x1920 30 fps; V1 BASE, V2 MOTION_ALPHA, A1 VOZ, SFX em faixas sem sobreposição, com Audio Levels.
- `pathurl` = `file://localhost/` + caminho absoluto do arquivo dentro da `pasta_saida`, com barras `/` e url-encoded (ex.: `file://localhost/C:/Users/.../Meu%20Projeto_PACOTE/BASE.mp4`).

## Leia-me do pacote
`LEIA-ME.txt` dentro do pacote explicando as camadas e como montar no editor.
