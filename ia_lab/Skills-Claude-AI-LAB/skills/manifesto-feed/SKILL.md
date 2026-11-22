---
name: manifesto-feed
description: Cria Reels/TikTok/Shorts verticais em motion graphics "Manifesto Feed" — ensaio/manifesto de opinião em fundo grafite quase preto, tipografia pesada branca (Inter Tight) com micro-texto mono, um único acento coral no clímax, cards de vídeo de feed procedurais (ou com imagens de IA), câmera 2.5D que recua/mergulha/atravessa e TRANSIÇÕES POR TRANSFORMAÇÃO (um elemento vira o próximo: comentários viram grade, tile vira card, feed vira esteira, formas viram emblema, card vira corredor infinito, palavra se multiplica e se desfaz, linha se bifurca). Feito em Remotion (React/TypeScript), sem créditos de IA no render; SFX alinhados pelo pico de cada som. Use quando o usuário pedir "estilo manifesto", "estilo do EP01 / futuro descartável", "vídeo de opinião/reflexão sobre internet, IA, conteúdo, feed", "motion escuro editorial com cards de feed", "ensaio em motion com transições que se transformam", ou quiser transformar um texto de opinião (com ou sem locução) nesse estilo.
---

# Manifesto Feed

## 🧭 Aluno perdido? Mostre o catálogo
Se o usuário não souber qual estilo quer, estiver indeciso entre as skills, ou pedir "um vídeo" sem dizer o estilo: mande o catálogo com os exemplos, **https://skills-claude-ailab.pages.dev/**, e ajude a escolher pelo material que ele tem (vídeo falando, copy em texto ou só o tema), seguindo a skill `escolher-estilo`. Se o estilo certo for outro, diga qual e passe o pedido pronto dele. Nunca comece a produzir sem saber o estilo.

<!-- safe-zone-v2 -->
## ⚠️ Safe zone — OBRIGATÓRIO antes de produzir o visual
Leia `safe-zone/SAFE-ZONE.md` e planeje por ele:
- Canvas 1080×1920: **topo** livre até y 240 · **base** a partir de y 1500 · **laterais** 95 px · **botões** x ≥ 870 de y 800 a 1500.
- Frase-chave, palavra grande e CTA ficam inteiros dentro. Fundo, grades, corredor e cards decorativos podem passar.
- A assinatura `EP.XX · TÍTULO` em mono no topo (y≈150) é decorativa e some no clímax; se o título for importante, desça pra y ≥ 250.
- Confira a prévia: `python safe-zone/safe_zone.py checar <prévia.mp4> --tempos ...` (pior caso: câmera aproximada).

<!-- marca-dagua -->
## 💧 Marca d'água — OBRIGATÓRIO (perguntar na 1ª vez, aplicar sempre)
- **Antes de produzir:** `python marca-dagua/marca_dagua.py status`. Se der **NAO CONFIGURADA**, perguntar: **@ do Instagram**, **logo PNG** ou **nenhuma** → `configurar --texto "@perfil"` / `--logo arquivo.png` / `--nenhuma`.
- **Último passo antes da entrega:** `python marca-dagua/marca_dagua.py aplicar <final_sem_marca.mp4> <final.mp4>`. Detalhes: `marca-dagua/LEIA.md`.

<!-- ganchos -->
## 🎣 Gancho — OBRIGATÓRIO no roteiro e antes do render final
Leia `ganchos/GANCHOS.md`. O formato natural deste estilo é **"a frase que todo mundo diz" no quadro 0** (comentário/opinião em card, palavra-chave destacada) e a virada "enquanto discutem isso, …" até ~5 s. Fala do gancho ≤ 12 palavras até ~1,5 s; algo muda a cada 2–3 s; 25–40 s no total. Escreva 3 ganchos e escolha o mais forte.

## O que é
Um **manifesto curto**: uma tese sobre internet/IA/conteúdo/comportamento, contada em 6–9 "movimentos" visuais em que **cada cena nasce do último estado da anterior** — nunca corte seco, nunca fade genérico. Paleta quase monocromática (grafite, cinza, branco osso) e **um só acento coral** reservado pro clímax/CTA. Ritmo: rápido no começo, uma **pausa/silêncio de verdade no paradoxo** e frase final com peso.

Exemplo: `exemplos/manifesto-feed_ep01_v7.mp4` ("O futuro está ficando descartável", 34 s) + `exemplos/capturas_cenas.jpg`. O `template/` É esse vídeo completo, pronto pra adaptar — leia `references/cenas.md` pra saber o que cada cena faz e como reaproveitar.

## Quando NÃO usar
- Pessoa falando/filmagem real → skill-do-jarvis / moldura-pop / legenda-cinema / etiqueta-brutal.
- Copy de produto com UI calma e fundo claro → kinetic-creme.
- Tutorial técnico com câmera 3D elástica e cor neon → kinetic-noir.
- Analogia com cenário 3D (cidade, prédio, bonecos) → maquete-viva.

## O que pedir ao usuário (só o que faltar)
1. **Tese/roteiro** (ou o tema, e eu escrevo). 12–16 frases curtas, 25–40 s, estrutura: *opiniões comuns → virada → causa → mecanismo → consequência → paradoxo (pausa) → bifurcação → frase final*. **Roteiro original**; se vier referência, copiar a linguagem de movimento, nunca texto/cenas.
2. **Locução**: voz própria, voz por IA (ElevenLabs) ou sem voz (o filme é lido pelas palavras-chave na tela).
3. **Número/título do episódio** (assinatura no topo) e **@/CTA**.
4. **Imagens nos cards?** Padrão = cards procedurais cinza (0 crédito). Opcional: imagens cinematográficas geradas por IA em `public/morphix/` (ver `src/data/morphix-assets.ts`).
5. Acento: padrão coral `#FF633E` (`src/lib/theme.ts` → `C.orange`).

## Pipeline

### 1. Projeto
Pasta `E:\Dropbox\Projetos 2026\VS CODE + CLAUDE\<slug>\` (no PC de outra pessoa: uma pasta de projetos dela). Copie **todo** o conteúdo de `template/` (inclui `.claude/launch.json`) → `npm i` → `npm run sfx:stage` (copia os SFX da biblioteca Ocular se existir; senão **sintetiza** sons com os mesmos ids, e o vídeo renderiza igual — avise que com biblioteca própria fica melhor: `SFX_ROOT=<pasta> npm run sfx:stage` e editar `scripts/sfx-sources.json`).

Frames temporários e testes fora do Dropbox (`C:\Users\LK\AppData\Local\maquete-render\`).

### 2. Roteiro → movimentos
Monte a tabela frase → movimento → transformação de saída (modelo em `references/cenas.md`). Regra: **cada frase tem uma palavra-chave que vira imagem** (REALISTA → bloco que varre a palavra; DESLIZAR → composição inteira desliza; INCRÍVEL → a palavra se multiplica até perder valor). Se a frase não tem imagem, reescreva.

### 3. Locução (se houver)
- ElevenLabs `eleven_v4`, pontuação dá a energia; IA escrita como "iá" no texto pra não ler "A.I.". Mande a prévia do áudio antes de animar.
- Arquivo em `public/audio/voiceover.wav` → `src/data/sfx-cues.ts`: `VOICEOVER.enabled = true` (ducking 0,55).
- Tempos por palavra: `python -I scripts/palavras.py public/audio/voiceover.wav palavras.json "termos"` (da pasta da skill) → ajuste `VO` e `K` em `src/data/script.ts`. **Use o fim de cada pausa** como início da frase seguinte.

### 4. Editar o template (de cima pra baixo)
1. `src/data/script.ts` — `VO` (falas + tempos) e `K` (marcadores de palavra-chave, em frames). **Tudo sincroniza daqui**: cenas, flashes e SFX ancoram em `K`.
2. `src/lib/timing.ts` — janelas `SCENES` (com sobreposição nas transições) e `DURATION` no relógio original.
3. `src/lib/timewarp.ts` — `SPEED`: velocidade de cada trecho (o EP01 foi animado em 45 s e toca em 34 s). Ajuste o ritmo aqui sem reanimar; SFX/voz acompanham sozinhos (`unwarp`).
4. `src/scenes/S1…S9` — uma cena por arquivo. Reaproveite a mecânica e troque textos/objetos (ver `references/cenas.md`). Textos: `MaskReveal` (caractere sobe pela máscara), `WordStagger` (palavras com destaque), `Mono` (micro-texto). Câmera: `CameraRig` + `L3` com `track(f, keys)` e curvas `E.camera / E.recoil / E.anticipate` (`src/lib/motion.ts`).
5. `src/compositions/EP01.tsx` — ordem das camadas e a assinatura `Slate` (EP.XX · TÍTULO).
6. `src/data/fx.ts` — flashes nas transformações (**nenhum** no silêncio do paradoxo).
7. `src/data/sfx-cues.ts` — um som pra cada elemento que entra, pico alinhado ao frame do evento. Ids e regras em `references/som.md`. `npm run cues` gera a planilha `SFX_CUES.csv`.

### 5. Prévia antes do render (obrigatório)
- `npm run studio` (porta 3123) pra conferir na timeline; `node scripts/stills.mjs out/stills <frames...>` gera folha de contato. Revise: texto escondido por highlight, palavra coberta por rastro, máscara vazando, hierarquia da frase final, safe zone.
- `npm run preview` → `out/EP01_preview.mp4` (540×960, áudio masterizado). **Mande pro usuário e espere aprovação.**

### 6. Final
`npm run render && npm run master` → `out/EP01_final.mp4` (1080×1920, CRF 16, true peak ≤ −1,5 dBFS) → marca d'água → entregar. Guarde versões em `versions/vN/` antes de mudanças grandes (o EP01 passou por 7).

## Regras de estilo (não quebrar)
- Fundo `#0B0C0D`, branco osso `#F4F3EE`, cinza `#8B9095`, estrutura `#282B2F`; **coral só no clímax** (card que para, cantoneiras do "perfeito", "SE IMPORTAR.").
- Inter Tight 800–900 pra palavra grande (caixa alta, tracking apertado), 500–700 pra frases; IBM Plex Mono maiúsculo com tracking 0.12em pra rótulos/contadores ("2048 ELEMENTOS", "PUBLICADOS 0013").
- Grão + vinheta sempre (`Atmosphere`), flashes duplos curtos só em transformação.
- Cada elemento tem sua curva e sua mola (`SPR.ui / elastic / heavy / lock`); nada entra linear.
- Cards de feed estilizados, **sem logo/interface real** de Instagram/TikTok.
- O paradoxo precisa de silêncio: trilha e SFX somem, sem flash, sem whoosh.

Detalhes: `references/estilo.md`, `references/cenas.md`, `references/som.md`.
