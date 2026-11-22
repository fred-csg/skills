# Prompts pra doodles por IA (vetorizáveis)

Gerar no Higgsfield (`generate_image`, modelo `gpt_image_2_5`, `aspect_ratio: "1:1"`, count 1).
O vetorizador precisa de: **traço preto grosso e uniforme, fundo branco puro, sem sombra/cinza/preenchimento**,
e os detalhes de destaque em **laranja-vermelho** (viram a cor de destaque do tema).

## Modelo
```
Simple hand-drawn whiteboard doodle illustration: <CENA EM INGLÊS, 1 ideia só>.
<DETALHES DE DESTAQUE> drawn in orange-red (#E8452C).
Thick uniform black marker lines (same line width everywhere), clean outlines only, no shading, no fill,
no gray, no text, no background elements, pure white background, centered, explainer video doodle style,
lots of white space around.
```

## Exemplos (da referência)
- Boneco irritado segurando lista longa: `a cartoon stick-figure person with a round head, frowning annoyed face, wearing a t-shirt, holding a very long paper receipt list that unrolls down to the floor` · destaque: `two small circular refresh arrows above the head`.
- Dois vendedores em guerra de preço: `two angry cartoon stick-figure people pulling a price tag in opposite directions, tug of war` · destaque: `the price tag and small impact lines`.
- Fila de lojas iguais: `a long row of identical small market stalls in perspective` · destaque: `the striped awning of the first stall`.
- Pessoa saindo pela porta: `a happy stick-figure person walking out through an open door, leaving a pile of price tags behind` · destaque: `light rays coming from the door`.
- Compradora pensativa: `a cartoon girl with a shopping basket and a thought cloud with two identical product boxes` · destaque: `question marks next to her head and the basket`.
- Mão entregando troféu: `a hand giving a trophy to one smiling price tag among sad price tags` · destaque: `the winning price tag with a down arrow`.

## Dicas
- Uma ação por imagem. Personagem simples (cabeça redonda, corpo de linha/camiseta) — combina com a biblioteca vetorial.
- Evitar texto na imagem (a letra manuscrita vem do motor).
- Se vier com cinza/sombra, pedir de novo com "no shading" reforçado ou usar `--sem-acc` quando não tiver destaque.
- Depois de vetorizar, conferir na prévia: traços demais (> 120) deixam o desenho lento — usar `dur` maior ou simplificar o prompt.
