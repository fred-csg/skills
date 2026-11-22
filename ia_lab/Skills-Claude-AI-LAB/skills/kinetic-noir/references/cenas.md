# Cenas — o que o template já tem e como reaproveitar

| Elemento (id no template) | Demonstra | Reuso |
|---|---|---|
| Losango gigante + etiqueta (`#kA`, `#tag`) | "isso é um X" — apresentar o herói | trocar por qualquer ícone/forma; etiqueta mono com linha tracejada |
| Timeline com marcações + agulha (`#tline`, `#ticks`, `#ph`) | tempo, sequência, etapas | marcar etapas com losangos; agulha em `E.ioE` |
| Bolinha no trilho (`#ball`, `ballState`) | movimento, antes/depois | idas e voltas com easing trocável (linear, Bézier, mola) |
| Gráfico de curva (`#graph`: `gpath`, alças, `epath`, `varea`) | qualidade, evolução, comparação | linear → S → elástico → gráfico de área |
| Cursor arrastando (`#cursor`, `ctrl()`) | "você ajusta", "é fácil" | cursor vai até o alvo com `E.ioE`, aperta (escala 0,86) e arrasta |
| Palavra grande em passos (`#robo`) | rígido, travado, antigo | tempo quantizado |
| Palavra gelatina (`#elas`) | elástico, divertido, vivo | mola frouxa por letra |
| Barra que revela a palavra (`#bar`, `#trw`) | definição, "isso é…" | clip-path + barra → sublinhado |
| Grade de itens em onda (`#grid`) | quantidade, escala, "nenhum desses" | ripple do centro; trocar losangos por ícones |
| Mão + X carimbado (`#hand`, `#xmark`) | negação, "não precisa", "acabou o manual" | X com mola + tranco |
| Itens colapsando num cartão de código (`#ccard`) | "foi código", automação | itens viajam ao centro e encolhem; código digitando com cores |
| Caixa de comentário + coração (`#cbox`, `#posted`) | CTA "comenta X" | digita a palavra, Publicar fica verde, comentário cai, coração explode |
| Assinatura (`#lock`) | fecho de marca | quadrado verde girando + letras caindo |

## Ideias novas no mesmo idioma (quando o roteiro pedir)
- Número contando com mola (contador que passa do valor e volta).
- Antes/depois: tela dividida que gira em `ry` revelando o verso.
- Lista de etapas como cartões empilhados em profundidade (z diferentes) e a câmera passando por cada um.
- Notificação/celular caindo do topo com quique.
- Palavra que estica até virar uma linha e a linha vira o próximo elemento.
