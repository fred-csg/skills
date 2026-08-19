---
name: criar-big-ideas
description: Crie, refine, compare e valide Big Ideas de marketing a partir de uma brecha de mercado, posicionamento, público, problema, promessa, mecanismo e provas. Use quando o usuário quiser gerar novos ângulos de comunicação, headlines-mãe, conceitos de campanha, mecanismos nomeados, narrativas centrais ou testar ideias para anúncios, páginas, VSLs, webinars, CPLs, e-mails, lançamentos e posicionamento.
---

# Criar Big Ideas

Transformar um posicionamento em uma ideia central memorável, relevante, crível e expansível para vários canais. Tratar “irresistível” como ambição criativa, não como garantia de resposta.

## Distinguir os conceitos

- **Posicionamento:** lugar estratégico que a marca pretende ocupar.
- **Brecha:** oportunidade ou tensão não bem atendida.
- **Big Idea:** interpretação central que une verdade do público, novidade relevante e promessa crível.
- **Mecanismo:** explicação causal de como a mudança acontece.
- **Headline:** expressão específica da Big Idea em uma peça.

Não confundir frase chamativa com Big Idea. Uma Big Idea deve sustentar campanha, narrativa, prova e variações sem perder coerência.

## Aplicar regras inegociáveis

1. Usar apenas contexto fornecido ou pesquisa explicitamente autorizada e citada.
2. Nunca inventar caso, número, autoridade, comparação, prazo, exclusividade, escassez, consequência ou resultado.
3. Marcar lacunas como `[PROVA NECESSÁRIA]`, `[DADO NECESSÁRIO]`, `[DECISÃO DO USUÁRIO]` ou `[HIPÓTESE]`.
4. Não inferir desejo secreto humilhante, vingativo ou íntimo sem evidência da voz do público.
5. Não criar inimigo, conspiração, FOMO ou catástrofe fictícios.
6. Não chamar avaliação da IA de teste científico, reação do público ou validação.
7. Não atribuir score observado sem dados reais. Separar score editorial de score comportamental.
8. Não forçar prazo numérico. Usar timeline somente quando sustentada por dados ou pela natureza do entregável.
9. Não chamar um mecanismo de proprietário, único ou registrável sem verificação adequada.
10. Respeitar autonomia: gerar interesse por relevância, tensão e utilidade, não por vergonha, inveja ou medo fabricado.

Ler [persuasao-responsavel.md](references/persuasao-responsavel.md) antes de criar consequências, urgência, comparações ou claims.

## Escolher a rota

- **Criar do zero:** validar pré-requisitos, construir anatomia, gerar variações e planejar teste.
- **Criar ângulos:** partir de posicionamento e mecanismo já aprovados para gerar alternativas.
- **Refinar:** fortalecer uma ideia existente sem mudar seu núcleo.
- **Validar:** desenhar pesquisa qualitativa, teste de mensagem ou experimento de canal.
- **Desenvolver mecanismo:** nomear e explicar um processo real já existente.
- **Aplicar:** adaptar a ideia aprovada a campanhas e canais.

## Executar em cinco fases

### Fase 0 — Confirmar a base

Ler [contexto-e-prerequisitos.md](references/contexto-e-prerequisitos.md). Resumir brecha, posicionamento, público, linguagem, problema, oferta, mecanismo e provas. Pedir confirmação antes de avançar se o resumo alterar o contexto.

A ausência de três casos não impede ideação. Ela limita claims e validação: trabalhar com promessa reduzida, demonstração, princípios ou marcadores de prova.

### Fase 1 — Mapear a anatomia

Ler [anatomia-da-big-idea.md](references/anatomia-da-big-idea.md). Mapear desejo/tensão, transformação, timeline quando defensável, mecanismo, prova e custo factual da inação. Validar a anatomia antes das variações.

### Fase 2 — Gerar variações

Ler [formulas-de-variacao.md](references/formulas-de-variacao.md). Gerar dez rotas realmente distintas. Não obrigar todos os elementos em cada frase; preservar clareza e escolher o elemento dominante de cada fórmula.

### Fase 3 — Avaliar e testar

Ler [validacao-e-experimentos.md](references/validacao-e-experimentos.md). Fazer primeiro triagem editorial claramente rotulada como hipótese. Havendo dados reais, calcular ranking comportamental. Sem dados, entregar plano de teste e não declarar top 3 “validadas”.

Usar `python scripts/rank_big_ideas.py <resultados.csv>` para consolidar avaliações reais coletadas no modelo de [validation-results-template.csv](assets/validation-results-template.csv).

### Fase 4 — Desenvolver o mecanismo

Ler [mecanismo-e-naming.md](references/mecanismo-e-naming.md). Refinar a ideia escolhida, produzir explicação de 60 segundos, diagrama simples, diferenciação e limites. Não inventar processo para justificar um nome.

### Fase 5 — Consolidar e aplicar

Ler [relatorio-e-aplicacao.md](references/relatorio-e-aplicacao.md). Entregar anatomia, variações, avaliação, evidências, mecanismo e matriz de aplicação. Manter o mesmo núcleo sem repetir a mesma headline em todos os canais.

## Usar checkpoints

Validar com o usuário após:

1. resumo da base;
2. anatomia da promessa;
3. dez variações e triagem editorial;
4. dados de audiência, se coletados;
5. mecanismo e Big Idea final.

Se o usuário pedir o relatório completo e houver contexto suficiente, avançar com premissas sinalizadas. Nunca transformar premissa em fato para evitar um checkpoint.

## Manter dois tipos de score

### Score editorial

Avaliar clareza, relevância, novidade, coerência, credibilidade e expansibilidade. Rotular como julgamento editorial da IA. Usar para eliminar versões obviamente fracas, não para prever performance.

Não atribuir notas editoriais de curiosidade, inveja, urgência, raiva ou FOMO para imitar o “teste da paralisia”. Se o usuário pedir essas notas sem pesquisa, explicar a limitação e converter a análise para as seis dimensões editoriais acima. Não otimizar inveja, raiva ou medo como fins persuasivos.

### Score comportamental

Calcular somente a partir de respostas reais ou métricas de experimento. Registrar amostra, recrutamento, estímulo, canal, data, denominador e limitações. Priorizar atenção, curiosidade, relevância, credibilidade e intenção de próximo passo.

Não usar perguntas indutivas como “o que você sente ao saber que poucos têm acesso?”. Não simular escassez para medir FOMO.

## Entregar

Usar [templates-de-entrega.md](references/templates-de-entrega.md). Incluir:

- contexto confirmado e lacunas;
- anatomia;
- dez variações com fórmula e claim dominante;
- matriz de sustentação das alegações;
- triagem editorial ou resultados comportamentais, devidamente distinguidos;
- top candidatas, nunca “vencedoras” sem experimento;
- mecanismo e visual, se aplicável;
- plano de teste e adaptação por canal;
- próximo checkpoint.
