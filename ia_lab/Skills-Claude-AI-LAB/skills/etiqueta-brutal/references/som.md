# Etiqueta Brutal — som

Base: **áudio original do vídeo** (voz) em 0 dB. SFX curtos, secos, de "objeto de papel/interface". Sem música por padrão (se usar, −24 dB e com ducking).

Prioridade de busca (`sfx_lib.find` já faz): biblioteca do usuário em `sfx_pasta.txt` → se não houver ou o nome não existir, som gerado por código (`sfx_synth.py`). Os nomes abaixo são da biblioteca original do autor e servem de referência do tipo de som.
**Nunca** riser/suspense crescendo antes de revelação; nunca SFX sintetizado.

| Evento | Som (trecho do nome) | Ganho |
|---|---|---|
| início de cada grupo de legenda | `Very Short Click_Camera` | −21 dB |
| etiqueta/sticker pequeno entrando | `Very Short Click_Camera` / `Short Click_Camera` | −9 a −15 |
| bloco grande entrando | `Camera Clicks, Low Impact, Mech Double Hit` (favorito) | −8 a −10 |
| janela de app abrindo | `DSGNWhsh_Paper Whoosh` | −14 |
| arrastar slider | `Clicky Potentionmeter` (0,38 s) | −15 |
| clique de botão | `Single Click Shutter` | −8 |
| sucesso / ✓ | `Treadmill Start Button, Tone` (favorito) | −12 |
| contador subindo | `Stopwatch Clicks_Cinematic` (0,9 s) | −17 |
| palavra-soco (NADA.) | `Dry Break Impact, Crispy` (favorito, alinhar no pico) | −5 |
| revelação da tese (CONTEÚDO) | `Agressive Impact, Alarm Clock Wing` (favorito, pico) | −9 |
| risco/ corte | `Distorted Paper Whoosh` (0,35 s) | −15 |
| papel/panfleto | `Book Page Flip` (favorito, 0,6 s) | −11 |
| troca de cena (fundo lilás) | `Multi Small Gear Rotation, Double Low Whoosh` (favorito) | −11 |
| giro/chicote | `Cartoonish Whoosh, Whip` (pico) | −7 a −11 |
| selo da tese | `Metal Lever Activation` (favorito) | −9 |
| digitação CTA | `Very Short Click` a cada 0,08 s | −17 |

Masterização: soma voz + SFX(−1 dB), normaliza pico em −1 dBFS, fade de 0,25 s no fim.
