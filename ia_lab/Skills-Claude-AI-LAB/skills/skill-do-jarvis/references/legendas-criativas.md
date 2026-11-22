# Legenda criativa com tracking (estilo "colagem cinética")

Aprendido em 2026-10-09 analisando um vídeo de referência enviado pelo usuário (35 s, edição de criador de tech: palavras espalhadas pela cena, presas ao que se move, atrás da pessoa, com palavras-chave gigantes em curva). É o estilo de legenda padrão da skill quando o usuário pedir legenda "criativa", "dinâmica" ou "com tracking". Legenda simples (2–4 palavras embaixo) só se pedirem.

## 1. O que define o estilo
1. **Palavra por palavra, no tempo exato da fala.** Cada palavra surge no início da sílaba (timestamps por palavra, nunca por frase). Ritmo de 0,12–0,35 s entre palavras.
2. **A frase se acumula na tela como colagem** e some inteira no fim da frase (ou no corte de cena). Nada de "uma linha que troca": as palavras ficam e vão preenchendo o espaço livre.
3. **Hierarquia em duas vozes:**
   - palavras comuns: brancas, pequenas/médias, Poppins Bold 700 (nunca fina: peso 500 foi reprovado), leve sombra;
   - **1 palavra-chave por frase** (às vezes 2): ENORME (3–8× maior), Poppins Black 900, na cor de destaque. É ela que dá o impacto.
4. **Cor de destaque vem da cena** (na referência, o vermelho do abajur e do tapete). Amostrar a cor dominante saturada do vídeo; se não houver, usar o acento do look (gelo `#bfeaff` no VIDRO, ciano `#7fe3ff` no HOLOGRAMA, ou limão `#D7FF3A` só se pedirem).
5. **CENTRALIZADO em volta do rosto (regra do usuário, 2026-10-09).** O foco é sempre o centro: tudo perto do rosto, NUNCA na frente do rosto, nunca colado nele, e NUNCA no teto, nos cantos ou encostado nas bordas. Margem central de 12% da largura de cada lado (nada fora dos ~76% do meio). Nada de faixa fixa embaixo.
6. **Texto atrás da pessoa:** a palavra-chave gigante passa ATRÁS da cabeça/corpo (máscara de segmentação, seção 6 da skill). As letras somem atrás do cabelo e reaparecem do outro lado.
7. **Texto em curva:** a palavra-chave faz um arco em volta da cabeça (como uma auréola), ou segue uma curva no chão/na mesa. Palavras secundárias às vezes também curvam ("editor" em arco, "MCP" girado 30°).
8. **Preso à cena (tracking):** o bloco de palavras acompanha o rosto (âncora do rosto por frame) ou o objeto. Em plano de detalhe (mão, teclado, mesa), o texto é colado NA SUPERFÍCIE, em perspectiva (plano 3D com 4 cantos rastreados): parece impresso no tapete/teclado.
9. **Mistura de tamanhos, pesos e inclinações** na mesma frase: rotação −15°…+15°, uma palavra em itálico ou esticada, outra pequena colada embaixo. Composição solta, não em grade, mas equilibrada (pesos visuais opostos).
10. **Micro-legenda de apoio (opcional):** frase completa em fonte minúscula (≈14 px em 1080) num canto inferior, digitando letra por letra. Dá "cara de interface" sem competir.

## 2. Animações (tudo com easing, nunca linear)
| Momento | Como |
|---|---|
| Entrada padrão (palavra comum) | 2–4 frames: scale 0.6→1.08→1 (out back), blur 8px→0, opacity 0→1. Leve deslocamento de 10–20 px vindo da direção da leitura. |
| Entrada da palavra-chave | 4–6 frames: scale 1.6→1 com motion blur direcional (blur só em X ou Y), squash & stretch (scaleY 1.3→0.9→1), ou letras caindo uma a uma girando (stagger 1 frame, rotação aleatória ±25° que assenta). |
| Letras espalhadas | Para palavras emocionais ("CRAZIER"): cada letra em posição/rotação própria, empilhadas na vertical, cada uma entrando com bounce. |
| Ênfase | RGB split (cópia vermelha e ciano deslocadas ±6 px por 3–4 frames) + shake curto de 2–3 px. |
| Transição entre cenas | Blur de whip pan arrastando o texto junto com a câmera, ou só o corte. **PROIBIDO: mosaico/pixelate/blocos coloridos** (fica amador). |
| Saída | Corta com a cena; ou o bloco inteiro sai com blur + scale 1→0.9 em 4 frames. Nunca dissolver em pixels. |
| Elemento de apoio | Linha/swoosh em gradiente (rosa → roxo) desenhando entre ícones ou palavras (stroke-dashoffset), sincronizada com a fala. |

## 3. Como implementar (Remotion)
1. **Timestamps por palavra:** 1º `.srt`/roteiro do usuário remapeado; 2º `@remotion/install-whisper-cpp` (`installWhisperCpp` + `downloadWhisperModel('medium')` + `transcribe({tokenLevelTimestamps: true})`, roda local, só npm) e `@remotion/captions` para agrupar em palavras/frases. Revisar ortografia e acentos à mão.
2. **Frases:** quebrar por pausa (> 0,35 s) ou pontuação; cada frase vira um "bloco" que limpa a tela no fim. Marcar a palavra-chave de cada frase (substantivo/verbo de impacto, número, nome de ferramenta).
3. **Layout automático do bloco:** a partir da máscara da pessoa e da caixa do rosto, achar as regiões livres; colocar a palavra-chave na maior região (ou em arco sobre a cabeça) e as comuns em volta, sem cobrir olhos/boca. Revisar em contact sheet.
4. **Componentes:**
   - `Word` (entrada pop + blur), `KeyWord` (gigante, cor de destaque, motion blur, squash);
   - `ArcWord` (SVG `<textPath>` num arco com centro na âncora do topo da cabeça; raio ≈ 0,9× largura do rosto);
   - `ScatterLetters` (letras soltas com stagger);
   - `SurfaceText` (CSS `matrix3d` a partir de 4 pontos rastreados = homografia, para texto no chão/mesa/teclado);
   - `MicroCaption` (máquina de escrever no canto);
   - `RgbSplit` (nunca `PixelTransition`).
5. **Profundidade:** camadas `#behind` (atrás da pessoa, recortada pela máscara) e `#front`. Palavra-chave em `#behind`, comuns em `#front`.
6. **Tracking:** bloco inteiro dentro de um wrapper que segue a âncora do rosto (`fm` → frame original); texto de superfície segue os 4 cantos rastreados (`references/tracking.md`).
7. **Não poluir:** no máximo 1 palavra-chave gigante + ~6 palavras comuns na tela ao mesmo tempo. Se a frase for longa, limpar no meio (sub-bloco).
8. **Formato:** funciona em 9:16 e 4:3/16:9. Em 9:16, a faixa de baixo (y > 1500) fica para a micro-legenda e o CTA.

## 4. Checklist antes do preview
- [ ] Toda palavra aparece no frame em que começa a ser falada (conferir 5 trechos no Studio).
- [ ] 1 palavra-chave por frase, gigante, na cor de destaque.
- [ ] Tudo centralizado perto do rosto: nada na frente do rosto, nada no teto, nos cantos ou nas bordas.
- [ ] Palavra-chave passa atrás da cabeça pelo menos nas frases mais fortes.
- [ ] Em plano de detalhe, texto colado na superfície com perspectiva.
- [ ] Nenhuma transição em mosaico/pixel; corte ou whip com o texto saindo junto.
- [ ] Ortografia e acentos conferidos.

## 5. Caminho validado (teste "LUCAS FALANDO", 2026-10-09, 23 s, 720x1280 → 1080x1920)
Template pronto em `assets/legenda-template/` (Remotion + scripts Python). Passo a passo:
1. **Transcrição por palavra:** `scripts/transcrever.py` com `faster-whisper` large-v3, `language="pt"`, `word_timestamps=True`, `vad_filter=True`. Na GPU o ctranslate2 pode falhar por falta de `cublas64_12.dll`: usar `device="cpu", compute_type="int8"` (23 s de áudio em ~40 s). Gera `palavras.json` (`w`, `a`, `b`).
2. **Análise por quadro:** venv próprio (não mexer no Python do usuário) com `mediapipe==0.10.14` + `opencv-contrib-python`. `scripts/analise.py` gera `public/mk/NNNNN.png` (máscara da pessoa, 360x640, guided filter + suavização temporal que não atravessa corte), `analise.json` com âncora do rosto por quadro (`cx, cy, fw, fh, top`, normalizados e suavizados), cortes de cena e as 3 cores saturadas dominantes do cenário (a 1ª vira a cor de destaque).
3. **Remotion:** `public` fora de pasta sincronizada (`Config.setPublicDir`). Camadas: vídeo → palavras-chave "behind" → vídeo de novo com `maskImage: url(mk/NNNNN.png)` (a pessoa por cima) → palavras comuns e chaves "front". Pré-carregar a máscara do quadro com um `<Img>` invisível (senão o CSS mask pode não estar pronto no screenshot).
4. **Layout pela âncora do QUADRO ATUAL** (não da início da frase): o texto acompanha o rosto e é reencaixado na tela a cada quadro. Ancorar no início e só transladar empurra o texto para fora quando a pessoa anda.
5. **Medir antes de posicionar** (`@remotion/layout-utils` `measureText`): reduzir a fonte da linha até caber no próprio lado (mín. 42%, sem invadir o outro lado nem o rosto) e prender dentro da margem central (12% da largura); palavra-chave gigante limitada a ~76% da largura e centro preso por meia-largura; arco com raio que cabe na tela e texto que cabe em ~86% da meia-circunferência.
6. **Zonas aprovadas em 9:16 (v3; `u` = largura do rosto, a partir do centro do rosto):**
   - palavra-chave gigante ATRÁS da cabeça, na altura do topo (`y ≈ −0.8u`) — a cabeça cobre só o meio das letras; no rosto fica ilegível;
   - palavras comuns ao lado do pescoço (`y +0.85u`) e dos ombros (`y +1.42u`), começando a `0.8u` do centro (folga do rosto), e no centro do peito (`y +2.0u`);
   - ao lado da cabeça (`y −0.75u` / `−0.25u`) só em bloco sem chave atrás da cabeça, e só palavras curtas; palavra longa vai para o centro, logo abaixo do queixo (`y ≈ +0.95u`);
   - arco em cima da cabeça: raio 1.3–1.45u, linhas do bloco vão para o pescoço/ombros;
   - segunda palavra-chave do bloco (ex.: INTERAÇÕES) entra grande na frente, no centro do peito.
   - REPROVADO na v2: palavras no teto (`y −2.35u`) e encostadas nas bordas.
7. **Render:** stills de conferência em lotes de no máximo 4 em paralelo (12 de uma vez travou um processo). Vídeo de 23 s renderizou em ~2 min com `--concurrency=8`.
8. **Pendências conhecidas:** texto colado em superfície (`SurfaceText`) e swoosh ainda não implementados no template.
