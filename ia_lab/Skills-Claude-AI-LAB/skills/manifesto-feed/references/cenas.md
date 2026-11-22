# Cenas do template (EP01) — o que cada uma faz e como reaproveitar

Tempos no relógio original (45 s); o vídeo final toca mais rápido via `timewarp.ts`.

| # | Arquivo | Fala do EP01 | Mecânica (reaproveitável) | Transformação de saída |
|---|---|---|---|---|
| 1 | `S1Opinion.tsx` | 3 opiniões comuns ("A IA ainda não é realista"…) | Cards de comentário (@, curtidas, palavra-chave varrida por bloco branco) chegando de lados diferentes; cada novo empurra o anterior em profundidade | **Recuo violento** da câmera (`E.recoil`): os 3 cards encaixam em slots de uma grade gigante |
| 2 | `S2Bigger.tsx` | "uma mudança MAIOR já começou" | Grade de 2.048 tiles com contador mono; palavra gigante com expansão tonal | **Um tile da grade morfa num card 9:16** e a câmera mergulha nele |
| 3 | `S3Scroll.tsx` | "consumir, deslizar e esquecer" | Feed de cards com rolagem por inércia; cada verbo é um gesto: CONSUMIR suga as laterais, DESLIZAR desliza a composição, ESQUECER desfoca o card | **O feed deita** e vira esteira |
| 4 | `S4Loop.tsx` | "publicar mais vs esperar o perfeito" | Esteira cuspindo cards (cadência crescente, contador PUBLICADOS) × card isolado sendo refinado (grade, camadas, cantoneiras coral) | Esteira, máquina e card refinado **se contraem em 3 formas** |
| 5 | `S5Forces.tsx` | "velocidade, custo menor e qualidade" | 3 ícones 3D extrudidos com rótulo mono numerado (01/02/03), cada um com movimento próprio (dispara, colapsa, gira até alinhar) | As formas **travam num emblema** (lock mecânico) que gera o 1º card |
| 6 | `S6Infinite.tsx` | "vídeos incríveis produzidos em massa" | Multiplicação ×4 ×16 ×64 ×256 e câmera atravessando um **corredor infinito de cards** | Os cards passam a exibir a palavra INCRÍVEL |
| 7 | `S7Paradox.tsx` | "quando tudo é incrível… nada parece tão incrível" | Parede de INCRÍVEL repetida → **silêncio** → a palavra se desfaz em unidades tipográficas → "deixa de ser DIFERENCIAL." | O vazio vira **um ponto que traça uma linha** |
| 8 | `S8Split.tsx` | "o conteúdo está se dividindo" | Linha se bifurca: à esquerda um fluxo descartável (card a cada 3 frames, repetitivo, apagado); à direita **um card que para** (maior, luz coral atrás) | **Dolly para dentro** do card que parou |
| 9 | `S9Care.tsx` | "Todo mundo produz. Quase ninguém faz alguém se importar." | Frase seca → respiro → frase final em 3 linhas: branca, **branca em caixa invertida**, **coral** | Fim com repouso de leitura (~1,4 s) |

## Como adaptar a outro tema
- Mantenha o **arco**: senso comum → virada → causa → mecanismo → consequência → paradoxo → bifurcação → frase final.
- Troque o **objeto-símbolo**: no EP01 é o card de vídeo. Pode ser mensagem, notificação, currículo, produto, moeda… O símbolo atravessa o vídeo inteiro e muda de estado.
- Reaproveite as mecânicas pela função, não pelo texto: S1 = "vozes", S2 = "escala", S3 = "verbos-gesto", S4 = "quantidade × qualidade", S5 = "N forças que se juntam", S6 = "explosão/abundância", S7 = "paradoxo com silêncio", S8 = "dois caminhos", S9 = "frase final".
- Menos cenas é ok: apague a cena de `LAYERS` (`EP01.tsx`), ajuste `SCENES` e garanta que a cena seguinte nasce do estado final da anterior.
- Palavras de destaque viram `K.<palavra>` em `script.ts`; animação, flash e SFX daquela palavra apontam pro mesmo `K`.
