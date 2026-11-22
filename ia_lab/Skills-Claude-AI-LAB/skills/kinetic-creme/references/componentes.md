# Kinetic Creme — catálogo de componentes (API do `engine.js`)

Todos os tempos são **absolutos** (segundos do vídeo). `parent` é a cena (`s`) ou o `body` de uma janela. Coordenadas = centro do elemento, canvas 1080×1920, `KC.CX = 495` (centro da área segura).

## Estrutura
```js
function roteiro() {
  const { CX } = KC;
  const cam = KC.setup({ duration: 15, handle: '@seuperfil' });   // fundo + câmera
  let s = KC.scene(cam, 0, 3.4, { out: 'whip' });                // cena 0–3,4 s
  ...
  s = KC.scene(cam, 12.9, 15, { last: true });                    // última cena não sai
}
```
`KC.scene(cam, inicio, fim, { out: 'whip'|'tilt', last, breathe })` — entra sempre pela direita (chicote), sai conforme `out`. Gera cue `whoosh`.

## Texto
| Função | Uso |
|---|---|
| `KC.words(parent, 'Essa *ferramenta*\nfaz *mágica*', { x, y, size, cls, t0, step, letters, align, width })` | Texto palavra a palavra. `*x*` = laranja, `\n` = quebra. `cls`: `'hl'` (título, padrão), `'sub'` (cinza de apoio), `'caps'` (caps espaçadas). `letters:true` = letra a letra. Retorna `{ box, spans, lines, end }`. |
| `KC.captionCard(parent, { x, y, w, spec, t0, step, size })` | Cartão creme com legenda à esquerda (embaixo de janelas). |
| `KC.strikeLines(wordsResult, { t0, gap, dim })` | Risca cada linha do texto e esmaece. Cue `swipe`. |
| `KC.stamp(parent, { x, y, text, rot, t0 })` | Carimbo laranja com impacto + tremida. Cue `impact`. |
| `KC.underline(parent, { x, y, w, t0 })` | Sublinhado laranja que cresce do centro. |
| `KC.glyph(parent, { x, y, text: '{ }', t0 })` | Glifo mono laranja translúcido flutuando. |

## Ícones e conexões
| Função | Uso |
|---|---|
| `KC.tile(parent, { x, y, size, icon, t0, spin, pulses, bare })` | Tile branco com ícone. `icon`: `doc`, `spark`, `play`, `mail`, `q`. `pulses`: tempos de "pulsar". `bare`: sem fundo. |
| `KC.connector(parent, { x1, y1, x2, y2, t0, d, dots })` | Linha laranja que se desenha + bolinhas viajando. |
| `KC.monoChip(parent, { x, y, t0, text })` | Chip mono branco; `text` pode ser função `t => '...'` (contador `1 → ∞`). |
| `KC.pill(parent, { x, y, text, t0, icon: 'check' })` | Pílula branca com ✓ verde. Cue `pop`. |
| `KC.cardBurst(parent, { fx, fy, t0, t1, n, region, hubPulses })` | Miniaturas jorrando de (fx,fy) para uma região `[x0,y0,x1,y1]`. |
| `KC.hubNetwork(parent, { cx, cy, r, n, t0, icon, labels })` | Hub + halo + celulares em rede com linhas e "+N mil" flutuando. |

## Janela escura
```js
const win = KC.windowCard(s, { x: CX, y: 640, w: 820, h: 640, t0, title: '<i>●</i> studio · painel' });
KC.codeTyper(win.body, { t0, cps: 130, until: 6.75, lines: [[['const ', 'k'], ['x', ''], [' = ', 'p'], ['"oi"', 's']]] });
KC.statTile(win.body, { x: 24, y: 22, w: 376, label: 'views', to: 248000, t0, d: 1.1 });
KC.areaChart(win.body, { x: 24, y: 192, w: 772, h: 360, t0, d: 1.2 });
KC.tag(s, { x, y, text: 'em apenas 3 dias', t0, rot: -3 });          // tag laranja
KC.tag(s, { x, y, text: 'feito em código', t0, white: true, icon }); // chip branco
```
Classes de código: `k` laranja (palavra-chave), `s` verde (string), `p` pontuação, `c` comentário. `until` = quando o código some (pra dar lugar ao painel).

## CTA
| Função | Uso |
|---|---|
| `KC.commentBox(parent, { x, y, w, text, t0, cps, pubAt })` | Caixa de comentário digitando → "Publicado ✓" em `pubAt`. |
| `KC.dmToast(parent, { x, y, w, label, html, t0 })` | Rótulo mono + barra laranja de DM. Cue `ding`. |

## Utilidades pra criar componentes novos
`KC.el(tag, cls, parent, html)`, `KC.svg(tag, attrs, parent)`, `KC.put(e, x, y)` (centra), `KC.tf(e, { x, y, s, r, o, b, rx, sx })` (aplica transformação/opacidade/desfoque), `KC.popIn(e, t0)` (retorna função de entrada padrão), `KC.on(t => ...)` (atualizador por quadro), `KC.prog(t, a, d, KC.Ease.outExpo)`, `KC.cue(t, tipo, ganhoDb)`, `KC.shake(t, amp, dur)`, `KC.thumbHTML(rng, 'photo'|'ui'|'dark')`.

Regra: todo estado visual deve ser **função de t** (nada de `setTimeout`/animação CSS) — senão o render quadro a quadro não bate com a prévia.

## Ainda não implementados (vistos na referência — criar quando a copy pedir)
- **Selo "?"**: `KC.tile(..., { icon: 'q' })` com fundo laranja (`e.style.background = 'linear-gradient(#FF8E2E,#EA6511)'`, ícone em branco).
- **Barras comparativas**: dentro de `windowCard`, divs com `height` animado por `outExpo`; barra herói laranja, demais cinza `#4A4541`, rótulos 22 px embaixo.
- **Mockup de editor** (timeline + waveform + preview): janela escura com tiras coloridas e um mini-frame do próprio vídeo.
