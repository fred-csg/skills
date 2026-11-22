# Som — Maquete Viva

## PADRÃO ATUAL: tudo no ElevenLabs (MCP oficial)
- **Locução**: voz favorita do usuário, modelo `eleven_v4`, pt, `mp3_44100_192`. Um arquivo com o texto inteiro (inclui a CTA).
- **Trilha**: `compose_music`, instrumental (`force_instrumental`), duração ≈ vídeo + 6 s, prompt de clima do nicho (ex. "warm cozy lo-fi, felt piano, pizzicato, 90 BPM, steady, clean ending, no vocals"). Se a música termina antes do vídeo: `music_jump=(corte, volta)` no `mvm.mix` (emenda com crossfade).
- **SFX**: `text_to_sound_effects` 0,5–4 s, descrição concreta em inglês. Comuns prontos em `scripts/molde/sfx/`: whoosh (transição), pop (etiqueta/check), titulo (placa de capítulo), redes (CTA), foto, celular (notificação), porta, apagar.
- **Mix** (`mvm.mix`): voz −17 dBFS RMS; trilha `music_db=-14` com ducking `-9` dB quando há voz (ataque rápido, soltura lenta); SFX normalizados e posicionados por `onset` (cliques), `peak` (impactos) ou `start`; limiter suave; loudnorm −14 LUFS no encode.
- Sem riser/suspense antes de revelação : corte seco + impacto.

Mapa típico: placa de capítulo → titulo; check/etiqueta → pop; câmera grande → whoosh; foto → foto; mensagem → celular; cartões do CTA → redes.

---

## (legado) sons sem ElevenLabs


## De onde vêm os sons
1. **Biblioteca do usuário**, se ele tiver e quiser usar: pastas em `sfx_pasta.txt` (na pasta da skill, um caminho por linha) ou na variável `SFX_PASTA`. `sfx_lib.find(trecho_do_nome)` procura pelo trecho do nome da tabela abaixo; se a biblioteca tiver outros nomes, escolher os equivalentes e trocar em `mix.py`.
2. **Sem biblioteca (ou nome não encontrado):** `sfx_synth.py` gera o som por código com a mesma intenção (impacto, sopro, engrenagem, tique-taque, páginas, moedas, ambiente de rua). Não precisa baixar nada. Para ouvir: `python -I sfx_synth.py teste.wav`.

Os nomes da tabela são da biblioteca original do autor (★ = favoritos dele); servem de referência do tipo de som.

## Mapa evento → som (usado no exemplo)
| Evento | Arquivo (trecho do nome) | Alinhamento | Ganho |
|---|---|---|---|
| Título de capítulo (assinatura) | Camera Clicks, Low Impact, Mech Double Hit ★ | pico em t+0.08 | −9 |
| Abertura / câmera grande | Synth Bass Double Whoosh ★ | pico | −14 |
| Câmera sobe / revela | Multi Small Gear Rotation, Double Low Whoosh ★ | pico | −13 |
| Algo abre (vitrine) | Metal Lever Activation ★ + Small Gear Rotation On Metal Surface ★ | pico / início | −10 / −17 |
| "Deu certo" / ding | Treadmill Start Button, Tone ★ | pico | −15 |
| Papel/panfleto | Book Page Flip ★ (recortes por onset) | onset | −18 |
| Contagem de tempo | Clock From Another World 6 ★ | início, 2.7 s | −12 |
| "Lixo"/quebra | Dry Break Impact, Crispy ★ | pico | −9 |
| Transição pra outro mundo | Time Control Clock, Pendulum Transition ★ | pico | −12 |
| Muitos itens aparecendo | Mech Mini Gears, Camera Switch Buttons ★ | onset | −14 |
| Máquina liga | Mech Mini Gears Rotation 3 ★ | onset | −15 |
| Frenesi / acelerando | Stopwatch That Goes Out Of Control, Metal Clicks, Rising | início (trecho 1.3→7.4 s) | −17 |
| "Parou" / desliga | Assembling Heavy Metal Parts, System Slowing Down ★ | onset | −9 |
| "Constrói" | Agressive Impact, Assembling Metal Parts, Slowing Down 1 ★ | pico | −11 |
| Fechamento | Agressive Impact, Alarm Clock Wing (Weird High Resonance) ★ + Deep Drum Hit | pico | −10 / −8 |
| Post/foto aparecendo | Camera Shutters (Clicky / Cirpsy / Crackling) | pico | −13 |
| Pop de etiqueta | Clicky / Cirpsy Short Shutter | pico | −23 |
| Swipe | Quick Whips (Short Whoosh 7 / 13) | pico | −11/−13 |
| Moeda | OBJGym Barbells Handling, Small Drops (recortes) | onset | −19 |
| Antes do clímax | **nada de riser/suspense** (proibido pelo usuário) — usar corte seco + impacto | — | — |
| Ambiente | AMBUrbn Busy Street, People Passing By (loop) | — | −29 |

★ = da pasta de favoritos. O pacote não tem moeda nem papel amassado: usar recortes.

## Mix
Voz −17 dBFS RMS · limiter suave −1.5 dBFS · master `loudnorm=I=-14:TP=-1.5:LRA=11` no encode (Instagram).
