---
name: diario-experimento
description: Edita Reels/TikTok/Shorts verticais no estilo "Diário de Experimento" — série/episódio ("DIA 06/30", "EP 01") com palco quase preto e brilho colorido de fundo, selo + barra de progresso + @ no topo, títulos condensados em caixa alta com a palavra-chave colorida e subtítulo itálico, palavras que sobem desfocando→nítido, vídeos/prints em cartões arredondados que entram em chicote com desfoque de movimento, números grandes com contador, cronômetros e barras em cartões de vidro, calendário 3D com o dia aceso, bateria enchendo, rabisco à mão com seta, chips "✓", ícone ✓/✗, CTA (seguir, curtir, comentar digitando a palavra, DM) e legenda palavra a palavra com sublinhado colorido. 6 paletas (lima padrão AI LAB, elétrico, âmbar, violeta, ciano, rosa) ou cor livre. Tudo por código (Python/PIL + ffmpeg), render paralelo, som automático. Use quando o usuário pedir "estilo diário/série de dias", "DIA X de 30", "estilo do reel do notebook velho", "edit com fundo preto e brilho, números grandes e calendário", "experimento do dia", ou mandar locução/vídeos/prints pra virar um episódio de série.
---

# Diário de Experimento

Formato de **série** (dia N de 30, EP 01, parte 2): cada vídeo mostra um experimento/resultado com **material real** (gravação de tela, render, print, vídeo de celular) sobre um **palco escuro com brilho da cor da marca**, e cada fala vira um **objeto gráfico** (número, cronômetro, barra, calendário, bateria, rabisco, chip). Visual limpo, premium, sem moldura chamativa: o material real é a estrela.

Exemplo: `exemplos/EP01_exemplo.mp4` (roteiro em `exemplos/roteiro_EP01.py`), paletas em `exemplos/paletas.jpg`.

<!-- catalogo -->
## 🧭 Aluno perdido? Mostre o catálogo
Se o usuário não souber qual estilo quer, mande **https://skills-claude-ailab.pages.dev/** e siga a skill `escolher-estilo`. Nunca comece a produzir sem saber o estilo.

<!-- safe-zone-v2 -->
## ⚠️ Safe zone — OBRIGATÓRIO
Leia `safe-zone/SAFE-ZONE.md`. Canvas 1080×1920: **topo** livre até y 240 · **base** a partir de y 1500 · **laterais** 95 px · **botões** x ≥ 870 de y 800 a 1500. Nesta skill: barra de progresso em y 252, selo/@ logo abaixo, títulos a partir de y ≈ 340, legenda em y 1430, nada essencial em x > 870 entre y 800 e 1500 (vídeos podem passar). Antes do render final: `python safe-zone/safe_zone.py checar <prévia.mp4>`.

<!-- marca-dagua -->
## 💧 Marca d'água — OBRIGATÓRIO
`python marca-dagua/marca_dagua.py status` antes; se NAO CONFIGURADA, perguntar (@, logo ou nenhuma). Último passo: `python marca-dagua/marca_dagua.py aplicar <sem_marca.mp4> <final.mp4>`. Capa sem marca.

<!-- ganchos -->
## 🎣 Gancho — OBRIGATÓRIO
Leia `ganchos/GANCHOS.md`. Quadro 0 já com título grande e o material mais forte (no exemplo: 3 vídeos reais em leque, título com `t0` negativo pra estar visível no quadro 0). Algo muda na tela a cada 2–3 s. Escrever 3 ganchos e escolher o mais forte.

## O que pedir (só o que faltar)
1. **Material**: vídeos/prints/renders do experimento (procure nas pastas do usuário antes de pedir) e a **locução** (vídeo falado, áudio, ou texto pra gerar voz).
2. **Série**: texto do selo (`DIA 06/30`, `EP 01`, `PARTE 2`), total do calendário e o @.
3. **Cor**: paleta (`lima` padrão, `eletrico`, `ambar`, `violeta`, `ciano`, `rosa`) ou um RGB livre. Na dúvida, mostrar `exemplos/paletas.jpg` (ou gerar a folha com o material dele: `python scripts/paletas.py roteiro.py folha.jpg 3.6,15.6`).
4. **CTA**: palavra do comentário e o que vai ser mandado — não inventar promessa.

## Pipeline
0. **Requisitos (1º uso)**: Python 3.10+ com `python -m pip install pillow numpy imageio-ffmpeg faster-whisper` (confira com `python -c "import PIL, numpy, imageio_ffmpeg"` e instale só o que faltar). Não precisa de Node, Blender nem GPU.
1. **Projeto**: pasta nova do usuário (ex.: `Videos-Claude\NN-slug`). Copiar `exemplos/roteiro_EP01.py` como `roteiro.py`. Os scripts ficam na skill (o roteiro aponta pra `~/.claude/skills/diario-experimento/scripts`).
2. **Voz**: se for gerada, ElevenLabs com a voz do usuário (modelo `eleven_v4`, speed ~1.08). Se vier de vídeo, extrair o áudio. Vídeo de iPhone HDR → tonemap antes.
3. **Transcrever**: `python scripts/transcrever.py fonte/voz.mp3 fonte/palavras.json` (faster-whisper, CPU int8). Corrigir grafias no `fix=` de `grupos_legenda` (ex.: "Clod."→"Claude.").
4. **Roteiro** (`roteiro.py`): `CFG` (dur, paleta, selo, handle, voz, `sem_legenda` nos trechos com título grande), `GRUPOS` (legenda) e a lista `EL` de elementos com tempos tirados de `palavras.json`. Cada fala = um elemento; ver tabela abaixo e `references/elementos.md`.
5. **Conferir quadros**: `python scripts/render.py roteiro.py folha.jpg --stills 0,1.5,3.2,...` (1–3 s). Ler a folha, corrigir sobreposição, buraco sem nada na tela e texto ilegível. Repetir.
6. **Som**: `python scripts/mix.py roteiro.py mix.wav` — automático: pop por palavra de título, ROCK + whoosh nas entradas de vídeo, catraca nos contadores, cascata no calendário, cliques na digitação, obturador nos flashes, tique em cada grupo da legenda; voz ~5 dB acima do bus de SFX. Ajuste fino com `CUES_EXTRA = [(t, "rockin", -6), ...]` no roteiro. Biblioteca do usuário via `sfx_pasta.txt`; sem biblioteca, sons gerados por código. Se a biblioteca estiver configurada e mesmo assim aparecer "usando efeitos gerados por código", confira o caminho no `sfx_pasta.txt`.
7. **Render**: `python scripts/render.py roteiro.py final_sem_marca.mp4 --proc 28 --audio mix.wav` (multiprocesso; ~25 s pra 20 s de vídeo no 7950X).
8. **Marca d'água** → final. **Capa**: quadro do gancho (`ffmpeg -ss 0.7 -frames:v 1`). Entregar MP4 + capa + folha de quadros e explicar cada trecho.

## Fala → elemento
| Fala | Elemento (`tipo`) | Dica |
|---|---|---|
| frase de impacto / nome do assunto | `titulo` (`txt` com `*destaque*`, `sub` itálico) | 1–2 linhas, ≤ 4 palavras por linha |
| número/especificação ("4 GB", "64 GB") | `numeros` (lado a lado, `rot` embaixo, `de`+`conta` pra contador) | entra exatamente na palavra falada |
| comparação | `barras` (cartão de vidro, `destaque` na linha que importa) | |
| tempo/velocidade, A × B | `timer` (2 pílulas, `conta_de`/`conta_ate`, `cor` bom/ruim) | junto com 2 clipes empilhados |
| "dia 6 de 30", série | `calendario` (`total`, `dia`, `cols`) + `titulo` "DIA *06*" | abrir/fechar o vídeo com ele (loop) |
| antes → depois | `bateria` (`de`, `ate`, `rot_de`, `rot_ate`) ou `icone` ✗ → ✓ | |
| comentário pessoal | `rabisco` (letra à mão, `*destaque*`, seta) | |
| "funciona", "real", característica | `chip` (vidro + ✓) | |
| deu erro / deu certo | `icone` (`ok=False/True`) | |
| mostrar o material | `clip` (`cartao`, `palco` = bordas somem no escuro, `cheio` = tela toda) / `imagem` | entradas `sobe`/`lado`/`zoom`, saídas `sobe`/`some` |
| transição forte | `flash` + `tremor` | no número-soco |
| CTA | `titulo` "COMENTA *PALAVRA*" + `comentar` (digita) + `dm`; ou `seguir` + `curtir` | |

## Regras de estilo
- Uma cor de acento só (paleta). Branco no resto; cinza pros rótulos. Nunca duas cores de destaque na mesma tela (exceto ruim/bom do semáforo).
- Título: fonte condensada (Anton/Bebas se instaladas, senão Impact), caixa alta; palavra-chave em acento; subtítulo serif itálico cinza-claro.
- Tudo entra animado (sobe + desfoque→nítido, pop com overshoot, chicote com desfoque de movimento) e sai desfocando/subindo. Nada linear, nada parado > 2–3 s.
- Legenda: 2–3 palavras, branca, Poppins Bold, palavra-chave sublinhada em acento; esconder (`sem_legenda`) quando o título já diz a mesma coisa.
- Vídeo em cartão com cantos 34 px, borda branca sutil, sombra e aura da cor do acento.

## Arquivos
- `scripts/dx.py` — motor: paletas, fundo, topo, legenda e todos os elementos (`TIPOS`). Novo elemento = função com `@tipo("nome")`.
- `scripts/render.py` — render paralelo + folha de quadros. `scripts/mix.py` — som automático. `scripts/paletas.py` — folha com todas as cores.
- `scripts/transcrever.py`, `ambiente.py`, `sfx_lib.py`, `sfx_synth.py` — apoio.
- `references/elementos.md` — parâmetros de cada elemento.
- `assets/fonts/` — Poppins, JetBrains Mono, Permanent Marker (OFL).
