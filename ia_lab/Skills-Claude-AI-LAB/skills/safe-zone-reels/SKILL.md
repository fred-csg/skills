---
name: safe-zone-reels
description: Guia OBRIGATÓRIO de safe zone para qualquer vídeo/imagem vertical 9:16 (Reels, TikTok, Shorts, capas) — medidas reais da interface do Instagram (topo 240, base 1500, laterais 95, botões x≥870 de y 800 a 1500), faixas recomendadas pra título/herói/legenda, script que confere caixas e gera folha de quadros com a guia por cima. Use SEMPRE antes de produzir o visual em qualquer skill de vídeo (maquete-viva, moldura-pop, etiqueta-brutal, kinetic-creme, skill-do-jarvis) e quando o usuário falar de "safe zone", "área segura", "elemento tampado pelo Instagram", "legenda coberta pelo @".
---

# Safe zone Reels (v2, out/2026)

Leia [SAFE-ZONE.md](SAFE-ZONE.md) — é a fonte única das medidas. Resumo:

- **Topo** livre até y 240 · **base** a partir de y 1500 · **laterais** 95 px · **botões** x ≥ 870 de y 800 a 1500.
- Usar a tela toda: fundo, cenário e vídeo podem passar das linhas; só o **essencial** (texto, legenda, números, rosto/objeto explicado, selos) fica inteiro dentro.
- Faixas: título y 250–430 · herói y 430–1150 · legenda y 1150–1470 (centro x ≈ 482).
- Capa: grade do perfil mostra só y 240–1680.

## Ferramentas
- `python safe_zone.py overlay [saida.png]` → overlay transparente (já incluso: `safe_zone_overlay_1080x1920.png`).
- `python safe_zone.py caixa x0 y0 x1 y1` → diz o que a caixa invade.
- `python safe_zone.py checar video.mp4 [--tempos 1,5,9] [--saida folha.jpg]` → folha de quadros com a guia.
- Em Python: `from safe_zone import TOPO, BASE, LAT, BOT_X, BOT_Y, SLOTS, problemas`.

## Quando aplicar
Antes de posicionar qualquer elemento (planejamento) e de novo antes do render final (folha de conferência). Cada skill de vídeo do pacote traz uma cópia em `safe-zone/`.
