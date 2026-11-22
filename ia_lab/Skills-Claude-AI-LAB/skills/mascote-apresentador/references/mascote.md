# Mascote — como animar e como criar um novo

## Lugares = layouts (`PLACES` e `MP`)
| lugar | x, y, escala | quando usar |
|---|---|---|
| `palco` | 510, 880, 1.45 | apresentação, piada, pergunta, virada |
| `base` | 510, 1235, 0.62 | conteúdo em cima (layout **centro** e **bento**) |
| `lado` | 245, 1150, 0.62 | coluna de cards à direita (layout **do lado**) |
| `lousa` | 812, 1215, 0.5 | lousa grande, ele sentado no canto (layout **lousa**) |
| `balao` | 510, 1240, 0.66 | balão de fala saindo dele (layout **balão**) |

`MP = [[t, 'lugar'], ...]` — a troca é com mola + pulinho. Lugar novo = nova entrada em `PLACES`.

## Caras (`FACES` e `FK`)
`neutro, feliz, surpreso, nervoso, bravo, piscadinha, confiante, triste`. Mistura de 0,12 s entre caras; piscada automática a cada 2,4–4,6 s.
Parâmetros: `eh` altura do olho · `lt` pálpebra de cima (0–1) · `la` inclinação (+ preocupado, − bravo) · `lb` pálpebra de baixo (olho sorrindo) · `mw/mc/mo/mv` boca (largura, curva, abertura, tremida) · `wk` piscadinha · `es` escala dos olhos.
Troca rápida de 4–5 caras com pulinho = gag "olha minhas caras".

## Mãos (`HK`)
`nada, acena, aponta_cima, aponta_esq, aponta_dir, joinha, ombros, nega, aponta_si, comemora, pega`. Formas: `h-open`, `h-point`, `h-thumb` (o `#hR` é cópia espelhada do `#hL`). Pose nova = novo `case` em `poseOf()`.

## Olhar (`GK`)
`[t, x, y]` de −10 a 10. Conteúdo em cima → `[t, 0, -9]`. Olhar pra câmera → `[t, 0, 0]`.

## Os 5 mascotes (`MASCOTES`)
| id | nome | olhos | detalhe animado |
|---|---|---|---|
| `boo` | BOO | 2 escuros | flutua, barra ondulando (`booPath`) |
| `tela` | TELA | 2 de luz na tela | linhas de scan |
| `mochi` | MOCHI | 2 escuros com brilho | amassa 1,9× mais, bochecha no acento |
| `astro` | ASTRO | 2 de luz na viseira | luz do peito pulsa com a voz |
| `orbita` | ÓRBITA | 1 olho-lente | íris gira e "foca" |

## Criar um 6º mascote
Adicione uma entrada em `MASCOTES`:
```js
meu: { pivo: 160, sombra: 200, face: 'escuro' /* ou 'luz' */, olhos: [[-50, -20], [50, -20]], r: [20, 28],
  bocaY: 40, bocaE: 0.5, ant: [0, -150] /* pivô da antena */, amassa: 1, flutua: false,
  svg: `<g id="ant">...antena...</g> ...corpo com fill="${G('gw')}" e brilho ${G('shine')}... <g id="FACE"></g>` },
```
- Coordenadas da cabeça com centro (0,0), ~300 px de largura. `pivo` = base (onde amassa); `sombra` = y da sombra.
- Corpo branco com `gw`, partes cinza com `gg`, tela/viseira com `visor`, brilho por cima com `shine`.
- O `<g id="FACE"></g>` marca onde entram olhos e boca. Antena dentro de `<g id="ant">`.
- Desenhe primeiro numa ficha (`references/estilos/fontes/mascotes.html`) e mostre ao usuário antes de animar.
