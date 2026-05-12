---
name: long-audio-transcriber
description: >
  Transcreve arquivos de áudio muito longos (≥ 1h30) com alta eficiência, robustez e salvamento incremental.
  Use esta skill sempre que o usuário pedir para transcrever um áudio, gerar legendas (.srt), 
  ou extrair texto de gravações de voz, reuniões, podcasts, etc., especialmente se os arquivos forem grandes.
---

# Long Audio Transcriber

Esta skill fornece uma solução otimizada e incremental para transcrever áudios longos usando a engine `faster-whisper`.
O processamento suporta arquivos grandes graças ao filtro de detecção de atividade de voz (VAD) interno e salva o resultado
incrementalmente, em formato `.srt`, mitigando perdas por travamentos.

## Fluxo de Execução

Ao ser ativado pelo usuário para transcrever um áudio, siga estritamente os passos abaixo:

### 1. Detecção de GPU
Execute o seguinte comando no terminal do usuário para verificar a presença de uma placa de vídeo NVIDIA:
```powershell
nvidia-smi
```
- Se o comando for bem-sucedido e mostrar os dados da placa, utilizaremos `--device cuda`.
- Se falhar ou não encontrar placas compatíveis, utilizaremos `--device cpu`.

### 2. Instalação de Dependências
Assegure-se de que a biblioteca principal está instalada. Execute:
```powershell
pip install faster-whisper
```
> **Aviso:** Se for no Windows, é provável que precise do `ffmpeg` também, mas o usuário ou o agente já devem se certificar de que o ffmpeg está no PATH do sistema.

### 3. Execução da Transcrição
O motor desta skill fica em `scripts/transcribe.py` (relativo à pasta desta skill). Chame-o passando os parâmetros necessários. Exemplo genérico:
```powershell
python <caminho_absoluto_da_skill>/scripts/transcribe.py --input "<caminho_do_audio>" --output "<caminho_do_srt>" --device <cuda|cpu>
```
Se o modelo principal demorar muito a carregar ou a máquina for limitada, você pode adicionar o parâmetro opcional `--model base` ou `--model small` (o padrão é `medium`).

### 4. Acompanhamento
- Informe ao usuário que o comando foi lançado e o `faster-whisper` processará o áudio em chunks (pedaços).
- Avise que o arquivo destino (`.srt`) começará a aparecer no disco em breve, sendo preenchido frase por frase.
- Após o comando finalizar com sucesso, confirme a conclusão ao usuário e apresente eventuais resumos de tempo.
