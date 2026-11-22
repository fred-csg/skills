# Marca d'água padrão

Configuração única em `~/.claude/marca-dagua.json`, lida por todas as skills de vídeo.

## Primeira vez (instalação ou primeiro vídeo)
1. `python marca_dagua.py status`. Se responder **NAO CONFIGURADA**, perguntar ao usuário (uma pergunta só, com opções):
   - "Quer uma marca d'água nos seus vídeos pra proteger contra repost sem crédito?" → **@ do Instagram** (pedir o @), **logo** (pedir o arquivo PNG, de preferência com fundo transparente) ou **sem marca d'água**.
2. Salvar: `python marca_dagua.py configurar --texto "@perfil"` · `--logo caminho.png` · `--nenhuma`.
   Ajustes opcionais: `--opacidade 0.45` (0.3 = mais discreta, 0.6 = mais visível) e `--tamanho 34`.
3. Mostrar uma amostra: `python marca_dagua.py amostra amostra.png`.

Depois disso não perguntar de novo; vale pra todas as produções. Pra trocar, o usuário pede ("muda minha marca d'água pra …").

## Em cada vídeo (último passo antes da entrega)
`python marca_dagua.py aplicar master_sem_marca.mp4 master.mp4` → gerar o preview leve a partir do master já marcado. Capa não leva marca d'água. Se a marca estiver desativada, o comando só copia.

## Como fica
Texto com ~45% de opacidade (branco em vídeo escuro, grafite em vídeo claro — automático) com sombra leve (ou o logo), logo acima da coluna de botões, alternando direita ↔ esquerda a cada 8 s — dentro da safe zone (não some atrás da interface) e difícil de cortar fora.
