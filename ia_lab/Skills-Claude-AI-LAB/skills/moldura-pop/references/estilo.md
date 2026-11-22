# Moldura Pop — estilo

## Cores
- Tema (cores + fontes) vem do passo 0 do SKILL.md: `classico` (padrão aprovado, valores abaixo), `ai-lab` (preto #050505 + limão #D7FF3A + Poppins) ou `tema.json` tirado de print/vídeo. As medidas e os movimentos desta página valem para todos.
- `ACC` = cor de destaque (UMA só): contorno da moldura, brilho, palavra do título, pílulas, legenda `acc`, barras. Escolher pela marca/tema (referência: laranja #F38020; exemplo Homem-Aranha: vermelho #E8302A). `ACC2` = versão clara pro brilho/texto em fundo escuro.
- Fundo claro: papel `#FAFAF9` com pontinhos a cada 36 px (−26 de luminância). Texto `#111113`, secundário `#46464C`, linhas `#E4E4E8`.
- Fundo escuro: estilo escolhido no passo 0 (`fundo_escuro` / `MP_FUNDO`). Folha de comparação em `exemplos/amostra_fundos_escuros.jpg`.
  - `grid-cinza`: base `#161617`, grade de 60 px (+13 de luz) com cruzinhas a cada 240 px, luz cinza atrás da moldura (y=40%), vinheta, grão σ 5. Vidro `#28282A`.
  - `cinza-grao`: base `#161616`, luz cinza (y=40%), toque da cor de destaque no topo (8%), vinheta, grão σ 6,5. Vidro `#2A2A2A`.
  - `grid-azul`: base `#0B0F1E`, grade azulada, luz azul `#1E3C8C` no topo, cor de destaque no canto de cima à esquerda (28%), grão σ 4. Vidro `#181E32`.
  - `azul-grao`: base `#0C0F1C`, manchas azul + roxo + destaque, sem vinheta, grão σ 5,5. Vidro `#1A1E30`.
  - `cinza-azul`: grade cinza `#141518` com luz azul no topo, grão σ 5. Vidro `#24262E`.
  - `brilho` (original): `#0E0A0A` + brilho radial da cor de destaque no topo (centro y=16% da altura, 42% de força) + granulado leve. Vidro `#221A19`.
- Vidro escuro (janelas/cartões no escuro): cor do vidro do estilo a 93%, borda branca a 11%.

## Tipografia (fontes do Windows do Lucas)
- Títulos/legenda: **Cera Pro Black/Bold** (geométrica; na referência é uma grotesca tipo Inter Display). Título 100 px, tracking −3%.
- Editorial: **Georgia Itálico condensado a 80%** (simula Instrument Serif). Linha de apoio 46–66 px; palavra de impacto na legenda em CAIXA ALTA 1,32×.
- Caixa alta espaçada (header): Cera Black 31 px, tracking +16%.
- Mono (rótulos, "COMENTA", "/mês"): Cascadia Mono 20–34 px, tracking +20–30%.
- Ícones: Segoe MDL2 Assets (traço fino, igual ao da referência). Mapa em `mp.ICON`.
- Se quiser mais fiel: instalar *Instrument Serif* e *Inter* (Google Fonts, OFL) e trocar em `FONTES` (pedir permissão antes de baixar).

## Moldura
- CARD: largura 830 (margem 125), topo 960–1040, raio 64, desce além da tela. Contorno 4 px na cor + brilho desfocado 16 px, mais forte em cima e sumindo pra baixo. Sombra suave (claro 30%, escuro 55%).
- Cabeça vaza ~100 px acima da borda: máscara × (acima da borda) × (faixa lateral do cartão ±10 px). O contorno passa POR TRÁS do cabelo.
- Tamanho da cabeça: `head_w` = largura do rosto/cabelo em px finais (CARD 420, FULL 520, CIRCLE ≈1,25·r). O motor garante que o vídeo sempre cobre a moldura (zoom mínimo + trava de borda) — se a fonte for muito fechada, a cabeça fica maior que o pedido.
- CIRCLE: anel 5 px na cor + brilho; nunca vaza.

## Movimento
- Tudo com curva: `eout5` pra posição, `eback(2.2)` pra pop, `eio5` pra transições. Nada linear.
- Entrada padrão: desfoque 14→0 + sobe 26 px + escala 0,96→1 em 0,42 s.
- Pop: escala 0,6→1 com overshoot + desfoque 6→0.
- Wipe do título: máscara gradiente da esquerda pra direita (0,7 s) — sensação de "letra por letra".
- Saída: desfoque +10, encolhe 6%, some em 0,22 s.
- Badges flutuam ±6 px (seno lento) com rotação leve acompanhando.
- Transição de cena: moldura e fundo interpolam juntos em 0,44 s.
