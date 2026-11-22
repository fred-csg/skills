# Changelog — skill-do-jarvis

Autor: Lucas Sena.

## 2026-10-14 — versão de venda atualizada
- Pacote refeito a partir da versão em uso (inclui o estilo CLEANSTILL e o SFX só da biblioteca do usuário).
- Removidos caminhos fixos e comentários pessoais: `pasta_sfx` volta a ser perguntada na primeira execução; nomes de arquivos de SFX específicos viraram buscas por tipo (keyboard, mouse click, UI app open).
- `config.json` pessoal não vai no pacote (só `config.example.json`).

## 2026-10-09 — estilo CLEANSTILL
- Novo estilo de motion **cleanstill** aprendido de um vídeo de referência (anúncio 60 s): `references/cleanstill.md` (paleta medida, tipografia Bricolage Grotesque + Instrument Serif italic + Inter, palcos, catálogo de 20+ recursos, transições, estrutura de 12 beats, layout 16:9/9:16, som, checklist).
- Novo template `assets/cleanstill-template/` (Remotion): componentes `PastelHaze`, `SkyClouds`, `NightArc`, `Line`/karaokê/palavra-chave com brilho/destaque selecionado, `FocusList`, `ZoomExit`, `Impact`, `GlassPill`, `PricePill`, `PaperCard` com seleção, `Cursor`, `Laptop`, `Carousel3D`, `ThumbWall`, `SlotCard`, `LensReveal`, transições `Bloom`, `BlobReveal`, `RayBurst`, `CrossBlur`; demo `CleanstillDemo` (16:9 e 9:16) testada com render.
- SKILL.md: toda peça com motion agora oferece a escolha Jarvis padrão × Cleanstill. Dissolve em retícula da referência excluído (regra de "sem mosaico").

## 2026-10-08 — versão para distribuição
- `config.example.json` + instrução no SKILL.md: na primeira execução a skill pergunta pastas, cor de acento, look padrão e idioma e grava `config.json`. Nenhum caminho fixo no texto da skill. Entregas: padrão = Área de Trabalho do sistema (resolvida de verdade, inclusive Desktop no OneDrive).
- Referências pessoais removidas do SKILL.md e das references ("o usuário" no lugar do nome; caminhos viram valores do config; o vídeo de referência virou "exemplo aprovado").
- Removido todo o conteúdo do ambiente na nuvem do claude.ai (ponte de arquivos, .bat, partes de 24 MB, C2PA, 2 CPUs, proxy, pipeline HTML/GSAP/Playwright). A skill roda em qualquer PC com Claude Code + Node.js.
- SFX: padrão passa a ser SFX sintetizado por código (`assets/sfx-gen/` + `references/sfx-codigo.md`); biblioteca própria só opcional.
- Ferramentas só via npm: `ffmpeg-static` (ffmpeg completo, verificado no Windows com zscale/tonemap/eq/drawtext/tile/silencedetect…), `npx remotion ffprobe`, tracking em Node com `@techstark/opencv-js` (substitutos para `goodFeaturesToTrack`/`estimateAffinePartial2D`). Python só opcional (recorte da pessoa).
- SKILL.md enxuto (progressive disclosure), só Claude Code local com Remotion. Detalhes movidos para `references/`: `tracking.md`, `segmentacao.md`, `icones-3d.md`, `sfx.md`, `master-camadas.md`, `plano-motion.md`.
- Novo `LEIA-ME.md` de instalação.
- `estilo-visual.md`, `remotion-3d.md` e o template mantidos; só trocados nome/caminhos pessoais por config (e versão do Remotion alinhada ao template, 4.0.534).
- Regra fixa mantida: nunca escrever o nome do usuário no vídeo.

## 2026-10-08 — base
- Skill antiga `video-edit-motion` (nuvem do claude.ai) virou `skill-do-jarvis` com motor Remotion + three.js local, template `assets/remotion-3d-template` (planta 3D) e o guia `references/estilo-visual.md` (VIDRO padrão, HOLOGRAMA secundário).
