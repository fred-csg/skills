# Som — COMPILED SELECTIONS + CONSTRUÇÃO (Cinematic Stone), só em cima dos elementos

## ⭐ Dois sons que o Lucas AMA (usar SEMPRE)
- **`m_build1`** = `ROCKBrk_Dry Break Impact, Crispy, Small Rise And Hit` (Ocular › Cinematic Elements › **Cinematic Stone**): subida curta + batida crocante, "tecnológico, de construção". Vai no nascimento do mascote e nos momentos principais.
- **`m_build`** = 12 irmãos dele da mesma pasta (Short Rise and Hit, Organic Stones, Molten Rocks + Electronic Whistling, Tonal Scratchs, Crispy Clicks...), recortados em volta da batida (`WIN` no mix-sfx). Vai em TODO card/bloco/elemento que se monta. Use `whoosh(t, 'm_build')` pra a batida cair no elemento.
- **`m_pop`** = pops do **Reel Sumama** (`COMPILED SELECTIONS/UI POP - Reel Sumama (sound design Drive)`, 17 pops): pop principal de tudo que surge. Os do Timi ficaram em `m_popt`.


**Regra do Lucas (23/10/2026):** usar apenas `E:/Dropbox/ADDONS/SFX/COMPILED SELECTIONS` (raiz + `UI MOTION - Reel Timi` + `MECANICOS - Reel Alvin Juan` + `avulsos`). Som curto e criativo em cada elemento que entra/se mexe. **Nada de ambiência, palmas, digitação longa, riser, sopro contínuo.** Os favoritos longos da raiz (mecânicos, pedra, água) entram cortados com fade (`TRIM` no `mix-sfx.mjs`).

`sfx(t, id, ganho, pan)` · `whoosh(t, id)` alinha o pico no corte. Cada id tem várias variações e o mixer alterna sozinho.

| id | de onde (COMPILED SELECTIONS) | usar em |
|---|---|---|
| `m_pop` (8) | UI MOTION pops | elemento aparecendo, "?", balão |
| `m_click` (19) | UI MOTION clicks + avulsos HIT | ícones, barras, rótulos, envio |
| `m_swish` (4) | UI MOTION swish | card entrando, gesto de mão (baixinho) |
| `m_whip` (4) | UI WHOOSH + MECÂNICOS whoosh | transição, deslocamento do mascote |
| `m_impact` (5) | UI impacts + avulsos IMPACT | algo assentando com peso |
| `m_mec` (4) | MECÂNICOS cliques | check, etapa, letra assentando |
| `m_rajada` (2) | MECÂNICOS click x5 / riser+cliques | texto digitando, cronômetro, contagem |
| `m_catraca` (2) | MECÂNICOS catraca | lista abrindo, desmontar |
| `m_shutter` (5) | MECÂNICOS obturador | troca de capítulo |
| `m_hit` (3) | raiz: Rock Dry Break, Camera Clicks Low Impact, Metal Lever | título batendo, clímax, nascimento |
| `m_sparkle` (3) | raiz: Treadmill Button Tone, Mini Gears Camera Switch | acerto, palavra-chave, piscadinha |
| `m_magic` (3) | raiz: Mini Gears Rotation, Multi Gear + Low Whoosh, Synth Bass Gears | algo voando/se transformando |
| `m_morph` (3) | raiz: Rocks Multi Whoosh, Pendulum Transition | mudança de forma |
| `m_bell` (2) | raiz: Alarm Clock Wing | número, resultado, "show" |
| `m_bubble` (1) | raiz: WATRBubl (0,4 s) | pousinho do mascote |
| `m_paper` (1) | raiz: Book Page Flip (0,5 s) | documento |
| `m_assemble` (2) | raiz: Assembling Metal Parts, Rock Yielding | desmontar/montar |

Automáticos no template: deslocamento do mascote (`MP`) → `m_whip` + `m_bubble`; gesto (`HK`) → `m_swish` 0.25; capítulo (`CH`) → `m_shutter`.

## Mix
`mix-final.mjs`: voz −15 LUFS, SFX **−23 LUFS** (pico ≈ 10 dB abaixo da voz), master −14. Sem trilha.
