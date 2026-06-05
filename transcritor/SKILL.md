---
name: transcritor
description: Skill local para realizar transcricao de arquivos de audio/video locais ou links do YouTube, salvando os resultados (.srt e .md) em uma pasta 'transcricoes' no diretorio de trabalho atual.
---
# Skill Transcritor

Esta skill local encapsula um motor de transcricao de audio e video baseado em Inteligencia Artificial (Whisper e faster-whisper) integrado ao download automatico de videos do YouTube.

## Como Usar

Quando o usuario solicitar a transcricao de um video (local ou URL do YouTube) ou de um arquivo de audio, voce deve invocar a execucao desta skill no terminal do Windows usando o ambiente virtual dedicado dela.

### Comando de Execucao

Voce deve rodar o script passando o caminho do interpretador Python do ambiente virtual da skill e o caminho do script `executar.py`:

```powershell
G:\SKILLS\transcritor\.venv\Scripts\python.exe G:\SKILLS\transcritor\scripts\executar.py "<entrada>" "[nome_da_transcricao_opcional]"
```

*   `<entrada>`: Pode ser uma URL de video do YouTube ou o caminho absoluto de um arquivo de video ou audio local.
*   `[nome_da_transcricao_opcional]`: (Opcional) Nome amigavel que sera usado para os arquivos gerados (ex: `minha_videoaula`). Se omitido, para arquivos locais sera usado o nome do arquivo sem extensao, e para links do YouTube sera usado `videoaula_transcrita`.

### Pasta de Saida

Os arquivos de transcricao (`.srt` e `.md`) serao salvos automaticamente em um subdiretorio chamado `transcricoes` (sem acento) criado na pasta de onde voce executou o comando (o diretorio de trabalho atual - Cwd).

### Requisitos

*   A skill executa em seu proprio ambiente virtual com suporte a aceleracao por GPU/CUDA de forma isolada do workspace.
