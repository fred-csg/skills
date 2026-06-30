---
name: audio-transcriber
description: Transcreve arquivos de áudio extensos (≥ 1h30) com robustez e alta eficiência, gerando um arquivo de legenda incremental (.srt). Acione esta skill sempre que o usuário pedir para transcrever um áudio/vídeo longo ou gerar legendas a partir de um arquivo de mídia.
---

# Audio Transcriber Skill

Esta skill fornece uma solução otimizada para transcrever arquivos de áudio (incluindo áudios muito longos) utilizando Inteligência Artificial local de forma robusta e incremental.

## Como funciona

O script desenvolvido para esta skill faz o seguinte:
1. **Verificação Automática de Hardware**: Detecta se há uma placa de vídeo (GPU NVIDIA) disponível.
2. **Estratégia Adaptativa**: 
   - Se houver GPU: Utiliza a biblioteca `faster-whisper` com suporte a CUDA para máxima performance e uso da tecnologia VAD (Voice Activity Detection), otimizando a memória.
   - Se não houver GPU: Fallback seguro para `openai-whisper` padrão utilizando a CPU.
3. **Escrita Incremental**: As legendas (formato `.srt`) são salvas incrementalmente. Se a execução parar no meio de um áudio longo, o usuário não perde o que já foi transcrito.

## Como executar a transcrição

Você deve usar o script embutido nesta skill. Para transcrever um áudio, execute o comando abaixo através de seu shell (substituindo os caminhos conforme o que o usuário pedir):

```bash
python g:\SKILLS\audio-transcriber\scripts\transcribe.py "Caminho/para/audio.mp3" "Caminho/para/saida.srt"
```

## Resolução de Problemas
- **Falta de FFMPEG**: O Whisper exige a presença do FFmpeg instalado no sistema operacional do usuário. Caso o script acuse erro de falta do `ffmpeg`, instrua o usuário a instalar o `ffmpeg` (ex: `winget install ffmpeg` no Windows) antes de tentar novamente.
- **Erros de importação/CUDA**: O script instanciará o `faster-whisper` se houver GPU. Se o usuário tiver os drivers de GPU desatualizados, pode ocorrer um erro. Sugira atualizar os drivers caso o erro mencione "cublas" ou "cudnn".
