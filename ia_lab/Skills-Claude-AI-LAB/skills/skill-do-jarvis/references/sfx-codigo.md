> **APOSENTADO em 2026-10-12:** SFX sintetizados soaram artificiais. Todo som vem da biblioteca em `pasta_sfx` (ver `sfx.md`). Este arquivo fica só como histórico; não usar.

# SFX por código (padrão da skill)

Todo som é sintetizado por `assets/sfx-gen/sfx.mjs` (Node puro, zero dependências, ~5 s para 15 s de áudio). Nenhuma biblioteca de SFX é necessária. Se o usuário pedir para usar a própria pasta de SFX, perguntar o caminho e usar os arquivos dele; caso contrário, sempre por código.

## Uso
1. Copiar `assets/sfx-gen/sfx.mjs` para `<projeto>/sfx/`.
2. Escrever `<projeto>/sfx/<peca>-cues.mjs`: `export default (variante) => ({duration, name, cues: [{t, s, p, g, send, bus}]})`.
   - `t` em segundos (= frame / fps), lido da MESMA timeline da animação (constantes `T`, lista de itens). Nunca chutar tempo.
   - `s` = som; `p` = parâmetros; `g` = ganho (0–1); `send` = reverb (0–1); `bus` = stem onde ele cai.
3. `node sfx/sfx.mjs sfx/<peca>-cues.mjs public/sfx <variante>` → `public/sfx/<name>.wav` (mix, pico −1 dBFS), `public/sfx/stems/<name>/*.wav` (stems alinhados para o Premiere) e `<name>-cues.csv`.
4. No Remotion: `<Audio src={staticFile('sfx/<name>.wav')} />` na composição; render com `--audio-bitrate=320k`.
5. Conferir SEM ouvir: desenhar a forma de onda do mix e de cada stem com marcação de segundos (Python+PIL ou canvas) e checar se cada som cai no evento certo, se nada domina e se não há buraco. Ajustar ganhos e regenerar (é instantâneo).

## Sons disponíveis (`SOUNDS`)
| som | o que é | quando usar |
|---|---|---|
| `pad` | cama sonora (acorde Em9, filtro respirando, fade in/out) | fundo de peça só de motion, ganho .5–.6 |
| `glass` | "tim" de vidro (parciais inarmônicos) | look VIDRO: objeto aparecendo, chip, card, acorde final |
| `digi` | blip digital quadrado + bitcrush + eco | look HOLOGRAMA: os mesmos eventos do `glass` |
| `blip` | blip de UI limpo | cota, botão, ícone acendendo |
| `tick` | clique curtinho | rótulos, contador (count-up), digitação |
| `scan` | varredura com tremolo | linhas/blueprint desenhando, scan de holograma |
| `whoosh` | ruído com banda varrendo + pan | movimento de câmera, transição, card entrando |
| `riser` | crescendo subindo até a revelação | antes de impacto/revelação grande |
| `impact` | sub com queda de pitch + corpo + clique | 1 por virada grande (estrutura subindo, revelação) |
| `thump` | baque grave curto | peças encaixando, objeto aterrissando (ganho baixo) |
| `swell` | acorde quente crescendo | luzes acendendo, fechamento |

## Regras de sentido (as mesmas da edição)
- Cada som casa com um evento visual claro E com o significado. Whoosh só em movimento, impacto só em revelação grande, tick/blip só em UI, riser só antes de revelação.
- Menos é mais: elementos pequenos repetidos ganham som baixinho (thump .2–.3) ou nenhum.
- Montagem em sequência = melodia: dar a cada item uma nota da escala pentatônica de Mi menor (`[76,79,81,83,86,88,91,93]`) subindo, para casar com o pad em Em9.
- Alinhar ao frame do evento visível (ex.: objeto que cai com bounce toca na 1ª batida no chão ≈ início + 9 frames de 24; objeto que sobe toca em início + 4).
- Look VIDRO → `glass`; look HOLOGRAMA → `digi` + `scan` mais alto.
- Mix: pico normalizado em −1 dBFS, limitador suave (tanh), reverb Freeverb no bus de send. Peça com voz: ducking de −40% no bus de SFX enquanto há fala.

## Exemplo completo
`assets/remotion-3d-template/sfx/planta-cues.mjs` (planta 3D: pad, scan, rótulos, whoosh da câmera, riser → impacto nas paredes, baques, melodia dos móveis, swell das luzes, ticks do contador, acorde final).
