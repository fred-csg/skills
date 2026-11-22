# Som

## Ids de SFX (`sfx(t, id, ganho, pan, {dur, align, fadeOut})`)
click_short click_metal pop_soft snap_elastic beep_tick whip_a whip_b whip_c whip_d swipe_paper swipe_rl swipe_sand whoosh_exhale reverse_swell impact_soft impact_low final_hit sub_tail tonal_accent bass_mecha gears ticking bed mech_lock riser_pulse riser_sparkle glitch glitch2 glitch3 robot_down servo_init mouse typing glitchy_counter glitchy_bleep bursting_bleep chime msg_bleep app_open tonal_beeps elec_ui stutter_whoosh braam fut_blip 

- Mapa id → arquivo no topo de `scripts/mix-sfx.mjs` (biblioteca de sons do autor; se o usuário tiver uma biblioteca própria, troque os caminhos pelos arquivos dele). Sem biblioteca: `python -I scripts/gerar_sfx.py out/cues.json` gera cada efeito por código em `<projeto>/sfx/<id>.wav` — o mixer usa automaticamente. Qualquer som pode ser trocado por um arquivo com o mesmo nome (ex.: gerado no ElevenLabs `text_to_sound_effects`).
- `whoosh(t, id)` = alinha o PICO do som no corte (use em todo chicote/travessia).
- Sons contínuos (`riser_pulse`, `typing`, `ticking`, `gears`…) aceitam `{dur}`.

## Mapa usado no exemplo
| Momento | Som |
|---|---|
| herói entra no quadro 0 | impact_low + chime |
| objeto voa / pousa | whoosh_exhale, pop_soft, impact_soft + click_metal |
| robótico | glitchy_counter (dur) + servo_init |
| cursor pega a alça | mouse + snap_elastic |
| "ganha vida" | chime |
| acelera → corte | riser_pulse (dur até o corte) + whip_c no pico |
| barra revelando | swipe_sand |
| chuva de itens | tonal_beeps |
| X carimbado | impact_low + glitch |
| código digitando | typing (dur) |
| travessia | stutter_whoosh / whip_c / whip_d |
| comentário publicado | mouse, msg_bleep, bursting_bleep |
| assinatura | sub_tail + chime |

## Mix (`mix-musica.mjs`)
Voz −15 LUFS na frente; SFX −24 LUFS com compressão pela voz; trilha −28 LUFS com ducking forte; master −14 LUFS e limitador. Locução atrasada `OFF` (0,08 s) — o mesmo `OFF` do template.
