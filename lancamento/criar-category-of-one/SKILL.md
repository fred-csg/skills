---
name: criar-category-of-one
description: Transforma expertise, um Download Cerebral ou contexto estruturado de negócio em uma metodologia proprietária e uma proposta de Category of One, combinando categoria tradicional com um twist real do especialista, naming, mecanismos, pilares, framework, diferenciação, evidências e aplicação em produto. Use quando o usuário pedir Category of One, criação de categoria, metodologia única, framework proprietário, naming de método, transformação de conhecimento em ativo intelectual, posicionamento sem comparação direta ou execução dos prompts de Criador de Metodologia via Download Cerebral ou Contexto de Negócio.
---

# Criar Category of One

## Objetivo

Transformar conhecimento real em uma categoria que o mercado consiga entender, distinguir e testar. Tratar “Category of One” como estratégia de posicionamento, não como declaração automática de monopólio, superioridade ou exclusividade jurídica.

Usar como fórmula inicial:

```text
categoria reconhecível + twist demonstrável do especialista = candidata a nova categoria
```

## Diagnosticar a rota

Ler `references/input-contracts.md` e escolher uma rota:

- **Rota DC**: há Download Cerebral produzido pela `extrair-area-de-conhecimento` ou documento equivalente com método, decisões, casos, mecanismos, limites e evidências. Ler `references/workflow-dc.md`.
- **Rota Contexto**: não há DC, mas existe contexto de negócio suficiente sobre especialista, público, método atual, resultados e produto. Ler `references/workflow-context.md`.
- **Extração necessária**: não há material suficiente em nenhuma rota. Orientar o usuário a executar `extrair-area-de-conhecimento` ou responder ao briefing mínimo de `references/input-contracts.md`. Não criar uma categoria genérica para preencher o vazio.

Não exigir que o usuário repita informações já presentes na conversa ou nos anexos. Informar a rota escolhida, o que foi encontrado e quais lacunas impedem apenas a próxima fase.

## Trabalhar por checkpoints

1. Executar uma fase por vez.
2. Separar fatos, evidências, inferências, hipóteses e decisões de naming.
3. Entregar opções comparáveis, não uma escolha arbitrária.
4. Aplicar `references/category-design.md` ao criar a categoria e os nomes.
5. Aplicar `references/evidence-and-ip.md` antes de alegar ciência, superioridade, resultados ou registrabilidade.
6. Apresentar `Aprovar`, `Revisar`, `Aprofundar` ou `Pausar`.
7. Aguardar aprovação explícita antes de avançar.

Se o usuário pedir somente a Category of One, concluir a fase de categoria e naming sem forçar a criação do infoproduto inteiro. Se pedir a metodologia completa, executar toda a rota escolhida.

## Construir a categoria

Gerar de 5 a 10 territórios de categoria e reduzir para 3 finalistas. Para cada finalista, registrar:

- categoria de referência;
- twist real e sua origem no material;
- público e problema delimitados;
- mecanismo ou princípio diferenciador;
- definição em uma frase;
- o que inclui e exclui;
- alternativas contra as quais será comparada;
- evidência existente e evidência ainda necessária;
- risco de confusão, exagero, cópia e dependência de jargão;
- nome candidato e variações.

Não escolher nomes apenas por soarem técnicos. Um nome forte deve comprimir uma diferença operacional que possa ser explicada e entregue.

## Desenvolver a metodologia

Depois da categoria aprovada:

1. Identificar 3–7 mecanismos reais.
2. Organizar conhecimento em filosofia, estratégia, metodologia, técnicas e execução.
3. Criar 3–7 pilares com fronteiras claras e progressão justificável.
4. Definir critérios de entrada, passagem, conclusão, exceções e contraindicações.
5. Criar glossário, ferramentas, diagnósticos e métricas somente quando tiverem função operacional.
6. Produzir uma promessa condicionada ao público, contexto, esforço e evidência disponíveis.
7. Mapear aplicação em produto apenas se solicitada ou se fizer parte da rota completa.

Não inventar acrônimos, fórmulas ou percentuais apenas para parecer proprietário. Não nomear práticas comuns como exclusivas sem explicitar a síntese ou execução realmente diferente.

## Validar a diferenciação

Para análise de concorrentes, disponibilidade de nome, pesquisa científica ou qualquer dado que possa ter mudado, pesquisar fontes atuais. Em questões técnicas, usar fontes primárias e oficiais. Citar cada comparação perto da afirmação correspondente.

Se não houver acesso a pesquisa atual, marcar:

- comparação competitiva como `hipótese`;
- fundamento científico como `evidência pendente`;
- disponibilidade de nome como `não pesquisada`;
- registrabilidade como `revisão jurídica necessária`.

Nunca adicionar `®` sem registro confirmado na jurisdição pertinente. Não afirmar que um nome é registrável, protegido ou exclusivo sem busca oficial e análise profissional adequada.

## Produzir a entrega

Ler `references/output-template.md`. Entregar, conforme o escopo:

- tese da categoria;
- três finalistas e decisão aprovada;
- nome, definição, fronteiras e narrativa;
- metodologia, mecanismos, pilares e progressão;
- glossário e ativos operacionais;
- matriz competitiva baseada em fontes;
- matriz de alegações e evidências;
- testes de mensagem e validação de mercado;
- blueprint de produto, flash comercial ou roadmap somente quando solicitados.

Evitar metas artificiais de páginas. Priorizar uma metodologia utilizável e auditável.

## Validar o manifesto

Registrar o projeto conforme o exemplo em `references/output-template.md` e executar:

```powershell
python scripts/validate_methodology.py caminho\methodology-manifest.json
```

Não declarar a metodologia concluída se houver dependência não aprovada, alegação verificada sem fonte, símbolo de registro sem comprovação ou categoria sem twist rastreável.
