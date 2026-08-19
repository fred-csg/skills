---
name: criar-livro-bestseller
description: Planeje, escreva, revise e prepare livros originais de não ficção com alto potencial comercial, incluindo conceito, posicionamento, promessa, avatar, título, arquitetura, outline, capítulos, casos, exercícios, edição, metadados e plano de publicação. Use quando o usuário quiser transformar expertise, método, pesquisa, aulas ou uma ideia em livro, e-book, lead magnet, livro de autoridade, manuscrito para Amazon KDP ou estratégia editorial orientada a bestseller.
---

# Criar Livro Bestseller

Transformar conhecimento verificável em um livro útil, coerente, original e comercialmente bem posicionado. Tratar “bestseller” como meta dependente de qualidade, mercado, distribuição, timing e vendas; nunca garantir ranking ou volume.

## Escolher o modo

Identificar a necessidade:

- **Criar do zero:** conduzir conceito, arquitetura, outline, escrita, revisão e publicação.
- **Continuar:** recuperar decisões e escrever somente o próximo capítulo ou fase.
- **Transformar materiais:** extrair tese e conteúdo de aulas, transcrições, notas ou método existente.
- **Reestruturar:** diagnosticar e reorganizar manuscrito parcial.
- **Revisar:** executar edição estrutural, de conteúdo, estilo, evidências ou preparação editorial.
- **Publicar:** preparar metadados, arquivos e lançamento sem reescrever o livro inteiro.

Não refazer decisões aprovadas. Antes de cada fase, resumir o estado atual, as decisões fixadas e as lacunas.

## Aplicar regras inegociáveis

1. Nunca inventar credenciais, fatos, pesquisas, citações, fontes, casos, depoimentos, métricas ou resultados.
2. Marcar lacunas como `[FONTE NECESSÁRIA]`, `[CASO PENDENTE]`, `[DECISÃO DO AUTOR]` ou `[VERIFICAR]`.
3. Não criar “caso real” fictício. Usar exemplo hipotético somente com rótulo explícito e números ilustrativos claramente identificados.
4. Não imitar a voz de autor vivo nem reproduzir passagens protegidas. Extrair princípios abstratos e escrever com voz própria.
5. Não prometer número de páginas, prazo de produção, conversão, vendas, reviews ou ranking.
6. Não aumentar extensão com redundância. Definir palavras pela experiência de leitura e pela função do livro.
7. Distinguir alegação do autor, inferência editorial e fato sustentado por fonte.
8. Preservar consentimento e anonimização em histórias de terceiros.
9. Verificar regras atuais da plataforma em fontes oficiais antes de recomendar metadados, formatos, categorias, limites ou preços.
10. Solicitar revisão profissional quando houver risco jurídico, médico, financeiro, difamação, privacidade ou aconselhamento regulado.

## Conduzir as cinco fases

### 1. Conceito e posicionamento

Ler [conceito-e-posicionamento.md](references/conceito-e-posicionamento.md). Definir objetivo, leitor, problema, transformação, tese, promessa calibrada, diferencial e critérios de sucesso observáveis.

### 2. Arquitetura e outline

Ler [arquiteturas.md](references/arquiteturas.md) e [outline.md](references/outline.md). Recomendar uma arquitetura principal e, se útil, uma alternativa. Criar outline detalhado antes da prosa longa.

### 3. Escrita incremental

Ler [escrita-de-capitulos.md](references/escrita-de-capitulos.md). Produzir introdução ou um capítulo por vez, validar e atualizar o mapa de continuidade. Não tentar gerar um livro longo inteiro em uma única resposta se isso comprometer qualidade ou consistência.

### 4. Casos e recursos práticos

Ler [casos-e-evidencias.md](references/casos-e-evidencias.md). Integrar histórias autorizadas, exemplos, exercícios, checklists, diagramas e ferramentas onde aumentarem compreensão ou aplicação.

### 5. Edição, publicação e lançamento

Ler [edicao-e-controle-de-qualidade.md](references/edicao-e-controle-de-qualidade.md) e, quando solicitado, [publicacao-e-lancamento.md](references/publicacao-e-lancamento.md). Separar prontidão editorial de prontidão comercial.

## Usar checkpoints

Pausar para validação quando uma decisão alterar:

- leitor prioritário;
- tese ou promessa central;
- arquitetura;
- título/subtítulo finais;
- ordem dos capítulos;
- voz autoral;
- alegações sensíveis;
- publicação, preço ou CTA comercial.

Se o usuário pedir execução completa e os materiais determinarem essas escolhas, avançar autonomamente e registrar as premissas. Caso contrário, agrupar apenas perguntas bloqueadoras.

## Manter artefatos de continuidade

Usar os modelos de [templates-de-entrega.md](references/templates-de-entrega.md) e manter:

- `book-brief.md`: objetivo, leitor, tese, promessa, voz e restrições;
- `outline.md`: partes, capítulos, objetivos, evidências e transições;
- `source-ledger.md`: alegações, fontes, permissão e status;
- `style-sheet.md`: voz, termos, grafia, pessoas e convenções;
- `manuscript.md` ou capítulos separados;
- `revision-log.md`: decisões e alterações relevantes.

Usar [manuscript-template.md](assets/manuscript-template.md) como base quando criar arquivos no workspace.

## Escrever com voz autoral

Inferir a voz a partir de amostras do próprio autor. Se não houver amostra, propor três direções breves e pedir escolha antes da prosa extensa. Preservar precisão, ritmo, nível técnico e postura sem fabricar experiências pessoais.

Em cada capítulo:

1. declarar a transformação local;
2. abrir com tensão ou pergunta relevante, sem choque artificial;
3. desenvolver uma ideia central;
4. explicar por que importa;
5. demonstrar como funciona;
6. incluir evidência ou exemplo proporcional;
7. tratar limites e armadilhas;
8. oferecer ação, reflexão ou síntese;
9. conectar ao próximo capítulo.

Variar a estrutura quando o gênero pedir; não forçar sete seções idênticas em todos os capítulos.

## Validar o manuscrito

Executar `python scripts/audit_manuscript.py <arquivo.md>` para obter contagem de palavras, capítulos, marcadores pendentes e possíveis repetições. Tratar o relatório como diagnóstico, não como avaliação literária.

Depois executar a auditoria editorial de [edicao-e-controle-de-qualidade.md](references/edicao-e-controle-de-qualidade.md). Corrigir falhas objetivas e encaminhar decisões autorais ao usuário.

## Entregar

Incluir:

- fase concluída e decisões tomadas;
- artefato solicitado;
- alegações e fontes pendentes;
- contagem real de palavras, se houver manuscrito;
- riscos ou revisões especializadas;
- próximo checkpoint.

Não declarar “pronto para publicar” enquanto conteúdo, direitos, fontes, revisão e requisitos da plataforma não estiverem verificados.
