# Elementos (`EL` do roteiro)

Todo elemento tem `tipo`, `t0` (entra) e quase todos `t1` (sai; sem `t1` fica até o fim). `t0` negativo = já está na tela no quadro 0.
Texto com `*palavra*` sai na cor de acento (pontuação colada também: `*RENDER*?`).

| tipo | parâmetros principais |
|---|---|
| `titulo` | `txt` ("LINHA 1\nLINHA *2*"), `sub`, `y` (topo, padrão 350), `size` (118), `stagger` (0.07), `fonte` ("titulo") |
| `texto` | `txt`, `y`, `size` (40), `fonte` ("bold") |
| `numeros` | `y` (centro), `size` (150), `gap`, `itens=[dict(v="4 GB", rot="MEMÓRIA", t=2.6, de=0, conta=0.6, cor="branco"/"acento"/"bom"/"ruim")]` |
| `timer` | `rot` ("WINDOWS"), `valor` (s), `conta_de`, `conta_ate`, `cor`, `x`, `y`, `cor_sempre` |
| `barras` | `x`, `y`, `w`, `linhas=[dict(rot, val, frac 0..1, destaque)]` |
| `calendario` | `total` (30), `dia`, `cols` (6), `y` (centro), `escala`, `rot` (-4), `t_press` |
| `bateria` | `cx`, `y`, `de`, `ate` (0..1), `enche_de`, `enche_ate`, `rot_de` ("2h30"), `rot_ate` ("8h36") |
| `rabisco` | `txt` (com `\n` e `*`), `cx`, `y`, `size` (52), `rot` (3), `escreve` (s), `seta` |
| `chip` | `txt`, `x`/`cx`, `y`, `fonte` ("mao" ou "bold"), `size`, `check` |
| `icone` | `ok` (True ✓ / False ✗), `cx`, `y`, `r` |
| `clip` | `src`, `ini` (s no arquivo), `modo` ("cartao"/"palco"/"cheio"), `larg`, `alt`, `cx`, `cy`, `rot`, `zoom=(1,1.06)`, `foco=(0.5,0.5)`, `entrada` ("sobe"/"desce"/"lado"/"zoom"/"some"/"corte"), `saida` (idem), `vel`, `escurecer` (0..1), `aura`, `sombra`, `r` |
| `imagem` | `src` (png/jpg), `larg`, `cx`, `cy`, `rot`, `r` |
| `seguir` | `avatar` (png) ou `iniciais`, `handle`, `r`, `y`, `t_ok` |
| `curtir` | `cx`, `y`, `size`, `t_ok` |
| `comentar` | `palavra`, `t_digita`, `y`, `w` |
| `dm` | `handle`, `avatar`/`iniciais`, `msg`, `y`, `w` |
| `flash` | `dur` (0.2), `forca` (0.35), `cor` ("acento"/"branco") |
| `tremor` | `dur` (0.3), `amp` (18) |

Ordem da lista = ordem das camadas (clipes primeiro, textos depois). O topo (barra/selo/@) e a legenda são desenhados por cima de tudo.

## CFG
`dur`, `paleta` (ou `dx.set_paleta("x", acento=(r,g,b))` pra cor livre), `selo` ("DIA 06/30"), `handle`, `voz`, `legenda_y` (1430), `legenda_size` (46), `sem_legenda=[(t0,t1),...]`, `topo` (False esconde), `brilho` (0.40 = força do brilho do fundo).

## Layout que funciona (1080×1920)
- Título em cima (y 340–600), material no meio (cartão 560–640 px de largura, cy ≈ 1000–1060), legenda em 1430.
- Dois clipes comparando (A × B): cartões de 520 px, cy 640 e 1180, cada um com `timer` à esquerda.
- Calendário: escala 1.0 pra 30 dias (6×5), 1.3 pra 10 (5×2); título "DIA *06*" acima e frase de série embaixo.
