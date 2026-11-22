---
name: esquadrao-voxel
description: Cria Reels/TikTok/Shorts verticais 3D "Esquadrão Voxel" — bonequinhos de bloco (Claudes laranja de cabeça quadrada, olhos de retângulo com brilho, bochecha coral, tênis com faixa limão e pin de asterisco; elenco próprio de 19 personagens com roupa e objeto por função: capitã de quepe e luneta, maestro de batuta, mapeadora de lanterna, mecânica de bandana e chave, pintora de rolo, escriba de pena, controlador de pista, feirante, influencer de pau de selfie, novato de boné de hélice, telegrafista, arquivista, câmera, cientista, jurada, alfaiate, maquinista, apresentador e você como humano) explicando um processo de várias etapas em formatos próprios (fábrica com esteira em que um objeto se transforma, missão por fases, antes×depois, tour de estúdio, maquete de cima) — sem copiar o formato "time de N Claudes, o primeiro, o segundo" de outros perfis. Feito por código no Blender (EEVEE, sombra suave, motion blur, desfoque) + HUD 2D próprio (título-adesivo creme com contorno grosso, contador que sobe, legenda palavra a palavra em etiqueta escura com palavra-chave limão, terminal digitando, cartões de doc/onda/notificação/comentário/carimbo/estouro) + pós (brilho, aberração cromática, grão, vinheta). Use quando o usuário pedir "esquadrão voxel", "bonequinhos de bloco / voxel / estilo Crossy Road", "Claudes 3D", "fábrica de Reels", "agentes trabalhando", ou quiser explicar um fluxo de várias etapas com personagens 3D.
---

# Esquadrão Voxel (out/2026)

Vídeo 3D de bonequinhos de bloco que explica um processo de várias etapas, 18–40 s. A técnica (bonecos, salas, câmera, HUD) é desta skill; **a narrativa é inventada a cada vídeo**.

## 🚫 Não parecer cópia (regra nº 1)
Esse visual de bonequinhos de bloco já circula em outros perfis com uma estrutura muito marcada ("time de N Claudes", um por cena). Copiar essa estrutura queima a sua imagem. Nunca usar:
- "Montei um time/banca de N Claudes que…" nem a espinha "o primeiro… o segundo… o terceiro…";
- título "O <PROFISSÃO>" + contador numérico em toda cena; número no peito dos bonecos;
- abertura com terminal digitando um /comando; CTA comentário → "Publicado" → DM; papel com fita; etiqueta laranja na legenda; cidade à noite como cenário principal.
- personagens da referência: chapéu de detetive xadrez + lupa, safari, boné azul, boina + claquete, óculos de tela com código, CEO de terno e gravata, homem das cavernas, velhinho de bigode branco, tubarões de terno → use o **elenco próprio** (`bonecos.elenco(...)`, ver `references/ELENCO.md`);
- cenários da referência: prédio de escritório em corte, fliperama com máquina de garra, biblioteca de estantes, estúdio Shark Tank; HUD deles: tarja de papel com fita, legenda laranja serifada, contador em pílula branca, abas de departamento, coração "Curtiu?".
Antes de escrever o roteiro, escolha um formato abaixo (ou invente outro) e diga ao usuário qual é. O que aprendemos com as referências (cenário-metáfora, mostrar a função com objeto + painel, número que sobe, virada antes do último item, time reunido no fim, ritmo de 1,5–3 s) está em `references/ESTUDO-REFERENCIAS.md` — leia antes do roteiro.

## Formatos próprios
1. **Fábrica / linha de montagem** (exemplo pronto em `exemplos/fabrica-de-reels/`): um OBJETO é o protagonista. Entra num funil, anda na esteira e cada máquina o transforma (ideia → roteiro → voz → vídeo → post). Câmera em travelling contínuo seguindo o objeto, empurrão a cada transformação. HUD: `hud.trilho` (etapas que acendem). Operários de macacão e capacete.
2. **Missão / corrida de obstáculos:** um Claude atravessa salas-fase (cada fase = um problema resolvido), pulando de plataforma em plataforma; barra de vida/fase no HUD.
3. **Antes × depois na mesma sala:** a sala bagunçada (tudo manual) vira a sala organizada (automatizado), em duas passadas da câmera pelo mesmo caminho.
4. **Bastidor do estúdio:** um tour guiado por um Claude apresentador que abre portas de salas diferentes (cada porta = uma ferramenta).
5. **Maquete de cima:** câmera alta olhando o mapa de um bairro de blocos; cada prédio acende quando a etapa acontece (estilo jogo de cidade).

Identidade visual (só nossa): título em adesivo creme com contorno grosso e sombra dura, legenda em etiqueta escura com palavra-chave limão #C6F432, paletas `manha` (padrão), `crepusculo` e `noite`, e cada sala/máquina com cor própria.

<!-- catalogo -->
## 🧭 Aluno perdido? Mostre o catálogo
Se o usuário não souber qual estilo quer: mande **https://skills-claude-ailab.pages.dev/** e siga a skill `escolher-estilo`.

<!-- safe-zone-v2 -->
## ⚠️ Safe zone — OBRIGATÓRIO
Leia `safe-zone/SAFE-ZONE.md`. Canvas 1080×1920: topo livre até y 240 · base a partir de y 1500 · laterais 95 · botões x ≥ 870 de y 800 a 1500.
Nesta skill (já vem no `hud.py`): título y≈312 · contador y≈446 · cartões y 560–900 · terminal/comentário y≈1270 · legenda y≈1395, centro x≈490. O 3D ocupa a tela toda; o boneco da cena fica entre y 800 e 1450. Antes do final: `python safe-zone/safe_zone.py checar <prévia.mp4>`.

<!-- marca-dagua -->
## 💧 Marca d'água — OBRIGATÓRIO
`python marca-dagua/marca_dagua.py status` antes de produzir (se não configurada, perguntar @/logo/nenhuma). Último passo: `marca_dagua.py aplicar <sem_marca.mp4> <final.mp4>`. Capa sem marca.

<!-- ganchos -->
## 🎣 Gancho — OBRIGATÓRIO
Leia `ganchos/GANCHOS.md`. Quadro 0 já com boneco caindo + título grande; fala do gancho ≤ 12 palavras, mostrando o resultado antes ("Eu jogo uma ideia aqui… e lá do outro lado sai um Reel pronto"); algo muda a cada 2–3 s.

## Primeiro uso
`python scripts/instalar.py` — instala as bibliotecas (Pillow, NumPy, faster-whisper, ffmpeg), confere o **Blender 5** (grátis; se faltar, mostra o comando pra instalar) e renderiza 1 quadro de teste. Precisa de placa de vídeo a partir de 2017 (integrada serve, só fica mais lento) ou Mac com chip Apple.

## Pipeline (pasta do projeto: `audio/`, `blender/`, `video/`, `capa/`)
Os módulos ficam em `scripts/molde/` e as cenas importam direto de lá (`sys.path.insert(0, ~/.claude/skills/esquadrao-voxel/scripts/molde)`). Exemplo com o elenco novo: `exemplos/estacao-voxel/` (trem que para em estações, travelling, elenco inteiro numa arquibancada, contador 0→19, mix com os sons que vêm na skill). Exemplo completo e testado: `exemplos/fabrica-de-reels/` (cena.py com câmera de travelling, overlay.py, texturas.py, mix.py, locucao.md, vídeo).

1. **Roteiro** — escolher o formato (seção acima). Gancho mostrando o resultado antes da explicação (ex. "Eu jogo uma ideia aqui… e lá do outro lado sai um Reel pronto"). Cada etapa = uma frase curta + UMA transformação/ação visual. Termina com a frase-síntese + CTA do usuário.
2. **Voz** — ElevenLabs com a voz do usuário (pergunte qual e anote; modelo `eleven_v4` deixa a voz clonada mais natural), `language="pt"` → `audio/locucao.mp3`. Tempo das palavras: `python scripts/molde/transcrever.py audio/locucao.mp3 blender/palavras.json`. Monte `T = {cena: segundo}` pelas palavras "o primeiro / o segundo…" (corte ~0,05 s antes).
3. **Texturas** — `blender/texturas.py` usando `telas.py`: `cidade`, `terminal`, `doc`, `grafico`, `onda`, `timeline`, `agenda`, `cortica`, `placa(topo, texto, cor)`, `neon(texto)`, `app`, `letreiro`. `python texturas.py` → `blender/tex/`.
4. **Cena 3D** (`blender/cena.py`):
   - `vox.setup(DUR, paleta="crepusculo"|"noite"|"manha")` (EEVEE; `cycles=True` = mais bonito, ~4× mais lento).
   - Sets: `cenario.sala(x, parede_cor, "madeira"|"azulejo"|"carpete", fundo=(img,w,h,z), luz=cor)` — um por personagem, espaçados 30 em X. Peças: `mesa, notebook, monitor, quadro, neon, luminaria, planta, caneca, estante, tripe_mic, botao_grande, pedestal`.
   - Bonecos: **padrão = `bonecos.elenco("nome", "capita"|"maestro"|"mapeadora"|"mecanica"|"pintora"|"escriba"|"pista"|"feirante"|"influencer"|"novato"|"telegrafista"|"arquivista"|"camera"|"cientista"|"jurada"|"alfaiate"|"maquinista"|"apresentador"|"voce")`** (19 personagens com a assinatura; retratos em `references/elenco/`, refazer com `scripts/molde/retratos_elenco.py`). O objeto da mão aparece com `b.gesto("mostra", t0, t1)` / `"mostra2"`. As `receitas` antigas (detetive, boné, boina+claquete) ficam só pra projetos velhos. Peças avulsas: `bonecos.receita("nome", "pesquisador")` ou `Boneco(pele=, roupa=, chapeu=, rosto=[], mao=, mao_esq=, cabelo=, extras=[])`. Peles: `PELES` (claude, lima, lilás, azul, rosa, menta, robô, humano…). Chapéus: safari, detetive, bone, boina, cartola, capacete, coroa, chef, fone. Rosto: oculos, oculos_sol, bigode, barba, bochecha. Corpo: gravata, gola, moletom, cracha, antena. Mão: lupa, lapis, microfone, claquete, celular, caneca, prancheta, envelope.
   - Roteiro do boneco: `b.trilha=[(t,(x,y),yaw)]` (anda pulando; salto > 6 = teletransporte no corte), `b.chao=[(t,z)]`, `b.surge(t,"cai"|"pula"|"pop")`, `b.some(t)`, `b.gesto("acena"|"ergueR"|"ergueL"|"segura"|"segura2"|"digita"|"aponta"|"comemora"|"bate"|"olha"|"pula"|"tremer"|"fala", t0, t1)`, `b.segura_placa("placa.png", t0, t1, mao="L")`. Pisca sozinho e respira.
   - Câmera: `vox.CAM=[(t, pos, alvo, lente, "corte"|"chicote"|"suave")]` (empurrão lento automático dentro do plano; chicote com motion blur real). `vox.SHAKE=[(t, força)]` nos impactos.
   - Gestos lidos de frente: braço pra frente some (fica de topo pra câmera) — use "segura"/"ergue" (pra cima).
5. **Prévia (obrigatória)** — `blender -b --factory-startup --python cena.py -- <tmp> 50 "15,150,300,..."` (~2 s/quadro) e `python scripts/molde/montar.py <tmp> overlay.py - folha.jpg --folha 0.5,5,8,...` → corrigir enquadramento antes do render.
6. **HUD** (`blender/overlay.py`): `H = hud.HUD()`; `H.legenda(palavras, chaves=[...])`; `H.titulos=[(t,"TEXTO",nº)]`; `H.contadores=[(t0,t1,"RÓTULO|LINHA 2",[(t,valor)],cor,sufixo)]`; `H.terminais=[(t0,t1,"/comando",dig0,dig1)]`; `H.extras=[hud.cartao_doc, cartao_onda, notificacao, comentario, coracao, carimbo, estouro, selo, cartao_img (print real), confete, flash]`. O "✓" é desenhado como traço (as fontes não têm o glifo).
7. **Render** — `python scripts/molde/render.py cena.py <frames> 100 3` (3 processos; ~0,7 s/quadro efetivo numa RTX 4090). Frames fora de pastas sincronizadas (Dropbox/Drive/OneDrive).
8. **Som** — `mix.py` do projeto com `mix.mix(voz, trilha|None, cues, dur, saida, pasta_sfx)`. Sons prontos em `scripts/molde/sfx/` (whoosh, pop, titulo, foto, celular, porta, apagar, redes); com ElevenLabs dá pra gerar mais (`text_to_sound_effects`); se o usuário tiver biblioteca própria, use a pasta dele. Todo elemento que aparece e todo corte tem som; toque leve em cada palavra da legenda.
9. **Montagem** — `python scripts/molde/montar.py <frames> overlay.py audio/mix.wav video/x_sem_marca.mp4` (pós: brilho, aberração, grão, vinheta; ajuste em `POS = {...}` no overlay) → marca d'água → `video.py preview`.
10. **Capa** — quadro do CTA (time inteiro) ou de um personagem com placa, título grande dentro do recorte 3:4.

## Armadilhas já resolvidas
- Objeto do Blender não aceita atributo novo (`obj._x = …`) — guardar estado em Python.
- Placa na mão: o grupo gira 180° em X (o cabo acompanha o braço erguido).
- Plano aberto 9:16 é estreito: 5 bonecos cabem com espaço 1,0 e câmera a ~11 m (lente 35); 6+ → 2 fileiras (atrás em cima do teclado do notebook).
- `show(obj, s)` usa escala base (1,1,1): em objeto com escala própria passe `base=` (senão vira bolha de 1 m).
- Cena de dia estoura fácil: luzes de frente ~3800, glow 1,3, `POS = dict(bloom=0.1, limiar=0.9)` no overlay.
- Câmera de travelling: sobrescreva `vox.cam_at` na cena (ver exemplo da fábrica), suavizando a posição do objeto (média de ±0,4 s).
- Personagem atrás de tela/monitor: tirar o notebook da frente ou subir o boneco num banco (`b.chao`).
- Emissão forte estoura na cor (Standard): botões e telas com emit ≤ 1,2, placas 0,7.
- Mudou só HUD/cor de cartão? Rode só o `montar.py` (minutos), não o Blender.
