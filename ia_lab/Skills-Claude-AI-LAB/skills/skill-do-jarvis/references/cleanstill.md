# CLEANSTILL — estilo de motion "limpo e calmo"

Aprendido em 2026-10-09 a partir de um vídeo de referência enviado pelo usuário (anúncio de 60 s, 16:9, 30 fps, locução em inglês). Nome dado pelo usuário: **cleanstill**. É um estilo ALTERNATIVO ao padrão Vidro/Holograma: quando o usuário escolhe cleanstill, este arquivo manda na paleta, na tipografia e nas transições (as regras de movimento do `estilo-visual.md` continuam valendo: easing sempre, nada linear, nada seco, sem mosaico).

Template pronto: `assets/cleanstill-template/` (Remotion, sem three.js). Componentes em `src/cleanstill/`, demo de ~35 s com cada recurso em `src/CleanstillDemo.tsx` (16:9 e 9:16).

## 1. A ideia em uma frase
Anúncio "Apple keynote + Notion": fundo claro quase branco com névoa pastel, muito ar, **uma ideia por plano**, texto cinético palavra a palavra sincronizado com a locução, objetos de UI e "produto" flutuando com profundidade suave, câmera sempre num push lento ("still" vivo, nunca parado), transições de luz (bloom, portal, burst), nada de HUD, nada de glitch, nada de neon.

Quando oferecer: anúncio de produto/serviço/infoproduto, lançamento, explicação de ferramenta ou app, conteúdo "premium/clean", CTA de comentário. Quando NÃO: vídeo falado com pessoa (aí o padrão Jarvis com tracking é melhor), conteúdo tech/HUD, tom zoeiro pesado.

## 2. Paleta (medida no vídeo)
| Token | Cor | Uso |
|---|---|---|
| bg | `#F3F4FB` | fundo base off-white azulado |
| névoas | lavanda `#E4DDFB`, azul-bebê `#D8E5FA`, pêssego `#F9E4DF` | manchas radiais grandes derivando nos cantos |
| ink | `#363948` | texto principal (nunca preto puro) |
| inkSoft | `#A3A7B6` | kicker, palavras-fantasma, linhas fora de foco |
| blue | `#3764E0` (brilho `#6F93F0`) | 1 palavra-chave por frase, setas, colchetes |
| pill | `#3B6FF0` | pills de preço, botões, destaque "selecionado" |
| céu | `#0A6CCB` → `#5DB2F2` → `#A8D8FA` | palco de céu com nuvens |
| night | `#040714` + arco `#2F55E8` + linha `#CEF3FF` | cena escura de virada (1 por vídeo) |
| warm | `#E7986B` | só 1 ícone/acento quente por cena (asterisco, "PAGO") |

Se o cliente tiver marca, trocar `blue`/`pill` pela cor da marca e manter o resto.

## 3. Tipografia
- **Títulos:** Bricolage Grotesque 700/800, tracking −0.025em (−0.04em nas palavras de impacto). Grotesca larga e simpática.
- **Acento serifado:** Instrument Serif *Italic* 400 — a segunda linha "emocional" ("like mine?", "beautiful.", "in minutes."), ~55–65% do tamanho do título, cor ink.
- **Apoio/kicker:** Inter 500/600, pequeno, inkSoft, acima do título ("could make", "Just this.").
- Tudo via `@remotion/google-fonts` (já no template). Exceção consciente à regra "sempre Poppins": o cleanstill tem tipografia própria. Se o usuário preferir Poppins, trocar só `FONT_HEAD`.
- Tamanhos (unidade = menor dimensão 1080): título 150–190, frase 70–90, serifa 90–100, kicker 40–46, pills 44–48.

## 4. Palcos (fundos)
1. **PastelHaze** (padrão, ~70% do vídeo): off-white + 4 névoas radiais derivando devagar + grão 4%.
2. **SkyClouds**: céu azul saturado com nuvens volumosas emoldurando laterais e base; o centro fica livre para o objeto herói (notebook, arquivo, cartão). Nuvens procedurais no template; para ficar igual à referência, usar uma FOTO/vídeo de nuvens (do usuário, banco de imagens ou gerada por IA) em `public/` com leve push — fica bem mais rico.
3. **NightArc**: quase preto + arco de planeta subindo com brilho azul e linha fina clara. Uma vez por vídeo, na virada emocional ("e agora você está pensando…").
4. Abertura opcional: foto de paisagem (céu + montanhas) com texto branco → bloom.

## 5. Catálogo de recursos (frase → recurso) — componentes do template
| Recurso | Componente | Receita |
|---|---|---|
| Texto palavra a palavra | `Line` / `W` | cada letra: blur 10→0, y .28em→0, opacidade, stagger 1 f, 14 f, ease out quint (`bezier(.22,1,.36,1)`). Tempo de cada palavra = tempo dela na locução. |
| Palavra-chave azul com brilho | `s: 'key'` | azul + faixa de luz atravessando a palavra (máscara 100°, 30 f) logo depois que ela assenta. 1 por frase. |
| Segunda linha serifada | `s: 'serif'` | Instrument Serif italic, entra 1 beat depois do título. |
| Karaokê com fantasmas | `Line ghost` | a frase inteira já aparece a 18% (blur 2.5) e cada palavra "acende" quando é falada. Ótimo para frases longas no topo com imagem embaixo. |
| Destaque "selecionado" | `s: 'hl'` | retângulo azul cresce da esquerda atrás da palavra (scaleX 0→1, 10 f), texto fica branco, glow azul. |
| Kicker | `Kicker` | Inter 500 cinza, pequeno, entra antes do título. |
| Saída zoom-through | `ZoomExit` | o bloco cresce 1→1.35, blur 0→16, some em 10 f (ease in). Saída padrão de cartela de texto. |
| Lista em foco | `FocusList` | roda tipo seletor iOS: linha central nítida com seta azul →, vizinhas 22% e blur 2.5, rola 1 linha por beat (14 f inOut). "Sem estúdio / Sem editor / Sem equipe". |
| Pills de vidro laterais | `GlassPill` | duas metades da frase em pills translúcidas à esquerda e à direita do objeto herói, entrando de lado com blur. |
| Pill de preço/selo | `PricePill` | azul, pop com out back, no canto superior direito de cartões. |
| Cartão-arquivo com seleção | `PaperCard` | papel branco inclinado em 3D flutuando + caixa de seleção azul estilo Figma (8 alças + etiqueta) + cursor clicando. |
| Cursor | `Cursor` | seta macOS andando por pontos-chave com easing, encolhe no clique. |
| Objeto herói | `Laptop` | notebook flutuando no céu (bob ±8 px), tela com a UI; push lento da câmera. Pode receber um cartão voando para dentro da tela. |
| UI do app | (livre) | UI clara e real: campo de prompt digitando, dropdown de opções com ✓, botão azul redondo com clique, toasts "Designing layout ✓ / Writing index.html ◌". Câmera mergulha na UI (zoom 1→1.6 + leve tilt). |
| Carrossel 3D | `Carousel3D` | cartões (sites/produtos) em arco com perspectiva, girando devagar; pode girar em volta de um título ("Premium websites / in minutes."). |
| Parede de miniaturas | `ThumbWall` | grade de cartões correndo em linhas alternadas, arranque com blur de movimento. |
| Cartão slot | `SlotCard` | vidro fosco central com colchetes azuis, palavra trocando como slot (anterior sobe e desfoca, próxima vem de baixo): "Portfólios → Lojas → Landing pages". |
| Lupa revelando | `LensReveal` | lupa passa sobre o cartão e mostra outro conteúdo dentro da lente ("GRÁTIS" → "PAGO"); no fim a revelação toma o cartão todo. |
| Palavra de impacto | `Impact` | branca, 190, blur 24→0, escala 1.15→1, glow — na cena escura. |
| Logo + tagline | (livre) | ícone quente girando 1 vez + nome Bricolage 800 + tagline Inter com 1 palavra em serifa italic quente. |
| CTA social | (livre) | cartão de perfil branco (avatar com anel azul, @, grade de posts, botão Seguir → "Seguindo ✓"), campo de comentário digitando a palavra, DM chegando com arquivo anexado; fecho: avatar + botão azul "Comente 'PALAVRA'" + linha pequena "só os primeiros N". |
| Mascote (opcional) | (livre) | personagem pixel-art PRÓPRIO desenhado em código, reagindo (chapéu de mago desenhando número com faíscas, segurando a lupa). Nunca copiar o mascote da referência. |
| Número em matriz de pontos | (livre) | numeral feito de pontos/bolinhas que aparecem seguindo o traço (desenhado pela varinha). |

## 6. Transições (`transitions.tsx`)
| Transição | Quando | Receita |
|---|---|---|
| `Bloom` (sol/brilho) | sair de cena de céu/foto para o branco | disco branco radial nasce no centro, cresce e lava a tela (55% do tempo), próxima cena aparece enquanto o branco dissipa. 18–20 f. |
| `BlobReveal` (portal) | revelar o palco de céu/objeto herói | bolha orgânica ondulando cresce do centro com borda ciano luminosa, revelando a cena nova dentro. 20–22 f. |
| `RayBurst` | virada para "resultado/mostruário" | ícone-asterisco gira e cresce num squircle branco, raios explodem para fora + flash branco. ~26 f. |
| `ZoomExit` | sair de cartela de texto | ver acima. |
| `CrossBlur` | trocas suaves entre UIs | dissolve com desfoque e escala leve. 10–14 f. |
| Whip com blur de movimento | entrar na parede de miniaturas | arranque rápido com blur que assenta. |
| Corte seco | entrar na cena escura e sair dela | cortar no beat da fala. |
- **PROIBIDO:** o dissolve em retícula/halftone (pontinhos) que aparece na referência aos 13 s — é mosaico/pixel, esse tipo de transição fica amador. Usar `CrossBlur` ou `Bloom` no lugar.

## 7. Câmera e ritmo
- Câmera "still" viva: todo plano tem push lento 1.00→1.06 (`Drift`) ou deriva lateral; objetos flutuam (seno lento). Nunca um frame congelado.
- Um plano a cada 2–3 s; uma ideia por plano; no máximo 2 elementos de texto + 1 objeto por vez. Muito respiro.
- Texto 100% sincronizado à locução (transcrever com `assets/legenda-template/scripts/transcrever.py` e usar o tempo de cada palavra como `at`).
- Estrutura da referência (60 s), usar como molde de anúncio:
  1. 0–1.5 s HOOK "E se…" sobre céu/paisagem → bloom.
  2. 1.5–4.3 promessa em cartelas ("um arquivo… poderia fazer / **vídeos** / *como os meus?*") → zoom-through.
  3. 4.3–6.6 negações em lista em foco ("Sem estúdio. Sem editor. Sem equipe.").
  4. 6.9–9 o produto: "Só isso. Um **arquivo**." + cartão com seleção e cursor.
  5. 9–15 portal → objeto herói no céu + pills laterais; câmera mergulha na UI (escolher opção, clicar enviar) → resultado "Assista."
  6. 15–19 prova de valor: karaokê "Todo dia, pagam **milhares** por um site assim" + carrossel com pills de preço.
  7. 19–24 a ferramenta trabalhando (UI + toasts "Desenhando layout ✓").
  8. 24–29.5 burst → mostruário: parede de miniaturas + cartão slot; carrossel girando em volta de "Sites premium *em minutos.*"
  9. 30–38 assinatura (logo + tagline serifada), objeto herói de novo com pills "Cada frame que você viu veio desse arquivo".
  10. 38.4–41 cena escura: "E agora você tá **pensando…**" → "**sem chance.**"
  11. 41.5–56 oferta + CTA: arquivo flutuando "Quer?", perfil/seguir/comentar/DM, escassez com lupa GRÁTIS→PAGO, cartão final com botão "Comente 'PALAVRA'".
  12. 56.5–60 end card (só se o usuário quiser a marca dele).

## 8. Layout
- 16:9 (formato da referência): composição central; cena "texto à esquerda + objeto à direita" no plano do produto.
- 9:16: os mesmos componentes (tudo em unidade da menor dimensão). Empilhar: objeto em cima, texto embaixo; pills acima e abaixo do objeto; frase karaokê no topo (y ≈ 300) com padding lateral 70.
- Margem mínima de 6% das bordas para texto. Nada de HUD, cantoneiras, REC ou barra de progresso neste estilo.

## 9. Som
Sons SEMPRE da biblioteca do usuário (`pasta_sfx`, ver `references/sfx.md`), nunca por código: trilha do usuário (ou drone/ambiência da biblioteca) + whoosh suave nos blooms/portais/carrossel, shutter/glitch curto nos cliques e pills, impacto leve no "sem chance." e no burst. Voz por cima com ducking.

## 10. Checklist antes do preview
- [ ] Fundo claro com névoa (não branco chapado), grão leve.
- [ ] Cada palavra entra no tempo da fala; 1 palavra-chave azul por frase; serifa italic só na linha emocional.
- [ ] Todo plano com push/deriva; nada parado, nada linear, nada aparecendo seco.
- [ ] Transições só do item 6 (zero mosaico/halftone/pixel).
- [ ] No máximo 1 acento quente por cena; 1 cena escura no vídeo.
- [ ] Sem HUD/glitch/tracking (isso é do estilo padrão).
- [ ] Nada copiado da referência: sem @ do autor original, sem mascote dele, sem marcas de terceiros; nome do usuário só se ele pedir.
