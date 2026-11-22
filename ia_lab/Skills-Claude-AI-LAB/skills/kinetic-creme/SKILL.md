---
name: kinetic-creme
description: Cria Reels/TikTok/Shorts verticais em motion graphics "Kinetic Creme" — fundo creme com cidade em traço fino, texto que surge palavra por palavra (desfoque→nítido) com destaques em laranja, cartões de interface (ícones ligados por linha, pílulas com ✓, janela escura com código digitando, painel com contadores e gráfico subindo, frase riscada + carimbo laranja, rede de celulares, caixa de comentário + DM) e transições "chicote" com desfoque. Tudo em HTML/JS renderizado quadro a quadro, sem créditos de IA. Use quando o usuário pedir "vídeo estilo creme/laranja", "motion de copy com cards de interface", "no estilo do reels da skill ilimitada", "kinetic typography com UI", ou quiser transformar uma copy/roteiro (com ou sem locução) nesse estilo.
---

# Kinetic Creme

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
- Nesta skill: `KC.CX = 495` continua servindo, mas abaixo de y 800 elementos centrados têm no máximo 750 px de largura (borda direita ≤ 870); nada essencial acima de y 240 nem abaixo de y 1500. Cidade em traço e cards decorativos podem sair da área.

<!-- marca-dagua -->
## 💧 Marca d'água — OBRIGATÓRIO (perguntar na 1ª vez, aplicar sempre)
- **Antes de produzir:** `python marca-dagua/marca_dagua.py status`. Se der **NAO CONFIGURADA**, perguntar ao usuário se quer marca d'água pra proteger os vídeos contra repost sem crédito: **@ do Instagram**, **logo PNG** ou **nenhuma** → salvar com `configurar --texto "@perfil"` / `--logo arquivo.png` / `--nenhuma` (fica em `~/.claude/marca-dagua.json` e vale pra todas as skills e próximas produções; não perguntar de novo).
- **Último passo antes da entrega:** `python marca-dagua/marca_dagua.py aplicar <master_sem_marca.mp4> <master.mp4>` e gerar o preview a partir do master já marcado. Capa sem marca d'água.
- Visual: sutil (branco ~45%, sombra leve), acima da coluna de botões, alternando direita ↔ esquerda a cada 8 s — dentro da safe zone. Detalhes: `marca-dagua/LEIA.md`.

<!-- ganchos -->
## 🎣 Gancho — OBRIGATÓRIO no roteiro e antes do render final
Leia `ganchos/GANCHOS.md`. Quadro 0,0 s com ação + texto grande do gancho (3–7 palavras, sem tela preta/fade/moldura entrando); fala do gancho ≤ 12 palavras, com energia, até ~1,5 s; mostrar o resultado antes da explicação; algo muda na tela a cada 2–3 s; 25–40 s pra explicação; dar um motivo pra mandar pra alguém. Escrever 3 opções de gancho e escolher a mais forte; rodar o checklist do fim do guia antes de entregar.

Vídeo 9:16 em que **a copy é a protagonista**: cada frase aparece palavra por palavra no centro de um fundo creme limpo, e **cartões de interface** ilustram o que está sendo dito (prova, números, objeção, CTA). Estética "produto de tecnologia premium, quente e minimalista". Tudo é código: HTML + JS determinístico → Chromium headless tira um PNG por quadro → ffmpeg.

Exemplo: `exemplos/kinetic-creme_preview_15s.mp4` (copy genérica, mostra todos os componentes). Análise completa da referência: `references/estilo.md`.

## Quando NÃO usar
- Pessoa falando/filmagem real → edição (skill-do-jarvis).
- Animação 3D de cenário/personagens → maquete-viva.

## O que pedir ao usuário (só o que faltar)
1. **Copy/roteiro** (ou tema, e eu escrevo). 15–45 s, frases curtas.
2. **Locução**: áudio pronto (ideal), ou sem voz (só texto + SFX), ou voz por IA (ElevenLabs etc.).
3. **@ do perfil** pra marca d'água discreta (ou nenhuma).
4. Cor de destaque, se não for laranja (trocar `--acc*` em `kc.css`).

## Pipeline

### 1. Roteiro em blocos (beats)
Cada bloco = 1 ideia + 1 componente visual. Estrutura que funciona (a da referência):
| Beat | Duração | Componente típico |
|---|---|---|
| Gancho | 3–4 s | 2 ícones ligados + cards jorrando + título palavra a palavra + 2 pílulas ✓ |
| Virada | 1,5–2 s | caps letra a letra ("DEIXA EU TE MOSTRAR") + palavra gigante + sublinhado |
| Prova | 3–8 s | janela escura: código digitando → painel com contadores + gráfico; legenda em cartão creme embaixo |
| Objeção | 2,5–3 s | frase cinza + frase grande → riscada → carimbo laranja inclinado |
| Escala | 1,5–3 s | hub central + celulares em rede + "+12 mil" flutuando |
| CTA | 2–5 s | "Comenta" + caixa digitando a palavra-chave → Publicado ✓ → DM laranja |
Outros possíveis (ver `references/componentes.md`): selo "?" laranja, gráfico de barras comparativo, mockup de app/editor.

Marque `*palavras*` de destaque (números, nome do produto, a promessa). No máximo 1–2 por frase.

### 2. Tempos
- **Com locução**: transcrever com `faster_whisper` (`medium`, `word_timestamps=True`, `language="pt"`; se a GPU falhar com cublas → `device="cpu", compute_type="int8"`). O `t0` de cada `KC.words` = início da 1ª palavra − 0,05 s; `step` = média entre palavras (ou passe tempos exatos editando `sp._t`). Corte de cena ~0,2 s antes da frase nova.
- **Sem locução**: ~5–6 palavras/s nos títulos (`step` 0,13–0,2), e deixe cada bloco "respirar" 0,6–1 s depois da última palavra.

### 3. Montar o projeto
Criar uma subpasta `<slug>` na pasta de projetos do usuário (perguntar se não souber) e copiar de `scripts/`: `index.html`, `kc.css`, `engine.js`, e `roteiro_exemplo.js` → **`roteiro.js`**. Editar só o `roteiro.js` (e cores no `kc.css`).
- Canvas 1080×1920. **Área segura Reels (obrigatória, v2):** ver `safe-zone/SAFE-ZONE.md` — essencial em y 240..1500, x 95..985 e x ≤ 870 abaixo de y 800 → centro `KC.CX = 495` (abaixo de y 800, largura ≤ 750). Cards decorativos podem sair dessa área.
- Uma cena por beat: `KC.scene(cam, inicio, fim, { out: 'whip' | 'tilt', last })`. Os elementos usam tempos ABSOLUTOS (segundos do vídeo).

### 4. Prévia antes do render (obrigatório)
```
node render.mjs <pasta_projeto> <pasta_saida>/x.mp4 30 --at 0.5,3.2,6,9.5,14
```
Gera PNGs nesses instantes → montar folha de contato com ffmpeg (`tile`) → revisar: sobreposição de texto e cards, elementos fora da área segura, transição no ponto certo, ícone colado em palavra (posicione pela largura real: `wd.box.offsetWidth`). Também dá pra abrir `index.html?t=7.5` no navegador pra congelar um instante, ou sem parâmetro pra ver em loop.

### 5. Render
```
node render.mjs <pasta_projeto> <scratchpad>/video_mudo.mp4 30
```
- ~2,7 quadros/s (15 s ≈ 2min45). Precisa de `npm i playwright-core` na pasta do script (ESM não usa NODE_PATH) e do Chromium do Playwright.
- **Windows:** o `chrome.exe` completo pode dar `spawn UNKNOWN`; o script já prefere o `chromium_headless_shell`. Se o sandbox do Claude Code bloquear, rodar fora do sandbox.
- `FFMPEG` = caminho do ffmpeg (ex.: o do `imageio_ffmpeg`). O render também grava `cues.json` (eventos de som).

### 6. Som (`scripts/mix.py`)
```
python -I mix.py cues.json sfx.wav <duracao> [--voz voz.wav] [--trilha musica.wav]
ffmpeg -i video_mudo.mp4 -i sfx.wav -c:v copy -c:a aac -b:a 192k -shortest video/<nome>.mp4
```
- Os componentes já registram cues: `whoosh` (corte), `pop` (pílula/ícone), `type` (digitação), `tick` (contador), `swipe` (risco), `impact` (carimbo), `click` (publicar), `ding` (DM), `flick` (cards).
- Sons: se a biblioteca de sons do autor existir no computador (caminhos em `mix.py`), usa ela; senão `mix.py` gera cada som por código (`sfx_synth.py`) automaticamente. Perguntar no começo se o usuário tem uma biblioteca própria; se tiver, trocar os caminhos em `SOUNDS` pelos arquivos dele. Nunca riser antes de revelação. Detalhes: `references/som.md`.
- Não dá pra ouvir: avisar que o balanço foi calculado e pedir pro usuário escutar.

### 7. Entregáveis
`video/<nome>_v1.mp4` (+ `_preview.mp4` crf 25 se > 30 MB). Capa = um frame forte (título + componente). Legenda do post honesta sobre as ferramentas.

## Regras de estilo (resumo — detalhes em `references/estilo.md`)
- Nada linear: entradas `outExpo`/`outBack`, saídas `inCubic`. Todo elemento entra com **desfoque + leve subida/escala**.
- Um destaque por vez: no máximo 1 componente "herói" + texto em cada cena.
- Paleta fixa: creme `#ECE3D5`, tinta `#1C1915`, laranja `#F47B20` (gradiente `#FF8E2E→#EA6511`), cinza `#6F665C`, verde ✓ `#1FA463`, janela `#1E1C1A`.
- Tipografia: Inter 800 (títulos, tracking −0,035em), Inter 600 (apoio, cinza), JetBrains Mono (chips, código, rótulos em caps espaçadas).
- O fundo vive: passarinhos e cidade derivam devagar; a cena "respira" (zoom 1→1,025).
- Não copiar a marca/@ do criador da referência nem o logo de terceiros; ícone central é genérico (`spark`, `doc`, `play`, `mail`, `q`).

## Armadilhas já resolvidas
- Emoji não renderiza no headless shell (vira retângulo) → usar SVG inline (envelope, setas `↓`).
- Ícone ao lado de palavra calculado "no olho" invade o texto → posicionar por `offsetWidth`.
- Rede de celulares com stagger longo não completa antes do corte → stagger ≤ 0,1 s e iniciar junto com a cena.
- Celular de baixo da rede encosta no título → hub mais alto (cy ≈ 555, r ≈ 285) e título em y ≈ 1130.
- Fontes: carregar com `document.fonts.load(...)` antes de montar (senão a medição de largura sai errada).
