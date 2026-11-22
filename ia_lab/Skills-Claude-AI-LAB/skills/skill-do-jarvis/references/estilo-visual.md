# Estilo visual padrão

Aprovado em 2026-10-08 (teste "planta 3D"): **VIDRO** é o estilo principal e **HOLOGRAMA** é o secundário. Vale para TODA edição, a menos que o pedido diga outra coisa ou o usuário escolha o estilo **Cleanstill** (`references/cleanstill.md`), que tem paleta, tipografia e transições próprias. Este arquivo é autossuficiente: não depende de nenhuma pasta externa.

## 1. Paleta
| Token | Cor | Uso |
|---|---|---|
| fundo-centro | `#13284f` | gradiente radial do fundo (centro) |
| fundo-borda | `#050b1a` | gradiente radial do fundo (bordas) |
| grid | `#ffffff` @ 8–12% | grid fino de fundo (chão 3D ou overlay 2D) |
| gelo (acento VIDRO) | `#bfeaff` (ou `cor_acento` do config) | arestas, linhas, HUD, cotas, texto de etapa |
| ciano (acento HOLOGRAMA) | `#7fe3ff` | arestas e preenchimentos do holograma |
| texto | `#F2F4EE` | títulos e números |
| destaque | `#D7FF3A` | só pontinhos de destaque (1–2 por cena), nunca como cor dominante |
| quente | `#ffd89a` | luzes que "acendem" no final (abajures, glow de fechamento) |

- **Peça só de motion (sem filmagem):** fundo azul-escuro em gradiente + grid branco fino. Preto puro só se pedirem.
- **Sobre filmagem (vídeo falado):** o vídeo é o fundo. Os overlays usam vidro/holograma com acento gelo/ciano no lugar do verde-limão antigo.

## 2. Look VIDRO (padrão)
- 3D (three.js): `MeshPhysicalMaterial` com `transmission: 1`, `thickness: .35`, `ior: 1.45`, `roughness` .02–.12 (móveis até .45), `clearcoat: 1`, `attenuationColor: #9fc8ff`. Arestas com `EdgesGeometry` + `LineBasicMaterial` gelo (opacidade .85). Sem sombras projetadas.
- Elemento que brilha (contorno, lâmpada, destaque) deve ser `transparent: true`, para não aparecer borrado dentro do vidro.
- Precisa de `scene.background` (textura de gradiente) para o vidro ter o que refratar.
- Chão: escuro e brilhante (`#0c1a36`, roughness .18, metalness .55) com linhas finas a cada 0,5 m.
- 2D/HTML (cards, HUD sobre vídeo): `background: rgba(10,20,42,.5)`, `backdrop-filter: blur(18px)`, borda 1.5px gelo a ~33%, cantos 24–32px, sombra `0 30px 80px rgba(0,0,0,.45)`, um reflexo diagonal sutil (gradiente branco 6% → 0) no topo. Referência de clima: cartões de vidro translúcido "Tony Stark", com o assunto visível por trás.

## 3. Look HOLOGRAMA (secundário)
- Quando usar: dados/tecnologia/IA, scan, "projeção", explicação técnica, transição entre ideias, ou como fase "blueprint" antes de virar vidro.
- 3D: `MeshBasicMaterial` ciano `#7fe3ff`, `transparent`, opacidade .08–.3, `depthWrite: false`, `side: DoubleSide` + arestas ciano fortes (opacidade 1). Nenhuma luz necessária.
- 2D: linhas ciano finas, preenchimento ciano 6–12%, scanline e leve flicker (opacidade ±8%, nunca piscando forte).
- Combinação forte: começar em holograma/blueprint e "materializar" em vidro (crossfade de material + arestas que permanecem).

## 4. Movimento (regras fixas)
- Keyframes profissionais: sempre com ease in/out (inOut cubic, out back nas entradas, bounce só em objeto caindo). Nunca linear, nunca aparecer/sumir seco.
- Texto entra letra por letra (cada caractere com fade + translateY 18px + blur 6px → 0, stagger ~1 frame).
- Câmera 3D aprovada: topo → gira → deita em perspectiva → órbita lenta contínua (curvas sobrepostas, sem parar seco).
- Montagem: estrutura sobe com out back em stagger de ~6 frames; objetos montam um por um; no final as luzes quentes acendem.
- **Transição em mosaico/pixelate/blocos coloridos é PROIBIDA** em qualquer peça (fica amador e datado). Usar corte, whip pan com blur, flash ou glitch curto.
- Minimalista com detalhes bem escolhidos: no máximo 1 card + 1 elemento de detecção + 1 objeto 3D grande por vez.

## 5. HUD padrão
- Cantoneiras nos 4 cantos (acento), barra de progresso fina no topo com glow, rótulo de etapa `01 · NOME` com glow suave, bússola/ícone pequeno no canto superior direito, card de vidro de fechamento com count-up e chips.
- **Nunca escrever o nome do usuário (nem o nome da skill/autor) no vídeo.** Marca só se o pedido mandar.
- **Tipografia: SEMPRE Poppins** (`@remotion/google-fonts/Poppins`, baixada e embutida no render). Texto comum Bold 700, destaques e palavras-chave Black 900, rótulos pequenos SemiBold 600 com letter-spacing largo. Nada de fonte fina: peso 500 some no celular. Outra fonte só se o usuário pedir.

## 6. Como reproduzir rápido
Copiar `assets/remotion-3d-template/` (já tem os looks `vidro`, `fosco`, `cromado`, `holograma` em `src/scene/looks.ts`) para a pasta do projeto, rodar `npm install` e trocar os dados de cena em `src/scene/data.ts`. Detalhes técnicos em `references/remotion-3d.md`.
