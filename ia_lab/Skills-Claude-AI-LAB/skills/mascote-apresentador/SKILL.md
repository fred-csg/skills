---
name: mascote-apresentador
description: Cria Reels/TikTok/Shorts verticais em motion graphics "Mascote Apresentador" — um mascote branco (5 personagens à escolha — BOO fantasminha, TELA monitorzinho, MOCHI bolinho, ASTRO capacete, ÓRBITA olho-lente) que APRESENTA o vídeo inteiro e NUNCA sai da tela, sobre fundo escuro com gradiente, spot de luz que segue o mascote e grão; 6 paletas (Tinta+Lima padrão, Noite+Vermelho, Marinho+Âmbar, Petróleo+Coral, Vinho+Ouro, Grafite+Ciano), 4 molduras (Régua padrão, Vidro, Anel, Palco, ou nenhuma) e layouts que variam por cena (centro, do lado, lousa, balão, bento). O mascote fala junto com a voz (boca pelo áudio), troca de cara, aponta, acena, comemora, e faz animações avançadas de explicar — nome caindo letra por letra, ícones orbitando em volta dele, número que vira gráfico, objeto desmontando em vista explodida, antes/depois com slider, caminho enrolado que fica reto, confete com canhões de luz, palavra da legenda que voa pro título. Roteiro em diálogo (você pergunta, o mascote responde). Tudo em HTML/SVG renderizado quadro a quadro, sem créditos de IA no render. Use quando o usuário pedir "estilo do mascote", "vídeo com o Ghost", "bonequinho/mascote apresentando", "robozinho/fantasminha que apresenta o vídeo", "mascote no fundo escuro", ou quiser transformar uma copy/roteiro num vídeo apresentado por mascote.
---

# Mascote Apresentador

## 🎨 Passo 0 — PERGUNTAR O ESTILO, SEMPRE, ANTES DE CRIAR (obrigatório)
Nunca comece um vídeo sem estas respostas. Mostre as referências visuais (mande as imagens de `references/estilos/`) e pergunte, numa mensagem só:

1. **Mascote** → mostrar `references/estilos/v_mascotes.jpg` (renderizado no motor) e `1_mascotes.jpg` (ficha).
   `boo` (BOO, fantasminha — **padrão**) · `tela` (TELA) · `mochi` (MOCHI) · `astro` (ASTRO) · `orbita` (ÓRBITA)
2. **Nome do mascote** (aparece no vídeo e no CTA). Padrão do BOO: **GHOST**.
3. **Paleta** → `v_paletas.jpg` / `3_cores.jpg`.
   `lima` (Tinta + Lima, roxo e verde-limão — **padrão**) · `noite` (Noite + Vermelho) · `marinho` (Marinho + Âmbar) · `petroleo` (Petróleo + Coral) · `vinho` (Vinho + Ouro) · `ciano` (Grafite + Ciano)
4. **Moldura/HUD** → `v_molduras.jpg` / `2_huds.jpg`.
   `regua` (Régua — **padrão**) · `vidro` (cápsulas de vidro) · `anel` (anel em volta do mascote) · `palco` (pedestal + canhão de luz) · `nenhum`
5. **Layouts** → `4_layouts.jpg`. Não é escolha única: o vídeo usa vários, um por cena (centro, do lado, lousa, balão, bento). Pergunte só se o usuário quer priorizar algum.
6. **Nome do episódio** pro HUD (ex.: `EP02 · GHOST`).

As escolhas vão no objeto `ESTILO` no topo do `index.html`. Prévia rápida de qualquer combinação no navegador: `index.html?mascote=astro&hud=anel&paleta=petroleo`.

<!-- safe-zone-v2 -->
## ⚠️ Safe zone — OBRIGATÓRIO antes de produzir o visual
Leia `safe-zone/SAFE-ZONE.md`. Canvas 1080×1920: **topo** livre até y 240 · **base** a partir de y 1500 · **laterais** 95 px · **botões** x ≥ 870 de y 800 a 1500.
- O template já respeita: centro em x 510, conteúdo entre y 370 e 1180, mascote "base" em y 1235, legenda em y 1405 (encolhe sozinha acima de 800 px).
- A moldura (régua, vidro, anel, palco) é decorativa: pode encostar nas linhas.
- Antes do render final: `python safe-zone/safe_zone.py checar <prévia.mp4> --tempos ...`.

<!-- marca-dagua -->
## 💧 Marca d'água — OBRIGATÓRIO (perguntar na 1ª vez, aplicar sempre)
- **Antes de produzir:** `python marca-dagua/marca_dagua.py status`. Se der **NAO CONFIGURADA**, perguntar: **@ do Instagram**, **logo PNG** ou **nenhuma** → `configurar --texto "@perfil"` / `--logo arquivo.png` / `--nenhuma`.
- **Último passo:** `python marca-dagua/marca_dagua.py aplicar <master_sem_marca.mp4> <master.mp4>`.

<!-- ganchos -->
## 🎣 Gancho — OBRIGATÓRIO no roteiro e antes do render final
Leia `ganchos/GANCHOS.md`. Quadro 0 com ação (o mascote nasce de uma explosão de faíscas), primeira fala ≤ 12 palavras, algo muda a cada 2–3 s, 25–35 s no total. Escreva 3 ganchos e escolha o mais forte.

## O que é
Vídeo 9:16 em que **o mascote é o apresentador** e o roteiro é uma **conversa**: o apresentador (voz do usuário, fora da tela) pergunta, e o mascote responde **mostrando**. Cada resposta vira uma animação que demonstra a fala. O mascote fica grande no "palco" nos momentos de personalidade e pequeno quando o conteúdo ocupa a tela, mas nunca some.

Exemplo: `exemplos/ghost_exemplo_38s.mp4` (BOO "GHOST" + Tinta/Lima + Régua). Roteiro em `exemplos/roteiro.txt`, locução em `exemplos/locucao.mp3`. É o `scripts/template.html` renderizado — o template É o exemplo completo.

## Regras do mascote (a alma do estilo)
1. **Nunca sai da tela.** Muda de lugar com mola + pulinho, nunca some.
2. **Reage a toda fala**: cara, gesto ou olhar (`FK`, `HK`, `GK`). Mascote parado = erro.
3. **Olha e aponta pro que está explicando.**
4. **Grande = personalidade** (apresentação, piada, virada, CTA). **Pequeno = conteúdo** (lousa, gráfico, comparação).
5. **Fala junto**: a boca abre só nas falas DELE (`voz_mascote.wav` → `boca.js`). Nas perguntas ele escuta (olha, inclina a cabeça).
6. Personagens são **originais** (todos com a antena de raio ⚡). Pra criar um 6º mascote: `references/mascote.md`.

## Roteiro em diálogo (o formato que funciona)
`P:` = apresentador (voz do usuário), `M:` = mascote. Estrutura do exemplo, que pode ser reaproveitada pra qualquer tema:
**Tom = papo de PARCEIRO** (o Lucas pediu): fala solta, como amigo ("E você faz o quê?", "Bora, mostra aí", "Tá, e eu?"), nunca formal ("E o que que você faz?"). Nada de bordão forçado tipo "eu faço o show". Falas curtas (≤ 8 palavras).
1. **P:** "Ué… e você, quem é?" → nasce da faísca, assustado.
2. **M:** "Prazer… eu sou o [NOME]! Teu novo parceiro de vídeo." → nome cai letra por letra. (Nunca "Prazer, [NOME]!" — soa como se chamasse o apresentador pelo nome.)
3. **P:** "Parceiro? E você faz o quê?" → inclina a cabeça, "?".
4. **M:** "Eu explico qualquer parada. Quer ver?" → ícones orbitando + balão "QUER VER?".
5. **P:** "Bora, mostra aí." → rastreador 01 02 03 04.
6. **M:** 3–4 demonstrações, uma animação avançada diferente cada (`references/cenas.md`).
7. **P:** "Tá, mas como é que funciona?" → "? ?".
8. **M:** explica o processo mostrando: roteiro chega quicando e ele engole → 5 mascotes entram em fila → paleta troca ao vivo → cursor escolhe → tudo é sugado pra dentro dele → barra "montando vídeo".
9. **P:** "Só isso?" / **M:** "Só isso! Você fala, eu transformo em cena." → onda da voz entra nele, grade bento monta, confete.
10. **CTA**: palavra da legenda voa pro título + comentário digitando.
Bounce elástico em tudo (molas com z ≈ 0,4), mascote estica no pulo e amassa no pouso. 35–40 s.

## Pipeline

### 1. Locução em diálogo
- Dois TTS no ElevenLabs (`eleven_v4`, `language pt`): **todas as falas P** num áudio (voz do usuário; Lucas = "LK") e **todas as falas M** em outro. **Voz padrão do mascote = Lax Whisper (`EeTjZnu1OfgjhGKT6ywY`), stability 0.4, style 0.5, speed 1.08, +4,5 semitons no `dialogo.py`** (aprovada pelo Lucas). Falas separadas por linha em branco no texto. Escreva o nome como se pronuncia (ex.: "Gôust") e "iá" em vez de "IA".
- Monte `audio/roteiro.txt` (uma fala por linha, `P:`/`M:`) e rode:
  `python -I scripts/dialogo.py audio/roteiro.txt audio/perguntas.mp3 audio/mascote.mp3 audio 1.30`
  → corta pelas palavras, deixa a voz do mascote +4,5 semitons (personagem) e intercala: `locucao.mp3`, `voz_mascote.wav`, `falas.json`.
- `python -I scripts/boca.py audio/voz_mascote.wav audio/boca.js` (boca só nas falas dele).
- `python -I scripts/palavras.py audio/locucao.mp3 audio/palavras.json "Nome, termos"` → preencher `W` (use os inícios do `falas.json` como âncora de cada fala).
- Mandar a prévia do áudio antes de animar. CTA: se a voz do mascote não é a do usuário, ele fala do usuário em 3ª pessoa ("que o Lucas te manda").

### 2. Montar o projeto
Pasta com: `index.html` (cópia de `scripts/template.html`), `fonts/` (de `scripts/fonts`), `audio/`, `scripts/` (render.mjs, mix-sfx.mjs, mix-final.mjs, dialogo.py, boca.py, palavras.py, gerar_sfx.py, sfx_synth.py, shot.mjs), `package.json` (de `scripts/package.json`) → `npm i`. Frames temporários fora de pastas sincronizadas.

No `index.html`, de cima pra baixo: `ESTILO` (passo 0) → `W` + cortes `S2…S11` → `CAPS` (falas `'P'` ganham a etiqueta VOCÊ) → `MP` (lugares/layouts), `FK` (caras), `HK` (mãos), `GK` (olhar) → cenas (HTML de cada `.sc` + bloco no `render(t)`) → `CH` (capítulos da moldura) → `sfx(...)` + `IMPACTS`.

### 3. Prévia antes do render (obrigatório)
`node scripts/render.mjs stills <pasta> 0.3,2.6,...` (um tempo por fala) → folha de contato (copie para `q_%03d.png` e `ffmpeg -i q_%03d.png -vf "scale=360:-1,tile=8x2" folha.jpg`). Conferir: mascote sempre visível, conteúdo sem encostar nele, legenda dentro da largura, cara certa em cada fala, contraste do acento (acento claro nunca em texto sobre fundo branco — use o acento como fundo e texto escuro). Outra combinação sem editar: `Q="mascote=astro&paleta=noite" node scripts/render.mjs stills ...`.

### 4. Render
`node scripts/render.mjs all <pasta_frames> out/video_mudo.mp4 12 6` (~1 min pra 30 s). Conferir 2–3 trechos em movimento (folha a 10 fps).

### 5. Som (sem trilha)
`node scripts/render.mjs cues out/cues.json` → (sem a biblioteca de sons: `python -I scripts/gerar_sfx.py out/cues.json`) → `node scripts/mix-sfx.mjs out/cues.json out/sfx.wav -16` → `node scripts/mix-final.mjs out/video_mudo.mp4 out/sfx.wav audio/locucao.mp3 out/master_sem_marca.mp4` (voz −15 LUFS, SFX −23 LUFS, master −14). SFX da COMPILED SELECTIONS (pops do Reel Sumama = pop principal) + **construção** `m_build1`/`m_build` (família 'Dry Break Impact' da Cinematic Stone, o som favorito do Lucas) em todo elemento que se monta — curtos, nada contínuo/ambiência. Ids em `references/som.md`. Trilha só se pedirem.

### 6. Entrega
Marca d'água → master + `_celular` (crf 23, ≤ 30 MB).

## Armadilhas já resolvidas
- `pop()` reescreve `transform`/`opacity` a cada quadro: efeitos extras vão DEPOIS dele no `render(t)`.
- Moldura `palco` e `anel` ficam ATRÁS do mascote (vão pro `#back`); `regua` e `vidro` ficam por cima de tudo.
- Ícones da órbita trocam de camada (`#back` ↔ `#front`) conforme passam atrás/na frente dele.
- Pálpebras são `clipPath`: funcionam em qualquer mascote, com 1 ou 2 olhos, olho escuro ou de luz.
- Rótulo da régua some 1,5 s depois de cada capítulo pra não brigar com os cards.
- `dialogo.py` corta pelas palavras: o texto do `roteiro.txt` tem que bater com o que foi falado (mesmo número de palavras por fala).
- Caminhos no Git Bash: passe `C:/...` pro node. Fontes locais (`fonts/`).
