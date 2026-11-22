# API do roteiro (`roteiro.js`)

```js
LV.config({ tema, duracao, foco, cx, x0, lapisEscala, espiral, cores });
LV.roteiro(({ w, we, p, legendas, legenda, doodles, E, rnd, PAUTA }) => { ... });
```

## config
| chave | padrão | |
|---|---|---|
| `tema` | `'grafite'` | `'grafite'` · `'creme'` · `'quadriculado'` (ou `--q tema=…` no render) |
| `duracao` | fim do último traço + 1,2 s | duração total em s (fim da locução + ~1,5 s) |
| `foco` | `1400` | y da TELA onde a linha atual para (1180 automático se usar `legendas`) |
| `cx` | `520` | centro horizontal dos itens centralizados |
| `x0` | `150` | margem esquerda do texto |
| `lapisEscala` | `1` | tamanho do lápis (0,8–1,2) |
| `espiral` | `true` | `false` tira a espiral da esquerda |
| `cores` | do tema | trocar qualquer cor: `{ amarelo: '#FFB020', verde: '#3DDC97', papel: ['#222', '#1a1a1a'] }` |

## Tempo
- `w('palavra', n=1)` → início da n-ésima ocorrência na locução (ignora acento/pontuação/maiúscula).
  Aceita várias palavras: `w('o que')`. Número falado costuma vir como algarismo: `w('12')`.
- `we('palavra', n=1)` → fim da palavra.
- Todo elemento aceita `at` (início). Texto aceita também `ate` (termina nesse instante).
- Sem `at`: começa logo depois do elemento anterior.
- **Um lápis só:** não sobreponha elementos no tempo.

## Posição
A página tem um cursor `p.y` (linha de base atual, em coordenadas da PÁGINA; a 1ª é 340 e cada pauta tem
`PAUTA` = 92 px). Cada elemento escreve em `p.y` e avança. Pra duas colunas, guarde e volte:
```js
const y0 = p.y;
p.lista(['regra de três', 'porcentagem', 'juros']);
p.y = y0;
p.lista(['média', 'área', 'volume'], { x: 520 });
```
`p.pular(n)` pula n linhas (aceita 0.5). Passar `y` explícito num elemento NÃO move o cursor.
Largura útil: x 150 a 870.

## Texto
Todos devolvem a caixa `{ x0, x1, base, w, h, cx, cy, t0, fim }` (use em `sublinhar/circular/riscar` e `at: caixa.fim`).
`*trecho*` no texto = cor de destaque (`destaque`, padrão amarelo).

| função | padrão |
|---|---|
| `p.titulo(str, op)` | centralizado, 80 px, negrito, branco |
| `p.sub(str, op)` | centralizado, 46 px, cinza |
| `p.linha(str, op)` | à esquerda, 52 px, branco. `centro: true` centraliza (contas) |
| `p.secao(str, op)` | pula uma linha, 66 px, negrito, verde |
| `p.nota(str, op)` | 42 px, cinza (observação) |
| `p.lista([..], op)` | uma `linha` por item; `ats: [t1, t2, …]` dá o tempo de cada um |

Opções de texto: `x`, `y`, `size`, `cor` (`'ink'|'cinza'|'amarelo'|'verde'|'vermelho'|'azul'|'#hex'`),
`destaque`, `at` / `ate`, `dur` (duração total) ou `vel` (s por letra, padrão .05), `ancora`
(`'start'|'middle'|'end'`), `negrito`, `pula` (linhas que avança, padrão 1), `pausa` (folga depois, .22 s).

## p.grade(op) → caixa
Quadradinhos desenhados e pintados um a um: "38 de 45", "12 de 30 dias", "7 em cada 10".
`total`, `cheios`, `cols` (9), `lado` (46), `x`, `cor` ('verde'), `at`, `durGrade` (traçar, .9 s),
`dur` (pintar), `atPinta`, `rotulo` (`'*38* de 45'`, escrito à direita), `atRotulo`.

## p.tabela(linhas, op) → tabela
`linhas = [['gotas', 'quilos'], ['5', '2'], ['30', null]]` — `null` = célula vazia pra preencher depois.
`x` (ou `centro: true`), `colW` (número ou lista; automático pela maior palavra), `alt` (92), `at`,
`durLinhas` (1 s), `cab` (1ª linha colorida, padrão true), `corCab` ('amarelo'), `size` (46),
`tempos` (`[[t, t], [t, t], …]` — o tempo de cada célula; sem isso vão em sequência), `atTexto`, `gap`.
Devolve `{ x0, x1, top, bot, alt, meio(r), cel(r, c, 'texto', op), fim }`:
```js
const t = p.tabela([['', 'dica', '30 pessoas'], ['carne', '250 g cada', null]], { at: w('tabela') });
t.cel(1, 2, '7,5 kg', { at: w('sete'), cor: 'verde' });
```

## p.chave(x, yA, yB, op)
Seta curva lateral de yA até yB com rótulo (o "× 6" ao lado da tabela).
`lado` (`'esq'|'dir'`), `rotulo`, `cor` ('verde'), `barriga` (34), `at`, `dur`.
Uso típico: `p.chave(t.x0 - 24, t.meio(1), t.meio(2), { lado: 'esq', rotulo: '× 6' })`.

## p.seta(x1, y1, x2, y2, op) · p.tracar(d, op)
`seta`: linha com ponta; `curva` = barriga em px (sinal muda o lado), `cor`, `w` (5), `at`, `dur`.
`tracar`: qualquer path SVG (`'M150 900 L600 900'`) desenhado pelo lápis; `cor`, `w`, `at`, `dur` ou `vel` (px/s).

## p.desenho(nome | traços, op) · marcações
Vetores de `doodles.js`: check, xis, setas, brilho, raios, interrogacao, exclamacao, coracao, cifrao, raio,
lampada, alvo, celular, prancheta, lupa, nuvem, boneco, boneco-triste, grupo, cronometro, porta, etiqueta,
trofeu, grafico, balao, presente, carrinho, dinheiro, casa, envelope, cadeado, documento, megafone, relogio,
engrenagem. `x`, `y` (centro), `s` (escala; a caixa do desenho é ~±100), `rot`, `cor`, `w` (5), `at`, `dur`.
Traços próprios: `[{ d: 'M-80 0 L80 0', cor: 'verde' }]` em coordenadas centradas em 0,0.
- `p.sublinhar(caixa, op)` (amarelo) · `p.circular(caixa, op)` (amarelo) · `p.riscar(caixa, op)` (vermelho).

## p.icone(emoji, op)
Emoji que o lápis "pinta" e estoura no lugar. `x` (800), `y` (centro), `size` (120), `at`, `rot`.
Imagem própria: `p.icone('', { src: 'img/logo.png', size: 140 })`.

## p.foto(src, op)
Print/foto colado com fita, entra com "pop". `x`, `y` (centro), `w` (420), `prop` (h/w, .62) ou `h`, `rot`, `at`.
`src` relativo ao projeto (`img/print.png`). Sem `y`, entra abaixo da linha atual e o cursor desce.

## p.cta(linha1, linha2, op)
A página escurece e o lápis escreve a chamada por cima, em coordenadas de TELA (fora dos botões).
`at`, `seta` (`'baixo'` padrão · `'comentario'` aponta pro botão de comentar · `false`), `cor` ('amarelo'),
`y` (905), `size` (124), `size2` (68). Deve ser o ÚLTIMO elemento. `*trecho*` inverte a cor.

## Legenda em pílula (opcional)
O texto escrito já é a legenda; ligue só se a fala disser mais do que está no caderno.
`legendas({ destaques: ['doze'], max: 3 })` (precisa de `words.js`) ou `legenda('TEXTO com *destaque*', t0, t1)`.
