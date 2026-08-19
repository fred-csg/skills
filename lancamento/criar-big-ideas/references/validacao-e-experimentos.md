# Validação e experimentos

## Camada 1 — Triagem editorial

Pontuar de 0 a 10 com justificativa textual:

- clareza;
- relevância;
- novidade significativa;
- coerência com o posicionamento;
- credibilidade;
- expansibilidade em campanha.

Rotular: “avaliação editorial, não resposta observada”. Eliminar claims sem prova antes de comparar força criativa.

Não preencher o score legado de curiosidade, inveja, urgência, raiva e FOMO com julgamento da IA. Sem observação real, esses campos permanecem sem nota. Mesmo em pesquisa, tratar inveja, raiva e medo como reações a compreender e mitigar, não como metas a maximizar.

## Camada 2 — Teste qualitativo

Recrutar pessoas compatíveis com o público. Randomizar a ordem das ideias e evitar mostrar dez versões à mesma pessoa quando houver fadiga.

Perguntar de modo neutro:

1. O que você entende desta ideia?
2. O que parece mais relevante ou irrelevante?
3. O que você gostaria de saber em seguida?
4. O que torna a ideia crível ou pouco crível?
5. Que ação, se alguma, você tomaria?

Codificar compreensão, relevância, perguntas espontâneas, credibilidade e intenção. Registrar também objeções e interpretações erradas.

## Camada 3 — Teste quantitativo de mensagem

Usar amostra compatível, estímulo e contexto constantes. Medir, conforme o canal:

- atenção ou parada;
- compreensão;
- relevância autodeclarada;
- credibilidade;
- intenção de próximo passo.

Não chamar dez entrevistas de prova científica. Informar desenho e incerteza.

## Camada 4 — Experimento de canal

Comparar candidatas com distribuição aleatória quando possível. Definir antes:

- hipótese;
- controle e variantes;
- unidade de randomização;
- métrica primária;
- guardrails;
- janela;
- regra de parada;
- tamanho de amostra ou critério prático;
- segmentos.

Não usar 20% como limiar universal nem inventar benchmark. Analisar efeito, incerteza, qualidade do tráfego e downstream.

## Ranking

O script consolida avaliações reais por ideia. Cada linha deve representar um respondente ou observação com notas de 0 a 10 para `attention`, `curiosity`, `relevance`, `credibility` e `action_intent`.

Não preencher o CSV com notas imaginadas pela IA. Com dados insuficientes, apresentar apenas tendências e plano de coleta.

## Decisão

Classificar como:

- **candidata editorial:** passou na triagem;
- **promissora qualitativamente:** compreensão e relevância aparecem em entrevistas;
- **validada no estímulo testado:** resultado quantitativo dentro do desenho declarado;
- **validada no canal:** superou alternativa no experimento especificado.

Evitar “vencedora definitiva”: efeito pode mudar por canal, público e momento.
