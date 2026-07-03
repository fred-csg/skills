---
name: keshav-paper-reader
description: >
  Conduz a leitura de artigos científicos usando o método clássico das "três passadas" de
  S. Keshav ("How to Read a Paper", 2007), em vez de gerar apenas um resumo direto. Use esta
  skill sempre que o usuário pedir para "ler", "avaliar se vale a pena ler", "fazer a leitura
  do Keshav", "aplicar o método das três passadas / three-pass approach" em um paper, artigo
  científico, preprint ou publicação acadêmica — especialmente quando ele quer decidir se vale
  a pena investir tempo no artigo antes de se aprofundar, ou quando quer entender o artigo em
  camadas crescentes de profundidade (visão geral → leitura atenta → leitura profunda com
  reimplementação mental). Também use quando o usuário pedir uma "revisão de literatura",
  "levantamento do estado da arte" ou "mapear os principais papers de um tema" — o método do
  Keshav também cobre como usar as três passadas para pesquisar e organizar múltiplos artigos
  de uma área. Aciona com PDF enviado, link (arxiv, ACM, IEEE, ScienceDirect, Springer, etc.)
  ou texto colado. Diferente de um simples "resumo de paper": aqui o objetivo é a metodologia
  de leitura crítica e progressiva, com um ponto de decisão explícito entre cada passada.
---

# Leitura de Papers — Método Keshav (Three-Pass Approach)

Baseada no artigo de S. Keshav, *"How to Read a Paper"* (ACM SIGCOMM CCR, 2007). A ideia central
é não ler um artigo do início ao fim de uma vez só: isso desperdiça tempo em papers que não
valem a pena e não gera profundidade suficiente nos que valem. Em vez disso, o método usa três
passadas sucessivas, cada uma mais profunda que a anterior, com uma decisão consciente de
continuar (ou não) entre elas.

Você deve **conduzir o usuário passada por passada**, parando ao final de cada uma para
perguntar se deseja avançar para a próxima. Não pule direto para um relatório completo — o
valor do método está justamente no ponto de decisão entre as passadas.

## 1. Identificar a fonte do paper

- **PDF enviado** → extrair o texto (usar a ferramenta de leitura de PDF disponível, ou pedir
  que o usuário cole o texto se a extração falhar).
- **Link** (arxiv.org, dl.acm.org, ieee, sciencedirect, springer, nature, etc.) → buscar o
  conteúdo da página/PDF via busca web.
- **Texto colado diretamente no chat** → usar como está.

Se a fonte fornecida não permitir extrair título, abstract e introdução, avise o usuário e
peça uma fonte alternativa antes de iniciar a Passada 1.

## 2. Passada 1 — Visão geral (equivalente a 5–10 min de leitura humana)

Leia apenas: título, abstract, introdução, cabeçalhos de seção (ignorando o resto do texto de
cada seção), conclusão, e dê uma passada nas referências marcando quais você já conhece.

Não leia o corpo das seções, não tente entender detalhes técnicos ainda.

Produza os **cinco Cs**, o núcleo da primeira passada:

```markdown
## Passada 1 — Visão Geral

**Categoria:** [tipo de trabalho — ex: medição de sistema, análise de algoritmo existente,
descrição de protótipo de pesquisa...]

**Contexto:** [com quais outros artigos/áreas ele se relaciona; quais fundamentos teóricos
são usados]

**Corretude:** [as suposições parecem válidas à primeira vista?]

**Contribuições:** [quais são as contribuições principais do artigo, em 1–2 frases cada]

**Clareza:** [o artigo está bem escrito?]

**Recomendação:** [vale a pena investir na Passada 2? Por quê?]
```

Depois de apresentar isso, **pare e pergunte ao usuário**: "Quer que eu continue para a
Passada 2 (leitura atenta, ~1h)?" — não prossiga sem essa confirmação, mesmo que sua
recomendação tenha sido positiva. Essa é a decisão de triagem que dá valor ao método.

## 3. Passada 2 — Leitura atenta (equivalente a ~1h de leitura humana)

Só execute se o usuário confirmar após a Passada 1.

Leia o artigo com atenção, mas **ignore prova matemáticas e derivações detalhadas** — marque-as
para a Passada 3 caso sejam relevantes. Preste atenção especial a figuras, gráficos e outras
ilustrações: são frequentemente onde os erros aparecem (eixos mal rotulados, escalas
questionáveis, barras de erro ausentes). Marque referências ainda não lidas que valem
investigação futura para entender o pano de fundo do trabalho.

```markdown
## Passada 2 — Leitura Atenta

**Resumo do conteúdo:** [síntese das ideias principais com suas evidências de suporte —
o suficiente para explicar o artigo a outra pessoa]

**Figuras e dados-chave:** [o que os principais gráficos/tabelas mostram; alguma
inconsistência visual ou metodológica notada]

**Pontos não compreendidos / termos não familiares:** [o que ficou obscuro nesta passada]

**Referências para investigar depois:** [lista]

**Recomendação:** [vale a pena a Passada 3 (reimplementação e crítica profunda)? Por quê?]
```

Pare novamente e pergunte: "Quer que eu continue para a Passada 3 (leitura profunda,
reimplementação mental)?"

## 4. Passada 3 — Leitura profunda (equivalente a 4–5h de leitura humana)

Só execute se o usuário confirmar após a Passada 2.

O objetivo é **reimplementar virtualmente o artigo**: refazer mentalmente o mesmo trabalho,
fazendo as mesmas suposições que os autores fizeram, e comparar sua "reimplementação" com o
que foi de fato feito. Isso expõe suposições implícitas, erros, e permite identificar técnicas
inovadoras (ou questionáveis) de forma muito mais precisa do que uma leitura passiva.

```markdown
## Passada 3 — Leitura Profunda

**Reimplementação mental:** [como você refaria este trabalho; onde sua abordagem coincide ou
diverge da dos autores]

**Suposições implícitas:** [premissas que os autores não deixaram explícitas]

**Pontos fracos / questionáveis:** [erros, omissões, técnicas experimentais ou analíticas
duvidosas]

**Pontos fortes / técnicas notáveis:** [o que vale a pena adotar ou estudar mais a fundo]

**Ideias para trabalhos futuros:** [extensões, aplicações, ou problemas em aberto sugeridos
pelo artigo]

**Avaliação final:** [síntese: o artigo entrega o que promete? vale a pena citá-lo/usá-lo?]
```

Ao final da Passada 3, pergunte se o usuário quer que o relatório completo (as três passadas
juntas) seja salvo como um arquivo `.md`.

## 5. Modo revisão de literatura (múltiplos papers)

Use este modo quando o usuário não está pedindo para ler um único paper, mas sim para mapear
um tema, campo ou "estado da arte" — ex: "quais são os principais trabalhos sobre X?",
"faça um levantamento da literatura sobre Y". Keshav descreve isso como uma extensão natural
do método das três passadas:

1. **Buscar e triar:** use um motor de busca acadêmica (Google Scholar, arXiv, etc.) com
   3–5 palavras-chave bem escolhidas para encontrar 3–5 artigos recentes e relevantes. Faça a
   **Passada 1** em cada um para ter uma visão geral do problema e da abordagem atual. Veja a
   seção de trabalhos relacionados de cada um para identificar outros grupos de pesquisa
   ativos na área.
2. **Encontrar os trabalhos centrais:** procure citações e nomes de autores que se repetem
   entre os artigos triados — isso costuma apontar para os artigos e pesquisadores mais
   influentes do tema. Busque as versões mais recentes desses autores/grupos para identificar
   o estado da arte atual.
3. **Aprofundar nos centrais:** aplique a **Passada 2** (e a **Passada 3** nos 1–2 mais
   centrais) apenas nesses artigos-chave, e sintetize os achados em um panorama do tema:
   principais abordagens, consenso, divergências, e lacunas em aberto.

Ao final, produza um documento único organizando os artigos por relevância, não uma lista
solta — o objetivo é que o usuário saia com um mapa do campo, não apenas resumos avulsos.

## Observações finais

- Sempre responda em português (pt-BR), mesmo que o artigo original esteja em inglês.
- Não pule as pausas de decisão entre passadas — isso é o que diferencia este método de um
  resumo comum. Se o usuário pedir explicitamente "faça tudo de uma vez", tudo bem atender,
  mas normalmente conduza passada por passada.
- Esta skill é sobre *metodologia de leitura crítica*, não sobre gerar o resumo mais longo
  possível. Prefira clareza e honestidade sobre os pontos fracos do artigo a um tom
  excessivamente elogioso.
