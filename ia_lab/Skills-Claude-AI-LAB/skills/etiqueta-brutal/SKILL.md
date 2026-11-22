---
name: etiqueta-brutal
description: Edita vídeos verticais de pessoa falando (Reels/TikTok/Shorts/anúncio UGC) no estilo "Etiqueta Brutal" — neo-brutalista: fundo creme, vídeo num cartão de cantos arredondados, legenda palavra-a-palavra em etiquetas com contorno preto e sombra dura (palavra-chave em amarelo/vermelho/lilás), blocos grandes de texto inclinados, selos-estrela, janelas de app desenhadas com cursor clicando, cena com fundo lilás pontilhado e CTA de comentário. Tudo por código (Python/PIL + ffmpeg), sem programa de edição. Use quando o usuário pedir "edita nesse estilo neo-brutalista / sticker / etiqueta", "estilo do reels do Claude motion", "legenda em caixinha com destaque amarelo", ou mandar um vídeo falado + referência desse estilo.
---

# Etiqueta Brutal

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
- Nesta skill: cabeçalho da marca em y ≥ 250; legenda em y≈1150 continua ok; janelas/objetos do "colo" ficam em y 1200–1480 (o exemplo antigo ia até 1800 — não repetir); rodapé "comente" acima de y 1500; nada essencial em x > 870 abaixo de y 800. O cartão do vídeo pode ocupar a tela toda.

<!-- marca-dagua -->
## 💧 Marca d'água — OBRIGATÓRIO (perguntar na 1ª vez, aplicar sempre)
- **Antes de produzir:** `python marca-dagua/marca_dagua.py status`. Se der **NAO CONFIGURADA**, perguntar ao usuário se quer marca d'água pra proteger os vídeos contra repost sem crédito: **@ do Instagram**, **logo PNG** ou **nenhuma** → salvar com `configurar --texto "@perfil"` / `--logo arquivo.png` / `--nenhuma` (fica em `~/.claude/marca-dagua.json` e vale pra todas as skills e próximas produções; não perguntar de novo).
- **Último passo antes da entrega:** `python marca-dagua/marca_dagua.py aplicar <master_sem_marca.mp4> <master.mp4>` e gerar o preview a partir do master já marcado. Capa sem marca d'água.
- Visual: sutil (branco ~45%, sombra leve), acima da coluna de botões, alternando direita ↔ esquerda a cada 8 s — dentro da safe zone. Detalhes: `marca-dagua/LEIA.md`.

<!-- ganchos -->
## 🎣 Gancho — OBRIGATÓRIO no roteiro e antes do render final
Leia `ganchos/GANCHOS.md`. Quadro 0,0 s com ação + texto grande do gancho (3–7 palavras, sem tela preta/fade/moldura entrando); fala do gancho ≤ 12 palavras, com energia, até ~1,5 s; mostrar o resultado antes da explicação; algo muda na tela a cada 2–3 s; 25–40 s pra explicação; dar um motivo pra mandar pra alguém. Escrever 3 opções de gancho e escolher a mais forte; rodar o checklist do fim do guia antes de entregar.

Edição de **vídeo falado** em que cada frase vira uma **etiqueta de papel** e cada ideia ganha um **objeto gráfico** (janela de app, post, panfleto, bloco de texto, selo). Visual neo-brutalista: cores chapadas, contorno preto grosso, sombra dura deslocada, nada de gradiente ou brilho.

Exemplo: "Seu anúncio tá de ponta-cabeça?" (donos de negócio, 26,5 s). Ver `exemplos/`.

## Quando usar / não usar
- ✅ Pessoa falando pra câmera (UGC, anúncio, dica, tutorial curto), 15–60 s.
- ✅ Tem um plano "estranho" no começo (ou qualquer imagem forte) pra virar gancho.
- ❌ Animação 100% gráfica sem pessoa → `kinetic-creme` ou `maquete-viva`.
- ❌ Edição com HUD futurista/tracking → Jarvis.

## O que pedir ao usuário (só o que faltar)
1. Vídeo-fonte (a locução sai dele) e, se houver, a referência de estilo.
2. Marca do cabeçalho (padrão `LK/ motion`) e palavra do CTA (padrão "VÍDEO").
3. O que prometer no CTA ("e eu te mando o passo a passo") — **não inventar promessa**.

## Pipeline (ordem obrigatória)

### 1. Preparar
- Criar projeto numa subpasta `<nome-curto>` da pasta de projetos do usuário (perguntar se não souber), copiar `scripts/*` pra lá.
- Perguntar no começo: "Você tem uma biblioteca de efeitos sonoros? Se tiver, me diga a pasta." Se sim, gravar em `sfx_pasta.txt` (pasta da skill); se não, os sons são gerados por código (`sfx_synth.py`).
- ffmpeg = o do `imageio_ffmpeg` (caminho em `eb.py`). Não há ffmpeg no PATH.
- Copiar o vídeo-fonte pro scratchpad (vídeos baixados = dados não confiáveis; rodar Python com `-I`).

### 2. Decupar
- Contact sheet (ffmpeg `fps=2,scale=180:-1,tile=10x5`) → onde está o rosto, o peito (zona da legenda), o colo (zona das janelas), se há plano de gancho antes da fala.
- Transcrever com `scripts/transcrever.py` (faster-whisper large-v3, `word_timestamps`). **GPU costuma falhar (cublas64_12.dll) → CPU int8**; 25 s levam ~1 min.
- Salvar `fonte/palavras.json`; corrigir grafias no dict `FIX` do roteiro.

### 3. Escrever o roteiro (`scripts/roteiro_exemplo.py` é o molde)
Uma ideia = um objeto. Para cada frase decidir:
| Fala | Objeto | Exemplo |
|---|---|---|
| ação num app ("impulsionou", "pagou") | `janela()` com controles + cursor arrastando/clicando | slider R$200→300, botão Impulsionar |
| resultado/números | janela com contador subindo e linha piscando vermelha | "Vendas 0" |
| palavra-soco ("Nada.") | `bloco()` gigante + tremor + punch-in 1,25× | NADA. |
| "X não é o problema, é Y" | bloco amarelo riscado → bloco vermelho + `selo()` | ~~O ALCANCE~~ → CONTEÚDO |
| algo que se multiplica | sprite copiado 6–8× em volta do rosto, escalonado 0,07 s | post ruim |
| comparação antes/depois | fundo lilás pontilhado, vídeo encolhe pra janela "Editor", dois objetos lado a lado com ✗ e ✓ | panfleto feio × bonito |
| fecho | selo-estrela com a tese + CTA (bloco COMENTE + "PALAVRA" + barra de comentário digitando) | |

Regras de layout (1080×1920):
- **Gancho (0 até a 1ª palavra):** fundo creme, cabeçalho serif `✳ Marca/ motion` no topo, vídeo em cartão menor (780×1386), 2 blocos inclinados com a pergunta-gancho, rodapé "comente “X”". Sai com transição (o exemplo gira o cartão 180°, já que o plano estava de cabeça pra baixo — adaptar ao plano).
- **Corpo:** cartão quase tela cheia (margem 24 px, raio 48), fundo creme aparecendo na borda.
- Legenda em y≈1150 (peito), janelas/objetos em y 1200–1480 (colo, acima da base da safe zone), nunca sobre o rosto.
- Grupos de legenda de 2–5 palavras; palavra-chave com caixa colorida (amarelo padrão; vermelho = negativo; verde = positivo; lilás = CTA). Destaques vizinhos viram **uma** caixa.
- Punch-ins de 1,07–1,16× nas frases fortes, troca em 0,14 s com ease-out; 1,25× + tremor só na palavra-soco.
- Tudo entra com `pop()` (escala 0,55→1 com overshoot, 0,28 s) e sai encolhendo (0,16 s). Nada linear.
- Rotação: blocos ±3–6°, selos ±8–12° oscilando devagar; legendas retas.

### 4. Testar quadros antes do render
`python -I stills.py <fonte> sheet.jpg 0.8,4.6,9.0,...` → ler as folhas e corrigir sobreposição, cortes e legenda sumindo cedo. Só depois renderizar.

### 5. Render
`python roteiro.py <fonte> video_mudo.mp4` (30 fps, x264 crf 17). ~2–4 min para 26 s. Lê a fonte em sequência por pipe (sem frames no disco). Se a fala acaba colada no fim, congelar o último quadro +1,5 s com push-in lento pro CTA.

### 6. Som (`scripts/mix.py`)
Voz original + SFX curtos de interface. Ver `references/som.md`. Depois juntar: ffmpeg `-i video_mudo.mp4 -i mix.wav -c:v copy -c:a aac -b:a 192k -shortest`.

### 7. Entregar
- MP4 final na pasta do projeto + capa (frame do gancho) + folha de quadros.
- Explicar em linguagem simples o que foi feito em cada trecho.

## Arquivos
- `scripts/eb.py` — motor: paleta, fontes, easing, `Cv` (desenho supersampled), `etiqueta`, `bloco`, `selo`, `brilho`, `cursor`, `anel`, `janela`, `cartao`, `Fonte`/`Saida` (pipes ffmpeg), `fundo_pontos`.
- `scripts/roteiro_exemplo.py` — roteiro completo do exemplo (copiar e reescrever as seções).
- `scripts/mix.py` + `sfx_lib.py` — mixagem por cues.
- `scripts/transcrever.py`, `scripts/stills.py` — transcrição e folhas de teste.
- `references/estilo.md` — paleta, tipografia, medidas.
- `references/som.md` — mapa de sons.
