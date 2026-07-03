---
name: radar-de-papers
description: Pesquisa papers e publicações acadêmicas recentes em canais de IA/Ciência da Computação (arXiv, Hugging Face Papers, OpenReview, Semantic Scholar) e de Marketing/Neuromarketing/Consumo (SSRN, journals de consumer research, Frontiers), retornando título, resumo em português brasileiro e notas de 0-10 de potencial como base de conteúdo para LinkedIn e Instagram. Use esta skill sempre que o usuário pedir para pesquisar papers novos, buscar novidades acadêmicas, varrer os canais de pesquisa, encontrar material para posts, perguntar "o que saiu de novo" em IA/agentes/marketing/neuromarketing, ou mencionar termos como "radar", "garimpo de papers", "papers da semana", "material para conteúdo" ou variações. Também acione quando o usuário pedir avaliação de potencial de um paper para redes sociais.
---

# Radar de Papers

Skill de descoberta e triagem de papers acadêmicos com foco em reaproveitamento como conteúdo para LinkedIn e Instagram. O objetivo não é resumo profundo de um paper específico (para isso existe a skill `academic-paper-summarizer`). O objetivo é varrer os canais, filtrar o que importa e entregar uma seleção pronta para decisão editorial.

## Fluxo de trabalho

### 1. Entender o pedido

Identifique no pedido do usuário:
- **Tema**: agentes de IA, LLMs, RAG, neuromarketing, comportamento do consumidor, hábitos de consumo, ou outro. Se o usuário não especificar, pergunte OU cubra os dois eixos padrão dele (IA/agentes + marketing/consumo) de forma equilibrada.
- **Janela temporal**: padrão é os últimos 7 dias para IA (área rápida) e os últimos 30-60 dias para marketing/consumo (área lenta, movida a journals). Ajuste se o usuário pedir.
- **Quantidade**: padrão é 5 a 8 papers no total. Menos que isso empobrece a escolha, mais que isso vira ruído.

### 2. Pesquisar nos canais

Consulte o arquivo `references/fontes.md` para a lista completa de canais, URLs e dicas de consulta por canal.

Estratégia de busca:
- Use `web_search` com queries curtas combinando o tema + termos como "arxiv", "paper", "2026". Exemplo: `LLM agents evaluation arxiv`.
- Use `web_fetch` para abrir as páginas de listagem (Hugging Face Papers, arXiv recent) e os abstracts dos papers candidatos.
- Para IA: priorize Hugging Face Papers (triagem da comunidade) e arXiv (fonte crua). Hugging Face primeiro, porque já vem filtrado.
- Para marketing/neuromarketing/consumo: priorize busca por termo no Google Scholar/Semantic Scholar e SSRN. Não existe feed diário útil nessa área; a busca por palavra-chave é o caminho.
- Sempre abra o abstract real do paper antes de incluí-lo na seleção. Nunca avalie um paper só pelo título ou por menção de terceiros.

### 3. Filtrar

Critérios de corte antes de entrar na seleção final:
- O paper precisa ter abstract acessível e data de publicação identificável.
- Descarte papers puramente incrementais (melhoria marginal de benchmark sem ideia nova) a menos que o benchmark seja muito conhecido.
- Em marketing/neuromarketing, desconfie de achados chamativos sem amostra decente ou pré-registro. Se incluir mesmo assim por potencial de conteúdo, sinalize a fragilidade no resumo.
- Prefira diversidade de subtemas na seleção em vez de 6 papers sobre a mesma coisa.

### 4. Avaliar potencial de conteúdo

Atribua DUAS notas de 0 a 10, uma para LinkedIn e outra para Instagram. São critérios diferentes.

**Nota LinkedIn** avalia:
- Relevância profissional para audiência de marketing, IA, negócios e liderança (peso alto)
- Gancho de discussão: o achado provoca opinião, debate ou aplicação prática no trabalho?
- Autoridade: citar este paper posiciona o autor do post como alguém que lê pesquisa de verdade?
- Atualidade e ineditismo do tema no feed brasileiro

**Nota Instagram** avalia:
- O insight central cabe em uma frase simples e visual? (peso alto)
- Potencial de carrossel ou dado numérico que vira card
- Curiosidade de público amplo, fora da bolha técnica
- Conexão com o cotidiano de consumo das pessoas

Referências de calibragem:
- 9-10: raro; achado forte, fácil de comunicar e alinhado com o momento do feed
- 7-8: bom candidato; rende post com algum trabalho de tradução
- 5-6: usável como complemento ou citação dentro de um post maior
- 0-4: relevante academicamente, mas não rende conteúdo; ou frágil demais para citar

Um paper técnico denso pode ser 9 no LinkedIn e 3 no Instagram. Isso é normal e esperado. Notas divergentes são sinal de avaliação honesta.

### 5. Entregar

Responda em português brasileiro usando EXATAMENTE esta estrutura por paper:

```
## [N]. [Título do paper em pt-br]
[Título original do paper]

**Fonte:** [canal + link direto para o paper] | **Data:** [data de publicação]
**Autores:** [até 3 nomes, depois "et al."]

**Resumo:** [4 a 8 frases em pt-br cobrindo: qual o problema, o que o paper fez, qual o achado principal e por que importa. Escreva com frases de tamanho variado. Nada de tradução literal do abstract; explique como se estivesse contando para um colega.]

**LinkedIn: [nota]/10** — [1 frase justificando]
**Instagram: [nota]/10** — [1 frase justificando]
**Ângulo de post:** [1 a 2 frases sugerindo o gancho editorial mais forte]
```

Ao final da lista, adicione uma seção curta **"Destaque da rodada"** apontando qual paper você escolheria primeiro e por quê, em no máximo 3 frases.

## Regras de estilo da entrega

- Todo o texto de saída em português brasileiro.
- Nunca use travessão (—) exceto no separador fixo do formato de notas acima; se preferir, substitua por dois-pontos.
- Varie o tamanho das frases nos resumos: misture períodos longos com frases curtas e secas.
- Não invente dados. Se não conseguir confirmar data ou autores, escreva "não confirmado" em vez de chutar.
- Cite sempre o link direto do paper (abstract page), não o link de busca.

## Limitações conhecidas

- Journals de marketing ficam atrás de paywall. Quando só o abstract estiver acessível, avalie e resuma com base nele e sinalize isso.
- ResearchGate e Google Scholar bloqueiam fetch com frequência. Se falhar, use web_search com o título entre aspas para achar versão alternativa (SSRN, site do autor, PDF aberto).
- Se um canal estiver fora do ar, siga com os demais e informe o usuário no final.