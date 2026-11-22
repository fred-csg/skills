# Câmera 3D — como planejar os planos

## Modelo
- `#lens` tem `perspective: 1400px` (origem em 495, 800). Dentro dele, `#world` (cenário) e `#hud` (legendas/palavras grandes).
- Pose da câmera = `p(x, y, d, rx, ry, rz)`:
  - `x, y` — ponto do mundo que fica no centro da tela (495, 800 = neutro).
  - `d` — dolly: positivo aproxima (300 ≈ close; −600 = bem longe). Acima de ~1400 − z o elemento passa da câmera (travessia).
  - `rx` — inclina pra frente (positivo = olhar de cima, o plano vira "chão"; 30–60 deixa a timeline/grade em perspectiva).
  - `ry` — gira em volta (±15–35 dá paralaxe forte). `rz` — rolagem (±3–12, energia).
- Camadas com profundidade: `<div class="L" style="transform:translateZ(z)">` — legenda/elemento herói 130–200, objeto de cena 40–140, painel/gráfico −60…−110. Quanto maior a diferença, mais paralaxe quando `ry` muda.
- HUD (legendas): segue a câmera em parte (rotação × 0,32, deslocamento × 0,12, dolly × 0,35; acima de 450 acompanha inteiro, pra ser atravessado nos voos).

## KEYS — um plano por frase
`[tempo, pose, tipo]` — o tipo diz como a câmera CHEGA nessa pose a partir da anterior:
| tipo | uso | sensação |
|---|---|---|
| `drift` | dentro da mesma frase (seno suave) | câmera viva, nunca parada |
| `ramp` | troca de assunto | rampa de velocidade (lento → rápido → lento) |
| `spr` | chegada com quique | mola (1,6 Hz, 0,6) |
| `wob` | "elástico", exagero | mola frouxa (1,7 Hz, 0,3) |
| `soft` | "chega macio" | mola lenta e amortecida |
| `in` | vai pro corte acelerando | expo-in (travessia, giro pra fora) |
| `cut` | mesma hora do `in` anterior | salta pra pose nova (o corte) |
| `step` | "robótico" | câmera em passos de 8 fps |

Padrão de uma frase: `[início, pose A, 'ramp' ou 'spr']` + `[fim − 0,1, pose A' (deriva), 'drift']`.
Padrão de travessia: `[corte, p(x, y, 1500…1650, …), 'in']` + `[corte, pose longe e girada (d −500…−800), 'cut']` + `[corte + 0,9, pose nova, 'spr']`.

## TR — somados por cima
- `{c, type:'kick', amt, shake}` — tranco no impacto (aproxima `amt*900` e volta com mola) + tremida que some em ~0,3 s. Use em toda batida forte (palavra que cai, clique, X carimbado).
- `{c, type:'whip', dx|dy, dO, f, z}` — chicote lateral/vertical (1400 px). `dO` = duração da aceleração (0,15 s seco; ~1,7 s pra demonstrar "acelera"). `f/z` = mola da chegada.

## Receitas que funcionaram
- Abertura: câmera baixa (`rx −16`) e girada (`ry 30`), orbitando até `ry −20` enquanto o herói entra — 0 s já tem movimento.
- "Mostrar uma linha do tempo": `rx 35–40`, `ry 15–30` — a timeline vira uma pista em perspectiva.
- Seguir um objeto: alvo `x` acompanha o objeto, `ry` aumenta no sentido do movimento.
- Revelar um painel: recuar (`d −70`) e endireitar (`rx ~8`, `ry ~10`).
- Chuva/grade de itens: plano alto (`rx 40–58`) descendo com `spr`.
- Fim: travessia do último elemento → logo vindo de longe e girado (`d −650`, `ry −32`) com `spr`.

## Conferência
Stills nos tempos: início de cada plano + meio de cada `ramp`/`in`. Procure: texto cortado (aproximou demais), elemento herói fora do quadro (alvo errado), quadro vazio depois de corte.
