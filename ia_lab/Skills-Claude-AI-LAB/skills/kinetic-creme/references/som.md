# Kinetic Creme — som

## Princípio
Som de interface: leve, seco, curto. Whoosh só nos cortes, um impacto só no carimbo, "ding" só na DM. Se tiver locução, ela manda; SFX ficam por baixo.

## Mapa cue → arquivo (em `scripts/mix.py`, dict `SOUNDS`)
| Cue | Onde nasce | Arquivo | Alinhamento | Ganho |
|---|---|---|---|---|
| `whoosh` | todo corte de cena | Ocular · Quick Whips 3/7/12/16 (alternando) | pico no corte | −9 dB |
| `whoosh_soft` | janela entrando | Quick Whips 5/9 | pico +0,25 s | −17 dB |
| `swipe` | risco da frase | Quick Whips 14/19 (cortado 0,6 s) | pico +0,12 s | −19 dB |
| `pop` | pílula, ícone, celular | Ocular · Camera Shutters "Very Short Click" / "Short Click" | início | −11 dB |
| `flick` | cards jorrando (1 a cada 3) | "Pre Shifted Very Short Metal Click" | início | −20 dB |
| `type` | digitação (código, comentário) | Very Short Click / Metal Click alternando | início | −23 dB |
| `tick` | contadores | Metal Click, decrescendo | início | −26 dB |
| `click` | "Publicar" | "Single Click Shutter" | início | −10 dB |
| `impact` | carimbo | **favorito** `COMCam_Camera Clicks, Low Impact, Mech Double Hit` | início | −5 dB |
| `ding` | DM enviada | **favorito** `MACHGym_Foley Kit, Treadmill Start Button, Tone` | início | −9 dB |

Pastas da biblioteca do autor (opcionais; sem elas o `mix.py` gera os sons por código): favoritos `COMPILED SELECTIONS` (usar primeiro); Ocular `...\The Ultimate Sound FX Bundle\The Complete Whooshes Collection\Quick Whips` e `...\The Complete Devices Collection\Camera Shutters`. O acervo não tem "pop" de UI nem notificação — os cliques curtos de câmera fazem esse papel.

## Mix
- Voz (`--voz`): normalizada a −17 dBFS RMS. Trilha (`--trilha`): −27 dB com voz, −21 sem.
- Teto de pico ~−1 dBFS. Sem loudnorm quando é só SFX (ele levantaria os cliques).
- Proibido: riser/suspense crescendo antes de revelação; SFX sintetizado.
- Não dá pra ouvir daqui: sempre pedir pro usuário escutar e dizer se algum som está alto/baixo; ajustar o ganho no `SOUNDS`.
