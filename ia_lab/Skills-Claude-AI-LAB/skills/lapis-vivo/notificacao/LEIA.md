# Notificação no topo (padrão de todos os vídeos)

Configuração única em `~/.claude/notificacao.json`, lida por todas as skills de vídeo. Script: `notificacao.py` (Python + PIL + ffmpeg, sem créditos de IA, ~3 s pra aplicar).

## Primeira vez (instalação ou primeiro vídeo)
1. `python notificacao.py status`. Se responder **NAO CONFIGURADA**, perguntar ao usuário (uma vez só): o **@ do Instagram**, a **foto de perfil** (arquivo) e a **frase** (padrão: "Segue pra ver mais vídeos de IA" — sugerir uma do nicho dele). Se ele não quiser, `--nenhuma`.
2. Salvar: `python notificacao.py configurar --nome "perfil" --foto foto.jpg --texto "Segue pra …"`.
   Opcionais: `--verificado` (selo azul), `--inicio 3` (segundo em que desce), `--dura 3.5`, `--som-entrada pop.wav --som-saida swish.wav --som-db -12` (som sempre abaixo da voz).
3. Mostrar a amostra: `python notificacao.py amostra amostra.png`.

Depois disso não perguntar de novo. Pra trocar, o usuário pede ("muda a frase da notificação pra …").

## Em cada vídeo (fim do pipeline, ANTES da marca d'água)
`python notificacao.py aplicar master_sem_notif.mp4 master_notif.mp4` → depois `marca_dagua.py aplicar` → versão `_celular`.
- Entra em **3 s** por padrão (depois do gancho, nunca em cima dele). Se o vídeo tiver um momento melhor (pausa, troca de cena, logo depois de entregar a 1ª dica), usar `--inicio <s>`.
- Frase pode variar por vídeo: `--texto "Segue pra ver a parte 2"`.
- Não pode cobrir título/elemento-herói que esteja no topo naquele trecho: conferir 1 quadro em `inicio+1 s`; se colidir, mudar o `--inicio`.
- Capa não leva notificação. Se estiver desativada, o comando só copia.

## Como fica
Card #1E1E20 com borda fina, 800×110 px (em 1080), cantos 30, centralizado bem no topo (y 160, mesma posição da notificação do iPhone na referência). Foto redonda à esquerda, @ em semibold branco, frase em cinza, sino amarelo à direita, sombra suave (lê em vídeo claro). Movimento: desce com mola (overshoot pequeno, assenta em ~0,5 s), fica parado, dá uma puxadinha de 10 px pra baixo e sobe acelerando (~0,4 s).
