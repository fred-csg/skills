# API do roteiro (`roteiro.js`)

```js
HD.config({ tema, duracao, maoEscala, cx, cores, mao });
HD.roteiro(({ w, we, cena, legendas, legenda, doodles, E, rnd }) => { ... });
```

## config
| chave | padrão | |
|---|---|---|
| `tema` | `'papel'` | `'papel'` · `'lousa-verde'` · `'lousa-preta'` |
| `duracao` | fim da última cena | duração total em s (ponha o fim da locução + ~0,5 s) |
| `maoEscala` | `.56` | tamanho da mão (0,5–0,65) |
| `cx` | `520` | centro horizontal padrão dos itens |
| `cores` | do tema | `{ ink: '#...', acc: '#...' }` pra trocar tinta/destaque |
| `mao` | do tema | forçar `'marcador'` ou `'giz'` |

## Tempo
- `w('palavra', n=1)` → início da n-ésima ocorrência na locução (ignora acento/pontuação/maiúscula).
  Aceita várias palavras: `w('lousa verde')`. Erro claro se não achar.
- `we('palavra', n=1)` → fim da palavra.
- Sem locução: use números em segundos e `legenda('TEXTO com *destaque*', t0, t1)`.

## cena(t0, t1, { zoom = 1.035 })
Cria um quadro novo ao lado do anterior. A câmera chicoteia pra ele começando ~0,19 s antes de `t0`.
Retorna `c` com:

### c.texto(str, op) → caixa
Letra manuscrita escrita letra a letra (a ponta faz zigue-zague em cada letra; a letra é revelada da esquerda pra direita).
- `x` (centro, padrão cx), `y` (linha de base da 1ª linha), `size` (px), `cor` (`'ink'` | `'acc'` | `'#hex'`),
  `at` (início), `dur` (duração TOTAL) **ou** `vel` (s por letra, padrão .062), `linha` (entrelinha, 1.14), `ancora` (`'middle'`|`'start'`).
- `\n` quebra linha. Retorna `{x, y, w, h, fim, linhas:[{x, y, w, h, x0, x1, base}]}` → usar em `circular/sublinhar/riscar` e pra encadear (`at: t.fim`).

### c.desenho(nome | traços, op) → {fim}
- `nome` da biblioteca (`doodles.js`) ou array de traços `[{ d: 'M.. L..', cor: 'acc', fill: true, w: 1.5 }]`
  em coordenadas centradas em 0,0 (caixa ~±100). Ordem do array = ordem que a mão desenha.
- `x, y, s` (escala), `rot` (graus), `cor` padrão, `at`, `dur` (ou `vel` px/s, padrão 950), `w` (espessura px, 7), `params` (array).
- `fill: true` sem stroke = mancha que aparece depois do traço anterior (pontos, olhos).

### c.arte(nome, op) → {fim, x, y, w, h}
Doodle de IA vetorizado (`vetorizar.py`). `x, y` = centro, `w` = largura na tela, `at`, `dur` (ou `vel` px/s, 1500).

### c.foto(src, op) → {x, y, w, h, fim}
Imagem colada com fita, entra com "pop". `src` relativo ao projeto (ex.: `img/print.png`).
`x, y` (centro), `w`, `h` ou `prop` (h/w, 1.25), `rot`, `at`, `borda` (12), `fita` (true).

### Marcações (cor de destaque por padrão)
- `c.circular(caixa, op)` — elipse à mão em volta (passa um pouco do fechamento).
- `c.sublinhar(caixa, op)` — use `{ y: caixa.base + 20 }` pra ficar embaixo do texto.
- `c.riscar(caixa, op)` — risco atravessando (objeção, "não é isso").
Todas aceitam `at`, `dur`, `cor`, `x`, `y`.

## legendas({ destaques, max = 3, maxChars = 17 })
Pílula escura em y 1395 com 2–3 palavras por vez, quebra em pontuação e pausas; palavras em `destaques`
ficam na cor de destaque. Precisa de `words.js`.

## Escrevendo um vetor novo
```js
// dentro do roteiro: traços próprios
const caixa = [{ d: 'M-80 -100 L80 -100 L80 100 L-80 100 Z' }];
c.desenho(caixa, { x: 300, y: 760, at: w('papel'), dur: .3 });
```
Pra entrar na biblioteca: editar `scripts/doodles.js` usando os helpers `L(pts)` (polilinha suavizada com
tremidinha), `elip(cx, cy, rx, ry, {a0, sobra})`, `arco`, `ret(x, y, w, h, r)`, `ponto(cx, cy, r, cor)`, `seta(x1, y1, x2, y2, {curva})`,
`boneco(x, y, s, {feliz})`. Depois rodar `novo_projeto.py` de novo no projeto pra atualizar.
