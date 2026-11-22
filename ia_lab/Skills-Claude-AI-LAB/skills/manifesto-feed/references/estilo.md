# Estilo — Manifesto Feed

## Paleta (`src/lib/theme.ts`)
| token | cor | uso |
|---|---|---|
| bg | #0B0C0D | fundo |
| white | #F4F3EE | palavra grande, frases |
| gray | #8B9095 | micro-texto mono, rótulos |
| struct | #282B2F | grades, linhas, estrutura |
| panel / panel2 | #141618 / #1B1E21 | cards |
| orange (acento) | #FF633E | SÓ clímax: cantoneiras do "perfeito", card que para, "SE IMPORTAR." |

Thumbnails procedurais em 8 tons de cinza (`FeedCards.tsx`): horizonte+sol, blocos editoriais, anéis, retrato abstrato, diagonais — determinísticas pelo `seed`.

## Tipografia
- **Inter Tight** 800–900, caixa alta, tracking negativo: palavra-herói (MAIOR, DESLIZAR, INCRÍVEL).
- Inter Tight 500–700: frases dos comentários e frase final.
- **IBM Plex Mono** maiúsculo 20–24 px, tracking 0.12em, cinza: contadores e rótulos ("2048 ELEMENTOS", "REFINANDO 0006", "01 VELOCIDADE").
- Destaque de palavra: bloco branco que varre (texto vira escuro) ou caixa invertida.

## Movimento (`src/lib/motion.ts`)
- Curvas por função: `snap/outExpo` (objetos pequenos), `camera/cameraSoft` (câmera), `recoil` (recuo violento), `anticipate` (recua antes de ir), `overshoot` (assenta passando).
- Molas por elemento: `ui`, `elastic`, `heavy`, `lock`, `soft`.
- `kick()` = reação a impacto; `noise()` = deriva orgânica; `rng/hash` = tudo determinístico (render igual sempre).
- Câmera 2.5D (`CameraRig`): x/y/z, rotX/Y/Z, zoom, perspectiva 1800; mundo com `L3`.
- `OrbitLight` = luz que percorre o contorno de um objeto antes dele se transformar.
- Flashes: duplo pulso + bloom em `screen`, só nas transformações.
- Grão de filme 6% + vinheta em todos os quadros.

## Ritmo
- 25–40 s. Começo rápido (time-warp 1,2–1,45×), **pausa real no paradoxo** (sem som, sem flash), frase final lenta com ~1,4 s de repouso.
