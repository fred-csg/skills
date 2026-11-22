---
name: kinetic-noir
description: Cria Reels/TikTok/Shorts verticais em motion graphics "Kinetic Noir" — fundo preto com destaque verde-limão (padrão AI LAB), tipografia cinética, elementos de interface que DEMONSTRAM o que a fala diz (keyframes, curvas de animação, timeline, cursor, código, comentário) e câmera 3D elástica que navega pela cena — orbita, mergulha, gira, atravessa as palavras — com rampas de velocidade, molas, arrasto e motion blur real. Tudo em HTML/JS renderizado quadro a quadro (30 fps × 8 subquadros), sem créditos de IA no render. Use quando o usuário pedir "estilo kinetic noir", "motion com câmera 3D", "vídeo estilo keyframes/After Effects feito por código", "animação elástica/fluida como o reel do Claude", "motion de copy no preto e verde", ou quiser transformar uma copy/roteiro (com ou sem locução) nesse estilo.
---

# Kinetic Noir

<!-- catalogo -->
## 🧭 Aluno perdido? Mostre o catálogo
Se o usuário não souber qual estilo quer, estiver indeciso entre as skills, ou pedir "um vídeo" sem dizer o estilo: mande o catálogo com os exemplos, **https://skills-claude-ailab.pages.dev/**, e ajude a escolher pelo material que ele tem (vídeo falando, copy em texto ou só o tema), seguindo a skill `escolher-estilo`. Se o estilo certo for outro, diga qual e passe o pedido pronto dele. Nunca comece a produzir sem saber o estilo.

<!-- safe-zone-v2 -->
## ⚠️ Safe zone — OBRIGATÓRIO antes de produzir o visual
Antes de posicionar qualquer elemento, leia `safe-zone/SAFE-ZONE.md` e planeje o layout por ele:
- Canvas 1080×1920: **topo** livre até y 240 · **base** a partir de y 1500 · **laterais** 95 px · **botões** x ≥ 870 de y 800 a 1500.
- O fundo e os elementos decorativos podem passar das linhas; o essencial (legenda, palavra grande, número, elemento explicado) fica inteiro dentro.
- **Com câmera 3D isso vale pro quadro final, não pra posição no mundo**: confira os quadros de pior caso (câmera girada/aproximada). `python safe-zone/safe_zone.py checar <prévia.mp4> --tempos ...` e corrija os planos (`KEYS`) que empurram texto pra fora.
- Neste template o centro é `CX0 = 495`; as legendas ficam num HUD que segue a câmera só em parte, pra não sair da área.

<!-- marca-dagua -->
## 💧 Marca d'água — OBRIGATÓRIO (perguntar na 1ª vez, aplicar sempre)
- **Antes de produzir:** `python marca-dagua/marca_dagua.py status`. Se der **NAO CONFIGURADA**, perguntar se quer marca d'água: **@ do Instagram**, **logo PNG** ou **nenhuma** → `configurar --texto "@perfil"` / `--logo arquivo.png` / `--nenhuma` (vale pra todas as skills; não perguntar de novo).
- **Último passo antes da entrega:** `python marca-dagua/marca_dagua.py aplicar <master_sem_marca.mp4> <master.mp4>`. Detalhes: `marca-dagua/LEIA.md`.

<!-- ganchos -->
## 🎣 Gancho — OBRIGATÓRIO no roteiro e antes do render final
Leia `ganchos/GANCHOS.md`. Quadro 0,0 s já com ação (o elemento-herói entrando + texto), fala do gancho ≤ 12 palavras até ~1,5 s, algo muda a cada 2–3 s, 20–35 s no total. Escreva 3 ganchos e escolha o mais forte.

## O que é
Vídeo 9:16 em que **cada frase é demonstrada na tela enquanto é dita**: "isso é um keyframe" → um keyframe gigante; "linear é duro" → a bolinha anda dura e a câmera trava em passos; "puxa as alças" → um cursor puxa as alças e a curva muda; "atravessa" → a câmera atravessa a palavra. A câmera é personagem: **muda de lugar a cada frase**.

Exemplo: `exemplos/kinetic-noir_keyframes_31s.mp4` (roteiro "Keyframes", locução `exemplos/locucao_exemplo.mp3`). É o `scripts/template.html` renderizado — o template É o exemplo completo, pronto pra adaptar.

## Quando NÃO usar
- Pessoa falando/filmagem real → skill-do-jarvis / moldura-pop / etiqueta-brutal.
- Fundo claro, cartões de UI calmos → kinetic-creme.
- Cenário 3D de verdade (prédios, bonecos) → maquete-viva.

## O que pedir ao usuário (só o que faltar)
1. **Copy/roteiro** (ou tema, e eu escrevo). 8–12 frases curtas, 20–35 s. **Roteiro original** — se vier uma referência, copiar a linguagem de movimento, nunca o texto/cenas.
2. **Locução**: áudio dele, voz por IA (ElevenLabs) ou sem voz.
3. **@ pra marca d'água** (ver acima) e CTA/palavra-chave do comentário.
4. Cor: padrão preto `#050505` + verde-limão `#D7FF3A` (Poppins). Outra cor → trocar `#D7FF3A`/`215,255,58` no template.

## Pipeline

### 1. Roteiro = demonstração
Para cada frase, escolha **o elemento que prova a frase** e **o plano de câmera** (onde a câmera vai). Tabela no `references/cenas.md` (componentes que o template já tem e ideias novas). Regra: se a frase não tem um elemento que se mexe por causa dela, reescreva a frase ou invente o elemento.

### 2. Locução
- Sem áudio e sem ElevenLabs: faça sem voz (legendas + trilha + SFX) ou peça pro usuário gravar a locução no celular.
- ElevenLabs: modelo `eleven_v4` (o melhor; energia vem da pontuação: MAIÚSCULAS, "!", "..."), `stability 0.35`, `style 0.5`, `similarity 0.8`, `language pt`. Não usar tags `[shouting]` no v4 (só o v3 entende, e o v3 soa pior). Mandar a prévia do áudio pro usuário antes de animar.
- Tempos: `python -I scripts/palavras.py audio/locucao.mp3 audio/palavras.json "termos, técnicos"` → preencher o objeto `W` do template. **Use o fim de cada pausa** como início da frase seguinte (o whisper adianta).

### 3. Montar o projeto
Subpasta `<slug>` na pasta de projetos do usuário (perguntar se não souber) com: `index.html` (cópia de `scripts/template.html`), `fonts/` (cópia de `scripts/fonts`), `audio/`, `scripts/` (render.mjs, mix-sfx.mjs, mix-musica.mjs, gerar_sfx.py, sfx_synth.py) e `package.json` na raiz → `npm i` na raiz do projeto. Frames temporários fora de pastas sincronizadas (Dropbox/OneDrive/iCloud): use a pasta temporária do sistema.

No `index.html` edite, de cima pra baixo:
1. `W` (tempos da fala) e os **marcos/cortes** (`C1…`, sempre relativos a `W`).
2. **Legendas**: `cap(inicio, fim, [[palavras...]])` — palavra de destaque com `'it'` (itálico verde). Máx. ~22 caracteres por linha a 58 px.
3. **Cenas**: HTML dentro de `#world`, cada uma num `.sc` com `show(id, t, ini, fim)`; elementos em camadas `<div class="L" style="transform:translateZ(z)">` (z positivo = mais perto).
4. **Câmera**: lista `KEYS` (um plano por frase) e `TR` (trancos/tremidas/chicote). Guia completo: `references/camera-3d.md`.
5. **SFX**: `sfx(t, id, ganho, pan)` / `whoosh(t, id)` (pico no corte). Ids em `references/som.md`.

### 4. Prévia antes do render (obrigatório)
`node scripts/render.mjs stills <pasta> 0.3,1.2,...` (um tempo por frase + meio de cada transição) → folha de contato com ffmpeg (`tile`; o ffmpeg do Windows não aceita glob, copie para `q_%03d.png`). Conferir: texto cortado na borda em plano aproximado, legenda fora da safe zone, cena vazia depois de travessia, elemento que deveria estar visível. Abrir `index.html` no navegador (sem parâmetro) mostra em loop com áudio ao clicar.

### 5. Render
`node scripts/render.mjs all <pasta_frames> out/video_mudo.mp4 12 8` → 12 processos, 8 subquadros por quadro a 30 fps (obturador 324°, motion blur real). ~1 min por 30 s num PC de 16+ núcleos. Variáveis: `PAGE=outro.html`, `FPS`, `SHUTTER`, `BROWSER=<caminho do chrome/edge>`.

### 6. Som
- `node scripts/render.mjs cues out/cues.json` → (sem a biblioteca de sons: `python -I scripts/gerar_sfx.py out/cues.json` gera cada efeito por código em `sfx/`) → `node scripts/mix-sfx.mjs out/cues.json out/sfx.wav -16`.
- Trilha: a do usuário, ou ElevenLabs `compose_music` instrumental, duração do vídeo + 1 s (ex.: "playful tense minimal electronic motion-design track, rubbery synth bass, clicky glitch percussion, drop around X s").
- `node scripts/mix-musica.mjs out/video_mudo.mp4 out/sfx.wav audio/locucao.mp3 audio/trilha.mp3 out/final.mp4 0.08` (voz −15 LUFS, SFX −24, trilha −28 com ducking, master −14 LUFS).
- Não dá pra ouvir daqui: avisar e pedir pro usuário conferir o balanço.

### 7. Entrega
Master + versão `_celular` (crf 22, ≤ 30 MB) pra mandar no chat. Aplicar marca d'água. Conferir 2 transições em movimento (folha a 8–12 fps) antes de mandar.

## Regras de movimento (o que faz parecer orgânico)
- **Nada parado, nunca.** Toda cena tem deriva de câmera (empurrão/órbita lenta) e algo vivo (onda, pulso, tracking das letras).
- **Um plano de câmera por frase.** Trocou texto/contexto → a câmera vai pra outro lugar (outro alvo, outro ângulo, outra distância).
- **Corte = movimento**: chicote, travessia (atravessar palavra/cartão), zoom girando. Acelera (expo-in), corta no pico, chega com mola.
- **Mola em tudo que entra** (`spr(tau, f, z)`): overshoot e assentamento. Entradas em ~0,25 s.
- **Arrasto**: letras seguem a câmera atrasadas (`tf(el, s, lag)`), uma a uma.
- **Motion blur**: subquadros + desfoque direcional pela velocidade da câmera. 30 fps basta; 60 fps não resolve rigidez.
- Detalhes e números: `references/movimento.md`.

## Armadilhas já resolvidas
- `render.mjs all <frames> <saida> <workers> <sub>` — nessa ordem. Ordem errada = vídeo com metade da duração.
- Nunca mudar `transform` de um elemento que tem `translateZ` de camada: o código sobrescreve. Profundidade vai no wrapper `.L`.
- `overflow:hidden`, `filter` e `clip-path` achatam o 3D dos filhos — use só em elementos sem filhos 3D.
- Travessia: o elemento passa da câmera quando `d` > 1400 − z. Antes de atravessar, não aproxime tanto a ponto de cortar a palavra na borda.
- Depois de uma travessia/corte, a cena nova precisa já ter algo na tela no 1º quadro (não deixar 0,5 s vazio).
- Caminhos no Git Bash: passe `C:/...` para o node (não `/c/...`).
- Fontes locais (`fonts/`) — nada de Google Fonts no render.
