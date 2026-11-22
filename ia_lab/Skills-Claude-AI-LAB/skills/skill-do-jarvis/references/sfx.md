# SFX — quando usar, mix e entrega

## Fonte
- **SEMPRE a biblioteca do usuário em `pasta_sfx`** (config.json). Listar as subpastas primeiro: favoritos/avulsos curados (UI, teclado, mouse, whooshes) têm prioridade sobre pacotes grandes.
- **RISER/SUSPENSE PROIBIDO**: nada de crescendo antes de revelação (soa clichê). Durante "processando/gerando" usar um som de UI (contador/glitch curto).
- Digitação/lettering letra por letra SEMPRE leva som de teclado (procurar `keyboard`/`typing` na biblioteca; detectar as rajadas pelo envelope e recortar a que cobre o tempo da digitação, fade 20 ms). Clique de cursor: `mouse click`. Janela/app abrindo: `UI app open`/`pop`. **Nunca sintetizar SFX por código** (soa artificial).
- Fluxo: listar as coleções, escolher pelo nome do arquivo, fazer stage (cópia na pasta do projeto) só do que vai usar, converter para wav 48k estéreo (ffmpeg com `-nostdin`), medir o pico de cada som e posicionar o arquivo para o PICO cair no frame do evento. Mixar com ffmpeg (adelay/volume/amix) ou com `<Audio>` no Remotion.
- Mapa rápido (se a biblioteca tiver o Ocular Sounds Ultimate Bundle): whoosh/whip → `The Complete Whooshes Collection` (Quick Whips, Short Whooshes); impacto → `The Complete Impacts Collection` (Deep Impacts, Bass Drops); glitch/UI digital → `The Complete Sci-Fi Collection/Sci-Fi Glitches`; clique/botão/flash → `The Complete Devices Collection/Camera Shutters`; ambiências → `The Complete Ambiences Collection`; foley → `The Complete Foley Collection`.
- Teclado e blips de UI costumam estar nos avulsos (o Ocular não tem). Nunca sintetizar. Nunca baixar sons de sites sem pedir.

## Regra de sentido (feedback de reprovação)
SFX "aleatórios e sem sentido" já reprovaram uma edição. Cada som precisa casar com um evento visual claro E com o significado:
- whoosh só em movimento/transição;
- impacto só em punch/revelação grande;
- glitch só em glitch;
- click/blip em UI acendendo;
- riser: NUNCA (proibido pelo usuário).

Menos é mais: nada de som em todo elemento pequeno. Alinhar o PICO do som ao frame do evento.

## Mix
- Bus de SFX ~0.42 com ducking pela voz (−40% quando fala), tanh suave, `loudnorm` −14 LUFS, TP −1.2 (ffmpeg do `ffmpeg-static`).
- Sempre entregar os SFX separados (SFX_USADOS/ + SFX_CUES.csv) para o usuário ajustar no editor.
