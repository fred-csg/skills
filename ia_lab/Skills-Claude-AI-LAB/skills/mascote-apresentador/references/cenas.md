# Cenas — animações de explicar (catálogo)

Todas existem no `template.html` (exemplo GHOST). Copie o bloco HTML da `.sc` + o bloco do `render(t)`.

| animação | o que demonstra | layout | onde no template |
|---|---|---|---|
| **Nasce da faísca** — explosão de fagulhas + flash, mascote cresce com mola e leva susto | gancho / entrada | palco | `burst()` + `renderMascote` (intro) |
| **Nome caindo** — letras despencam com mola e giro, subtítulo digitando | apresentação, nome de produto | palco | S1 (`LET`) |
| **Interrogação** — "?" pula girando ao lado da cabeça | pergunta, dúvida | palco | S2 / S9 |
| **Órbita de ícones** — chips giram em volta dele, passando atrás e na frente (profundidade + desfoque) | "qualquer coisa", variedade, ecossistema | palco | S3 (`ORB`) |
| **Rastreador de etapas** — pílula de vidro com 01 02 03 04 acendendo | lista, série, progresso | todos | `#trk` |
| **Número vira gráfico** — número gigante encolhe e voa pro topo da última barra; barras sobem com mola; linha desenha | dado, crescimento, resultado | **lousa** | S5 |
| **Vista explodida** — objeto isométrico se separa em camadas com rótulos e linhas-guia | como funciona por dentro, partes | centro | S6 (`LAY`) |
| **Antes/depois com slider** — rabisco bagunçado × barras organizadas, slider varre + cronômetro | comparação, transformação, velocidade | **do lado** | S7 |
| **Caminho que desenrola** — trilha enrolada se desenha com etapas pipocando e fica RETA no "sem enrolar" | passo a passo, método, simplificar | centro | S8 (`CURVY`→`STRAIGHT`) |
| **Objeto voando pra mão** — documento faz arco e entra nas mãos dele | entrega, envio, "você manda" | palco/balão | S10 (`#doc`) |
| **Balão + show** — balão de quadrinho com tarja de acento, confete e canhões de luz | clímax, payoff | **balão** | S10 + `confetti()` + `drawSpot` |
| **Palavra da legenda vira título** — a palavra-chave sai da legenda e sobe pro título do CTA | CTA, palavra-chave | base | S11 (`CAP_NOME`) |
| **Comentário digitando + resposta** | CTA | base | S11 (`#inp`, `#rpl`) |

## Ideias pra próximas cenas (mesma linguagem)
- **Bento montando**: blocos de uma grade entram um a um, o mascote "liga" cada bloco com um toque (layout bento).
- **Lupa**: o olho do mascote (ou uma lente) passa sobre um card e revela o detalhe ampliado.
- **Balança**: dois pratos com ícones, o lado certo desce com mola (decisão, comparação).
- **Funil**: ícones caem num funil e saem como 1 resultado (filtro, conversão).
- **Linha do tempo puxada**: o mascote puxa uma fita que vai revelando datas/etapas.
- **Clones**: 2–3 cópias pequenas do mascote seguram plaquinhas (opções, perfis).

## Regras
- Uma animação diferente por demonstração; nunca repetir a mesma 2× seguidas.
- Tudo entra com mola (`pop`, `spr`) e sai encolhendo/desfocando; nada linear.
- Todo elemento que entra tem um SFX baixinho.
- Acento claro (lima, âmbar, ciano) nunca como texto sobre fundo branco: vira tarja com texto escuro.
