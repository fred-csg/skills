---
name: maquete-viva
description: Cria vídeos explicativos verticais (Reels/TikTok/Shorts) em 3D "maquete viva" premium — cidade/cenário em miniatura feito por código no Blender (Cycles, luz HDRI, quinas arredondadas, desfoque de miniatura), prédio "casa de boneca" aberto mostrando os andares, modelos prontos (Kenney CC0), bonequinhos de bloco, câmera de cinema, placas de capítulo em 3D, barra de etapas, cartões de interface (celular de app, notificação, checklist), legenda karaokê, locução/trilha/SFX no ElevenLabs e CTA padrão com as redes do usuário. Use quando o usuário pedir um vídeo explicativo/analogia em 3D, "motion 3D estilo maquete", "estilo do prédio da Nike / architectural microcosm", "no estilo do vídeo da rua que virou feed", "estilo raiox/low-poly", ou quiser transformar um roteiro em animação 3D didática.
---

# Maquete Viva (padrão premium, out/2026)

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
- Nesta skill: barra de etapas e títulos em y ≥ 250; placas 3D e callouts presos a objetos com a caixa INTEIRA dentro (inclusive no overshoot); legenda karaokê padrão y≈1150 (pode descer até 1470); CTA e cartão de redes acima de y 1500; trechos com vídeo real em moldura vão até y≈1490 com largura ~840. A cidade/cenário 3D ocupa a tela toda.

<!-- marca-dagua -->
## 💧 Marca d'água — OBRIGATÓRIO (perguntar na 1ª vez, aplicar sempre)
- **Antes de produzir:** `python marca-dagua/marca_dagua.py status`. Se der **NAO CONFIGURADA**, perguntar ao usuário se quer marca d'água pra proteger os vídeos contra repost sem crédito: **@ do Instagram**, **logo PNG** ou **nenhuma** → salvar com `configurar --texto "@perfil"` / `--logo arquivo.png` / `--nenhuma` (fica em `~/.claude/marca-dagua.json` e vale pra todas as skills e próximas produções; não perguntar de novo).
- **Último passo antes da entrega:** `python marca-dagua/marca_dagua.py aplicar <master_sem_marca.mp4> <master.mp4>` e gerar o preview a partir do master já marcado. Capa sem marca d'água.
- Visual: sutil (branco ~45%, sombra leve), acima da coluna de botões, alternando direita ↔ esquerda a cada 8 s — dentro da safe zone. Detalhes: `marca-dagua/LEIA.md`.

<!-- ganchos -->
## 🎣 Gancho — OBRIGATÓRIO no roteiro e antes do render final
Leia `ganchos/GANCHOS.md`. Quadro 0,0 s com ação + texto grande do gancho (3–7 palavras, sem tela preta/fade/moldura entrando); fala do gancho ≤ 12 palavras, com energia, até ~1,5 s; mostrar o resultado antes da explicação; algo muda na tela a cada 2–3 s; 25–40 s pra explicação; dar um motivo pra mandar pra alguém. Escrever 3 opções de gancho e escolher a mais forte; rodar o checklist do fim do guia antes de entregar.

Vídeo explicativo 9:16 em que **uma maquete 3D conta a história** e uma **interface limpa** guia o olhar. Tudo por código: Blender em background + Python + PIL + ffmpeg. Nenhuma janela de programa é aberta.

Referências:
- `exemplos/premium-costureira/` — **padrão atual**: abre na cidade, câmera mergulha no 1º andar de um prédio roxo aberto, placas 3D, celular de app, barra de etapas. Rode o exemplo pra ver o resultado.
- `scripts/legado/` + `exemplos/frames_do_video_exemplo.jpg` — 1ª versão ("A rua virou o feed", EEVEE). Só consulta.

## Quando NÃO usar
- Pessoa falando/filmagem real → edição (moldura-pop, etiqueta-brutal, Jarvis).
- Atuação realista, rosto expressivo, humano hiper-realista → vídeo por IA.

## Primeiro uso
1. `python scripts/instalar.py` — instala bibliotecas, confere o Blender 5, baixa os modelos 3D gratuitos (Kenney CC0 + céu HDRI Poly Haven CC0, ~25 MB) e testa 1 quadro.
2. Pergunte as redes do usuário e grave: `python scripts/instalar.py --redes @youtube @instagram @tiktok` ("-" pula uma rede). Elas aparecem nos cartões do CTA final.

## Regras de trabalho
- Explicar em português simples, a cada passo.
- Roteiro primeiro → usuário aprova → só então gera voz/vídeo.
- Cores: sem saturação extra (`grade=None`); o padrão é a cor que sai do Cycles (AgX Punchy).
- CTA no fim de todo vídeo (ver passo 1).
- Movimento sempre com ease in/out; nada linear.

## Pipeline

### 0. Pasta
uma pasta por vídeo (`<projeto>\NN-nome\`) com `audio/ (sfx/)`, `blender/`, `video/`, `capa/`, `locucao.md`. Copie `scripts/molde/` para `<projeto>\lib\` (as cenas fazem `sys.path.insert(0, "../../lib")`). Frames ficam numa pasta temporária, fora de pastas sincronizadas (Dropbox/Drive).

### 1. Roteiro
- 35–55 s de fala, frases curtas, ~2,8 palavras/s. Gancho na 1ª frase (sem "todo mundo tem a mesma dúvida").
- 4–5 capítulos, cada um = uma imagem forte na maquete. Nome curto (≤ 11 letras) pra barra de etapas.
- Termina com uma frase-síntese + **CTA padrão falado**: "Quer aprender a fazer vídeos assim, de forma automática, usando IA? Me segue nas redes."
- Entregar `locucao.md`: texto corrido + tabela por cena (tempo, chip, fala, o que a maquete mostra) + plano de som.

### 2. Voz, trilha e SFX
Com o **ElevenLabs** conectado (MCP oficial) gere tudo lá; sem ele, peça o áudio da locução ao usuário e use os sons de `scripts/molde/sfx/` + `scripts/sfx_synth.py` (sons por código).
- Voz: a voz favorita do usuário (pergunte e anote), modelo `eleven_v4`, `language="pt"` → `audio/locucao.mp3`.
- Trilha: `compose_music` instrumental, ~duração + 6 s, prompt de clima do nicho → `audio/trilha.mp3`. Se ela "acabar" antes do fim, use `music_jump=(corte, volta)` no mix.
- SFX: `text_to_sound_effects` curtos (0,5–4 s) → `audio/sfx/`. Comuns já prontos em `scripts/molde/sfx/` (whoosh, pop, titulo, redes, foto, celular, porta, apagar).
- Gera custo: só depois do roteiro aprovado.

### 3. Tempo de cada palavra
`python transcrever.py audio/locucao.mp3 blender/palavras.json` (faster-whisper medium, CPU int8). Corrija a legenda com `legenda.py palavras.json legenda.json '{"teça":"peça"}'` (já junta "para o"→"pro" e remove "o" antes de "IA"). Monte o dicionário `T = {evento: segundo}` pelas palavras-gatilho (dispare ~0,1–0,3 s antes da palavra).

### 4. Cena 3D (`blender/cena.py`)
- `mvb.setup(DUR)` já liga o **modo premium**: Cycles na GPU (NVIDIA OptiX/CUDA, Mac Metal, AMD HIP; sem GPU usa CPU), 32 amostras + denoiser, HDRI (`assets/modelos/hdri/ceu.hdr`), sol quente com sombra firme, material único guiado por `obj.color` com **bevel shader + grão**, desfoque de miniatura automático (`DOF_K=4`, foco no alvo da câmera). `premium=False` = modo rápido antigo (só rascunho).
- Base (`mvb`): `obj/empty/text3d`, `Person` (bonequinho; `tie=`, `apron=`, `cap=`), `walk_pose(path,t)`, `win()`, câmera por keyframes `mvb.CK = [(t, pos, alvo, lente, up)]` com smootherstep, `face_cam()`, `mvb.run(apply, ANCH, meta)` (âncoras projetadas → `meta.json` pro overlay).
- Modelos prontos: `mvb.place(caminho.glb, loc, rz, escala)` (importa uma vez, depois instancia). Pacotes Kenney CC0 em `assets/modelos/{commercial,cars,roads,suburban}/x/Models/GLB format/` (baixados pelo instalar.py). Escalas: prédios ×8,5–9, casas ×7,5, carros ×1,75, postes/semáforos ×8.
- **`cidade.py`** (molde): quarteirões, asfalto, faixas, zebras, árvores fofas com textura de folha (`fluffy_tree`), trânsito e pedestres animados (`traffic()` + `animate(t)`), e o **prédio-herói aberto** (cantos arredondados, lajes salientes, 1º andar em z=0..4,4 onde mora a cena, 2º andar decorado, letreiro deitado no telhado, luz interna). Troque cor/letreiro/decoração por nicho.
- **Placas de capítulo em 3D** (`titulos3d.Placas`): placa branca arredondada presa à câmera, entra girando, com número no disco colorido + "ETAPA N · TEMA" + título + descrição curta. Durante a placa o foco vai pra ela e o fundo desfoca. Chame `TIT.update(t)` no `apply`.
- Abertura padrão: câmera alta sobre a cidade → aproxima → atravessa a abertura do prédio → cai na cena interna. Fechamento: sai do prédio pra aérea (fundo do CTA).
- Checar sempre: câmera dentro de prédio/árvore, objeto tapando o herói, placa tapada por laje.

### 5. Prévia (obrigatória)
Render de 6–15 quadros-chave a 40–50 % → `folha.py <dir> <saida.jpg> 6` → revisar e corrigir antes do render completo.

### 6. Render final
`python scripts/molde/render.py <cena.py> <frames_dir> 100 [partes]` — 1 processo com todas as placas; com 2+ placas NVIDIA iguais use `partes=2`. Referência: RTX 4090 ≈ 1,3 s por quadro. Placas menores/Mac: bem mais lento — avise e sugira 50 % de resolução pra rascunho.

### 7. Interface (`blender/overlay.py` com `mvo.Cfg`) — ver `references/interface.md`
`Cfg(chips=..., chip_style="stepper", shadow=True, titles=[] (placas são 3D), calls=..., counters=..., late=[extras], phone=..., flash=..., cta=(t_pergunta, t_redes), tag=("ilustrativo", t))`. Celular de app desenhado por quadro (ver `exemplos/premium-costureira/overlay.py`, `phone_v2`). Área segura: ver `safe-zone/SAFE-ZONE.md` (y 240..1500, x 95..985, x ≤ 870 abaixo de y 800); legenda karaokê em y≈1150 (pode descer até 1470).

### 8. Som (`blender/mix.py` com `mvm.mix`)
Voz normalizada a −17 dBFS RMS; trilha com ducking automático (`music_db=-14`, `duck_db=-9`); cues `(arquivo, t, ganho, "onset"|"peak"|"start", dur_max)`. Mono vira estéreo igual nos dois lados. Master no encode: `loudnorm=I=-14:TP=-1.5`. **Avisar que o equilíbrio foi calculado e pedir pro usuário ouvir.**

### 9. Entregáveis
- `video/<nome>_vN.mp4` (crf 17) + `python scripts/molde/video.py preview <master>` (720p leve) + `video.py lado <antes> <depois> <saida>` quando houver versão anterior.
- Capa: arte por IA de imagem (ex. Nano Banana Pro, 9:16, "low-poly 3D miniature diorama… empty top third for a title, no text") + `capa.py arte.png capa.jpg "LINHA 1|LINHA 2" "etiqueta" cor` (título dentro do recorte 3:4 do grid).
- Legenda do post honesta sobre as ferramentas usadas.

## Armadilhas já resolvidas
- Prédios/árvores entre câmera e herói → reposicione câmera ou tire o objeto (filtre árvores perto do caminho).
- Elemento dentro de parede sólida fica invisível → modelar saliente.
- Contador atrasado em relação à fala → disparar ~1 s antes.
- Ícones/textos "de frente pra câmera" (`face_cam`) precisam ser modelados no plano XY (z = profundidade).
- Glb com várias peças (carros) → `kit()` já desparenta e junta antes de instanciar.
- Placa 3D: forma = contorno 2D extrudado (bevel de malha deu "asas").
- Mudou só cor/interface? Re-rode só o overlay (minutos), não o Blender.

## Adaptar a um tema novo
Copie `exemplos/premium-costureira/` (cena + overlay + mix), troque: cenário interno, `T`, `CK`, `ANCH`, itens de `titulos3d.Placas`, `chips`, `calls`, cartões do overlay e a lista de cues do mix. O resto (cidade, prédio, luz, CTA) já vem pronto.
