# Elementos (`EL` do roteiro) — caderno-tech

Todo elemento tem `tipo`, `t0` e quase todos `t1` (sem `t1` fica até o fim). `t0` negativo = já na tela no quadro 0.
O elemento pertence à cena em que começa (ou force com `cena=i`). Texto com `*palavra*` = palavra-chave.

| tipo | parâmetros |
|---|---|
| `fala` | criar com `ct.fala(txt, t0, t1, PAL, size=74, y=330, larg=890, adianta=0.10)` |
| `item` | `y` (650), `num` ("#01 / 09"), `nome`, `preco` (chip), `icone`, `apaga` (s) |
| `troca` | `y` (880), `nome`, `desc`, `rodape` (mono), `selo` ("★ 26,4 mil"), `icone`, `larg` |
| `carimbo` | `txt`, `cx`, `cy`, `rot` (-7), `size` (62) |
| `recibo` | `y`, `cab_e`, `cab_d`, `linhas=[dict(rot, val, icone)]`, `stagger`, `total` ("R$ 1.190"), `t_total`, `conta`, `risca`, `total_final` ("R$ 0"), `nota` ("linha1\nlinha2") |
| `onda` | `y`, `titulo` ("VOICESTUDIO · TOCANDO AGORA"), `rot` |
| `contador` | `v` ("351,5"), `pre` ("★ "), `suf` (" mil"), `de`, `conta`, `size`, `y`, `cx` |
| `grade` | `itens=[(icone, txt)]`, `cols`, `y`, `alt_linha`, `icone_s`, `size`, `mono`, `stagger`, `apaga` |
| `busca` | `txt`, `t_digita`, `y` |
| `comentar` | `palavra`, `t_digita`, `y`, `rot` ("Comentários"), `iniciais`/`avatar` |
| `seguir` | `nome`, `sub`, `t_ok`, `y`, `avatar`/`iniciais` |
| `dm` | `itens=[(nome, sub)]`, `tag`, `de`, `stagger`, `y` |
| `clip` / `imagem` | iguais ao dx (`src`, `ini`, `modo` "cartao", `larg`, `alt`, `cx`, `cy`, `foco`, `entrada`, `saida`, `r`) |
| `flash` / `tremor` | `dur`, `forca` / `amp` |

`icone`: caminho de png/jpg (corta quadrado) ou `"Ab|#fundo|#letra"`.

## CENAS
`dict(t0, fundo="escuro"|"papel", rotulo="troca 1", status="#01", fantasma="01", prog=0.45, trans=0.42)` — `prog` = quanto da linha do cabeçalho fica colorida (use o progresso da lista).

## Layout que funciona (1080×1920)
- Cabeçalho y 250 · título y 330 (até 3 linhas de 70 px) · `#NN / NN` y 650 · cartão "de" y 710 · cartão "para" y 880–1116 · carimbo cy 1150 · clipe faixa larga cy 1345 (alt 260).
- Recibo y 620–640 com 3–9 linhas. CTA: comentar 610, seguir 790, DM 940.
- `fantasma`: use letras/números (a fonte serif não tem ★).
