# Etiqueta Brutal — guia visual

## Paleta (RGB)
| Nome | Cor | Uso |
|---|---|---|
| CREME | 251,244,222 | fundo geral, borda do cartão |
| PAPEL | 255,250,236 | etiquetas, janelas, selos claros |
| TINTA | 20,18,16 | contornos, sombras duras, texto |
| AMARELO | 255,214,58 | destaque padrão, bloco "pergunta", selo da tese |
| VERMELHO | 236,88,60 | negativo / soco ("NADA.", "RUIM", ✗) e marca |
| VERDE_OK | 88,196,120 | positivo (✓, "bem feito", botão concluído) |
| LILÁS | 201,170,245 | fundo de cena de comparação (com pontos), CTA |
| AZUL | 60,90,240 | botões de app, enviar |
| PÊSSEGO | 247,222,204 | barra de título das janelas |

## Tipografia
- **Cera Pro Black** — legendas (58 px), blocos (92–200 px, caixa alta), selos.
- **Cera Pro Bold/Medium** — textos de interface (20–32 px).
- **Georgia / Georgia Itálico** — cabeçalho da marca (62 px) e rodapé "comente".
- **Cascadia Mono** — rótulos técnicos pequenos ("ORÇAMENTO").
- **Times Bold** — só para coisas propositalmente feias (post ruim, panfleto feio).

## Medidas-padrão
- Contorno: etiquetas 4 px, blocos 6 px, caixas de destaque 3 px.
- Sombra dura: deslocamento (s, 1,15·s) em TINTA — etiqueta 7, janela 10, bloco 12.
- Raio: etiqueta 0,22×fonte, janela 22, cartão de vídeo 48 (gancho 44).
- Janela: barra de título 56 px pêssego + 3 bolinhas (vermelho/amarelo/verde) + chip lilás à direita.
- Selo: 14–16 pontas, raio interno 0,80.

## Movimento
- Entrada `pop`: escala 0,55→1 easeOutBack (s=1,9) em 0,28 s, alfa em 0,13 s.
- Saída: escala ×0,8 easeIn + fade em 0,16 s.
- Legenda: cada palavra nova dá um "bump" de 6 % na etiqueta (0,12 s).
- Transições de cena: interpolação do retângulo do cartão (0,34–0,40 s, ease in-out).
- Giro de gancho: 180° em 0,66 s com 3 amostras de rotação misturadas (motion blur) e encolhimento a 86 % no meio.

## Composição 9:16
- Rosto: terço superior — **proibido cobrir**.
- Legenda: y≈1150 (corpo) ou logo abaixo da janela na cena lilás (y≈1112).
- Objetos/janelas: centro em y≈1550.
- Cópias multiplicadas: nas laterais (x≈170 / 910), nunca no eixo do rosto.
