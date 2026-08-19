---
name: construir-sistema-anti-objecao
description: Analisa pesquisas de leads e cria sistemas éticos de antecipação e tratamento de objeções para lançamentos, eventos, ofertas, páginas, aulas e equipes comerciais. Use quando o usuário pedir sistema anti-objeção, mapa de resistências, drives mentais, scripts de objeção, diagnóstico de tempo/dinheiro/confiança, tratamento de dúvidas ou kit de fechamento; se não houver respostas reais de pesquisa, orientar como preparar e enviar os dados antes de inferir objeções.
---

# Construir sistema anti-objeção

Transformar dúvidas, riscos percebidos e condições de compra em respostas claras, verificáveis e úteis. Tratar objeções como informação para melhorar oferta e comunicação, não como barreiras psicológicas a destruir.

## Verificar os insumos

1. Procurar respostas de pesquisa no pedido, anexos e arquivos indicados.
2. Se não houver respostas reais, ler [references/intake-guide.md](references/intake-guide.md), orientar o usuário e encerrar sem fabricar análise.
3. Se houver pesquisa, inventariar formato, perguntas, respostas válidas, período, origem e limitações.
4. Extrair também: evento, produto, preço, promessa, método, aulas, provas, garantia, bônus, cronograma, público e histórico.
5. Perguntar apenas pelos campos críticos ausentes. Não repetir perguntas respondidas nos materiais.

## Preservar evidência e autonomia

- Trabalhar no nível agregado. Não prever “a objeção exata de cada pessoa” nem criar perfis psicológicos individuais para persuasão.
- Não inferir escolaridade, renda, gênero, saúde mental, autoestima, trauma, vitimização, orgulho ou “raiz emocional” a partir de pistas vagas.
- Rotular cada achado como **declarado**, **inferência fundamentada** ou **hipótese a validar**.
- Vincular objeções a citações anonimizadas, contagens e denominadores. Não inventar desejos implícitos ou resistências ocultas.
- Distinguir objeção de falta de adequação. Se preço, tempo, risco ou esforço forem incompatíveis com a pessoa, respeitar a não compra.
- Não usar vergonha, insulto, comparação cruel, culpa, ameaça, ultimato, medo inflado ou falsa urgência.
- Não desqualificar parceiros, família ou consultores que participem da decisão.
- Usar provas, ROI, garantias, escassez e custos de oportunidade somente com premissas explícitas e verificáveis.
- Explicar para quem a solução não serve e manter espaço real para pensar, comparar e recusar.

## Executar as cinco fases

Ler [references/analysis-framework.md](references/analysis-framework.md). Conduzir uma fase por vez e pedir validação antes de avançar.

### Fase 1 — Análise da pesquisa

Mapear amostra, linguagem, problemas, objetivos, tentativas anteriores, confiança, riscos percebidos e condições de decisão. Não chamar intensidade lexical de “temperatura emocional” sem evidência adicional.

### Fase 2 — Diagnóstico de objeções

Agrupar objeções declaradas e hipóteses em categorias. Priorizar por prevalência, impacto na decisão, estágio em que surge e capacidade real da oferta de responder. Separar:

- dúvida informacional;
- risco percebido;
- restrição real;
- falta de confiança;
- falta de adequação;
- preferência ou prioridade diferente.

### Fase 3 — Biblioteca de respostas

Ler [references/response-patterns.md](references/response-patterns.md). Criar pelo menos 15 respostas somente quando houver objeções suficientes. Para cada resposta, incluir: objeção na voz do cliente, validação, pergunta de esclarecimento, resposta, prova, condição de adequação, CTA sem pressão e alternativa quando não fizer sentido comprar.

### Fase 4 — Implementação

Ler [references/implementation.md](references/implementation.md). Distribuir respostas no pré-lançamento, aulas, oferta, FAQ, checkout e pós-oferta. Antecipar dúvidas frequentes de forma transparente; não tentar neutralizar resistências desconhecidas subliminarmente.

### Fase 5 — Kit de última hora

Criar scripts curtos para “preciso pensar”, “preciso conversar”, “não é o momento”, preço, tempo, confiança, adequação e experiências anteriores. Priorizar diagnóstico, clareza e follow-up consentido, não fechamento a qualquer custo.

## Validar o sistema

1. Estruturar a biblioteca em JSON quando possível.
2. Executar `scripts/validate_objection_library.py` para verificar campos, evidências, duplicatas e linguagem de pressão.
3. Corrigir erros e revisar avisos manualmente.
4. Ler [references/report-template.md](references/report-template.md) e produzir o arquivo no caminho solicitado; sem caminho, usar `sistema_anti_objecao.md` no diretório de trabalho.
5. Adaptar a extensão à amostra e ao número de objeções; não preencher páginas com hipóteses frágeis.

Medir eficácia por clareza percebida, perguntas resolvidas, adequação, conversão, reembolso, arrependimento, reclamações e qualidade do atendimento. Não chamar vendas de “ciência” sem desenho experimental.
