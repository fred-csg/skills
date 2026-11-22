---
name: moldura-pop
description: Edita vídeos verticais de pessoa parada falando pra câmera (Reels/TikTok/Shorts, explicação, notícia, dica) no estilo "Moldura Pop" — o vídeo é recortado numa moldura arredondada com contorno colorido brilhante e a CABEÇA DA PESSOA SAI POR CIMA DA BORDA (recorte por IA quadro a quadro); em cima e nos lados entram letterings premium (título bold + serif itálico condensado), pílulas com brilho, cartões de interface, janelas de vidro com contador, avatar em círculo, tela cheia com pílula, fundo alternando claro pontilhado / escuro (grid cinza, cinza granulado, grid azul, azul granulado ou brilho, escolhido na hora), legenda palavra-a-palavra desfoque→nítido com destaques coloridos e em serif CAIXA ALTA, e SFX sutis. Tudo por código (Python/PIL + ffmpeg + BiRefNet), sem programa de edição. Use quando o usuário pedir "moldura com a cabeça saindo", "estilo do vídeo da Cloudflare/Security Audit", "edição com a pessoa na moldura e motion em cima", "letterings e cartões explicando o que eu falo", ou mandar um vídeo falado + referência desse estilo.
---

# Moldura Pop

<!-- catalogo -->
## 🧭 Aluno perdido? Mostre o catálogo
Se o usuário não souber qual estilo quer, estiver indeciso entre as skills, ou pedir "um vídeo" sem dizer o estilo: mande o catálogo com os exemplos, **https://skills-claude-ailab.pages.dev/**, e ajude a escolher pelo material que ele tem (vídeo falando, copy em texto ou só o tema), seguindo a skill `escolher-estilo`. Se o estilo certo for outro, diga qual e passe o pedido pronto dele. Nunca comece a produzir sem saber o estilo.

<!-- safe-zone-v2 -->
## ⚠️ Safe zone — OBRIGATÓRIO antes de produzir o visual
Antes de posicionar qualquer elemento, leia `safe-zone/SAFE-ZONE.md` (medido nos prints reais do Instagram, out/2026; vale pra TikTok e Shorts) e planeje o layout por ele:
- Canvas 1080×1920: **topo** livre até y 240 · **base** a partir de y 1500 · **laterais** 95 px · **botões** x ≥ 870 de y 800 a 1500.
- **Usar a tela toda:** fundo, cenário e vídeo podem passar das linhas; só o essencial (texto, legenda, números, selos, rosto/objeto explicado) fica inteiro dentro. Não encolher o vídeo.
- **Antes do render final:** `python safe-zone/safe_zone.py checar <prévia.mp4> [--tempos 1,4,8]` → olhar a folha, corrigir o que invadir e repetir. Caixa avulsa: `python safe-zone/safe_zone.py caixa x0 y0 x1 y1`. O master sai sem o overlay.
- Medidas antigas (y 300..1220, x 90..900) estão obsoletas — sempre seguir estas.
- Nesta skill: o `roteiro_exemplo.py` usa posições antigas (header y 172 fica embaixo da barra do app) — ao adaptar use header y≈280, título y≈380, linha serif y≈470; legenda em y≈1420 (caixa termina antes de y 1500); pílulas, cartões e janelas fora da coluna de botões (x > 870 abaixo de y 800). A moldura e o vídeo podem passar das linhas.

<!-- marca-dagua -->
## 💧 Marca d'água — OBRIGATÓRIO (perguntar na 1ª vez, aplicar sempre)
- **Antes de produzir:** `python marca-dagua/marca_dagua.py status`. Se der **NAO CONFIGURADA**, perguntar ao usuário se quer marca d'água pra proteger os vídeos contra repost sem crédito: **@ do Instagram**, **logo PNG** ou **nenhuma** → salvar com `configurar --texto "@perfil"` / `--logo arquivo.png` / `--nenhuma` (fica em `~/.claude/marca-dagua.json` e vale pra todas as skills e próximas produções; não perguntar de novo).
- **Último passo antes da entrega:** `python marca-dagua/marca_dagua.py aplicar <master_sem_marca.mp4> <master.mp4>` e gerar o preview a partir do master já marcado. Capa sem marca d'água.
- Visual: sutil (branco ~45%, sombra leve), acima da coluna de botões, alternando direita ↔ esquerda a cada 8 s — dentro da safe zone. Detalhes: `marca-dagua/LEIA.md`.

<!-- ganchos -->
## 🎣 Gancho — OBRIGATÓRIO no roteiro e antes do render final
Leia `ganchos/GANCHOS.md`. Quadro 0,0 s com ação + texto grande do gancho (3–7 palavras, sem tela preta/fade/moldura entrando); fala do gancho ≤ 12 palavras, com energia, até ~1,5 s; mostrar o resultado antes da explicação; algo muda na tela a cada 2–3 s; 25–40 s pra explicação; dar um motivo pra mandar pra alguém. Escrever 3 opções de gancho e escolher a mais forte; rodar o checklist do fim do guia antes de entregar.

Edição de **vídeo falado** em que a pessoa fica numa **moldura arredondada** (contorno na cor de destaque, com brilho) e a **cabeça vaza pela borda de cima**. O espaço acima e dos lados vira palco: cada frase ganha um **lettering** ou um **objeto de interface** que mostra o que está sendo dito. Visual premium, limpo, com movimento sempre suave (ease in/out, desfoque→nítido, pop com overshoot leve).

Exemplo: "A nova profissão do Peter Parker" (Lucas, 26,9 s). Ver `exemplos/`.

## Quando usar / não usar
- ✅ Pessoa parada falando pra câmera, 15–60 s, enquadramento de busto (cabeça + ombros), sem cortes bruscos de câmera.
- ✅ Assunto que dá pra "mostrar" com UI, números, ícones e palavras-chave (tech, finanças, curiosidade, notícia, dica).
- ❌ Pessoa andando / câmera na mão muito instável → a moldura fica nervosa (use `skill-do-jarvis`).
- ❌ Sem pessoa → `kinetic-creme`. Estilo de etiquetas neo-brutalistas → `etiqueta-brutal`.

## O que pedir ao usuário (só o que faltar)
1. Vídeo-fonte (a voz sai dele) e, se houver, a referência.
2. **Visual (tema de cores e fontes) e estilo do fundo escuro**, ver o passo 0.1. Pergunte sempre que o pedido não disser quais.
3. Texto do CTA final (palavra pra comentar + frase da pílula). **Não inventar promessa** ("te mando o link") — se o vídeo não promete nada, use pergunta/engajamento.

## Pipeline (ordem obrigatória)

### 0. Primeiro uso (só uma vez por computador)
1. Rodar `python -I scripts/instalar.py --checar` com o Python da skill (venv abaixo). Ele diz o que já está pronto e o que falta, sem instalar nada.
2. Se faltar algo, **avisar o usuário em uma frase e pedir um "ok"** antes de instalar, dizendo o tamanho:
   - bibliotecas (Pillow, numpy, faster-whisper, imageio-ffmpeg, onnxruntime): ~300 MB;
   - com placa NVIDIA, o recorte na GPU baixa também as bibliotecas CUDA: **~2 GB a mais**;
   - modelo de recorte BiRefNet-portrait (licença MIT, fonte oficial: releases do rembg no GitHub): **~973 MB**. Se o pacote já trouxer o arquivo em `moldura-pop/modelos/birefnet-portrait.onnx`, não baixa nada.
3. Criar um venv só da skill e instalar: `python -m venv ~/.moldura-pop-venv` → `~/.moldura-pop-venv/Scripts/python -I scripts/instalar.py` (Mac: `~/.moldura-pop-venv/bin/python`). Python 3.10 a 3.13. Sem Python, instalar o 3.12 (Windows `winget install -e --id Python.Python.3.12`; Mac `brew install python@3.12`).
4. O instalador termina dizendo onde o recorte vai rodar. **Placa NVIDIA** = ~3 min de recorte para 25 s de vídeo. **Sem NVIDIA (AMD, Intel, Mac)** = ~7 s por quadro (~1 h 30 para 27 s): avisar o usuário antes de começar e sugerir deixar rodando.
5. Fontes: usa a Cera Pro se estiver instalada; senão a Poppins que vem em `scripts/fontes/`; senão Segoe UI / Arial do sistema. Ícones usam a fonte de ícones do Windows; no Mac viram um ponto (avisar).

### 0.1 Escolher o visual (perguntar antes de começar o vídeo)
Se o pedido não disser o visual, pergunte (AskUserQuestion) com estas 4 opções:

| Opção | Quando o usuário diz | Como aplicar |
|---|---|---|
| **Clássico (padrão aprovado)** | "o padrão", "o de sempre", "igual o do Peter Parker", ou não quer escolher | `MP_TEMA=classico` (é o padrão; sem `tema.json` já sai assim). Papel claro pontilhado + fundo escuro escolhido abaixo, Cera Pro + Georgia itálico (sem Cera Pro instalada, usa a Poppins que vem junto). Cor de destaque: vermelho `#E8302A`, ou a da marca/assunto com `MP_ACC=#RRGGBB`. |
| **Preto AI LAB / Higgsfield** | "preto", "estilo Higgsfield", "AI LAB", "igual os Reels do AI LAB" | `MP_TEMA=ai-lab`. Tudo preto `#050505`, verde-limão `#D7FF3A`, texto quase branco, cartões de vidro escuro, Poppins + JetBrains Mono (fontes já em `scripts/fontes/`). |
| **Pela referência (print)** | manda um print, layout, site ou identidade visual pra seguir | Salvar a imagem e rodar `python -I tema_da_referencia.py ref.png tema.json`: fundo, texto e destaque saem da imagem. Ajustar o JSON se precisar (`--fundo claro\|escuro`, `--acc #RRGGBB`). |
| **Combinar com o vídeo** | "faz combinando com o vídeo", "nas cores do vídeo" | `python -I tema_da_referencia.py <video> tema.json` (lê ~24 quadros). O destaque vem da cor mais viva do cenário/roupa e o fundo segue o tom do vídeo. |

**Depois, pergunte o estilo do fundo escuro** (a não ser que o pedido já diga). Mostre antes a folha `exemplos/amostra_fundos_escuros.jpg` (ou gere de novo, já na cor de destaque escolhida: `python -I mp.py fundos fundos.jpg`) e pergunte com AskUserQuestion:

| Opção | Visual | Valor |
|---|---|---|
| **Grid cinza** (recomendado) | cinza grafite granulado + grade fina de planta técnica + luz atrás da moldura | `grid-cinza` |
| **Cinza granulado** | fundo de estúdio cinza, luz atrás da moldura, grão de filme | `cinza-grao` |
| **Grid azul** | azul-tinta + grade + luz azul no topo e um toque da cor de destaque no canto | `grid-azul` |
| **Azul granulado** | azul com manchas de luz desfocadas (azul, roxo e a cor de destaque), sem grade | `azul-grao` |

Pelo "Outro" a pessoa também pode pedir **Cinza + azul** (`cinza-azul`: grade cinza com luz azul por cima) ou o **Brilho original** (`brilho`: quase preto com brilho da cor de destaque no topo; é o que sai se nada for escolhido). Os cartões e janelas das cenas escuras já ganham o vidro na cor certa de cada estilo.
- Como aplicar: `"fundo_escuro": "grid-cinza"` no `tema.json` (vale pro projeto todo) ou a variável `MP_FUNDO=grid-cinza`. Funciona com qualquer tema: no `classico` muda as cenas `dark` (as `light` continuam no papel claro pontilhado); no `ai-lab` muda as cenas `dark` e as `light` continuam pretas com pontinhos.

- O tema vale para o projeto inteiro: `tema.json` na pasta do projeto (o `mp.py` acha sozinho) ou a variável `MP_TEMA` (nome ou caminho do `.json`). Campos aceitos: `base` (`classico`/`ai-lab`), `escuro`, `fundo_escuro`, `acc`, `acc2`, `paper`, `dark`, `glass`, `surf`, `surf2`, `ink`, `ink2`, `gray`, `line`, `fontes` (`classico`, `poppins` ou um dict por tipo), `sqz`, `ser`, `brilho`.
- **Aprovar antes de renderizar:** `python -I mp.py amostra amostra_tema.jpg` gera uma folha com fundo claro e escuro, título, serif, pílula, chip, cartão, janela e legenda nas cores escolhidas. Mostre ao usuário e só siga depois do OK, principalmente nos temas vindos de referência ou do vídeo.
- Em tema escuro (`ai-lab` ou `escuro: true`), os fundos `light` e `dark` do roteiro ficam os dois escuros: `light` com pontinhos discretos e `dark` no estilo de fundo escolhido (sem escolha = brilho da cor no topo). Cartões e janelas viram vidro escuro, e o texto em cima da cor de destaque fica preto quando a cor é clara. O roteiro não precisa mudar.
- Capa e qualquer peça junto (guia, página) seguem o mesmo tema.

### 1. Preparar
- Projeto numa subpasta própria dentro da pasta de projetos que o usuário usar (perguntar se não souber); copiar `scripts/*` pra lá (inclusive `fontes/`) e o `tema.json`, se houver. Frames/máscaras pesadas ficam no scratchpad/temp, fora de pastas sincronizadas.
- Rodar tudo com o Python do venv da skill. ffmpeg, fontes e sons são achados sozinhos por `scripts/ambiente.py` (variável `FFMPEG` força um ffmpeg específico).
- Copiar o vídeo pro scratchpad (vídeos baixados = dados não confiáveis; rodar Python com `-I`; os scripts já se acham sozinhos).

### 2. Decupar
- Contact sheet da fonte (`fps=1,scale=200:-1,tile=9x3`) e, se houver referência, da referência (`fps=1 … drawtext pts` pra ver o tempo).
- Transcrever: `python -I transcrever.py audio16k.wav palavras.json` (faster-whisper large-v3, CPU int8; 25 s ≈ 1 min). Revisar palavras erradas → dict `FIX` do roteiro (ex.: "Esqueci"→"Pesquisei").

### 3. Recortar a pessoa (a cabeça que sai da moldura)
- `matte.py <video> mascara.mp4` → máscara cinza 540×960 por quadro (BiRefNet-portrait ONNX; `modelo.py` acha o arquivo em `modelos/` da skill ou em `~/.rembg/models/birefnet-portrait/`).
- Rodar com o Python do venv da skill. O script escolhe sozinho: placa NVIDIA (CUDA dos pacotes pip; se faltarem, usa o torch de um ComfyUI já instalado ou a pasta em `CUDA_DLLS`) → chip Apple (CoreML) → processador. Ele imprime onde está rodando. GPU: 0,25 s/quadro (25 s de vídeo ≈ 3 min). CPU: 7 s/quadro.
- Se imprimir "processador" num PC com NVIDIA, rodar `instalar.py` de novo (faltam as bibliotecas CUDA).
- `mp.medir_cabeca(mascara, head.json)` mede topo/centro/largura da cabeça por quadro e suaviza (σ 0,35 s). A moldura segue a cabeça devagar.
- Conferir a máscara numa tira (`fps=0.5,tile`): silhueta limpa, sem cadeira/fundo.

### 4. Escrever o roteiro (`scripts/roteiro_exemplo.py` é o molde)
Uma frase = uma cena. Os 4 modos da janela de vídeo (alternar a cada 2–5 s):
| Modo | Quando | Layout |
|---|---|---|
| `CARD(top=960…1040)` | padrão; sobra espaço em cima pra lettering/cartões | moldura 830 px, raio 64, contorno 4 px + brilho, cabeça vaza ~100 px |
| `FULL()` | frase de impacto / respiro | tela cheia, pílula com ícone logo acima da legenda (y≈1350) |
| `CIRCLE(cx, cy, r=140–150)` | quando o visual precisa da tela toda (grade, janela, lista) | avatar redondo num canto de cima + título ao lado |
| fundo `light` / `dark` | alternar pra marcar mudança de assunto | claro = papel pontilhado; escuro = o estilo escolhido no passo 0.1 (grid cinza, cinza granulado, grid azul, azul granulado, cinza + azul ou brilho original) |

Objetos (`mp.py`; `header`, `strike`, `dots`, `grade`, `contador`, `barra`, `quarto`, `comenta` estão no roteiro de exemplo — copie e adapte):
| Fala | Objeto | Exemplo |
|---|---|---|
| abertura / tema | `header(ícone, CAIXA ALTA espaçada, serif itálico)` + título `black` 100 px com 1 palavra na cor + linha serif itálica | HOMEM-ARANHA *novo filme* / a **nova** profissão |
| "um em cada X", "uma cena" | fileira de 5 bolinhas com ícone, uma acende | `dots()` |
| personagem / item citado | `badge(ícone)` girado ±9° dos lados da cabeça, flutuando | câmera vermelha + ? preto |
| o que deixou de ser | `pill()` grande com brilho + `strike()` riscando + `chip()` explicando | ~~FOTÓGRAFO~~ |
| muitas pessoas/itens mudando | `grade()` de ladrilhos que viram ? em cascata | todo mundo esqueceu |
| quem/o quê em destaque | `card(..., theme="dark", extra=status())` | Peter Parker · esquecido |
| herança, preço, comparação | `card()` brancos lado a lado + `status("R$ 0", ok=False)` | Homem de Ferro / tia May |
| número | `glass_window()` + contador subindo + barra enchendo + brilho no fim | R$ 15.000/mês |
| "pequeno/encolheu" | caixa que encolhe trocando o rótulo | quarto → cubículo |
| lugar/objeto visual | ilustração desenhada em código (ex.: `bricks()` com janelas) + pílula branca | apê de tijolinho |
| CTA | caixa "COMENTA" digitando a palavra + pílula preta com ícone send | QUAL PROFISSÃO? |

Regras de layout (1080×1920):
- Lettering do topo (safe zone v2): header y≈280, título y≈380, linha serif y≈470 (o `roteiro_exemplo.py` ainda usa 172/292/400 — ajustar ao adaptar). Nada abaixo de y≈880 em modo CARD (é onde a cabeça vaza).
- **Legenda** em y≈1420 (peito; caixa termina antes de y 1500), 1–4 palavras por grupo; palavras entram uma a uma (desfoque 9→0, sobe 22 px, 0,24 s). Estilos: `n` branco/preto, `acc` cor de destaque com brilho (nomes, números), `ser` serif itálico condensado CAIXA ALTA 1,32× (palavra de impacto: ESQUECER, NADA, CUBÍCULO). Grupo sai 0,13 s antes do próximo (nunca sobrepor).
- Elementos: `El(..., enter="blur"|"pop"|"wipe")`. Título grande = `wipe` (revela da esquerda), objetos = `pop`, textos = `blur`. Saem com desfoque + encolhem 0,22 s no fim da cena.
- Transição entre cenas: moldura e fundo interpolados em 0,44 s (`eio5`), centrados no corte.
- CTA: se a fala acaba colada no fim, congela o último quadro +2 s com push-in de 3,5% (`zoom=`).

### 5. Testar quadros antes do render
`python -I roteiro.py stills <video> <mascara> head.json palavras.json folha.jpg 1.0,2.9,4.0,…` (1 tempo só = quadro em tamanho real). Conferir: cabeça vazando limpo, moldura sem faixa preta, legenda sem sobrepor, nada em cima do rosto.

### 6. Render
`python -I roteiro.py render <video> <mascara> head.json palavras.json video_mudo.mp4` — 29,97 fps, x264 crf 16, fonte lida em 1620×2880 por pipe. ~4–5 min para 27 s.

### 7. Som (`scripts/mix.py`)
Voz original + SFX **sutis** (−14 a −25 dB). Ver `references/som.md`.
- **Perguntar no começo (junto com as outras perguntas):** "Você tem uma biblioteca de efeitos sonoros que quer usar? Se tiver, me diga a pasta." Se sim, gravar o caminho em `sfx_pasta.txt` (na pasta da skill, um caminho por linha), listar os arquivos e trocar os nomes em `mix.py` pelos sons equivalentes dela. Se não, seguir: os sons são **gerados por código** (`sfx_synth.py`), sem baixar nada. Juntar: ffmpeg `-i video_mudo.mp4 -i mix.wav -map 0:v -map 1:a -c:v copy -c:a aac -b:a 192k -shortest`.

### 8. Entregar
MP4 final + capa + folha de quadros na pasta do projeto; explicar em linguagem simples o que acontece em cada trecho e o que foi suposição (palavra corrigida, texto do CTA).

## Arquivos
- `scripts/mp.py` — motor: temas (`TEMAS`: `classico`, `ai-lab`; `tema.json`; `MP_TEMA`/`MP_ACC`), estilos de fundo escuro (`FUNDOS_ESCUROS`, `MP_FUNDO`/`fundo_escuro`), paleta (`ACC`), fontes, `python -I mp.py amostra x.jpg` (folha pra aprovar o tema), `python -I mp.py fundos x.jpg` (folha com os fundos escuros), easing, `text_img` (com tracking e condensação), `glow`, `shadow`, `hstack/vstack`, ícones (Segoe MDL2), `badge`, `pill`, `chip`, `status`, `card`, `glass_window`, `bricks`, `El`, `fundo`, `medir_cabeca`, `CARD/FULL/CIRCLE`, `compor_video` (moldura + cabeça vazando), `Legenda`, `Fonte`/`Saida`, `Cena`/`Edicao`.
- `scripts/roteiro_exemplo.py` — roteiro completo do exemplo (copiar e reescrever cenas/legendas).
- `scripts/tema_da_referencia.py` — lê um print ou um vídeo e propõe o `tema.json` (fundo, texto, destaque). `scripts/fontes/` — Poppins + JetBrains Mono (licença OFL).
- `scripts/instalar.py` — instala bibliotecas, baixa o modelo e testa (`--checar` só mostra o que falta). `scripts/modelo.py` — onde está/baixar o modelo (confere tamanho e MD5). `scripts/ambiente.py` — acha ffmpeg, fontes e a biblioteca de sons.
- `scripts/matte.py` — recorte BiRefNet (NVIDIA → Apple → processador). `scripts/transcrever.py` — palavras com tempo.
- `scripts/mix.py` + `sfx_lib.py` — mixagem por cues (acha os sons por trecho do nome na biblioteca do usuário; sem biblioteca, `sfx_synth.py` gera por código).
- `references/estilo.md` — medidas, cores, tipografia, movimento. `references/som.md` — mapa de sons.
