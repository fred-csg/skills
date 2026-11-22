# Som — Manifesto Feed

- `src/data/sfx-cues.ts`: cada cue = `{scene, at: K.palavra + n, sfx, vol, pan?, fadeIn?, fadeOut?, maxDur?, align?, trimSec?, why}`.
- O mixer (`SoundTrack.tsx`) alinha o **PICO** de cada som ao frame do evento (`align: 'start'` pra loops), converte pro tempo final (`unwarp`) e faz ducking quando há voz.
- `npm run cues` → `SFX_CUES.csv` (planilha com justificativa de cada som).
- `npm run sfx:stage` → copia da biblioteca (Ocular Ultimate Sound FX Bundle) ou sintetiza. Variantes `_L/_R` pros sons espaciais (lista `panned` em `scripts/sfx-sources.json`).

## Ids disponíveis
cliques/UI: `click_short`, `click_single`, `click_metal`, `pop_soft`, `snap_elastic`, `beep_tick`, `glitch`, `mech_lock`
movimento: `whip_a…d`, `swipe_paper`, `swipe_rl`, `swipe_sand`, `whoosh_exhale`, `airy_sweep`, `reverse_swell`
peso: `impact_soft`, `impact_low`, `sub_tail`, `final_hit`, `tonal_accent`
textura: `gears`, `ticking_loop`, `riser_pulse`, `riser_sparkle`, `bed` (cama tonal)

## Regras
- **Todo elemento que entra tem som**, mesmo que levíssimo (0,06–0,15). Microinterações (curtida acendendo, camada aplicada) = `click_metal`/`beep_tick` baixos.
- Com locução: SFX bem abaixo da voz (pico ~16 dB abaixo, p95 ~21 dB abaixo). Sutil, mas audível — medir antes de entregar.
- **Padrão do Lucas: sem trilha** → zere o envelope de `BED` (ou remova o `<Audio>` da cama) e não use riser crescendo antes de revelação. Pra compradores do pack, a cama é opcional.
- Paradoxo: tudo some (cama em 0, sem whoosh) pro silêncio pesar.
- Master: `npm run master` (ganho + limitador, true peak ≤ −1,5 dBFS; EP01 ficou em −18,7 LUFS sem voz).
