---
name: gestor-de-lancamento
description: Planeje, coordene, acompanhe, retome e audite lançamentos digitais de ponta a ponta, gerenciando escopo, fases, dependências, cronograma, responsáveis, decisões, riscos, evidências, alegações, handoffs, aprovações, métricas e próxima ação. Use quando o usuário quiser organizar várias skills de lançamento, criar um plano mestre, saber o que fazer agora, verificar prontidão, atualizar status, resolver bloqueios, replanejar datas, controlar mudanças ou conduzir um lançamento em execução sem refazer os artefatos especializados.
---

# Gestor de Lançamento

Operar como sistema de controle do projeto. Coordenar artefatos e skills especializadas sem substituir o trabalho delas. Manter uma fonte de verdade rastreável e recomendar a próxima ação com base em dependências, risco e data-alvo.

## Escolher o modo

- **Iniciar:** criar plano e manifesto a partir do contexto existente.
- **Diagnosticar:** inventariar arquivos e reconstruir o estado real.
- **Planejar:** definir escopo, trilhas, dependências, responsáveis, marcos e datas.
- **Acompanhar:** atualizar progresso, próximos trabalhos, bloqueios e decisões.
- **Retomar:** recuperar projeto pausado sem repetir entregáveis aprovados.
- **Replanejar:** avaliar impacto de mudança de data, escopo, oferta ou estratégia.
- **Auditar:** comparar manifesto, arquivos e aprovações; não alterar conteúdo especializado sem autorização.
- **Encerrar:** verificar prontidão, registrar resultados e retrospectiva.

## Aplicar princípios operacionais

1. Tratar os arquivos existentes como evidência; não presumir que uma fase está concluída pelo nome da pasta.
2. Não marcar tarefa como aprovada sem entregável, checkpoint e responsável pela aprovação.
3. Não iniciar tarefa cuja dependência obrigatória esteja pendente, salvo exploração explicitamente rotulada.
4. Distinguir fato, hipótese, decisão, risco, bloqueio e alegação comercial.
5. Não apagar histórico ao replanejar; registrar mudança, razão, impacto e autor.
6. Não transformar estimativa em compromisso sem responsável e data.
7. Não inventar progresso, métricas, fontes, proprietários ou aprovações.
8. Preservar IDs estáveis mesmo quando nomes e datas mudarem.
9. Manter uma única fonte de verdade; relatórios derivados não podem contradizer o manifesto.
10. Recomendar no máximo três próximas ações priorizadas.

## Inicializar ou recuperar o projeto

Ler [modelo-operacional.md](references/modelo-operacional.md) e [esquema-do-projeto.md](references/esquema-do-projeto.md).

Ao iniciar:

1. Inventariar materiais fornecidos e skills disponíveis.
2. Definir tipo de lançamento, produto, público, data-alvo, dono e restrições.
3. Selecionar apenas as trilhas necessárias.
4. Copiar [project-template.json](assets/project-template.json) para `_lancamento/project.json` e adaptar sem remover o histórico necessário.
5. Criar os artefatos administrativos descritos em [templates-operacionais.md](references/templates-operacionais.md).
6. Executar o validador antes do primeiro checkpoint.

Ao recuperar:

1. Ler o manifesto e todos os arquivos apontados por `inputs` e `outputs`.
2. Comparar estado declarado com estado físico.
3. Marcar divergências; não aprovar automaticamente.
4. Reconstruir decisões, bloqueios e próximos passos a partir da evidência.
5. Pedir confirmação apenas para conflitos que não possam ser resolvidos pelos arquivos.

## Planejar o trabalho

Ler [planejamento-e-cronograma.md](references/planejamento-e-cronograma.md) e [roteamento-de-skills.md](references/roteamento-de-skills.md).

Para cada tarefa registrar:

- ID e trilha;
- objetivo e entregável verificável;
- skill recomendada;
- dependências;
- responsável e aprovador;
- prioridade, esforço e data;
- entradas e saídas;
- gate de qualidade;
- riscos, bloqueios e próxima ação.

Planejar de trás para frente a partir da data-alvo. Paralelizar apenas tarefas sem dependência causal e com capacidade disponível. Incluir folga para revisão, aprovação, contingência e correção técnica.

## Rotear sem duplicar

Usar `construir-lancamento-completo-pro` para desenhar ou integrar a estratégia completa. Usar as skills especializadas para produzir ou revisar seus artefatos. Usar esta skill para decidir ordem, estado, handoff, agenda e prontidão.

Quando a skill indicada não estiver disponível, registrar o contrato do entregável e marcar `skill` como `manual` ou `external`; não fingir que o trabalho foi executado.

## Atualizar o projeto após cada trabalho

1. Verificar o entregável físico.
2. Registrar caminho, versão e data.
3. Atualizar tarefa para `review`, nunca diretamente para `approved` sem checkpoint.
4. Aplicar gate e registrar achados.
5. Obter decisão: aprovar, pedir mudanças, pausar ou cancelar.
6. Registrar decisão e impacto.
7. Recalcular tarefas liberadas, marcos, riscos e caminho crítico.
8. Atualizar `status.md` e recomendar próximas ações.

Ler [gates-e-handoffs.md](references/gates-e-handoffs.md) para validar interfaces entre skills.

## Gerenciar mudanças e execução

Ler [mudancas-riscos-e-monitoramento.md](references/mudancas-riscos-e-monitoramento.md).

Para qualquer mudança material:

1. registrar solicitação;
2. identificar artefatos e tarefas afetados;
3. avaliar prazo, custo, evidência, qualidade e mensagem;
4. propor manter, absorver, trocar ou adiar;
5. obter decisão;
6. versionar artefatos e reabrir gates afetados;
7. comunicar handoffs.

Não reabrir toda a campanha quando uma mudança tiver impacto localizado.

## Validar e obter status

Executar:

```powershell
python scripts/manage_launch.py validate caminho\project.json
python scripts/manage_launch.py status caminho\project.json
```

Corrigir erros antes de recomendar execução. Tratar avisos como itens de decisão, não como falhas automáticas.

## Responder ao usuário

Usar esta ordem:

1. **Estado:** fase, saúde, data-alvo e confiança do diagnóstico.
2. **Concluído:** entregáveis aprovados desde a última atualização.
3. **Em andamento:** responsável, prazo e critério de saída.
4. **Bloqueios e riscos:** impacto e ação de mitigação.
5. **Próximas ações:** até três, em ordem, com skill e entrada necessária.
6. **Decisões:** escolhas que exigem confirmação humana.
7. **Manifesto:** arquivos atualizados e resultado da validação.

Não produzir longos artefatos criativos durante uma atualização de gestão. Encaminhar o trabalho à skill especializada e definir o contrato de handoff.

## Encerrar

Antes de declarar o lançamento pronto ou concluído:

- confirmar gates obrigatórios;
- verificar alegações, links, automações, capacidade e contingências;
- confirmar responsáveis e janela de operação;
- registrar baseline e plano de medição;
- separar “pronto para lançar” de “resultado alcançado”;
- após a campanha, consolidar métricas, aprendizados, decisões e itens reutilizáveis.
