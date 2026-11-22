---
name: skill-do-jarvis
description: "Jarvis — edição de vídeo com motion: decupagem, cortes de fala, punch-ins, glitch, tracking, HUDs, UI, legenda profissional com tracking (palavra por palavra, atrás da pessoa, transcrição e SRT gerados do próprio áudio), sonorização com a biblioteca de SFX do usuário (pasta definida no config.json) e motion 3D real (Remotion + three.js), estilo de motion CLEANSTILL (anúncio limpo e calmo: fundo pastel, texto palavra por palavra, UI flutuando), com preview na timeline do Remotion Studio e render local. Use para editar ou montar um vídeo inteiro a partir de takes/locução/trilha, legendar vídeo, gerar SRT, criar um vídeo 100% motion só a partir de um tema, motion graphics ou animações 3D."
---

# Jarvis (decupagem → corte → câmera + overlays com TRACKING → PREVIEW → aprovação → master em camadas)

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
- Nesta skill: HUD fixo (barra de progresso, ● REC, rótulo de etapa) em y 250–330 — não mais em y 110–200; cards a partir de y≈340; faixa da legenda y 1250–1450 continua; cards inferiores em y 1300–1480 (não mais 1500–1700); ícones/cards laterais à direita só acima de y 800. Cantoneiras decorativas podem ficar nas bordas.

<!-- marca-dagua -->
## 💧 Marca d'água — OBRIGATÓRIO (perguntar na 1ª vez, aplicar sempre)
- **Antes de produzir:** `python marca-dagua/marca_dagua.py status`. Se der **NAO CONFIGURADA**, perguntar ao usuário se quer marca d'água pra proteger os vídeos contra repost sem crédito: **@ do Instagram**, **logo PNG** ou **nenhuma** → salvar com `configurar --texto "@perfil"` / `--logo arquivo.png` / `--nenhuma` (fica em `~/.claude/marca-dagua.json` e vale pra todas as skills e próximas produções; não perguntar de novo).
- **Último passo antes da entrega:** `python marca-dagua/marca_dagua.py aplicar <master_sem_marca.mp4> <master.mp4>` e gerar o preview a partir do master já marcado. Capa sem marca d'água.
- Visual: sutil (branco ~45%, sombra leve), acima da coluna de botões, alternando direita ↔ esquerda a cada 8 s — dentro da safe zone. Detalhes: `marca-dagua/LEIA.md`.

<!-- ganchos -->
## 🎣 Gancho — OBRIGATÓRIO no roteiro e antes do render final
Leia `ganchos/GANCHOS.md`. Quadro 0,0 s com ação + texto grande do gancho (3–7 palavras, sem tela preta/fade/moldura entrando); fala do gancho ≤ 12 palavras, com energia, até ~1,5 s; mostrar o resultado antes da explicação; algo muda na tela a cada 2–3 s; 25–40 s pra explicação; dar um motivo pra mandar pra alguém. Escrever 3 opções de gancho e escolher a mais forte; rodar o checklist do fim do guia antes de entregar.

Foco: o VÍDEO é o protagonista. O motion complementa o que é falado/mostrado para aumentar retenção. Linguagem visual: HUD elegante de vidro, UI translúcida, arestas iluminadas.

## Habilidades
| Habilidade | Referência |
|---|---|
| **Montagem completa** (takes + locução + trilha → decupagem, melhores takes, vídeo inteiro montado, sem Premiere/CapCut) | `references/montagem-completa.md` |
| **Motion do zero** (só o tema: roteiro, narração com tempos, motion completo, som) | `references/motion-do-zero.md` |
| Edição de vídeo falado (decupagem, câmera viva, glitch, HUD/UI, tracking) | este arquivo + `references/plano-motion.md`, `references/tracking.md` |
| Cortes de fala (silêncios, gaguejos, repetições, hook) | seção 2 |
| **Legenda profissional com tracking** (APROVADA em 2026-10-09) | `references/legendas-criativas.md` + `assets/legenda-template/` |
| Transcrição e SRT a partir do áudio do vídeo (sem app externo) | seção 1 + `assets/legenda-template/scripts/` |
| Sonorização (SFX da biblioteca do usuário em `pasta_sfx`, mix, stems) | `references/sfx.md` |
| Motion 3D real (vidro/holograma, câmera 3D) | `references/remotion-3d.md` + `assets/remotion-3d-template/` |
| Estilo visual padrão (Vidro, Holograma, Poppins) | `references/estilo-visual.md` |
| **Estilo CLEANSTILL** (anúncio limpo e calmo: fundo claro com névoa pastel, texto cinético palavra por palavra, lista em foco, pills de vidro, objeto herói no céu, carrossel 3D, lupa, transições bloom/portal/burst) — APRENDIDO em 2026-10-09 | `references/cleanstill.md` + `assets/cleanstill-template/` |

## Antes de tudo
1. **Config do usuário.** Ler `config.json` nesta pasta da skill. Se não existir (primeira execução), perguntar em UMA rodada (AskUserQuestion) e gravar `config.json` a partir de `config.example.json`:
   - `pasta_projetos` — onde criar as pastas de projeto;
   - `pasta_saida` — onde entregar os renders/pacotes. Sugerir como padrão a Área de Trabalho do sistema (cada projeto em `<Desktop>\<projeto>`), resolvendo o caminho real: Windows `powershell -NoProfile -Command "[Environment]::GetFolderPath('Desktop')"` (pega o Desktop redirecionado pelo OneDrive); macOS `~/Desktop`; Linux `xdg-user-dir DESKTOP` (ou `~/Desktop`);
   - `pasta_sfx` — OBRIGATÓRIO: a pasta da biblioteca de efeitos sonoros do usuário (perguntar na primeira execução). Todo som da edição sai dela, nunca de outro lugar;
   - `pasta_referencias` — pasta de referências visuais do usuário (opcional, `null`);
   - `cor_acento` — padrão `#bfeaff` (gelo);
   - `look_padrao` — `vidro` (padrão) ou `holograma`;
   - `idioma` — idioma da conversa e dos textos na tela (padrão `pt-BR`);
   - `pasta_sincronizada` — `true` se a pasta de projetos fica em Dropbox/OneDrive/Google Drive.
   **Nunca assumir caminhos**: tudo que é pasta vem do config; se faltar, perguntar. Conversa casual no `idioma` do config.
2. **Escolha do estilo de motion (SEMPRE que for fazer motion):** em qualquer pedido com motion (motion do zero, montagem, edição com motion, motion graphics, anúncio), perguntar na rodada de perguntas iniciais (AskUserQuestion, pode ser junto das outras) qual estilo usar, com as opções:
   - **Jarvis padrão (Vidro/Holograma)** — fundo azul-escuro, HUD, tracking, glitch, ícones 3D (ver `estilo-visual.md`);
   - **Cleanstill** — limpo e calmo, fundo claro pastel, tipografia cinética sincronizada, UI flutuando, transições de luz (ver `references/cleanstill.md`, template `assets/cleanstill-template/`).
   Recomendar como 1ª opção o que casar melhor com o pedido: pessoa falando para a câmera → Jarvis padrão; anúncio de produto/serviço/ferramenta, lançamento ou peça "premium/clean" → Cleanstill. Se o usuário já disse o estilo ("faz em cleanstill"), não perguntar. Escolhido cleanstill, ler `references/cleanstill.md` inteiro e partir do template dele; a paleta, tipografia e transições de lá substituem as do estilo padrão (regras de movimento e proibições continuam).
3. **Estilo padrão (obrigatório quando o estilo for Jarvis padrão):** ler `references/estilo-visual.md` antes de qualquer peça. VIDRO é o look principal e HOLOGRAMA o secundário; fundo azul-escuro com grid branco nas peças só de motion. O acento é `cor_acento` do config; o verde-limão `#D7FF3A` fica só como pontinho de destaque. Se `pasta_referencias` existir, consultar antes de criar.
4. **Motor:** Claude Code local com Remotion + three.js (`references/remotion-3d.md`), partindo do template `assets/remotion-3d-template/`. Preview na timeline do Remotion Studio, aberto no painel do navegador do Claude; render local na GPU.
5. **Ferramentas (o usuário não instala nada na mão):** primeiro `node -v`. Se o Node.js não existir (ou for < 18), instalar o LTS sozinho, avisando o usuário: Windows `winget install -e --id OpenJS.NodeJS.LTS --accept-package-agreements --accept-source-agreements` (o Windows pode pedir confirmação de administrador: dizer para clicar em Sim); macOS `brew install node` se houver Homebrew, senão baixar e abrir o .pkg LTS oficial de nodejs.org (a senha do sistema é o usuário quem digita). Depois de instalar, o PATH da sessão pode não ter o node: usar o caminho completo (Windows `C:\Program Files
odejs
ode.exe` / `npm.cmd`) ou pedir para reabrir o app. Em seguida, no projeto, `npm install` do template + `npm i ffmpeg-static @techstark/opencv-js`.
   - `ffprobe`: `npx remotion ffprobe` (vem com o Remotion; lê `color_transfer`/HDR).
   - `ffmpeg` completo: o binário do `ffmpeg-static` (`node -p "require('ffmpeg-static')"`; ~80 MB, build estático baixado pelo npm). Verificado no Windows: tem zscale/tonemap/eq (HDR), scale, fps, crop, drawtext, drawgrid, tile, extractplanes, lut, silencedetect, loudnorm. O `npx remotion ffmpeg` é enxuto (sem eq, fps, crop, drawtext, tile, lut): serve só para encode simples e para o HDR sem o `eq`.
   - `drawtext` no Windows avisa "Fontconfig error" mas funciona; para fonte certa passar `fontfile='C\:/Windows/Fonts/arial.ttf'`.
   - Tracking: OpenCV em Node (`@techstark/opencv-js`), ver `references/tracking.md`. Python é opcional.
6. **Nunca escrever o nome do usuário (nem o nome da skill/autor) no vídeo.** Marca só se o pedido mandar.

## REGRAS DE OURO (sempre)
1. **Preview primeiro, alta só com autorização.** Renderizar SEMPRE um preview leve (<30 MB) e mostrar. NUNCA renderizar em alta antes de o usuário aprovar o preview E autorizar explicitamente ("Posso renderizar em alta?").
2. **Não refazer vídeo já entregue** se o usuário só pediu ajuste de skill ou fez pergunta — perguntar antes.
3. **Sem legenda** quando o usuário disser que vai fazer a legenda; deixar livre a faixa da legenda (~y 1250–1450).
4. **Cor certa (HDR do iPhone).** `ffprobe` no vídeo: se `color_transfer=arib-std-b67` (HLG) / smpte2084 / Dolby Vision, CONVERTER para SDR Rec.709 ao extrair os frames (senão fica lavado). Filtro aprovado:
   `zscale=t=linear:npl=203,format=gbrpf32le,zscale=p=bt709,tonemap=mobius:desat=0:param=0.3,zscale=t=bt709:m=bt709:r=tv,format=yuv420p,eq=gamma=0.95:saturation=1.05` (extrair com `-q:v 1`). Testar 1 frame antes. Usar o ffmpeg do `ffmpeg-static` (o do Remotion não tem `eq`).
5. **SFX SEMPRE da biblioteca do usuário (`pasta_sfx`), NUNCA gerados por código. NUNCA usar riser/suspense crescendo antes de revelação** (soa clichê e datado; sons sintetizados por código soam artificiais). Escolher pelo nome/categoria, medir o pico de cada arquivo e alinhar o pico ao evento; regras de uso e mix em `references/sfx.md`. O gerador `assets/sfx-gen/` está aposentado: não usar nem como tapa-buraco. Se faltar um tipo de som na biblioteca, deixar sem som e avisar.
6. **Trabalhar numa cópia**; nunca sobrescrever o original. Projeto novo = subpasta própria em `pasta_projetos`; frames e caches temporários fora de pasta sincronizada (em `%TEMP%`).

## Padrão de qualidade
(Vale para o estilo Jarvis padrão. No cleanstill não há HUD, glitch nem tracking: o padrão de qualidade é o checklist do item 10 de `references/cleanstill.md`.)
Histórico: v1 reprovada por "simples", v2 por não ter tracking; o exemplo aprovado tinha tudo abaixo. Só cards entrando e saindo = FRACO. Elemento de detecção em coordenada fixa = ERRADO. Nada sujo: no máximo 1 card de UI + 1 elemento de detecção + 1 ícone 3D grande por vez. Toda edição precisa ter:
- **Tracking real** em toda caixa, malha, scan, círculo, callout e mira → `references/tracking.md`.
- **Profundidade com a pessoa recortada**: números, palavras gigantes, ícones 3D e cards ATRÁS da cabeça; contorno luminoso da silhueta; fundo escurecendo/dessaturando/desfocando quando faz sentido → `references/segmentacao.md`.
- **Ícones 3D reais** simbolizando cada ideia → `references/icones-3d.md`.
- **Câmera viva**: zoom-out de abertura 1.2→1.0 com flash; punch-in 1.0→1.10 (0.14 s, power4.out) + flash .16 nos impactos, segura 0.6–1.7 s, volta 0.55 s; push lento em pergunta dramática/close emocional (+ escurecer 35%); whip pan (x ±160 + blur 18px) nas transições; shake curto (0.3 s, ±12px decrescente).
- **Glitch** (0.16–0.28 s) nas viradas: cópias do frame canal R e GB (feColorMatrix, mix-blend screen) com faixas clip-path inset aleatórias deslocadas ±18–38px + jitter do frame base.
- **Camada de detecção presa ao vídeo** (escala com o zoom): caixas com cantoneiras + scanline + tag, malha facial (pontos + anéis, olhos, boca, contador de pts e %), grid de scan com banda varrendo e células piscando + %, círculo à mão (stroke animado) com etiqueta, callouts (ponto pulsando + linha em cotovelo + label), mira/retícula giratória.
- **Camada de UI** (fora do zoom): cards de vidro (ver `estilo-visual.md`) com entrada 3D (rotationX −38°→0, blur→0); camada inteira "respirando" (y ±7px, rot ±0.35° em sine).
- **HUD fixo**: cantoneiras, barra de progresso no topo, ● REC piscando + timecode, rótulo de etapa (01 · HOOK / 02 · O QUE A IA FAZ / 03 · O PROBLEMA ou DIA 01 · MANHÃ / PROJETO 01 / FIM), medidor vertical IA % (sobe em cenas geradas/IA, desce nas reais), coluna de log rolando (opacity .4, máscara em fade).
- **Zoeira** leve, 1 piada a cada ~8–10 s sem poluir (exemplos em `references/plano-motion.md`).

## 1. Decupagem (sempre)
1. ffprobe (duração, resolução, fps, COR/HDR).
2. Texto com tempo: **o usuário não precisa mandar SRT** — o padrão é transcrever o próprio áudio do vídeo com `assets/legenda-template/scripts/transcrever.py` (faster-whisper large-v3, palavra por palavra) e gerar o `.srt` com `scripts/gerar_srt.py` (entregar o .srt junto, serve para Premiere/CapCut/YouTube). Se o usuário mandar .srt/roteiro, usar para conferir a grafia (tempo de cada palavra = proporção de caracteres dentro da linha, remapeado pela EDL). Outras rotas: 2º OCR de legenda queimada: `ffmpeg -i src.mp4 -vf "fps=5,crop=1000:320:40:1160,format=gbrp,extractplanes=r,lut=c0='if(gt(val,215),0,255)'" ocr/%04d.png` (ajustar o crop) → `tesseract f - --psm 7 -l eng` em paralelo → juntar repetições em segmentos in/out, reconstruir frases e acentos à mão; se não houver fala clara, pedir o roteiro. Python: se `python --version` falhar, instalar sozinho (Windows `winget install -e --id Python.Python.3.11`; macOS `brew install python@3.11`) e usar um venv do projeto para `faster-whisper`, `mediapipe==0.10.14` e `opencv-contrib-python` (nunca instalar no Python global do usuário).
3. (ffmpeg do `ffmpeg-static` em todos os comandos desta seção) `silencedetect=n=-35dB:d=0.35` + grid de frames com timestamp (`fps=1,scale=240:-1,drawtext=pts,tile=8x6`).
4. Cortes de cena: diferença média entre frames (135x240) >22 e >2.2× vizinhos. Elemento de detecção vive dentro de um único plano; encerrar 0.05 s antes do corte.
5. Coordenadas: frame exato com grade 10% (`scale=270:480,drawgrid=w=27:h=48`) → ×4 para 1080x1920; anotar `tref`. Conferir início/fim do plano (errar 0.5 s joga a caixa na cena errada).
6. `decupagem.md`: tempo | fala | imagem | motion.
7. Perguntas (AskUserQuestion, máx. 4, uma rodada) só se algo não for óbvio; se o usuário disser "aprovado"/"decide", seguir e dizer em 1 linha o que foi decidido.

## 2. Corte
- Remover silêncios >0.35 s, gaguejos, repetições; hook forte em 1.5 s. EDL em `edl.json` com `keep`, `segs` (a, b, na = início no tempo novo) e `fm` (frame novo → frame original). Crossfade de áudio 10 ms; recalcular timestamps. (Exemplo aprovado: 13 respiros, 90,3 → 85,2 s.)
- EXCEÇÃO: vídeo já enxuto com legenda queimada → não cortar (quebra o sync) e avisar.

## 3. Plano de motion (frase → recurso)
Cada frase da fala vira um visual. Catálogo de recursos aprovados e genéricos em `references/plano-motion.md`.

## 4. Layout 9:16
- HUD em y 250–330 (safe zone v2: nada essencial acima de y 240); cards a partir de y ≈ 340.
- Selfie sentado: topo livre (0–580) → elementos grandes atrás da cabeça entre y 250–650 (a cabeça cobre a parte de baixo); laterais x<300 e x>760 entre y 650–1100 para ícones 3D; cards inferiores só em 1300–1480, compactos (acima de y 1500 é do @perfil/legenda do app).
- Faixa da legenda (~1250–1450) sempre livre. Se o rosto estiver no topo do quadro, mover o card para baixo ou para o lado oposto.
- Labels nunca saem da tela: label à direita só se o ponto estiver em x < 650; senão, à esquerda. Label da mira abaixo do anel.
- Legenda (só se pedirem): o padrão é a **legenda criativa com tracking** de `references/legendas-criativas.md` (palavra por palavra, colagem em volta da pessoa, 1 palavra-chave gigante por frase na cor de destaque, atrás da cabeça e em arco, texto colado em superfícies). Legenda simples (2–4 palavras, Poppins 800, palavra ativa na `cor_acento`) só se o usuário pedir "legenda simples".

## 5. Composição e PREVIEW (Remotion)
- Projeto em `pasta_projetos\<nome-curto>` copiado de `assets/remotion-3d-template/` (setup em `references/remotion-3d.md`).
- Vídeo-fonte já cortado/convertido para SDR, lido com `<OffthreadVideo>` (ou frames via `fm`); overlays como `AbsoluteFill`s e cenas 3D com `ThreeCanvas`. Tudo deriva de `useCurrentFrame()`; RNG semeado; nada aparecendo fora de hora (opacidade 0 antes do `tin`).
- Antes do render: 10–35 stills-chave (`npx remotion still`) em contact sheet (encaixe, labels cortados, timing, tracking).
- Studio aberto no painel do navegador (`preview_start`) para o usuário ver a timeline. PREVIEW leve: `npx remotion render <Comp> out/preview.mp4 --gl=angle --scale=0.5 --crf=28` (ou H.264 ~2.5 Mbps), com o áudio mixado.
- Mandar o preview + `decupagem.md` (SendUserFile) e terminar perguntando se aprova e se pode renderizar em alta.

## 6. Master em alta (só após aprovação + autorização)
Camadas BASE / MOTION_ALPHA / BASE_LIMPA / MASTER_FINAL, áudio separado e XML do Premiere em `<pasta_saida>\<PROJETO>_PACOTE` → `references/master-camadas.md`.

## 7. Checagem final e resposta
- Grid do vídeo final (`fps=1/3,tile=10x3`): elementos no alvo certo, nada cortado nas bordas, nada visível fora de hora, cor ok, sem tela preta. Corrigir e re-renderizar só o necessário.
- Resposta curta: o que entrou por trecho, o que foi cortado (ou por que não), onde estão os arquivos, próximo passo.

## Referências
| Arquivo | Quando ler |
|---|---|
| `references/estilo-visual.md` | sempre, antes de qualquer peça |
| `references/cleanstill.md` + `assets/cleanstill-template/` | quando o estilo escolhido for cleanstill |
| `references/remotion-3d.md` | setup do projeto, render, cenas 3D |
| `references/plano-motion.md` | ao montar o plano frase → recurso |
| `references/tracking.md` | qualquer elemento preso a rosto/objeto |
| `references/segmentacao.md` | elementos atrás da pessoa, contorno |
| `references/icones-3d.md` | ícones 3D |
| `references/sfx-codigo.md` | APOSENTADO (SFX por código reprovado); só referência histórica |
| `references/sfx.md` | quando e como usar SFX, mix e entrega |
| `references/master-camadas.md` | master em alta e pacote de entrega |
