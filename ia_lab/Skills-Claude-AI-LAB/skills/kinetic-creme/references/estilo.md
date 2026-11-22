# Kinetic Creme — análise da referência e regras de estilo

Referência: Reels de 40,5 s, 720×1280, 30 fps (motion feito em código, sobre "skill que faz reels ilimitados"). Analisado quadro a quadro a cada 0,5 s + tiras de 0,1 s nas transições.

## Linha do tempo da referência (o que acontece e quando)
| Tempo | Beat | Visual |
|---|---|---|
| 0,0–4,3 | Gancho | Ícone `.skill` (doc) e ícone laranja tipo "sol" surgem; linha laranja liga os dois com bolinhas viajando; chip mono `reels: 1 → ∞`; dezenas de miniaturas de reels jorram do ícone e se espalham no topo girando. Título palavra a palavra "Essa skill do **Claude** faz reels **ilimitados**". Duas pílulas brancas com ✓ verde. |
| 4,3–6,3 | Virada | Chicote lateral com desfoque. Caps espaçadas letra a letra "DEIXA EU TE MOSTRAR", "COMO FUNCIONA" gigante, sublinhado laranja, glifos `{ }` e `( )` laranja translúcidos flutuando. Sai inclinando. |
| 6,3–9,3 | Prova 1 | Janela escura estilo macOS: código HTML digitando; tira de miniaturas; tag "IA de vídeo" que é riscada. Cartão creme embaixo com a legenda palavra a palavra. |
| 9,3–13,4 | Objeção | Linha cinza "Primeiro, você deve estar pensando", frase grande "que esses reels ficam ruins" → riscada (barra preta desenhando) e esmaecida → carimbo laranja inclinado "não ficam não." com overshoot. |
| 13,4–18,0 | Bastidor | Mockup de editor escuro (timeline, waveform, preview do próprio vídeo rebobinando), depois card de terminal com ✓ checklist. |
| 18,0–21,7 | Pergunta | Selo laranja redondo "?" + texto cinza + "Isso não **viraliza**" + linha de gráfico. |
| 21,7–28,3 | Prova 2 | Janela escura com contadores (views 0→400.000, visitas 0→17.000), gráfico de área subindo com ponto branco brilhante na ponta, tag laranja inclinada "em apenas 2 dias", chip branco com ícone, miniaturas. Legenda em cartão creme com números em laranja. |
| 28,3–32,3 | Comparação | Mesma janela vira gráfico de barras: barra laranja alta vs. 2 barras cinza baixas. |
| 32,3–34,6 | Escala | Ícone central + halo quadrado arredondado + 8 celulares em rede ligados por linhas laranja com bolinhas; "+12 mil" flutuando. Título "O **Claude** tá mudando o jogo de quem quer **alcance**". |
| 34,6–40,5 | CTA | "Se você quer saber como" + ícone + **Comenta**; caixa de comentário digitando "ILIMITADO" → "Publicado ✓"; rótulo mono "RESPOSTA AUTOMÁTICA" + barra laranja "DM enviada: todos os detalhes"; "chega no seu direct 👇". Segura até o fim. |

Ritmo: um corte a cada 2–6 s; dentro de cada cena, algo novo a cada 0,3–0,6 s (palavra, pílula, número). A locução dita o tempo de cada palavra.

## Fundo (constante, nunca corta)
- Creme `#ECE3D5` + brilho radial central `#FAF6EF` (elipse ~620×760 px em 46%/36%).
- Grão leve (ruído fractal, multiply, 7%).
- ~16 passarinhos em traço (`︶` duplo), `#B8A68F`, batendo asa devagar e derivando pra direita.
- Cidade em linha fina `#D5C2A8` (prédios com linhas de janela, casinhas, árvores, postes) com base em y≈1790, deriva lenta pra esquerda.
- Marca d'água: @ em mono, caps espaçadas, `#CBB89E`, repetida dentro da cidade.

## Tipografia
- Título: sans grotesca pesada (Inter 800), tracking −0,035em, entrelinha 1,06, 84–118 px. Cor `#1C1915`.
- Destaque: mesma fonte em gradiente laranja vertical `#FF8E2E→#EA6511`.
- Apoio: Inter 600, cinza `#6F665C`, 30–40 px, acima do título.
- Rótulos técnicos: JetBrains Mono (chips `reels: ∞`, código, "RESPOSTA AUTOMÁTICA" laranja com tracking .24em).
- Caps espaçadas (.34em) pra "virada".

## Componentes visuais
- **Tile de ícone**: quadrado branco, raio 30%, sombra quente `0 22px 44px rgba(128,92,52,.16)`.
- **Pílula**: branca, raio total, ✓ em círculo verde `#1FA463`, texto 700.
- **Janela escura**: `#1E1C1A`, raio 30, bolinhas vermelha/amarela/verde, título central cinza com ● laranja; tiles internos `#2A2724`.
- **Tag laranja**: gradiente, raio 16, inclinada −3°, sombra laranja.
- **Carimbo**: maior (78 px, 900), entra de escala 1,9 com overshoot + tremida de câmera.
- **Cartão de legenda**: creme `#F7F2EA`, raio 24, texto alinhado à esquerda, números em laranja.
- **Celulares**: moldura quase preta, raio 24, conteúdo variado (foto, UI branca, painel escuro).

## Movimento
- Entrada padrão: opacidade 0→1 + desfoque 13→0 px + subida 30→0 px + escala .94→1, `outExpo` 0,5 s.
- Pop (pílulas, ícones, celulares): escala .4–.55→1 com `outBack` (s≈2), desfoque 14→0.
- Janela: vem de baixo com `rotateX(28°)→0` (perspectiva) + desfoque.
- Contadores: `outExpo` (sobe rápido, freia no número final), formato pt-BR com ponto.
- Gráfico: revela da esquerda (clip), ponto branco com halo laranja acompanha a ponta.
- **Transição chicote**: cena sai pra esquerda (−640 px, `inCubic`) com desfoque até 32 px; a nova entra da direita (+620 px, `outCubic`); 0,44 s centrado no corte; whoosh no meio.
- **Transição inclinada**: cena sai girando −8°, descendo 70 px, encolhendo 10% + desfoque.
- Câmera: zoom lento 1→1,025 por cena; tremida curta (14 px, 0,5 s) no carimbo.

## Som da referência
Locução masculina conversacional (voz de IA), sem música evidente em primeiro plano; whooshes nos cortes, pops/cliques suaves nas entradas, digitação na caixa de comentário.
