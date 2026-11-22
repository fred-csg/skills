---
name: escolher-estilo
description: Guia pra escolher o estilo de vídeo certo entre as Skills Claude AI LAB (Jarvis, Kinetic Creme, Kinetic Noir, Etiqueta Brutal, Moldura Pop, Maquete Viva, Manifesto Feed, Hand Drawing, Mascote Apresentador, Esquadrão Voxel, Diário de Experimento, Caderno Tech, Lápis Vivo). Sempre mostra o catálogo com os vídeos de exemplo (https://skills-claude-ailab.pages.dev/) e ajuda o usuário a decidir pelo material que ele tem e pelo tipo de vídeo que quer. Use quando o usuário acabou de instalar, estiver perdido ou indeciso, ou perguntar "qual skill eu uso?", "que vídeos dá pra fazer?", "por onde eu começo?", "quais estilos tem?", "me ajuda a escolher", "quero fazer um vídeo" sem dizer o estilo, ou mandar um vídeo/copy/tema sem dizer o que quer.
---

# Escolher o estilo de vídeo

O usuário quase sempre é editor ou criador de conteúdo, **não programador**. Fale simples, sem termos técnicos, e decida junto com ele em poucas perguntas.

## 1. Sempre mostre o catálogo primeiro

Comece mandando o link e dizendo o que tem lá:

> Dá uma olhada no catálogo com os vídeos de exemplo de cada estilo: **https://skills-claude-ailab.pages.dev/**
> Clica em qualquer vídeo pra ver ele maior, com o que entra, o que sai e o pedido pronto pra copiar e colar aqui.

Se o usuário já viu o catálogo e escolheu, pule direto pra skill escolhida.

## 2. Faça no máximo 2 perguntas

1. **O que você tem em mãos?** Um vídeo seu falando pra câmera, uma copy/roteiro (texto), ou só o tema/ideia?
2. **Pra que é o vídeo?** Reels/TikTok de conteúdo, anúncio, explicação de um conceito, tutorial…

Se ele já mandou o material (arquivo de vídeo, texto), não pergunte o óbvio: deduza e confirme em uma frase.

## 3. Recomende 1 estilo (no máximo 2 opções)

| O usuário tem… | E quer… | Recomende | Skill |
|---|---|---|---|
| vídeo falando pra câmera | motion premium com HUD, cards e tracking | **Jarvis · Motion com tracking** | `skill-do-jarvis` |
| vídeo falando | só uma legenda bonita presa ao rosto | **Jarvis · Legenda com tracking** | `skill-do-jarvis` |
| takes brutos / gravação longa | cortar silêncios, gaguejos e montar | **Jarvis · Edição + cortes** | `skill-do-jarvis` |
| vídeo explicando um processo/ferramenta | telas e interfaces mostrando cada etapa | **Jarvis · HUD tutorial de IA** | `skill-do-jarvis` |
| vídeo falando (busto, parado) | ele numa moldura com a cabeça saindo, letterings e cartões | **Moldura Pop** | `moldura-pop` |
| vídeo falando (UGC, anúncio) | visual neo-brutalista: etiquetas, selos, janelas de app | **Etiqueta Brutal** | `etiqueta-brutal` |
| uma copy/roteiro em texto | Reels de texto animado com cartões de interface | **Kinetic Creme** | `kinetic-creme` |
| uma copy/roteiro em texto | motion escuro e energético: cada frase demonstrada na tela, câmera 3D que orbita e atravessa as palavras | **Kinetic Noir · Câmera 3D elástica** | `kinetic-noir` |
| um tema/roteiro (com ou sem voz) | um mascote fofo apresentando o vídeo num papo engraçado (pergunta e resposta), mostrando tudo com animação | **Mascote Apresentador** | `mascote-apresentador` |
| um texto de opinião/reflexão (ou só o tema) | manifesto em motion escuro: cards de feed, palavras grandes e cenas que se transformam umas nas outras | **Manifesto Feed** | `manifesto-feed` |
| uma copy/roteiro (com ou sem locução gravada) | uma mão desenhando a copy em quadro branco ou lousa: letra manuscrita, desenhos traço a traço, prints colados | **Hand Drawing · papel, lousa verde ou lousa preta** | `hand-drawing` |
| só o tema, sem gravar nada | vídeo 100% motion com roteiro e narração | **Jarvis · Motion do zero** | `skill-do-jarvis` |
| uma ideia pra explicar com analogia | animação 3D de cidade em miniatura | **Maquete Viva** | `maquete-viva` |
| um processo de várias etapas (fluxo, passo a passo, "como funciona") | bonequinhos 3D de bloco fofos (elenco de 19 personagens com função): um trem que leva a ideia por estações, uma fábrica com esteira, ou outro formato | **Esquadrão Voxel** | `esquadrao-voxel` |
| um assunto pra ENSINAR ou resumir (conta, passo a passo, matéria, finanças, comparativo), com locução ou só o tema | aula escrita num caderno: um lápis escreve tudo sozinho numa página que vai rolando, com lista, tabela, conta e a resposta em destaque | **Lápis Vivo · grafite, creme ou quadriculado** | `lapis-vivo` |
| uma LISTA (ferramentas, trocas, ranking, "X que tem versão grátis", "no lugar de A use B") com locução ou texto | lista numerada em motion: cenas azul-noite e papel quadriculado, cartão de antes que apaga, cartão de depois com selo, carimbo "US$ 0", recibo com total | **Caderno Tech** | `caderno-tech` |
| uma série de dias/episódios ("DIA 06/30", "EP 01") com locução e vídeos/prints do experimento | palco escuro com brilho da cor da marca, números grandes, cronômetro, calendário 3D com o dia aceso, material real em cartões | **Diário de Experimento** | `diario-experimento` |
| uma planta, objeto ou ideia em 3D | cena 3D de vidro/holograma/cromado | **Jarvis · Motion 3D Vidro** | `skill-do-jarvis` |

Explique a recomendação em 1–2 frases ("como você tem um vídeo seu falando e quer algo bem chamativo, o Moldura Pop combina…") e aponte o exemplo no catálogo.

**Avisos de máquina** (diga só quando for o caso): Maquete Viva e Esquadrão Voxel usam o **Blender** (grátis, o Claude instala) e pede um PC mais forte; Moldura Pop baixa um **recorte por IA** de ~1 GB na primeira vez.

## 4. Passe o pedido pronto

Mostre o pedido pronto do estilo (os mesmos do catálogo) e pergunte se pode começar. Com o OK, siga a skill escolhida normalmente.

- **Motion com tracking:** "Use o Jarvis e edite este vídeo com motion: decupe frase por frase, crie um visual para cada ideia (HUD, cards, tracking) e sonorize. Me mostre a prévia antes do render final."
- **Legenda com tracking:** "Use o Jarvis e faça a legenda com tracking neste vídeo: palavra por palavra presa ao rosto, com a palavra-chave grande atrás da cabeça. Gere também o SRT."
- **Edição + cortes:** "Use o Jarvis e monte este vídeo: corte silêncios, gaguejos e repetições, escolha os melhores takes, deixe um gancho forte no início e ajuste na batida da trilha."
- **HUD tutorial de IA:** "Use o Jarvis e edite este tutorial: a cada etapa que eu explico, mostre uma interface de vidro com a imagem correspondente, com tracking e legenda."
- **Motion do zero:** "Use o Jarvis e crie um vídeo 100% motion, sem gravação. Tema: … Público: … 9:16, 45 segundos. Escreva o roteiro e a narração, me mostre antes de animar."
- **Motion 3D Vidro:** "Use o Jarvis e crie uma animação 3D desta planta no material vidro, com câmera passando por cima e sonorização."
- **Kinetic Creme:** "Faz no estilo kinetic creme essa copy: "…". Meu @ é … Destaque em laranja. Me mostre uma prévia de 5 segundos antes do vídeo completo."
- **Kinetic Noir:** "Faz no estilo kinetic noir essa copy: "…". Meu @ é … Câmera bem energética, mudando de lugar a cada frase. Me mostre os quadros-chave antes do vídeo completo."
- **Etiqueta Brutal:** "Edita esse vídeo no estilo etiqueta brutal: legenda palavra por palavra em etiquetas com destaque amarelo, janelas de app com cursor e CTA "comente VÍDEO" no final."
- **Moldura Pop:** "Edita esse vídeo no estilo moldura pop: eu numa moldura com a cabeça saindo pela borda, cor de destaque …, título no topo e um lettering ou cartão para cada ideia. Me mostre os quadros de prévia antes do render final."
- **Manifesto Feed:** "Cria um vídeo no estilo manifesto feed com este texto: "…". Episódio 01, título "…". Cada cena nascendo da anterior, acento coral só no final. Me mostre a prévia antes do render final."
- **Hand Drawing:** "Faz no estilo hand drawing essa copy: "…". Tema lousa preta (ou papel / lousa verde). Uma mão escrevendo cada frase e desenhando o que eu falo. Me mostre os quadros de prévia antes do render final."
- **Mascote Apresentador:** "Faz um vídeo com o mascote sobre …: eu pergunto, ele responde mostrando com animação. Me pergunte antes qual mascote, nome, paleta e moldura, e me mostre a prévia antes do render final."
- **Esquadrão Voxel:** "Faz um vídeo no estilo esquadrão voxel explicando "…" com o elenco de personagens: a ideia viaja num trem e cada estação transforma numa etapa. Me mostre os quadros de prévia antes do render final."
- **Caderno Tech:** "Faz no estilo caderno tech essa lista: "…" (no lugar de A, use B). Paleta cobalto. Recibo com o total no começo e carimbo em cada troca. Me mostre os quadros de prévia antes do render final."
- **Lápis Vivo:** "Faz no estilo lápis vivo uma aula sobre "…" (ou: com esta locução). Tema grafite. Título, enunciado, tabela e a conta com a resposta em verde, e no final o CTA "…". Me mostre os quadros de prévia antes do render final."
- **Diário de Experimento:** "Edita no estilo diário de experimento, paleta lima, selo "DIA …/30": esta é a locução e estes são os vídeos do experimento. Me mostre os quadros de prévia antes do render final."
- **Maquete Viva:** "Cria um vídeo explicativo no estilo maquete viva com este roteiro: … Use a cidade em miniatura como analogia, com chips de capítulo e legenda karaokê."

## 5. Se ele continuar em dúvida

Sugira começar pelo **Moldura Pop** (se tiver vídeo falando) ou pelo **Kinetic Creme**, **Hand Drawing**, **Caderno Tech** ou **Lápis Vivo** (se tiver só texto; o Caderno Tech se for uma lista, o Lápis Vivo se for pra ensinar um assunto): são os mais rápidos pra ver resultado. Depois do primeiro vídeo pronto, ofereça testar outro estilo com o mesmo material.
