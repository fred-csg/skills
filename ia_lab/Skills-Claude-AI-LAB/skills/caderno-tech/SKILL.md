---
name: caderno-tech
description: Edita Reels/TikTok/Shorts verticais de LISTA NUMERADA no estilo "Caderno Tech" — "troca 1 / 09", "5 ferramentas que…", "X que tem versão grátis", "no lugar de A, use B" — com cenas alternando azul-noite (grade fina + brilho) e papel quadriculado, a cena nova SOBE por cima como uma folha, cabeçalho mono "// troca 1 ······ STATUS #01", título que aparece palavra a palavra junto com a fala (sans pesada + palavra-chave em serif itálico colorida), número-fantasma gigante no fundo, cartão "de" (ícone, nome, preço) que apaga e cartão "para" branco (ícone, nome, descrição, rodapé mono, selo ★), carimbo inclinado ("US$ 0", "GRÁTIS"), recibo com total contando e riscado, onda de áudio, contador grande, grade de chips, busca digitando, comentário + seguir e DM com checklist. 6 paletas (cobalto padrão, lima AI LAB, laranja, vinho, floresta, violeta) ou cor livre. Tudo por código (Python/PIL + ffmpeg), render paralelo, som automático. Use quando o usuário pedir "estilo caderno tech", "lista de ferramentas", "troca 1 de 9", "isso tem versão grátis", "no lugar de X use Y", "ranking/top 5 em motion", "estilo do reel das assinaturas grátis do GitHub", "recibo com total", ou mandar uma copy de lista pra virar Reels.
---

# Caderno Tech

Formato de **lista numerada com troca**: cada item é uma cena (`// troca 3`, `#03 / 09`), o "antes" aparece e apaga, o "depois" entra num cartão branco e um carimbo fecha a ideia. Fundo alterna entre **escuro** (azul-noite com grade e brilho) e **papel** (off-white quadriculado), e a cena nova sobe por cima da anterior como uma folha. Não tem rosto: a voz conduz, o **título é a própria legenda** (aparece palavra a palavra no tempo da fala).

Exemplo: `exemplos/apresentacao.mp4` (roteiro em `exemplos/roteiro_apresentacao.py`), paletas em `exemplos/paletas.jpg`.

<!-- catalogo -->
## 🧭 Aluno perdido? Mostre o catálogo
Se o usuário não souber qual estilo quer, mande **https://skills-claude-ailab.pages.dev/** e siga a skill `escolher-estilo`. Nunca comece a produzir sem saber o estilo.

<!-- safe-zone-v2 -->
## ⚠️ Safe zone — OBRIGATÓRIO
Leia `safe-zone/SAFE-ZONE.md`. Canvas 1080×1920: **topo** livre até y 240 · **base** a partir de y 1500 · **laterais** 95 px · **botões** x ≥ 870 de y 800 a 1500. Nesta skill: cabeçalho em y 250, título a partir de y 330, conteúdo até y ≈ 1480; o número-fantasma pode invadir a base (é decorativo). Carimbos à direita (cx ≈ 760) ficam acima de y 800 ou são decorativos. Antes do render final: `python safe-zone/safe_zone.py checar <prévia.mp4>`.

<!-- marca-dagua -->
## 💧 Marca d'água — OBRIGATÓRIO
`python marca-dagua/marca_dagua.py status` antes; se NAO CONFIGURADA, perguntar (@, logo ou nenhuma). Último passo: `python marca-dagua/marca_dagua.py aplicar <sem_marca.mp4> <final.mp4>`. Capa sem marca.

<!-- ganchos -->
## 🎣 Gancho — OBRIGATÓRIO
Leia `ganchos/GANCHOS.md`. No quadro 0 a primeira troca já está pronta na tela (item apagado + cartão + carimbo, com `t0` negativo) ou o recibo com o total. Título curto e falado em até 1,5 s. Algo muda a cada 2–3 s (cada palavra do título já conta).

## O que pedir (só o que faltar)
1. **A lista**: os itens (de → para), com preço/número de cada um, e **a fonte dos números** (preço do site oficial na data, estrelas do GitHub…). Nunca inventar preço: se não tiver fonte, use "valores de exemplo" na nota do recibo ou tire o preço.
2. **Locução**: áudio/vídeo falado, ou texto pra gerar voz (ElevenLabs com a voz do usuário).
3. **Ícones/material**: logos ou prints (png/jpg). Sem arquivo, o ícone vira letra num quadrado colorido (`"Ab|#1d2330|#ffffff"`).
4. **Paleta**: `cobalto` (padrão), `lima`, `laranja`, `vinho`, `floresta`, `violeta`, ou cor livre (`ct.set_paleta("x", acento=(r,g,b))`).
5. **CTA**: palavra do comentário e o que vai na DM — não prometer o que não existe.

## Pipeline
0. **Requisitos (1º uso)**: Python 3.10+ com `python -m pip install pillow numpy imageio-ffmpeg faster-whisper` (confira com `python -c "import PIL, numpy, imageio_ffmpeg"` e instale só o que faltar). Não precisa de Node, Blender nem GPU.
1. **Projeto**: pasta nova (ex.: `Videos-Claude\NN-slug`). Copiar `exemplos/roteiro_apresentacao.py` como `roteiro.py`.
2. **Voz** (modelo `eleven_v4`, speed ~1.08, `language=pt`) → `fonte/voz.mp3`. Vídeo de iPhone HDR → tonemap antes.
3. **Transcrever**: `python scripts/transcrever.py fonte/voz.mp3 fonte/palavras.json`.
4. **Roteiro**: `CENAS` (t0, fundo `escuro`/`papel`, `rotulo`, `status`, `fantasma`, `prog`) + `EL`. Cada frase falada = `F("texto com *destaque*", t0, t1)` (helper `ct.fala`, acha o tempo de cada palavra sozinho). Cenas alternam escuro/papel a cada item. Tempos de `palavras.json`.
5. **Conferir**: `python scripts/render.py roteiro.py folha.jpg --stills 0,2.4,5.9,...` → ler, corrigir sobreposição (título de 3 linhas empurra o conteúdo: item em y ≥ 650), repetir.
6. **Som**: `python scripts/mix.py roteiro.py mix.wav` — whoosh em cada folha, pop leve em cada palavra do título, swish no apagar, whoosh+pedra no cartão, impacto no carimbo, cliques e catraca no recibo/contador, cascata na grade, cliques na digitação, voz ~5 dB acima. Ajuste: `CUES_EXTRA = [(t, "impact", -6)]`. Biblioteca via `sfx_pasta.txt`.
7. **Render**: `python scripts/render.py roteiro.py final_sem_marca.mp4 --proc 28 --audio mix.wav` (~30 s pra 26 s de vídeo no 7950X).
8. **Marca d'água** → final. **Capa**: quadro da primeira troca completa (`ffmpeg -ss 2.6 -frames:v 1`). Entregar MP4 + capa + folha.

## Fala → elemento
| Fala | Elemento | Dica |
|---|---|---|
| qualquer frase | `fala` (via `F(...)`) | é a legenda; `*palavra*` vira serif itálico colorido; `size` 70–76 |
| "quanto custa tudo" | `recibo` (`linhas`, `total`, `risca`, `total_final`, `nota`) | `risca=t` risca linha a linha; junte um `carimbo` "GRÁTIS" |
| "no lugar de X" | `item` (`num` "#01 / 09", `nome`, `preco`, `icone`, `apaga`) | `apaga` = quando a troca é falada |
| "…use Y" | `troca` (`nome`, `desc`, `rodape`, `selo` "★ 26,4 mil", `icone`) | entra no nome falado |
| "de graça", "zero" | `carimbo` (`txt`, `cx`, `cy`, `rot`) | 0,3 s depois do cartão |
| voz/áudio/música | `onda` (`titulo`, `rot`) | |
| total/estrelas/número | `contador` (`v`, `pre` "★ ", `suf`, `de`) | vira cor de acento ao terminar |
| resumo de todos | `grade` (`itens=[(icone, txt)]`, `cols`) | |
| "pesquisa o nome" | `busca` (`txt`, `t_digita`) | |
| CTA | `comentar` (`palavra`) + `seguir` + `dm` (`itens`, `tag`) | |
| mostrar material real | `clip` (cartão, `alt` 260 pra faixa larga, `foco`) / `imagem` | |

## Regras de estilo
- Uma cor de acento (paleta). No escuro a palavra-chave usa o tom **claro** do acento; no papel, a **tinta**. Cartões são sempre brancos.
- Título alinhado à esquerda, nunca centralizado; sem legenda separada.
- Cada cena tem o próprio cabeçalho (`rotulo` + `status`) e número-fantasma (o número do item, "R$", "GUIA").
- Toda troca: item aparece → apaga quando o "para" é falado → cartão sobe com desfoque → carimbo bate.
- Números de preço/estrela sempre com fonte e data na legenda do post.

## Arquivos
- `scripts/ct.py` — motor (paletas, fundos, folha, cabeçalho, todos os elementos). `scripts/dx.py` — base comum (texto, clipe, vidro, easing).
- `scripts/render.py` (render paralelo + folha), `scripts/mix.py` (som), `scripts/paletas.py` (folha com as 6 cores).
- `references/elementos.md` — parâmetros de cada elemento.
- `assets/fonts/` — Inter ExtraBold, Instrument Serif Italic, Poppins, JetBrains Mono (OFL).
