# Moldura Pop — som

Base: **voz original** em 0 dB. SFX **sutis** (−14 a −25 dB) — o vídeo é premium/limpo, o som só "dá textura" a cada coisa que aparece. Sem música por padrão (se usar: −26 dB com ducking).

De onde vêm os sons (`sfx_lib.find` já faz):
1. **Biblioteca do usuário**, se ele tiver e quiser usar: pastas em `sfx_pasta.txt` (na pasta da skill, um caminho por linha) ou na variável `SFX_PASTA`. Procura pelo trecho do nome da tabela abaixo; se a biblioteca dele tiver outros nomes, escolher os equivalentes e trocar em `mix.py`.
2. **Sem biblioteca (ou nome não encontrado):** o som é **gerado por código** (`sfx_synth.py`) com a mesma intenção (clique, impacto duplo, sopro, sininho, digitação, tique-taque). Funciona em qualquer computador e não precisa baixar nada.

Para ouvir os sons gerados: `python -I sfx_synth.py teste.wav`.
**Nunca** riser/suspense crescendo antes de revelação.

| Evento | Som (trecho do nome) | Ganho |
|---|---|---|
| troca claro↔escuro | `Multi Small Gear Rotation, Double Low Whoosh` (favorito), 0,18 s antes do corte | −19 |
| outras trocas de cena | `Crispy Small Whoosh` / `Modern Minimize` (.aac) | −17 a −20 |
| header / título entrando | `Crispy Small Whoosh`, `DSGNWhsh_Paper Whoosh` | −19 a −21 |
| badge / chip / pílula pequena | `Very Short Click_Camera` | −15 a −19 |
| cartão entrando | `Short Click_Camera` | −18 |
| pílula grande / cartão-chave / ilustração | `Camera Clicks, Low Impact, Mech Double Hit` (favorito) | −14 a −16 |
| status ✗ / carimbo | `Single Click Shutter` | −15 |
| risco | `Distorted Paper Whoosh` (0,35 s) | −16 |
| cascata (grade virando) | `Very Short Click` a cada 0,06 s | −25 |
| contador subindo | `Stopwatch Clicks_Cinematic` (0,85 s) | −19 |
| contador chega | `UI Bright Chime` (.aac) | −17 |
| digitação do CTA | `Computer Keyboard Quick Typing` (.aac, 1 s) | −20 |

Masterização: voz + SFX(−1 dB), normaliza pico em −1 dBFS, fade 0,3 s no fim.
