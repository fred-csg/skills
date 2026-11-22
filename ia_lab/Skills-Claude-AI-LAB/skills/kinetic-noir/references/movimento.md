# Movimento — números e funções do template

## Funções
- `spr(tau, f, z)` — resposta de mola amortecida 0→1 (overshoot). Entrada de letra/palavra: `f 2.4–2.9, z 0.45–0.6`. Mola frouxa: `z 0.28–0.32`. Pouso suave: `f 0.85, z 0.9`.
- `E.ioE` — rampa de velocidade (o "speedrun"): lento → muito rápido → lento. Use pra mover algo de A até B com energia (agulha da timeline, câmera entre planos).
- `E.iE` — só acelera (saída pro corte). `E.oE` — só freia (desfoque sumindo).
- `bez(u, x1, y1, x2, y2)` — easing de Bézier (estilo CSS) — dá pra animar a própria curva e o objeto seguir.
- `wordIn(s, t, lag)` — palavra sobe 46 px com mola + desfoque 10→0 em 0,26 s.
- `slam(s, t, de, rot)` — palavra bate: escala 1,7→1 com mola + desfoque 22→0.
- `letterUp(s, t, dy, rot)` — letra a letra (itálicos, sufixos).
- `tf(el, transform, lag)` — aplica o transform somando o **arrasto**: o elemento fica onde a câmera estava `lag` s atrás (×0,4). Letras: `0.008 + i*0.006`.
- `blur(el, bx, by)` — desfoque direcional (filtro SVG por elemento).

## Tempos
- Entrada de palavra/letra: 0,25–0,35 s. Stagger de letras: 0,02–0,04 s. Saída de legenda: 0,15 s (sobe 60 px + desfoque).
- Plano de câmera: chega em 0,4–0,6 s (`ramp`/`spr`), deriva até a próxima frase.
- Chicote seco: 0,15 s de aceleração; chegada com mola 1,5 Hz.
- Travessia: 0,22–0,34 s de aceleração.
- Corte ~0,06–0,1 s antes da palavra nova (a fala "puxa" a imagem).

## Motion blur
- Render: 30 fps × 8 subquadros com obturador 0,9 (tmix no ffmpeg). Movimento rápido borra sozinho, como câmera de verdade.
- Somado: desfoque do `#lens` pela velocidade da câmera (px/s ÷ 520 + giro × 24 px/° ÷ 520; dolly ÷ 650).
- Objetos rápidos (bolinha, barra, rolagem): desfoque próprio pela velocidade (`|v| / 260`).

## Truques que funcionaram
- "Robótico": quantizar o tempo (`Math.floor(t*8)/8`) do objeto, das letras e da câmera (`step`).
- "Elástico": letra com `scale(1-0.35j, 1+0.6j)` onde `j = 1 - spr(tau, 2.2, 0.28)` (gelatina).
- Squash & stretch da bolinha pela velocidade: `sx = 1 + |v|/3200`, `sy = 1/sx`.
- Grade em onda: atraso pela distância ao centro (`d*0.0012`) + `sin(t*4 - d*0.02)` contínuo.
- Revelar palavra com barra: `clip-path` acompanhando a barra; a barra depois vira o sublinhado (mola).
- Tremida no impacto: `shake * sin(tau*71) * exp(-tau*11)`.
